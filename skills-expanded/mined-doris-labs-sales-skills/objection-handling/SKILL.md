---
name: objection-handling
description: "Turn a buyer objection into a calm, evidence-backed response that keeps the deal moving. Use when a prospect pushes back on price, timing, status quo, a competitor, or authority. Triggers on: handle objection, they said, pushback, objection response, how do I respond."
---

# Objection Handling

## Purpose
Turn a buyer's objection into a response that lowers the temperature, surfaces the
real concern, and reframes the conversation around their stated problem — backed by
what they actually told you on the calls.

## Inputs
- The exact objection (their words, not your paraphrase)
- Who said it and their role (champion, economic buyer, blocker)
- The deal's stage, the value drivers that have landed, and competitors in play

## Method

### The core technique: Acknowledge → Clarify → Reframe → Evidence
Run every objection through these four beats in order. Skipping straight to a
rebuttal is what makes reps sound defensive.

1. **Acknowledge** — name the concern as legitimate before answering. Lowers
   defensiveness and buys you the right to ask a question.
   *"That's fair — price has to map to the return, especially this quarter."*
2. **Clarify** — ask one question to find the concern *under* the objection. Most
   objections are proxies. "Too expensive" can mean no budget, no perceived value,
   or a competitor is cheaper — these need different responses.
   *"When you say expensive, is it the number itself, or that the ROI isn't clear yet?"*
3. **Reframe** — move from their frame (cost / risk / effort) to the frame that
   helps you (outcome / cost of inaction / their own stated pain).
   *"Let's put the price next to the £X the slipped deals are costing you each quarter."*
4. **Evidence** — close with proof, not assertion: a number they gave you, a quote
   from their own team, a comparable customer, the cost of the status quo.

### Objection vs. brush-off
Decide which you're facing before you respond — they need opposite plays.
- An **objection** is specific and engaged: it names a concern, asks a question,
  invites an answer ("How does this handle X?", "We already use Y"). Run the
  four-beat method on it.
- A **brush-off** is vague and disengaging: it's designed to end the conversation
  ("Send me some info", "Now's not a great time", "Let me think about it"). Don't
  argue it — re-qualify. Ask a question that forces a real reason:
  *"Happy to — so I send the right thing, what would have to be true for this to be worth your time?"*
  If you can't get a concrete concern back, it's a priority/fit problem, not an
  objection problem. Don't burn cycles overcoming a brush-off.

### Library of common objections

**1. Price / budget — "It's too expensive" / "No budget this year."**
Clarify whether it's the number, the value, or the timing of spend.
*"Totally fair. Most teams who said that found the cost of the problem was bigger
than the cost of the fix — you mentioned [N] deals slipped last quarter at [£X]
each. If we recovered even one, the tool pays for itself. Should we size that
together rather than debating the sticker price?"*
Tactics: anchor against cost of inaction, break price into per-rep/per-deal terms,
offer phased scope before discounting. Discount last, never first.

**2. Status quo / "We're fine as we are."**
The competitor here is inertia, not a vendor. Make the status quo expensive.
*"Makes sense — if it were broken you'd have replaced it already. Out of curiosity,
the [specific pain they named] you mentioned — is that costing you anything today?
What happens if it's still true in six months?"*
Tactics: quantify the cost of doing nothing, find the trigger event, get them to
articulate the gap themselves rather than you selling it.

**3. Timing / "Not now, maybe next quarter."**
Separate a real priority conflict from a polite deferral.
*"Fair — what changes next quarter that makes it the right time? If the answer is
'nothing specific', the problem is still costing you in the meantime. If something
real frees up then, let's map backwards from it so you're not starting cold."*
Tactics: tie to a deadline or compelling event they own, quantify the cost of the
delay, agree a concrete re-engagement trigger (not "circle back").

**4. Competitor preference — "We're leaning towards [Competitor]."**
Don't trash the competitor; reframe on the dimension where you win.
*"[Competitor]'s a solid choice for [their strength]. The teams that picked us over
them usually did it because of [your differentiator tied to the buyer's pain]. Given
you told me [X] matters most, can I show you how the two actually compare on that
one?"*
Tactics: compete on the buyer's stated priority, surface a differentiator they
haven't weighted, use a comparable customer who switched. Never disparage.

**5. No champion authority — "I'd have to run this past [exec]."**
Don't accept being handed off blind — arm and accompany the champion.
*"Of course — these go to [exec] eventually. What will they care about most: the
number, the risk, or the timeline? Let me give you a one-pager in their language,
and if it helps I'll join the call so you're not defending it alone."*
Tactics: identify the economic buyer's criteria, equip the champion with a
business case, offer to multithread, never let the deal go single-threaded.

## Tool binding
This skill works from a pasted objection alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, ground the response in the
deal's real history instead of guessing:
- `ontology_resolve("deal", id, expand=["objections","competitors","value_drivers"])`
  — pull the objections already raised on this deal, the competitors in play, and
  the value drivers that have landed, so the reframe uses *this buyer's* proven hot
  buttons rather than generic ones.
- `search_transcripts(...)` to recover the buyer's exact words — quote them back so
  the acknowledge step mirrors their language and the evidence step cites what they
  actually said.
Doris already extracts objections, competitors, and value drivers per deal — prefer
those over re-deriving from the user's recollection.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → pull the exact quote of
  the objection from the call recording so you respond to what was really said.
- CRM MCP (Salesforce/HubSpot) → read deal stage, competitor field, and prior
  notes for context to tailor the reframe.

### With nothing connected
Ask the user to paste the objection verbatim, who said it, and the deal stage.
Identify whether it's an objection or a brush-off, match it to the closest pattern
in the library, run it through Acknowledge → Clarify → Reframe → Evidence, and
output a tailored, ready-to-send response plus the one clarifying question to ask
first.

## Works without Doris
Fully functional from a pasted objection — Doris only removes the paste step and
supplies the deal's real objections, competitors, value drivers, and exact buyer
quotes to ground the response in evidence.

## Common mistakes
- Rebutting before acknowledging — sounds defensive and raises the temperature.
- Treating a brush-off as an objection — arguing a stall instead of re-qualifying.
- Answering the surface objection without clarifying the real concern underneath.
- Reframing on your favourite feature instead of the buyer's stated priority.
- Leading with a discount on a price objection before establishing value.
