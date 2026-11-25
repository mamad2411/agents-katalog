---
description: a list of rules that need to be reviewed before every command
globs: *.*
---
serialization-rules: Best practices for JSON serialization, including enum handling and migration strategies 

# Available Instructions

The following rules are available for use in this codebase:

cursor-rules-location: Guidelines for organizing and managing Cursor rules
no-late-keyword-rule: Best practices for avoiding the late keyword and alternative patterns
serialization-rules: Best practices for JSON serialization, including enum handling and migration strategies

## Usage

To use these rules in your code, you can:
1. Reference them directly in your code comments
2. Use the fetch_rules tool with the rule name
3. Follow their guidelines in your implementations

## Rule Summaries

### cursor-rules-location
- Defines the structure and organization of Cursor rules
- Explains how to create and maintain rule documentation
- Provides guidelines for rule naming and formatting

### no-late-keyword-rule
- Prohibits use of the `late` keyword to prevent runtime errors
- Provides alternative patterns like factory constructors and computed properties
- Defines exceptions and enforcement mechanisms

### serialization-rules
- Guidelines for JSON serialization implementation
- Best practices for handling enums and migrations
- Strategies for maintaining backward compatibility 
