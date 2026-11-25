---
name: refactor-dita-content
description: Improves the structure and modularity of existing DITA content. Use this skill when you need to split an oversized topic into focused sub-topics, convert duplicate paragraphs into conref fragments, replace inline href links with keyref references, or upgrade a generic topic element to a more specific type (concept, task, or reference).
compatibility: Python 3.9+. No third-party dependencies. File-system access required for multi-file refactoring operations.
---

## Overview

Applies structural refactoring to DITA content. Each operation is independent and can be run separately.

## Operations

### 1. Split a large topic

```bash
python scripts/refactor.py split path/to/large-topic.dita --output-dir out/
```

Splits `<section>` elements into individual topic files and generates a `<topicref>` hierarchy. Output:
- One `.dita` file per section, named from the section `<title>` (slugified)
- A `_map-fragment.ditamap` with `<topicref>` entries pointing to the new files

### 2. Extract conref fragments

```bash
python scripts/refactor.py extract-conrefs path/to/topic.dita --library conref-library.dita
```

Finds paragraphs with identical or near-identical text across the topic, extracts them to `conref-library.dita`, and replaces originals with `@conref` references.

### 3. Convert href to keyref

```bash
python scripts/refactor.py href-to-keyref path/to/map.ditamap
```

Finds all `<topicref href="...">` entries, adds `keys="key-<stem>"` attributes, and replaces inline cross-reference `href` with `keyref` throughout all topics in the map.

### 4. Upgrade topic type

```bash
python scripts/refactor.py upgrade path/to/topic.dita --to task
```

Re-wraps the topic body in the appropriate specialised body element and updates the root element and DOCTYPE. Validates the result with `validate-dita-topic` before writing.

## Rules and constraints

See [references/REFERENCE.md](references/REFERENCE.md) for full decision logic.

- Split: sections without a `<title>` are kept in the parent topic
- conref extraction: minimum 3 words; `@conref` format `library.dita#topic-id/element-id`
- href-to-keyref: does not modify external (http/https) links
- upgrade: only upgrades `<topic>` → `concept | task | reference`; never downgrades
- All operations write to `--output-dir` (default: same directory as input); originals are never overwritten

## Common edge cases

- A `<section>` containing a nested `<section>` will be split keeping inner sections intact (no recursive splitting)
- Conref chains are detected and refused (would create an invalid chained conref)
