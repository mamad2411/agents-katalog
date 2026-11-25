---
name: shell-snippet-fmt
description: >-
  Formats shell commands and scripts meant for copy-paste, execution, or
  visual inspection so every line stays within 120 columns, with an
  explicit `\` line continuation at safe break points.
when_to_use: >-
  Use whenever about to output a shell command or script the user will
  copy, run, or read — fenced code blocks in chat responses, snippets in
  `SKILL.md` / `README.md`, scripts under `scripts/`, Makefile recipes,
  CI configs (`run:`, `script:`), Dockerfile `RUN`, install instructions,
  one-liners. Triggers: «покажи команду», «дай скрипт», «как запустить»,
  «оформи команду», «длинная команда», «команда не влезает», «перенеси
  строки», «show me the command», «give me a script», «how do I run»,
  «one-liner», «long command», «doesn't fit», «wrap this command».
---

# shell-snippet-fmt

Always format shell snippets so each line fits within 120 columns.
Where a line would exceed the limit,
break at a safe point and continue with a trailing `\`.

## Why

A 120-column cap keeps snippets readable in narrow terminals,
GitHub diffs,
side-by-side review panes,
and chat windows.
Explicit `\` continuation is the only portable way to wrap a shell
command without changing its semantics —
the shell preserves whitespace inside quoted strings and heredocs verbatim,
so wrapping there would alter the program.

## Rule

- Every line of a shell snippet stays ≤120 visual columns wide
  (one column per character, regardless of byte width).
- When a line would exceed the limit,
  break at the latest safe point that still fits
  and place a trailing `\` at end of line.
- Nothing follows the `\` —
  not even a space or a comment;
  only the newline.
- Continuation lines are indented by 4 spaces from the command start.
- If the snippet already fits in one line under 120 columns,
  you may leave it on one line
  or wrap it when multi-line form is clearer
  (complex pipeline, many flags, heredoc, long URL among short tokens).
  Readability beats compactness;
  120 is a hard upper bound, not a target.

## Safe break points

Break only where the shell still parses the result as one logical command:

- Before a flag (`--flag` or `-f value`).
- Before a pipe (`|`).
- Before a logical operator (`&&`, `||`).
- Before a redirect (`>`, `>>`, `<`, `2>&1`).
- Between positional arguments,
  when each is a self-contained token.

## Never break inside

- A quoted string —
  inside `'...'` the `\<newline>` is preserved literally
  (single quotes never interpret escapes),
  so the printed text gains a stray backslash and newline;
  inside `"..."` POSIX treats `\<newline>` as line continuation
  and silently removes both,
  joining the surrounding text.
  Either way the rendered string differs from the single-line version.
- A heredoc body (between the opening `<<EOF` and its terminator) —
  the contents are passed to the command verbatim,
  so an inserted `\<newline>` becomes part of the data.
- An unquoted token —
  splitting it changes word boundaries.
- A URL,
  path,
  identifier,
  or any other unbreakable unit.

If an unbreakable token alone exceeds 120 columns,
leave the line over the limit
and note the exception in the surrounding text
so the reader knows the cap was relaxed deliberately.

## Examples

Bad — single line at 138 columns:

```sh
docker run --rm -it --name foo -v "$PWD:/work" -w /work -e FOO=bar -e BAZ=qux ghcr.io/example/tool:1.2.3 build --target prod --output dist
```

Good — wrapped with `\`, every line ≤120:

```sh
docker run --rm -it --name foo \
    -v "$PWD:/work" \
    -w /work \
    -e FOO=bar \
    -e BAZ=qux \
    ghcr.io/example/tool:1.2.3 \
    build --target prod --output dist
```

The next three examples (pipe, logical operators, heredoc) are kept short
so the wrapping convention is easy to see —
the rule «wrap only when it helps» still applies,
but the shape shown is what to use whenever wrapping is warranted.

Pipes go at the start of the continuation line,
preceded by `\` on the previous line:

```sh
curl -sSL https://example.com/data.json \
    | jq '.items[]' \
    | head -20
```

Logical operators follow the same convention:

```sh
docker build -t image:tag . \
    && docker push image:tag \
    && echo "deployed"
```

Heredoc — wrap the surrounding command,
leave the heredoc body alone (no `\`, original lines intact):

```sh
ssh -o ConnectTimeout=10 \
    -o StrictHostKeyChecking=no \
    deploy@host bash <<'EOF'
cd /app
./run --restart
EOF
```

Bad — comment between `\` and the newline kills the continuation:

```sh
docker run \  # mount the work dir
    -v "$PWD:/work" image
```

The `\` is followed by spaces and `#`, not a newline,
so the shell stops continuing the line
and parses `-v` on the next line as a separate command.
Put comments on their own line above the command,
never after a trailing `\`.

Bad — break inside a quoted string changes program output:

```sh
echo 'this is a very long error message that needs to clearly demonstrate \
exceeding the 120-character width limit when written on one line'
```

In single quotes the `\<newline>` prints literally as `\` + newline;
in double quotes POSIX strips it and joins the adjacent text —
either way the result differs from the single-line version.
Keep the string intact even if the line goes over 120:

```sh
echo 'this is a very long error message that needs to clearly demonstrate exceeding the 120-character width limit when written on one line'
```

Same applies to a long unbreakable token (URL, path, hash):

```sh
curl -O https://github.com/very-long-org-name/very-long-repo-name/releases/download/v1.2.3-rc.4/binary-name-linux-amd64.tar.gz
```

Note the over-cap line in the surrounding text so the reader knows
the cap was relaxed deliberately.

## Scope

Applies to any shell snippet you produce or edit:

- Fenced code blocks in chat responses.
- Snippets in `SKILL.md` / `README.md` / docs.
- Scripts under `scripts/`.
- Makefile recipes.
- CI configs (GitHub Actions `run:`, GitLab `script:`).
- Dockerfile `RUN` instructions.
- Install instructions and one-liners.

If you encounter a long unwrapped command while editing a file,
reformat it as part of the same edit.
