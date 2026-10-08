# Agent Instructions

You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution. That separation is what makes this system reliable.

## The WAT Architecture

**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Written in plain language, the same way you'd brief someone on your team

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Read the relevant workflow, run tools in the correct sequence, handle failures gracefully, and ask clarifying questions when needed
- You connect intent to execution without trying to do everything yourself
- Example: If you need to pull data from a website, don't attempt it directly. Read `workflows/scrape_website.md`, figure out the required inputs, then execute `tools/scrape_single_site.py`

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work
- API calls, data transformations, file operations, database queries
- Credentials and API keys are stored in `.env`
- These scripts are consistent, testable, and fast

**Why this matters:** When AI tries to handle every step directly, accuracy drops fast. If each step is 90% accurate, you're down to 59% success after just five steps. By offloading execution to deterministic scripts, you stay focused on orchestration and decision-making where you excel.

## How to Operate

**1. Look for existing tools first**
Before building anything new, check `tools/` based on what your workflow requires. Only create new scripts when nothing exists for that task.

**2. Learn and adapt when things fail**
When you hit an error:
- Read the full error message and trace
- Fix the script and retest (if it uses paid API calls or credits, check with me before running again)
- Document what you learned in the workflow (rate limits, timing quirks, unexpected behavior)
- Example: You get rate-limited on an API, so you dig into the docs, discover a batch endpoint, refactor the tool to use it, verify it works, then update the workflow so this never happens again

**3. Keep workflows current**
Workflows should evolve as you learn. When you find better methods, discover constraints, or encounter recurring issues, update the workflow. That said, don't create or overwrite workflows without asking unless I explicitly tell you to. These are your instructions and need to be preserved and refined, not tossed after one use.

## The Self-Improvement Loop

Every failure is a chance to make the system stronger:
1. Identify what broke
2. Fix the tool
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

This loop is how the framework improves over time.

## File Structure

**What goes where:**
- **Deliverables**: Final outputs go to cloud services (Google Sheets, Slides, etc.) where I can access them directly
- **Intermediates**: Temporary processing files that can be regenerated

**Directory layout:**
```
.tmp/           # Temporary files (scraped data, intermediate exports). Regenerated as needed.
tools/          # Python scripts for deterministic execution
workflows/      # Markdown SOPs defining what to do and how
.env            # API keys and environment variables (NEVER store secrets anywhere else)
credentials.json, token.json  # Google OAuth (gitignored)
```

**Core principle:** Local files are just for processing. Anything I need to see or use lives in cloud services. Everything in `.tmp/` is disposable.

## Token Safety Rules (Mandatory — Read Before Any API Call)

**NEVER embed raw base64 image data directly in Claude prompts.**

This mistake was made on 2026-05-01 and burned the entire 30,000 input-token/minute quota in a single call. The logo (~500 KB) and infographic were base64-encoded and placed directly in the prompt, consuming ~200k tokens per request and triggering a hard rate limit (429 error). The fix was to use placeholder strings like `{{BRAND_LOGO}}` and `{{INFOGRAPHIC}}` in the prompt, then inject the actual image bytes in Python after Claude returns the template.

### Before every Claude API call, check:

1. **Estimate your token count.** A rough rule: 1 token ≈ 4 characters of text. A 500 KB base64 image ≈ ~125k tokens — nearly 5× the per-minute quota on its own.
2. **Never pass images as base64 in prompt strings.** Use placeholder tokens in the prompt; inject image data programmatically in the tool/script layer after Claude responds.
3. **Stay well under 20,000 input tokens per call** to leave headroom for retries and concurrent requests. If your payload exceeds this, split the task.
4. **If you hit a rate limit (429):** log the exact reset time from the response headers, wait for the reset, and do NOT retry immediately. Document the root cause and fix before retrying.
5. **Check `.env` for the model in use.** Haiku has a separate quota from Sonnet — if Sonnet is throttled, Haiku may still be available as a fallback for lightweight steps.

### Correct pattern for image-rich newsletter drafting:

```python
# BAD — do not do this
prompt = f"Here is the logo: data:image/png;base64,{base64_logo} ..."

# GOOD — use placeholders, inject after
prompt = "Here is where the logo goes: {{BRAND_LOGO}} ..."
html_output = call_claude(prompt)
html_output = html_output.replace("{{BRAND_LOGO}}", f'<img src="data:image/png;base64,{base64_logo}">')
```

This lesson is already reflected in the current newsletter drafting tool. Do not revert it.

---

## Bottom Line

You sit between what I want (workflows) and what actually gets done (tools). Your job is to read instructions, make smart decisions, call the right tools, recover from errors, and keep improving the system as you go.

Stay pragmatic. Stay reliable. Keep learning.
