---
name: yistc-linear-research
description: Workflow for researching a Linear issue, gathering all relevant context, synthesizing key insights, and posting a structured summary back to the issue as a comment.
---

# Workflow for researching a Linear issue
## Linear MCP References
- Get Issue - get_issue (MCP)(id: "L-115")
- List Comments - list_comments (MCP)(issueId: "L-115")
- Create Comment: save_comment (MCP)(issueId: "L-115", body: "<comment body>")
- Update commentt: save_comment (MCP)(id: "<comment_id>", issueId: "L-115", body: "<comment body>")
- Delete comment: delete_comment (MCP)(id: "<comment_id>")

## Scope
Use this workflow when:
	•	an issue requires investigation, clarification, or context gathering
	•	the goal is to understand the problem deeply before implementation
	•	you are asked to research, analyze, or summarize an issue

Issue format example: L-114
## Goal
Produce a high-quality research summary by:
	1.	collecting all relevant context
	2.	analyzing and organizing the information
	3.	extracting key insights and open questions
	4.	posting a structured summary to the Linear issue

## Steps
### Step 1: Read and collect context
Before doing any analysis:
	•	Retrieve the issue:
	•	title
	•	description
	•	status
	•	Retrieve all comments
	•	Identify any:
	•	linked issues
	•	referenced PRs
	•	external context (docs, APIs, tools mentioned)

Goal: Build a complete picture of the issue from all available sources

### Step 2: Expand research (if needed)

If the issue is not self-contained:
	•	Search the codebase for:
	•	related modules
	•	relevant functions
	•	prior implementations
	•	Identify:
	•	similar past issues
	•	existing patterns or constraints

Do NOT modify code at this stage.

### Step 3: Analyze and synthesize

Process the collected information:
	•	Summarize the problem in your own words
	•	Identify:
	•	core objective
	•	constraints
	•	assumptions
	•	Extract:
	•	key technical points
	•	relevant system behavior
	•	Detect:
	•	inconsistencies or unclear areas
	•	missing information

### Step 4: Structure the research output

Organize findings into a clear structure.

The output must include:
- Problem Summary
- Key Context
- Findings
- Constraints and Assumptions
- Open Questions
- Suggested Direction (if applicable)

Rules:
	•	Keep it concise but complete
	•	Prefer bullet points over long paragraphs
	•	Avoid speculation unless clearly labeled

### Step 5: Post summary to Linear

Add a comment to the issue containing:
	•	the structured research summary
	•	no raw logs or unprocessed data
	•	clear formatting (markdown)

The comment should:
	•	help others quickly understand the issue
	•	serve as a shared reference for future work

## Failure or ambiguity handling

If information is incomplete:
	•	explicitly list unknowns under Open Questions
	•	do NOT invent missing details

If conflicting information exists:
	•	highlight the conflict
	•	do not resolve it silently

## Behavioral rules
	- Do NOT implement code in this workflow
	- Do NOT open PRs
	- Do NOT change issue status unless explicitly requested
	- Focus only on understanding and communication
	- If a research summary already exists: update or refine it instead of duplicating
