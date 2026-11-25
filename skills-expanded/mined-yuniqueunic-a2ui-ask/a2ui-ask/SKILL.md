---
name: a2ui-ask
description: >
  Ask the user through a browser form instead of chat whenever they must pick
  among options, fill in structured config, or settle a batch of decisions
  (including "grill me" interviews once they reach concrete choices). You write
  a JSON Schema; the bundled script serves it with the schemaui web engine
  (sliders, ranges, colour pickers, segmented and radio options, conditional
  fields, Mermaid/SVG/Markdown figures on questions and options), opens the
  browser, blocks until the user saves, and writes the answers to
  .schemaui/answers/. Trigger phrases: "give me a form", "ask me via form",
  "configure", "I need to choose", "grill me", "a2ui", "给我个表单", "配置一下",
  "用表单问我", "问我几个问题", "拷问我".
---

# a2ui-ask

You write a draft-07 JSON Schema that describes the questions. `scripts/ask.py`
serves it as a web form through the
[schemaui](https://github.com/YuniqueUnic/schemaui) engine, prints the URL,
waits until the user clicks **Save & Exit**, and leaves the answers in
`.schemaui/answers/<topic>-<timestamp>.json`.

## Contract

1. **Browser form, never a terminal prompt.** Your process has no TTY, so a
   terminal UI renders nowhere and hangs.
2. **Say it before you block.** The message that starts the form gives the user
   the URL, the time budget, and the answer file path.
3. **Block on the script, then read the answer file.** The file is the record,
   not the chat.
4. **Never abort the task over a form.** Exit 6 means fix the schema and run
   again; any other non-zero exit means ask in plain text (see
   [Fallback](#fallback-plain-text)) and say that you fell back.
5. **Ask only what only the user can decide.** Check the code, git history and
   `.schemaui/answers/` first, and pass a relevant past answer as `--config`.

## Steps

1. **Draft the schema** by the rules in
   [Writing the schema](#writing-the-schema). One form covers one cluster of
   related decisions: not one form per question, and not a serial interview in
   chat.
2. **Run the script** from this skill's directory. Pipe the schema in; the
   script keeps a copy under `.schemaui/schemas/` for the audit trail:

   ```bash
   python3 scripts/ask.py --schema - --topic deploy-config \
     --title "Deployment config" --description "Decides the staging rollout" \
     --timeout 600 <<'EOF'
   { "type": "object", "properties": { "…": {} }, "required": ["…"] }
   EOF
   ```

   Without Python, `bash scripts/ask.sh` and `pwsh scripts/ask.ps1` take the
   same flags. On a remote or headless machine add `--no-open` and relay
   `SCHEMAUI_LAN_URL` or the forwarded URL. For sensitive answers bind
   `--host 127.0.0.1` and ask remote users to tunnel first
   (`ssh -L 8787:localhost:8787 <host>`).
3. **Relay what the script prints** (`SCHEMAUI_URL=…`), for example: "Form ready
   at http://localhost:8787. You have about 10 minutes; the form counts down and
   closes itself, saving nothing, when time runs out. Answers go to
   `.schemaui/answers/deploy-config-….json`." Size `--timeout` to the form; the
   default is 300 seconds.
4. **Read the answers** after exit 0 (`SCHEMAUI_RESULT=<path>`) and cite field
   paths: "`environment = staging`, `replicas = 3`". When a field holds
   `其他`/`other`, the real answer is in its `<field>_custom` sibling. Read a
   conditional field only when its `x-visible-when` rule holds: hiding a field
   does not remove its value.

## Writing the schema

- **Recommend every answer, and make the recommendation stick.** Put it in
  `default` **and** list the key in the parent's `required`. From schemaui-cli
  0.9.4 the form pre-fills defaults only for required fields: an optional field
  with a `default` renders empty (a radio group shows nothing picked) and is
  missing from the answer file unless the user touches it. An object that holds
  recommended answers must be required too, all the way up. Leave optional only
  fields with no recommendation, such as `_custom` inputs and free-form notes.
- **Explain in the description, never in the label.** Say why you recommend the
  default ("推荐 X：因为…") and what the answer changes downstream. A `(推荐)`
  suffix on an option leaks into the answer file, because the label is the
  value.
- **Write in the user's language**: every `title`, `description` and option.
- **Give every choice an escape hatch.** Add `其他`/`other` to each enum, plus
  an optional `<field>_custom` sibling that appears only when it is picked
  (`"op": "contains"` for a multi-select). The escape value is never the
  default:

  ```json
  "delivery": { "type": "string", "enum": ["单个 HTML 文件", "其他"], "default": "单个 HTML 文件" },
  "delivery_custom": {
    "type": "string",
    "title": "交付形式 · 自定义",
    "x-multiline": true,
    "x-visible-when": { "field": "delivery", "op": "equals", "value": "其他" }
  }
  ```

- **Pick the control the value deserves**, from the table below. Plain text
  boxes make the user translate in their head; a hint earns its place when it
  removes typing or rules out a wrong answer.
- **Show a figure when options differ in shape**, such as topologies, rollout
  strategies or data models, so the user picks by recognising the picture. A
  three-option enum with one-word labels needs no diagram.

### Control picker

| The answer is…                               | Schema                                                                                                    |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| one of 2–4 short labels                      | `enum` + `"x-control": "segmented"`                                                                       |
| one of a few options that need a full line   | `enum` + `"x-control": "radio"`                                                                           |
| one of many                                  | `enum` (dropdown)                                                                                         |
| several of a set                             | `{"type": "array", "items": {"enum": […]}, "uniqueItems": true}` (checkbox list)                          |
| a yes/no that switches a mode                | `boolean` (switch); one tick among several → `"x-control": "checkbox"`                                    |
| a number on a scale                          | `minimum` + `maximum` + `"x-control": "slider"`; named stops → `"x-slider-marks"`                         |
| a window with two ends                       | array of two numbers, `minItems`/`maxItems: 2`, `minimum`/`maximum` on the array, `"x-control": "range"`  |
| a colour                                     | `string` + `"x-control": "color"`                                                                         |
| a paragraph                                  | `string` + `"x-multiline": true`                                                                          |
| a diagram the user corrects                  | `string` + `"x-control": "mermaid"` (live preview)                                                        |
| a variant with its own settings              | `oneOf` of titled objects                                                                                 |
| a group, a list of records, key/value pairs  | nested `object`; array of objects; `additionalProperties`                                                 |
| something that only matters sometimes        | `"x-visible-when": {"field": "<sibling>", "op": "equals" \| "contains", "value": …}`                      |
| context a sentence cannot carry              | `"x-content": {"type": "mermaid" \| "svg" \| "markdown", "source": "…"}` on the field                     |
| options the user recognises by their picture | `"x-options": [{"label", "description", "content"}, …]`, one entry per enum value, with `radio` or select |

Snippets for each row, figure rules and the example index:
[references/controls.md](references/controls.md).

### What the engine rejects

schemaui checks hints when it loads the schema. The script turns a rejection
into exit 6 and prints the engine's message, for example
`` `x-control: "slider"` on `/name` needs a number, but the property is a string ``.
The engine rejects:

- a control that does not fit the value, or an unknown control name;
- `x-options` whose length differs from the `enum`, and option figures on a
  `segmented` control;
- an `x-visible-when` rule naming a property that is not a sibling in the same
  object;
- an `x-content` or option figure with an empty `source`.

A slider or range missing a bound is not an error; it falls back to a plain
input. Controls need schemaui-cli 0.8 or later and figures 0.9 or later; older
builds ignore the hints and show plain inputs.

## Exit codes

| Code | Meaning                                         | Do                                                                                                                                         |
| ---- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 0    | answers written                                 | read the file and continue                                                                                                                 |
| 3    | engine missing                                  | offer `bash scripts/install.sh` or `pwsh scripts/install.ps1` (`--source gitee` / `-Source gitee` behind a blocked github.com), then rerun |
| 4    | timed out, nothing saved                        | fall back to plain text, or rerun with a longer `--timeout` if the user wants the form                                                     |
| 5    | cancelled or failed                             | fall back to plain text                                                                                                                    |
| 6    | bad input: schema or config rejected/unreadable | fix it from the error message and rerun                                                                                                    |

## Fallback: plain text

When the form cannot run, ask the same questions in one message, numbered, each
with its recommended answer, and ask for a JSON reply. Save the reply to
`.schemaui/answers/<topic>-manual-<YYYYMMDD-HHMMSS>.json` so manual answers
share the audit trail.

## More

- [references/controls.md](references/controls.md): every control and figure
  surface with snippets, and which example to copy from.
- [references/engine.md](references/engine.md): the raw `schemaui web` command,
  theming with `--theme`, and custom frontends.
- [install.md](install.md): every way to install the engine.
- [skills/grill-with-docs/SKILL.md](skills/grill-with-docs/SKILL.md): interview
  discipline for open-ended designs. Use it only when the user has no grilling
  skill of their own.

MIT, see [LICENSE](LICENSE).
