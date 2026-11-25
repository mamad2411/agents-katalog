---
name: mj-design
description: "Majordomus design: Whether the declared colours can be read; What a design token means; Whether the interface is built on the kit; Whether a public tree holds a licensed kit's files; The design system; The design tokens."
argument-hint: "[request]"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: module:design; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Majordomus `design`

The capabilities the Majordomus registry declares in its module `design`. Choose the one that answers the request below — or, without one, the person's last request about `design` — call it through its MCP tool, and report what it answers, as it answered:

$ARGUMENTS

| Capability | What it is | MCP tool | Command line | Effect |
|---|---|---|---|---|
| `design.contrast` | Whether the declared colours can be read | `majordomus_design_contrast` | — | reads |
| `design.explain` | What a design token means | `majordomus_design_explain` | — | reads |
| `design.kit` | Whether the interface is built on the kit | `majordomus_design_kit` | `majordomus design kit` | reads |
| `design.licence` | Whether a public tree holds a licensed kit's files | `majordomus_design_licence` | `majordomus design licence` | reads |
| `design.system` | The design system | `majordomus_design` | — | reads |
| `design.tokens` | The design tokens | `majordomus_design_tokens` | — | reads |

A capability that *changes* something runs only when the person asked for that change: call it once, and if it is refused or its outcome is not known, report that as it is and do not try again by another way. One that *reads* may be called whenever the request needs it.

Without the Majordomus MCP server attached, run the command line form from the repository root; `--help` shows its arguments. What each capability accepts and answers is defined once, in its declaration: `majordomus capabilities describe <id>`, or the MCP tool's own description. This file is derived from the registry and says nothing the declarations do not.
