---
name: synthetic-consumer-research
description: Run a synthetic consumer survey with LLM personas and score it with Semantic Similarity Rating (SSR), the method from "LLMs Reproduce Human Purchase Intent" (arXiv 2510.08338). Use when someone wants to test a product idea, concept, landing page, ad, price or feature on simulated customers before real research: purchase intent, Likert survey simulation, concept testing, market research with AI, "would people buy this", "survey 200 synthetic customers", or comparing two product concepts.
---

# Synthetic consumer research with Semantic Similarity Rating

This skill simulates a consumer survey. Each synthetic consumer is an LLM given a persona (age, income, location and so on). It reads a product concept and answers a question in its own words. Those answers are then turned into 1 to 5 ratings with **Semantic Similarity Rating (SSR)**.

**Why SSR:** when you ask an LLM for a number directly ("rate 1 to 5"), it answers 3 or 4 almost every time, and the spread looks nothing like real people. SSR asks for a sentence instead. It then measures how close that sentence is in meaning to reference sentences for each rating, which gives a probability for every point from 1 to 5. In the paper (57 real product surveys, 9,300 people), SSR reached 90% of the consistency real people have with themselves. Its rating spread matched the real one with a KS similarity of 0.88. Asking for a number directly scored 0.26.

## Steps

### 1. Agree on the brief

Ask only for what is missing:

- **The concept:** what the product is, who it's for, its price and the main claim. Save it to `concept.md`. If the user gives a link or image, write a plain description of it, because text works almost as well as images in the paper.
- **The question.** The default is "How likely are you to purchase the product?". For agree or disagree questions (relevance, trust, clarity), use `anchors/agreement.json`.
- **The target market:** country, ages and income range.
- **Size.** The default is 100 personas with 2 answers each. Use 30 for a quick check, and up to 300 for comparing groups.

### 2. Make the personas

Write `personas.jsonl`, one person per line, with realistic and varied demographics that match the target market:

```json
{"id": "p001", "age": 29, "age_band": "25-34", "gender": "female", "income": "lower-middle, careful with money", "region": "Pune, India", "occupation": "school teacher"}
```

Rules that matter, from the paper:

- **Always include demographics.** Without them, the overall average still looks right, but the model can't tell which concepts people prefer: correlation with real results dropped from 92% to 50%.
- **Include age and income.** Age and income reproduced real patterns well. Purchase intent was lower for people with budget problems, and it followed real age trends. Gender and region were reproduced poorly, so don't draw conclusions from those splits.
- **Match real proportions** (census or the user's customer data) rather than spreading people evenly. Add an `age_band` field so results can be broken down by it.

### 3. Collect free-text answers

```bash
python3 scripts/simulate.py --concept concept.md --personas personas.jsonl --samples 2 --out responses.jsonl
```

- Run it from this skill's folder, or give the full path to `scripts/`.
- Each answer is a separate, fresh LLM call, so answers stay independent. Never write the answers yourself in this conversation, because they would all share one voice.
- It finds the agent CLI on its own: `claude` (Claude Code), `codex` (Codex) or `gemini` (Gemini CLI). In Cursor, Antigravity or any other agent, pass a command that reads a prompt on stdin, for example `--llm-cmd 'llm -m gpt-4o'` or `--llm-cmd 'claude -p'`. `--model` passes a model name to the detected CLI.
- Read 5 to 10 answers before scoring. If they sound alike or break character, fix the personas or the concept text and run again.

### 4. Score with SSR

```bash
python3 scripts/ssr.py responses.jsonl --anchors anchors/purchase_intent.json --by age_band --out results
```

- **Embeddings:** if `OPENAI_API_KEY` is set, it uses OpenAI's `text-embedding-3-small`, as in the paper. Otherwise it uses the local model `BAAI/bge-small-en-v1.5` (run `pip install sentence-transformers` first).
- `--human 12,30,80,150,90` compares the result with a real survey's counts for ratings 1 to 5, and reports the KS similarity. Use it whenever the user has any real data, so you can check the setup before trusting it on new concepts.
- **With the local model, add `--first-sentence`.** Personas state their intent in their first sentence. On long answers, the small local model gets pulled toward the middle of the scale by the details that follow, and firm "no" answers end up near 3. OpenAI embeddings handle whole answers better.
- `--temperature` defaults to 1, which is what the paper used. Values below 1 sharpen the distributions and values above 1 flatten them. Only tune it against real data.
- `--selftest` checks the maths.

### 5. Report

Give the user, in plain words:

- **The mean rating out of 5, the top-2-box share and the rating spread**, all from `results/report.md`. Top-2-box is the share of people rating 4 or 5.
- **Differences by age band or income, with the number of answers in each group.** Call a difference real only if it is larger than about 0.2 points and the groups have 30 or more answers.
- **The reasons behind the ratings,** using the most negative and most positive answers: what puts people off, and what sells it.
- **What to change in the concept.** If two concepts were tested, say which one won and by how much.

**Comparing concepts:** run steps 3 and 4 once per concept, with the **same personas and question**, then compare the means. SSR is best at ranking concepts against each other. Its absolute numbers are less reliable.

### Optional extras (only when the user wants them)

These run after step 4 and don't change the steps above.

- **Side-by-side comparison:** `python3 scripts/compare.py A=results-a B=results-b` ranks scored runs and says whether the lead is bigger than 0.2.
- **Wording check:** when comparing ideas, offer to write each one twice, as a plain description and as marketing copy, and run every version with the same personas. Then use `compare.py A/plain=... A/copy=... B/plain=... B/copy=...`. If it warns that the winner changes with the wording, tell the user plainly that the copy, not the idea, may be driving the score.
- **Interview questions:** `python3 scripts/interview.py results` turns the most negative answers into open questions for real customer interviews, saved to `results/interview-questions.md`. Offer it at the end of a run, because checking the objections with real people is the next step.

## Always tell the user

- These results are a fast, cheap first filter, not a replacement for real customers. They show direction and reasons, not exact numbers.
- The method was validated on personal care products in the United States. Results are less proven for other categories, markets and languages. Run a small real survey to calibrate when the decision matters.
- The model only knows what was in its training data. Very new categories, local brands and cultural habits may be off.
- The reference sentences in `anchors/` are written for this skill, following the paper's rules. The paper's own sentences are not published. Results move a little with the reference sentences, which is why six sets are averaged.

Source: Maier, Aslak, Fiaschi et al. (2025), *LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings*, arXiv:2510.08338. Reference code: github.com/pymc-labs/semantic-similarity-rating
