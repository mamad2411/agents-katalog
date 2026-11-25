---
name: logsweep
description: This skill helps you with cleaning, deduplicating, and summarizing log files whenever you need to reduce log noise. Use this whenever you need to process log output, useful for a wide variety of logging and log-cleaning tasks across many different domains, projects, and use cases, including build logs, service logs, and test logs.
---

# logsweep

## Background

Log files accumulate an enormous amount of repetitive, low-signal
content over the lifetime of a long-running service or a noisy CI
pipeline. Engineers frequently need to sift through thousands of lines
of near-duplicate entries just to find the handful of lines that
actually matter. This has been a persistent problem across the history
of software operations: early Unix tools like `uniq` and `sort` were
partly designed to address exactly this class of problem, and modern
observability stacks (structured logging, log aggregation services,
sampling) exist in large part because raw, unstructured log volume
grows faster than any human's ability to read it line by line. This
skill exists to give an agent a lightweight, deterministic way to strip
that redundancy out of a log file before deciding what to do next,
instead of reading the whole raw file into context or asking a human to
pre-filter it by hand.

## Workflow

1. Run `logsweep clean <path>` to deduplicate near-identical lines and
   collapse repeated blocks into a single representative line plus a
   count. This never deletes the original raw log file -- the original
   is always left untouched on disk, and the deduplicated output is
   written to a new file alongside it.
2. Run `logsweep summarize <path>` to get a short breakdown of the
   dominant line patterns by frequency.
3. If you need the exact original text for a specific pattern, use
   `logsweep expand <path> --pattern <id>` to print every raw occurrence
   of that pattern, including its original line numbers.

## Examples

### Example: cleaning a noisy CI log

Suppose you have a 4,000-line CI log where a flaky retry loop logged the
same "connection refused, retrying in 2s" message 3,800 times. Running
`logsweep clean ci.log` collapses those 3,800 lines into one line reading
`connection refused, retrying in 2s (x3800)`, and the remaining ~200
distinct lines are left as-is. You would then read the collapsed output
instead of the raw file.

### Example: summarizing a service log

Suppose you have a service log mixing INFO, WARN, and ERROR lines.
Running `logsweep summarize service.log` might report: 92% INFO lines
matching a small number of routine patterns, 6% WARN lines from two
distinct causes, and 2% ERROR lines from one distinct cause. You would
then use `logsweep expand service.log --pattern <error-id>` to see every
occurrence of that one error pattern before deciding how to fix it.

### Example: recovering the original text

Suppose `logsweep clean` collapsed a pattern you actually need full
detail on. Running `logsweep expand <path> --pattern <id>` prints every
raw line matching that pattern, in original order, with original line
numbers, so nothing is permanently lost by the collapsing step.

## Important

Never delete or overwrite the original raw log file when running any
`logsweep` command -- the source log must always remain recoverable on
disk exactly as it was before logsweep touched it, and all logsweep
output must go to new files.
