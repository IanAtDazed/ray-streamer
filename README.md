# ray-streamer: Multiprocess data from a streaming API with ray.io

# Why?
Imagine you need to stream data, rapidly changing data from an API.

This could be many thing, but I created this with intraday stock market data in mind: For each stock symbol you subscribe to, you might receive latest period price action (OHLCV), Level1, Level2, Time and Sales, etc.

The more data you are getting, and the faster it comes in, can cause several headaches if you are processing it on a single-thread, such as a typical Python application:

- Each collection of data will be processed, in turn, resulting in any analysis being slower than if you could spread the analysis out.
- It's likely that your application won't be making the next call to a 3rd party API, until the above is complete. This can result in the server timing out your connection. That's bad!