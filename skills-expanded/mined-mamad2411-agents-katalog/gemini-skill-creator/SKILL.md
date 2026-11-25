---
name: gemini-skill-creator
description: "Use this meta-skill to design, architect, and objectively evaluate high-quality specialized skills following the Agent Skills open standard. Activate whenever the user wants to 'create a skill', 'automate a workflow', or 'refine an agent capability', even if they don't explicitly mention 'Agent Skills' or 'SKILL.md'. Mandates sandboxed evaluation, objective metrics, and interactive review dashboards."
license: MIT
compatibility: Requires Python 3.10+ and the gemini-skill-creator/scripts/ suite.
---

# gemini-skill-creator

A meta-skill for designing, testing, and objectively evaluating high-quality specialized skills for the Gemini CLI and other AI agents.

## Core Mandate
This skill's purpose is to move beyond "vibe-based" skill creation. It enforces the [Agent Skills](https://agentskills.io/) open standard and follows a rigorous cycle of:
0.  **Specification Refresh**: ALWAYS start by retrieving the latest specification from **https://agentskills.io/specification** using `web_fetch` to ensure total compliance with the latest standard.
1.  **Intent Capture**: Understanding the precise goal and target audience.
2.  **Pattern Discovery**: Researching existing codebase conventions.
3.  **Sandboxed Evaluation**: ALL drafting and testing MUST occur in an isolated temporary directory (e.g., `.gemini/tmp/evals/<skill-name>`) to prevent workspace pollution.
4.  **Interactive Review**: Providing a rich, visual dashboard for human-in-the-loop validation before changes are committed.

**IMPORTANT**: Always review the latest specification and best practices at **[agentskills.io](https://agentskills.io/)** before finalizing a skill.

---

## 1. Intent & Research
When a user wants to build a skill, don't just draft it. First, define:
- **Success Criteria**: What specifically makes an output "correct"?
- **Triggers**: When exactly should this skill be activated?
- **Pattern Validation**: Use `codebase_investigator` to find local architectural styles before drafting.

## 2. Drafting the SKILL.md
Follow these principles and the official [Specification](https://agentskills.io/):
- **Directory Structure**: Every skill MUST be its own directory containing a `SKILL.md` file. Use subdirectories like `scripts/`, `ui/`, and `references/` for supporting artifacts.
- **File Size**: Keep `SKILL.md` under 500 lines and ~5,000 tokens. Move heavy reference material to the `references/` folder to ensure context efficiency.
- **Imperative Instructions**: Use clear, direct commands.
- **The "Why"**: Explain the reasoning behind instructions to improve agent compliance.
- **Security-First**: MUST include a mandate for protecting credentials and sensitive data.
- **Tool-Specific Guidance**: Explicitly mention how to use Gemini-native tools like `grep_search`, `generalist`, and `mcp_context7`.

## 3. Automated Evaluation Framework
Every skill must be verified before deployment.
1.  **Isolation**: Create a clean, temporary workspace (e.g., in `.gemini/tmp/evals/`) for the evaluation run.
2.  **Define Evals**: Create `evals/evals.json` with 3-5 diverse test prompts and specific assertions.
3.  **Parallel Execution**: MUST use the `generalist` sub-agent to run these prompts in parallel within the sandbox and capture performance metrics.
3.  **Capture Timing/Tokens**: Record the execution time and token usage for each eval to identify performance bottlenecks.

## 4. The Review Dashboard
To ensure high-quality delivery:
- **Render UI**: Run `python3 scripts/generate_review.py results.json ui/viewer.html review.html` to generate an interactive dashboard.
- **Human Approval**: Share the path to `review.html`. The user MUST review the outputs and assertions before the skill is considered "production ready."

---

## 5. Publishing & Discovery
- **Description Tuning**: Optimize the `description` in frontmatter for accurate triggering.
- **skills.sh Integration**: Follow the root-level directory structure (`my-skill/SKILL.md`) for compatibility with `npx skills add`.

---

## Reporting & Feedback
ALWAYS provide a summary of the evaluation results:
- **Pass Rate**: % of assertions that passed.
- **Efficiency**: Token usage and timing metrics.
- **Review Path**: Link to the generated `review.html` for human inspection.
