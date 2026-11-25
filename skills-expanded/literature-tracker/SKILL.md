---
name: literature-tracker
description: Tracks every paper, study, dataset, and source that has been shared, recommended, or discussed across research email threads — building a structured reading list with context on why each was surfaced and what action is expected. Use when a researcher wants to consolidate the literature and sources scattered across email without losing track of anything. Triggers on "papers shared in email", "literature from email", "what have people sent me to read", "research reading list", "track papers discussed", "consolidate research sources".
metadata:
  version: 1.0.0
---

# Literature Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans research email threads for every paper, preprint, dataset, report,
and external source that was shared, mentioned, or recommended — extracting
the title, source, who shared it, why it was flagged, and whether any
follow-up action was expected — and assembles a structured literature
tracking list.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the conference"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [topic_scope] — either "all" (default) or a specific research topic
     or project to focus on.
   - [topic_clause] — derived. When [topic_scope] is not "all", set to
     " related to [topic_scope]". When [topic_scope] is "all", set to
     empty string.

2. Call search with:
   - query: paper study preprint arxiv pubmed doi dataset report read
     relevant interesting found this published journal
     (if [topic_scope] is not "all", append the topic or project to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all research email threads from [time_range][topic_clause]. Find every paper, preprint, dataset, report, or external source that was shared, mentioned, or recommended. For each source extract: the title or description, the source or journal if mentioned, who shared it, when, why they flagged it as relevant, what research topic or project it relates to, and whether any follow-up action was expected such as reading, citing, replicating, or responding to.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Literature and source tracker assembled from research email threads",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this tracker was generated"
   },
   "sources": {
   "type": "array",
   "description": "List of every paper, dataset, or source found in research email threads",
   "items": {
   "type": "object",
   "description": "A single research source with context and action status",
   "additionalProperties": false,
   "properties": {
   "title_or_description": {
   "type": "string",
   "description": "Title of the paper or dataset, or a description if no title was given"
   },
   "source_type": {
   "type": "string",
   "description": "Type of research source",
   "enum": [
   "journal_paper", "preprint", "dataset", "technical_report",
   "thesis", "book_chapter", "conference_paper", "blog_or_commentary",
   "tool_or_software", "other"
   ]
   },
   "journal_or_venue": {
   "type": "string",
   "description": "Journal, conference, or repository where this was published, empty string if not mentioned"
   },
   "doi_or_url": {
   "type": "string",
   "description": "DOI, URL, or arxiv ID if mentioned in email, empty string if not provided"
   },
   "shared_by": {
   "type": "string",
   "description": "Name or role of the person who shared or mentioned this source"
   },
   "date_shared": {
   "type": "string",
   "description": "ISO8601 date this source was shared in email"
   },
   "relevance_reason": {
   "type": "string",
   "description": "Why this source was flagged as relevant based on the email context"
   },
   "related_project": {
   "type": "string",
   "description": "The research project or topic this source was shared in relation to"
   },
   "expected_action": {
   "type": "string",
   "description": "Any follow-up action expected based on the email context",
   "enum": [
   "read_and_review", "cite_in_work", "replicate_or_build_on",
   "share_with_team", "respond_with_feedback", "no_action", "unknown"
   ]
   },
   "action_completed": {
   "type": "boolean",
   "description": "Whether the expected action has been confirmed as completed in email"
   },
   "priority": {
   "type": "string",
   "description": "Priority of engaging with this source based on email signals",
   "enum": ["high", "medium", "low", "unknown"]
   }
   },
   "required": [
   "title_or_description", "source_type", "journal_or_venue",
   "doi_or_url", "shared_by", "date_shared", "relevance_reason",
   "related_project", "expected_action", "action_completed", "priority"
   ]
   }
   },
   "unactioned_count": {
   "type": "number",
   "description": "Number of sources with an expected action that has not been completed"
   },
   "high_priority_count": {
   "type": "number",
   "description": "Number of sources flagged as high priority"
   },
   "by_project": {
   "type": "array",
   "description": "Summary of sources grouped by research project or topic",
   "items": {
   "type": "object",
   "description": "Source count for a single research project or topic",
   "additionalProperties": false,
   "properties": {
   "project": {
   "type": "string",
   "description": "Name of the research project or topic"
   },
   "source_count": {
   "type": "number",
   "description": "Number of sources related to this project"
   },
   "unactioned_count": {
   "type": "number",
   "description": "Number of unactioned sources for this project"
   }
   },
   "required": ["project", "source_count", "unactioned_count"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of literature found and most important unactioned items"
   }
   },
   "required": [
   "as_of", "sources", "unactioned_count",
   "high_priority_count", "by_project", "summary"
   ]
   }
   }

4. Present high priority unactioned sources first, ordered by date shared
   descending. Group by project. Lead with unactioned count and high
   priority count.

5. Ask: "Would you like me to organize these into a formatted literature
   review list or export by project?"