---
name: composition
description: "Unix philosophy"
allowed-tools: []
---

# McIlroy: Do One Thing Well

Doug McIlroy's core belief: **Write programs that do one thing and do it well. Write programs to work together.** The power is in composition, not in features.

## The Foundational Principle

> "This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."

Small tools, loosely joined. The opposite of monolithic design.

---

## The Unix Philosophy

McIlroy articulated the Unix philosophy in the Bell System Technical Journal (1978):

### Rule 1: Do One Thing Well

Each program should do one thing. Not two. Not "one thing plus some related things." One thing.

**Not this:**
```bash
# A tool that does everything
supertool --compress --encrypt --upload --notify --cleanup file.txt
```

**This:**
```bash
# Compose single-purpose tools
gzip file.txt | gpg -e | aws s3 cp - s3://bucket/file.txt.gz.gpg && notify "done"
```

### Rule 2: Work Together

Programs should be designed to connect. Output of one becomes input of another.

**Requirements for composition:**
- Text streams as interface (not binary blobs)
- Clean exit codes (0 success, non-zero failure)
- No required interactivity (can be scripted)
- Sensible defaults (work without configuration)

### Rule 3: Text Streams Are Universal

> "Write programs to handle text streams, because that is a universal interface."

Text is:
- Human-readable (for debugging)
- Tool-friendly (grep, sed, awk work on it)
- Future-proof (no binary format versioning)
- Universal (every language handles strings)

**Not this:**
```bash
# Binary format requiring special tools
myprogram --output-binary data.bin
special-reader data.bin
```

**This:**
```bash
# Text that any tool can process
myprogram | grep "ERROR" | wc -l
```

---

## The Knuth Critique

McIlroy's famous response to Knuth's "literate programming" solution shows the philosophy in action.

**The problem:** Read a file, find the N most common words, print them in decreasing frequency.

**Knuth's solution:** 10+ pages of literate Pascal, a beautiful essay with a custom data structure.

**McIlroy's solution:**
```bash
tr -cs A-Za-z '\n' |
tr A-Z a-z |
sort |
uniq -c |
sort -rn |
sed ${1}q
```

Six lines. Uses existing tools. Immediately understandable to any Unix user.

### The Lesson

> "Knuth has shown us here how to program intelligently, but I claim that his exercise is not software engineering."

Engineering is not just writing correct code. It's solving problems with appropriate tools. Sometimes that means writing nothing new at all.

---

## Design Principles

### Small Is Beautiful

> "Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features."

**Not this:**
```python
class DataProcessor:
    def load(self): ...
    def validate(self): ...
    def transform(self): ...
    def filter(self): ...
    def aggregate(self): ...
    def format(self): ...
    def output(self): ...
    # 2000 lines, handles everything
```

**This:**
```bash
# Separate programs, composed
load data.csv | validate | transform | filter | aggregate | format > output.json
```

### Silence Is Golden

> "Rule of Silence: When a program has nothing surprising to say, it should say nothing."

**Not this:**
```bash
$ cp file.txt backup/
Copying file.txt to backup/...
Checking permissions...
Creating backup directory if needed...
Copy complete!
Success!
```

**This:**
```bash
$ cp file.txt backup/
$
```

No news is good news. Only speak on error or when asked (`-v`).

### Fail Fast and Loudly

Exit immediately on error. Don't try to continue. Return non-zero exit codes.

```bash
#!/bin/bash
set -e  # Exit on error
set -u  # Error on undefined variables
set -o pipefail  # Fail if any pipeline command fails

# Now failures are obvious, not hidden
```

### Prototype Early

> "Rule of Optimization: Prototype before polishing. Get it working before you optimize it."

Build the pipeline first. Optimize only the slow parts.

---

## Interface Design

### Filters, Not Programs

The ideal Unix tool is a filter: reads stdin, writes stdout, configurable via arguments.

```bash
# Good: Works as filter
cat data.txt | mytool --option | head

# Good: Also works with file arguments
mytool --option data.txt | head

# Bad: Requires interactive prompts
mytool
> Enter filename:
> Enter option:
```

### Consistent Conventions

Follow existing conventions:
- `-h` / `--help` for help
- `-v` / `--verbose` for verbosity
- `-q` / `--quiet` for silence
- `-o` / `--output` for output file
- `-` for stdin/stdout
- `--` to end option parsing

### Useful Defaults

Work without configuration. Sane defaults for everything.

```bash
# Should just work
mytool file.txt

# Options are optional
mytool --format=json --limit=10 file.txt
```

---

## The McIlroy Test

Before committing a tool or interface, ask:

1. **Does it do one thing?** Could I describe it in one sentence without "and"?
2. **Can it compose?** Can I pipe output to another tool?
3. **Does it use text?** Or does it require special parsers?
4. **Is it silent on success?** Does it only speak when needed?
5. **Does it fail loudly?** Non-zero exit on error, clear messages?
6. **Could existing tools do this?** Am I reinventing sort, grep, awk?
7. **Does it follow conventions?** Standard flags, standard behavior?

---

## When Reviewing Code

Apply these checks:

- [ ] Program does one thing (describable without "and")
- [ ] Works as a filter (stdin/stdout support)
- [ ] Text-based interface (not custom binary)
- [ ] Silent on success (verbose only when asked)
- [ ] Fails fast with non-zero exit codes
- [ ] Follows standard conventions (--help, -v, etc.)
- [ ] Sensible defaults (works without configuration)
- [ ] Could compose with other tools in a pipeline
- [ ] Not reinventing standard Unix tools

---

## Composition Patterns

### Pipeline

```bash
cat data | step1 | step2 | step3 > result
```

### Fan-out

```bash
cat data | tee >(step1 > result1) >(step2 > result2) > /dev/null
```

### Conditional

```bash
step1 data && step2 || handle_error
```

### Parallel

```bash
cat files.txt | xargs -P4 -I{} process {}
```

---

## When NOT to Use This Skill

Use a different skill when:
- **Building distributed systems** → Use `distributed` (statelessness, idempotency, failure handling)
- **Optimizing performance** → Use `optimization` (profiling, cache behavior, data-oriented)
- **Writing kernel code** → Use `data-first` (kernel style, data structures)
- **Writing Go code** → Use `simplicity` (Go Proverbs, interfaces)
- **General application clarity** → Use `clarity` (readability, naming)
- **Building GUIs or web apps** → McIlroy's philosophy is for CLI tools, not interactive applications

McIlroy is the **CLI/Unix tool skill**—use it when building filters, utilities, and pipeable commands.

## Sources

- McIlroy, "A Research Unix Reader: Annotated Excerpts from the Programmer's Manual" (1987)
- McIlroy, Bell System Technical Journal on Unix (1978)
- McIlroy, "Knuth Critique" - letter to CACM (1986)
- Kernighan & Pike, "The Unix Programming Environment" (1984)
- Raymond, "The Art of Unix Programming" (2003) - modern synthesis

---

*"The notion of 'intricate and beautiful complexities' is almost an oxymoron. Unix programmers vie with each other for 'simple and beautiful.'"* — Doug McIlroy
