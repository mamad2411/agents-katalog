---
name: product-question-research
description: Research and answer Databricks product questions for customers. Use this skill when asked about feature support, capabilities, limitations, or whether something is supported. Triggers on "does [feature] support", "is [feature] supported", "can [feature] do", "do materialized views support", or any question about Databricks feature behavior, limitations, or capabilities. Searches public docs, Glean, and Slack to provide an answer with confidence rating.
user-invocable: true
---

# Product Question Research Skill

This skill researches Databricks product questions by systematically gathering information from multiple sources and creating a well-formatted Google Doc with the answer, confidence rating, and references.

## Critical Research Principles

**NEVER use WebFetch for Google Docs URLs.** Always use the google-docs skill:
```
/google-docs read <google_doc_url>
```

**Follow the research path.** When you discover a related feature, roadmap item, or gap-filling solution, research it thoroughly - don't just mention it exists.

**Cite everything.** Every claim should trace back to a source. High-weight sources must be cited inline in the answer.

## Quick Start

**Invoke the `product-question-researcher` agent** to handle the full research workflow:

```
Task tool with subagent_type='fe-workflows:product-question-researcher' and model='opus'
```

Pass the user's question directly to the agent. The agent will:
1. Parse the question and map the feature landscape (related features, dependencies)
2. Search public Databricks documentation
3. Search Glean for internal documentation
4. Identify relevant Slack channels and people
5. Search Slack for recent discussions
6. **Deep-dive on any roadmap/preview features** discovered (status, timeline, access, alternatives)
7. Validate the answer against the original question's specificity
8. Handle uncertainty explicitly (what we know vs. don't know)
9. Compile findings with confidence rating and inline citations
10. Create a formatted Google Doc with the answer

## Research Methodology

### Step 1: Understand and Map Dependencies

First, identify all related features that might affect the answer:
- **Direct feature** - What the question explicitly asks about
- **Upstream/downstream dependencies** - What this feature depends on or enables
- **Alternative approaches** - Other ways to achieve the same goal
- **Related formats/protocols** - Data formats, table types involved

**Example:** For "Does Lakeflow Connect support Iceberg sinks?":
- Direct: Lakeflow Connect
- Dependencies: Streaming Tables, Delta
- Related: UniForm, Managed Iceberg, Lakeflow Pipelines
- You MUST research enough of these to arrive at a precise answer

### Step 2: Determine Feature Status

Identify whether the question involves:
- **GA features** - Answer likely in public docs
- **Public Preview features** - Answer in public docs with preview caveats
- **Private Preview features** - Answer in internal docs, Slack, or preview guides
- **Unreleased/Roadmap features** - Answer requires PM/engineering confirmation

### Step 3: Check Public Documentation

Fetch the llms.txt index to find relevant public docs:

```
WebFetch https://docs.databricks.com/llms.txt
```

Then fetch relevant documentation pages for details.

### Step 4: Search Glean

Use Glean MCP to search internal knowledge:

```python
# Search for relevant docs
mcp__glean__glean_read_api_call(
    endpoint="search.query",
    params={"query": "<question keywords>", "page_size": 20}
)
```

Filter results by:
- **Recency** - Prioritize recently modified documents
- **Source type** - Internal docs, FAQs, preview guides
- **Relevance** - Direct answers vs tangential mentions

**Read Google Docs using the skill, NOT WebFetch:**
```
/google-docs read <google_doc_url>
```

### Step 5: Identify Slack Channels

From Glean results and domain knowledge, identify relevant channels:

| Topic | Channels |
|-------|----------|
| Materialized Views | #materialized-views, #sdp-enzyme |
| Iceberg/Delta | #iceberg-hudi, #swat-iceberg-hudi |
| DLT/Lakeflow | #lakeflow-pipelines, #dlt-users |
| Streaming | #streaming-help |
| Unity Catalog | #unity-catalog, #hms-federation |
| General Product | #product-roadmap-ama, #investech |

### Step 6: Search Slack

Use Slack MCP to search for recent discussions:

```python
mcp__slack__slack_read_api_call(
    endpoint="search.messages",
    params={"query": "<question keywords>", "count": 20}
)
```

**Weight recent messages higher** - Product information changes frequently.

### Step 7: Deep-Dive on Roadmap/Preview Features

**CRITICAL:** When you discover ANY future feature, roadmap item, or preview capability that might resolve the gap, you MUST research it thoroughly:

1. **Current status** - Private Preview, Public Preview, GA, or roadmap?
2. **Timeline** - Estimated GA date, target quarter/FY
3. **Naming/Evolution** - Is there a newer name? Has it been superseded?
4. **Customer access** (for previews) - How to onboard, feature flags, PM contact
5. **Current limitations** - What doesn't work yet?

**Don't just say "Feature X is in Private Preview" - get the details!**

### Step 8: Validate Answer Against Original Question

Before finalizing, check:
- Does my answer address the EXACT scenario asked?
- If the question had "or" options, did I address all of them?
- Did I explain WHY, not just yes/no?
- Can additional research give a more specific answer?

### Step 9: Handle Uncertainty Explicitly

When you can't get a fully specific answer, structure your disclosure:

1. **What we ARE confident about** - Facts with strong sources
2. **What we are LESS confident about** - Why uncertain, what would help
3. **What we could NOT determine** - Gaps, who to contact

### Step 10: Compile Answer with Confidence

Rate confidence on a 1-10 scale:

| Score | Meaning | Evidence Required |
|-------|---------|-------------------|
| 9-10 | Very High | Multiple authoritative sources agree |
| 7-8 | High | Public docs + internal confirmation |
| 5-6 | Medium | Single authoritative source |
| 3-4 | Low | Indirect evidence, old sources |
| 1-2 | Very Low | Speculation, no direct sources |

### Step 11: Create Google Doc

Use the google-docs skill to create a formatted document with:
- Proper heading styles (Title, H1, H2)
- Real bullet lists (not text bullet characters)
- Embedded hyperlinks for all references
- Sorted lists for channels and people
- **Inline citations for key facts**

## Output Document Structure

1. **Question** - The original question
2. **Answer** - Direct answer with reasoning and inline citations
   - Why Not? (if applicable) - Technical reasons
   - Workaround - If applicable
   - Future Roadmap - MUST include: status, timeline, how to access, alternatives
3. **What We Know vs Don't Know** - Uncertainty breakdown
   - High Confidence (with sources)
   - Lower Confidence (with reasons)
   - Could Not Determine (who to contact)
4. **Confidence Level** - Score (1-10) with justification
5. **Relevant Slack Channels** - Alphabetically sorted, with links
6. **Relevant People** - Alphabetically sorted, with titles
7. **References** - Primary, Secondary, Supporting sources

## Document Formatting Requirements

**CRITICAL:** The agent MUST follow these formatting rules to avoid double-bullets and plain text URLs:

| Element | Requirement | Common Mistake to Avoid |
|---------|-------------|-------------------------|
| Headings | Use Google Docs heading styles (TITLE, HEADING_1, HEADING_2) | Using text like "## Heading" instead of applying styles |
| Bullet lists | Insert PLAIN TEXT (no `-`, `•`, or `*`), then apply `createParagraphBullets` | Inserting `"- Item\n"` creates BOTH a Google Docs bullet AND a visible dash character |
| Links | Embed URLs in text using `updateTextStyle` with link field | Showing `"Title https://url"` instead of embedded hyperlink in "Title" |
| References | Format as `"Title"` with embedded hyperlink, NO visible URLs | Showing `"Title - https://url"` with plain text URL |
| Slack channels | Embed channel archive URL in channel name like `"#channel-name"` | Showing `"#channel-name - https://databricks.slack.com/..."` |
| Google Docs | Embed doc URL in document title | Showing `"Title - https://docs.google.com/..."` |
| Public docs | Embed docs.databricks.com URL in description | Showing `"Description - https://docs.databricks.com/..."` |
| People | Include ALL people mentioned in answer, with titles if known | Missing people from final list |
| Citations | Inline citations for key facts (e.g., "claim [Public Docs: page]") | No inline citations for key claims |

**Example of WRONG formatting (what we're fixing):**
```
References

Primary Sources

- Public Docs: Billable usage system table reference - https://docs.databricks.com/aws/en/admin/system-tables/billing
```
Problems: Double bullet (Google Docs bullet + dash character), visible plain text URL

**Example of CORRECT formatting:**
```
References

Primary Sources

Public Docs: Billable usage system table reference
```
With `createParagraphBullets` applied (no dash in text) and the entire text as a blue clickable hyperlink (no visible URL)

## Example Invocations

```
User: Does Lakeflow Connect support sinking data as Iceberg?
-> Agent maps dependencies (Lakeflow Connect, Streaming Tables, Delta, UniForm, Iceberg)
-> Researches each dependency to arrive at precise answer
-> Discovers "Compatibility Mode" / "Smart Clones" in preview
-> Deep-dives on preview: status, timeline, access, limitations
-> Validates answer addresses both Iceberg AND Delta+UniForm
-> Creates doc with answer, uncertainty breakdown, and inline citations

User: Do materialized views on foreign iceberg tables support incrementalization?
-> Agent researches MV + Iceberg + incremental refresh + CDF requirements
-> Creates doc with answer explaining technical constraints

User: What's the status of Auto CDF?
-> Agent determines feature status, finds preview docs
-> Researches timeline, how to access, limitations
-> Creates doc with full roadmap details
```

## Resources

- `fe-google-tools/skills/google-docs/resources/gdocs_builder.py` - Helper for creating properly formatted Google Docs (supports `add-bullets`, `add-link`, `add-links-by-text`)
- `agents/product-question-researcher.md` - Agent implementation details
