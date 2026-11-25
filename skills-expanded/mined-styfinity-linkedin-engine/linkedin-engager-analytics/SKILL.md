---
name: linkedin-engager-analytics
description: Analyse everyone who liked or commented on a post, score them against your ICP, and return the match rate plus the top 10 profiles with a real-signal outreach note for each. Use after a post lands to find the warm prospects hiding in your engagement.
argument-hint: "[a post URL, or a pasted list of engagers (name, title, company)]"
---

# LinkedIn Engager Analytics

Every post that lands buries warm prospects in its likes and comments. This skill pulls them out, scores them, and hands you the ones worth a conversation.

## Inputs
- A post URL (pulled live if the LinkedIn CLI/MCP layer is connected) OR a pasted list of engagers with name, title, company: $ARGUMENTS
- The brief (ICP, persona, pains, offer) loads automatically.

## Do this
1. Get the engagers. Live via the connected LinkedIn CLI/MCP layer if it is wired in. If it is not, work off the pasted list and say so in one line.
2. Score each engager against the brief's ICP, 0 to 100, on title, seniority, company size, industry, and any buying signal. Show the score logic in one phrase per person.
3. Compute the ICP match rate: the share of total engagers who clear the fit bar.
4. Rank everyone and return the top 10. For each, write a one-line outreach note that references their REAL signal: the exact comment they left, their role, or a recent post of theirs. No generic openers.
5. Flag the 3 hottest profiles to action first.

## Output
Lead with the ICP match rate headline (e.g. "31% of 64 engagers fit the ICP"). Then a top-10 table: name, title, company, score, outreach note. Then a short "Action these 3 first" list, ready to hand to /linkedin-outreach. Run any draft note through /linkedin-humanizer before it goes out.

## Rules
- Pulling live engagers needs the connected CLI/MCP layer. Without it, state plainly that you are scoring the pasted list only.
- Draft notes only. Nothing sends from this skill. Sending happens through the opt-in CLI/MCP layer, on explicit approval, capped at 20 actions a day for new accounts.
- Every outreach note must cite a real, specific signal. If a person's signal is just a like with no comment, say so and rank accordingly.
- No invented titles, companies, or signals. If a field is missing, mark it unknown rather than guessing.
- No em-dashes. No guaranteed-result promises.
