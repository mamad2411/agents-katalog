---
name: explain
description: "Explain how a system or process works as an offline page of Mermaid diagrams drawn from the code: one takeaway per section. Use when asked how something is built or works, or to show or visualize it."
metadata:
  internal: true
---

# Explain

> In progress: the page format and the build are being reworked, see the repository's issues. Use it, but expect changes.

Each section answers one question with one diagram, and its heading states the takeaway:
«Only composition.ts connects the core features», not «Modules». For what an agent did, use `recap`.

## Steps

1. **Pick the sections** from the question and the code; the example shows form only.

   | Section | Question | Diagram |
   |---|---|---|
   | Overview | What runs and where data lives | `flowchart LR`, 5–10 nodes: processes, features inside them, background jobs, stores; `subgraph` per process |
   | Modules | How the code depends on itself | `flowchart` from real imports, folded to packages or features. `:::removed` marks only an import the project's boundary rules reject; name the rule under the diagram. An import the rules allow is a plain arrow |
   | A mechanism | What happens when X | `sequenceDiagram` of one scenario, 4–8 messages; the page steps through them |
   | States | Which states an entity has | `stateDiagram-v2` with every transition the code allows: walk each branch of the transition function; only when the question is about states |

   - Usually 3–5 sections. Leave out glossaries, file layouts and linter rules.
   - Every arrow label is a verb. Node labels up to 4 words; the type goes in brackets: `S[Сервер · Node]`.
   - Imports: `dependency-cruiser` or `madge` (TypeScript), `grimp` (Python), `go list -deps -json` (Go). Without a tool, collect imports with a script and fold them.
   - A diagram over 15 nodes does not read: split it, or show one level.

   Done when each section names its question and its takeaway heading.
2. **Gather evidence in the code.** For each arrow write `A -> B: verb; evidence: <file>`.
   Take module dependencies from the project's import tool and its boundary rules; take states from every branch of the transition code.
   Done when every part has a path in the code and every arrow has an evidence line.
3. **Write `explain.md` in its folder:**

   | Where you run | Folder for `explain.md` and the page | Show the page |
   |---|---|---|
   | Orca chat (`ORCA_CHAT_SCRATCH_DIR` set) | `$ORCA_CHAT_SCRATCH_DIR/`, page `explain-<4 hex>.html` | a line `::orca-visual{file="<name>.html" title="<title>"}` |
   | terminal | `<repo>/.reports/explain/`, page `<date>-<topic>.html` | `open <file>` (`xdg-open` on Linux), and the path in your reply |

   When `.reports/` is not in the repo's `.gitignore`, add it to `.git/info/exclude`.
   Start from [the example](examples/interview-sensei/explain.md); marks and diagram rules: [markdown.md](kit/markdown.md).
   Draw only what the evidence holds; name files with `[[path]]` in the text under each diagram.
   After each `sequenceDiagram`, add an ordered list: one plain-language note per message.
4. **Build fast, then check once.** Fix errors with the fast build; it takes about a second:

   ```bash
   python3 <skill dir>/kit/build.py explain.md <page>.html
   ```

   The fast build leaves the page unchecked. Run the same command once more with `--check`: it opens the page headless, offline,
   in both themes and at phone width, and opens no window. Look at its screenshots once. Done when it prints `✓`.
5. **Show the page** as the table in step 3 says. In the reply, list the sections with their takeaways.
