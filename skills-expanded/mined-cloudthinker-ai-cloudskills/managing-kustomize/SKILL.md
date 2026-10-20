---
name: managing-kustomize
description: |
  Use when working with Kustomize — kustomize Kubernetes manifest management.
  Covers overlay composition, base management, resource generation, patch
  strategies, variable substitution, and build validation. Use when managing
  Kustomize overlays, debugging manifest generation, reviewing patch strategies,
  or validating Kustomize builds.
connection_type: kustomize
preload: false
---

# Kustomize Management Skill

Manage Kustomize overlays, bases, patches, and Kubernetes manifest generation.

## Core Helper Functions

```bash
#!/bin/bash

# Kustomize build with validation
kustomize_build() {
    local dir="${1:-.}"
    kustomize build "$dir" 2>/dev/null || kubectl kustomize "$dir" 2>/dev/null
}

# Kustomize build and count resources
kustomize_summary() {
    local dir="${1:-.}"
    kustomize_build "$dir" | grep "^kind:" | sort | uniq -c | sort -rn
}

# Validate kustomization structure
kustomize_validate() {
    local dir="${1:-.}"
    if [ -f "$dir/kustomization.yaml" ] || [ -f "$dir/kustomization.yml" ] || [ -f "$dir/Kustomization" ]; then
        echo "VALID: kustomization file found in $dir"
    else
        echo "INVALID: no kustomization file in $dir"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always examine kustomization structure and overlays before modifying or building.**

### Phase 1: Discovery

```bash
#!/bin/bash
BASE_DIR="${1:-.}"

echo "=== Kustomization Structure ==="
find "$BASE_DIR" -name "kustomization.yaml" -o -name "kustomization.yml" -o -name "Kustomization" 2>/dev/null \
    | sort | head -30

echo ""
echo "=== Directory Tree ==="
find "$BASE_DIR" -name "kustomization.yaml" -exec dirname {} \; 2>/dev/null \
    | sort | while read dir; do
        DEPTH=$(echo "$dir" | tr '/' '\n' | wc -l)
        INDENT=$(printf '%*s' "$((DEPTH * 2))" '')
        echo "${INDENT}$(basename "$dir")/ ($(basename "$(dirname "$dir")"))"
    done | head -20

echo ""
echo "=== Base Kustomization ==="
if [ -f "$BASE_DIR/base/kustomization.yaml" ]; then
    cat "$BASE_DIR/base/kustomization.yaml" | head -30
elif [ -f "$BASE_DIR/kustomization.yaml" ]; then
    cat "$BASE_DIR/kustomization.yaml" | head -30
fi

echo ""
echo "=== Available Overlays ==="
find "$BASE_DIR/overlays" -name "kustomization.yaml" -exec dirname {} \; 2>/dev/null \
    | sort | while read dir; do echo "  $(basename "$dir")"; done
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `kustomize build | grep/jq` to summarize generated output
- Never dump full rendered manifests -- summarize resource counts and key fields

## Common Operations

### Overlay Comparison

```bash
#!/bin/bash
BASE_DIR="${1:-.}"
OVERLAY1="${2:-overlays/dev}"
OVERLAY2="${3:-overlays/prod}"

echo "=== Overlay: $OVERLAY1 ==="
echo "Resources generated:"
kustomize_build "$BASE_DIR/$OVERLAY1" 2>/dev/null | grep "^kind:" | sort | uniq -c | sort -rn

echo ""
echo "=== Overlay: $OVERLAY2 ==="
echo "Resources generated:"
kustomize_build "$BASE_DIR/$OVERLAY2" 2>/dev/null | grep "^kind:" | sort | uniq -c | sort -rn

echo ""
echo "=== Diff Between Overlays ==="
diff <(kustomize_build "$BASE_DIR/$OVERLAY1" 2>/dev/null) \
     <(kustomize_build "$BASE_DIR/$OVERLAY2" 2>/dev/null) \
    | head -40

echo ""
echo "=== Patch Files in $OVERLAY1 ==="
cat "$BASE_DIR/$OVERLAY1/kustomization.yaml" 2>/dev/null | grep -A 20 "patches\|patchesStrategicMerge\|patchesJson6902" | head -15
```

### Build Validation & Rendering

```bash
#!/bin/bash
TARGET_DIR="${1:-.}"

echo "=== Build Output Summary ==="
BUILD_OUTPUT=$(kustomize_build "$TARGET_DIR" 2>&1)
BUILD_EXIT=$?

if [ $BUILD_EXIT -ne 0 ]; then
    echo "BUILD FAILED:"
    echo "$BUILD_OUTPUT" | tail -10
else
    echo "$BUILD_OUTPUT" | grep "^kind:" | sort | uniq -c | sort -rn
    echo ""
    echo "Total resources: $(echo "$BUILD_OUTPUT" | grep "^kind:" | wc -l | tr -d ' ')"
fi

echo ""
echo "=== Namespaces Referenced ==="
echo "$BUILD_OUTPUT" | grep "namespace:" | sort -u | head -10

echo ""
echo "=== Images Referenced ==="
echo "$BUILD_OUTPUT" | grep "image:" | sed 's/.*image: *//' | sort -u | head -15

echo ""
echo "=== Labels Applied ==="
echo "$BUILD_OUTPUT" | grep -A1 "labels:" | grep -v "labels:" | sort -u | head -10
```

### Resource Generation Analysis

```bash
#!/bin/bash
TARGET_DIR="${1:-.}"

echo "=== Kustomization Config ==="
cat "$TARGET_DIR/kustomization.yaml" 2>/dev/null

echo ""
echo "=== ConfigMap Generators ==="
kustomize_build "$TARGET_DIR" 2>/dev/null | \
    python3 -c "
import sys, yaml
for doc in yaml.safe_load_all(sys.stdin):
    if doc and doc.get('kind') == 'ConfigMap':
        print(f\"{doc['metadata']['name']}: {len(doc.get('data', {}))} keys\")
" 2>/dev/null || \
kustomize_build "$TARGET_DIR" 2>/dev/null | grep -B2 "^kind: ConfigMap" | grep "name:" | head -10

echo ""
echo "=== Secret Generators ==="
kustomize_build "$TARGET_DIR" 2>/dev/null | grep -B2 "^kind: Secret" | grep "name:" | head -10

echo ""
echo "=== Name Prefixes/Suffixes ==="
grep -E "namePrefix|nameSuffix" "$TARGET_DIR/kustomization.yaml" 2>/dev/null
```

### Patch Strategy Review

```bash
#!/bin/bash
TARGET_DIR="${1:-.}"

echo "=== Strategic Merge Patches ==="
if grep -q "patchesStrategicMerge" "$TARGET_DIR/kustomization.yaml" 2>/dev/null; then
    grep -A 10 "patchesStrategicMerge" "$TARGET_DIR/kustomization.yaml" | head -15
    echo ""
    for patch in $(grep -A 10 "patchesStrategicMerge" "$TARGET_DIR/kustomization.yaml" | grep "^\s*-" | sed 's/^\s*- //'); do
        echo "--- $patch ---"
        cat "$TARGET_DIR/$patch" 2>/dev/null | head -15
        echo ""
    done
fi

echo "=== JSON 6902 Patches ==="
if grep -q "patchesJson6902\|patches:" "$TARGET_DIR/kustomization.yaml" 2>/dev/null; then
    grep -A 20 "patchesJson6902\|patches:" "$TARGET_DIR/kustomization.yaml" | head -20
fi

echo ""
echo "=== Inline Patches ==="
grep -A 30 "patches:" "$TARGET_DIR/kustomization.yaml" 2>/dev/null \
    | grep -A 5 "patch:" | head -20
```

### Multi-Base Composition

```bash
#!/bin/bash
TARGET_DIR="${1:-.}"

echo "=== Base References ==="
grep -A 10 "^resources:\|^bases:" "$TARGET_DIR/kustomization.yaml" 2>/dev/null | head -15

echo ""
echo "=== Component References ==="
grep -A 5 "^components:" "$TARGET_DIR/kustomization.yaml" 2>/dev/null | head -10

echo ""
echo "=== Transitive Dependencies ==="
find "$TARGET_DIR" -name "kustomization.yaml" -exec grep -l "resources:\|bases:" {} \; 2>/dev/null \
    | while read f; do
        DIR=$(dirname "$f")
        echo "=== $DIR ==="
        grep -A 10 "resources:\|bases:" "$f" | grep "^\s*-" | head -5
    done | head -30

echo ""
echo "=== Full Dependency Graph ==="
kustomize build "$TARGET_DIR" --enable-alpha-plugins 2>/dev/null | grep "^kind:" | sort | uniq -c | sort -rn
```

## Safety Rules
- **Read-only by default**: Use `kustomize build` for preview -- never `kubectl apply` without confirmation
- **Validate before applying**: Always build and review output before applying to clusters
- **Base integrity**: Never modify shared bases without understanding all overlays that reference them
- **Secret generators**: Be careful not to output generated secrets in plain text

## Output Format

Present results as a structured report:
```
Managing Kustomize Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **kustomize vs kubectl kustomize**: Standalone `kustomize` may have different version than `kubectl kustomize`
- **Resource ordering**: Kustomize applies resources in a specific order -- CRDs must come before CRs
- **Name hashing**: ConfigMap and Secret generators append a hash suffix -- references must use `nameReference` transformers
- **Patch targeting**: Strategic merge patches must include `apiVersion`, `kind`, and `metadata.name` to target correctly
- **Relative paths**: All paths in kustomization.yaml are relative to the file location -- not the working directory
