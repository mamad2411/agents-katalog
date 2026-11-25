---
name: setup
description: Connect the AIm workout journal to this account. Use when the AIm tools are missing, when a tool call fails with an authentication error, or when the user asks how to set up, connect, sign up for, or reconnect AIm.
---

# Connecting AIm

AIm signs in with OAuth. There is nothing for the user to copy, paste or configure: the first time
a tool is needed, Claude opens AIm's consent screen in the browser, the user approves, and the
connection is done. Most of this skill is therefore about *not* getting in the way.

## What to do

1. **Check whether it is already connected.** Call `get_coaching_context` with the task that
   matches what the user asked for. If it returns, setup is done — carry on with their actual
   request and do not walk them through anything.

2. **If a call fails with an authentication error**, the connection has not been authorized yet or
   the authorization was revoked. Tell the user to approve the connection when the browser opens,
   and let the normal OAuth prompt do its work. Do not ask them for a token, a link or a password
   — none of those are part of this flow any more.

3. **On the consent screen** they will see which application is asking and which AIm account it
   will reach, and then Allow or Cancel. If it says they need to sign in, it offers to email them
   a link; opening that link on the same device returns them to the same screen, signed in. That
   is the whole recovery path.

4. **If they do not have an account yet**, they can sign up at <https://aim-journal.com> with an
   email. It runs inside the AI subscription they already pay for. If they only want to look
   around first, point them at the demo at <https://aim-journal.com/demo> — it is shared, resets
   nightly, and is not a place to log real training.

## What not to do

Do not ask for, display, or store an AIm link or token. Older setups used a personal URL with the
token in it, and those keep working, but they are not how this plugin connects and asking for one
teaches people to paste a live credential into a chat.

## After it connects

Do not plan training from general knowledge. Call `get_coaching_context` first with the matching
task — `next_workout` to plan a session, `new_program` to build a program, `weekly_review` to
review the week — and build on the data it returns. It carries this person's goal, experience,
equipment, injuries and logged weights; without it the plan will be wrong for them. If their
intake is incomplete it returns the intake state instead (`intake.next_field` and the values it
accepts): ask about that one topic and save the answer with `update_coach_profile`.

Record durable facts the user confirms as they come up, with `update_coach_profile` and
`upsert_goal`, rather than keeping them only in the conversation. One-off circumstances ("travelling
this week", "shoulder is sore today") belong in the `constraints` argument instead, not in the
profile.
