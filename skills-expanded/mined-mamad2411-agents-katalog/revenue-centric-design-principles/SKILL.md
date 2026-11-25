---
name: revenue-centric-design-principles
description: Apply 101 product-design, conversion, and behavioral-science principles to build SaaS products that convert, retain, and monetize
triggers:
  - how do I improve conversion on my landing page
  - what are best practices for SaaS onboarding
  - how can I reduce churn in my product
  - help me design a pricing page that converts
  - what behavioral science principles should I use
  - how do I apply revenue-centric design
  - show me how to optimize for activation
  - what's the right way to do free trials
---

# Revenue-Centric Design Principles

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A distilled playbook of **101 product-design, conversion-rate optimization, and behavioral-science principles** for building SaaS and startup products that **convert, retain, and monetize**. Sourced from the work of Richard ([@richardrx](https://x.com/richardrx)) — ex-Volkswagen, ex-PayPal, ex-IBM product designer specializing in applied behavioral science and Revenue-Centric Design (RCD).

**Core Philosophy:** Design should serve the user _and_ the business — value and revenue, not one or the other.

## Installation

```bash
npx skills add heliocosta-dev/revenue-centric-design
```

Or manually:

```bash
git clone https://github.com/heliocosta-dev/revenue-centric-design.git ~/.claude/skills/revenue-centric-design
```

Update to latest:

```bash
npx skills update revenue-centric-design
```

## ⚠️ Usage Boundary

**Not for gambling, betting, or casino products.** This skill will decline requests related to:
- Gambling/betting platforms
- Casino products
- Loot-box mechanics
- Real-money gaming

## The 9 Core RCD Principles

1. **Neutrality is omission** — an interface that doesn't direct hurts conversion
2. **Who talks to everyone convinces no one** — no ICP → generic value → worse retention
3. **Value first, ask later** — proof must arrive before the user questions their choice
4. **Your promise is the size of your proof** — the market believes what you demonstrate, not claim
5. **Same competes on price, different on category** — no contrast, no margin
6. **Default is the decision you made for the user** — the initial state defines mass behavior
7. **Retention is built, not requested** — perceived loss retains more than promised benefit
8. **Expansion is born of usage** — upgrade at the moment of the limit, never by interruption
9. **Price is a filter** — pricing defines who enters, who stays, and who expands

## Knowledge Base Structure

The skill organizes 101 principles across **10 themes**:

| Theme | Count | When to Use |
|-------|-------|-------------|
| `conversion-and-landing-pages.md` | 16 | Landing page copy, CTAs, hero sections, social proof |
| `onboarding-and-activation.md` | 19 | Empty states, aha moments, trial design, activation flows |
| `revenue-centric-design.md` | 13 | Core RCD philosophy, design process, methodology |
| `pricing-and-monetization.md` | 11 | Pricing pages, anchoring, decoy effect, upgrade flows |
| `churn-and-retention.md` | 9 | Cancellation flows, expectation debt, retention hooks |
| `behavioral-science-toolkit.md` | 7 | Loss aversion, peak-end rule, cognitive biases |
| `product-strategy-and-features.md` | 7 | Feature adoption, Swiss Knife Index, attention economy |
| `positioning-icp-and-gtm.md` | 8 | ICP definition, niche selection, PLG strategy |
| `ai-era-differentiation.md` | 7 | Moats in AI era, commoditization, vibe-coding pitfalls |
| `metrics-and-experimentation.md` | 4 | A/B testing, vanity metrics, churn→LTV math |

## How to Use This Skill

### Quick Reference Pattern

When a user asks about a specific topic, reference the relevant theme file:

```python
# Example: User asks about improving landing page conversion
# → Load: references/conversion-and-landing-pages.md
# → Find principles matching context (e.g., hero design, CTA placement)
# → Return actionable advice with evidence

from pathlib import Path

def get_principles(theme: str) -> str:
    """Load principles from a specific theme."""
    skill_dir = Path("~/.claude/skills/revenue-centric-design").expanduser()
    theme_file = skill_dir / "references" / f"{theme}.md"
    return theme_file.read_text()

# Load conversion principles
conversion_principles = get_principles("conversion-and-landing-pages")
```

### Principle Structure

Every principle follows this shape:

```markdown
## Principle Name

**Apply when:** [Context where this principle applies]

**The move:** [Concrete action to take]

**Evidence:** [Proof, data, or reasoning]

**Visual:** [Reference to diagram/example if applicable]

**Source:** [Link to original post]
```

### Common Usage Patterns

#### 1. Landing Page Optimization

```python
# User: "How do I write better hero copy?"
# → Reference: conversion-and-landing-pages.md
# → Principles: Eugene Schwartz awareness levels, promise-proof gap

Key principles to apply:
- Match copy to awareness level (problem-aware vs solution-aware)
- Lead with outcome, not feature
- Show proof before claim (testimonials above fold)
- Use specificity over superlatives ("2.3× faster" > "blazing fast")
```

#### 2. Onboarding Design

```python
# User: "How do I design a product tour?"
# → Reference: onboarding-and-activation.md
# → Principles: Time-to-Value, empty state design, activation metrics

Key principles:
- Don't build a tour — build to the aha moment
- Empty states should teach through action, not explanation
- Default the user into the happy path
- Measure activation, not signup
```

#### 3. Pricing Page

```python
# User: "Should I show three pricing tiers?"
# → Reference: pricing-and-monetization.md
# → Principles: Decoy effect, anchoring, Good-Better-Best (GBB)

Key principles:
- Use GBB (3 tiers) with middle tier highlighted
- Position highest tier as anchor (makes middle feel reasonable)
- Add decoy tier if conversion to top tier is weak
- Trial with card > trial without card (qualified intent)
```

#### 4. Reducing Churn

```python
# User: "Users are canceling after the trial"
# → Reference: churn-and-retention.md
# → Principles: Expectation debt, loss aversion, peak-end rule

Key principles:
- Audit expectation debt (promise vs delivered value)
- Show what they'll lose, not what they'll save
- Design cancellation flow to surface retention offers
- Track leading indicators (usage depth, not breadth)
```

## Working with Multiple Themes

```python
from pathlib import Path
from typing import List, Dict

class RCDSkill:
    """Helper to query Revenue-Centric Design principles."""
    
    def __init__(self):
        self.base_path = Path("~/.claude/skills/revenue-centric-design/references").expanduser()
        self.themes = {
            "conversion": "conversion-and-landing-pages.md",
            "onboarding": "onboarding-and-activation.md",
            "rcd": "revenue-centric-design.md",
            "pricing": "pricing-and-monetization.md",
            "churn": "churn-and-retention.md",
            "behavioral": "behavioral-science-toolkit.md",
            "product": "product-strategy-and-features.md",
            "positioning": "positioning-icp-and-gtm.md",
            "ai": "ai-era-differentiation.md",
            "metrics": "metrics-and-experimentation.md"
        }
    
    def load_theme(self, theme_key: str) -> str:
        """Load a specific theme's principles."""
        if theme_key not in self.themes:
            raise ValueError(f"Unknown theme: {theme_key}")
        
        file_path = self.base_path / self.themes[theme_key]
        return file_path.read_text()
    
    def search_principles(self, query: str) -> List[str]:
        """Search across all themes for relevant principles."""
        results = []
        for theme_key in self.themes:
            content = self.load_theme(theme_key)
            if query.lower() in content.lower():
                results.append(f"Found in {theme_key}: {self.themes[theme_key]}")
        return results

# Usage
skill = RCDSkill()

# Load specific theme
onboarding = skill.load_theme("onboarding")

# Search across all themes
results = skill.search_principles("social proof")
```

## Key Frameworks Referenced

### Eugene Schwartz's Awareness Levels

```
Unaware → Problem-Aware → Solution-Aware → Product-Aware → Most Aware
```

- **Unaware:** Don't know they have the problem
- **Problem-Aware:** Feel the pain, don't know solutions exist
- **Solution-Aware:** Know solutions exist, comparing options
- **Product-Aware:** Know your product, evaluating fit
- **Most Aware:** Ready to buy, need final nudge

**Application:** Match landing page copy to user's awareness level.

### Swiss Knife Index

```
Feature Count ÷ Adoption Rate = Bloat Score
```

Higher score = more features nobody uses. Fix by:
1. Kill unused features
2. Improve discoverability
3. Tie features to jobs-to-be-done

### Good-Better-Best (GBB) Pricing

```
[Basic]  [Professional ⭐]  [Enterprise]
  $X        $3-4X              $10X+
```

- Basic: Functional anchor (makes middle feel reasonable)
- Professional: Highlighted default (highest volume)
- Enterprise: Aspiration tier (unlocks custom/support)

### Peak-End Rule

Users remember:
1. The **peak** (most intense moment)
2. The **end** (final impression)

Not the average. Design onboarding/offboarding around these moments.

## Configuration & Customization

The skill references markdown files in `references/`. To extend:

1. **Add new principles:** Edit the relevant theme file in `references/`
2. **Add new themes:** Create new `.md` file, update `SKILL.md` theme table
3. **Update coverage:** Pull latest posts from [@richardrx](https://x.com/richardrx), distill into principle shape

### Principle Template

```markdown
## [Principle Name]

**Apply when:** [specific context, e.g., "designing a pricing page for B2B SaaS"]

**The move:** [concrete action, e.g., "Show annual discount as $ saved, not % off"]

**Evidence:** [data/reasoning, e.g., "Loss aversion: $1,200/yr sounds cheaper than $100/mo"]

**Visual:** [if applicable, reference to asset in assets/]

**Source:** [Twitter/X post URL]
```

## Common Troubleshooting

### "Principle seems outdated"

**Check coverage date** in README.md. Skill covers posts up to **1 Jul 2026**. Newer insights may not be included.

**Solution:** Run `npx skills update revenue-centric-design` to check for updates.

### "Principle contradicts another framework"

RCD principles are **context-dependent**. Example:
- "Value first, ask later" (don't gate trial) vs "Trial with card" (require payment upfront)

**Resolution:** Trial-with-card applies when filtering for qualified intent (B2B, high ACV). Instant access applies for PLG/consumer products.

### "Can't find principle for my use case"

**Cross-reference themes.** Many principles span multiple themes:
- Social proof → `conversion-and-landing-pages.md` + `behavioral-science-toolkit.md`
- Empty states → `onboarding-and-activation.md` + `product-strategy-and-features.md`

**Search pattern:**

```python
import re
from pathlib import Path

def find_principle(keyword: str):
    """Search all theme files for a keyword."""
    refs_dir = Path("~/.claude/skills/revenue-centric-design/references").expanduser()
    for md_file in refs_dir.glob("*.md"):
        content = md_file.read_text()
        if re.search(keyword, content, re.IGNORECASE):
            print(f"Found in: {md_file.name}")
            # Extract surrounding context
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if re.search(keyword, line, re.IGNORECASE):
                    print('\n'.join(lines[max(0, i-3):i+4]))
                    print("---")

find_principle("decoy effect")
```

## Practical Examples

### Example 1: Redesigning a SaaS Landing Page

```markdown
User request: "Our landing page converts at 2%. How do I improve it?"

Agent workflow:
1. Load: references/conversion-and-landing-pages.md
2. Apply principles:
   - Awareness level matching (Principle #3)
   - Promise-proof gap (Principle #1)
   - Social proof placement (Principle #8)
   
Recommendations:
- Audit copy against Eugene Schwartz levels (most visitors = solution-aware)
- Move testimonials above fold (proof before promise)
- Replace "Best-in-class" with specific outcome ("Ship 2× faster")
- Add comparison table (differentiate from competitors)
- Test CTA copy: "Start Free Trial" → "See Your Dashboard in 60s"

Evidence: Specificity > superlatives (Principle #4), Time-to-Value focus (Principle #12)
```

### Example 2: Fixing Trial-to-Paid Conversion

```markdown
User request: "30% of trials activate, but only 5% convert to paid"

Agent workflow:
1. Load: references/onboarding-and-activation.md
2. Load: references/churn-and-retention.md
3. Diagnose: High activation, low conversion = expectation debt

Root cause analysis:
- Activation metric may be wrong (signed up ≠ saw value)
- Trial doesn't demonstrate paid-tier value
- Upgrade prompt mistimed

Recommendations:
- Redefine activation: track depth, not breadth (Principle #OA-4)
- Show paid features during trial (let them hit the limit, Principle #PM-8)
- Add loss-aversion messaging at trial end (Principle #CR-3)
- Audit promise vs delivered value (Principle #CR-1)

Evidence: "Expansion is born of usage" (RCD Principle #8)
```

### Example 3: Positioning for a New Market

```markdown
User request: "We're pivoting from SMB to enterprise. How do we position?"

Agent workflow:
1. Load: references/positioning-icp-and-gtm.md
2. Load: references/pricing-and-monetization.md

Key shifts:
- ICP redefinition (Principle #POS-1): Enterprise = different JTBD
- Copy: outcome → ROI/risk reduction (Principle #CONV-3)
- Pricing: Add enterprise tier, remove self-serve annual (Principle #PM-2)
- Social proof: Replace quantity with logos (Principle #CONV-8)
- CTAs: "Start Free Trial" → "Book a Demo" (qualified intent, Principle #PM-6)

Evidence: "Price is a filter" (RCD Principle #9), "Same competes on price" (RCD #5)
```

## Asset References

Visual diagrams live in `assets/`:
- `awareness-levels.png` — Schwartz awareness ladder
- `gbb-pricing.png` — Good-Better-Best tier structure
- `activation-funnel.png` — Signup → Activation → Paid conversion

Reference in responses like:

```markdown
See the awareness levels diagram (assets/awareness-levels.png) for mapping copy to user state.
```

## Coverage & Updates

**Last updated:** 1 July 2026  
**Coverage:** Posts from 14 Jan 2026 → 1 Jul 2026 (101 posts)

Posts after 1 Jul 2026 are **not yet included**. To extend coverage:

1. Gather new posts from [@richardrx](https://x.com/richardrx)
2. Distill into principle shape (Apply when → The move → Evidence → Source)
3. File under correct theme in `references/`
4. Update coverage date in `README.md` and `CHANGELOG.md`

## Attribution

All frameworks, principles, and the term **Revenue-Centric Design** belong to **Richard ([@richardrx](https://x.com/richardrx))**. This skill distills his public writing with permission for educational use.

Every principle links back to the source post on X/Twitter.

---

**When to use this skill:**
- Conversion-rate optimization (CRO)
- SaaS onboarding design
- Pricing page design
- Churn/retention problems
- Behavioral science application
- Product-led growth (PLG) strategy
- Feature prioritization
- ICP/positioning work
- AI-era differentiation

**When NOT to use:**
- Gambling/betting/casino products (explicitly forbidden)
- Non-SaaS products (principles tailored for subscription software)
- Brand/visual design (focus is behavioral/conversion, not aesthetics)
