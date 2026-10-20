---
name: vim-ex
description: >-
  How to use Ex mode in Vim for non-interactive file editing (e.g., complex text
  substitution, deleting lines, file parsing, wrapping text, sorting lines).
  You MUST load this skill when using Vim Ex mode for non-interactive file editing.
license: MIT
---
<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->
# File Editing with Ex Mode

`ex` is the line-editor mode of Vim, which is useful for non-interactive file editing in shell scripts
or agent-executed terminal commands.

Unlike tools such as `sed` or `awk` which are *stream editors* designed to process data sequentially line-by-line—`ex`
is a true *file editor*. It loads the entire file into a buffer, allowing you to freely navigate forwards and backwards,
execute complex multi-line modifications, and utilize powerful normal-mode commands. Furthermore, while `sed -i` merely
mimics in-place editing by secretly using temporary files (which leads to notoriously frustrating syntax
incompatibilities between GNU/Linux and macOS), `ex` safely and natively edits the file directly in-place.

## WHEN TO USE

You should prefer using `ex` over standard shell utilities (`sed`, `awk`, `grep`) in the following scenarios:

- **Batch editing multiple files:** When modifying multiple files at once, especially for small identical changes,
  making `ex` (via `find -exec` or `argdo`) far more efficient and flexible than generating and applying patch tooling.
- **Complex structured parsing:** When editing unstructured or multi-line formats (HTML, XML) where strict line-by-line
  stream processing is too fragile.
- **Multi-line manipulation:** When your edits require moving around a file (e.g., finding a specific pattern, moving up
  a few lines, and applying a change).
- **Native in-place editing:** To avoid the GNU/BSD syntax nightmare of `sed -i` across different operating systems.
- **Script reliability:** When writing bash heredocs (`<< EOF`) for complex configuration file patching.
- **Vim power from the shell:** Whenever you want to leverage Vim's normal mode commands (like `gqq` for formatting or
  `norm! vitd` for text object deletion) non-interactively.

## WHEN NOT TO USE

- Simple, single-line replacements on a few files where `sed` or `awk` are well-understood and sufficient.
- Operations that require complex external data processing better suited for Python, Node.js, or dedicated parsing tools.
- Tasks that are inherently interactive and require visual feedback to complete correctly.

## Basic Usage

You can run `ex` using the `-c` flag for commands and `-s` for silent (batch) mode:

```bash
# Search and replace all occurrences in a user-owned configuration file
ex -s -c '%s/alias/alias_new/g' -c 'wq' ~/.bashrc

# Append text (e.g., a new export path) to the end of your bash profile
ex -s -c '$put =\"export PATH=$PATH:~/bin\"' -c 'wq' ~/.bash_profile

# Delete a specific line (e.g., line 5) from an SSH configuration
ex -s -c '5d' -c 'wq' ~/.ssh/config

# Wrap all lines in a markdown document to 120 characters
ex -s -c 'set tw=120' -c '%normal gqq' -c 'wq' README.md

# Wrap specific lines (e.g., lines 19 to 23) to 120 characters
ex -s -c 'set tw=120' -c '19,23normal gqq' -c 'wq' README.md

# Sort a specific range of lines alphabetically (e.g., lines 10 to 20)
ex -s -c '10,20sort' -c 'wq' list.txt

# Reverse sort the entire file
ex -s -c '%sort!' -c 'wq' list.txt
```

## Using Heredocs

For multiple commands, a heredoc is often cleaner (e.g., removing debugging logs from a python code file):

```bash
ex -s main.py << 'VIMEOF'
%s/print("debug: .*/pass/g
3,5d
wq
VIMEOF
```

## Using a Script File

When you have a complex or reusable set of commands, you can store them in a `.vim` file
and apply them to your target using standard input redirection or the `source` command:

```bash
# Using standard input redirection
ex -s ~/.bashrc < ~/.vim/custom_bash_rules.vim

# Alternatively, using the source command
ex -s -c "source ~/.vim/custom_bash_rules.vim" ~/.bashrc
```

## Advanced Examples

You can also use Ex mode for more advanced manipulation like piping streams or executing normal mode commands:

```bash
# Print file contents to stdout after making a substitution
ex -s -c '%s/127/128/ge' -c '%p' -c 'q!' /etc/hosts

# Edit data piped via standard input
echo Example | ex -s -c '%p' -c 'q!' /dev/stdin

# Edit multiple files using find
find . -name "*.txt" -type f -exec ex -s -c '%s/old/new/ge' -c 'wq' {} \;

# Use normal mode commands (e.g. to extract or delete complex HTML tags or XML node)
ex -s -c '/<div.*id="the_div_id"/norm nvatd' -c '%p' -c 'q!' index.html

# String parsing examples
echo "This is example." | vim -es '+s/example/test/g' '+%print' '+q!' /dev/stdin
echo "This is example." | ex -s -c '%s/example/test/g' -c '%p' -c 'q!' /dev/stdin

# More examples for editing files in-place or via streams (non-interactive)
ex -s -c '%s/127/128/g' -c 'wq' /etc/hosts
ex -s -c '%s/olddomain\.com/newdomain.com/g' -c 'wq' /etc/nginx/nginx.conf
printf '%s\n' '%s/olddomain\.com/newdomain.com/ge' w q | ex -s /etc/nginx/nginx.conf
ex -s /etc/hosts <<< $'%s/localhost/localhost.localdomain/ge\nw\nq'
ex -s -c 'argdo %s/old/new/ge|update' -c 'q' ./**/*.txt
ex -s -c 'argdo g/TODO/d|update' -c 'q' ./**/*.txt
ex -s -c 'argdo g/^debug_print/s/^/# /|update' -c 'q' ./**/*.py
find . -type f -name '*.txt' -exec ex -s -c '%s/old/new/ge' -c 'wq' {} \;
ex -s -c '%p' -c 'q!' /etc/hosts
```

Instead of maintaining an external `.vim` script file (which adds clutter),
you can stream multiple `ex` commands directly using a here-document:

```bash
ex -s /etc/hosts << 'EOF'
%s/127/128/g
%print
q!
EOF
```

### Overcoming Patch Tooling Limitations

Standard patching (`diff`/`patch`) often fails across multiple files if surrounding line offsets drift or function
boundaries vary slightly in spacing. Using `ex` solves this by applying structural or contextual logic independently
of line numbers.

**1. Replacing a Multi-line Block Across Many Files:**
If files contain dynamically sized headers (e.g., varying length copyright blocks), `patch` often rejects changes.
Using `ex` and `argdo`, you can safely target and overwrite the entire block contextually without caring about line
numbers or varied spacing:

```bash
# Delete everything between two patterns and insert a new standardized block
ex -s -c 'argdo silent! /^# BEGIN COPYRIGHT/,/^# END COPYRIGHT/c\
# BEGIN COPYRIGHT 2026\
# All rights reserved.\
# END COPYRIGHT' -c 'update' -c 'q' ./**/*.py
```

**2. Conditionally Removing Code Structures (e.g., Functions):**
Traditional patches fail if the body of a target function has extra newlines injected by another developer.
`ex` utilizes Vim's structural text objects (like `dap` to delete a paragraph or `da{` to delete a bracket group):

```bash
# Locate 'function deprecated_handler' and structurally delete its entire body
ex -s -c 'argdo silent! /function deprecated_handler/norm! dap' -c 'update' -c 'q' ./**/*.js
```

**3. Conditionally Appending to Contextual Sections:**
When appending settings into config files with varying contents, a `.patch` file will fail if the target section is
on line 10 in one file and line 50 in another. `ex` finds the explicit section context and intelligently drops the
new payload directly beneath it:

```bash
# Safely append a new property immediately following the '[plugins]' category
ex -s -c 'argdo silent! /^\[plugins\]/a\
enable_new_feature = true' -c 'update' -c 'q' ./**/*.conf
```

### Practical Examples with Macros

When complex line-by-line transformations are too tedious to write via regular expressions (like parsing nested
brackets or dynamically moving text objects), you can define and execute Vim macros programmatically.

```bash
# Example: Extract just the URLs from Markdown links (e.g. `[name](URL)` -> `URL`).
# The macro 'q' performs the exact Vim keystrokes:
# 1. di[ - Delete inner bracket content
# 2. da[ - Delete the now-empty brackets
# 3. x   - Delete the leading '('
# 4. $x  - Go to the end of the line and delete the trailing ')'
ex -s links.md << 'EOF'
let @q = 'di[da[x$x'
%norm! @q
update
q
EOF
```

```bash
# Example: Convert a list of unformatted words into a quoted YAML array.
# The macro 'q' uses `\e` in double quotes to represent the <Esc> key:
# 1. I"  - Insert quote at the beginning of the line
# 2. \e  - Return to Normal mode
# 3. A", - Append quote and comma at the end of the line
# 4. \e  - Return to Normal mode
ex -s items.txt << 'EOF'
let @q = "I\"\eA\",\e"
%norm! @q
update
q
EOF
```

### Parse HTML/XML with Ex Mode

Examples:

```bash
# Extracting html tags
ex -s -c 'bufdo! /<div.*id=.the_div_id/norm nvatdggdG"2p' -c 'bufdo! %p' -c 'qa!' *.html

# Removing XML tags by piping stream data directly to standard input
echo "<root> <item>data</item> </root>" | ex -s -c '%s/<[^>].\{-}>//ge' -c '%p' -c 'q!' /dev/stdin

# Removing style tag from the header and print the parsed output
curl -s https://example.com/ | ex -s -c '/<style.*/norm nvatd' -c '%p' -c 'q!' /dev/stdin

# Parse html with multiple complex rules by passing HTML dynamically
ex -s <(curl -s https://example.com) << 'EOF'
  %s,'//,'http://,ge
  %s,"//,"http://,ge
  " Remove the margin on the left of the main block. "
  %s!id="doc_container"!id="doc_container" style="min-width:0px;margin-left : 0px;"!ge
  %s!<div class="outer_page!<div style="margin: 0px;" class="outer_page!ge
  " Remove useless html elements. "
  %s!<div.*id="global_header".*</div>!!ge
  %p " Print changes
  q! " Quit without saving
EOF

# Real live example from an RPM specification dynamically compiled via stdin
ex -s main.spec << 'EOF'
   %s/CFLAGS = -g$/CFLAGS =-fPIC -DPIC -g/ge
   %s/CFLAGS =$/CFLAGS =-fPIC -DPIC/ge
   %s/ADAFLAGS =$/ADAFLAGS =-fPIC -DPIC/ge
   %p
   q!
EOF
```

Create a new HTML structure by downloading HTML of Example site
and replacing its body by an auto-generated 20x20 table with random numbers in it (streamed to standard out):

```bash
ex -s <(curl -s https://example.com) << 'VIMEOF' > /tmp/generated_table.html
let @t='<table>'.repeat('<tr>'.repeat('<td>_</td>',20).'</tr>',20).'</table>'
%s!<body>.*</body>!\='<body>'.@t.'</body>'!g
%s!_!\=trim(system('echo $RANDOM'))!g
%p
q!
VIMEOF
```

### Plugins

One-liner to convert source code file into HTML using one of the standard plugins
(redirecting standard output to `/dev/null` avoids unnecessary logging):

```bash
ex -s -c 'let g:html_no_progress=1' -c 'syntax on' -c 'set ft=c' \
  -c 'runtime syntax/2html.vim' -c 'wqa' main.c > /dev/null
```

## Tips

- **Appending Text in Heredocs:** When appending lines within an `ex` heredoc script, use `a` followed by a newline,
  the text to insert, and a single `.` on a new line to terminate the block. Do not use the `a\` syntax
  (which is only suitable for inline `-c` commands).
- **Custom Delimiters:** Use alternative delimiters in substitutions (e.g., `%s!pattern!replacement!g` or
  `%s,pattern,replacement,g`) when manipulating HTML tags (like `</body>`), paths, or URLs to bypass
  repetitive backslash escaping.
- **Inserting Newlines in Substitutions:** When using the substitution command (`s/.../.../`),
  you cannot insert literal newlines or `\n`. You must use `\r` in the replacement string to generate a newline (e.g., `%s/old/new\rnewLine/g`).
- **Non-interactive Execution:** When adding or updating examples in this file, ensure they work
  non-interactively and do not require user input.
- **Preserve Examples:** Do not change existing examples unless they are not working; keep proven examples unchanged.
- **Silent Mode:** The `-s` flag suppresses prompts and feedback, making it ideal for automated file edits.
- **Terminal Automation:** Use `ex` when complex string replacements or regular expression-based modifications
  are required directly from the terminal without breaking the automated flow.
- **Write and Quit:** Always include `wq` at the end to write changes and quit when you intend in-place edits.

## Common Pitfalls

- **Forgetting the `-s` Flag**: Omitting `-s` causes `ex` to run interactively, leading to hung agent sessions waiting for user input.
- **Incorrect Delimiters in Heredocs**: Using spaces or tabs incorrectly around `EOF` or failing to terminate the heredoc properly.
- **Missing `wq` or `update`**: Forgetting to save changes before quitting, causing the command to run successfully but without modifying the file.
- **Overly Complex Regex**: Attempting to parse deeply nested HTML/XML using only regex in `ex` instead of specialized parsing tools.

## Troubleshooting

- **Debugging Silent Failures:** If a command fails silently with an exit code or hangs without output,
  temporarily replace the `-s` (silent) flag with `-V1` (verbose level 1) to print the command execution steps
  and exact error messages to the terminal.
- **Hanging Commands:** When testing new commands, use `timeout` to prevent hanging risks on read-only files.
- **Hanging Processes (Control-Z or infinite wait)**: If you accidentally find yourself stuck in an
  interactive `ex` command-line prompt (often indicated by messages like `The terminal is
  awaiting input` or `Type "visual" to go to Normal mode`), **do not kill the terminal** and
  **never type `visual`** (this launches the full interactive UI and completely breaks headless
  agents). This usually happens if you forget the `-s` (silent) flag. Simply type `qa!` and press
  Enter to safely abort. In batch mode using `argdo`, a missing `update` or standard `q` command
  may leave `ex` waiting for interactively unsaved buffers. Run `qa!` unconditionally at the end
  of heredocs to cleanly abort everything if any step stalled.
- **Heredoc Conflicts / Infinite Hangs:** Avoid piping data (`command | ex -s /dev/stdin`) when you are also
  providing commands via a heredoc (`<< EOF`). This causes `ex` to confuse its input streams and hang indefinitely.
  Use process substitution instead: `ex -s <(command) << EOF`.

- **Newline appending via string (`$put=""/a\`)**: In headless automated CI or agent scripts,
  using `$put="string"` or `a\` across multiple files via `argdo` can fail explicitly or
  invisibly swallow newlines depending on shell escaping. Use Vimscript's explicit `call
  append('$', 'your string')` to safely bypass multiline shell escaping issues completely.

- **Range Errors (e.g. Exit code 1 with no output):** Complex address ranges like `/<pattern>/+1,+3command` often fail
  because `ex` evaluates the second relative address before the cursor moves to the pattern. Splitting them solves this by
  explicitly moving the cursor first:

  ```bash
  # Fails (evaluates +3 relative to line 1)
  ex -s -c '/MyPattern/+1,+3d' -c 'wq' file.txt

  # Succeeds (moves cursor to MyPattern, then deletes the next 3 lines)
  ex -s -c '/MyPattern/' -c '+1,+3d' -c 'wq' file.txt
  ```

- **Unexpected Pattern Errors:** Prefer using `ex` string substitution commands (`%s/...`) instead of automated
  normal mode actions (e.g., `norm! vitd`) when editing unstructured data like raw HTML, which might break
  text-object selections and fail implicitly if tags are unexpectedly unclosed.

## Appending to multiple files

Example of safely appending text across multiple files via `argdo` and `call append()` instead of multi-line shell escaping:

```bash
ex -s */SKILL.md << 'VIMEOF'
set hidden
let m = 'Note that this file should be updated if outdated or steps/examples are not working.'
argdo call append('$', ['', '## Maintenance', '', m]) | update

qa!
VIMEOF
```

## References

- [Does Ex mode have any practical use?](https://vi.stackexchange.com/a/2692/467)
- [How to edit files non-interactively (e.g. in pipeline)?](https://vi.stackexchange.com/a/789/467)
- [Vim Ex Mode Documentation](https://vimhelp.org/)
- [Vim Q&A](https://vi.stackexchange.com/)
- [Learning the vi Editor/Vim/Modes](https://en.wikibooks.org/wiki/Learning_the_vi_Editor/Vim/Modes#Ex-mode)

## Related Skills

- **shell**:
  You MUST load this skill when handling shell commands with performance monitoring or timeouts.
