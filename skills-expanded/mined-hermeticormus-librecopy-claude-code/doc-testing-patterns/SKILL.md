---
name: "doc-testing-patterns"
description: "Documentation testing patterns: the testing pyramid, Python doctest, Vale configuration and custom rules, link checker tuning, code example freshness, markdownlint rules, automated freshness detection, and anti-patterns. Use when setting up docs checks in CI."
---

# Documentation Testing Patterns

## The Documentation Testing Pyramid

Analogous to the software testing pyramid, documentation testing should be layered:

```
        E2E (manual, periodic)
       /  Can a real user follow the guide?  \
      /                                       \
   Integration (automated, weekly)
  /  Cross-file links, external URLs  \
 /                                     \
Unit (automated, every PR)
  Prose style, code execution,
  internal anchors, markdown formatting
```

Unit checks are fast and cheap - run on every PR. Integration checks (external links) are slower and network-dependent - run weekly or on release. E2E tests are human - conduct them quarterly or when major changes land.

## Python doctest Integration

Python's doctest module tests examples embedded in docstrings and Markdown:

```python
def calculate_discount(price: float, percent: float) -> float:
    """Calculate discounted price.

    >>> calculate_discount(100.0, 20)
    80.0
    >>> calculate_discount(50.0, 10)
    45.0
    >>> calculate_discount(0, 50)
    0.0
    """
    return price * (1 - percent / 100)
```

Run with `pytest --doctest-modules` or `python -m doctest module.py -v`.

For Markdown files: `pytest --doctest-glob="docs/**/*.md"`

**Doctest limitations**: tests are sensitive to whitespace and exact output. Use `# doctest: +ELLIPSIS` and `# doctest: +NORMALIZE_WHITESPACE` for flexible matching.

## Vale Style Configuration

Vale is a linter for prose - it checks documentation text against style rules.

### Built-in style packages
- `Google`: Google Developer Style Guide rules (headings, passive voice, word list)
- `Microsoft`: Microsoft Writing Style Guide
- `proselint`: Literary quality rules (clichés, redundancies)
- `write-good`: Passive voice, weasel words, adverb overuse

### Custom rule patterns
```yaml
# Substitution rule: enforce product name spelling
extends: substitution
message: "Use '%s' instead of '%s'"
level: error
swap:
  (?i)the sdk: the SDK       # Case-insensitive match
  (?i)javascript: JavaScript  # Correct capitalization

# Existence rule: flag forbidden phrases
extends: existence
message: "Avoid '%s' - too vague. Use a specific action instead."
level: warning
tokens:
  - 'simply'
  - 'just'
  - 'easily'
  - 'obviously'
```

### Vale false positive management
Use inline suppression for specific lines:
```markdown
<!-- vale off -->
The term "whitelist" is used in this security protocol for historical reasons.
<!-- vale on -->
```

## Link Checker Patterns

### Exclusion strategy
Some URLs should always be excluded from link checking:
1. `localhost` and `127.0.0.1` - development-only
2. Social media sites (Twitter/X, LinkedIn) - block bot crawlers
3. Private/intranet URLs - not accessible from CI
4. Anchor-only links that reference headings outside the checker's awareness

### Retry and timeout tuning
External links are unreliable. Configure:
- `timeout = 10` seconds per request
- `max_retries = 3` with `retry_wait_time = 2`s
- Accept `429 Too Many Requests` as "probably fine" (rate limited, not broken)

### Distinguishing 404 from redirect
A 301 redirect to a valid page is not broken. A 301 redirect to a 404 is broken. Configure link checkers to follow redirects and report the final status code.

## Code Example Freshness

Code examples rot faster than prose. Warning signs:
- Examples import packages that have been deprecated or renamed
- Examples use an API that was changed in a major version
- Examples reference environment variables that no longer exist
- Examples show output that doesn't match the current version's output

Detection strategies:
- Compare code examples against the current version's API surface (grep for removed symbols)
- Tag examples with `<!-- version: 2.x -->` and check against current major version
- Run examples against the current version in CI

## markdownlint Rules for Technical Docs

Key rules with rationale:

```yaml
MD001: true   # Heading levels increment by 1 (no skipping from H1 to H3)
MD004: true   # Consistent unordered list marker (* or - or +, pick one)
MD010: true   # No hard tabs (spaces only)
MD012: true   # No multiple consecutive blank lines
MD022: true   # Headings surrounded by blank lines
MD025: true   # Only one H1 per document
MD041: true   # Document starts with H1
MD051: true   # Link fragments must be valid anchors in the file
MD052: true   # Reference-style links must be defined
```

Disable for technical docs:
```yaml
MD013: false  # Line length (too strict for code-heavy docs)
MD033: false  # Inline HTML (needed for admonitions, tabs)
```

## Automated Freshness Detection

```bash
# Find all docs files not modified in 180+ days
git log --format="%ci %H" -- docs/ | \
  awk -v cutoff="$(date -d '180 days ago' +%Y-%m-%d)" '$1 < cutoff'

# Find version references that might be stale
grep -r "v[0-9]\+\.[0-9]\+" docs/ | grep -v "CHANGELOG"
```

## Anti-Patterns

### Testing only links, not examples
Broken links are visible failures. Broken code examples are silent failures. Users copy the example, it doesn't work, and they assume the product is broken. Example testing catches issues before users do.

### Running full link check on every PR
External link checks take 2-10 minutes and are unreliable (network conditions). Move external link checks to scheduled CI (nightly or weekly). Run internal link checks on PRs only.

### No baseline for Vale style
Introducing Vale to an existing docs repository will report hundreds of violations. Use `MinAlertLevel = error` initially to catch only critical issues, then lower the threshold over time.

### Ignoring 301 redirects
Accumulated redirects slow page load and create dependency on the redirect chain. Update links to their final destination during content audits.

## References
- [Vale documentation](https://vale.sh/docs/)
- [lychee link checker](https://github.com/lycheeverse/lychee)
- [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [pytest doctest integration](https://docs.pytest.org/en/stable/how-to/doctest.html)
- [Write the Docs: Testing your docs](https://www.writethedocs.org/guide/writing/testing/)
