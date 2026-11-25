---
name: product-questions
description: Answer questions about using or running Tines 3B, such as how to set something up, what a role or setting does, limits, pricing, or self-hosting. Use when the user asks how 3B itself works rather than for help with their own work.
license: Apache-2.0
compatibility: Tines 3B
---

# Product questions

Answer from the most specific source, in this order:

1. **Skills.** If another skill’s description covers the topic, load it and answer from it.
2. **This 3B instance.** For questions about the user’s own setup, such as their spaces, roles, connectors, or usage, check it with the read tools.
3. **Public docs.** When neither answers the question, search 3B’s public help center with `search_docs` using a few keywords, read the matching article with `get_doc`, answer from it, and link the article.

The public docs can lag the product. If they disagree with a skill or with what the instance shows, go with the skill or the instance, and say the article may be out of date. If no source covers the question, say so instead of guessing.
