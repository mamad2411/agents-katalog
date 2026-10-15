---
name: serena-mcp
description: |
  Use this skill whenever working with the Serena MCP tools for semantic code analysis, intelligent code editing, refactoring, architecture analysis, or any codebase project work. Trigger this skill when the user wants to understand code structure, find symbols or references, search patterns across a codebase, safely rename or refactor code, analyze module dependencies, run code quality checks, map architecture, generate documentation from code, or perform any multi-step workflow on a code project using Serena. Always use this skill when Serena MCP tools are available and the task involves exploring, understanding, or editing code — even if the user does not explicitly say "use Serena".
---

# Serena MCP - Semantic Code Analysis & Editing

Serena is a Model Context Protocol (MCP) server providing semantic code analysis via Language Server Protocol (LSP). It understands code structure at a symbolic level — far more efficient and safe than reading raw files.

## Session Startup (Always Do This First)

```
1. serena:activate_project("/path/to/project")
2. serena:check_onboarding_performed()        # If false → serena:onboarding()
3. serena:list_memories()                      # Read relevant memories
4. serena:read_memory("project_overview")      # Understand project context
```

## Core Workflow Pattern

**Understand → Analyze → Plan → Edit → Verify**

```
# Step 1: Understand a file
get_symbols_overview("path/to/File.kt", depth=0)

# Step 2: Find target symbol
find_symbol("ClassName", depth=1, include_body=false)

# Step 3: Read specific code
find_symbol("ClassName/methodName", include_body=true)

# Step 4: Check dependencies before any change
find_referencing_symbols("ClassName/methodName", "path/to/File.kt")

# Step 5: Make targeted edit
replace_symbol_body("ClassName/methodName", "path/to/File.kt", "new code")

# Step 6: Verify & document
search_for_pattern("OldName", restrict_search_to_code_files=true)
write_memory("refactoring/change_name", "## What changed and why")
```

---

## Essential Tools — Quick Reference

| Task | Tool |
|------|------|
| Get file overview | `get_symbols_overview(file, depth=0)` |
| Find a symbol | `find_symbol(name, relative_path, depth=1)` |
| Read symbol code | `find_symbol(name, include_body=true)` |
| Find who uses a symbol | `find_referencing_symbols(name, exact_file_path)` |
| Search codebase | `search_for_pattern(regex, relative_path, restrict_search_to_code_files=true)` |
| Replace a method/class | `replace_symbol_body(name_path, file, new_body)` |
| Small text replacement | `replace_content(file, old_str, new_str)` |
| Safe rename everywhere | `rename_symbol(name, file, new_name)` |
| Store findings | `write_memory("topic/subtopic", "## Markdown content")` |
| Run build/test | `execute_shell_command("./gradlew test")` |

---

## Recipes

For detailed, copy-paste ready workflows, read the reference file:
→ **`references/recipes.md`** — 16 proven recipes organized by category

### Recipe Categories
- **Large-Scale Refactoring** (Recipes 1–3): API migration, interface extraction, deduplication
- **Architecture Analysis** (Recipes 4–6): Module dependency mapping, layer violations, dependency graphs
- **Test Coverage** (Recipes 7–8): Find untested code, analyze test organization
- **Code Quality** (Recipes 9–10): Anti-pattern detection, lint-like analysis
- **Multi-File Refactoring** (Recipes 11–12): Safe rename, move class to new package
- **Performance** (Recipes 13–14): Identify bottlenecks, optimize collection operations
- **Documentation** (Recipes 15–16): Generate module docs, create architecture diagrams

### Quick-Start Recipes (Inline)

**Add logging to a method:**
```
find_symbol("ClassName/methodName", include_body=true)
replace_symbol_body("ClassName/methodName", "file.kt",
  "fun methodName(...) {\n  Timber.d('methodName called')\n  // original body\n}")
```

**Find all instances of an annotation:**
```
search_for_pattern("@HiltViewModel|@Composable",
  relative_path="app/src/main/java/com/myapp/modules",
  restrict_search_to_code_files=true,
  context_lines_after=1)
```

**Safe class rename:**
```
find_referencing_symbols("OldName", "app/src/.../OldName.kt")
rename_symbol("OldName", "app/src/.../OldName.kt", "NewName")
search_for_pattern("OldName", restrict_search_to_code_files=true)
```

**Map module dependencies:**
```
list_dir("app/src/main/java/com/myapp/modules", recursive=false)
search_for_pattern("^import.*modules\.", relative_path="modules/eventList/",
  context_lines_before=0)
write_memory("architecture/module_dependencies", "## Module Dependencies\n...")
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Reading entire files first | Use `get_symbols_overview()` first |
| Editing without checking references | Always `find_referencing_symbols()` before changing |
| Skipping memories | Read `style_and_conventions` before any edit |
| Searching entire codebase | Use `relative_path` to restrict scope |
| Using `include_body=true` broadly | Get overview first, then body for specific symbols |

---

## Modes

```
switch_modes(["editing", "interactive"])   # When making changes
switch_modes(["planning"])                 # When thinking through approach
switch_modes(["no-memories"])              # When memories are not needed
```

---

## Tool Parameters Cheat Sheet

**`find_symbol`** key params:
- `name_path_pattern`: `"ClassName"`, `"ClassName/method"`, or `"/ExactPath"`
- `depth`: `0` = symbol only, `1` = symbol + children (use this most)
- `include_body`: `true` only when you need the source code

**`search_for_pattern`** key params:
- `substring_pattern`: Regex (e.g., `"@Inject|@HiltViewModel"`)
- `restrict_search_to_code_files`: Always `true` for code searches
- `context_lines_after`: `2-3` to understand surrounding code

**`find_referencing_symbols`** key params:
- `relative_path`: Must be the **exact file path**, not a directory

---

## Memory Strategy

Use memories to persist project knowledge across sessions:
```
write_memory("architecture/module_dependencies", "## eventList → circles, notifications")
write_memory("refactoring/api_migration_2026", "## Old → New API\n- Status: Complete")
write_memory("conventions/naming", "## Naming Rules\n- ViewModels: *ViewModel\n- Use cases: *UseCase")
```

---

## Full Reference

Read `references/recipes.md` for complete, step-by-step versions of all 16 recipes including the full **Codebase Audit** workflow that combines architecture analysis, code quality checks, technical debt tracking, and action planning into a single comprehensive session.
