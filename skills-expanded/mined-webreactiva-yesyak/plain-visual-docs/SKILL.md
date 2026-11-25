---
name: plain-visual-docs
description: Convention for explaining technical work to mixed audiences with a plain-language opening paragraph, ASCII trees and diagrams, and validated Mermaid charts. Use it whenever you write or improve a spec, a plan, a pull request description, a README section or a report that other people will read, and whenever the user asks for a TL;DR, a non-technical summary, diagrams, trees, flowcharts, sequence diagrams or "something my manager can understand".
---

# Plain visual docs

If AGENTS.md sets a different convention for this topic, follow AGENTS.md.

A reader must understand the purpose in 30 seconds and the structure in 2 minutes. Text alone does not do that for most technical changes.

## 1. Plain-language opening

Start the document with a short section (`## TL;DR` in specs, `## In plain words` in pull requests).

- Write for a reader who does not know the code, the jargon or this session.
- Describe the effect, not the mechanism. Write "too many wrong passwords and the sign-in waits a minute", not "rate limit of 5 requests per minute per IP".
- Cover: what changes, who uses it, what they can do, what stays the same, what is not included.
- One paragraph, or one sentence and up to eight bullets.
- Do not use: framework names, protocol names, acronyms, file names.

## 2. ASCII for structure

Use ASCII inside ```` ```text ```` fences for:

- **File trees.** Mark new files with `+` and changed files with `~`. Add a short comment after each entry.
- **Before and after** views of a data flow or a process.
- **Process timelines**, such as "spec → plan → build → review".

## 3. Mermaid for behavior

Use Mermaid for things that move:

| Need | Diagram |
| --- | --- |
| How a request or job passes through checks | `flowchart TD` |
| Who talks to whom, in which order | `sequenceDiagram` |
| Tables and relations | `erDiagram` |
| Lifecycle of a session, order or record | `stateDiagram-v2` |
| A decision table | `flowchart` with one diamond per question |

Draw one diagram per question the reader has. Do not add a diagram only because a type exists.

Syntax rules that prevent broken renders on GitHub, GitLab and other hosts:

- Quote every label that contains `/`, `:`, `(`, `)`, `{`, `?` or `,`: `A["POST /login"]`.
- Use `<br/>` for line breaks. Do not use other HTML.
- Keep `erDiagram` attribute types simple (one word, for example `int`, `string`).

## 4. Validate every Mermaid block

Render each block before you deliver. A diagram that does not render is worse than no diagram.

```bash
mkdir -p .scratchpad/mermaid && rm -f .scratchpad/mermaid/*
python3 - <<'EOF'
import re
text = open("PATH/TO/DOC.md").read()
for index, block in enumerate(re.findall(r"```mermaid\n(.*?)```", text, re.S)):
    open(f".scratchpad/mermaid/d{index}.mmd", "w").write(block)
EOF
for file in .scratchpad/mermaid/*.mmd; do
  npx -y @mermaid-js/mermaid-cli -q -i "$file" -o "${file%.mmd}.svg" >/dev/null 2>&1 \
    && echo "ok $file" || echo "FAIL $file"
done
```

If the command fails for every file, the renderer did not find a browser. This happens in containers and cloud sessions. Point it to an installed Chromium with a Puppeteer config and add `-p .scratchpad/puppeteer.json` to the command:

```bash
echo '{"executablePath":"<path to chrome>","args":["--no-sandbox"]}' > .scratchpad/puppeteer.json
```

If the error is `Cannot find package 'puppeteer'`, the CLI needs `puppeteer` next to it. Install both once in `.scratchpad/tools` with `PUPPETEER_SKIP_DOWNLOAD=1 npm i --prefix .scratchpad/tools @mermaid-js/mermaid-cli puppeteer`, point `executablePath` to the installed Chrome, and run `.scratchpad/tools/node_modules/.bin/mmdc`.

Check the validator once with a broken block. It must print `FAIL`.

Without Node.js, say that the diagrams were not rendered, and check them in the preview of the code host (for example the GitHub or GitLab file view) before you publish.

Do not read the generated SVG files into the context. They are large. The exit status is enough.

## 5. Faithfulness

- Diagrams show only behavior that the code or the spec defines. Do not invent routes, fields or checks.
- If a diagram needs a detail that the spec does not define, leave it out and list it as an ambiguity for the user.
- Put each diagram next to the section it explains, with a one-line lead-in. Do not collect all diagrams at the end.
- A diagram task is a good candidate for a subagent. Brief it with this skill and with the subagent rules in `scratchpad-working-files`.
