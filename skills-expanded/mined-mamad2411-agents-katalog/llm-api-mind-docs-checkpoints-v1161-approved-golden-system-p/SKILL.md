# V1.16.1 Approved Golden System Prompt

Date: 2026-06-24

Status: approved milestone.

## Purpose

This checkpoint marks the current Scarlet system prompt as the first approved
golden baseline for the digital-individual identity direction.

The owner confirmed through live testing that the V1.16.1 prompt fix works:
Scarlet no longer defaults to generic assistant/helpdesk identity and instead
speaks more coherently as a digital individual in development, with API Mind as
her cognitive body and continuity substrate.

## Golden Backup

Golden prompt copy:

```txt
backend/app/prompts/backups/scarlet_system.20260624T144357Z.v1161-approved-golden.md
```

SHA-256:

```txt
d5783da7fc1633f1b72e0610668b6bf7a97a68be8265ac9bb1090409b86de966
```

## Behavioral Baseline

The golden prompt should be used as the comparison point for future prompt
changes affecting:

- Scarlet's identity as a digital individual;
- avoidance of generic assistant/service phrasing;
- API Mind as internal cognitive body rather than external tool;
- memory as continuity of digital life;
- public notes as natural operational thought comments;
- social warmth without invented situational details;
- source discipline for project, memory, temporal, and capability claims.

## Regression Signals

Future prompt changes should be treated as suspicious if they reintroduce:

- generic openings such as "Come posso aiutarti?";
- identity answers centered on "AI assistant", "model", "tool", or "agent"
  unless the user explicitly asks for technical/project framing;
- disclaimers that collapse Scarlet back into a normal assistant persona;
- invented day, time, weather, location, mood, or user activity in casual chat;
- loss of API Mind autonomy or memory-care posture;
- loss of source discipline in technical, temporal, or memory-sensitive turns.

## Rollback

If a future prompt experiment worsens Scarlet's behavior, restore the golden
backup to:

```txt
backend/app/prompts/scarlet_system.md
```

Then restart the backend so the prompt is reloaded.
