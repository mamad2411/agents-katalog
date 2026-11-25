---
name: "blog-structures"
description: "Blog post structures: the anatomy of a technical post, structures per article type, writing voice, code example guidelines, and engagement metrics to target. Use when planning the shape of a technical post."
---

# Blog Structures

> Structural patterns and frameworks for different types of technical blog posts.

## Knowledge Base

### The Technical Blog Post Anatomy

Every technical blog post has these layers:

```
Hook          --> Why should I care? (2-3 sentences)
Context       --> What problem exists? (1-2 paragraphs)
Solution      --> How do we solve it? (bulk of the post)
Evidence      --> Does it work? (benchmarks, examples, results)
Takeaways     --> What did we learn? (3-5 bullet points)
Call to Action --> What should I do next? (1-2 sentences)
```

### Article Type Structures

**Tutorial Structure:**
```
1. What we are building (with screenshot/result preview)
2. Prerequisites
3. Setup
4. Step-by-step implementation
5. Testing/verification
6. Key takeaways
7. Next steps / further reading
```

**Deep Dive Structure:**
```
1. The question or concept we are exploring
2. Surface-level understanding (what most people know)
3. Going deeper (internals, mechanics, edge cases)
4. Practical implications (how this knowledge changes your code)
5. Key insights
```

**Case Study Structure:**
```
1. The context (what we were building, constraints)
2. The problem (specific metrics: latency, errors, cost)
3. What we tried (including things that did not work)
4. The solution (technical details)
5. Results (before/after metrics)
6. Lessons learned
```

**Comparison Structure:**
```
1. The decision (what are we choosing between?)
2. Evaluation criteria (what matters?)
3. Candidate A (strengths, weaknesses, code example)
4. Candidate B (strengths, weaknesses, code example)
5. Head-to-head comparison table
6. Recommendation by use case
```

**Announcement Structure:**
```
1. The headline feature (lead with impact)
2. Why we built it (user request, pain point)
3. How to use it (quick code example)
4. Other changes (secondary features, fixes)
5. Breaking changes and migration
6. What is next
```

### Writing Voice for Technical Blogs

| Do | Avoid |
|----|-------|
| "This approach reduces latency by 40%" | "This amazing approach dramatically improves performance" |
| "Here is a trade-off to consider" | "The only downside is..." |
| "We chose X because Y" | "X is the best choice" |
| "Let's look at the code" | "As you can see from the above" |
| Active voice | Passive voice |
| Second person ("you") | Third person ("the developer") |

### Code Example Guidelines

1. **Minimal**: Show only the code relevant to the point. Strip boilerplate.
2. **Commented**: Add comments for non-obvious lines, not for every line.
3. **Runnable**: A reader should be able to paste and run. Include imports.
4. **Progressive**: First show the simple version, then add complexity.
5. **Diffed**: When modifying code, use diff blocks to show changes:

````markdown
```diff
 const app = new Hono();
+const authMiddleware = bearerAuth({ token: process.env.API_KEY });

-app.get('/data', (c) => {
+app.get('/data', authMiddleware, (c) => {
   return c.json({ items: [] });
 });
```
````

### Engagement Metrics to Target

| Metric | Good | Great |
|--------|------|-------|
| Average read time | >3 min | >5 min |
| Scroll depth | >60% | >80% |
| Bounce rate | <60% | <40% |
| Social shares | >10 | >50 |
| Bookmark rate | >2% | >5% |

## Patterns

1. **Lead with Code**: Many developers read code blocks first, then prose. Put a compelling code example in the first 25% of the post.
2. **The Before/After**: Show the painful way first, then the elegant way. The contrast creates the "aha" moment.
3. **Numbered Takeaways**: End with 3-5 numbered takeaways. These are the most shared and bookmarked parts.
4. **Internal Links**: Link to your own related posts. This helps both SEO and keeps readers on your site.
5. **Updated Dates**: Show when the post was last updated. Developers distrust undated technical content.

## Anti-Patterns

1. **The Wall of Theory**: Paragraphs of explanation before any code. Show code early, explain after.
2. **The Disclaimer Paragraph**: "Before we begin, I should mention..." -- just begin.
3. **Clickbait Titles**: "You Won't Believe This TypeScript Trick." Developers lose trust immediately.
4. **No Working Code**: Pseudocode or abbreviated snippets that cannot actually run. Every example should work.
5. **One-Sided Comparisons**: Comparing X to Y where the author clearly prefers X and strawmans Y.
6. **The Eternal Post**: 5000+ words with no clear structure. Break it into a series or ruthlessly edit.

## References

- [Technical Blogging by Antonio Cangiano](https://pragprog.com/titles/actb2/)
- [Google's Technical Writing Courses](https://developers.google.com/tech-writing)
- [Write the Docs - Blog Posts](https://www.writethedocs.org/)
- [Dev.to Writing Guidelines](https://dev.to/p/editor_guide)
