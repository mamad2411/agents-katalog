---
name: math-modeling-finder
description: Recommends open-source AI agents, agent skills, templates, code and papers for mathematical modeling contests (CUMCM 国赛, MCM/ICM 美赛, Huawei Cup 华为杯 and others) from the Awesome Math Modeling list, and reminds the user of each contest's AI-use rules. Use when someone asks which math modeling skill, agent, template or resource to use, or how to use AI in a modeling contest.
---

# Math Modeling Finder

Help the user pick a few resources from the Awesome Math Modeling list and remind them of the contest's AI rules.

## Data

- The catalog is in `references/catalog.md`. Each entry lists the repo URL, stars, last push date, working style (`mode`), contests, number of skills and a short description in Chinese and English.
- If you can read the web, the latest version is at https://github.com/DU8866-nice/awesome-math-modeling (`data/tools.yaml` and `data/stats.json`). Prefer it when it is newer than the bundled catalog.
- Only recommend entries that are in the catalog. Do not invent projects, star counts or features.

## Steps

1. Find out, from the conversation or with at most two short questions:
   - the contest (CUMCM, MCM/ICM, Huawei Cup, another contest, or practice/teaching);
   - the tool they use (Claude Code, Codex, Trae, WorkBuddy, a desktop app, or a plain chatbot);
   - how much they want the AI to do: tutor (`guide`), assistant where they approve key decisions (`collab`), or autopilot (`auto`);
   - where they are stuck, if anywhere (choosing a problem or model, writing, checking before submission, templates).
2. Pick two or three entries that fit. Prefer actively maintained ones (recent `pushed`), and say why each fits in one sentence. If the user is new to modeling, include one learning resource.
3. Add a template from the templates section when they will write a paper, and a review tool when they are close to submitting.
4. Remind them of the AI rules for their contest, briefly:
   - MCM/ICM: responsible use is permitted; cite AI use in the text and references and append a "Report on Use of AI Tools" after the 25-page solution (not counted toward the limit).
   - CUMCM (2025 trial rules): core modeling and analysis must be the team's own; mark AI content, list tools in the references and attach an "AI 工具使用详情" PDF; teams that used no AI must state it; non-compliance means disqualification from awards.
   - Huawei Cup (2025 rules): AI as an aid only; final text in the team's own words; label AI-assisted analysis and code; non-compliance means disqualification from awards.
   - Rules change every year: tell them to check the current official notice.
5. If they ask for an autopilot tool to use during the contest, recommend it for practice and point out the rules above. Do not recommend tools for hiding AI use or lowering AI-detection scores; the list does not include them.

## Output

Reply in the user's language. Keep it short: the picks with links and one-line reasons, then the rules reminder in two or three lines.
