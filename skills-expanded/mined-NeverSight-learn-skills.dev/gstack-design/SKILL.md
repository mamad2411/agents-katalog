---
name: gstack-design
description: AI-powered UI mockup generation — generate, iterate, diff, QA, and evolve mockups via GPT-4o
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# design

AI-powered UI mockup CLI built on GPT-4o image generation. Generates production-quality PNG mockups, not wireframes. Supports multi-turn iteration, visual QA, visual diff, and design-to-code prompt extraction.

Requires an OpenAI API key. Run `design setup` to configure.

## Commands

| Command | Description |
|---|---|
| `design generate --brief "..." --output /path.png` | Generate a mockup from a text brief |
| `design generate --brief-file brief.json --output /path.png` | Generate from a structured JSON brief |
| `design generate --brief "..." --output /path.png --check` | Generate + auto-QA the result |
| `design variants --brief "..." --count 3 --output-dir /path/` | Generate N variant explorations |
| `design variants --brief "..." --count 3 --viewports "desktop,tablet,mobile"` | Variants at multiple viewport sizes |
| `design iterate --session /path/session.json --feedback "..." --output /path.png` | Refine a mockup with feedback |
| `design check --image /path.png --brief "..."` | Vision QA — does mockup match brief? |
| `design compare --images "/path/*.png" --output /path/board.html` | HTML comparison board |
| `design compare --images "/path/*.png" --output /path/board.html --serve` | Comparison board + live feedback server |
| `design diff --before /path/a.png --after /path/b.png` | Visual diff between two mockups |
| `design evolve --screenshot /path/live.png --brief "..." --output /path.png` | Evolve a live screenshot into a new design |
| `design design-to-code --image /path.png` | Extract implementation prompt from mockup |
| `design gallery --output /path/gallery.html` | HTML timeline of all design explorations |
| `design serve --html /path/board.html` | Serve a comparison board with feedback loop |
| `design setup` | Configure OpenAI API key |
| `design --version` | Print version |

## Structured Brief Format

For `--brief-file`, provide a JSON file:

```json
{
  "goal": "Dashboard for coding assessment tool",
  "audience": "Technical users, hiring managers",
  "style": "Dark theme, cream accents, minimal",
  "elements": ["score badge", "narrative letter", "metric cards"],
  "constraints": "Max width 1024px, mobile-first",
  "screenType": "desktop-dashboard"
}
```

`screenType` values: `desktop-dashboard`, `mobile-app`, `landing-page`, `settings-page`, `modal-dialog`, etc.

## Common Patterns

### Explore → Pick → Iterate

```bash
# Generate 3 variants
design variants --brief "Landing page for a dev tool called Stackflow" --count 3 --output-dir /tmp/explore/

# Compare side-by-side (opens in browser)
design compare --images "/tmp/explore/*.png" --output /tmp/explore/board.html --serve

# Iterate on the chosen variant
design iterate --session /tmp/explore/session.json --feedback "make the CTA more prominent" --output /tmp/v2.png
```

### Evolve from a live site

```bash
# Screenshot your current site (via browse or any tool)
browse goto https://example.com
browse screenshot /tmp/current.png

# Generate an evolved version
design evolve --screenshot /tmp/current.png --brief "simplify the header, add more whitespace" --output /tmp/evolved.png

# Diff to see what changed
design diff --before /tmp/current.png --after /tmp/evolved.png
```

### Design-to-code handoff

```bash
# Generate the mockup
design generate --brief "Settings page with profile section and notification toggles" --output /tmp/settings.png --check

# Extract implementation instructions
design design-to-code --image /tmp/settings.png
# Returns: { implementationPrompt, colors, typography, layout, components }
```

### Build a design system from approved mockups

```bash
# After approving a mockup, extract its design language into DESIGN.md
# (This is done automatically by the memory module when invoked from a skill,
# or manually via the design-to-code command)
design design-to-code --image /tmp/approved.png
```

Future `generate` calls in the same repo will read `DESIGN.md` as a constraint, keeping new mockups on-brand.

## Project Directory

All generated output defaults to `.design/` in the current git project root (or cwd if not in a repo). This directory is auto-created on first use and auto-added to `.gitignore`.

```
.design/
├── mockup.png              # Latest generate output
├── variants/               # Latest variant exploration
│   ├── variant-A.png
│   ├── variant-B.png
│   └── variant-C.png
├── board.html              # Latest comparison board
├── iterate.png             # Latest iteration output
├── evolved.png             # Latest evolve output
└── gallery.html            # Design history timeline
```

All paths are overridable with `--output` or `--output-dir` flags.

Multi-turn session state (API threading IDs) lives in `/tmp/design-session-*.json` — ephemeral, not persisted across reboots.

## Configuration

```bash
design setup                    # Interactive API key setup
export OPENAI_API_KEY=sk-...    # Or set via environment variable
```

Config stored at `~/.config/design/config.json`. Also reads `~/.gstack/openai.json` as a fallback for existing gstack users.

## Note for existing gstack users

If you already have gstack installed, the design binary is available at `~/.claude/skills/gstack/design/dist/design`. This standalone package is for using design independently of gstack. Both installations can coexist — they use separate config paths (`~/.gstack/` for gstack, `~/.config/design/` for this package), with a fallback to read gstack's OpenAI key if the standalone config doesn't exist yet.
