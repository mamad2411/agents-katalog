# Agent Coordination Guide

## Overview

This document describes how different agents coordinate to achieve the project goals. Each agent has specific responsibilities, and they work together in a structured workflow.

## Agent Roles

### 1. Tool Analysis Agent

**Primary Focus**: Research and analysis

- Identifies and catalogs bioinformatics tools
- Assesses code quality, performance, and documentation
- Prioritizes tools for recoding

**Outputs**: Analysis reports, tool databases, priority lists

**Dependencies**: None (starting point)

### 2. GoLang Recoding Agent

**Primary Focus**: Implementation

- Recodes tools in Go
- Maintains functional compatibility
- Optimizes performance

**Outputs**: Go source code, build scripts

**Dependencies**: Tool Analysis Agent (receives tool specifications)

### 3. Testing Agent

**Primary Focus**: Quality assurance

- Creates comprehensive test suites
- Validates functionality
- Ensures code coverage

**Outputs**: Test code, test data, test reports

**Dependencies**: GoLang Recoding Agent (receives code to test)

### 4. Documentation Agent

**Primary Focus**: Knowledge capture

- Documents code and APIs
- Creates user guides
- Maintains project documentation

**Outputs**: Documentation files, API references, guides

**Dependencies**: All agents (documents their outputs)

### 5. MCP Server Agent

**Primary Focus**: Integration

- Creates MCP servers for tools
- Enables LLM integration
- Simplifies tool access

**Outputs**: MCP servers, integration docs

**Dependencies**: GoLang Recoding Agent, Testing Agent

## Workflow

### Phase 1: Discovery and Analysis

```
Tool Analysis Agent
    ├── Identify top 100 tools
    ├── Gather metadata (citations, downloads, links)
    ├── Analyze code quality
    ├── Assess performance
    ├── Review documentation
    └── Identify use cases and edge cases
    
Output: Prioritized list of tools with detailed analysis
```

### Phase 2: Planning

```
Tool Analysis Agent + Documentation Agent
    ├── Create detailed specifications for selected tool
    ├── Document expected behavior
    ├── Identify test cases
    └── Create implementation plan
    
Output: Tool specification document
```

### Phase 3: Implementation

```
GoLang Recoding Agent
    ├── Design Go architecture
    ├── Implement core functionality
    ├── Implement CLI interface
    ├── Optimize performance
    └── Self-review code
    
Parallel: Documentation Agent
    ├── Document code as it's written
    └── Create usage examples
    
Output: Working Go implementation with initial docs
```

### Phase 4: Testing

```
Testing Agent
    ├── Create test data
    ├── Write unit tests
    ├── Write integration tests
    ├── Write edge case tests
    ├── Run benchmarks
    └── Verify coverage
    
Parallel: Documentation Agent
    ├── Document test strategy
    └── Create testing guide
    
Output: Comprehensive test suite
```

### Phase 5: Integration

```
MCP Server Agent
    ├── Design MCP server
    ├── Implement tool wrappers
    ├── Create resource handlers
    ├── Test with LLM clients
    └── Optimize performance
    
Parallel: Documentation Agent
    ├── Document MCP server
    └── Create integration guide
    
Output: MCP server with documentation
```

### Phase 6: Iteration

```
All Agents
    ├── Review feedback
    ├── Identify improvements
    ├── Update code, tests, docs
    └── Re-deploy
    
Loop until: Tool is robust and well-documented
```

## Communication Between Agents

### Handoff Points

1. **Analysis → Recoding**
   - Tool specification document
   - Code quality report
   - Performance baseline

2. **Recoding → Testing**
   - Source code
   - Build instructions
   - Expected behavior description

3. **Testing → MCP Development**
   - Validated tool binaries
   - Test suite
   - Performance benchmarks

4. **All → Documentation**
   - Regular updates on progress
   - New features to document
   - Issues to note

### Shared Resources

- **Tool Database**: Central repository of tool metadata
- **Issue Tracker**: Track problems and improvements
- **Documentation Site**: Centralized documentation
- **Test Data Repository**: Shared test datasets

## Agent Collaboration Examples

### Example 1: New Tool Implementation

1. **Analysis Agent** identifies "FastQC" as a priority tool
2. **Analysis Agent** creates analysis report
3. **Documentation Agent** creates specification from analysis
4. **Recoding Agent** implements Go version
5. **Testing Agent** creates test suite
6. **Documentation Agent** writes user guide
7. **MCP Agent** creates MCP server
8. **All agents** iterate based on findings

### Example 2: Bug Fix

1. **Testing Agent** discovers edge case bug
2. **Recoding Agent** fixes the bug
3. **Testing Agent** adds test for edge case
4. **Documentation Agent** updates known issues
5. **MCP Agent** updates if server affected

### Example 3: Performance Optimization

1. **Testing Agent** identifies performance bottleneck
2. **Recoding Agent** optimizes code
3. **Testing Agent** validates improvement with benchmarks
4. **Documentation Agent** updates performance notes
5. **MCP Agent** adjusts resource limits if needed

## Quality Gates

Each phase has quality gates that must be passed before moving forward:

### Analysis Phase

- ✓ Tool metadata complete
- ✓ Code quality assessed
- ✓ Performance baseline established
- ✓ Documentation gaps identified
- ✓ Use cases documented

### Implementation Phase

- ✓ Code passes linting
- ✓ All exported items documented
- ✓ Unit tests pass
- ✓ Performance meets baseline
- ✓ CLI works as expected

### Testing Phase

- ✓ >80% code coverage
- ✓ All edge cases tested
- ✓ Integration tests pass
- ✓ Benchmarks recorded
- ✓ No critical bugs

### Integration Phase

- ✓ MCP server responds correctly
- ✓ LLM integration tested
- ✓ Error handling works
- ✓ Performance acceptable
- ✓ Documentation complete

## Success Metrics

Track these metrics across the project:

- Number of tools analyzed
- Number of tools recoded
- Average test coverage
- Documentation completeness
- MCP servers deployed
- Performance improvements achieved
- Agent effectiveness ratings

## Agent Feedback Loop

Agents continuously provide feedback to improve the process:

1. **What worked well?**
2. **What challenges were encountered?**
3. **What could be improved?**
4. **What was learned?**

This feedback informs process improvements and agent refinements.
