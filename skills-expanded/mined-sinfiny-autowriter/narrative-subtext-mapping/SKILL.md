---
name: narrative-subtext-mapping
description: "Use when drafting or revising fiction dialogue, character interaction, romance, rivalry, betrayal, negotiation, secrets, fan fiction character dynamics, or autonomous writing-agent scenes where characters should not state their feelings directly. Provides a hidden-state map for Current_Knowledge, Hidden_Agenda, and True_Emotional_State so invisible narrative forces shape visible prose indirectly. Based on Judy Fan's cognitive tools framing of making invisible structure visible for reasoning."
---

# Narrative Subtext Mapping

Use this skill to make invisible character state steer the surface text without turning dialogue into confession-by-summary.

## Source Protocol

- Read `references/source-notes.md` when source grounding or tuning is needed.
- Use the source as a cognitive-tool metaphor for fiction: make hidden structure explicit during planning, then indirect on the page.
- Do not expose private author notes in final prose unless the user asks for planning artifacts.

## Operating Loop

Before writing dialogue or interpersonal action, build this compact hidden map:

```xml
<subtext_map>
Reader_Knows:
Scene_Pressure:
Character:
  Current_Knowledge:
  Hidden_Agenda:
  True_Emotional_State:
  Visible_Tactic:
  Forbidden_Direct_Line:
Subtext_Channel:
</subtext_map>
```

For multiple active characters, repeat the character fields for each one.

Field meanings:

- `Current_Knowledge`: what the character believes right now, including mistaken beliefs.
- `Hidden_Agenda`: what the character wants from the exchange but may not admit.
- `True_Emotional_State`: the real feeling underneath the tactic.
- `Visible_Tactic`: the surface behavior used to pursue the agenda.
- `Forbidden_Direct_Line`: the blunt line the character must not say.
- `Subtext_Channel`: body language, deflection, overprecision, silence, joke, topic shift, object handling, status move, false concession, or selective honesty.

## Shadow Text Rule

Never write dialogue that directly matches `True_Emotional_State` unless the scene is explicitly a hard-won confession payoff.

Instead, translate the hidden state:

- Fear becomes control, preparation, withdrawal, or a question about logistics.
- Jealousy becomes criticism of timing, taste, risk, or propriety.
- Desire becomes attention to small needs, teasing, interruption, or avoidance.
- Grief becomes practical caretaking, irritation, numbness, or fixation on an object.
- Shame becomes humor, competence display, blame, or refusal to meet the other person's eyes.
- Love becomes sacrifice, noticing, restraint, or choosing the other person's cost over one's own.

## Dialogue Procedure

1. Give each character a different knowledge state or pressure.
2. Decide what each character cannot afford to say.
3. Let each line try to achieve an agenda while hiding or displacing the true emotion.
4. Use action beats only when they reveal a hidden variable or change the power balance.
5. End the exchange when at least one hidden variable changes, leaks, or becomes harder to hide.

## Revision Targets

When revising flat dialogue:

- Replace emotion labels with tactical speech.
- Replace symmetrical honesty with asymmetrical knowledge.
- Replace exposition with a character trying to get something.
- Replace generic body language with a specific action tied to the hidden agenda.
- Preserve productive ambiguity; remove only accidental confusion.

## Self Check

```xml
<subtext_check>
Hidden states explicit in planning:
Dialogue avoids direct emotional naming:
Each line has a tactic:
Body language reveals pressure:
Reader can infer the feeling:
Scene changes a hidden variable:
Revision needed:
</subtext_check>
```

If the reader cannot infer the feeling at all, add one concrete leak. If the character states the feeling too cleanly, displace it into tactic, gesture, or misdirection.

## Guardrails

- Do not make every character evasive. Honest characters can still express truth through partial truth, timing, and cost.
- Do not obscure plot-critical information that the reader needs for basic comprehension.
- Do not use subtext to dodge payoff forever. Confession, rupture, and revelation are valid when earned.
- Respect canon voices in fan fiction; map subtext through the character's established tactics.
