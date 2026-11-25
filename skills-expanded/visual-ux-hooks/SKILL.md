---
name: visual-ux-hooks
description: Structure spatial attention, choice caps, skimmer eye-brakes, and response timing using Von Restorff isolation and Hick's Law. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Visual, Spatial & Perceptual UX Hooks

Users perceive the spatial geometry of a page or screen in roughly 500 milliseconds (working heuristic, verify with your own data) before they read a single word. If the visual layout triggers **Choice Overload** or looks like a wall of uniform gray text, even the best copy will be skipped.

Use these 4 perceptual psychology principles to hook attention visually and spatially.

---

## 1. The Von Restorff Isolation Budget (Von Restorff 1933)

Hedwig von Restorff proved that when multiple homogeneous items are presented, the single item that differs in color or surrounding whitespace is noticed and remembered at higher rates (`M27`).

- **The 1-in-10 Visual Isolation Rule** states that if 5 elements on a screen are bold, colored, badged, or animated, **zero** elements are isolated. Keep 90% of your interface or document in calm neutral tones with generous whitespace, and spend your entire **Isolation Budget** on the single highest-impact element (e.g., the live interactive input box on a landing page, or the single anomalous row in a benchmark table).
- **Asymmetric Callout Anchors** work best in long-form writing or docs when you place at most one visually distinct block every 350-450 words (a 4-line code diff, a 3-row comparison table, or a single-sentence blockquote with a concrete metric).

---

## 2. Choice Overload & Progressive Action Architecture (Iyengar & Lepper 2000; Hick 1952; Scheibehenne et al. 2010)

In Iyengar & Lepper's classic field experiment (`M28`), a tasting booth with 24 jam flavors attracted more lookers, but converted only **3%** into buyers, whereas a booth with 6 flavors converted **30%** - a 10x conversion lift in that specific deli setting (30% vs 3% is the original 2000 study result only; Scheibehenne, Greifeneder & Todd's 2010 meta-analysis found a near-zero mean effect across 50 studies unless options are uncategorized and users lack prior preferences, so treat as a working heuristic and verify with your own data). By **Hick's Law**, decision time grows logarithmically with every visible option.

- **The "1 Primary + 1 Escape" CTA Cap** keeps at most 2 action elements in the same visual viewport. Pair **1 High-Contrast Primary Micro-Action** (`"Run 10s check on my URL"`) with **1 Low-Contrast Autonomy Escape Hatch** (`"Or inspect a sample report first"`).
- **The 3-Tier Pricing & Diagnostic Filter** avoids showing more than 3 pricing tiers or 3 onboarding templates at once. Pre-highlight the recommended tier based on a 1-click filter (`"Team size: 1-5 | 6-25 | 25+"`) so the user evaluates 1 tailored option instead of comparing 15 feature rows.

---

## 3. Eye-Tracking "Skimmer Brakes" & Caption Hooks

Eye-tracking studies (Nielsen Norman Group) show that readers do not read top-to-bottom on first pass; they scan in an **F-pattern** or **Layer-Cake pattern** (fixating on headings, diagram captions, tables, and the first 3 words of list items).

1. **Hook the Skimmer in the Figure Caption** because figure captions and table footnotes are among the most-read elements on a page after headlines (working heuristic, verify with your own data). Never write a wasted label caption like `"Figure 1: Latency comparison"`. Write the caption as a complete **Information Gap + Payoff hook**: `"Figure 1: Why p99 latency spikes at exactly 4,000 connections on default Linux kernels (and how 1 sysctl flag flattens the curve)."`
2. **Front-Load the First 3 Words of Every Subhead & Bullet** since skimmers fixate on the left margin. Put the concrete verb or number in the first 3 words (`"Cut 180ms by..."` instead of `"Another way that you can potentially reduce latency is by..."`).
3. **Visual Contrast Tables Over Paragraph Comparisons** work because whenever you compare `Before vs. After` or `Old Workaround vs. New Mechanism`, a compact 2-column or 3-column table locks eye fixation and promises high cognitive fluency (`M3`).

---

## 4. Temporal Psychology: Doherty Flow (<400ms) vs. The Labor Illusion (1.5s-3.5s)

Response time is itself a psychological signal (`M29`):

- **Instant Direct Manipulation (`< 400ms` - Doherty Threshold, Doherty & Thadani 1982)** requires every UI toggle and sandbox slider to respond in under 400ms. Below 400ms, the user enters a state of flow where the tool feels like an extension of their own hand.
- **Visible Step-by-Step Effort (`1.5s to 3.5s` - The Labor Illusion, Buell & Norton 2011)** applies when performing a high-trust diagnostic or security audit where an instantaneous `10ms` result can feel fake or pre-canned. Display the real underlying operations sequentially (`Checking DNS records... -> Verifying TLS 1.3 cipher suite... -> Auditing 14 security headers...`) over 1.5 to 3 seconds so the user sees the rigor of the work performed. Never fake steps that are not actually running.
