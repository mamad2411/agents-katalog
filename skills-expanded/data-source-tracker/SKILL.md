---
name: data-source-tracker
description: Tracks every data access request, dataset agreement, data sharing arrangement, and data source dependency referenced in research email threads — what has been requested, what has been approved, what is still pending, and what data access could be blocking research progress. Use when a researcher wants to know the status of all their data access requests and agreements. Triggers on "data access requests", "dataset agreements", "data sharing status", "what data are we waiting for", "data access tracker", "research data pipeline".
metadata:
  version: 1.0.0
---

# Data Source Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans research email threads for every data access request, data sharing
agreement, DUA negotiation, API access request, and dataset dependency —
tracking approval status, access granted or pending, any conditions attached,
and whether blocked data access is holding up research progress.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since the project started"). Default: the last 12 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific project
     or dataset type to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: data access dataset agreement DUA data sharing request API
     repository access credentials approved pending data request
     (if [scope] is not "all", append the project or dataset type to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all research email threads from [time_range][scope_clause] related to data sources, datasets, and data access. For each data source or access request identify: the dataset or source name, the provider or custodian, what type of access was requested, whether a data use agreement or formal request was required, the current approval status, any conditions or restrictions attached to the access, and whether pending data access is blocking any research progress.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Research data source and access tracker from email threads",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "data_sources": {
   "type": "array",
   "description": "List of every data source or access request found in research email",
   "items": {
   "type": "object",
   "description": "A single data source or access request with full tracking",
   "additionalProperties": false,
   "properties": {
   "dataset_name": {
   "type": "string",
   "description": "Name or description of the dataset or data source"
   },
   "provider": {
   "type": "string",
   "description": "Name of the data provider, repository, or custodian"
   },
   "data_type": {
   "type": "string",
   "description": "Category of data source",
   "enum": [
   "clinical_data", "survey_data", "administrative_data",
   "genomic_data", "imaging_data", "environmental_data",
   "social_media_data", "api_feed", "proprietary_dataset",
   "public_repository", "partner_data", "other"
   ]
   },
   "access_type_requested": {
   "type": "string",
   "description": "What level or type of access was requested",
   "enum": [
   "full_download", "query_access", "api_access", "secure_enclave",
   "data_sharing_agreement", "linkage_request", "other"
   ]
   },
   "dua_required": {
   "type": "boolean",
   "description": "Whether a data use agreement or formal contract was required"
   },
   "request_date": {
   "type": "string",
   "description": "ISO8601 date the access request was initiated, empty string if unknown"
   },
   "access_status": {
   "type": "string",
   "description": "Current status of this data access request",
   "enum": [
   "access_granted", "pending_approval", "dua_in_negotiation",
   "awaiting_irb", "conditionally_approved", "denied",
   "access_expired", "not_yet_requested", "unknown"
   ]
   },
   "days_pending": {
   "type": "number",
   "description": "Number of days this request has been pending, 0 if already resolved"
   },
   "conditions_or_restrictions": {
   "type": "string",
   "description": "Any conditions, use restrictions, or obligations attached to access, empty string if none"
   },
   "blocking_research": {
   "type": "boolean",
   "description": "Whether pending access to this data source is blocking research progress"
   },
   "related_project": {
   "type": "string",
   "description": "Research project this data source relates to"
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended next step to progress or resolve this data access request"
   }
   },
   "required": [
   "dataset_name", "provider", "data_type", "access_type_requested",
   "dua_required", "request_date", "access_status", "days_pending",
   "conditions_or_restrictions", "blocking_research",
   "related_project", "recommended_action"
   ]
   }
   },
   "blocking_count": {
   "type": "number",
   "description": "Number of data access requests whose pending status is blocking research"
   },
   "pending_count": {
   "type": "number",
   "description": "Total number of data access requests still awaiting resolution"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of data access pipeline and most critical blockers"
   }
   },
   "required": [
   "as_of", "data_sources", "blocking_count", "pending_count", "summary"
   ]
   }
   }

4. Present blocking requests first, then pending requests ordered by
   days_pending descending. Lead with blocking count and pending count.

5. Ask: "Would you like me to draft a follow-up email to any data providers
   or custodians with outstanding requests?"