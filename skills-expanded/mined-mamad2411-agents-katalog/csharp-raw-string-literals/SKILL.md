---
name: csharp-raw-string-literals
description: >
  Use C# raw string literals (""" … """) and interpolated raw strings for SQL,
  JSON, HTML, and multi-line test data in owned .NET code. Use when improving
  readability of embedded payloads, fixing indentation with end-delimiter rules,
  or choosing between raw strings, verbatim @"", and ordinary strings — without
  turning string concat into SQL/XSS injection.
---

# C# Raw String Literals

## Scope And Authorization

- **In scope:** C# language usage in codebases you maintain (C# 11+).
- **Out of scope:** Using raw strings to hide secrets in source; treating raw SQL strings as safe parameterization.
- Pair with `csharp-style-conventions` and `code-quality-standards`; use SQL parameterization skills for queries.

## When To Use

- Multi-line JSON/XML/HTML fixtures in tests.
- Embedded DSL snippets (GraphQL, YAML) in source generators or tests.
- Improving escape hell from nested quotes.
- Aligning indentation of multi-line content with the closing `"""`.
- Interpolated raw strings `$"""...{expr}..."""` carefully.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SQL injection prevention | sqli / parameterized query practices |
| XSS prevention | `xss-cross-site-scripting` |
| Required members / init models | `csharp-required-members` |
| Style broadly | `csharp-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Syntax essentials

| Form | Notes |
| --- | --- |
| `"""content"""` | Raw string; no escape processing for `\` |
| `""""...""""` | More quotes when content contains `"""` |
| `$"""...{x}..."""` | Interpolation; still format-safe for display only |
| `$$"""...{{x}}..."""` | Double `$` changes interpolation braces |

Closing delimiter column defines **minimum indentation stripped** from content lines.

## Workflow

### 1. Confirm scope

1. LangVersion ≥ 11 / TFM supporting raw strings.
2. Success: readable literals; tests pass; no accidental whitespace regressions; no security sink misuse.

### 2. Replace painful literals

```csharp
// Before: verbose escapes
var json = "{\r\n  \"name\": \"Ada\",\r\n  \"id\": 1\r\n}";

// After
var json = """
    {
      "name": "Ada",
      "id": 1
    }
    """;
```

### 3. Indentation rules

```csharp
// Content indented relative to closing """
var sql = """
    SELECT id, name
    FROM users
    WHERE active = 1
    """;
// Leading whitespace common to all lines (based on closing delimiter) is removed
```

Verify exact string in tests when whitespace matters (snapshots, hashes).

### 4. Interpolation without injection

```csharp
// OK for logging / test names
var msg = $"""
    User {userId} updated
    """;

// NOT a substitute for SQL parameters:
// BAD: $"""SELECT * FROM users WHERE id = {userId}"""
// GOOD: command.Parameters.AddWithValue("@id", userId) with fixed SQL text
var sql = """
    SELECT * FROM users WHERE id = @id
    """;
```

Same rule for HTML: raw strings do not HTML-encode `{name}`.

### 5. Content containing quotes

```csharp
var text = """
    He said "hello"
    """;

var containsTriple = """"
    Contents may include """ markers
    """";
```

### 6. Refactor checklist

1. Prefer raw strings for multi-line fixed content.
2. Keep single-line simple strings as `"..."`.
3. Do not embed secrets/tokens in literals.
4. For localization, use resource files, not giant raw strings in code.

### 7. Verify

```bash
dotnet test
dotnet format
# Snapshot tests if whitespace-critical
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| JSON fixtures | Raw string + parse | Slash-escape nightmares |
| SQL | Raw text + parameters | Interpolated user input into SQL |
| Indent | Align with closing `"""` | Mixed tabs breaking expected content |
| Secrets | Config providers | API keys in `"""` |
| Quotes | Increase quote count | Manual `\"` soup for multi-line |

## Output Checklist

- [ ] LangVersion supports raw strings
- [ ] Multi-line literals migrated where clarity wins
- [ ] Whitespace expectations tested
- [ ] No interpolated injection sinks introduced
- [ ] Quote-count cases handled
- [ ] Secrets not introduced in source
- [ ] Style consistent with team conventions
- [ ] Build/tests green
- [ ] Docs/examples updated if public API samples
- [ ] Residual risks noted

## Rules

- Raw strings improve readability, not security boundaries.
- Never “parameterize” SQL/HTML with interpolation alone.
- Focus on **C# raw string literal usage**.
