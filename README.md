# ray-streamer: Multiprocess data from a streaming API with ray.io

## Purpose
Imagine you need to stream rapidly changing data from a 3rd party API.

This could be many thing, but this example has been created with intraday stock market data in mind: For each stock symbol you subscribe to, you might receive latest period price action (OHLCV), Level1, Level2, Time and Sales, News, etc.

The more data you are getting with each call, and the faster the API churns it out, can cause several headaches if you are processing it on a single-thread (such as a typical Python application):

- Each collection of data will be processed, in turn, resulting in any transformations / analysis being slower than if you could spread that processing out to multiple workers across multiple processors.
- It's likely that your application won't be making the next call to a 3rd party API, until all latest transformations / analysis is complete. This can easily result in the server timing out your connection. That's bad! Especially for something like a trading app.