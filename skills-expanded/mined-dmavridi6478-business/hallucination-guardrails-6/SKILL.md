---
name: hallucination-guardrails-6
description: The six groups of practical ways to reduce AI hallucination from a Sivasankar Natarajan infographic (grounding in real data, safety and guardrails, smarter reasoning, human oversight, model and training enhancements, monitoring and continuous learning), eighteen actions in all, each with an evidence question and an honest note on what it can and cannot guarantee. Use when designing or auditing an AI workflow that must be accurate, adding checks to a prompt or app, or answering what to do about hallucinations.
---

# How to stop AI from hallucinating: six groups, eighteen actions

Source: a 12-second video of an infographic by Sivasankar Natarajan (@shiva.bytes), "Practical ways to make AI more accurate, reliable and trustworthy". Action text below is the infographic's; the "evidence" column and the limits are mine. Two typos on the graphic ("guadrails", "continous") were corrected.

| Group | Action (as printed) | Evidence to ask for [mine] |
|---|---|---|
| **1 Grounding in real data** | Connect to trusted sources: pull facts from real databases or documents | A list of the sources and a sample answer traced to one |
| | Use live data: link AI with tools and APIs for up-to-date results | Which APIs, how fresh |
| | Show references: ask AI to share where it got the information | Citations a person can open and match to the claim |
| **2 Safety and guardrails** | Double-check: check numbers, names and dates before answers are shown | A check step in code, not only in the prompt |
| | Block risky outputs: filters stop harmful or misleading replies | Filter rules and a log of what they blocked |
| | Stress-test the AI: regularly test with tricky questions | A fixed test set and its pass rate over time |
| **3 Smarter reasoning** | Let it say "I don't know": better to admit not knowing than make things up | Prompts that allow abstention, and a count of abstentions |
| | Make AI review its own work: re-check and improve before finalising | A second pass that is allowed to change the answer |
| | Think step by step: break tough problems into smaller steps | Visible intermediate steps for hard cases |
| **4 Human oversight** | Keep humans in the loop: send low-confidence answers to a person | The threshold, and who reviews |
| | Get experts involved: doctors, lawyers or finance pros verify critical answers | Named reviewers for high-stakes outputs |
| | Learn from feedback: let users report mistakes so the system improves | A report button and what happens to reports |
| **5 Model and training enhancements** | Train on feedback: use corrected answers to teach the AI what is right | A dataset of corrections |
| | Specialize the model: smaller AIs for domains like healthcare or finance | Domain test results |
| | Reward truthfulness: training methods that favour honest answers | Training or evaluation method named |
| **6 Monitoring and continuous learning** | Track mistakes: dashboards and logs show where hallucinations happen | A metric and a dashboard |
| | Keep updating the AI: feed it fresh, verified data over time | An update schedule |
| | Set up alerts: notify teams on a suspicious or low-confidence reply | An alert rule and an owner |

## Limits the infographic does not state

- **None of this removes hallucination.** It lowers the rate and catches some cases. Say so to users. [Certain]
- **Self-review is weak.** A model checking its own answer can repeat its own mistake. Prefer checks against an external source or code. [Likely]
- **Confidence is not correctness.** A "low-confidence" gate only catches answers the model doubts, not confident errors; see `jev-vs-llm`.
- **Citations can be invented.** Always open the cited source and match it to the claim. [Certain]
- Groups 5 and 6 need engineering effort most teams cannot do quickly; groups 1 to 4 can often be applied within a week.

## Use

Score a workflow: for each of the 18 actions mark in place / partial / absent, and fix the absent items in groups 1 to 4 first. Use `/hallucination-audit`.
