# ray-streamer: Parallel processing data from a streaming API with Ray

I created this concept application to *hopefully* help others and to garner constructive feedback on how it might be improved.

## The Problem
Imagine you need to stream rapidly changing data from a 3rd party API.

This could be many scenarios, but this example has been created with intraday stock market data in mind: For each stock symbol you subscribe to, you might receive latest period price data (OHLCV), Level1, Level2, Time and Sales, News, etc.

The more data you are getting, with each call, and the faster the API churns it out, the more headaches you can experience when you are processing it on a single-thread (such as a typical Python application - even if you are using a blazing fast DataFrame, such as [Polars](https://pola.rs/).)

The main problems being:

- Each collection of data will be processed, in turn, resulting in any transformations / analysis being potentially slower than if you could spread that processing out to multiple *Worker*s across multiple processors.
- It's likely that your application won't be making the next call to the 3rd party API until all the latest transformations / analysis is complete. This can easily result in the server timing out your connection. That's bad! Especially for something like a trading app.

## This Solution
This solution employs multiprocessing with [Ray](https://www.ray.io/) (which I find easier to work with than the Python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), and it is apparently [faster](https://towardsdatascience.com/10x-faster-parallel-python-without-python-multiprocessing-e5017c93cce1).)

However, I struggled to find an existing [Ray](https://www.ray.io/) solution for streaming that truly fitted my needs. The closest I could find was: [Serve a Chatbot with Request and Response Streaming](https://docs.ray.io/en/latest/serve/tutorials/streaming.html), but a chatbot seems very different to data that might require significant processing before an application can move onto the next API call.

So... This is my *solution*. (Let me know if you do or don't agree to the *solution* part! :smiley:)

## High-Level Overview
This is basically what things look like when it is running:
![High Level Activity Diagram](images/high_level_activity.png)
- Streaming takes place, on it's own process, and dumps the raw results onto a Ray *processing* [Queue](ray.util.queue.Queue).
  - The streamer is not waiting for current transformations, analysis, etc. to complete before it can make the next API call.
  - The 3rd party API is not having to wait for an extended period for the next API call, so it *hopefully* won't time out the connection. (Nothing is ever certain with a 3rd party!)
  - It will carry on grabbing data, regardless of whatever else your application is doing.
- The latest streamed data is grabbed from the *processing* queue and sent to individual *Worker* objects that are created to deal with data belonging to specific *labels*.
  - In this example, a *label* is a stock symbol, and a *Worker* is created for each symbol that has been subscribed to.
  - The *Worker* processes each latest period (OHLCV) as it receives that data.
  - **Note:** The latest data is actually sent to *all* the *Workers*, but they simply ignore data that is not for them.
    - This should typically be faster than deciding which *Worker* specific data should be sent to.
- Once the *Worker* has completed its transformation / analysis / whatever clever stuff you want to do, it puts its latest result onto a *results* queue.
- An *Administrator* object fetches the latest result from the *results* queue in order to do whatever is required with it, after that.
  - In this case, it simply prints it to the console.
  - In other scenarios, it might hand it to a callback function of a single-threaded GUI, etc. (I intend to create a simple repo that demonstartes this with PyQt6, sometime in the future.)

## Potential Enhancements
### *Worker* (*SymbolWorker*)
- In the code example, it simply grabs some intraday stock price data, from a *fake* streamer, and peforms minimal processing of it directly in the *SymbolWorker* object.
- However, supposing data is coming in for: OHLCV, Level1, Level2, Time and Sales, News, etc.?
- In such a case, *SymbolWorker* could be composed of classes to specifically hold each data-type's state and to perform specific processing upon it, e.g.:
![SymbolWorker Composite Class Diagram](images/symbol_worker_composite_class.png)

Imagine data comes in looking something like this:
'''
{
  'timestamp:': 1665427314480,
  'service': 'TIMESALE',
  'symbols': {
    'AAPL': {..}
    'TSLA': {..}
}
'''

*SymbolWorker* could easily be adapted to process it with the appropriate composite object.

### General
- This is very much a proof of concept, that would need to be amended for specific requirements.
- I am sure there are many ways to improve it - please let me know if you can suggest some! :smiley: