---
name: bag-evidence
description: Use when a set of items must be handed over or archived as one unit — packages a directory as a BagIt bag with per-file checksums and a manifest that any receiving party can validate without this plugin. Triggers - "bag this evidence", "package for handover", "make a BagIt archive".
allowed-tools: Bash(bagit.py *), Bash(python3 *), Bash(command *), Bash(mkdir *), Bash(cp *), Bash(du *), Bash(find *), Read, Write
---

# Bag Evidence

Package a set of items as a BagIt bag — a plain directory layout with per-file
checksums that any receiving party can validate with standard tooling.

## When to use

- Handing a set of items to another party.
- Freezing a batch before it is replicated to archival storage.
- Producing a self-describing bundle that outlives this plugin.

## Inputs

- Source directory. Required.
- `--out <path>` — destination. Defaults to `exports/<name>-<date>-bag/`.

## Procedure

### 1. Verify before bagging

Never bag unverified content. Run verify-bundle over the source first. Bagging a
corrupted tree produces a bag that is internally consistent and externally wrong, which
is worse than no bag at all.

### 2. Copy, do not move

```bash
mkdir -p "$BAG_DIR"
cp -Rp "$SOURCE"/. "$BAG_DIR"/
```

Bagging rewrites the directory into BagIt's payload layout. Doing that in place would
restructure the evidence tree, so always work on a copy.

### 3. Create the bag

```bash
bagit.py --sha256 --contact-name "$HANDLER" "$BAG_DIR"
```

`bagit.py` moves the existing contents into `data/` and writes `bagit.txt`,
`bag-info.txt`, `manifest-sha256.txt`, and `tagmanifest-sha256.txt`. Use SHA-256
explicitly; the default algorithm set has changed across versions and an implicit
choice is not reproducible.

Add whatever identifying metadata the collection carries, for example
`--source-organization` and `--external-identifier` with the case reference.

### 4. Validate what was just written

```bash
bagit.py --validate "$BAG_DIR"
```

Report the result verbatim. A bag that has not been validated in this run must not be
described as valid.

### 5. Record it

Note the bag path, its file count, and its total size in the operation log, and add a
line to the custody record describing the handover unit rather than its members.

## Output

- A BagIt bag at the resolved path.
- A validation result.

## Notes

- BagIt is a specification, not this tool. A recipient can validate the bag with any
  conforming implementation, or by hand from `manifest-sha256.txt`. That is the point of
  using it.
- Do not edit anything inside a bag afterwards. Any change invalidates the manifests —
  make a new bag instead.
- Bags nest badly. Bag a flat set of items, not a tree of other bags.
