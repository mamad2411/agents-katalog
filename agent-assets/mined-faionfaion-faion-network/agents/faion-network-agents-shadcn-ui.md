# shadcn/ui

## Summary

**One-sentence:** Configures shadcn/ui as code (`npx shadcn@latest add`) — components live in `src/components/ui/`, owned by the consumer, with `cn` utility, CSS-var design tokens, and a drift-check script that diffs local copies against upstream.

**One-paragraph:** shadcn/ui is not an npm dependency — the CLI copies React + Radix + Tailwind component code into `src/components/ui/` where the consumer owns and edits it. The trade is: zero version-lock-in and full restyling freedom, but no automatic upgrades. This methodology pins the `cn` utility location, the `globals.css` design-token block (color CSS vars in HSL), forbids importing from `@/components/ui/*` outside `src/components/`, and ships a drift-check shell script that warns when an upstream component diverges from the local copy (so you upgrade intentionally).

**Ефективно для:**

- Solopreneur SaaS: контрольована візуальна ідентичність без vendor lock-in.
- AI-loop генерації UI: фіксована поверхня компонентів → агент знає, що писати.
- Багатотенентні landing pages з різним брендингом — CSS-vars дозволяють swap themes per-tenant.
- Audit accessibility: Radix primitives під капотом — ARIA correct out of the box.

## Applies If (ALL must hold)

- Next.js / Vite / Remix project with React ≥18 and Tailwind ≥3.
- TypeScript-friendly codebase (shadcn CLI emits `.tsx`).
- Project does not already vendor a competing UI kit (MUI, Chakra, Ant) at scale.

## Skip If (ANY kills it)

- Server-only Node app without React.
- Codebase needs animated runtime themes — shadcn assumes light/dark via CSS class on `&lt;html&gt;`, not arbitrary mid-session swaps.
- Strict-CSP environment forbidding inline styles — Tailwind JIT + dark-mode class needs configuration.
- Sub-1kb-budget marketing landing — Radix + Tailwind bundle is heavier than hand-written.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `package.json` | JSON | repo root |
| `tailwind.config.ts` | TS / JS | repo root |
| Component manifest | path list | `components.json` (CLI-managed) |
| Design-token plan | brand spec | `src/styles/globals.css` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind]] | shadcn requires a configured Tailwind setup; design-token block lives there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: cli-add-not-npm-install, cn-utility-canonical, css-vars-tokens, no-cross-import, drift-check, components-json-committed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for shadcn install spec + components.json shape | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: importing-as-package, mixing-ui-kits, undeclared-drift, dark-mode-class-missing | 700 |
| `content/06-decision-tree.xml` | essential | Routing: greenfield vs adopt → component picking → drift policy | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_components` | sonnet | Map design intent → component list. |
| `add_component` | haiku | Run `npx shadcn add` — mechanical. |
| `customize` | sonnet | Per-component variant additions. |
| `drift_review` | opus | Decide accept/reject upstream changes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cn-util.ts` | `cn` clsx + twMerge utility canonical location at `src/lib/utils.ts` |
| `templates/globals.css` | Design-token CSS vars block + dark-mode class config |
| `templates/shadcn-drift-check.sh` | Script comparing local component to upstream repo HEAD |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[tailwind]] — shadcn rides Tailwind tokens.
- [[storybook-setup]] — shadcn components live happily in Storybook stories.

## Decision tree

See `content/06-decision-tree.xml`. Routes setup mode (greenfield vs adopt-existing-UI), component selection (composition primitives vs full layouts), and drift policy (accept-all vs review-each). All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cn-util.ts`

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * cn() — the only class merger in a shadcn/ui project.
 * Combines clsx (conditional logic) + tailwind-merge (conflict resolution).
 *
 * Usage:
 *   cn("p-4", condition && "bg-red-500", className)
 *   cn(buttonVariants({ variant, size }), className)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### `templates/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
```

### `templates/shadcn-drift-check.sh`

```bash
#!/usr/bin/env bash
# shadcn-drift-check.sh — warn when local ui/ files diverge from upstream registry.
# Usage: shadcn-drift-check.sh [components/ui/*.tsx ...]
# Run weekly in CI to surface upstream bugfixes.
set -euo pipefail
ROOT="${ROOT:-components/ui}"
DRIFT=0
TMPDIR_WORK="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_WORK"' EXIT

for f in "$@"; do
  name="$(basename "$f" .tsx)"
  pristine="$TMPDIR_WORK/$name.tsx"

  # Download pristine version from upstream (skip on network error)
  npx --yes shadcn@latest add "$name" --yes \
      --cwd "$TMPDIR_WORK" >/dev/null 2>&1 || continue

  target="$TMPDIR_WORK/$ROOT/$name.tsx"
  [ -f "$target" ] || continue

  cp "$target" "$pristine"

  if ! diff -q "$f" "$pristine" >/dev/null 2>&1; then
    echo "drift: $f differs from upstream"
    diff -u "$pristine" "$f" | head -30
    DRIFT=$((DRIFT + 1))
  fi
done

[ "$DRIFT" -eq 0 ] && echo "OK — no drift" || { echo "drift in $DRIFT file(s)"; exit 1; }
```
