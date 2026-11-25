---
name: ai-driven-content-taxonomy-and-tagging
description: "Automatically categorize and tag content using AI-powered taxonomy to improve discoverability. Use when the user needs content organization, SEO optimization, or multi-platform content management."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","CONTENT_TAXONOMY_CONFIG"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🏷️"}}
---

## Overview

**AI-Driven Content Taxonomy and Tagging** automatically analyzes and categorizes your content using advanced machine learning models. This skill transforms unorganized content into a discoverable, searchable knowledge base by applying intelligent taxonomies, hierarchical tags, and semantic metadata—all without manual effort.

### Why This Matters
- **Content Discoverability**: Improve search rankings and user navigation across WordPress, Contentful, and Shopify
- **SEO Optimization**: Auto-generate schema markup, meta tags, and structured data
- **Multi-Channel Publishing**: Maintain consistent taxonomy across Slack, email, web, and social platforms
- **Time Savings**: Eliminate manual tagging workflows that consume 20+ hours/month
- **Content Intelligence**: Discover content gaps, trending topics, and audience intent patterns

### Supported Integrations
- **CMS**: WordPress, Ghost, Contentful, Strapi, Webflow
- **Communication**: Slack, Microsoft Teams, Discord
- **Databases**: MongoDB, PostgreSQL, Airtable
- **Search**: Elasticsearch, Algolia, Meilisearch
- **Cloud Storage**: Google Drive, Dropbox, AWS S3
- **Analytics**: Google Analytics 4, Mixpanel, Segment

---

## Quick Start

### Example 1: Tag a Blog Post Automatically
```
Analyze this blog post and apply a comprehensive taxonomy:

Title: "How to Build a Sustainable E-commerce Business in 2024"
Content: [paste article body]

Use these taxonomy categories:
- Industry: [e-commerce, sustainability, business]
- Format: [guide, tutorial, best-practices]
- Audience: [entrepreneurs, business-owners, startups]
- Topics: [auto-detect from content]
- Reading Level: [intermediate, advanced]

Return JSON with tags, confidence scores, and SEO meta tags.
```

### Example 2: Bulk Tag WordPress Content
```
Connect to my WordPress site (wp.example.com) and:
1. Retrieve all posts from the past 6 months
2. Apply AI taxonomy to each post
3. Auto-assign WordPress categories and tags
4. Generate meta descriptions and schema markup
5. Return a CSV report with tagging results and coverage %

Use my custom taxonomy: [list your categories]
```

### Example 3: Create a Content Map
```
Analyze my content library (100+ articles) and:
1. Identify all unique topics and subtopics
2. Create a hierarchical taxonomy tree
3. Map content to audience personas
4. Highlight content gaps and overlap
5. Recommend new content opportunities

Export as an interactive JSON structure and Markdown outline.
```

---

## Capabilities

### 1. Intelligent Content Analysis
- **Multi-dimensional Tagging**: Simultaneously categorize by topic, format, audience, industry, intent, and custom dimensions
- **Semantic Understanding**: Uses transformer-based NLP to understand context beyond keywords
- **Confidence Scoring**: Every tag includes a 0-100 confidence score for quality control
- **Multi-language Support**: Analyze content in 50+ languages and tag in your preferred language

### 2. Custom Taxonomy Management
- **Build Custom Taxonomies**: Define hierarchical category trees specific to your business
- **Dynamic Tag Suggestions**: AI learns from your existing tags and suggests new ones
- **Taxonomy Versioning**: Track taxonomy changes and maintain backward compatibility
- **Synonym Management**: Map related terms (e.g., "AI" = "artificial intelligence" = "machine learning")

### 3. Content Organization
- **Bulk Processing**: Tag 100+ articles in minutes via batch operations
- **Incremental Updates**: Process new content automatically as it's published
- **Duplicate Detection**: Identify similar content and consolidate taxonomies
- **Cross-linking**: Suggest related content based on shared tags

### 4. SEO & Metadata Generation
- **Schema Markup**: Auto-generate JSON-LD structured data for rich snippets
- **Meta Tags**: Create optimized title tags, meta descriptions, and OG tags
- **Keyword Extraction**: Identify primary and secondary keywords with search volume
- **Readability Scoring**: Assess content complexity and reading level

### 5. Multi-Platform Distribution
- **Content Syndication**: Apply consistent tags across WordPress, Shopify, and custom CMS
- **API Webhooks**: Push tags to external systems via REST/GraphQL APIs
- **Format Conversion**: Export tags as CSV, JSON, XML, or proprietary formats
- **Slack Integration**: Post tagging results and recommendations to team channels

---

## Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="sk-..."                    # GPT-4 or GPT-3.5-turbo for analysis
export CONTENT_TAXONOMY_CONFIG="config.json"      # Path to taxonomy definition

# Optional
export WORDPRESS_URL="https://yoursite.com"       # WordPress REST API endpoint
export WORDPRESS_TOKEN="xxxxxxxx"                 # WordPress application password
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
export ELASTICSEARCH_HOST="localhost:9200"        # For tag indexing
export CUSTOM_TAXONOMY_FILE="taxonomy.json"       # Your taxonomy rules
```

### Taxonomy Configuration File (taxonomy.json)
```json
{
  "version": "1.0.0",
  "categories": {
    "industry": [
      "e-commerce", "saas", "healthcare", "fintech", "education"
    ],
    "format": [
      "blog-post", "video", "infographic", "case-study", "whitepaper", "guide"
    ],
    "audience": [
      "c-suite", "managers", "individual-contributors", "entrepreneurs"
    ],
    "intent": [
      "educational", "promotional", "how-to", "comparison", "news"
    ]
  },
  "confidence_threshold": 0.75,
  "max_tags_per_content": 15,
  "language": "en"
}
```

### Setup Instructions
1. **Obtain API Keys**: Get OpenAI API key from platform.openai.com
2. **Define Taxonomy**: Create or upload your taxonomy.json file
3. **Test Connection**: Run `openclaw test ai-driven-content-taxonomy-and-tagging`
4. **Configure Integrations**: Connect WordPress, Slack, or other platforms (optional)
5. **Dry Run**: Process 5-10 sample articles to validate results before bulk operations

---

## Example Outputs

### Output 1: Detailed Tag Report (JSON)
```json
{
  "content_id": "post_12345",
  "title": "How to Build a Sustainable E-commerce Business",
  "tags": {
    "industry": [
      { "tag": "e-commerce", "confidence": 0.98, "weight": 1.0 },
      { "tag": "sustainability", "confidence": 0.92, "weight": 0.8 }
    ],
    "format": [
      { "tag": "guide", "confidence": 0.95, "weight": 1.0 }
    ],
    "audience": [
      { "tag": "entrepreneurs", "confidence": 0.89, "weight": 0.9 },
      { "tag": "business-owners", "confidence": 0.85, "weight": 0.8 }
    ],
    "intent": [
      { "tag": "educational", "confidence": 0.96, "weight": 1.0 }
    ]
  },
  "seo_metadata": {
    "meta_title": "How to Build a Sustainable E-commerce Business in 2024",
    "meta_description": "Learn proven strategies for building an eco-friendly e-commerce business. Expert guide covering sustainable sourcing, green logistics, and customer education.",
    "primary_keyword": "sustainable e-commerce",
    "secondary_keywords": ["eco-friendly online store", "green business practices"],
    "schema_markup": {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "How to Build a Sustainable E-commerce Business in 2024",
      "keywords": ["sustainable e-commerce", "eco-friendly"]
    }
  },
  "reading_level": "intermediate",
  "estimated_read_time": "8 minutes",
  "related_content": ["post_12340", "post_12341"],
  "processing_time_ms": 2340
}
```

### Output 2: Bulk Processing Summary (CSV)
```csv
post_id,title,industry,format,audience,intent,confidence_avg,seo_score,status
12345,"How to Build Sustainable E-commerce",e-commerce,guide,entrepreneurs,educational,0.92,92,success
12346,"Q3 Financial Report",fintech,whitepaper,c-suite,promotional,0.88,85,success
12347,"Customer Success Story",saas,case-study,managers,promotional,0.91,89,success
12348,"API Documentation",saas,guide,developers,educational,0.94,91,success
```

### Output 3: Content Gap Analysis
```markdown
## Content Taxonomy Coverage Report

### Strengths
- **E-commerce**: 45 articles (excellent coverage)
- **Sustainability**: 28 articles (good coverage)
- **Guides**: 92 articles (strong format diversity)

### Gaps Identified
- **Healthcare + Sustainability**: 0 articles (opportunity)
- **Video Format**: Only 3 articles (underutilized)
- **C-Suite Audience**: 5 articles (expand for enterprise market)

### Recommendations
1. Create 3-5 healthcare sustainability case studies
2. Produce 10-15 video tutorials on core topics
3. Develop 5 executive briefings for C-suite audience
4. Consolidate 8 overlapping articles on "green logistics"
```

---

## Tips & Best Practices

### 1. Taxonomy Design
- **Start Simple**: Begin with 3-5 main dimensions (industry, format, audience, intent, topic)
- **Avoid Overlap**: Ensure categories are mutually exclusive where possible
- **Use Hierarchies**: Organize tags in parent-child relationships (e.g., "Technology > AI > LLMs")
- **Regular Audits**: Review and refine your taxonomy quarterly as your content evolves

### 2. Confidence Thresholds
- **Strict (>0.90)**: Use for critical content, compliance-heavy industries
- **Balanced (0.75-0.90)**: Default for most content; catches 95% of correct tags
- **Permissive (<0.75)**: Use for discovery/brainstorming; requires manual review

### 3. Bulk Operations
- **Test First**: Always run 5-10 articles before processing entire library
- **Batch Size**: Process 100-500 articles per batch to avoid API rate limits
- **Monitor Progress**: Check Slack notifications or logs for errors in real-time
- **Schedule Off-Peak**: Run bulk jobs during low-traffic hours

### 4. Content Maintenance
- **Incremental Tagging**: Tag new content within 24 hours of publication
- **Seasonal Updates**: Refresh tags quarterly to capture trending topics
- **Remove Obsolete Tags**: Archive taxonomy versions no longer in use
- **Document Changes**: Maintain a changelog of taxonomy modifications

### 5. Integration Best Practices
- **Webhook Validation**: Verify WordPress/Slack webhooks are receiving data
- **Error Handling**: Set up alerts for failed tag updates across platforms
- **Backup Original Tags**: Keep manual tags as fallback if AI tagging fails
- **A/B Test Results**: Compare AI tags vs. human-created tags for 30 days

---

## Safety & Guardrails

### What This Skill Will NOT Do
- **Override Manual Tags**: AI tags are suggestions; existing manual tags are never auto-deleted
- **Make Sensitive Decisions**: Does not classify content as harmful, illegal, or NSFW without human review
- **Modify Content**: Only adds metadata; never rewrites article text or titles
- **Store Sensitive Data**: Does not retain or log content body text; only processes for tagging
- **Guarantee Accuracy**: AI tagging is 90-95% accurate; always review high-stakes classifications

### Limitations & Boundaries
- **Language Support**: Optimal performance in English; other languages may have 5-10% lower accuracy
- **Domain-Specific Jargon**: May struggle with highly specialized terminology; use custom synonym mapping
- **Content Length**: Works best with 300+ word articles; very short content (< 100 words) may be undertagged
- **Rate Limits**: OpenAI API has 3,500 requests/minute limit; batch processing respects this automatically
- **Cost Implications**: Typical cost is $0.02-0.05 per article depending on length and API model

### Privacy & Compliance
- **GDPR Compliance**: Does not store PII; processes content in memory only
- **SOC 2 Alignment**: Compatible with enterprise security requirements
- **Data Retention**: Tagging results stored locally; no external logging by default
- **Audit Trail**: Maintains version history of all taxonomy changes for compliance

---

## Troubleshooting

### Q: Why are some tags showing low confidence scores (<0.70)?
**A:** Low confidence indicates ambiguous content or domain-specific terminology not in the AI model's training data. **Solutions**:
- Add custom synonyms to your taxonomy.json (e.g., "ML" → "machine learning")
- Review the content; it may genuinely be multi-topic
- Increase confidence threshold to filter low-quality tags
- Provide training examples for niche topics

### Q: Bulk tagging is slow. How can I speed it up?
**A:** Default settings use GPT-4 for accuracy. **Solutions**:
- Switch to GPT-3.5-turbo for 3x faster processing (slight accuracy trade-off)
- Increase batch size from 100 to 500 articles
- Disable schema markup generation if not needed
- Run processing during off-peak hours (fewer concurrent API requests)

### Q: My WordPress tags aren't syncing. What's wrong?
**A:** Common causes: expired authentication token, incorrect REST API endpoint, or insufficient permissions. **Solutions**:
1. Verify WordPress URL is correct: `https://yoursite.com/wp-json/wp/v2/posts`
2. Regenerate application password in WordPress: Settings > Application Passwords
3. Check user role has "edit_posts" capability
4. Test with: `curl -u user:password https://yoursite.com/wp-json/wp/v2/posts`
5. Enable debug logging: `export DEBUG=openclaw:*`

### Q: How do I prevent over-tagging (too many tags per article)?
**A:** Set `max_tags_per_content` in your taxonomy.json configuration:
```json
{
  "max_tags_per_content": 12,
  "tag_priority": "confidence_desc"
}
```
This keeps only the 12 highest-confidence tags per article. Adjust based on your CMS and user experience preferences.

### Q: Can I use this for non-English content?
**A:** Yes, but with caveats. **Supported languages**: Spanish, French, German, Chinese, Japanese, Portuguese.
- Accuracy: 85-90% (vs. 95% for English)
- Set language in config: `"language": "es"` for Spanish
- Consider using language-specific OpenAI models if available
- Provide more training examples for non-English taxonomies

### Q: What if my content is behind a paywall or login?
**A:** The skill processes content you provide directly. **Options**:
1. Copy/paste article text directly into the prompt
2. Export content from your CMS API (WordPress, Contentful, etc.)
3. Use browser automation to fetch login-protected content
4. Provide raw content files (CSV, JSON, Markdown)

### Q: How do I maintain consistency across multiple content creators?
**A:** Implement a taxonomy governance process:
1. **Centralized Taxonomy**: Store taxonomy.json in version control (GitHub)
2. **Training**: Show team examples of correctly tagged articles
3. **Approval Workflow**: Have editors review AI tags before publishing
4. **Feedback Loop**: Update custom synonyms based on rejected tags
5. **Monthly Audits**: Spot-check 50 articles for consistency

### Q: Can I export tags in a specific format for my CMS?
**A:** Yes. The skill supports multiple export formats:
```bash