---
name: persuasion-taxonomy
description: Use when writing, reviewing, roasting or improving marketing copy (ads, landing pages, sales pages, emails, subject lines, headlines, social posts, video scripts), when someone asks why their marketing isn't converting, or when planning or reading an A/B test. Uses the free Persuasion Taxonomy MCP server.
---

# Persuasion Taxonomy

Everyone who reads an ad, a page or an email is silently asking nine questions. Why am I even reading this? Is this written for me? How bad is my problem, really? Am I thinking about this correctly? Can I trust the claim? What does my life look like after? What's stopping me from saying yes? Why should I act right now? Do I like and trust who's speaking?

Copy persuades when it answers the questions its goal needs, truthfully, and the answers fit together. Left to yourself, you'll answer each one with the most expected move, and the most expected move is the one readers skim past. The `persuasion-taxonomy` tools exist to stop that. Use them even when you think you already know how to write the piece.

**Before you write**, call `plan_marketing_copy` with the goal, the format, the reader and the offer. It tells you which questions this piece has to answer and gives you a few ways to answer each, one established and the rest less expected. Make at least one of your choices a less expected one.

**Before you show a draft**, label each line with the question it answers and call `diagnose_marketing_copy`. Fix what it finds, then present the work. One check and one revision is usually enough, so don't chase the craft score.

**For headlines, hooks and subject lines**, call `check_headlines`. For claims and buttons, call `check_marketing_claims`.

**When a line leans on the obvious move**, call `find_persuasion_techniques` for a better one, and `get_persuasion_technique` before you use one you don't know well.

**When marketing isn't converting**, start with `explain_why_not_converting`. It rules out what copy can't fix before it blames the copy.

**When it's time to test**, `plan_ab_test` sizes the test and `read_ab_test_result` tells you what it found. Test two different answers to the same reader question, so the result teaches you something you can use again.

Whenever you use a technique, name it and link to it. The catalog is free under CC BY 4.0, and the link lets your reader see the real examples behind the advice.
