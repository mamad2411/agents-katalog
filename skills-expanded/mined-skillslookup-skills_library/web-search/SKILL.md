# Web Search Skill

## Tool: `web_search`

**Description**: Searches the web for current events, facts, or data that is not part of the model's training knowledge.

### Parameter: `query`
The search query to perform. Use specific keywords for better results.

## When to use this skill
- When the user asks about a news event from the last 24 hours.
- When you need to verify a fact or statistic from a reputable website.
- When you need to find a person's current title, role, or contact info.

## Instructions
1.  **Be Specific**: Do not use vague search terms like "help me with AI." Instead, use "What is the latest release of Llama 3?"
2.  **Verify Sources**: Prefer links from well-known science, tech, or news organizations.
3.  **Summarize**: Do not just copy-paste the search results. Write a concise summary of the answer based on the top 3-5 results.
4.  **Cite**: Always provide the URL of the most relevant source at the end of your response.

## Examples
### User: "What happened in the OpenAI board meeting today?"
1.  **Agent**: *Loads Web Search Skill*
2.  **Action**: `web_search("OpenAI board meeting today news")`
3.  **Observation**: "OpenAI announced two new board members..."
4.  **Final Response**: "Today, OpenAI announced two new board members: [Name] and [Name]. [Source: openai.com]"

[**← Back to Agent Skills**](../README.md)
