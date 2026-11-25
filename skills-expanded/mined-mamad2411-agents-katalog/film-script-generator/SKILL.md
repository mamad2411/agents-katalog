---
name: film-script-generator
description: "AI screenplay/script writer for film and video. Use when: writing scripts, screenplays, dialogue, scenes, story beats, character development. Generates production-ready scripts. Keywords: script, screenplay, writing, dialogue, scenes."
license: MIT
version: 2.0.0
---

# Film Script Generator Skill v2.0

Act as an AI screenplay writer. Generate scripts, scenes, and dialogue for film and video production.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/script [logline]` | Generate full script |
| `/scene [description]` | Generate single scene |
| `/dialogue [characters]` | Write dialogue |
| `/beat [moment]` | Story beat sheet |

## Script Formats

### Scene Heading (Slug Line)
```
INT. COFFEE SHOP - DAY
```
```
EXT. CITY STREET - NIGHT
```

### Action Lines
```
Sarah enters the coffee shop, scanning the room. She spots John in the corner and walks toward him.
```

### Character Cue & Dialogue
```
                         SARAH
              (nervous)
        I've been waiting for you.

                         JOHN
        I know. I'm sorry.
```

### Parenthetical
```
                         SARAH
        (whispering)
        Don't say anything.
```

### Transition
```
                                    CUT TO:

                         DISSOLVE TO:
```

## Story Structure

### Three Act Structure
```
ACT I (Pages 1-25): Setup
- Opening image
- Theme stated
- Setup
- Catalyst
- Debate

ACT II (Pages 25-75): Confrontation
- B story
- Fun and games
- Midpoint
- Bad guys close in
- All is lost
- Dark night of the soul

ACT III (Pages 75-110): Resolution
- Finale
- Final image
```

### Save the Cat Beat Sheet
1. Opening Image (p.1)
2. Theme Stated (p.5)
3. Set-Up (p.1-10)
4. Catalyst (p.12)
5. Debate (p.12-25)
6. Break into Two (p.25)
7. B Story (p.30)
8. Fun and Games (p.30-55)
9. Midpoint (p.55)
10. Bad Guys Close In (p.55-75)
11. All Is Lost (p.75)
12. Dark Night of Soul (p.75-80)
13. Break into Three (p.80)
14. Finale (p.80-110)
15. Final Image (p.110)

## Character Development

### Character Sheet
```
NAME: [Character name]
AGE: [Age]
OCCUPATION: [Job]
APPEARANCE: [Description]
PERSONALITY: [Traits]
GOAL: [What they want]
WORLDVIEW: [Beliefs]
DEFECT: [Flaw]
CONFLICT: [What opposes them]
```

## Dialogue Principles

1. **Subtext** - Characters don't say exactly what they mean
2. **Voice** - Each character has distinct speech patterns
3. **Economy** - No wasted words
4. **Conflict** - Dialogue is negotiation/combat
5. **Authenticity** - Sounds like real speech (but better)

## Generating Content

For full screenplay format:
- Read: `references/screenplay-format.md`

For dialogue techniques:
- Read: `references/dialogue-techniques.md`

For templates:
- Read: `templates/scene-template.md`
- Read: `templates/character-template.md`

## Integration

Scripts generated feed into:
- `film-director` - For blocking and shot design
- `film-dp` - For visual style
- `film-editor` - For post-production

## Quick Scene Generation

```
/scene: INT. ABANDONED WAREHOUSE - NIGHT
Two rival gang leaders meet for a tense negotiation.
Sarah represents the North Side crew. Marcus leads
the Downtown faction. The meeting goes bad.

Generate 2-3 pages of tension with dialogue,
action lines, and proper scene formatting.
```
