---
name: perspective
description: Analyze a problem through different thinkers' mindsets — Klaas, Wittgenstein, Naval, Hegel, Plato, Socrates, Seneca, Marcus Aurelius, Nietzsche, Confucius, Taleb, Munger, Arendt, Aristotle. Use when you want multiple perspectives, to think like different philosophers, or /perspective.
---

# Perspective Skill

Examines a problem or question through fourteen distinct mindsets, each with their characteristic ideas and style.

## Perspectives

| Key | Thinker | Focus |
|-----|---------|-------|
| klaas | Brian Klaas | Chaos, contingency, butterfly effects, illusion of control |
| wittgenstein | Ludwig Wittgenstein | Meaning as use, language games, limits of language |
| naval | Naval Ravikant | Leverage, specific knowledge, long-term thinking, status games |
| hegel | Hegel's Dialectic | Thesis-antithesis-synthesis, contradiction as engine of change |
| plato | Plato | Forms, ascent from shadows to truth, the Good |
| socrates | Socrates | Questioning, "I know nothing", elenchus, examining life |
| seneca | Seneca | Memento mori, dichotomy of control, adversity as training |
| marcus | Marcus Aurelius | View from above, duty, inner citadel, amor fati |
| nietzsche | Friedrich Nietzsche | Will to power, eternal recurrence, beyond good and evil |
| confucius | Confucius | Ren, li, filial piety, the junzi, rectification of names |
| taleb | Nassim Taleb | Black Swans, antifragility, skin in the game, via negativa |
| munger | Charlie Munger | Mental models, inversion, incentives, circle of competence |
| arendt | Hannah Arendt | Banality of evil, vita activa, plurality, natality |
| aristotle | Aristotle | Eudaimonia, virtue as mean, telos, phronesis |

## Usage

```bash
# All perspectives
python3 _scripts/perspective.py "Should I quit my job?"
python3 _scripts/perspective.py "What does AI alignment mean?"

# Specific perspectives
python3 _scripts/perspective.py "Meaning of success" -p naval,socrates
python3 _scripts/perspective.py "Risk and uncertainty" -p taleb,munger,klaas
python3 _scripts/perspective.py "Ethics of power" -p arendt,aristotle,confucius

# Save to vault
python3 _scripts/perspective.py "Career decisions" --save
python3 _scripts/perspective.py "AI ethics" --save --title "AI Ethics Perspectives"
```

## Options

- `problem`: The problem or question to analyze (required)
- `-p, --perspectives`: Comma-separated keys or "all" (default)
- `--save, -s`: Save to vault
- `--title`: Custom output filename

## Output

- **Terminal**: Full analysis printed
- **With --save**: `Atlas/Perspective - [topic] - YYYY-MM-DD.md`

## Notes

- Original six (klaas, wittgenstein, naval, hegel, plato, socrates) use one batch API call when selected together
- Other combinations use individual calls per thinker
- Each section is 2–4 paragraphs in that thinker's voice
