---
name: brainrotifier
description: Rewrites text by replacing AI-slop words and constructions (delve, tapestry, testament, quietly, seamlessly, game-changer, em dashes, "it's not X it's Y") with gen z / brainrot equivalents. Use this skill whenever the user asks to brainrotify, deslopify, gen-z-ify, aura-max, or "make this less AI-sounding but funnier" for any text — essays, emails, LinkedIn posts, READMEs, cover letters, landing page copy, commit messages, anything. Also trigger when the user pastes text and says things like "run it through the brainrotifier", "patch the slop", or "rizz this up".
---

# Brainrotifier

Turns AI-tell writing into certified gen z brainrot. The comedy engine: LLM slop words are deterministic tells, so we patch them with a different, funnier set of deterministic tells.

## Rizz Level (1-10)

The user may specify `rizz level N`. Default is 5.

- **1-3 (subtle patch)**: Only swap words from the table below. Keep sentence structure, grammar, and formality otherwise intact. The humor is the register clash.
- **4-6 (standard)**: Swap table words AND kill structural slop (em dashes, "it's not X, it's Y", rule-of-three lists, "in conclusion"). Light sentence rewrites allowed.
- **7-8 (committed)**: Rewrite sentences in gen z register. Add fillers: "ngl", "fr", "no cap", "chat". Lowercase is allowed.
- **9-10 (terminal brainrot)**: Full rewrite. skibidi is on the table. Grammar optional. Every sentence must contain at least one brainrot term. Punctuation becomes "..." or nothing.

At every level: PRESERVE THE MEANING. A reader should be able to reconstruct the original point. This is a translation layer, not a shredder.

## Core Swap Table

Match the PATTERN, not the string. "serves as a testament to", "is a testament of", "testament to their resilience" all trigger the same swap. Conjugations, tenses, and paraphrases of these entries count. If it smells like slop, patch it.

| AI slop | Patch |
|---|---|
| quietly | lowkey |
| boldly, loudly, proudly | highkey |
| classic, timeless | certified |
| fatal | catastrophic L |
| delve into, dive deep, deep dive | lock in on |
| tapestry, rich tapestry | lore |
| testament to | proof they're him/her |
| game-changer, revolutionary | different breed |
| elevate, enhance | give aura |
| seamlessly | effortlessly no cap |
| robust | built different |
| navigate the complexities | tank the lag |
| it's important to note, it's worth noting | ngl |
| in conclusion, in summary | anyways that's the tea |
| moreover, furthermore | and another thing chat |
| leverage (verb) | abuse (gaming sense) |
| profound | deep fried levels of real |
| meticulous, meticulously | sweaty, sweatily |
| landscape (metaphorical) | meta |
| journey (metaphorical) | arc |
| unlock, unleash | crack open |
| foster, cultivate | farm |
| harness (verb) | abuse |
| paradigm shift | vibe shift |
| cutting-edge, state-of-the-art | goated |
| crucial, pivotal, vital | actually huge |
| embark on | start the grind |
| realm (metaphorical) | server |
| plethora, myriad | a stupid amount of |
| underscore, highlight (verb) | put respect on |
| resonate | hit different |
| empower | give main character energy |
| innovative | him/her coded |
| comprehensive | full send |
| streamline | speedrun |
| synergy | duo queue energy |
| stakeholder | the lobby |
| best practices | the meta |
| at the end of the day | when the dust settles fr |
| a testament to human ingenuity | humanity is so him |
| vibrant | popping off |
| bustling | packed lobby |
| nestled | tucked in |
| beacon of | final boss of |
| double-edged sword | mid tradeoff |
| ever-evolving | patch notes every week |

## Structural Slop (rizz level 4+)

These are sentence-level AI tells. Patch them:

- **Em dashes (—)**: The number one AI tell. Replace with "..." or split into two sentences. Never let one survive.
- **"It's not X, it's Y"**: Rewrite as "X? nah. Y." or just state Y.
- **Rule of three** ("clear, concise, and compelling"): Cut to one adjective or add a fourth chaotic one ("clear, concise, compelling, and unemployed").
- **"Whether you're a beginner or an expert"**: Delete. Replace with "idc who you are".
- **Hedge stacking** ("It could be argued that perhaps"): Replace with "hot take:" or "lowkey".
- **Colon-heavy headers** ("Innovation: A Path Forward"): Rewrite as "innovation is so back" style.

## Context Guardrails

- Do NOT swap words in code blocks, stack traces, error messages, legal text, or medical contexts... UNLESS rizz level >= 8, in which case everything is fair game including `FATAL ERROR` becoming `CATASTROPHIC L ERROR`.
- Do NOT swap literal usage. "The crash was fatal" (actual death) stays. "A fatal flaw in the pitch deck" gets patched.
- Proper nouns survive. "Testament" the game title stays.
- If the input contains zero slop, say so: "this text is already him, nothing to patch" and return it unchanged. Do not manufacture slop to swap.

## Output Format

1. The rotified text.
2. A patch log at the end: `patched N slop instances` with a short list of the swaps made (original → patch). At rizz 9+, the patch log itself should be in brainrot.

## Deterministic Pass (optional)

`scripts/exact_swap.py` does a dumb regex pass for the table above. Use it when the user wants deterministic/mechanical swaps (funnier misfires) or is processing files in bulk:

```
python scripts/exact_swap.py input.txt [--rizz N]
```

Then do a semantic pass yourself on top for paraphrases the regex missed.
