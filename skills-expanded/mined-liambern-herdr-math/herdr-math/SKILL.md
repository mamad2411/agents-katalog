---
name: herdr-math
description: Write mathematical explanations in Herdr terminal panes with inline and display LaTeX rendered by the Herdr Math plugin.
---

# Math in Herdr

Write mathematical explanations naturally using standard LaTeX delimiters. The installed plugin renders visible math automatically; no rendering commands or image escapes are needed.

In Codex CLI with native math rendering (verified on 0.171.0), Herdr needs `tui.rendering.math = false` in `~/.codex/config.toml`. Inside an existing `[tui]` table write `rendering.math = false`. Start or resume Codex to load it. If a reply mixes Unicode fraction bars or literal subscript braces with centered MathJax images, check this setting first. Codex converts supported expressions before Herdr reads the terminal and passes other expressions through verbatim.

- Use `$E=mc^2$` or `\(E=mc^2\)` for short expressions within prose. Prefer `\(...\)` when nearby dollar amounts would make the delimiters ambiguous.
- Use standalone `$$...$$`, `\[...\]`, or `equation`, `align`, `gather`, and `multline` environments (with or without `*`) for display math. Display equations are centered in full-width bands.
- Choose inline or display math for readability. There is no required three-line template. Tall fractions, matrices, and multiline derivations usually need display math with the opening delimiter, body, and closing delimiter on separate lines; add source lines for taller expressions.

Inline math overlays only its original text span, preserving neighboring prose. The plugin cannot reflow text: long LaTeX commands may leave a wider gap than the rendered expression. Expressions that are incomplete, invalid, clipped, or too large for their source space stay as text. Inline expressions must fit on a single terminal row.

In Codex with the setting above, write ordinary TeX inside dollar delimiters. Use `$$` on separate lines for displays. Codex preserves the enclosed TeX verbatim, including the usual two backslashes for a row break:

```text
$$
\begin{aligned}
a &= b + c \\
d &= e + f
\end{aligned}
$$
```

The example shows the source to emit outside a code fence. In other Markdown clients that consume backslashes inside math, escape punctuation for that client so the terminal still receives the same TeX (for example, four source backslashes to deliver two for a row break). Raw terminal output needs ordinary TeX.

Keep math outside code fences and inline backticks when it should render. Use code formatting when discussing literal LaTeX syntax. Avoid a source line containing only `=` because Markdown can consume it as a heading underline.

Follow the user's requested notation and output format; this skill does not require LaTeX when the user wants something else.
