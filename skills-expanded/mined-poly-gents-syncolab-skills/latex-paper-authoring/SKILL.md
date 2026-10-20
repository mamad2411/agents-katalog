---
name: latex-paper-authoring
description: "amsmath / amsthm scaffold, theorem environments, figure & equation cross-refs, journal templates."
---

# LaTeX paper authoring

- Scaffold: `\documentclass{amsart}` (or the journal template), `amsmath`, `amsthm`, `amssymb`, `mathtools`, `hyperref` (last), `cleveref`.
- Theorems: `\newtheorem{thm}{Theorem}[section]` plus `lem`, `prop`, `cor`, `defn`, `rem`.
- Cross-references through `\label{eq:foo}` + `\cref{eq:foo}` — never hard-code numbers.
- Compile with **`latex_compile`** (tectonic in the sandbox); ship the PDF via **`latex_get_pdf`**.
- For Overleaf-hosted work, pull with **`overleaf_pull_project`**, edit locally, push with **`overleaf_push_project`** + a clear commit message.
