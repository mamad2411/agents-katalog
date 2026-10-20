# /research — NotebookLM Deep Research → Claude Code Execution

## FLOW
1. Research phase (NotebookLM + multi-source)
2. Analysis phase (synthesis + ranking)
3. Execution phase (Claude Code acts on enriched context)

## INSTRUCTIONS

When the user says `/research [topic]`, execute this pipeline:

### Phase 1: Gather Sources
Run the research pipeline script:
```bash
python scripts/notebooklm-research.py --topic "$ARGUMENTS" --output .research/latest.json
```

If notebooklm-py is not installed or auth fails, fall back to multi-source web research:
```bash
# Manual fallback: use Exa, Tavily, or web search
curl -s "https://api.tavily.com/search" -X POST -H "Content-Type: application/json" \
  -d '{"api_key":"'$TAVILY_API_KEY'","query":"$ARGUMENTS","search_depth":"advanced","max_results":10,"include_answer":true,"include_raw_content":true}'
```

### Phase 2: Analyze Results
Read the research output:
```bash
cat .research/latest.json
```

Synthesize the research into actionable insights:
- What are the key findings?
- What are the best practices?
- What code patterns / architectures are recommended?
- What are the common mistakes to avoid?
- What libraries / tools are recommended?

### Phase 3: Execute
Based on the research, take action:
- If the topic is about improving an Aurion tool → apply the findings to the code
- If the topic is about a bug → research the root cause and fix it
- If the topic is about a feature → research best implementations and build it
- If the topic is about architecture → propose and implement changes

### Phase 4: Document
Save the research summary:
```bash
mkdir -p .research
# Write a summary markdown file
```

## EXAMPLE
User: `/research React 19 Server Components best practices for SaaS tools`

1. NotebookLM searches academic papers, documentation, blog posts
2. Finds: RSC patterns, data fetching strategies, caching, streaming
3. Synthesizes: "For SaaS tools like Aurion, use RSC for..."
4. Applies findings to relevant Aurion tool code
5. Saves research to `.research/react-19-rsc.md`

## RULES
- Always cite sources with URLs
- Prefer official documentation over blog posts
- Cross-reference at least 3 sources before drawing conclusions
- If research contradicts current Aurion implementation, flag it clearly
- Never apply changes without showing the research first
