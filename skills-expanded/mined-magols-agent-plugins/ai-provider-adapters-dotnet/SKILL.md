---
name: ai-provider-adapters-dotnet
description: 'Build provider adapters for .NET AI applications enabling vendor-neutral code. Use when implementing Azure OpenAI, Azure AI Foundry, OpenAI, Anthropic, Ollama (local) adapters behind Microsoft.Extensions.AI abstractions with multi-provider failover, circuit breakers, and normalized error handling.'
---

# AI Provider Adapters for .NET

Consistent adapter patterns for provider SDKs using Microsoft.Extensions.AI abstractions, enabling provider switching and resiliency.

## When To Use This Skill

- Need to switch providers (Azure OpenAI ↔ OpenAI ↔ Anthropic ↔ local) without changing application code.
- Need fallback/failover strategies across multiple providers.
- Need consistent auth, configuration, and error handling across all providers.
- Multi-tenant scenarios requiring provider variance by customer/environment.

## Adapter Interface Template

```csharp
/// <summary>
/// Common adapter contract for provider-specific chat clients.
/// </summary>
public interface IChatProviderAdapter
{
    /// <summary>
    /// Human-readable provider identifier (e.g., "azure_openai", "openai", "anthropic", "ollama").
    /// </summary>
    string ProviderId { get; }

    /// <summary>
    /// Health check: verify connectivity and auth without consuming tokens.
    /// </summary>
    Task<AdapterHealthStatus> GetHealthAsync(CancellationToken cancellationToken = default);

    /// <summary>
    /// Get available models for this provider.
    /// </summary>
    Task<IReadOnlyList<ProviderModel>> GetModelsAsync(CancellationToken cancellationToken = default);

    /// <summary>
    /// Create IChatClient for the specified model with normalized options.
    /// </summary>
    Task<ChatClient> CreateClientAsync(
        string modelId,
        ChatClientOptions? options = null,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Normalize provider-specific errors to common error types for retry logic.
    /// </summary>
    AdapterErrorInfo NormalizeError(Exception ex);
}

public record AdapterHealthStatus(bool IsHealthy, string? FailureReason = null, TimeSpan? Latency = null);

public record ProviderModel(string ModelId, string DisplayName, int? MaxTokens = null, decimal? CostPer1kInputTokens = null);

public record AdapterErrorInfo(string ErrorType, bool IsRetryable, string Message)
{
    public static AdapterErrorInfo FromException(Exception ex, string providerId) => new(
        ErrorType: GetErrorType(ex),
        IsRetryable: IsRetryableError(ex),
        Message: $"[{providerId}] {ex.Message}");

    private static string GetErrorType(Exception ex) => ex switch
    {
        HttpRequestException => "NetworkError",
        TimeoutException => "TimeoutError",
        OperationCanceledException => "CancelledError",
        InvalidOperationException => "ConfigurationError",
        _ => "UnknownError"
    };

    private static bool IsRetryableError(Exception ex) => ex switch
    {
        TimeoutException or OperationCanceledException => true,
        HttpRequestException hre => hre.StatusCode is >= 500 or 408 or 429,
        _ => false
    };
}
```

## Initial Workflow

### 1. Azure OpenAI Adapter

```csharp
public class AzureOpenAiAdapter : IChatProviderAdapter
{
    private readonly AzureOpenAIClient _client;
    private readonly ILogger<AzureOpenAiAdapter> _logger;
    private readonly string _deploymentName;

    public string ProviderId => "azure_openai";

    public AzureOpenAiAdapter(string endpoint, string deploymentName, AzureKeyCredential credential, ILogger<AzureOpenAiAdapter> logger)
    {
        _client = new AzureOpenAIClient(new Uri(endpoint), credential);
        _deploymentName = deploymentName;
        _logger = logger;
    }

    public async Task<AdapterHealthStatus> GetHealthAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            var sw = System.Diagnostics.Stopwatch.StartNew();
            // Lightweight health check: get model info
            var models = await _client.GetModelAsync(_deploymentName, cancellationToken);
            sw.Stop();
            return new AdapterHealthStatus(IsHealthy: true, Latency: sw.Elapsed);
        }
        catch (Exception ex)
        {
            _logger.LogWarning("Azure OpenAI health check failed: {Error}", ex.Message);
            return new AdapterHealthStatus(IsHealthy: false, FailureReason: ex.Message);
        }
    }

    public async Task<IReadOnlyList<ProviderModel>> GetModelsAsync(CancellationToken cancellationToken = default)
    {
        // For Azure OpenAI, return the single deployment
        var model = await _client.GetModelAsync(_deploymentName, cancellationToken);
        return new[]
        {
            new ProviderModel(ModelId: _deploymentName, DisplayName: $"Azure OpenAI ({_deploymentName})")
        };
    }

    public async Task<ChatClient> CreateClientAsync(string modelId, ChatClientOptions? options = null, CancellationToken cancellationToken = default)
    {
        var chatClient = _client.GetChatClient(_deploymentName);
        
        // Wrap with instrumentation middleware
        return new ChatClientBuilder(chatClient)
            .UseLogging()
            .Build();
    }

    public AdapterErrorInfo NormalizeError(Exception ex) => AdapterErrorInfo.FromException(ex, ProviderId);
}
```

### 2. OpenAI Adapter

```csharp
public class OpenAiAdapter : IChatProviderAdapter
{
    private readonly OpenAIClient _client;
    private readonly ILogger<OpenAiAdapter> _logger;

    public string ProviderId => "openai";

    public OpenAiAdapter(string apiKey, ILogger<OpenAiAdapter> logger)
    {
        _client = new OpenAIClient(apiKey);
        _logger = logger;
    }

    public async Task<AdapterHealthStatus> GetHealthAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var models = await _client.GetModelsAsync(cancellationToken);
            sw.Stop();
            return new AdapterHealthStatus(IsHealthy: true, Latency: sw.Elapsed);
        }
        catch (Exception ex)
        {
            return new AdapterHealthStatus(IsHealthy: false, FailureReason: ex.Message);
        }
    }

    public async Task<IReadOnlyList<ProviderModel>> GetModelsAsync(CancellationToken cancellationToken = default)
    {
        var models = await _client.GetModelsAsync(cancellationToken);
        return models
            .Where(m => m.Id.Contains("gpt"))
            .Select(m => new ProviderModel(ModelId: m.Id, DisplayName: m.Id))
            .ToList();
    }

    public async Task<ChatClient> CreateClientAsync(string modelId, ChatClientOptions? options = null, CancellationToken cancellationToken = default)
    {
        var chatClient = _client.GetChatClient(modelId);
        return new ChatClientBuilder(chatClient)
            .UseLogging()
            .Build();
    }

    public AdapterErrorInfo NormalizeError(Exception ex) => AdapterErrorInfo.FromException(ex, ProviderId);
}
```

### 3. Fallback/Failover Strategy

```csharp
public class MultiProviderAdapter : IChatProviderAdapter
{
    private readonly IReadOnlyList<IChatProviderAdapter> _adapters;
    private readonly ILogger<MultiProviderAdapter> _logger;

    public string ProviderId => "multi-provider";

    public MultiProviderAdapter(IEnumerable<IChatProviderAdapter> adapters, ILogger<MultiProviderAdapter> logger)
    {
        _adapters = adapters.ToList();
        _logger = logger;
    }

    public async Task<AdapterHealthStatus> GetHealthAsync(CancellationToken cancellationToken = default)
    {
        var results = await Task.WhenAll(_adapters.Select(a => a.GetHealthAsync(cancellationToken)));
        var healthyCount = results.Count(r => r.IsHealthy);
        return new AdapterHealthStatus(
            IsHealthy: healthyCount > 0,
            FailureReason: healthyCount == 0 ? "All providers unhealthy" : null);
    }

    public async Task<IReadOnlyList<ProviderModel>> GetModelsAsync(CancellationToken cancellationToken = default)
    {
        var allModels = new List<ProviderModel>();
        foreach (var adapter in _adapters)
        {
            try
            {
                var models = await adapter.GetModelsAsync(cancellationToken);
                allModels.AddRange(models);
            }
            catch (Exception ex)
            {
                _logger.LogWarning("Failed to get models from {Provider}: {Error}", adapter.ProviderId, ex.Message);
            }
        }
        return allModels;
    }

    public async Task<ChatClient> CreateClientAsync(string modelId, ChatClientOptions? options = null, CancellationToken cancellationToken = default)
    {
        Exception? lastError = null;

        foreach (var adapter in _adapters)
        {
            try
            {
                var models = await adapter.GetModelsAsync(cancellationToken);
                if (models.Any(m => m.ModelId == modelId))
                {
                    _logger.LogInformation("Creating client for {Model} via {Provider}", modelId, adapter.ProviderId);
                    return await adapter.CreateClientAsync(modelId, options, cancellationToken);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning("Failover from {Provider}: {Error}", adapter.ProviderId, ex.Message);
                lastError = ex;
            }
        }

        throw new InvalidOperationException($"No adapter available for model {modelId}", lastError);
    }

    public AdapterErrorInfo NormalizeError(Exception ex) => AdapterErrorInfo.FromException(ex, ProviderId);
}
```

### 4. Dependency Injection Registration

```csharp
// Program.cs
public static class AdapterServiceCollectionExtensions
{
    public static IServiceCollection AddChatProviderAdapters(this IServiceCollection services, IConfiguration config)
    {
        // Register primary adapter
        services.AddSingleton<IChatProviderAdapter>(sp =>
            new AzureOpenAiAdapter(
                endpoint: config["AzureOpenAI:Endpoint"]!,
                deploymentName: config["AzureOpenAI:Deployment"]!,
                credential: new AzureKeyCredential(config["AzureOpenAI:ApiKey"]!),
                logger: sp.GetRequiredService<ILogger<AzureOpenAiAdapter>>()));

        // Register fallback adapter
        services.AddSingleton<IChatProviderAdapter>(sp =>
            new OpenAiAdapter(
                apiKey: config["OpenAI:ApiKey"]!,
                logger: sp.GetRequiredService<ILogger<OpenAiAdapter>>()));

        // Register multi-provider wrapper for failover
        services.AddSingleton(sp =>
        {
            var adapters = sp.GetRequiredService<IEnumerable<IChatProviderAdapter>>();
            return new MultiProviderAdapter(adapters, sp.GetRequiredService<ILogger<MultiProviderAdapter>>());
        });

        return services;
    }
}

// Startup
var builder = WebApplicationBuilder.CreateBuilder(args);
builder.Services.AddChatProviderAdapters(builder.Configuration);
```

## Adapter Contract Tests

```csharp
[TestClass]
public class ChatProviderAdapterTests
{
    private IChatProviderAdapter _adapter;

    [TestInitialize]
    public void Setup()
    {
        // Initialize adapter with test credentials
        _adapter = new AzureOpenAiAdapter(
            endpoint: "https://test.openai.azure.com/",
            deploymentName: "gpt-4-turbo",
            credential: new AzureKeyCredential("test-key"),
            logger: new NullLogger<AzureOpenAiAdapter>());
    }

    [TestMethod]
    public async Task CreateClient_ReturnsValidChatClient()
    {
        // Arrange
        var modelId = "gpt-4-turbo";

        // Act
        var client = await _adapter.CreateClientAsync(modelId);

        // Assert
        Assert.IsNotNull(client);
    }

    [TestMethod]
    public async Task NormalizeError_HandlesTimeoutCorrectly()
    {
        // Arrange
        var timeoutEx = new TimeoutException("Request timeout");

        // Act
        var normalized = _adapter.NormalizeError(timeoutEx);

        // Assert
        Assert.IsTrue(normalized.IsRetryable);
        Assert.AreEqual("TimeoutError", normalized.ErrorType);
    }

    [TestMethod]
    public async Task GetHealth_ReturnsStatusOnSuccess()
    {
        // Act
        var health = await _adapter.GetHealthAsync();

        // Assert
        Assert.IsNotNull(health);
    }
}
```

## Gotchas

- **SDK Leakage**: Never return provider-specific types (e.g., `Azure.AI.OpenAI.ChatCompletionOptions`) from adapter methods. Always normalize to `ChatClientOptions` or generic types.
- **Retry Conflicts**: Disable provider SDK built-in retries; let application-level retry policies (Polly, etc.) manage all retries to avoid exponential backoff stacking.
- **Auth Secret Rotation**: For long-running processes, refresh credentials before they expire. Use credential providers (e.g., `DefaultAzureCredential`) instead of raw keys.
- **Model Availability Drift**: Cache `GetModelsAsync()` with TTL; don't call on every request. Use background refresh for production.
- **Cost Attribution**: Track which adapter handled each request; log cost per provider to catch budget drift early.

## References

- **Microsoft.Extensions.AI**: <https://learn.microsoft.com/dotnet/ai/microsoft-extensions-ai>
- **Azure OpenAI Client**: <https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/>
- **OpenAI .NET SDK**: <https://github.com/openai/openai-dotnet>
- **ChatClient Middleware Pattern**: <https://learn.microsoft.com/dotnet/ai/microsoft-extensions-ai#use-middleware>
- **Polly Retry Policies**: <https://www.thepollyproject.org/>
