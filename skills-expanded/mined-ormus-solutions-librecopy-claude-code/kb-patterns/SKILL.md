---
name: "kb-patterns"
description: "Knowledge base patterns: article title patterns, taxonomy design, article lifecycle, search performance analysis, article structure, feedback and metrics, and anti-patterns. Use when designing or maintaining a help center or internal wiki."
---

# Knowledge Base Patterns

## Article Title Patterns

The title is the single most important field for findability. Users search with the same words they would type in a title.

```
# Good: question format
How do I cancel my subscription?
How do I export my data to CSV?
What's the difference between API keys and OAuth tokens?

# Good: task format
Cancel your subscription
Export data to CSV
Reset two-factor authentication

# Bad: topic format (too vague, no search intent)
Subscription management
Data export
Authentication settings
```

**Test**: would a user type this exact phrase in a search box? If not, rewrite the title.

## Taxonomy Design

### Controlled vocabulary vs freeform tags
- **Controlled vocabulary** (recommended): Fixed list of tags, requires approval to add new ones. Prevents tag proliferation ("authentication", "auth", "login" all meaning the same thing).
- **Freeform tags**: Flexible but degrades over time. Three articles tagged "authentication", two tagged "auth", one tagged "login". Search by tag returns incomplete results.

### Category depth
```
# Too deep: users cannot navigate more than 2-3 levels
Account → Security → Authentication → Two-Factor → SMS → Enable

# Good: flat and clear
Account & Security
  └── Two-factor authentication
       ├── Enable two-factor authentication
       ├── Disable two-factor authentication
       └── Troubleshoot two-factor authentication
```

## Article Lifecycle Management

```
new ticket → support logs it → KB gap identified
     ↓
writer drafts article
     ↓
SME review (accuracy) + editor review (clarity)
     ↓
publish
     ↓
schedule review: [feature change] or [6 months], whichever comes first
     ↓
review: is it still accurate? still relevant? search data shows it being found?
     ↓
update or archive
```

### Archiving vs deleting
- **Archive** (preferred): Article is no longer accurate but has inbound links. Add a banner: "This article is outdated. See [updated article]." Keep URL for redirect.
- **Delete**: Article is redundant (merged into another) or never published. Set up redirect first.

## Search Performance Patterns

### Analyzing failed searches
Zero-result searches reveal content gaps directly:

```
Search term with no results → content gap analysis:
  "how to delete account" → Do we have a deletion guide?
  "export pdf" → Do we document PDF export?
  "saml sso" → Do we have SSO documentation?
  "billing api" → Do we have API docs for billing?
```

### Common causes of low search success rate
1. Article titles don't match how users phrase questions (jargon vs plain language)
2. Key terms only appear deep in the article, not in title or summary
3. Missing synonym handling (users type "invoice", article says "receipt")
4. Content exists but in the wrong category (users search billing, content is in account settings)

### Title SEO for internal search
Most KB search engines weight the title heavily. Keyword-first title outperforms generic title:

```
# Keyword at the end (lower weight)
"Two-factor authentication: how to enable it"

# Keyword at the start (higher weight)
"Enable two-factor authentication"

# Question form (matches natural search queries)
"How do I enable two-factor authentication?"
```

## Article Structure Patterns

### The summary is the most-read section
Users scan the summary to determine if the article answers their question before reading it. The summary should:
- State what the article covers in one sentence
- Include 2-3 key search terms naturally
- Be under 150 words

### Steps vs prose
Use numbered steps for procedures. Never write procedures as paragraphs:

```
# Bad: procedure in prose form
To reset your password, first go to the login page and click "Forgot password".
Then enter your email address and click Submit. You'll receive an email within a
few minutes with a reset link. Click the link and enter a new password.

# Good: numbered steps
1. Go to the login page and click **Forgot password**.
2. Enter your email address and click **Submit**.
3. Check your email for a reset link (arrives within 5 minutes).
4. Click the link and enter your new password.
```

### Troubleshooting section placement
Put troubleshooting at the end of every procedural article, not in a separate article. Users who hit problems are already on the article - they should not have to navigate away.

## Feedback and Metrics

### Minimum viable feedback
Every article needs a yes/no feedback widget. Articles with consistent "No" votes need review.

### Deflection measurement
```
KB deflection = 1 - (support tickets / KB article views)
# A deflection rate of 0.05 means 5% of KB readers still opened a ticket
# Target: < 5% for well-written articles on solvable problems
```

### Zero-results monitoring
Check zero-results queries weekly. Each zero-results query is a potential article to write.

## Anti-Patterns

### Organizing by team, not user
```
# Bad: reflects internal org chart
Support Team Docs
Engineering FAQs
Product Updates

# Good: reflects user goal
Getting Started
Using [Feature]
Billing & Account
API Reference
```

### Answers embedded in FAQ instead of articles
FAQ pages grow without limit and become unsearchable. Each FAQ item that gets repeated traffic deserves its own article with a descriptive title. FAQ should contain only 10-15 items; redirect surplus to proper articles.

### No review cadence
Articles published without a review date go stale silently. The KB becomes a source of misinformation. Add a `last_reviewed` field to every article template and create a scheduled task to review articles older than 6 months.

### Missing related articles
Articles in isolation. Users who finish reading have no path forward. Every article should link to 2-3 related articles (next logical step, alternative approach, deeper dive).

## References
- [Zendesk KB Best Practices](https://support.zendesk.com/hc/en-us/articles/4408886186010)
- [Confluence Best Practices](https://www.atlassian.com/software/confluence/guides)
- [Every Page Is Page One (Mark Baker)](https://everypageispageone.com/)
- [The Web Content Style Guide (Gerry McGovern)](https://nngroupk.com/articles/)
