# GEO Brand Mentions — AI Citation & Brand Presence
## Triggers: brand mentions, geo mentions, ai citations, brand cited, perplexity mentions, chatgpt mentions

## WHAT IT DOES
Tracks and improves brand mentions in AI-generated answers (ChatGPT, Perplexity, Gemini, Claude)

## AUDIT STEPS
1. Search brand in ChatGPT, Perplexity, Gemini — screenshot results
2. Search top competitor — compare mention frequency
3. Identify cited sources — Reddit, G2, Clutch, industry blogs
4. Build presence on those platforms
5. Create llms.txt at domain/llms.txt
6. Submit to AI directories: theresanaiforthat, futuretools, etc.

## QUICK TEST
```bash
# Test brand citation in Perplexity via API
curl "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -d '{"model":"sonar","messages":[{"role":"user","content":"what is [BRAND]?"}]}'
```
