# anthropic-sdk-java

Use the Anthropic Java SDK (`com.anthropic:anthropic-java`) to build Java applications on top of the Claude API.

## Overview

Official Java SDK for Claude. Java 8+ compatible. Multi-module Gradle project. Provides sync and async clients, streaming, tool use (manual and automatic), structured outputs, batch processing, managed agents, and Skills API access.

**Maven coordinates:** `com.anthropic:anthropic-java:2.64.0`
**Gradle:** `implementation("com.anthropic:anthropic-java:2.64.0")`

All parameter objects use a fluent `.builder()...build()` pattern. All response types expose typed getters.

---

## Module structure

| Module | Purpose |
|--------|---------|
| `anthropic-java` | Umbrella — re-exports everything; add this to your deps |
| `anthropic-java-core` | Core models, types, request/response classes |
| `anthropic-java-client-okhttp` | Sync + async HTTP clients (OkHttp) |
| `anthropic-java-example` | Runnable examples |
| `anthropic-java-aws` / `anthropic-java-bedrock` | AWS Bedrock client |
| `anthropic-java-vertex` | Google Vertex AI client |
| `anthropic-java-google-cloud` | Google Cloud client |
| `anthropic-java-foundry` | Azure Foundry client |
| `anthropic-java-mcp` | MCP integration helpers |

---

## Client setup

### Sync client

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;

// From ANTHROPIC_API_KEY env var
AnthropicClient client = AnthropicOkHttpClient.fromEnv();

// Explicit key
AnthropicClient client = AnthropicOkHttpClient.builder()
        .apiKey("sk-ant-...")
        .build();
```

### Async client

```java
import com.anthropic.client.AnthropicClientAsync;
import com.anthropic.client.okhttp.AnthropicOkHttpClientAsync;

AnthropicClientAsync client = AnthropicOkHttpClientAsync.fromEnv();
```

Async methods return `CompletableFuture<T>`. Chain with `.thenAccept()`, `.thenApply()`, `.join()`.

### Builder with custom configuration

```java
AnthropicClient client = AnthropicOkHttpClient.builder()
        .fromEnv()
        .addInterceptor(myInterceptor)
        .build();
```

---

## Messages API

### Basic sync request

```java
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(2048)
        .addUserMessage("Tell me a story about building the best SDK!")
        .build();

client.messages().create(createParams).content().stream()
        .flatMap(contentBlock -> contentBlock.text().stream())
        .forEach(textBlock -> System.out.println(textBlock.text()));
```

### Async request

```java
import com.anthropic.client.AnthropicClientAsync;
import com.anthropic.client.okhttp.AnthropicOkHttpClientAsync;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

AnthropicClientAsync client = AnthropicOkHttpClientAsync.fromEnv();

MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(2048)
        .addUserMessage("Tell me a story about building the best SDK!")
        .build();

client.messages().create(createParams)
        .thenAccept(message -> message.content().stream()
                .flatMap(b -> b.text().stream())
                .forEach(t -> System.out.println(t.text())))
        .join();
```

### Streaming

```java
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.messages.RawMessageStreamEvent;

try (StreamResponse<RawMessageStreamEvent> streamResponse =
        client.messages().createStreaming(createParams)) {
    streamResponse.stream()
            .flatMap(event -> event.contentBlockDelta().stream())
            .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
            .forEach(textDelta -> System.out.print(textDelta.text()));
}
```

`StreamResponse` implements `Closeable`. Always use try-with-resources to ensure the connection is closed.

### Streaming (async)

```java
import com.anthropic.core.http.AsyncStreamResponse;

client.messages().createStreaming(createParams)
        .subscribe(event -> event.contentBlockDelta()
                .flatMap(d -> d.delta().text())
                .ifPresent(t -> System.out.print(t.text())))
        .onCompleteFuture()
        .join();
```

### System prompt

```java
MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(1024)
        .system("You are a helpful assistant.")
        .addUserMessage("Hello")
        .build();
```

### Multi-turn conversation

Keep a builder alive across turns to append messages:

```java
MessageCreateParams.Builder builder = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(2048)
        .addUserMessage("Tell me a story about building the best SDK!");

for (int i = 0; i < 4; i++) {
    // .build() produces an immutable snapshot; builder continues to accumulate
    Message message = client.messages().create(builder.build());
    message.content().stream()
            .flatMap(b -> b.text().stream())
            .forEach(t -> System.out.println(t.text()));

    builder.addMessage(message).addUserMessage("But why?" + "?".repeat(i));
}
```

### Image input (base64)

```java
import com.anthropic.models.messages.*;
import java.util.Base64;
import java.util.List;

byte[] imageBytes = /* load image bytes */;
String base64 = Base64.getEncoder().encodeToString(imageBytes);

ContentBlockParam imageParam = ContentBlockParam.ofImage(
        ImageBlockParam.builder()
                .source(Base64ImageSource.builder()
                        .mediaType(Base64ImageSource.MediaType.IMAGE_PNG)
                        .data(base64)
                        .build())
                .build());

MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .addUserMessage("Describe this image.")
        .addUserMessageOfBlockParams(List.of(imageParam))
        .maxTokens(2048)
        .build();
```

### Count tokens

```java
import com.anthropic.models.messages.MessageCountTokensParams;

MessageCountTokensParams countParams = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .addUserMessage("Tell me a story about building the best SDK!")
        .build();

long inputTokens = client.messages().countTokens(countParams).inputTokens();
```

---

## Thinking / Extended reasoning

```java
import com.anthropic.models.messages.*;

MessageCreateParams createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(16000)
        .thinking(ThinkingConfigAdaptive.builder()
                .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
                .build())
        .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.HIGH)
                .build())
        .addUserMessage("Create a haiku about Anthropic. Think carefully about syllable counts.")
        .build();

for (ContentBlock block : client.messages().create(createParams).content()) {
    if (block.isThinking()) {
        System.out.println("Thinking: " + block.asThinking().thinking());
    } else if (block.isText()) {
        System.out.println("Text: " + block.asText().text());
    }
}
```

`ThinkingConfigAdaptive.Display` options: `SUMMARIZED`, `NONE`.
`OutputConfig.Effort` options: `LOW`, `MEDIUM`, `HIGH`.

---

## Structured outputs (GA — non-beta)

Structured outputs are generally available on the standard `client.messages()` API. No beta header required.

### Simple: pass a class directly

`outputConfig(Class<T>)` derives the JSON schema from the class and returns `StructuredMessageCreateParams<T>`.

```java
import com.anthropic.models.messages.*;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import java.util.List;

static class Book {
    public String title;
    public String author;
    @JsonPropertyDescription("Four-digit year published")
    public int year;
}

static class BookList {
    @ArraySchema(minItems = 1)
    public List<Book> books;
}

StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(2048)
        .outputConfig(BookList.class)
        .addUserMessage("List some famous late twentieth century novels.")
        .build();

client.messages().create(createParams).content().stream()
        .flatMap(b -> b.text().stream())
        .flatMap(t -> t.text().books.stream())
        .forEach(book -> System.out.println(book.title));
```

### Advanced: `StructuredOutputConfig` (set effort + format together)

```java
import com.anthropic.models.messages.StructuredOutputConfig;

StructuredOutputConfig<BookList> outputConfig = StructuredOutputConfig.<BookList>builder()
        .effort(OutputConfig.Effort.HIGH)
        .format(BookList.class)
        .build();

StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
        .model(Model.CLAUDE_SONNET_5)
        .maxTokens(2048)
        .outputConfig(outputConfig)
        .addUserMessage("List some famous late twentieth century novels.")
        .build();
```

**Schema annotations:** use `@JsonPropertyDescription` for property descriptions, `@ArraySchema(minItems = N)` for array constraints, `@JsonClassDescription` for class-level descriptions.

---

## Tool use

### Automatic tool runner (recommended)

Define tools as POJOs with Jackson annotations implementing `Supplier<String>`. The SDK handles the agentic loop automatically.

```java
import com.anthropic.helpers.BetaToolRunner;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import java.util.function.Supplier;

@JsonClassDescription("Get the weather in a given location")
static class GetWeather implements Supplier<String> {
    @JsonPropertyDescription("The city and state, e.g. San Francisco, CA")
    public String location;

    @Override
    public String get() {
        return "The weather in " + location + " is foggy and 60°F";
    }
}

BetaToolRunner toolRunner = client.beta()
        .messages()
        .toolRunner(MessageCreateParams.builder()
                .model("claude-sonnet-5")
                .putAdditionalHeader("anthropic-beta", "structured-outputs-2025-11-13")
                .maxTokens(1000)
                .addUserMessage("What is the weather in San Francisco?")
                .addTool(GetWeather.class)
                .build());

for (BetaMessage message : toolRunner) {
    System.out.println(message);
}
```

### Streaming tool runner

```java
import com.anthropic.core.http.StreamResponse;
import com.anthropic.models.beta.messages.BetaRawMessageStreamEvent;

for (StreamResponse<BetaRawMessageStreamEvent> streamResponse : toolRunner.streaming()) {
    try (streamResponse) {
        streamResponse.stream()
                .flatMap(e -> e.contentBlockDelta().stream())
                .flatMap(d -> d.delta().text().stream())
                .forEach(t -> System.out.print(t.text()));
    }
}
```

### Manual tool use loop (beta messages)

For full control over the tool use loop:

```java
import com.anthropic.models.beta.messages.*;
import java.util.List;

MessageCreateParams.Builder createParamsBuilder = MessageCreateParams.builder()
        .model("claude-sonnet-5")
        .putAdditionalHeader("anthropic-beta", "structured-outputs-2025-11-13")
        .maxTokens(2048)
        .addTool(GetWeather.class)  // registers the tool schema
        .addUserMessage("What's the temperature in New York?");

// First call: detect tool use
client.beta().messages().create(createParamsBuilder.build()).content().stream()
        .flatMap(b -> b.toolUse().stream())
        .forEach(toolUseBlock -> createParamsBuilder
                // Append assistant's tool-use turn
                .addAssistantMessageOfBetaContentBlockParams(
                        List.of(BetaContentBlockParam.ofToolUse(
                                BetaToolUseBlockParam.builder()
                                        .name(toolUseBlock.name())
                                        .id(toolUseBlock.id())
                                        .input(toolUseBlock._input())
                                        .build())))
                // Append tool result
                .addUserMessageOfBetaContentBlockParams(
                        List.of(BetaContentBlockParam.ofToolResult(
                                BetaToolResultBlockParam.builder()
                                        .toolUseId(toolUseBlock.id())
                                        .contentAsJson(callTool(toolUseBlock))
                                        .build()))));

// Second call: get final answer
client.beta().messages().create(createParamsBuilder.build()).content().stream()
        .flatMap(b -> b.text().stream())
        .forEach(t -> System.out.println(t.text()));

// Deserialize tool input:
static Object callTool(BetaToolUseBlock block) {
    GetWeather tool = block.input(GetWeather.class);
    return tool != null ? tool.execute() : new Weather("unknown");
}
```

### MCP tool runner

Connect to a remote MCP server and run its tools through the tool runner:

```java
import com.anthropic.helpers.McpBetaTool;
import com.anthropic.mcp.BetaMcp;
import io.modelcontextprotocol.client.McpClient;
import io.modelcontextprotocol.client.McpSyncClient;
import io.modelcontextprotocol.client.transport.HttpClientStreamableHttpTransport;

HttpClientStreamableHttpTransport transport = HttpClientStreamableHttpTransport
        .builder("https://api.githubcopilot.com/mcp/")
        .jsonMapper(McpJsonDefaults.getMapper())
        .customizeRequest(req -> req.header("Authorization", "Bearer " + token))
        .supportedProtocolVersions(List.of("2025-03-26"))
        .build();

try (McpSyncClient mcpClient = McpClient.sync(transport)
        .clientInfo(new McpSchema.Implementation("my-app", "1.0.0"))
        .build()) {

    mcpClient.initialize();
    List<McpBetaTool> betaTools = BetaMcp.mcpTools(mcpClient.listTools().tools(), mcpClient);

    MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_SONNET_5)
            .maxTokens(1024)
            .addUserMessage("List the 5 most recently opened issues in org/repo.")
            .addTools(betaTools)
            .build();

    BetaToolRunner runner = anthropic.beta().messages().toolRunner(params);
    for (BetaMessage message : runner) {
        System.out.println(message);
    }
}
```

---

## Fallbacks

When a model refuses a request, fall back to another model automatically.

### Server-side fallbacks (preferred)

```java
import com.anthropic.models.beta.messages.BetaFallbackParam;
import com.anthropic.models.beta.AnthropicBeta;

BetaMessage served = client.beta().messages().create(
        MessageCreateParams.builder()
                .model(Model.CLAUDE_FABLE_5)
                .maxTokens(1024)
                .addUserMessage("Some prompt that triggers a refusal")
                .fallbacksOfFallbackParams(List.of(
                        BetaFallbackParam.builder().model(Model.CLAUDE_OPUS_4_8).build()))
                .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
                .build());

System.out.println("served by: " + served.model().asString());
```

### Client-side fallbacks (for providers that don't support server-side)

```java
import com.anthropic.helpers.BetaFallbackState;
import com.anthropic.helpers.BetaMessageAccumulator;
import com.anthropic.helpers.BetaRefusalFallbackInterceptor;
import com.anthropic.core.RequestOptions;

AnthropicClient fallbackClient = AnthropicOkHttpClient.builder()
        .fromEnv()
        .addInterceptor(BetaRefusalFallbackInterceptor.builder()
                .addFallback(Model.CLAUDE_OPUS_4_8)
                .build())
        .build();

// state pins follow-ups to the model that accepted
BetaFallbackState state = BetaFallbackState.create();

// Streaming fallback
BetaMessageAccumulator accumulator = BetaMessageAccumulator.create();
try (StreamResponse<BetaRawMessageStreamEvent> streamResponse = fallbackClient
        .beta().messages()
        .createStreaming(createParams,
                RequestOptions.builder().fallbackState(state).build())) {
    streamResponse.stream()
            .peek(accumulator::accumulate)
            .forEach(event -> {
                event.contentBlockDelta()
                        .flatMap(d -> d.delta().text())
                        .ifPresent(t -> System.out.print(t.text()));
                event.contentBlockStart()
                        .flatMap(s -> s.contentBlock().fallback())
                        .ifPresent(f -> System.out.println(
                                "\nfell back: " + f.from().model().asString()
                                        + " -> " + f.to().model().asString()));
            });
}
System.out.println("served by: " + accumulator.message().model().asString());

// Non-streaming fallback (reuse state to keep conversation pinned)
BetaMessage message = fallbackClient.beta().messages().create(
        createParams, RequestOptions.builder().fallbackState(state).build());
```

---

## Message batches

Create batches of requests, poll for completion, stream results, and delete.

```java
import com.anthropic.models.messages.batches.*;

BatchCreateParams createParams = BatchCreateParams.builder()
        .addRequest(BatchCreateParams.Request.builder()
                .customId("best-sdk")
                .params(BatchCreateParams.Request.Params.builder()
                        .model(Model.CLAUDE_SONNET_5)
                        .maxTokens(2048)
                        .addUserMessage("Tell me a story about building the best SDK!")
                        .build())
                .build())
        .addRequest(BatchCreateParams.Request.builder()
                .customId("sdk-company")
                .params(BatchCreateParams.Request.Params.builder()
                        .model(Model.CLAUDE_SONNET_5)
                        .maxTokens(2048)
                        .addUserMessage("Which company made of metal generates SDKs?")
                        .build())
                .build())
        .build();

// Create and poll
MessageBatch batch = client.messages().batches().create(createParams);
while (batch.processingStatus().equals(MessageBatch.ProcessingStatus.IN_PROGRESS)) {
    Thread.sleep(2000);
    batch = client.messages().batches().retrieve(
            BatchRetrieveParams.builder().messageBatchId(batch.id()).build());
}

// Stream results
try (StreamResponse<MessageBatchIndividualResponse> streamResponse = client.messages()
        .batches()
        .resultsStreaming(
                BatchResultsParams.builder().messageBatchId(batch.id()).build())) {
    streamResponse.stream().forEach(response -> {
        System.out.println(response.customId());
        Message message = response.result().asSucceeded().message();
        message.content().stream()
                .flatMap(b -> b.text().stream())
                .forEach(t -> System.out.println(t.text()));
    });
}

// Delete when done
client.messages().batches().delete(
        BatchDeleteParams.builder().messageBatchId(batch.id()).build());
```

---

## Skills API

Create skills from local SKILL.md files, retrieve them, and manage versions.

```java
import com.anthropic.core.MultipartField;
import com.anthropic.models.skills.SkillCreateParams;
import com.anthropic.models.skills.versions.VersionRetrieveParams;
import java.io.InputStream;

// Create a skill from multiple files
var skill = client.skills().create(
        SkillCreateParams.builder()
                .displayName("greeting-" + System.currentTimeMillis())
                // Each file's filename is its path inside the skill, including the top-level dir
                .addFile(MultipartField.<InputStream>builder()
                        .value(classloader.getResourceAsStream("greeting-SKILL.md"))
                        .filename("greeting/SKILL.md")
                        .build())
                .addFile(MultipartField.<InputStream>builder()
                        .value(classloader.getResourceAsStream("greeting-reference.md"))
                        .filename("greeting/reference.md")
                        .build())
                .build());
System.out.println("Created skill: " + skill.id());

// Retrieve skill and its latest version
var retrieved = client.skills().retrieve(skill.id());
String versionId = retrieved.latestVersionId();

// Get version details — name/description parsed from SKILL.md
var skillVersion = client.skills().versions().retrieve(
        VersionRetrieveParams.builder()
                .skillId(skill.id())
                .version(versionId)
                .build());
System.out.println("name=" + skillVersion.name() + ", desc=" + skillVersion.description());
```

---

## Managed agents

Full lifecycle: environment → agent → session → events.

```java
import com.anthropic.models.beta.environments.*;
import com.anthropic.models.beta.agents.*;
import com.anthropic.models.beta.sessions.*;

// 1. Create environment
BetaManagedAgentsEnvironment environment = client.beta().environments().create(
        BetaManagedAgentsEnvironmentCreateParams.builder().build());

// 2. Create agent
BetaManagedAgentsAgent agent = client.beta().agents().create(
        BetaManagedAgentsAgentCreateParams.builder()
                .environmentId(environment.id())
                .modelConfig(BetaManagedAgentsModelConfigParams.builder()
                        .model(Model.CLAUDE_SONNET_5)
                        .systemPrompt("You are a helpful assistant.")
                        .maxTokens(1024L)
                        .build())
                .build());

// 3. Create session
BetaManagedAgentsSession session = client.beta().sessions().create(
        BetaManagedAgentsSessionCreateParams.builder()
                .agentId(agent.id())
                .build());

// 4. Send a user message event
client.beta().sessions().events().send(
        BetaManagedAgentsUserMessageEventParams.builder()
                .sessionId(session.id())
                .content("What is 2 + 2?")
                .build());

// 5. Stream session events until idle
try (StreamResponse<BetaManagedAgentsSessionEvent> streamResponse =
        client.beta().sessions().events().streamStreaming(
                BetaManagedAgentsSessionEventStreamParams.builder()
                        .sessionId(session.id())
                        .build())) {
    streamResponse.stream()
            .takeWhile(event -> !event.isSessionStatusIdle())
            .forEach(event -> {
                event.textDelta().ifPresent(t -> System.out.print(t.delta()));
            });
}
```

---

## Model listing

```java
import com.anthropic.models.models.*;

SyncPage<ModelInfo> models = client.models().list(ModelListParams.builder().build());
models.forEach(model -> System.out.println(model.id()));
```

Async version:

```java
client.models().list(ModelListParams.builder().build())
        .thenAccept(page -> page.forEach(model -> System.out.println(model.id())))
        .join();
```

---

## Cloud provider clients

### AWS Bedrock

```java
// IAM credentials (SDK auto-discovers from environment)
import com.anthropic.client.bedrock.AnthropicBedrock;
AnthropicClient client = AnthropicBedrock.client();

// API key
AnthropicClient client = AnthropicBedrock.builder()
        .awsAccessKey("...")
        .awsSecretKey("...")
        .awsRegion("us-east-1")
        .build();
```

### Google Vertex AI

```java
import com.anthropic.client.vertex.AnthropicVertex;
AnthropicClient client = AnthropicVertex.client();  // uses ADC
```

### Google Cloud

```java
import com.anthropic.client.googlecloud.AnthropicGoogleCloud;
AnthropicClient client = AnthropicGoogleCloud.client();
```

### Azure Foundry

```java
import com.anthropic.client.foundry.AnthropicFoundry;
// API key
AnthropicClient client = AnthropicFoundry.builder().apiKey("...").build();
// Bearer token
AnthropicClient client = AnthropicFoundry.builder().bearerToken("...").build();
```

All cloud clients implement `AnthropicClient` and support the full Messages API.

---

## Error handling

```java
import com.anthropic.errors.AnthropicError;
import com.anthropic.errors.PermissionDeniedException;
import com.anthropic.errors.RateLimitException;
import com.anthropic.errors.BadRequestException;

try {
    client.messages().create(createParams);
} catch (PermissionDeniedException e) {
    System.err.println("403: " + e.getMessage());
} catch (RateLimitException e) {
    System.err.println("429: " + e.getMessage());
} catch (BadRequestException e) {
    System.err.println("400: " + e.getMessage());
} catch (AnthropicError e) {
    System.err.println("API error: " + e.statusCode() + " " + e.getMessage());
}
```

---

## Common patterns

### Access typed content blocks

```java
message.content().stream()
        .flatMap(b -> b.text().stream())       // TextBlock
        .forEach(t -> System.out.println(t.text()));

message.content().stream()
        .flatMap(b -> b.toolUse().stream())    // ToolUseBlock
        .forEach(tu -> System.out.println(tu.name()));
```

### Check content block type

```java
for (ContentBlock block : message.content()) {
    if (block.isText()) {
        System.out.println(block.asText().text());
    } else if (block.isToolUse()) {
        System.out.println(block.asToolUse().name());
    } else if (block.isThinking()) {
        System.out.println(block.asThinking().thinking());
    }
}
```

### Additional headers (e.g., beta features)

```java
MessageCreateParams params = MessageCreateParams.builder()
        .putAdditionalHeader("anthropic-beta", "structured-outputs-2025-11-13")
        // ...
        .build();
```

### Run examples via Gradle

```bash
./gradlew :anthropic-java-example:run -Pexample=MessagesExample
./gradlew :anthropic-java-example:run -Pexample=BetaToolRunner
./gradlew :anthropic-java-example:run -Pexample=BetaMcpToolRunner
./gradlew :anthropic-java-example:run -Pexample=ManagedAgents
./gradlew :anthropic-java-example:run -Pexample=StructuredOutputs
./gradlew :anthropic-java-example:run -Pexample=Batch
```

---

## Quick reference

| Task | API |
|------|-----|
| Basic message | `client.messages().create(params)` |
| Streaming | `client.messages().createStreaming(params)` in try-with-resources |
| Async | `AnthropicOkHttpClientAsync.fromEnv()` + `.thenAccept().join()` |
| Count tokens | `client.messages().countTokens(params).inputTokens()` |
| Structured output | `MessageCreateParams.builder().outputConfig(MyClass.class)` |
| Thinking | `.thinking(ThinkingConfigAdaptive.builder()…)` |
| Auto tool runner | `client.beta().messages().toolRunner(params)` + `for (BetaMessage m : runner)` |
| Manual tool loop | beta messages `.create()` → detect `.toolUse()` → append → create again |
| MCP tools | `BetaMcp.mcpTools(mcpClient.listTools().tools(), mcpClient)` → `.addTools(betaTools)` |
| Server fallback | `.fallbacksOfFallbackParams(...)` + `.addBeta(SERVER_SIDE_FALLBACK_...)` |
| Client fallback | `BetaRefusalFallbackInterceptor` + `BetaFallbackState` |
| Batch | `client.messages().batches().create()` → poll → `.resultsStreaming()` |
| Skills API | `client.skills().create(SkillCreateParams...)` |
| Managed agents | environments → agents → sessions → events → streamStreaming |
| Model list | `client.models().list(ModelListParams.builder().build())` |
| Bedrock | `AnthropicBedrock.client()` |
| Vertex AI | `AnthropicVertex.client()` |
