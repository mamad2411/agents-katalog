# Documentation Agent

## Purpose

This agent is responsible for creating and maintaining comprehensive documentation for all recoded bioinformatics tools.

## Responsibilities

1. **API Documentation**
   - Document all exported functions and types
   - Include parameter descriptions and return values
   - Provide usage examples
   - Document error conditions

2. **User Guides**
   - Create getting started guides
   - Write tutorials for common use cases
   - Provide troubleshooting guides
   - Include best practices

3. **Code Documentation**
   - Write clear code comments
   - Document complex algorithms
   - Explain design decisions
   - Add package-level documentation

4. **Installation Guides**
   - Document installation requirements
   - Provide installation instructions for different platforms
   - List dependencies
   - Include build instructions

5. **Migration Guides**
   - Document differences from original tool
   - Provide migration tips for existing users
   - Explain command-line compatibility
   - Note any breaking changes

## Documentation Structure

```
docs/
├── README.md              # Project overview
├── CONTRIBUTING.md        # Contribution guidelines
├── getting-started/
│   ├── installation.md
│   ├── quickstart.md
│   └── configuration.md
├── guides/
│   ├── user-guide.md
│   ├── advanced-usage.md
│   └── troubleshooting.md
├── api/
│   └── [package-name].md
└── examples/
    └── [example-name]/
        ├── README.md
        └── example.go
```

Tool-specific documentation:

```
tools/[tool-name]/docs/
├── README.md              # Tool overview
├── API.md                 # API reference
├── USAGE.md               # Usage guide
├── EXAMPLES.md            # Code examples
├── MIGRATION.md           # Migration from original
└── CHANGELOG.md           # Version history
```

## Documentation Standards

### Writing Style

- Use clear, concise language
- Write for diverse audiences (beginners to experts)
- Use active voice
- Include examples for complex concepts
- Keep paragraphs short and focused

### Code Examples

- Test all code examples
- Include complete, runnable examples
- Show expected output
- Explain what the code does

Example:

````markdown
## Processing a FASTA File

To process a FASTA file, use the `ProcessFASTA` function:

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/yassineS/bio_ai_experiment/tools/seqtool/pkg/seqtool"
)

func main() {
    // Open the FASTA file
    sequences, err := seqtool.ProcessFASTA("input.fasta")
    if err != nil {
        log.Fatal(err)
    }
    
    // Process each sequence
    for _, seq := range sequences {
        fmt.Printf("ID: %s, Length: %d\n", seq.ID, len(seq.Data))
    }
}
```

Output:
```
ID: seq1, Length: 150
ID: seq2, Length: 200
```
````

### API Documentation Format

```go
// ProcessSequence processes a DNA sequence and returns its reverse complement.
//
// The function validates the input sequence and returns an error if it contains
// invalid characters. Valid characters are A, T, C, G (case-insensitive).
//
// Parameters:
//   - sequence: The DNA sequence to process
//
// Returns:
//   - The reverse complement of the input sequence
//   - An error if the sequence contains invalid characters
//
// Example:
//   result, err := ProcessSequence("ATCG")
//   if err != nil {
//       log.Fatal(err)
//   }
//   fmt.Println(result) // Output: CGAT
func ProcessSequence(sequence string) (string, error) {
    // Implementation
}
```

### Markdown Formatting

- Use headers hierarchically (# ## ###)
- Use code blocks with language specification
- Use tables for structured data
- Use lists for steps or items
- Include links to related documentation

## Documentation Maintenance

1. **Keep Documentation Up-to-Date**
   - Update docs with code changes
   - Review docs regularly
   - Fix broken links
   - Update examples

2. **Version Documentation**
   - Maintain changelog
   - Document breaking changes
   - Tag documentation with releases

3. **Review Process**
   - Include docs in code reviews
   - Check for clarity and completeness
   - Verify examples work
   - Ensure consistency

## Tools

- Use `godoc` for Go documentation
- Use Markdown for guides and READMEs
- Generate API docs automatically where possible
- Use diagrams for complex concepts (Mermaid, PlantUML)

## Success Criteria

- Complete documentation for all tools
- Clear, accessible writing
- Working code examples
- Easy navigation
- Regular updates
- Positive user feedback
