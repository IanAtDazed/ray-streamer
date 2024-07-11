"""The *main* module that allows us to kick off the application.

**NOTE:**
- Because this application fakes its streamed data,
  the symols in *STREAM_SYMBOLS* will make no difference to
  what is streamed.
- They **WILL** make a difference to what is processed.
- Currently, you will get messages for APPL & AMZN, but nothing for DUD
  as there is no fake streamed data created for it. You can make some!
  - This demonstrates a situation, where you are streaming a
    symbol with no current price action.
"""

from actors.administrator import Administrator

if __name__ == '__main__':

    STREAM_SYMBOLS = ('AAPL', 'DUD', 'AMZN')

    print('Running... Press Ctrl-C to stop.')

    administrator = Administrator(STREAM_SYMBOLS)

    while True:
        pass
