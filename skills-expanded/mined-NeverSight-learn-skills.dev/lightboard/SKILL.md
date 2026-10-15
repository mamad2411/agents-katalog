---
name: lightboard
description: How to develop Lightboard modules for Risuai. Also includes Miniboard renderer development process.
---

# Lightboard

Lightboard is a Lua-based auxiliary model request framework for Risuai.

## Risuai

Risuai is an open-source LLM chat frontend.

- Persona: User-controlled character.
- Character: In 1:1 chat, the other, LLM-controlled character. In 1:N chat, the Character represents the world itself.
- Lorebooks: May contain everything from world settings and character profiles to meta instructions.

### Risuai and modules

- Toggles
- Lorebooks
- Lua scripts for advanced interactions or editing, called "Trigger scripts"
- Regex scripts for editing input/output/display/request
- Custom CSS wrapped in `style` tags. Restricted: No `html`, `body`, or `:root` access. Best practice: Prefix all class names.

Lua runs first, and then the regexes are evaluated.

List of edits and their execution timing:

- input: Once after user submits their message. Edits the original.
- request: Every time a chat is being sent. Preserves the original.
- output: Once after chat response received. Edits the original.
- display: Every time a chat is being rendered. Preserves the original.

Note: Output edits only apply to chat responses. Lightboard responses are not affected.

#### Toggles

Toggles define module-level user preferences.

```
{key}={label}[={type}[={opt1,opt2,...}]]
```

`type`:

- (omit): Checkbox, '0'|'1'.
- select: Dropdown. Index of the selected option.
- text: Text input. User typed text.

```
booleanValue=Check Me
selectValue=Select Me=select=opt1,opt2,opt3
textValue=Type Me=text
```

A divider and collapsible groups are also available.

```
=Collapsible Group=group
=optional label=divider
==groupEnd
```

Module toggles appear in the sidebar, so the module does not need to provide an interface for them.

### Security concerns

Do not include external links when rendering HTML. JavaScript is not allowed. UI interaction without scripts is limited to `<details>`, `<input type="checkbox">`, and popovers.

Use Lua to implement stateful buttons with `risu-trigger` or `risu-btn` and custom handlers that set chat variables. See `references/000-lua.md`.

## Available References

- To understand Risuai's Lua script environment, start with `references/000-lua.md`.
- To understand Risuai's double-curly-brace templating language for lorebooks, background embeddings, and regex output values, read `references/000-cbs.md`.

For a complete Lightboard module development, read `references/000-lightboard.md`.

For a Lightboard Miniboard renderer code, read `references/000-miniboard-renderer.md`.

## Packing

If the environment has Node.js installed, use `risupack` to build the final CharX file. See `risupack`'s `README.md` for project requirements and structures.

```
npm i risupack
npm risupack build-charx -- my-module/charx.json
```

## The CSS

Risuai restricts the selector scope. Do not use `html`, `body`, or `:root` selectors. Always select by classes first, then by attributes or states. Prefix all classes with the module identifier (`.{identifier}-{class}`). Never rely on Risuai's built-in classes, such as `.chattext`.

Global styles from Risuai or other modules will interfere, especially with font colors. Do not rely on the cascade. Specify every required property.

## Axiom of Doubt

Do not assume anything not provided to you. Question your prior knowledge. Read the necessary resources.

Both Lua and CBS might feel familiar, but they are not.

- Read the Lightboard resource when developing or reviewing a full Lightboard frontend module.
- Read the Lua resource when the task needs Risuai Lua APIs beyond a task-specific reference.
- Read the CBS resource when encountering unfamiliar curly-brace syntax.
