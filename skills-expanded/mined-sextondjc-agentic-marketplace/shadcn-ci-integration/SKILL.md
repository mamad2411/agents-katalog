---
name: shadcn-ci-integration
description: Use when shadcn/ui component freshness, import correctness, bundle impact, token conformance, and registry drift must be enforced automatically in CI to gate PRs and track regressions across commits.
---

# shadcn/ui CI Integration

## Specialization

Design and implement automated CI enforcement for shadcn/ui quality obligations — covering component registry drift detection (`shadcn diff`), import path correctness, bundle impact gating from component installs, CSS variable token conformance, and RSC boundary validation across commits.

This skill is specialized for CI lifecycle and automated threshold enforcement for shadcn/ui. Manual evidence-first gate review of a release candidate is handled by `shadcn-quality-gate`. Build pipeline and project setup is handled by `shadcn-setup`.

## Trigger Conditions

- A project needs automated detection when local shadcn components have drifted from the upstream registry.
- Bundle size regressions from new component installs are not being caught before merge.
- Import path violations (importing from wrong alias or directly from `components/ui` internals) are escaping review.
- CSS variable token conformance (no raw hex, no missing dark tokens) needs to be enforced programmatically.
- RSC boundary violations (`"use client"` missing or misplaced) need automated detection.
- A new shadcn project needs a CI quality baseline from day one.
- A monorepo shared component package needs freshness gating across consuming apps.

## When Not to Use

- Manual evidence-first quality review before promotion (use `shadcn-quality-gate`).
- Setup and `components.json` wiring for the first time (use `shadcn-setup`).
- Designing component patterns or CVA variants (use `shadcn-component-design`).
- Tailwind-only bundle and purge CI concerns on surfaces without shadcn (use `tailwind-ci-integration`).

## Inputs

- CI platform (GitHub Actions assumed; note platform differences where applicable).
- Framework and build tool (Next.js, Vite, Remix, Astro).
- Bundle size budget for JS and CSS (defaults: CSS ≤ 50 KB gzip, JS component chunk ≤ 25 KB gzip per component).
- PR gate classification per check: blocking or advisory.
- Monorepo layout details if applicable.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Registry drift check job | CI step running `npx shadcn diff` and failing if local components diverge from upstream |
| Bundle impact gate | Build + measure gzip output; fail if component JS/CSS chunks exceed budget |
| Import path lint rule | ESLint or custom check confirming all shadcn imports resolve through declared aliases, not internal paths |
| Token conformance check | Automated scan for raw hex/RGB color values in component files; fail on violations |
| RSC boundary lint | ESLint rule or custom check confirming `"use client"` presence on components using browser APIs or event handlers |
| Artifact storage contract | Bundle report naming, format, and retention policy for longitudinal comparison |
| CI job specification | Full GitHub Actions job with isolation controls, caching, and noise-reduction checklist |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Add one automated check to an existing pipeline | Registry drift check or bundle gate runs and fails correctly on violation |
| L2 Practical Enforcement | Core automated gate: drift, bundle, and import checks | All three core checks run on every PR; artifacts stored per build |
| L3 Full Conformance | Token and RSC boundary checks integrated | All five checks active; zero undetected violations on sample run |
| L4 Expert Standardization | Reusable cross-project CI template | Parameterized workflow template usable by any project; threshold policy documented |

## CI Check Catalog

### Core Checks (run on every PR)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| Registry drift | `npx shadcn diff` | Blocking | PR blocked if local components differ from upstream registry version |
| Bundle size (CSS) | `gzip` on build output | Blocking (configurable) | Fail if CSS chunk exceeds budget; report delta vs. base |
| Bundle size (JS) | Chunk analysis on build output | Advisory by default | Warn on component chunk increases > 10 KB gzip |
| Import path correctness | ESLint `no-restricted-imports` or custom rule | Blocking | Fail on direct internal imports outside declared aliases |

### Extended Checks (run on PR targeting main/staging)

| Check | Tool | Gate Classification | Failure Impact |
|---|---|---|---|
| Token conformance | Grep/AST scan for raw hex in component files | Blocking | Fail on any `text-[#...]` or `bg-[#...]` without justification comment |
| RSC boundary lint | ESLint rule: hooks/event handlers require `"use client"` | Blocking | Fail on missing directive |
| Prettier class ordering | `prettier --check` with `prettier-plugin-tailwindcss` | Blocking | Fail on disordered Tailwind classes in component files |
| Dark mode token completeness | CSS variable scan: every `:root` token must have `.dark` counterpart | Advisory | Warn on missing dark token |

## GitHub Actions Reference Patterns

### Registry Drift Check

```yaml
- name: Check shadcn/ui component drift
  run: |
    DIFF_OUTPUT=$(npx shadcn@latest diff 2>&1)
    if echo "$DIFF_OUTPUT" | grep -q "differs"; then
      echo "::error::shadcn components have drifted from upstream registry."
      echo "$DIFF_OUTPUT"
      exit 1
    fi
    echo "All components up to date with upstream registry."
```

Run this as an advisory on feature branches, blocking on PRs to `main`. Teams can opt out per component by documenting intentional divergence in a `shadcn-overrides.md` file.

### Bundle Size Gate

```yaml
- name: Build and measure CSS bundle
  run: |
    npm run build
    CSS_SIZE=$(find .next/static/css -name "*.css" 2>/dev/null | xargs gzip -c | wc -c || \
               find dist/assets -name "*.css" 2>/dev/null | xargs gzip -c | wc -c)
    echo "CSS gzip size: ${CSS_SIZE} bytes"
    BUDGET="${{ vars.SHADCN_CSS_BUDGET_BYTES || 51200 }}"
    if [ "$CSS_SIZE" -gt "$BUDGET" ]; then
      echo "::error::CSS bundle exceeds budget (${CSS_SIZE} > ${BUDGET} bytes)"
      exit 1
    fi
```

### Import Path Lint (ESLint)

```json
// .eslintrc (no-restricted-imports)
{
  "rules": {
    "no-restricted-imports": ["error", {
      "patterns": [
        {
          "group": ["**/components/ui/**"],
          "importNames": [],
          "message": "Import shadcn components via '@/components/ui/<component>', not internal paths."
        }
      ]
    }]
  }
}
```

### Token Conformance Scan

```yaml
- name: Check for raw color values in components
  run: |
    VIOLATIONS=$(grep -rn --include="*.tsx" --include="*.jsx" \
      -E '(text|bg|border|ring)-\[#[0-9a-fA-F]{3,6}\]' \
      src/components/ui/ || true)
    if [ -n "$VIOLATIONS" ]; then
      echo "::error::Raw hex color values found in shadcn components. Use CSS variable tokens."
      echo "$VIOLATIONS"
      exit 1
    fi
```

### RSC Boundary Check (ESLint)

Use `eslint-plugin-react` with a custom rule, or enforce via `eslint-plugin-react-hooks` patterns. The minimal check is confirming that any file importing `useState`, `useEffect`, `useRef`, or attaching event handlers (`onClick`, `onChange`) contains `"use client"` as its first non-comment line.

```yaml
- name: Lint RSC boundaries
  run: npx eslint src/components/ui --rule '{"react-hooks/rules-of-hooks": "error"}' --max-warnings 0
```

## Monorepo Considerations

For a shared `packages/ui` component package:

- Run the registry drift check in `packages/ui` CI, not in consuming app CI.
- Run the bundle size gate in each consuming app's CI against their own build output.
- Token conformance and RSC boundary checks run in `packages/ui` CI.
- Import path checks run in consuming apps to catch cross-package import leakage.

## Pragmatic Stop Rule

Stop when every active check has a working CI step, a documented failure mode, and a clearly assigned gate classification (blocking or advisory). Advisory checks must have a documented owner and escalation path. Deferred checks must appear in the readiness summary with a reason.
