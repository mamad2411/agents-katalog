---

name: hr-hiring
description: HR workflow for creating optimized Upwork job posts, saving them to Notion, and evaluating applicant files from Google Drive. Use this skill when the user wants to hire for a new role, post a job on Upwork, or evaluate candidates for a job.

---
This skill automates the HR process of creating job posts for Upwork, organizing them in Notion, and evaluating candidates based on files dropped into Google Drive.

## What This Skill Does

This skill HR workflow for creating optimized Upwork job posts, saving them to Notion, and evaluating applicant files from Google Drive. Use this skill when the user wants to hire for a new role, post a job on Upwork, or evaluate candidates for a job.

## Workflow Overview

The hiring process consists of two main phases:

**Phase 1: Job Creation & Setup**
1. Generate optimized job posts (Title, Short Form, Long Form) based on user requirements.
2. Create a new Notion database for the job post.
3. Create a new Google Drive folder named `Hiring / [Job Title]` for collecting applicant files.

**Phase 2: Candidate Evaluation**
1. Read all applicant files (resumes, portfolios, cover letters, website links, etc.) from the specific Google Drive folder.
2. Perform a deep-dive evaluation of all submitted materials against the job requirements.
3. Rank the candidates and send the top recommendations to the user via email.

---

## Phase 1: Job Creation & Setup

When the user provides details for a new job they want to hire for on Upwork, follow these steps:

### 1. Generate Job Posts

Create three versions of the job post based on the user's details:

- **Job Title**: Catchy and optimized for Upwork search.
- **Short Form**: A concise version for quick reading or social sharing.
- **Long Form**: A comprehensive, professional Upwork job description including responsibilities, requirements, and expectations.

*Note: The user will manually post this to Upwork.*

### 2. Save to Notion

Create a new Notion page for the job post using the `zapier` MCP server under the "Hiring Applicants" parent page.

**Implementation:**

Use `mcporter call zapier notion_create_page` with JSON arguments to create the page automatically.

Example:
```bash
mcporter call zapier notion_create_page \
  --args '{
    "instructions": "Create a Notion page under Hiring Applicants (ID: 32ec60d0-9b6a-81b8-9965-fad1a9fa8bc8) for job post: [Job Title]",
    "title": "HR Hiring - [Job Title] - [Date]",
    "content": "[Full job post content with Title, Short Form, Long Form, and metadata in markdown format]",
    "parent_page": "32ec60d0-9b6a-81b8-9965-fad1a9fa8bc8"
  }'
```

**Key Details:**
- Set `parent_page: "32ec60d0-9b6a-81b8-9965-fad1a9fa8bc8"` (the page ID for "Hiring Applicants") to organize all job posts under the dedicated parent page
- Always use the page ID, not the page title, to ensure Zapier MCP creates the page in the correct location
- Format `content` as markdown with proper headings and structure
- Include all three job post versions (Title, Short Form, Long Form)
- Add metadata: Status (Draft), Date Posted, Applicant Count (0), Google Drive Folder link

**Parent Page:**
- **Title:** Hiring Applicants
- **Page ID:** `32ec60d0-9b6a-81b8-9965-fad1a9fa8bc8`
- **URL:** https://www.notion.so/Hiring-Applicants-32ec60d09b6a81b89965fad1a9fa8bc8

**Content Structure:**
```markdown
# [Job Title]

**Job Title:** [Optimized Title]

## Short Form
[Concise version]

## Long Form
[Full Upwork description with About Us, The Role, Responsibilities, Requirements, Nice to Have, What We Offer, How to Apply]

## Applicant Tracking
- **Google Drive Folder:** [link]
- **Status:** Draft
- **Date Posted:** Not yet posted
- **Applicant Count:** 0
```

### 3. Setup Google Drive Folder

**IMPORTANT:** The `gog` CLI is NOT installed on this box. There are two options:

**Option A — Google Workspace Python skill (preferred, if OAuth is configured):**
Check auth status first:
```bash
python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```
If `AUTHENTICATED`, use the Python API to create Drive folders. The google-workspace skill uses the Python `google-api-python-client` library with OAuth2. Google Drive folder creation must be done via a custom Python script using the Drive API v3 `files.create` method — the current `google_api.py` wrapper does NOT include a `drive mkdir` command. If Drive folder creation is needed, write a quick Python script using the existing OAuth token.

**Option B — No Google Drive available:**
If OAuth is NOT configured, inform the user you cannot create the Drive folder automatically. Instead:
- Save the job post locally to `~/.hermes/estimates/job-post-[title-slug].md`
- Present the job post in chat for the user to copy
- Offer to help them set up Google Drive OAuth for future automation (4-step process via the google-workspace skill)

---

## Phase 2: Candidate Evaluation

When the user indicates that applicants have submitted their files and they are ready for evaluation:

### 1. Retrieve Applicant Files

**IMPORTANT:** The `gog` CLI is NOT installed. Use the Google Workspace Python skill instead.

Check auth status first:
```bash
python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
```
If `AUTHENTICATED`, use the Python API wrapper:
```bash
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py drive search "folder-name" --max 10
```

If Drive files need to be downloaded, write a custom Python script using the `google-api-python-client` with the existing OAuth token at `~/.hermes/google_token.json`. The current `google_api.py` wrapper supports `drive search` but not `drive download` — write a quick script if needed.

If OAuth is NOT configured, inform the user that candidate evaluation requires access to the Google Drive folder. They'll need to either share files directly in chat or set up OAuth.

### 2. Deep-Dive Evaluation & Ranking

Perform a comprehensive analysis of each candidate's entire submission package against the original job requirements.

- Evaluate not just their resume, but the quality of their portfolio, past work, and any websites they provided.
- Identify the top candidates based on a holistic view of their skills and proof of work.
- Create a structured summary highlighting their strengths, weaknesses, portfolio quality, and why they are a good fit for the specific role.

### 3. Email the Results

Use the `gmail` MCP server to send the final rankings and evaluation summary to the user via email.

- Format the email professionally with clear rankings and bullet points for each top candidate.

**IMPORTANT:** The `gog` CLI is NOT installed. Use the Google Workspace Python skill:
```bash
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail get --help
```
Or send via the user's connected messaging platform (e.g., Telegram) as an alternative.

---

## Tools & Dependencies

- **MCP Server: notion** - For saving job posts to Notion databases.
- **CLI Tool: gog** - For Google Drive folder creation, file listing, and Gmail sending.
- **OpenClaw Tool: browser** - For analyzing candidate portfolio websites.
- **OpenClaw Tool: read** - For reading downloaded resumes and cover letters.
- **OpenClaw Tool: pdf** - For analyzing PDF resumes.

---

## Example Usage

**Phase 1 Example:**
> "I need to hire a full-stack developer. Create a job post for Upwork."

**Phase 2 Example:**
> "I have 10 applicants in the Google Drive folder. Evaluate them and send me the top 3."
