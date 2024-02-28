# AlpacaStockBuyer
# Alpaca Buy Order History Lambda

The Alpaca Buy Order History Lambda is a serverless function deployed on AWS Lambda. It allows you to place buy orders for stocks and retrieve order history by invoking other AWS Lambda functions through API Gateway. The function is instrumented with OpenTelemetry for distributed tracing, allowing you to monitor and trace the execution of your code. Here's a detailed explanation of this Lambda function:

## Purpose

The purpose of this Lambda function is to handle stock buying requests and retrieve order history. It receives requests with a specific stock symbol and quantity, places a buy order, and then invokes another Lambda function to retrieve the order history.

## Components

1. **Handler Function**: The `handleRequest` function is the entry point of the Lambda function. It accepts a `Map` representing the input, which typically contains a stock symbol and quantity. It also receives a `Context` object. Inside this function, it does the following:

   - Extracts the stock symbol and quantity from the input.
   - Initializes OpenTelemetry and creates a new span for the operation.
   - Calls the `placeStockOrder` function to place a buy order and records the order response.
   - Invokes the `invokeOrderHistoryLambda` function to retrieve order history and measures the time delay.
   - Ends the span and returns the order response or an error message.

2. **Instrumentation with OpenTelemetry**: The function uses OpenTelemetry to instrument the code for distributed tracing. It creates spans to trace the execution of different operations and records various attributes, such as HTTP method, URL, status code, and timing information.

3. **Place Stock Order**: The `placeStockOrder` function is responsible for placing a buy order for a stock. It makes an HTTP POST request to the Alpaca API to execute the order. The span for this function records details of the HTTP request, including the URL, method, and response.

4. **Invoke Order History Lambda**: The `invokeOrderHistoryLambda` function invokes another AWS Lambda function through an API Gateway endpoint. It measures the time delay between the request and response, which can be useful for performance monitoring.

## API Gateway Integration

This Lambda function is integrated with API Gateway to expose an HTTP endpoint. The API Gateway URL (defined as `API_GATEWAY_ENDPOINT`) is used to invoke this Lambda function remotely. When an HTTP request is made to this endpoint, the Lambda function processes the request, interacts with the Alpaca API, and invokes the order history Lambda function.

## How it Works
1.The Lambda function is triggered by an API Gateway request, which passes data including the stock symbol and quantity.

2.The function starts a tracing span using OpenTelemetry, capturing information about the stock buying operation.

3.It then sends an HTTP POST request to the Alpaca API to place the stock order. This is done within the context of the tracing span, and relevant information about the request and response is recorded as attributes of the span.

4.After placing the order, the function introduces a 20-second delay to simulate a time-consuming operation. This delay is represented as a separate span within the trace.

5.The Lambda function captures and logs the response from the order history service.

6.The tracing span for the stock buying operation is ended, and the trace data is exported to the Jaeger instance.

7.The function returns the response from the stock buying operation to the API Gateway, and the result is sent as a response to the client.

## Distributed Tracing

The Lambda function is instrumented with OpenTelemetry and exports traces to a Jaeger instance for distributed tracing. This allows you to monitor the flow and performance of the code and identify any issues or bottlenecks.

## Conclusion

The Alpaca Buy Order History Lambda is a serverless function that extends the functionality of placing buy orders by also retrieving order history through an AWS Lambda function. It provides tracing capabilities for performance monitoring and debugging. This Lambda function can be part of a broader serverless architecture for stock trading or other related applications. Make sure to secure your AWS Lambda functions and endpoints and handle exceptions and errors gracefully.
