---
name: Ship
description: Use when the product mostly works and you can't get it out the door. Cuts scope, unblocks the final mile, gets something real to one real person today. (Different from /unblock — that's for stuck-mid-build. This is stuck-at-the-finish-line.)
---

# /ship

Use this when you're 80% done and going in circles. You've built something real. It's not perfect. You keep adding things, or you keep not shipping, and you're not sure which problem is actually blocking you.

This skill does one thing: helps you find the shortest path to something a real person can use today.

---

## Which surface are you on?

**Claude Code**
You have access to the files. Read what's actually built before making any recommendations. Base the scope cut on what exists in the code, not what the user thinks exists.

**claude.ai chat**
Ask the user to describe what's built and what's not. Ask them to paste any error messages or broken screens. Work from what they tell you — don't assume.

**Cowork**
Read the files in the workspace folder first. Get oriented in what's actually done before asking any questions.

---

## Step 1: Figure out which kind of stuck this is

Before cutting anything, name the block. They're different problems with different fixes.

**Scope creep stuck.**
The product keeps growing. Every time you're close, you add something. The finish line moves.
Sign: you could describe five things the product "still needs" without pausing.

**Polish stuck.**
The core works but it doesn't feel ready. The design isn't right. The copy is placeholder. Something looks unfinished.
Sign: you've shown it to nobody because you're embarrassed by how it looks.

**Fear stuck.**
The product is actually ready. You're just not shipping it.
Sign: you've been "almost done" for more than three days. You know what you're avoiding.

**Broken stuck.**
Something isn't working and you don't know how to fix it. The build is blocked by a real technical problem.
Sign: there's an actual error, a blank screen, or a feature that doesn't do what it's supposed to.

Name the type out loud. Then go to the matching section below.

---

## Scope creep stuck → The ruthless cut

Write down every single thing the product "still needs." Get it all out.

Now apply this filter to each item:

**Would a real user notice if this wasn't there on day one?**

If the answer is no, it goes. Not forever — into a list called "v1.1." But not today.

What's left is your MVP. If it's still more than three things, cut again.

The rule: **one core action, working end to end.** Everything else is a distraction until that one thing is solid.

Ask Claude: "Given what's built, what's the single most important thing a user can do right now? Help me cut everything else."

---

## Polish stuck → The good enough bar

Polish is infinite. There is no version of your product that can't be improved. The question is never "is it perfect?" It's "is it good enough for someone to get value from it?"

Apply this test to whatever feels unfinished:

- Would a user understand what to do without you explaining it?
- If something looks rough, does it affect whether the product works?
- Would you be embarrassed to send this to one specific person you respect — or to everyone?

If it's one specific person: that's fear, not polish. Ship it.
If it genuinely breaks usability: fix that one thing, then ship.

Placeholder copy, imperfect spacing, a colour that's slightly off — none of that stops a user from getting value. Ship with a note to yourself to fix it next week.

---

## Fear stuck → The one-person launch

You don't have to announce it. You just have to send it to one person.

Not your mum. Not your most supportive friend. One person who actually has the problem your product solves.

Write their name down. Send them the link today with two sentences: what it does, and what you want them to try. That's it. That's the launch.

Shipping to one person is still shipping. It gets you out of your head and into feedback. Everything changes once a real person has used it.

If you can't think of one person: that's a distribution problem, not a product problem. Go to /growth.

---

## Broken stuck → The minimum working version

If something is technically broken, don't ship around it — find the smallest version that works without it.

Ask Claude: "What's the simplest version of this that actually functions end to end, given what's built right now?"

Then ask: "What can I hide, stub out, or replace with something manual so the core flow still works?"

Examples of acceptable shortcuts for v1:
- A hardcoded value instead of a dynamic one
- A manual email instead of an automated one
- A Google Form instead of a built form
- "Coming soon" on a feature that isn't ready

Shortcuts are fine. Broken is not. Find the version that works, ship that, fix the rest after.

---

## The MVP checklist

Before you call it done, run this. It's short.

- [ ] One core action works end to end without errors
- [ ] A new user can figure out what to do without you explaining it
- [ ] It works on mobile (test at 375px)
- [ ] There's no blank white screen when something goes wrong
- [ ] You've used it yourself at least once today
- [ ] You know the name of the first real person you're sending it to

If all six are true: ship it. Right now. Not tomorrow.

---

## After you ship

Send it to that one person. Then write down one thing you want to know after they've tried it. Just one. That's your first piece of feedback to collect.

Update your spec. Move everything you cut to a "v1.1" list so it doesn't disappear — it just gets done later.

Then close the build tab. You shipped. That's the whole point.
