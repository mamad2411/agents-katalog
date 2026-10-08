# Parallel Experiment Optimizer

A reference implementation skill demonstrating TeaAgent's parallel experiment capabilities for algorithm optimization.

## Use Case

When optimizing algorithms or hyperparameters, you often need to test multiple approaches simultaneously. This skill uses TeaAgent's `ParallelExperimentStack` to:
- Create isolated Git branches for each optimization strategy
- Run experiments in parallel
- Compare results using a quality matrix (compilation, tests, performance)
- Select the best approach and merge it back

## Capabilities

- **Parallel Branch Creation**: Creates isolated sandbox branches for each experiment
- **Quality Matrix Evaluation**: Compiles code, runs tests, measures performance
- **Automated Selection**: Chooses the best result based on configurable metrics
- **Cleanup**: Automatically removes failed experiment branches

## Usage

```bash
teaagent agent run --parallel "strategy-a,strategy-b,strategy-c" --task "Optimize the sorting algorithm"
```

## Example Workflow

1. Define your optimization strategies in a configuration file
2. Run the skill with parallel experiment options
3. Review the quality matrix output
4. The skill automatically selects the best performing strategy
5. Failed branches are cleaned up automatically

## Requirements

- Git repository initialized
- TeaAgent with parallel experiment support
- Python project with test suite

## Quality Matrix Metrics

- **Compilation Success**: Does the code compile without errors?
- **Test Pass Rate**: Percentage of tests passing
- **Performance**: Execution time (lower is better)
- **Code Quality**: Linter checks (if configured)

## Author

TeaEntityLab

## License

MIT
