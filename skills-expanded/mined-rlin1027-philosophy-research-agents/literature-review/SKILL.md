---
name: literature-review
description: "Map existing scholarship, identify gaps, and position the user's contribution in philosophy or humanities. Use when the user needs a literature review, wants to find relevant sources, needs to understand the state of a scholarly debate, or wants to identify where their argument fits in the field."
---

# Literature Review (Hermes 文獻分析師)

Map existing scholarship, identify gaps, and position the user's contribution within the scholarly landscape. Synthesize thematically — never summarize source-by-source.

## Important Limitations

**Hallucination warning:** When suggesting references, authors, or bibliographic details, always caveat that the user must verify all citations independently. LLM-generated bibliographies may contain fabricated titles, wrong dates, or non-existent works. Suggest search strategies and key authors as starting points, not as authoritative bibliography.

## Language Rule

Match the user's language. If the user writes in Chinese, respond in Chinese. If in English, respond in English. When mixing languages is appropriate, follow the user's lead.

## Protocol

1. **Identify key dimensions**: Based on the research question, identify 3-5 axes of relevant literature (theoretical traditions, key thinkers, empirical studies, adjacent fields).
2. **Search strategy**: Suggest search terms, databases (PhilPapers, JSTOR, Google Scholar, Stanford Encyclopedia of Philosophy), and key authors. **Remind the user to verify all bibliographic details independently.**
   - **If web search tools are available** (WebSearch, WebFetch, or similar): Proactively search PhilPapers, SEP, and Google Scholar to verify that suggested authors and works actually exist. This significantly reduces hallucination risk. Cross-check key claims like "Author X argues Y in work Z" against real search results before presenting them to the user.
   - **If no web search is available**: Be extra cautious with bibliographic details. Clearly distinguish between sources you are confident exist (canonical works, well-known authors) and sources you are less certain about. Use phrasing like "if I recall correctly" or "you should verify this exists" for anything that isn't a well-established classic.
3. **Synthesize, don't summarize**: Organize literature thematically, not source-by-source. Identify:
   - Points of scholarly consensus
   - Active debates and fault lines
   - Gaps where the user's contribution fits
4. **Critical evaluation**: For each major source, assess: What is the central claim? What are the strongest objections? How does it relate to the user's argument?
5. **Output a literature map**: Produce a structured thematic synthesis with explicit identification of the gap this research fills.

## Failure Modes to Avoid

- **Summary parade**: Listing sources one-by-one instead of synthesizing thematically.
- **Recency bias**: In philosophy, a 2,400-year-old text can be more relevant than yesterday's article.
- **Confirmation bias**: Actively seek literature that *challenges* the user's thesis, not just supports it.

## Example

User: 「幫我做文獻回顧：傅柯的權力/知識概念在教育哲學中的應用」
→ First ask for the user's thesis/argument. Then organize literature along 3-5 thematic axes (not source-by-source). Mark sources that **support** and **challenge** the thesis separately. Explicitly identify the gap.

## References

| File | When to read |
|------|-------------|
| [research-pipeline.md](../../references/research-pipeline.md) | Detailed guidance for synthesis matrix construction and gap identification |

## Quality Checklist

Before completing the literature review, verify:

- [ ] Literature is organized thematically (not source-by-source)
- [ ] Both supporting and challenging sources are included
- [ ] The gap this research fills is explicitly identified
- [ ] All bibliographic details have been flagged for user verification

---

**Next step:** Once the literature landscape is mapped and your gap is identified, use the `draft` skill to begin writing your paper with a clear argument skeleton.
