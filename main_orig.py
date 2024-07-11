import ray
from ray.util.queue import Queue

import time

@ray.remote
class ProductionSupervisor:
    '''Fake data stream
    IRL: Streams complex (badly structured) JSON from a 3rd party API.
    Each message contains data for separate subjects'''

    def __init__(self, stream_msg_queue):

        self._stream_msg_queue = stream_msg_queue

        self._cnt = -1
        self._msg_txt = 'msg_'
    
    def gen_msgs(self):

        while True:
            time.sleep(1)
            
            self._cnt += 1

            # Serialize the message
            ser_msg = ray.put(f'{self._msg_txt}{self._cnt}')
            
            # Put the serialized message on the stream msg queue
            # NOTE: Wrap in brackets, so it will remain serialized
            # when a queue.get is performed on it
            self._stream_msg_queue.put([ser_msg])

@ray.remote
class ConsumptionSupervisor:
    '''Distribute each newly received message
    to ALL workers.'''

    def __init__(self, _stream_msg_queue):

        self._stream_msg_queue = _stream_msg_queue
        self._workers = [Worker.remote(id_val) for id_val in range(3)]

    def process_msgs(self):
        
        while True:
            # Get the message from the queue
            ser_msg = self._stream_msg_queue.get()

            # Pass the message to all workers
            for worker in self._workers:
                
                worker.work.remote(ser_msg)

@ray.remote
class Worker:
    '''IRL: each worker represents a specific subject; Extracts
    the relevant data, from the passed in message dict,
    processes it, and stores it here'''

    def __init__(self, worker_id: int) -> None:
        
        self._worker_id = worker_id
    
    def work(self, ser_msg):

        # Unserialize the message
        wrapped_msg = ray.get(ser_msg)

        # Unwrap the message
        msg = wrapped_msg[0]

        # Output
        output_msg = f'From Worker {self._worker_id}: {msg}'
        print(output_msg)

if __name__ == '__main__':

    ray.init()

    stream_msg_queue = Queue()
    
    producer = ProductionSupervisor.remote(stream_msg_queue)
    consumer = ConsumptionSupervisor.remote(stream_msg_queue)

    producer.gen_msgs.remote()
    consumer.process_msgs.remote()

    while True:
        pass