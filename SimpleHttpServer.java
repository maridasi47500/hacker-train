import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        // Create an HTTP server listening on port 8000
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        
        // Define a context for the root path
        server.createContext("/", new RootHandler());
        
        // Start the server
        server.start();
        System.out.println("Server is listening on port 8000");
    }

    static class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // Read HTML content from the file
            String response = new String(Files.readAllBytes(Paths.get("index.html")));
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
