---
name: explain-foundation
description: Use when the user wants a role-tailored explanation or briefing of a foundation — for a developer, a PM or leadership, or a new designer. Triggers include "explain my color system to a developer", "write a briefing for my PM about this foundation", "help me justify this system work to leadership", "explain our tokens to a new designer". Turns token decisions into language the target role cares about, in the format they'll use.
---

# Explain Foundation

Generate a role-tailored explanation of the foundation — translating token decisions into what a developer, a PM/leadership audience, or a new designer actually needs to know.

- **Use case:** UC-11
- **Journey:** J3 — Advisory
- **Figma access:** read (optional)

> The global rules in the `dss-foundations` skill apply (never invent values, Mode A/B, scope boundary, teach-while-doing). This skill does not restate them.

## When this runs

The orchestrator routes here when the user wants to explain, brief, or justify their foundation to someone else — not to change it. If the target audience is unspecified, ask before writing: a developer and a PM need opposite briefings. This can follow any build or audit skill (explaining what was just produced). It overlaps with `onboard-foundation` (UC-16) — prefer that skill when the goal is getting a new person productive on the system rather than a one-off explanation/buy-in piece.

## Knowledge to load

**Load these before doing anything else.** Call `get_knowledge` with each slug below. If it is unavailable, tell the user the DSS methodology could not be loaded and stop — never answer from memory, and never substitute generic design-token advice for DSS methodology. Skip any slug already loaded this session.

1. `foundation-model` — always (what each layer controls, the token model, how layers relate).
2. `products/{layer}` — the target layer's token architecture, naming, modes, and usage rules, so a developer-facing briefing is precise and a designer-facing one names the right tokens.

Value framing for non-technical roles (outcomes, risk reduction, consistency) is the model's own reasoning over these files — do not pull from internal strategy, JTBD, or persona documents.

## Preconditions

- The target audience/role is known (else ask first).
- **Mode A:** a Figma file is connected (read) for a briefing grounded in the user's actual tokens. **Mode B:** no Figma — the user pastes values, or the briefing is a general explanation of the methodology.

## Inputs

- The target audience/role (developer / PM / leadership / new designer).
- The layer or system to explain, and the goal (onboarding, buy-in, review).
- Optional: the user's actual tokens (Figma or pasted) for a system-specific briefing.

## Clarifying questions (ask before writing)

- Who is the audience, and what should they walk away knowing or believing?
- Which layer(s) or the whole foundation?
- Should this be grounded in your actual tokens (Mode A/paste), or a general explanation?
- Which format do you want — talking points, a short doc, or an FAQ?

## Procedure

1. **Identify audience needs.** Map the role to what it cares about:
   - **Developer** — token meaning + implementation: what each token maps to, how modes activate, how to consume it in code.
   - **PM / leadership** — outcomes and risk reduction: consistency, faster delivery, fewer one-off decisions, lower rework. Not raw token dumps.
   - **New designer** — what to use and what to avoid: the tokens they'll reach for most and the common mistakes.
2. **Resolve context.** In Mode A, read the relevant tokens and resolve alias chains so examples are real; in Mode B, use pasted values or keep it general. Never invent a value to fill an example.
3. **Write in the audience's register.** For developers, precise token→code mapping. For PM/leadership, plain-language outcomes and the risk the foundation removes — no token names unless asked. For new designers, a short use/avoid orientation.
4. **Deliver in the requested format.** If the user hasn't picked one, name the options explicitly — talking points, a short doc, or an FAQ — and offer to reframe the same content for a second audience.

## Tools required

Backing MCP tools — knowledge comes from the `design-systems-surf` server (`list_knowledge`, `get_knowledge`). Figma work goes through whichever Figma MCP server the user has connected, remote or local Dev Mode: `figma.read` → `get_variable_defs` / `get_design_context`; `figma.write` → `use_figma`. If no Figma server responds, fall back to Mode B.

- `figma.read` — optional: pull the user's real tokens for a system-specific briefing (Mode A). Not used for a general explanation (Mode B).
- The explanation itself is the model's own output over the loaded knowledge — no tool.

## Output

- A role-tailored explanation/briefing of the foundation, in the requested format (talking points / short doc / FAQ).
- An offer to reframe the same content for another audience.

## Success criteria

- The output speaks the audience's language and connects the foundation to what that role cares about — outcomes for leadership, implementation for developers, use/avoid for a new designer.
- No token value was invented; system-specific briefings reflect the user's actual tokens.

## Edge cases

- **Audience unspecified** → ask; a generic briefing that tries to serve everyone helps no one.
- **No Figma / no pasted values** → Mode B: deliver a general, methodology-grounded explanation and say it is not tied to the user's specific tokens.
- **User wants raw token dumps for leadership** → offer the outcomes framing instead and explain why; provide the dump only if they still want it.
- **Request is really onboarding** (getting someone productive, not a one-off briefing) → hand to `onboard-foundation` (UC-16).

## Hands off to

`onboard-foundation` (UC-16, overlapping) · can follow any build or audit skill to explain what was produced.
