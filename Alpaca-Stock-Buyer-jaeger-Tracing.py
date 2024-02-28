package alpacabuy;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.trace.samplers.Sampler;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
public class alpacabuy {
	privatestatic final String ALPACA_API_KEY = "PKBAIZAFKXUNUQ8CAP27";
	}
privatestatic final String ALPACA_SECRET_KEY = "yF4rZ6K3EjGhwDhNiRo3pw8hnwV4SZ58bhBegFiN";
privatestatic final String ALPACA_BASE_URL = "https://paper-api.alpaca.markets"; // Use 'https://api.alpaca.markets' for live trading
privatestatic final HttpClient httpClient = HttpClients.createDefault();
privatestatic final ObjectMapper objectMapper = new ObjectMapper();
publicstatic JsonNode retrieveStockInfo(String symbol) throws IOException {
	String apiUrl = ALPACA_BASE_URL + "/v2/assets/" + symbol;
	HttpGet request = new HttpGet(apiUrl);
	request.setHeader("APCA-API-KEY-ID", ALPACA_API_KEY);
	request.setHeader("APCA-API-SECRET-KEY", ALPACA_SECRET_KEY);
	HttpResponse response = httpClient.execute(request);
	String json = EntityUtils.toString(response.getEntity());
	returnobjectMapper.readTree(json);
	}
publicstatic void main(String[] args) throws IOException {
	System.out.println("Alpaca API Console Application - Buy Stocks");
	// Create an OTLP gRPC exporter for Jaeger
	OtlpGrpcSpanExporter jaegerExporter = OtlpGrpcSpanExporter.builder()
			.setEndpoint("http://13.53.39.127:4317") // Include http:// or https:// protocol
			.build();
	Resource resource = Resource.create(Attributes.of(AttributeKey.stringKey("service.name"), "HomeService"));
	// Create a tracer provider with samplers and exporters for tracing
	SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
			.setSampler(Sampler.alwaysOn())
			.setResource(resource)
			.addSpanProcessor(BatchSpanProcessor.builder(jaegerExporter).build())
			.build();
	// Build and register the global OpenTelemetry instance for tracing
	OpenTelemetrySdk.builder()
	.setTracerProvider(tracerProvider)
	.buildAndRegisterGlobal();
	OpenTelemetry openTelemetry = GlobalOpenTelemetry.get();
	while (true) {
		try {
			System.out.print("\nEnter a stock symbol (e.g., AAPL): ");
			BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
			String symbol = reader.readLine();
			if (symbol.equalsIgnoreCase("EXIT")) {
				System.out.println("Exiting...");
				break;
				}
			// Start a new span for this operation
			Tracer tracer = openTelemetry.getTracer("AlpacaAPIService");
			Span span = tracer.spanBuilder("Retrieve Stock Info").startSpan();
			span.setAttribute("symbol", symbol);
			// Simulate some work
			Thread.sleep(100);
			JsonNode stockInfo = retrieveStockInfo(symbol);
			// Add more span attributes based on the stock information
			if (stockInfo.has("symbol")) {
				span.setAttribute("name", stockInfo.get("name").asText());
				span.setAttribute("exchange", stockInfo.get("exchange").asText());
				span.setAttribute("tradable", stockInfo.get("tradable").asBoolean());
				span.setAttribute("status", stockInfo.get("status").asText());
				} else {
					span.setAttribute("error", "Stock symbol not found or an error occurred");
					}
			// End the span
			span.end();
			} catch (Exception e) {
				System.out.println("Error: " + e.getMessage());
				}
		}
	}
