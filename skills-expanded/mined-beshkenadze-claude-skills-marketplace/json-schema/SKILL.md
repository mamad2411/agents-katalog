---
name: json-schema
description: Generate and validate JSON Schema definitions. Use when asked to create schemas, validate JSON structure, or document API payloads.
version: 1.0.0
---

# JSON Schema Generator

## Overview

Creates JSON Schema definitions for data validation and API documentation.

## Instructions

When generating JSON Schema:

1. **Analyze the data structure** or requirements
2. **Determine types** for each field (string, number, object, array, etc.)
3. **Add constraints**: required fields, patterns, min/max values
4. **Include descriptions** for documentation
5. **Set appropriate `$schema`** version (draft-07 recommended)

## Schema Components

### Basic Types
- `string` - Text values
- `number` / `integer` - Numeric values
- `boolean` - True/false
- `object` - Nested structures
- `array` - Lists of items
- `null` - Null values

### Common Constraints
- `required` - Mandatory fields
- `minLength` / `maxLength` - String length
- `minimum` / `maximum` - Number bounds
- `pattern` - Regex validation
- `enum` - Allowed values
- `format` - Semantic formats (email, uri, date-time)

## Examples

### Example: User Schema

**Input:**
"Create a schema for a user with name, email, age, and optional phone"

**Output:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "User",
  "type": "object",
  "required": ["name", "email", "age"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "User's full name"
    },
    "email": {
      "type": "string",
      "format": "email",
      "description": "User's email address"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150,
      "description": "User's age in years"
    },
    "phone": {
      "type": "string",
      "pattern": "^\\+?[1-9]\\d{1,14}$",
      "description": "Optional phone number in E.164 format"
    }
  },
  "additionalProperties": false
}
```

## Guidelines

### Do
- Always include `$schema` declaration
- Add descriptions for all properties
- Use `additionalProperties: false` for strict validation
- Prefer specific formats over loose patterns
- Use `required` array for mandatory fields

### Don't
- Use overly permissive types (avoid `{}` or `true`)
- Skip validation constraints on user input
- Mix draft versions in same schema
- Forget to handle nullable fields explicitly
