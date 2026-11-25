---
name: "how-to-script-it-instead"
description: "Guidance for writing batch scripts to replace repetitive tool call loops — covers discovering available runtimes and CLI tools, choosing the right scripting approach, and structuring efficient collect-then-reason workflows"
---


# Batch Scripting Instead of Tool Call Loops

You're here because you recognized you were about to loop tool calls over a mechanical operation. Good. This skill helps you write the script that replaces the loop.

## Step 1: Know What You Have

Before writing a script, confirm what the environment provides. Don't inventory everything — check what you need for the task at hand.

**Assume nothing about the platform.** POSIX baseline tools (`grep`, `awk`, `sed`, `find`, `sort`, `diff`, `xargs`, `cut`, `wc`, `head`, `tail`, `tee`) are available on Unix-like systems but not on Windows. When the platform is ambiguous, verify before depending on them.

**Distinguish API CLIs from manipulation CLIs — they are not interchangeable.**

*API CLIs* (`gh`, `aws`, `gcloud`, `az`, `kubectl`, `heroku`, `stripe`, `fly`, `vercel`, `docker`, etc.) are pre-authenticated, domain-aware interfaces to remote services. They carry the user's OAuth tokens, IAM sessions, or API keys. They know their service's pagination, rate limiting, error handling, and endpoint structure. They often have built-in batch modes (`gh api --paginate`, `aws s3 sync`, `kubectl get -o json`). **A runtime stdlib cannot cheaply substitute for these** — you'd have to reconstruct auth discovery, endpoint URLs, pagination cursors, and error handling from scratch. When your task involves a remote service, check for its API CLI first. If it's present, it is almost certainly the right tool.

*Manipulation CLIs* (`jq`, `yq`, `rg`, `fd`, `tree`, `csvkit`, etc.) are ergonomic shortcuts for data processing — JSON filtering, fast search, directory visualization, YAML parsing. They're nice to have and can make scripts dramatically shorter, but **they are fully replaceable by a runtime's stdlib.** `jq '.name'` and `python3 -c "import json; ..."` produce the same result. Check for them, use them when present, fall back without them.

**Runtime stdlibs are the universal fallback for data manipulation.** Once you confirm a runtime is available, your training knowledge of its standard library becomes your tool inventory. A single `python3 --version` check unlocks `json`, `csv`, `re`, `pathlib`, `glob`, `subprocess`, `tempfile`, `difflib`, `collections.Counter`, `xml.etree`, `sqlite3`, `http.client`, `shutil`, and more. A single `node --version` check unlocks `fs`, `path`, `child_process`, `JSON`, `os`, `url`, `readline`, `crypto`, `zlib`. Ruby's stdlib includes `yaml` (Psych), `json`, `csv`, `fileutils`, `open-uri`, `erb`, and `tempfile` — notably, Ruby is the only common runtime with YAML parsing in its stdlib, which matters in config-heavy environments.

**Never install tools to satisfy this optimization.** No `pip install`, no `npm install`, no `gem install`, no `brew install`. Use what the environment already provides. The goal is zero setup cost.

**If you need to check multiple things, check them in one tool call.** Write a small probe that tests for everything you need in a single execution. Don't fall into the very anti-pattern that brought you here by checking tools one at a time.

## Step 2: Choose Your Approach

**Decision order:**

1. **Can baseline shell tools handle this?** Simple filtering, counting, sorting, deduplication, file-finding — POSIX tools handle these without needing anything else. A `grep | sort | uniq -c` pipeline is often the whole answer.

2. **Does the task involve a remote service with a CLI?** Check for the API CLI. If present, prefer it — it carries auth, knows the API's idioms, and often supports batch/paginated operations natively. This is not a nice-to-have; rebuilding what `gh api --paginate '/repos/{owner}/{repo}/issues'` does with raw `curl` and token management is a waste of effort the CLI already solved.

3. **Does this involve data manipulation (JSON, CSV, XML, text transformation)?** Check for a manipulation CLI that fits the format. If present, use it for brevity. If not, confirm a runtime is available and use its stdlib. Python is the strongest general-purpose fallback. Node is strong when the task is JSON-centric or the project is already JS/TS. For YAML specifically, Ruby is the only runtime with stdlib support — otherwise you need a manipulation CLI.

4. **Does this need complex logic, branching, or error handling?** Use a runtime. Shell pipelines get brittle past a certain complexity threshold. A 10-line Python script is clearer and more reliable than a 10-line bash script with nested conditionals.

## Step 3: Write the Script

**The "script" is usually just the body of a single tool call.** You are replacing N tool calls with one tool call whose argument contains the loop. A bash one-liner, a `python3 -c "..."` invocation, a heredoc — inline it directly in the tool call. Don't write a file to disk when the logic fits in a few lines. Only break it out to a temp script file when the logic is complex enough that inline becomes unreadable, or when you'll need to run the same collection logic again later in the conversation.

**Structure the logic the same way regardless of whether it's inline or in a file:**

1. **Collect** — iterate over the inputs, call APIs/read files/query databases in batch where possible, extract only the fields you'll need for reasoning
2. **Compress** — reduce verbose outputs to just the relevant data; don't dump 4KB of JSON when you need 3 fields
3. **Output** — for simple cases, let the result come back as stdout from the tool call; for larger outputs, write to a tempfile so the data can be re-read later without re-executing

**Batch-first I/O:** Prefer bulk operations over iteration. GraphQL over per-resource REST. `--paginate` flags over manual page-following. `find -exec` over per-file tool calls. `SELECT ... FROM information_schema` over per-table `DESCRIBE`. Multi-key queries over single-key lookups.

**Compression matters.** Raw API responses, full file contents, and verbose command outputs burn context window when read back. The script should extract, filter, and format before the result hits the context window. The reasoning step that follows should receive a clean, minimal dataset — not raw firehose output.

## Step 4: Execute and Read

**Best case: one tool call.** The inline script runs and its stdout is your compressed result. You reason on it directly.

**If the output is large or you'll need it again:** write to a tempfile. That's two tool calls — execute, then read. If you need to re-examine the data later in the conversation, re-read the tempfile. Don't re-collect.

## Recognizing Common Shapes

These situations all share the same structure — a loop that should be a script:

- **Serial API calls** over a list of resources when a batch endpoint, paginated fetch-all, or query language (GraphQL, SQL) exists
- **Opening files one-by-one** to search for content that a search tool can locate in one pass
- **Walking API pagination** by fetching each page as a separate tool call instead of scripting the cursor-following loop
- **Data format conversion** (CSV↔JSON, field extraction, restructuring) that any data-processing runtime handles natively
- **Generating N similar files** from a template with variable substitution
- **Collecting environment info** (versions, paths, configurations) one command per tool call
- **Traversing dependency trees, database schemas, or directory structures** that a single query or command already exposes in full
- **Diffing or comparing** by reading both sides into context and eyeballing, instead of using a diff tool
- **Filtering logs or output** by reading large files into context and scanning, instead of letting a filter tool extract matches

In every case, the diagnostic question is the same: **between step N and step N+1, does the agent need to understand language to decide what to do next?** If the next step is mechanically derivable from the current step's output — if it's just incrementing through a list — it's a for-loop, and it belongs in a script.

