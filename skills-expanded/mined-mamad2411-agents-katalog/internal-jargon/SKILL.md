---
name: internal-jargon
description: Look up Databricks internal jargon, acronyms, and terminology from the company glossary. Context-efficient - only fetches specific terms when needed.
---

# Internal Jargon Lookup

This skill provides access to Databricks internal jargon, acronyms, and terminology from the company glossary. Use this skill when you encounter unfamiliar terms, especially in Salesforce records, Logfood data, or internal documentation.

## When to Use This Skill

Use this skill when you encounter:
- Unknown acronyms (e.g., DNB, FSI, EDNB)
- Internal terminology you're unsure about
- Terms in Salesforce Use Cases, accounts, or opportunities
- Jargon in Logfood analytics queries or results
- Industry or product-specific terminology

**DO NOT** load this skill proactively. Only invoke it when you actually encounter an unknown term that you need to look up.

## How This Skill Works

The Databricks Glossary/Jargon is maintained at: https://databricks.atlassian.net/wiki/spaces/UN/pages/8749065/Glossary+Jargon (go/glossary, go/jargon)

The page contains hundreds of terms organized alphabetically. To keep context usage low, this skill searches for specific terms on-demand rather than loading the entire glossary.

### Data Sources (in priority order)

1. **Confluence MCP** (preferred): Fetches the latest content from the live glossary page
2. **Local copy** (fallback): `resources/GLOSSARY.txt` - Used when Confluence MCP is unavailable or user lacks access

The local copy is a snapshot of the glossary and may become stale over time. Always try Confluence first for the most up-to-date definitions.

## Lookup Process

**IMPORTANT**: ONLY use Confluence MCP to fetch Confluence pages. DO NOT use WebFetch or any other tool for Confluence URLs. If Confluence MCP is not available, use the local copy instead.

When you need to look up a term, follow this fallback strategy:

### Option 1: Confluence MCP (Preferred - Most Up-to-Date)

1. **Try to load the Confluence MCP tool**:
   ```
   Use ToolSearch to load: mcp__confluence__get_confluence_page_content
   ```

2. **If Confluence MCP is available**, fetch the glossary page using ONLY the MCP:
   ```
   Call mcp__confluence__get_confluence_page_content with:
   - page_id: "8749065"
   - is_full: true
   - write_to_file: true
   ```

3. **Search for the term** in the returned file using grep:
   ```bash
   grep -i "<TERM>" <file_path>
   ```

### Option 2: Local Copy (Fallback - May Be Stale)

If Confluence MCP tools are not available or fail:

1. **Use the local glossary copy**:
   ```bash
   # Get the skill base directory
   SKILL_DIR="${CLAUDE_PLUGIN_ROOT:-~/.claude/plugins}/fe-internal-tools/skills/internal-jargon"

   # Search the local glossary
   grep -i "<TERM>" "$SKILL_DIR/resources/GLOSSARY.txt"
   ```

2. **Note the limitations**: Inform the user that this is a local copy and may be outdated. The Confluence page is the source of truth.

### Searching Tips

For multi-word searches or more context, use grep with context lines:
```bash
grep -i -A 2 "<TERM>" <file_path>
```

For multiple terms, search once and grep multiple times to avoid redundant fetches.

## Examples

### Example 1: Looking up DNB (with Confluence)
```
User context: "This account is classified as DNB in Salesforce"

1. Load Confluence MCP tool (ToolSearch)
2. Fetch page 8749065 with write_to_file=true
3. grep -i "DNB" <file_path>
4. Found: DNB - Digital Native Businesses
5. Use this definition in your response
```

### Example 2: Looking up FSI (with local fallback)
```
User asks: "What does FSI mean in this opportunity?"

1. Try to load Confluence MCP - not available
2. Fall back to local copy:
   grep -i "FSI" ~/.claude/plugins/fe-internal-tools/skills/internal-jargon/resources/GLOSSARY.txt
3. Found: FSI - Financial Services Industry
4. Respond: "FSI stands for Financial Services Industry (from local glossary copy)"
```

### Example 3: Multiple acronyms
```
Encounter unknown terms: "This U6 account is in FSI and DNB segments"

1. Fetch glossary once
2. grep for each term:
   - grep -i "U6" <file_path>
   - grep -i "FSI" <file_path>
   - grep -i "DNB" <file_path>
3. Return all definitions
```

## Integration with Other Skills

Skills that commonly need jargon lookup:
- **salesforce-actions**: When reading Use Cases, accounts, or opportunities with unfamiliar terminology
- **logfood-querier**: When query results contain internal acronyms or industry terms
- **uco-consumption-analysis**: When analyzing Use Case Objects with industry segment classifications

These skills should invoke `/internal-jargon` when they encounter unfamiliar terms rather than guessing or asking the user.

## Performance Notes

- The glossary page is ~3700 lines, so always use `write_to_file=true`
- The Confluence MCP caches responses for 15 minutes
- Use grep efficiently - search for specific terms rather than reading the entire file
- If looking up multiple terms, fetch the page once and grep multiple times

## Alternative Sources

If you cannot find a term in the glossary, consider:
1. **Glean Chat**: https://databricks.glean.com/chat - may have more context
2. **Ask the user**: They may know the term's meaning in their specific context
3. **Context clues**: Sometimes the surrounding text makes the meaning clear

## Common Terms Quick Reference

Here are some frequently encountered acronyms (but always verify with the glossary for accuracy):
- **DNB**: Digital Native Businesses
- **FSI**: Financial Services Industry
- **U1-U6**: Use Case stages (progression from opportunity to production)
- **EDNB**: Enterprise Digital Native Businesses
- **PubSec**: Public Sector
- **AMER**: Americas (region)
- **EMEA**: Europe, Middle East, and Africa
- **APJ**: Asia Pacific and Japan

**Note**: This quick reference is for common terms only. Always fetch the current definition from the glossary for accuracy, as terms and definitions may change.

## Maintaining the Local Copy

The local glossary copy at `resources/GLOSSARY.txt` should be updated periodically to stay current.

**Last Updated**: 2026-01-26 (Confluence page version 806)

**To update the local copy**:
1. Fetch the latest content from Confluence using the MCP
2. Save to `resources/GLOSSARY.txt`
3. Update the "Last Updated" timestamp above
4. Commit the changes

**Update frequency recommendation**: Quarterly, or when major terminology changes are announced.
