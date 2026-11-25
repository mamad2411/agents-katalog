# Azure Foundry Integration Testing Setup

This guide shows how to configure Azure Foundry credentials and enable real integration tests with gpt-4o.

## Quick Setup

### 1. Get Your Azure Foundry Credentials

You need:
- **Azure Foundry Endpoint** (format: `https://your-resource.openai.azure.com/`)
- **Azure Foundry API Key** (from your Azure OpenAI resource)

### 2. Store Credentials Securely (User Secrets)

Run these commands from the repo root:

```powershell
# Set Azure Foundry endpoint
dotnet user-secrets set "Parameters:azure-foundry-endpoint" "https://your-resource.openai.azure.com/" --project Blaze.LlmGateway.AppHost

# Set Azure Foundry API key
dotnet user-secrets set "Parameters:azure-foundry-api-key" "your-api-key-here" --project Blaze.LlmGateway.AppHost
```

**Note:** User secrets are stored locally (not in git) at:
- **Windows:** `%APPDATA%\Microsoft\UserSecrets\{AppHost-project-guid}\secrets.json`
- **macOS/Linux:** `~/.microsoft/usersecrets/{AppHost-project-guid}/secrets.json`

### 3. Verify Credentials Are Set

```powershell
dotnet user-secrets list --project Blaze.LlmGateway.AppHost | Select-String "azure-foundry"
```

Should output:
```
Parameters:azure-foundry-endpoint = https://your-resource.openai.azure.com/
Parameters:azure-foundry-api-key = [REDACTED]
```

## Running Tests

### Mocked Tests (Fast, No Credentials Needed)
```powershell
# Run mocked Azure Foundry tests (5 tests, ~2 seconds)
dotnet test --filter "FullyQualifiedName~AzureFoundryIntegrationTests" --no-build
```

Result:
- ✅ 5 tests passing (mocked responses)
- ⏭️ 1 test skipped (real integration)

### Real Integration Tests (Slow, Requires Credentials)

Once you have credentials set up, edit `AzureFoundryIntegrationTests.cs` and change:

```csharp
[Fact(Skip = "Requires Azure Foundry credentials...")]
public async Task AzureFoundry_RealIntegration_ChatCompletionsWithGpt4o_Succeeds()
```

to:

```csharp
[Fact]
public async Task AzureFoundry_RealIntegration_ChatCompletionsWithGpt4o_Succeeds()
```

Then enable the Aspire-based test runner:

```powershell
# Run via Aspire AppHost (picks up your user-secrets)
dotnet run --project Blaze.LlmGateway.AppHost

# In another terminal:
dotnet test --filter "RealIntegration" --no-build
```

## What Gets Tested

### Mocked Tests (5 tests)
1. ✅ Chat completions with gpt-4o (non-streaming)
2. ✅ Chat completions streaming (SSE format)
3. ✅ Text completions (legacy `/v1/completions` endpoint)
4. ✅ Model discovery (`/v1/models` includes gpt-4o)
5. ✅ Request routing (gpt-4o requests are handled)

### Real Integration Test (1 test, currently skipped)
- 🔗 Actually calls Azure OpenAI API with gpt-4o
- Requires live credentials
- Slower (~2-3 seconds per request)
- Best run separately in CI/CD pipeline or on-demand

## Troubleshooting

### Error: "Unable to resolve service for type 'Aspire.Hosting.Publishing.IContainerRuntime'"

This happens with real integration tests. You need to run via AppHost:
```powershell
dotnet run --project Blaze.LlmGateway.AppHost
```

### Error: "Unauthorized (401)" from Azure API

Your credentials are invalid or expired. Verify with:
```powershell
dotnet user-secrets list --project Blaze.LlmGateway.AppHost
```

### Tests are too slow

Mocked tests should take ~1-2 seconds. If slow:
- Check for network issues
- Run only mocked tests: `--filter "AzureFoundry"`

## Architecture

```
AzureFoundryIntegrationTests
├── Mocked Tests (WebApplicationFactory)
│   ├── ChatCompletions (streaming + non-streaming)
│   ├── TextCompletions (legacy endpoint)
│   ├── Models list
│   └── Routing verification
│
└── Real Integration Test (Aspire-based, skipped by default)
    └── Requires credentials + live Azure endpoint
```

## Test File Location

- **Source:** `Blaze.LlmGateway.Tests/AzureFoundryIntegrationTests.cs`
- **Config:** User secrets in `~/.microsoft/usersecrets/`

## Next Steps

1. ✅ Add your Azure credentials (user-secrets)
2. ✅ Run mocked tests to verify setup
3. ✅ Optionally enable and run real integration tests
4. ✅ Add to CI/CD pipeline (consider running real tests on schedule or separate job)
