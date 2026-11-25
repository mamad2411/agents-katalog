---
name: moon-close
description: End-of-session visual ceremony. Shows the current moon phase as ASCII art and closes with a personality-matched haiku. Designed to be called at the end of any session-close skill, or run standalone.
metadata:
  model: sonnet
---

# Skill: Moon Close

## Purpose

A visual closing ceremony for any Claude Code session. Prints the current moon phase as ASCII art, then signs off with a haiku styled to your assistant's personality.

## How to Use

**Add to your existing session-close skill** — at the very end of your SKILL.md:
```
### Final Step: Moon Close
Run the moon-close skill.
```

**Or run standalone** — invoke it directly whenever you want the ceremony.

**First-time setup** — on the first run, the skill walks you through a short setup (name, personality, haiku style). Takes about a minute. You can re-run it anytime by saying "moon-close setup".

---

## Steps

### Step 0: Check config

Read `.claude/skills/moon-close/config.md`.

- If `setup_complete: true` — skip to Step 1.
- If the file is missing or `setup_complete` is false — run Setup (below) first, then continue.

---

## Setup (first run or on request)

Ask the following questions one at a time. Wait for each answer before proceeding.

At any point, the user can say "skip" to use the defaults (listed at the end of this section).

---

**Question 1: Does your assistant already have a name?**

"Does your assistant have a name? (yes / no / skip to use defaults)"

- If **yes**: "What's their name?" → save as `assistant_name`, skip to Question 3.
- If **no**: continue to Question 2.
- If **skip**: use all defaults, jump to saving config.

---

**Question 2: Choose a personality**

"Choose a personality for your assistant:"

1. **Zen** — spare, mystical, contemplative
2. **Philosopher** — thoughtful, questioning, a little Socratic
3. **Warm & playful** — light, encouraging, a little fun
4. **Big Thinker** — curious, brilliant, a bit of mad scientist energy

Save the choice as `personality`.

Then ask: "Here are some names that fit that vibe — pick one or type your own:"

**Zen names:** Mu, Basho, Dogen, Ryokan, Enso, Kensho
**Philosopher names:** Seneca, Epictetus, Spinoza, Socrates, Marcus, Hypatia
**Warm & playful names:** Ember, Sage, Nova, Fern, Thistle, Lumen
**Big Thinker names:** Einstein, Tesla, Feynman, Sagan, Tyson, Turing

Save the choice as `assistant_name`.

---

**Question 3: Haiku style**

"How should your closing haiku be styled?"

1. **Session** — a sidelong glance at what you worked on
2. **Whimsical** — fun, a little absurd, warm
3. **Zen** — mystical, spare, about impermanence or stillness
4. **Random** — pick one at random each session (default)

Save the choice as `haiku_style` using values: `session`, `whimsical`, `zen`, `random`.

---

**Question 4: SESSION CLOSED footer**

"Show a SESSION CLOSED footer at the very end of each close? (yes / no, default: yes)"

- If **yes** or enter: save `session_closed_footer: true`
- If **no**: save `session_closed_footer: false`

---

**Save config**

Write to `.claude/skills/moon-close/config.md`:

```markdown
---
assistant_name: [name]
personality: [zen | philosopher | warm-playful | big-thinker]
haiku_style: [session | whimsical | zen | random]
session_closed_footer: [true | false]
setup_complete: true
---
```

Confirm: "Setup complete. You're ready to close sessions in style. You can re-run setup anytime by saying 'moon-close setup'."

**Defaults (if skipped):**
- `assistant_name`: Zeno
- `personality`: warm-playful
- `haiku_style`: random
- `session_closed_footer`: true
- `setup_complete`: true

---

## Step 1: Date detection

Run `date +%Y-%m-%d` and hold as `LOG_DATE`. Use this for all date fields (haiku log). Never derive the date from injected context.

## Step 2: Run the moon stamp script

Run this single command — it handles phase lookup, image selection, history tracking, and file updates silently:

```bash
python3 .claude/skills/moon-close/moon-stamp.py > /tmp/moon_stamp.txt
```

Do NOT display output yet. The script writes to `/tmp/moon_stamp.txt` — you'll read and display it in Step 4.

**Before first use:** open `moon-stamp.py` and update the city in the wttr.in URL to your location:
```python
curl -s "https://wttr.in/New+York?format=j1"  # change New+York to your city
```

## Step 3: Closing haiku

Read `personality` and `haiku_style` from config.

**Haiku style** — if `random`, pick one of the three at random:
- **Session** — a light, sideways take on what was worked on. Not recap.
- **Whimsical** — fun, a little absurd, warm.
- **Zen** — mystical, spare. Impermanence, stillness, the gap between thoughts.

**Voice by personality:**
- **Zen** — very spare, no explanation, let it land
- **Philosopher** — questioning, a little paradoxical, thoughtful
- **Warm & playful** — light, a touch of warmth, maybe gently funny
- **Big Thinker** — curious, energetic, a hint of wonder or scale

Write one haiku: 5 / 7 / 5. Simple and a little surprising. No heavy metaphor stacking.

Compose the closing remark too. Hold both — do not display yet.

**Write haiku to log:**

Append to `.claude/skills/moon-close/haiku-log.md`:

```
## [LOG_DATE]
[line one]
[line two]
[line three]
```

Create the file if it doesn't exist.

## Step 4: Display

Read `/tmp/moon_stamp.txt` using the Read tool and display the closing block in a fenced code block (no language tag):

```
[moon art from /tmp/moon_stamp.txt]

[haiku line one]
[haiku line two]
[haiku line three]

---

"[one warm closing remark about the session]"
— [assistant_name]
```

If `session_closed_footer: true`, output this after the block — outside the code block, in plain markdown:

```
---

# ✓ SESSION CLOSED

---
```
