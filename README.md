# Stock Market Application Microservice - Buying Stocks

This repository is dedicated to a microservice within our Stock Market Application, focused on enabling users to purchase stocks using the Alpaca API. It also implements Jaeger tracing for comprehensive monitoring and debugging. The repository is organized into three branches, each addressing specific aspects of this microservice.

## Branch 1
**Buying Stocks from Alpaca API:** 

This branch contains code to facilitate stock purchases through the Alpaca API, providing stock information retrieval and buy order placement.

## Branch 2
**Tracing Code for Buying Stocks:** 

Here, Jaeger tracing is introduced into the codebase, allowing for the creation and management of spans to trace and monitor stock buying operations.

## Branch 3
**Tracing Alpaca Buy Stocks and Delayed Integration:** 

The final branch showcases complex use cases by invoking another microservice, "Order History," with deliberate delays. This code provides an end-to-end view of the process, including time measurement.

## Usage

To use this microservice, follow these steps:
1. Clone the repository.
2. Select the branch corresponding to your needs (Branch 1, 2, or 3).
3. Build and deploy the code as required for your application or environment.
4. Ensure you have the necessary Alpaca API keys.
5. Run the microservice and follow the provided instructions for stock purchasing or tracing.
