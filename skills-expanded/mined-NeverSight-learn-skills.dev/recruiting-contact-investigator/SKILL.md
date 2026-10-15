---
name: recruiting-contact-investigator
description: Recruiting contact investigation for finding recruiter, talent acquisition, HR, or hiring-manager contacts from a vacancy, company, person name, HH/HeadHunter vacancy, Habr Career page, LinkedIn profile, Telegram lead, or public web traces. Use when the user asks to identify who to contact about a job, find a recruiter or hiring manager, enrich hiring contacts, or produce an outreach target list.
---

# Recruiting Contact Investigator

## Operating Rule

Run this as an investigation, not a search dump: follow leads, keep evidence, and rank contacts by likelihood that they can influence the hire.

Use only user-provided or publicly available traces. Do not invent contacts, bypass access controls, or treat a stale profile as current without evidence.

## Inputs

Extract what the user provided:

- company name
- vacancy title
- HH/HeadHunter vacancy ID or URL
- vacancy source URL
- region or language market
- known person names
- target specialty or department

If a required input is missing, infer from the source when possible. Ask only when neither the company nor the vacancy/source is known.

## Investigation Loop

1. Build search roles before searching.
   - If the input includes an HH/HeadHunter vacancy ID or URL, first run `firehh <vacancy-id>` to extract vacancy title, employer, region, skills, and description. Example: `firehh 133561763`.
   - Generate likely titles for this hire: recruiter, talent acquisition, HR partner, head of department, CPO, CTO, team lead, and role-specific leaders.
   - Completion: HH vacancy details are captured when applicable, and the role list includes recruiting roles plus at least one plausible hiring-manager path.

2. Search the company and vacancy across source branches.
   - Use the detailed branch playbook in [contact-search-playbook.md](references/contact-search-playbook.md).
   - Always run the Telegram branch for the vacancy, company, and every promising person unless Telegram is unavailable in the environment.
   - Run other branches that match available evidence: vacancy title + company, Habr Career, LinkedIn, Google X-Ray, person name + company, company site, public posts.
   - Completion: every available branch has either produced candidate contacts or has an evidence-backed reason to stop.

3. Convert traces into contact candidates.
   - Capture name, role, company fit, source URL or source description, contact route, evidence quality, and confidence.
   - Label evidence quality as `verified page`, `public indexed snippet`, `cross-source match`, or `unverified lead`.
   - Prefer direct Telegram handles contact routes over generic email and weaker social DMs. Treat plain email as weak unless the user asks for email.
   - Completion: each candidate has a contact route or is explicitly marked as unresolved.

4. Verify relevance.
   - Check that recruiters hire for the user's specialty when evidence allows.
   - Check that hiring managers work in the relevant department, product, or sector.
   - Prefer current employees over former employees unless current contacts fail.
   - Downgrade blocked, login-only, stale, or snippet-only evidence unless another public source confirms it.
   - Completion: ranked candidates have a reason tied to the role, department, or hiring function.

5. Escalate if direct contacts fail.
   - Try adjacent recruiters, hiring managers, HR leadership, department leadership, agency/contract recruiters, public employees, and social-publication trails.
   - Completion: the report names the fallback path used, not just that no contact was found.

## Output

Return a concise investigator report:

```text
Best contacts
1. Name — role — contact route — confidence — evidence quality — why this person

Evidence checked
- Source/branch — result

Next actions
- Message priority order
- Any missing data that would materially improve the search
```

Never output raw unranked links without explaining why each matters.
