---
name: cross-platform-content-syncer
description: "Distribute content across WordPress, Substack, Medium, and LinkedIn with one-click automation. Use when the user needs multi-channel publishing, content syndication, or unified social distribution."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "WORDPRESS_API_TOKEN",
          "SUBSTACK_API_KEY",
          "MEDIUM_API_TOKEN",
          "LINKEDIN_ACCESS_TOKEN",
          "SLACK_WEBHOOK_URL"
        ],
        "bins": ["curl", "jq"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔄"
    }
  }
---

## Overview

**Cross-Platform Content Syncer** automates one-to-many content distribution across WordPress, Substack, Medium, and LinkedIn. Instead of manually copying, reformatting, and republishing content on each platform, this skill handles the entire workflow: it takes your source content, adapts it for each platform's unique requirements and audience, and publishes simultaneously or on a schedule.

### Why This Matters

Content creators, marketers, and agencies waste 4-6 hours weekly republishing the same article across platforms. Each platform requires different formatting (LinkedIn's character limits, Medium's clap-friendly structure, Substack's subscriber segmentation). This skill eliminates that friction.

**Specific Integrations:**
- **WordPress** (self-hosted or WordPress.com) via REST API
- **Substack** for email-first publishing and subscriber lists
- **Medium** for reach and algorithmic distribution
- **LinkedIn** for professional networking and thought leadership
- **Slack** for team notifications and approval workflows
- **Google Drive** for draft storage and collaboration

---

## Quick Start

Try these prompts immediately:

### Example 1: Publish a Blog Post Across All Platforms
```
Sync this blog post to WordPress, Medium, and LinkedIn:
Title: "5 Hidden Features in Claude AI You're Not Using"
Content: [paste full article]
Platforms: wordpress, medium, linkedin
Tone: professional, slightly conversational
Featured image: [image URL]
Tags: AI, productivity, Claude, automation
Schedule: immediately
```

### Example 2: Distribute a Newsletter to Multiple Channels
```
Distribute my Substack newsletter to WordPress and LinkedIn:
Newsletter subject: "Weekly AI Digest — October 2024"
Content: [newsletter body]
Substack list: paid_subscribers
WordPress category: newsletters
LinkedIn article type: newsletter_post
Add CTA: "Subscribe on Substack for weekly insights"
Schedule: 2024-10-15 09:00 AM EST
```

### Example 3: Batch Sync with Platform-Specific Adaptations
```
Sync 5 blog posts across all platforms with custom adaptations:
Source: WordPress blog (category: "tutorials")
Destinations: medium, linkedin, substack
Adaptations:
  - Medium: Add "Originally published on [blog name]" footer
  - LinkedIn: Convert to carousel posts (1 image per section)
  - Substack: Add subscriber-only bonus section
  - WordPress: Keep as-is
Notify team via Slack when complete
```

---

## Capabilities

### 1. Intelligent Content Adaptation
The skill automatically reformats content for each platform's unique requirements:

- **WordPress**: Preserves full formatting, embeds, and custom fields. Optimizes for SEO with meta descriptions and excerpt generation.
- **Medium**: Strips WordPress-specific markup, converts to Medium's native formatting, adds publication selection and story tags.
- **LinkedIn**: Converts long-form articles into LinkedIn article format, creates carousel post versions for visual content, optimizes headlines for engagement.
- **Substack**: Extracts key sections, adds subscriber-only gates, integrates with your mailing list, generates email subject lines.

### 2. Multi-Channel Scheduling
- Publish immediately across all platforms simultaneously
- Stagger publication (e.g., WordPress first, then Medium after 24 hours, LinkedIn after 48 hours)
- Schedule recurring content (weekly digests, monthly roundups)
- Timezone-aware scheduling for global audiences

### 3. SEO & Metadata Management
- Auto-generate meta descriptions from content
- Create platform-specific slugs and URLs
- Manage canonical URLs to avoid duplicate content penalties
- Sync featured images and alt text across platforms
- Preserve or optimize tags and categories per platform

### 4. Team Collaboration & Approvals
- Send draft previews to Slack for team review before publishing
- Require approval workflows (editor → manager → publish)
- Track publication history with audit logs
- Enable/disable platforms per content piece

### 5. Performance Analytics Integration
- Log publication URLs to a tracking spreadsheet
- Monitor initial engagement metrics (views, clicks, shares)
- Generate weekly distribution reports
- Track which platforms drive the most traffic back to your site

### 6. Subscriber List Management
- Sync Substack subscriber segments with content distribution
- Segment LinkedIn posts by audience (connections, followers, specific groups)
- Tag Medium followers for future campaigns
- Manage WordPress subscriber notifications

---

## Configuration

### Required Environment Variables

Set these before using the skill:

```bash
export WORDPRESS_API_TOKEN="your_wordpress_rest_api_token"
export WORDPRESS_SITE_URL="https://yourblog.com"

export SUBSTACK_API_KEY="your_substack_api_key"
export SUBSTACK_PUBLICATION_ID="your_publication_id"

export MEDIUM_API_TOKEN="your_medium_integration_token"
export MEDIUM_PUBLICATION_ID="your_publication_id"

export LINKEDIN_ACCESS_TOKEN="your_linkedin_oauth_token"
export LINKEDIN_ORGANIZATION_URN="urn:li:organization:123456"

export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_CHANNEL="#content-publishing"
```

### Configuration File (Optional)

Create a `sync-config.json` for default settings:

```json
{
  "default_platforms": ["wordpress", "medium", "linkedin"],
  "scheduling": {
    "stagger_hours": 24,
    "timezone": "America/New_York",
    "auto_publish": false
  },
  "adaptations": {
    "medium": {
      "add_canonical_link": true,
      "footer_text": "Originally published on [BLOG_NAME]"
    },
    "linkedin": {
      "create_carousel": true,
      "images_per_section": 1
    },
    "substack": {
      "add_subscriber_gate": false,
      "bonus_section": true
    }
  },
  "notifications": {
    "slack_preview": true,
    "slack_on_publish": true,
    "require_approval": false
  }
}
```

---

## Example Outputs

### Output 1: Publication Confirmation
```
✅ Content Successfully Synced

Article: "5 Hidden Features in Claude AI You're Not Using"
Published: 2024-10-15 09:30 AM EST

📱 Platform Status:
  ✓ WordPress — Published (ID: 4521)
    URL: https://yourblog.com/claude-ai-features/
    SEO: 92/100 | Featured image: 1200x630px
  
  ✓ Medium — Published (ID: abc123def456)
    URL: https://medium.com/@yourname/claude-ai-features
    Claps: 0 (check back in 1 hour)
  
  ✓ LinkedIn — Published (Article)
    URL: https://www.linkedin.com/feed/update/urn:li:activity:7123456789/
    Engagement: Track in LinkedIn analytics
  
  ⏳ Substack — Scheduled (Draft ID: draft_789)
    Sending to: 2,341 subscribers
    Scheduled: 2024-10-16 08:00 AM EST
    CTA: "Read the full article on our blog"

📊 Analytics Dashboard:
  Sync Duration: 45 seconds
  Content Size: 2,847 words
  Images Processed: 3
  Slack Notification: Sent to #content-publishing
```

### Output 2: Batch Sync Report
```
Batch Sync Complete: "October Tutorial Series"

Synced: 5 articles across 4 platforms
Total Time: 3 minutes 22 seconds
Success Rate: 100% (20/20 publications)

Platform Breakdown:
├─ WordPress: 5 published (5 featured images optimized)
├─ Medium: 5 published (5 canonical links added)
├─ LinkedIn: 5 articles + 15 carousel posts
└─ Substack: 5 drafts (awaiting approval)

Next Steps:
1. Review Substack drafts in your account
2. Approve scheduled LinkedIn posts
3. Check Medium publication settings
4. Monitor engagement over next 48 hours

Team Notified: #content-publishing (Slack)
```

---

## Tips & Best Practices

### 1. Optimize for Each Platform's Audience
- **WordPress**: Full SEO optimization, internal linking, evergreen content
- **Medium**: Trending topics, quick reads (5-10 min), engaging headlines
- **LinkedIn**: Professional insights, industry trends, thought leadership
- **Substack**: Personal voice, subscriber-exclusive insights, calls-to-action

### 2. Use Platform-Specific Adaptations
Don't just duplicate content. Leverage the skill's adaptation features:
- Add LinkedIn carousel posts for visual content (breaks up text, increases engagement)
- Gate premium insights behind Substack subscriber walls
- Add "Read More" CTAs linking back to your WordPress blog
- Include Medium's native recommendation system by tagging appropriately

### 3. Schedule Strategically
- Publish to WordPress first (your owned platform)
- Stagger Medium and LinkedIn by 24-48 hours (avoids algorithmic cannibalization)
- Send Substack newsletters at peak subscriber engagement times (typically 9-11 AM)
- Use timezone awareness for global audiences

### 4. Maintain Canonical URLs
Always set WordPress as canonical source to avoid SEO penalties:
```
Medium: Add canonical link to WordPress URL
LinkedIn: Use "originally published" footer with WordPress link
Substack: Include "Read full article" CTA with WordPress link
```

### 5. Leverage Analytics Integration
- Track which platform drives most traffic back to your site
- Monitor engagement metrics per platform (LinkedIn reactions, Medium claps, WordPress comments)
- Identify high-performing content and repurpose it
- Use data to optimize future distribution strategy

### 6. Build Team Workflows
- Enable Slack preview + approval for editorial control
- Assign platform responsibilities (e.g., one person manages LinkedIn adaptations)
- Use scheduling to create buffer time for reviews
- Document platform-specific best practices for your team

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Override Platform Policies**: This skill respects each platform's terms of service. It will not:
   - Post duplicate content that violates Medium's guidelines
   - Create spam or misleading headlines
   - Bypass LinkedIn's native content restrictions
   - Violate Substack subscriber privacy

2. **Guarantee Engagement**: Publication does not equal virality. The skill distributes content but cannot:
   - Guarantee views, clicks, or shares
   - Bypass algorithmic suppression
   - Force audience engagement
   - Predict content performance

3. **Modify Sensitive Content**: The skill will not:
   - Automatically remove sensitive information (you must review)
   - Translate content (you must provide translations)
   - Rewrite content to deceive audiences
   - Publish without explicit user confirmation

4. **Handle Paywalled Content**: If your WordPress blog has paywalls, the skill will:
   - Warn you before syncing to free platforms
   - Require explicit confirmation to publish behind paywalls
   - Not automatically gate content on Substack without your approval

### Limitations & Boundaries

- **Rate Limits**: Respects each platform's API rate limits. Batch syncs may take longer during peak hours.
- **Image Optimization**: Automatically resizes images but may lose quality on very large files (>10MB).
- **Character Limits**: LinkedIn has character limits; very long posts will be truncated with warning.
- **Formatting Loss**: Some WordPress formatting (custom CSS, plugins) may not transfer to Medium/LinkedIn.
- **Scheduling Window**: Cannot schedule more than 90 days in advance on most platforms.

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "API Token Invalid" Error**
```
Solution:
1. Verify token is not expired (regenerate if necessary)
2. Check token has correct permissions for each platform
3. Ensure token is set in environment variables (not hardcoded)
4. Test token with platform's native API first

Command to test:
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.medium.com/v1/me
```

**Issue: Images Not Uploading to Medium/LinkedIn**
```
Solution:
1. Verify image URLs are publicly accessible (not behind login)
2. Check image format (JPEG/PNG preferred; WebP may fail)
3. Ensure image size < 10MB
4. Try uploading image directly to platform first

Supported formats: JPG, PNG, GIF (animated GIFs may fail on LinkedIn)
```

**Issue: LinkedIn Post Truncated or Formatting Broken**
```
Solution:
1. LinkedIn article limit: 3,000 characters (use carousel posts for longer content)
2. Remove HTML formatting—LinkedIn only supports plain text + links
3. Use skill's carousel adaptation for visual content
4. Preview on LinkedIn before syncing in bulk

Check: Is your content >3,000 characters? Use carousel posts instead.
```

**Issue: Substack Draft Not Appearing**
```
Solution:
1. Verify Substack API key has "draft" permissions (not just "publish")
2. Check publication ID is correct (not your user ID)
3. Drafts may take 5-10 seconds to appear in Substack UI
4. Refresh Substack browser window to see new drafts

Debug: List all drafts with:
curl -H "Authorization: Bearer YOUR_KEY" https://api.substack.com/v1/drafts
```

**Issue: Canonical URL Not Showing on Medium**
```
Solution:
1. Medium requires canonical URLs in article settings (not just footer)
2. Skill automatically adds to article metadata
3. Verify in Medium editor: Settings → Story Details → Canonical URL
4. May take 24-48 hours for Google to recognize

Note: Canonical URLs are optional but recommended for SEO.
```

### FAQ

**Q: Will syncing content hurt my SEO?**
A: No, if you set WordPress as canonical source. The skill automatically adds canonical links to Medium and LinkedIn, telling Google to credit your WordPress blog.

**Q: Can I sync only to specific platforms?**
A: Yes. Specify platforms in your sync command: `platforms: medium, linkedin` (skip WordPress and Substack).

**Q: What if I want different content for each platform?**
A: Use the skill's adaptation features to customize per platform, or create separate sync commands with different source content.

**Q: How often can I sync?**
A: No limit on frequency, but respect each platform's guidelines. Posting the same content multiple times daily may be flagged as spam.

**Q: Can I undo a publication?**
A: The skill logs all publications and provides delete/unpublish commands for each platform. However, some platforms (Medium, LinkedIn) may cache content briefly.

**Q: Does this work with WordPress multisite?**
A: Yes, if you have API access to each site. You'll need separate API tokens per site.

**Q: Can I schedule content months in advance?**
A: Most platforms limit scheduling to 90 days. The skill will warn you and suggest alternatives (manual scheduling later, or publish immediately).

---

## Integration Examples

### With Zapier/Make
```
Trigger: New WordPress post
→ Cross-Platform Content Syncer
→ Publish to Medium + LinkedIn
→ Send Slack notification
```

### With Editorial Calendar
```
Publish WordPress post
→ Automatically sync to Medium (24h later)
→ Sync to LinkedIn (48h later)
→ Send Substack draft (await approval)
```

### With Analytics Tools
```
Sync content
→ Log URLs to Google Sheets
→ Track engagement metrics daily
→ Generate weekly distribution report
```

---

## Support & Resources

- **GitHub Issues**: Report bugs at https://github.com/ncreighton/empire-skills/issues
- **Documentation**: Full API reference at https://github.com/ncreighton/empire-skills/wiki
- **Community**: Join our Slack for tips and troubleshooting
- **Updates**: Follow @EmpireSkills for