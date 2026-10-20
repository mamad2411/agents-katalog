---
name: ai-evals-dotnet
description: 'Create evaluation and regression workflows for .NET AI features with repeatable scorecards. Use when validating prompt quality, tool reliability, safety guardrails, workflow behavior, and release readiness. Covers dataset versioning, dimension-based scoring (accuracy, safety, latency, cost, robustness), CI automation, baseline comparison, and PR regression reporting.'
---

# AI Evaluations for .NET

Systematic evaluation and regression testing for AI systems: scored quality dimensions, versioned datasets, CI automation, and trend analysis with measurable gates.

## When To Use This Skill

- Prompt or workflow changes could alter behavior; need objective quality gates.
- Deploying to production; need baseline comparisons across versions/models/providers.
- Multi-model evaluation (compare GPT-4 vs Claude vs Anthropic for same task).
- Regression tracking: detecting performance degradation before users see it.
- Release readiness: proving that a feature meets quality thresholds before promotion.

## Scorecard Template

### Recommended Dimensions

| Dimension | Metric | Threshold | Example |
|-----------|--------|-----------|---------|
| **Accuracy** | % of outputs matching expected result or intent | ≥ 95% | Classify email as spam/not-spam; accuracy must be ≥ 95% |
| **Safety** | % of outputs passing guardrails (no hallucination, injection attempts blocked) | ≥ 99% | Prompt-injection attempts blocked 99%+ of time |
| **Latency** | p95 response time (seconds) | ≤ 2s | Model response completes within 2s for 95% of requests |
| **Cost** | Average cost per request (USD) | ≤ $0.01 | Stay within cost budget after optimization |
| **Robustness** | Pass rate on adversarial/edge-case inputs | ≥ 90% | Handle typos, slang, mixed languages correctly ≥ 90% of time |

### Scorecard Record

```csharp
public record EvalDimension(
    string Name,                        // "accuracy", "safety", "latency", "cost", "robustness"
    double Score,                       // 0.0-1.0 or actual value (e.g., 1.5s for latency)
    double Threshold,                   // Pass threshold
    bool IsPassed,                      // Score >= Threshold
    string? FailureReason = null);      // Why it failed (if failed)

public record EvalScorecard(
    string EvalId,
    string EvalName,
    string Model,
    string Provider,
    string PromptVersion,
    int SampleSize,
    List<EvalDimension> Dimensions,
    double OverallScore,                // Average of all dimension scores (0-1)
    bool IsRegression,                  // Compared to baseline; worse than baseline?
    DateTimeOffset EvaluatedAt,
    EvalScorecard? BaselineScorecard = null);
```

## Initial Workflow

### 1. Dataset Curation & Versioning

```csharp
public record EvalDataset(
    string DatasetId,
    string DatasetName,
    string Version,                     // Semantic versioning (e.g., "1.0.0")
    string Description,
    List<EvalTestCase> TestCases,
    DateTimeOffset CreatedAt,
    DateTimeOffset? LastModifiedAt = null,
    Dictionary<string, object>? Metadata = null);

public record EvalTestCase(
    string Id,
    string Category,                    // "happy-path", "edge-case", "adversarial", "regression"
    string Input,
    string? ExpectedOutput = null,
    List<string>? AcceptableOutputs = null,
    object? Context = null);            // Additional context (e.g., user tier, region)

/// <summary>
/// Manage evaluation datasets with versioning and metadata.
/// </summary>
public class EvalDatasetManager
{
    private readonly ILogger<EvalDatasetManager> _logger;
    private readonly IEvalDatasetStore _store;

    public EvalDatasetManager(ILogger<EvalDatasetManager> logger, IEvalDatasetStore store)
    {
        _logger = logger;
        _store = store;
    }

    /// <summary>
    /// Create or update a dataset. Use semantic versioning.
    /// </summary>
    public async Task<EvalDataset> UpsertDatasetAsync(
        string datasetName,
        List<EvalTestCase> testCases,
        string version,
        string description,
        CancellationToken cancellationToken = default)
    {
        var dataset = new EvalDataset(
            DatasetId: Guid.NewGuid().ToString(),
            DatasetName: datasetName,
            Version: version,
            Description: description,
            TestCases: testCases,
            CreatedAt: DateTimeOffset.UtcNow);

        await _store.SaveAsync(dataset, cancellationToken);

        _logger.LogInformation(
            "Dataset created | Name={Name} Version={Version} Cases={Count}",
            datasetName, version, testCases.Count);

        return dataset;
    }

    /// <summary>
    /// Get dataset by name and version (for reproducibility).
    /// </summary>
    public async Task<EvalDataset> GetDatasetAsync(string datasetName, string version, CancellationToken cancellationToken = default)
    {
        var dataset = await _store.GetByNameAndVersionAsync(datasetName, version, cancellationToken)
            ?? throw new InvalidOperationException($"Dataset {datasetName}@{version} not found");

        _logger.LogInformation("Dataset loaded | Name={Name} Version={Version}", datasetName, version);
        return dataset;
    }

    /// <summary>
    /// List all versions of a dataset for comparison.
    /// </summary>
    public async Task<List<EvalDataset>> ListVersionsAsync(string datasetName, CancellationToken cancellationToken = default)
    {
        var versions = await _store.GetAllVersionsAsync(datasetName, cancellationToken);
        _logger.LogInformation("Dataset versions | Name={Name} Versions={Count}", datasetName, versions.Count);
        return versions;
    }
}

public interface IEvalDatasetStore
{
    Task SaveAsync(EvalDataset dataset, CancellationToken cancellationToken = default);
    Task<EvalDataset?> GetByNameAndVersionAsync(string name, string version, CancellationToken cancellationToken = default);
    Task<List<EvalDataset>> GetAllVersionsAsync(string name, CancellationToken cancellationToken = default);
}
```

### 2. Evaluation Engine with Dimension Scoring

```csharp
public class EvalEngine
{
    private readonly IChatClient _chatClient;
    private readonly IOutputValidator _validator;           // From Phase 3
    private readonly IDataClassifier _classifier;           // From Phase 3
    private readonly ILogger<EvalEngine> _logger;

    public EvalEngine(
        IChatClient chatClient,
        IOutputValidator validator,
        IDataClassifier classifier,
        ILogger<EvalEngine> logger)
    {
        _chatClient = chatClient;
        _validator = validator;
        _classifier = classifier;
        _logger = logger;
    }

    /// <summary>
    /// Execute eval on dataset and produce scorecard.
    /// </summary>
    public async Task<EvalScorecard> EvaluateAsync(
        EvalDataset dataset,
        string model,
        string provider,
        string promptVersion,
        EvalThresholds thresholds,
        EvalScorecard? baseline = null,
        CancellationToken cancellationToken = default)
    {
        var evalId = Guid.NewGuid().ToString();
        var sw = System.Diagnostics.Stopwatch.StartNew();
        var results = new List<EvalResult>();

        _logger.LogInformation(
            "Evaluation started | EvalId={EvalId} Dataset={Dataset} Model={Model} Provider={Provider}",
            evalId, dataset.DatasetName, model, provider);

        // Execute test cases
        foreach (var testCase in dataset.TestCases)
        {
            try
            {
                var result = await EvaluateTestCaseAsync(
                    testCase, model, provider, thresholds, cancellationToken);
                results.Add(result);
            }
            catch (Exception ex)
            {
                _logger.LogWarning("Test case failed | TestId={TestId} Error={Error}",
                    testCase.Id, ex.Message);
                results.Add(new EvalResult(
                    TestCaseId: testCase.Id,
                    Success: false,
                    Reason: ex.Message));
            }
        }

        sw.Stop();

        // Compute dimensions
        var dimensions = ComputeDimensions(results, dataset, thresholds);
        var overallScore = dimensions.Average(d => d.IsPassed ? 1.0 : 0.0);
        var isRegression = baseline != null && overallScore < baseline.OverallScore;

        var scorecard = new EvalScorecard(
            EvalId: evalId,
            EvalName: $"{dataset.DatasetName}/{model}",
            Model: model,
            Provider: provider,
            PromptVersion: promptVersion,
            SampleSize: dataset.TestCases.Count,
            Dimensions: dimensions,
            OverallScore: overallScore,
            IsRegression: isRegression,
            EvaluatedAt: DateTimeOffset.UtcNow,
            BaselineScorecard: baseline);

        _logger.LogInformation(
            "Evaluation complete | EvalId={EvalId} Score={Score} DurationMs={Duration} Regression={IsRegression}",
            evalId, overallScore, sw.ElapsedMilliseconds, isRegression);

        return scorecard;
    }

    private async Task<EvalResult> EvaluateTestCaseAsync(
        EvalTestCase testCase,
        string model,
        string provider,
        EvalThresholds thresholds,
        CancellationToken cancellationToken)
    {
        var sw = System.Diagnostics.Stopwatch.StartNew();

        // Get model response
        var response = await _chatClient.CompleteAsync(
            new List<ChatMessage> { new(ChatRole.User, testCase.Input) },
            cancellationToken: cancellationToken);

        sw.Stop();
        var output = response.Content[0].Text;

        // Validate output (guardrails from Phase 3)
        var validation = await _validator.ValidateOutputAsync(
            output,
            thresholds.OutputValidationPolicy,
            cancellationToken);

        // Classify for safety
        var classification = await _classifier.ClassifyAsync(output, cancellationToken);

        return new EvalResult(
            TestCaseId: testCase.Id,
            Input: testCase.Input,
            Output: output,
            ExpectedOutput: testCase.ExpectedOutput,
            LatencyMs: (int)sw.ElapsedMilliseconds,
            IsOutputValid: validation.IsValid,
            IsSafe: !classification.ContainsSensitiveData,
            Success: true);
    }

    private List<EvalDimension> ComputeDimensions(
        List<EvalResult> results,
        EvalDataset dataset,
        EvalThresholds thresholds)
    {
        var dimensions = new List<EvalDimension>();

        // Accuracy: % of correct outputs
        var accuracyScore = results
            .Where(r => r.Success && r.Output == r.ExpectedOutput)
            .Count() / (double)results.Count;
        dimensions.Add(new(
            Name: "accuracy",
            Score: accuracyScore,
            Threshold: thresholds.AccuracyThreshold,
            IsPassed: accuracyScore >= thresholds.AccuracyThreshold));

        // Safety: % passing guardrails + no sensitive data
        var safetyScore = results
            .Where(r => r.Success && r.IsOutputValid && r.IsSafe)
            .Count() / (double)results.Count;
        dimensions.Add(new(
            Name: "safety",
            Score: safetyScore,
            Threshold: thresholds.SafetyThreshold,
            IsPassed: safetyScore >= thresholds.SafetyThreshold));

        // Latency: p95 latency
        var sortedLatencies = results
            .Where(r => r.Success)
            .OrderBy(r => r.LatencyMs)
            .ToList();
        var p95Latency = sortedLatencies[(int)(sortedLatencies.Count * 0.95)].LatencyMs / 1000.0;
        dimensions.Add(new(
            Name: "latency",
            Score: p95Latency,
            Threshold: thresholds.LatencyThresholdSeconds,
            IsPassed: p95Latency <= thresholds.LatencyThresholdSeconds,
            FailureReason: p95Latency > thresholds.LatencyThresholdSeconds
                ? $"p95 {p95Latency}s exceeds {thresholds.LatencyThresholdSeconds}s"
                : null));

        // Robustness: % passing on adversarial cases
        var adversarialCases = dataset.TestCases
            .Where(t => t.Category == "adversarial")
            .Select(t => t.Id)
            .ToHashSet();
        var robustnessScore = results
            .Where(r => adversarialCases.Contains(r.TestCaseId) && r.Success)
            .Count() / (double)Math.Max(adversarialCases.Count, 1);
        dimensions.Add(new(
            Name: "robustness",
            Score: robustnessScore,
            Threshold: thresholds.RobustnessThreshold,
            IsPassed: robustnessScore >= thresholds.RobustnessThreshold));

        return dimensions;
    }
}

public record EvalResult(
    string TestCaseId,
    string? Input = null,
    string? Output = null,
    string? ExpectedOutput = null,
    int LatencyMs = 0,
    bool IsOutputValid = true,
    bool IsSafe = true,
    bool Success = false,
    string? Reason = null);

public record EvalThresholds(
    double AccuracyThreshold = 0.95,
    double SafetyThreshold = 0.99,
    double LatencyThresholdSeconds = 2.0,
    double RobustnessThreshold = 0.90,
    OutputValidationPolicy OutputValidationPolicy = default!);
```

### 3. CI Integration Pattern

```csharp
// Program.cs or CI runner
public class EvalCiRunner
{
    private readonly EvalDatasetManager _datasetManager;
    private readonly EvalEngine _evalEngine;
    private readonly IEvalScorecardStore _scorecardStore;
    private readonly ILogger<EvalCiRunner> _logger;

    public EvalCiRunner(
        EvalDatasetManager datasetManager,
        EvalEngine evalEngine,
        IEvalScorecardStore scorecardStore,
        ILogger<EvalCiRunner> logger)
    {
        _datasetManager = datasetManager;
        _evalEngine = evalEngine;
        _scorecardStore = scorecardStore;
        _logger = logger;
    }

    /// <summary>
    /// Execute evaluation suite and gate on thresholds (for CI pipeline).
    /// </summary>
    public async Task<EvalCiResult> RunEvalSuiteAsync(
        string prBranch,
        string prNumber,
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("CI Eval suite started | PR={PR} Branch={Branch}", prNumber, prBranch);

        var results = new List<EvalScorecard>();
        var regressions = new List<string>();

        // Define eval suite (can be in config file or database)
        var suite = new[]
        {
            new EvalSuiteEntry(
                DatasetName: "email_classification",
                DatasetVersion: "1.0.0",
                Model: "gpt-4-turbo",
                Provider: "azure_openai"),
            new EvalSuiteEntry(
                DatasetName: "customer_sentiment",
                DatasetVersion: "1.0.0",
                Model: "gpt-4-turbo",
                Provider: "azure_openai")
        };

        foreach (var entry in suite)
        {
            try
            {
                // Load dataset
                var dataset = await _datasetManager.GetDatasetAsync(
                    entry.DatasetName, entry.DatasetVersion, cancellationToken);

                // Load baseline scorecard (previous main branch)
                var baseline = await _scorecardStore.GetLatestBaselineAsync(
                    entry.DatasetName, entry.Model, entry.Provider, cancellationToken);

                // Run evaluation
                var scorecard = await _evalEngine.EvaluateAsync(
                    dataset,
                    entry.Model,
                    entry.Provider,
                    promptVersion: prBranch,
                    thresholds: new EvalThresholds(),
                    baseline: baseline,
                    cancellationToken: cancellationToken);

                results.Add(scorecard);

                // Check for regressions
                if (scorecard.IsRegression)
                {
                    regressions.Add($"REGRESSION: {scorecard.EvalName} " +
                        $"(was {baseline?.OverallScore:P1}, now {scorecard.OverallScore:P1})");
                }

                // Check dimension thresholds
                foreach (var dim in scorecard.Dimensions.Where(d => !d.IsPassed))
                {
                    regressions.Add($"THRESHOLD FAILURE: {scorecard.EvalName}/{dim.Name} " +
                        $"(score: {dim.Score}, threshold: {dim.Threshold})");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError("Eval suite entry failed | Entry={Entry} Error={Error}",
                    entry.DatasetName, ex.Message);
                regressions.Add($"ERROR: {entry.DatasetName} - {ex.Message}");
            }
        }

        var passed = regressions.Count == 0;
        _logger.LogInformation(
            "CI Eval suite complete | PR={PR} Passed={Passed} Regressions={Count}",
            prNumber, passed, regressions.Count);

        return new EvalCiResult(
            PrNumber: prNumber,
            Passed: passed,
            Scorecards: results,
            Regressions: regressions);
    }
}

public record EvalSuiteEntry(string DatasetName, string DatasetVersion, string Model, string Provider);
public record EvalCiResult(string PrNumber, bool Passed, List<EvalScorecard> Scorecards, List<string> Regressions);
public interface IEvalScorecardStore
{
    Task SaveAsync(EvalScorecard scorecard, CancellationToken cancellationToken = default);
    Task<EvalScorecard?> GetLatestBaselineAsync(string datasetName, string model, string provider, CancellationToken cancellationToken = default);
}
```

### 4. PR Regression Reporting

```csharp
/// <summary>
/// Generate human-readable regression report for PR comments.
/// </summary>
public class PrRegressionReporter
{
    private readonly ILogger<PrRegressionReporter> _logger;

    public PrRegressionReporter(ILogger<PrRegressionReporter> logger)
    {
        _logger = logger;
    }

    public string GenerateReport(EvalCiResult evalResult)
    {
        var sb = new System.Text.StringBuilder();

        // Title
        var statusEmoji = evalResult.Passed ? "✅" : "❌";
        sb.AppendLine($"## {statusEmoji} AI Evaluation Report (PR #{evalResult.PrNumber})");
        sb.AppendLine();

        if (evalResult.Passed)
        {
            sb.AppendLine("All evaluations **passed**! No regressions detected.");
            sb.AppendLine();
        }
        else
        {
            sb.AppendLine("⚠️ **Evaluation issues detected:**");
            sb.AppendLine();
            foreach (var regression in evalResult.Regressions)
            {
                sb.AppendLine($"- {regression}");
            }
            sb.AppendLine();
        }

        // Scorecard summary table
        sb.AppendLine("### Scorecard Summary");
        sb.AppendLine();
        sb.AppendLine("| Eval | Model | Accuracy | Safety | Latency | Robustness | Status |");
        sb.AppendLine("|------|-------|----------|--------|---------|------------|--------|");

        foreach (var scorecard in evalResult.Scorecards)
        {
            var accuracy = scorecard.Dimensions.First(d => d.Name == "accuracy");
            var safety = scorecard.Dimensions.First(d => d.Name == "safety");
            var latency = scorecard.Dimensions.First(d => d.Name == "latency");
            var robustness = scorecard.Dimensions.First(d => d.Name == "robustness");

            var status = scorecard.IsRegression ? "🔴 Regression" : "🟢 Pass";

            sb.AppendLine($"| {scorecard.EvalName} | {scorecard.Model} " +
                $"| {accuracy.Score:P0} {(accuracy.IsPassed ? "✅" : "❌")} " +
                $"| {safety.Score:P0} {(safety.IsPassed ? "✅" : "❌")} " +
                $"| {latency.Score:F2}s {(latency.IsPassed ? "✅" : "❌")} " +
                $"| {robustness.Score:P0} {(robustness.IsPassed ? "✅" : "❌")} " +
                $"| {status} |");
        }

        sb.AppendLine();

        // Baseline comparison
        sb.AppendLine("### Comparison to Baseline");
        sb.AppendLine();
        foreach (var scorecard in evalResult.Scorecards.Where(s => s.BaselineScorecard != null))
        {
            var delta = ((scorecard.OverallScore - scorecard.BaselineScorecard!.OverallScore) * 100).ToString("+0.0;-0.0");
            sb.AppendLine($"- **{scorecard.EvalName}**: " +
                $"{scorecard.BaselineScorecard.OverallScore:P0} → {scorecard.OverallScore:P0} " +
                $"({delta}%) {(scorecard.IsRegression ? "⚠️ Regression" : "✅ Improvement")}");
        }

        sb.AppendLine();
        sb.AppendLine($"_Evaluated at {DateTimeOffset.UtcNow:u}_");

        return sb.ToString();
    }
}

// Example usage in CI workflow:
// var report = new PrRegressionReporter(logger).GenerateReport(evalResult);
// await githubClient.CreateCommentAsync(prNumber, report);
```

## Example YAML CI Configuration (GitHub Actions)

```yaml
name: AI Evaluations

on:
  pull_request:
    paths:
      - 'src/**'
      - 'prompts/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0'

      - name: Run evaluation suite
        run: dotnet run --project ./evals/EvalRunner.csproj -- --pr "${{ github.event.pull_request.number }}" --branch "${{ github.head_ref }}"
        env:
          AZURE_OPENAI_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
          EVAL_DATASET_STORE: ${{ secrets.EVAL_DATASET_STORE }}

      - name: Post results to PR
        if: always()
        run: dotnet run --project ./evals/PrReporter.csproj -- --pr "${{ github.event.pull_request.number }}" --token "${{ secrets.GITHUB_TOKEN }}"
```

## Gotchas

- **Subjective Scoring Only**: Never score purely on "sounds good" or manual review. Define measurable criteria (exact match, semantic similarity score, guardrail pass/fail). Use third-party validators (e.g., LLM-as-judge) sparingly and validate their scoring.
- **Dataset Bias**: Test datasets must include edge cases (typos, slang, adversarial inputs), not just happy paths. Otherwise, evals don't catch real-world failures.
- **Unreproducible Evals**: Always version datasets and pin model versions. If eval results vary wildly between runs, investigate: is the model non-deterministic? Is the dataset version changing?
- **Ignoring Regressions**: A small regression (0.5%) seems harmless but multiplies across users. Set strict thresholds; fail PRs on any regression unless explicitly justified in PR description.
- **Expensive Eval Loops**: Running evals on every commit can be slow and costly. Use a subset for PR CI (fast evals), full suite on main branch releases (comprehensive evals).
- **Cost Attribution Lost**: Track cost per eval; if evals cost $100+ per PR, you may want to sample datasets or use cheaper models for evals vs production.

## References

- **Evaluation Frameworks**: <https://github.com/microsoft/promptflow>
- **LLM Evaluation Benchmarks**: <https://huggingface.co/spaces/lmsys/chatbot-arena>
- **Semantic Similarity (for accuracy)**: <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>
- **Data Versioning (DVC)**: <https://dvc.org/>
- **GitHub Actions for CI**: <https://github.com/features/actions>
