---
name: discovery-engine
description: |
  Find relevant people for outreach using Exa AI search capabilities.
  Supports LinkedIn search, company research, and cross-platform profile discovery.
  Use this skill when the user wants to find people based on topics, roles, companies, or industries.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Discovery Engine Skill

Finds relevant people for outreach using Exa AI integration.

## When to Use This Skill

Use this skill when the user:
- Wants to find people to reach out to based on criteria
- Searches for people by role, company, industry, or location
- Needs to research companies before outreach
- Wants to build a target list for campaigns

## When NOT to Use This Skill

Do NOT use this skill for:
- Sending messages → use `workflow-engine` or platform-specific skills
- Managing team → use `team-manager`
- Reading emails → use `inbox-reader`

## Capabilities

1. **People Search** - Find people using Exa AI LinkedIn search
2. **Company Research** - Research companies for targeting
3. **Profile Enrichment** - Cross-reference to find Twitter/Instagram
4. **Target Management** - Store and organize discovered people
5. **Export** - Export to JSON/CSV for campaigns

## MCP Selection Guidelines

**CRITICAL:** Select the correct MCP based on query requirements.

### When to Use Exa MCP (`exa-mcp-server`)

Use for **quick searches** and **exploration**:

| Scenario | Example |
|----------|---------|
| Quick lookup | "Find 5 marketers at Google" |
| Company info | "What does Acme Corp do?" |
| Small result set | < 10 prospects needed |
| Exploratory search | "Who are the AI startup founders?" |

**Exa Tools:**
- `linkedin_search_exa` - Quick LinkedIn search
- `company_research_exa` - Company information
- `web_search_exa` - General web search

**Characteristics:**
- Fast response (seconds)
- Good for initial discovery
- Limited depth

### When to Use Websets MCP (`websets-mcp-server`)

Use for **deep research** and **exhaustive prospect lists**:

| Scenario | Example |
|----------|---------|
| Large prospect list | "Find 50 LinkedIn marketers" |
| B2B lead generation | "Build outreach list for AI startups" |
| Enriched data needed | "Find verified emails for founders" |
| Campaign-ready leads | "Prospect list for Series B CTOs" |

**Websets Tools:**
- Exhaustive LinkedIn searches
- AI-powered data enrichment
- Verified contact information
- Bulk prospect discovery

**Characteristics:**
- Thorough, complete results
- Takes longer but more comprehensive
- Best for outreach campaigns

### Auto-Selection Logic

```python
def select_mcp(query: str, result_count: int) -> str:
    websets_keywords = ['prospects', 'leads', 'outreach', 'campaign',
                        'enriched', 'verified', 'comprehensive', 'list of']

    # Use Websets for large counts
    if result_count >= 10:
        return 'websets'

    # Use Websets for prospect-related keywords
    if any(kw in query.lower() for kw in websets_keywords):
        return 'websets'

    # Default to Exa for quick searches
    return 'exa'
```

### MCP Configuration

Ensure MCPs are configured in `.claude/.mcp.json`:
```json
{
  "exa": { "command": "npx", "args": ["-y", "exa-mcp-server"] },
  "websets": { "command": "npx", "args": ["-y", "websets-mcp-server"] }
}
```

## Discovery Workflow

### 1. Create Discovery Session

Before searching, create a session to track results:

```bash
python .claude/scripts/discovery_engine.py session --query "AI startup founders San Francisco" --source linkedin_search
```

### 2. Perform Exa AI Search

Use Exa AI MCP to search (this happens through Claude's MCP integration):

**Example prompt to Exa:**
"Search LinkedIn for AI startup founders in San Francisco who have raised Series A funding"

### 3. Process and Store Results

After receiving Exa results, add people to the session:

```python
# The discovery_engine.py processes Exa responses
# Results are stored in output/discovery/people.json
```

### 4. View Discovered People

```bash
python .claude/scripts/discovery_engine.py list --has-linkedin
```

### 5. Export for Campaign

```bash
python .claude/scripts/discovery_engine.py export --format csv --output output/discovery/targets.csv
```

## Commands Reference

### View Discovery Stats

```bash
python .claude/scripts/discovery_engine.py stats
```

### List Discovered People

```bash
# All people
python .claude/scripts/discovery_engine.py list

# Filter by criteria
python .claude/scripts/discovery_engine.py list --query "founder" --has-linkedin --status not_contacted
```

### Get Person Details

```bash
python .claude/scripts/discovery_engine.py get --id PERSON_ID
```

### Update Outreach Status

```bash
python .claude/scripts/discovery_engine.py status --id PERSON_ID --status contacted --notes "Sent LinkedIn connection"
```

### Export People

```bash
# JSON export
python .claude/scripts/discovery_engine.py export --format json --output output/targets.json

# CSV export
python .claude/scripts/discovery_engine.py export --format csv --output output/targets.csv
```

## Example Discovery Workflow

**User:** "Find 10 DevOps engineers at Series B startups in Austin"

**Assistant Workflow:**

1. **Use TodoWrite to track:**
   ```json
   [
     {"content": "Create discovery session", "status": "in_progress"},
     {"content": "Search using Exa AI", "status": "pending"},
     {"content": "Process and store results", "status": "pending"},
     {"content": "Show discovered people", "status": "pending"}
   ]
   ```

2. **Create session:**
   ```bash
   python .claude/scripts/discovery_engine.py session --query "DevOps engineers Series B startups Austin" --source linkedin_search
   ```

3. **Search with Exa AI:**
   Use WebSearch or Exa MCP:
   "Search LinkedIn for DevOps engineers at Series B funded startups in Austin, Texas"

4. **Process results:**
   Parse Exa response and add people to discovery session.

5. **Show summary:**
   ```
   Found 10 DevOps engineers:

   1. John Smith - Senior DevOps at TechCo
      LinkedIn: linkedin.com/in/johnsmith
      Twitter: @john_devops

   2. Jane Doe - Platform Engineer at StartupX
      LinkedIn: linkedin.com/in/janedoe
      ...
   ```

6. **Ask user:**
   "Would you like to add these 10 people to a workflow for outreach?"

## Data Storage

Discovery data is stored in:
- `output/discovery/sessions.json` - Search sessions
- `output/discovery/people.json` - All discovered people

## Search Best Practices

1. **Be Specific:** "AI startup founders Series A San Francisco" > "startup founders"
2. **Include Location:** Helps narrow results
3. **Add Context:** Role + Industry + Company stage
4. **Use Tags:** Tag people for easy filtering later

## Enrichment

After initial discovery, you can enrich profiles:

1. **Find Twitter:** Search web for "[Name] [Company] twitter"
2. **Find Email:** Look for public email on LinkedIn or company site
3. **Company Research:** Use `company_research_exa` for company context

The discovery engine automatically deduplicates and merges enriched data.
