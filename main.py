"""The *main* module that allows us to kick off the application."""

from actors.administrator import Administrator

if __name__ == '__main__':

    STREAM_SYMBOLS = ('AAPL', 'TSLA', 'AMZN')
    
    administrator = Administrator(STREAM_SYMBOLS)

    while True:
        pass