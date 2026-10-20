# GoLang Recoding Agent

## Purpose

This agent is responsible for recoding bioinformatics tools in Go, maintaining functionality while improving performance, maintainability, and code quality.

## Responsibilities

1. **Requirements Analysis**
   - Review original tool functionality
   - Document expected inputs and outputs
   - Identify dependencies and external requirements
   - Create functional specifications

2. **Architecture Design**
   - Design Go package structure
   - Plan module organization
   - Define interfaces and types
   - Create architecture diagrams

3. **Implementation**
   - Write clean, idiomatic Go code
   - Follow Go best practices and conventions
   - Implement concurrent operations where appropriate
   - Handle errors properly
   - Ensure memory efficiency

4. **Compatibility**
   - Maintain command-line interface compatibility
   - Support original file formats
   - Preserve expected behavior
   - Document any intentional changes

5. **Code Quality**
   - Write self-documenting code
   - Add appropriate comments for complex logic
   - Follow project style guide
   - Use meaningful variable and function names

## Implementation Guidelines

### Code Structure

The repository is a **single Go module** — there is **no per-tool `go.mod`**,
and tests live inline as `*_test.go` next to the code (no separate `tests/`
or per-tool `docs/` subtree). The actual layout is:

```
tools/<tool>/
├── cmd/
│   └── <tool>/
│       └── main.go           # CLI entry point (arg parsing + wiring only)
├── pkg/
│   └── <tool>/
│       ├── <tool>.go         # tool logic (split into focused files)
│       └── <tool>_test.go    # inline table-driven tests
└── README.md                 # usage + parity notes
```

Shared format parsing/writing lives under `pkg/htsgo/`; reuse it rather than
re-implementing FASTA/FASTQ/VCF/BED/SAM/BAM/BCF/BGZF handling.

### Coding Standards

- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use `gofmt` for formatting
- Run `go vet` and `staticcheck` before committing
- Aim for >80% test coverage
- Document all exported functions and types

### Performance Considerations

- Use goroutines for parallelizable operations
- Implement proper buffering for I/O operations
- Profile and optimize hot paths
- Use appropriate data structures
- Avoid unnecessary allocations

## Success Criteria

- Functional parity with original tool
- Improved performance (benchmarked)
- Clean, maintainable code
- Comprehensive test coverage
- Complete documentation
