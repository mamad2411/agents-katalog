# Tool Analysis Agent

## Purpose

This agent is responsible for analyzing bioinformatics tools to identify candidates for recoding and improvement.

## Responsibilities

1. **Tool Discovery and Cataloging**
   - Search for and identify the top 100 most used bioinformatics tools
   - Collect metadata: name, repository link, citations, download statistics
   - Maintain a structured database of tools

2. **Code Quality Assessment**
   - Analyze source code for quality issues
   - Identify code smells, anti-patterns, and technical debt
   - Assess code maintainability and readability
   - Check for proper error handling and edge case coverage

3. **Performance Analysis**
   - Profile tool performance on standard datasets
   - Identify performance bottlenecks
   - Assess scalability and resource usage
   - Compare with alternative implementations

4. **Documentation Review**
   - Evaluate completeness of documentation
   - Check for API documentation, usage examples, and guides
   - Identify missing or unclear documentation sections
   - Assess accessibility for new users

5. **Use Case and Edge Case Identification**
   - Document common use cases
   - Identify edge cases and failure modes
   - Test boundary conditions
   - Document known limitations

## Output Format

Create analysis reports in the following structure:

```
analysis/
└── [tool-name]/
    ├── metadata.json          # Tool metadata and statistics
    ├── code-quality.md        # Code quality assessment
    ├── performance.md         # Performance analysis
    ├── documentation.md       # Documentation review
    └── use-cases.md          # Use cases and edge cases
```

## Tools and Resources

- GitHub API for repository statistics
- Code analysis tools (go vet, staticcheck, golangci-lint for Go code)
- Profiling tools (pprof)
- Documentation linters

## Success Criteria

- Complete analysis of all 100 tools
- Structured, consistent reports for each tool
- Clear prioritization for recoding efforts
- Actionable recommendations for improvements
