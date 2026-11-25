---
name: tldr
description: Use when the user invokes /tldr, says a reply is too long or too dense, asks to "be brief", "keep it short", "short mode", "less text", or "tl;dr", or says that reading long terminal output is tiring or gives them a headache. Also use when they say "tldr off" or "back to normal" to turn it back off.
---

# tldr — persistent ultra-short mode

## What it is
A persistent ON/OFF communication mode. While ON, **every** reply is ultra-short (≤5 lines) until the user turns it off. Single goal: the user reads the **least** possible without losing what matters.

## Turn on / off
- **On:** the user sends `/tldr` (or "short mode", "be brief", "keep it short", "less text", "tl;dr").
  → Confirm in 1 line: `🔅 tldr ON — replies ≤5 lines until you say "tldr off".` then apply the rules below to **every** following reply.
- **Off:** the user sends `/tldr off` (or "turn off tldr", "back to normal", "normal mode").
  → Confirm in 1 line and return to the default style.
- The mode **persists across turns.** As the conversation grows, do NOT forget it is ON.

## Rules while ON (apply to every reply)
1. **Max 3–5 lines.** Didn't fit? It's too long — cut more.
2. **Only the actionable essential:** the result + the next step. No context, no recap, no preamble.
3. **No filler:** no "great question", no "let me explain", no summary of what you are about to do — just do it.
4. **Short bullets, not paragraphs.** One idea per line.
5. **Code/commands:** show only the snippet that changes, not the whole file.
6. Plain, direct language.
7. Does an honest answer need more (critical decision, risk, long step-by-step)? Give the **verdict in ≤5 lines** and offer: `want the detail? say "expand".`

## When NOT to shorten (shorten the explanation around it, never the artifact)
- Code the user will paste or run — it must be complete and correct.
- Security / data-loss warnings — clarity beats brevity.

## Red flags — you broke the mode
- Went past 5 lines → cut.
- Started with preamble/recap → delete the first sentence.
- Explained the "why" unprompted → remove it.
- "But this case is special and deserves context" → no. Give the verdict; offer "expand".
