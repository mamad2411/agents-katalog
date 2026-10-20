---
name: "caveman-token-reduction"
description: "Claude Code Caveman mode: token-efficient communication, compressed responses, minimal output for context-heavy sessions, terse acknowledgments, and context budget optimization"
---

# Caveman — Token Reduction Mode

## When to activate
- Context window is above 70% capacity and you need to extend the session
- Working on a large codebase where tool outputs (file reads, grep results) dominate context
- Multi-step tasks where intermediate responses waste context budget
- User explicitly requests terse/minimal responses
- Running cost-sensitive sessions where token usage matters
- Long debugging sessions where you need maximum context for logs and traces

## When NOT to use
- First interaction on a new session with plenty of context headroom
- When the user is learning and needs detailed explanations
- Documentation generation or tutorial writing (verbosity is the product)
- When communicating with stakeholders who need full context
- Complex architectural discussions that require nuanced reasoning

## Instructions

### 1. Response Compression Levels

| Level | Name | Tokens/response | Use when |
|-------|------|-----------------|----------|
| 0 | Normal | 200-500 | Default, ample context |
| 1 | Concise | 50-150 | Context > 50%, routine tasks |
| 2 | Terse | 15-50 | Context > 70%, repetitive operations |
| 3 | Caveman | 5-15 | Context > 85%, emergency mode |

### 2. Level 1: Concise Mode

**Normal response:**
```
I've reviewed the authentication middleware in src/auth/middleware.ts. 
There are three issues I found:
1. The JWT verification on line 23 doesn't check the token expiration, 
   which means expired tokens will still be accepted.
2. The error handler on line 45 catches all errors but returns a generic 
   500 instead of distinguishing between auth failures and server errors.
3. The CORS configuration allows all origins, which is too permissive 
   for production.

I recommend fixing these in order of severity. Want me to proceed?
```

**Concise response:**
```
src/auth/middleware.ts — 3 issues:
1. L23: JWT expiry not checked (expired tokens accepted)
2. L45: Generic 500 for all errors (should be 401 vs 500)
3. L12: CORS allows all origins (too permissive for prod)

Fix in order?
```

### 3. Level 2: Terse Mode

```
auth/middleware.ts: 3 bugs
- L23: no expiry check
- L45: 500 for all errors (need 401/500 split)
- L12: CORS wildcard (prod risk)
Fix?
```

### 4. Level 3: Caveman Mode

```
auth fix: 3 bugs (L12,L23,L45). Fix all?
```

### 5. Acknowledgment Compression

| Full | Concise | Terse | Caveman |
|------|---------|-------|---------|
| "I've completed the task and all tests are passing." | "Done. Tests pass." | "Done ✓" | "✓" |
| "I've read the file and understand the structure." | "Read." | "Read" | "👁" |
| "That file doesn't exist, let me search for it." | "Not found. Searching..." | "Missing, searching" | "∅→🔍" |
| "I've made the requested changes and committed them." | "Committed." | "Committed" | "git✓" |

### 6. Tool Output Compression

**Compress grep/read results before including in response:**

```yaml
compression_rules:
  file_reads:
    - omit_lines: "unchanged/import/header"
    - show_only: "modified + context (3 lines)"
    - max_lines: 30  # never show more than 30 lines from a read
    
  grep_results:
    - max_matches: 10  # summarize beyond this
    - group_by: "file"
    - format: "file:line:match (not full line content)"
    
  bash_output:
    - tail_lines: 20   # last 20 lines of output
    - on_success: "exit 0"  # just the exit code
    - on_failure: "last 20 lines + exit code"
```

### 7. Context Budget Management

**Monitor and report context usage:**

```yaml
context_monitor:
  check_every: 10_turns
  thresholds:
    50_percent: "switch to concise"
    70_percent: "switch to terse, summarize old context"
    85_percent: "switch to caveman, aggressively compress"
    95_percent: "suggest handoff to new session"
  
  report_format: "ctx: 72% | mode: terse | ~45 turns remaining"
```

**Automatic context cleanup:**
```yaml
auto_cleanup:
  when: "context > 70%"
  actions:
    - summarize_conversation: "compress turns 1-50 into 10-line summary"
    - drop_tool_results: "keep only most recent 5 tool outputs in full"
    - compress_file_reads: "replace full reads with line-range references"
```

### 8. Batch Operation Compression

**Instead of reporting each step in a batch:**
```
Normal:
  1/10: Created src/api/users.ts ✓
  2/10: Created src/api/products.ts ✓
  3/10: Created src/api/orders.ts ✓
  ...

Caveman:
  10/10 files created ✓
```

**Instead of confirming each file read:**
```
Normal:
  Read package.json (45 lines)
  Read tsconfig.json (22 lines)
  Read .eslintrc.json (18 lines)

Caveman:
  Read 3 configs ✓
```

### 9. When to Expand Back

Automatically return to normal verbosity when:
- User asks a conceptual question ("Why did you choose X?")
- User says "explain" or "more detail"
- A critical error occurs that needs full context
- Context usage drops below 40% (after summarization/cleanup)
- Starting a new task within the same session

## Example

**Long debugging session in caveman mode:**

```
User: "The API is returning 500 on /users endpoint. Debug it."

Agent (normal): Read error logs, identified 3 issues in the request chain...
User: "Go caveman mode, we have a lot to debug"

Agent: "logs: 3 errs. L47 null ref in userRepo. Fix?"
User: "yes"
Agent: "fixed. Test?"
User: "still failing"
Agent: "err2: L82 missing await. Fix?"
User: "yes"  
Agent: "fixed. ctx:68% mode:terse ~60 turns left"
User: "next error?"
Agent: "L115: unhandled promise reject in cache. wrap try/catch?"
User: "do it"
Agent: "✓ /users returns 200. All 3 fixed."
```

## Anti-Patterns

- **Caveman by default:** Starting every session in caveman mode hurts onboarding and discoverability — use only when context pressure is real
- **Losing meaning:** Compressing so aggressively that the response becomes ambiguous — "fix?" is fine, "?" alone is not
- **Ignoring user preference:** Staying in caveman mode when user asks for details — always expand when asked
- **Compression without context:** Using caveman mode with a new user who doesn't understand the abbreviations — match the user's familiarity level
- **Premature summarization:** Summarizing tool outputs that you'll need in full later — only compress results you've already processed
- **Silent context overflow:** Not warning the user when context is critical — always report context status at terse/caveman levels
