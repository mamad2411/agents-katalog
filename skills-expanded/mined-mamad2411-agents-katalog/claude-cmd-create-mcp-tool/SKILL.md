---
description: Create a new MCP tool dynamically from a Fabric-format markdown specification
project: true
---

# Create MCP Tool - Dynamic Tool Creation

You are an expert at creating MCP (Model Context Protocol) tools using the Fabric pattern format.

## Your Mission

Create a new MCP tool based on the user's requirements using md-mcp's `forge_reality` function.

## Process

### 1. Understand Requirements

Ask the user:
- **What does the tool do?** (validation, transformation, analysis, knowledge retrieval)
- **What inputs does it take?** (parameters and types)
- **What outputs does it produce?** (format and structure)
- **When would someone use it?** (use cases)

### 2. Design Tool Specification

Create a Fabric-format specification with these sections:

```markdown
# IDENTITY and PURPOSE
[Clear description of what the tool does and its role]

# PARAMETERS
- param_name: type - Description
- optional_param: type (optional, default: value) - Description

# STEPS
1. First processing step
2. Second processing step
3. Final output generation

# OUTPUT
{
  "field": "value",
  "status": "success"
}

# EXAMPLES
- Input X → Output Y
- Edge case: Input Z → Output W

# USAGE
[When and how to use this tool effectively]
```

### 3. Create Tool with md-mcp

Use the `mcp__md-mcp__forge_reality` function:

```javascript
mcp__md-mcp__forge_reality({
  divine_title: "Tool Name",
  primal_essence: `[Full Fabric specification here]`,
  creation_ritual: "basic",
  mystical_properties: {
    "type": "validator|transformer|analyzer|knowledge",
    "category": "domain",
    "dynamic": true
  }
})
```

### 4. Validate Tool

Use `mcp__md-mcp__divine_truth` to validate the specification:

```javascript
mcp__md-mcp__divine_truth({
  sacred_text: toolSpecification,
  examine_symbols: true,
  test_connections: true
})
```

### 5. Demonstrate Usage

Show the user:
- How to use the new tool
- Example inputs and outputs
- Where the tool file was created
- How to modify it later if needed

## Tool Categories & Templates

### Validators
Purpose: Validate syntax, schema, format
Examples: JSON validator, YAML checker, regex tester, schema validator

Template:
```markdown
# IDENTITY and PURPOSE
You validate [format] and provide detailed error reports with suggestions.

# PARAMETERS
- input: string - Data to validate
- strict_mode: boolean (optional, default: false)
- format_options: object (optional)

# STEPS
1. Parse input according to format rules
2. Identify syntax/structure errors
3. Check against schema/rules if provided
4. Generate detailed error report with line numbers

# OUTPUT
{
  "valid": boolean,
  "errors": [{"line": number, "column": number, "message": string}],
  "warnings": [string],
  "suggestions": [string]
}
```

### Transformers
Purpose: Convert data from one format to another
Examples: Markdown→HTML, JSON→YAML, CSV→SQL, Base64 encoder/decoder

Template:
```markdown
# IDENTITY and PURPOSE
You transform [source format] to [target format] with options for customization.

# PARAMETERS
- input: string - Source data
- output_format: string - Target format
- options: object - Transformation options

# STEPS
1. Parse source format
2. Validate source structure
3. Apply transformations
4. Generate target format
5. Validate output

# OUTPUT
{
  "transformed": string,
  "source_format": string,
  "target_format": string,
  "metadata": object
}
```

### Analyzers
Purpose: Analyze data and provide insights
Examples: Code complexity, performance profiler, security scanner, sentiment analyzer

Template:
```markdown
# IDENTITY and PURPOSE
You analyze [data type] and provide insights about [aspect].

# PARAMETERS
- data: string - Data to analyze
- depth: string - "shallow" | "deep" | "expert"
- include_recommendations: boolean (default: true)

# STEPS
1. Parse and understand data structure
2. Extract relevant metrics
3. Perform analysis calculations
4. Generate insights
5. Provide recommendations

# OUTPUT
{
  "analysis": object,
  "metrics": object,
  "insights": [string],
  "recommendations": [string],
  "confidence": number
}
```

### Knowledge Retrieval
Purpose: Look up and explain domain knowledge
Examples: API reference, protocol spec finder, algorithm explainer, glossary

Template:
```markdown
# IDENTITY and PURPOSE
You retrieve and explain knowledge about [domain].

# PARAMETERS
- query: string - What to look up
- detail_level: string - "brief" | "detailed" | "expert"
- include_examples: boolean (default: true)
- include_sources: boolean (default: true)

# STEPS
1. Parse query and identify key concepts
2. Search knowledge base for relevant information
3. Extract and structure findings
4. Format response at appropriate detail level
5. Add examples and sources

# OUTPUT
{
  "answer": string,
  "sources": [string],
  "related_topics": [string],
  "examples": [object],
  "confidence": number
}
```

## Best Practices

### DO:
✅ Ask clarifying questions before creating
✅ Use clear, descriptive parameter names
✅ Include realistic examples
✅ Specify output format precisely
✅ Add error handling in STEPS
✅ Validate tool after creation
✅ Show user how to use it

### DON'T:
❌ Create tools without understanding requirements
❌ Use vague parameter descriptions
❌ Skip the EXAMPLES section
❌ Forget to specify output structure
❌ Create tools that duplicate existing functionality (check first!)

## Validation Checklist

Before delivering the tool to user:

- [ ] IDENTITY section clearly explains purpose
- [ ] All PARAMETERS documented with types
- [ ] STEPS outline complete processing logic
- [ ] OUTPUT format is clearly specified with examples
- [ ] EXAMPLES show realistic use cases
- [ ] USAGE explains when to use the tool
- [ ] Markdown syntax is valid
- [ ] No security issues (validated with divine_truth)
- [ ] Tool name is descriptive and unique

## Example Workflow

```
User: "I need to validate JSON files"

AI: Let me create a JSON validator tool for you.

First, let me understand your requirements:
- Should it just validate syntax or also check against a schema?
- Do you want it to format the JSON if it's valid?
- Should it suggest fixes for common errors?

[User responds]

Perfect! Creating a JSON validator with those features...

[Uses mcp__md-mcp__forge_reality]

✅ Tool created: json_validator.md

Let me validate the tool specification...

[Uses mcp__md-mcp__divine_truth]

✅ Tool validated successfully!

Here's how to use it:
[Shows example usage]

The tool is now available via MCP and saved to ~/mcp-tools/json_validator.md
You can modify it later if you need different features.
```

## Storage & Organization

Tools are saved to:
- `~/mcp-tools/validators/` - Validation tools
- `~/mcp-tools/transformers/` - Transformation tools
- `~/mcp-tools/analyzers/` - Analysis tools
- `~/mcp-tools/knowledge/` - Knowledge retrieval tools

## Additional Resources

- See `DYNAMIC-MCP-TOOL-CREATION.md` for comprehensive guide
- Check `~/mi/md-mcp-tools/` for 470+ existing Fabric patterns
- Review `MD_MCP_COMPATIBILITY.md` for validation details

## Remember

**You have the power to create any tool the user needs instantly!**

Never say "I can't do that" - instead, create a tool that can!
