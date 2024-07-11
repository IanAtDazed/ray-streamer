# ray-streamer: Multiprocess data from a streaming API with ray.io

## The Problem
Imagine you need to stream rapidly changing data from a 3rd party API.

This could be many scenarios, but this example has been created with intraday stock market data in mind: For each stock symbol you subscribe to, you might receive latest period price data (OHLCV), Level1, Level2, Time and Sales, News, etc.

The more data you are getting, with each call, and the faster the API churns it out, the more headaches you can experience when you are processing it on a single-thread (such as a typical Python application. Even if you are using a blazing fast DataFrame, such as [Polars](https://pola.rs/)):

- Each collection of data will be processed, in turn, resulting in any transformations / analysis being potentially slower than if you could spread that processing out to multiple workers across multiple processors.
- It's likely that your application won't be making the next call to a 3rd party API until all latest transformations / analysis is complete. This can easily result in the server timing out your connection. That's bad! Especially for something like a trading app.

## This Solution
This solution employs multiprocessing with [ray.io](https://www.ray.io/) (because I find it easier to work with than the Python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), and it is apparently faster. :smiley:)

However, I struggled to find an existing [ray.io](https://www.ray.io/) solution for streaming that truly fitted my needs. The closest I could find was: [Serve a Chatbot with Request and Response Streaming](https://docs.ray.io/en/latest/serve/tutorials/streaming.html), but a chatbot seems very different to data that might require significant processing before an application can move onto the next API call.

So... This is a *solution* (Let me know if you do or don't agree!)