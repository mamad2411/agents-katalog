```markdown
---
name: email-sequence-builder
description: Generate comprehensive email drip sequences from product descriptions with advanced personalization and automation features
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: ["OPENAI_API_KEY"]
      bins: []
    os: ["macos", "linux", "windows"]
---

# Email Sequence Builder

Transform your product descriptions and content ideas into high-converting email drip sequences with advanced personalization, A/B testing variations, and seamless integration capabilities. This skill generates complete email campaigns optimized for engagement, conversion, and customer retention across multiple industries and use cases.

## Overview

The Email Sequence Builder revolutionizes how businesses create email marketing campaigns by automatically generating comprehensive drip sequences from simple product or content descriptions. Whether you're launching a SaaS product, promoting an online course, or nurturing leads for a consulting service, this skill creates professionally crafted email sequences that drive results.

**Key Integrations & Platforms:**
- **Mailchimp** - Export-ready campaign templates
- **ConvertKit** - Creator-focused sequences with tagging
- **ActiveCampaign** - Advanced automation workflows
- **HubSpot** - CRM-integrated nurture campaigns
- **WordPress** - Blog content promotion sequences
- **Shopify** - E-commerce product launch campaigns
- **Slack** - Team collaboration on email content
- **Google Sheets** - Campaign performance tracking templates

**Why This Matters:**
Email marketing delivers an average ROI of $42 for every $1 spent, but creating effective sequences requires expertise in copywriting, psychology, and timing. This skill democratizes professional email marketing by generating sequences that incorporate proven conversion principles, personalization strategies, and industry best practices.

## Quick Start

Get started immediately with these example prompts:

```
Generate a 7-email welcome sequence for a productivity app called "FocusFlow" 
that helps remote workers eliminate distractions and boost deep work sessions. 
Include onboarding tips and feature highlights.
```

```
Create a 5-email product launch sequence for handmade ceramic coffee mugs 
targeting coffee enthusiasts. Include storytelling about the artisan process 
and limited-time launch pricing.
```

```
Build a 10-email nurture sequence for a B2B cybersecurity consulting firm 
targeting mid-size companies. Focus on education about common threats and 
positioning our expertise.
```

```
Design a re-engagement sequence (4 emails) for an online fitness coaching 
program targeting people who signed up but haven't started their workouts yet.
```

## Capabilities

### Sequence Types & Customization
- **Welcome Series** - Onboard new subscribers with value-driven content
- **Product Launch** - Build anticipation and drive sales for new releases
- **Nurture Campaigns** - Educate prospects and build trust over time
- **Re-engagement** - Win back inactive subscribers and customers
- **Upsell/Cross-sell** - Increase customer lifetime value with relevant offers
- **Event Promotion** - Drive registrations and attendance for webinars/events

### Advanced Personalization Features
- **Dynamic Content Blocks** - Customize based on subscriber behavior and preferences
- **Segmentation Variables** - Tailor messaging for different audience segments
- **Behavioral Triggers** - Adjust sequence based on engagement patterns
- **Industry-Specific Messaging** - Adapt tone and examples for target markets
- **Seasonal Adaptations** - Incorporate timely references and seasonal relevance

### Content Optimization
- **Subject Line Variations** - Generate A/B testing options for maximum open rates
- **Call-to-Action Optimization** - Create compelling CTAs that drive conversions
- **Social Proof Integration** - Incorporate testimonials and case studies naturally
- **Urgency and Scarcity** - Implement psychological triggers ethically and effectively
- **Mobile-First Design** - Ensure readability across all devices and email clients

## Configuration

### Required Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Optional Configuration
Set these environment variables to enhance functionality:
```bash
export EMAIL_BRAND_VOICE="professional|casual|friendly|authoritative"
export DEFAULT_SEQUENCE_LENGTH="5"
export INCLUDE_ANALYTICS_TRACKING="true"
export TARGET_AUDIENCE_DEFAULT="general"
```

### Setup Instructions
1. **API Access**: Ensure your OpenAI API key has sufficient credits for content generation
2. **Brand Guidelines**: Prepare your brand voice guidelines, color schemes, and messaging frameworks
3. **Customer Data**: Gather customer personas, pain points, and success stories for personalization
4. **Integration Planning**: Identify which email service provider you'll use for deployment

## Example Outputs

### Sample Email from SaaS Welcome Sequence:
```
Subject: Welcome to ProductivityPro - Your 30-day transformation starts now! 🚀

Hi [First Name],

Welcome to the ProductivityPro family! You've just taken the first step toward 
reclaiming 2+ hours of focused work time every single day.

Over the next 30 days, I'll be your personal guide as you transform from 
scattered and overwhelmed to laser-focused and accomplished.

Here's what happens next:

✅ Day 1-3: Master the "Deep Work Blocks" technique (this alone saves most users 90 minutes daily)
✅ Day 4-7: Set up your distraction-free workspace (both digital and physical)
✅ Week 2: Implement the "Priority Matrix" that top performers swear by
✅ Week 3-4: Advanced automation and delegation strategies

Your first mission (if you choose to accept it): Block out 25 minutes today 
for ONE important task. No phone, no notifications, just pure focus.

Ready to start? Click here to access your Day 1 training: [CTA BUTTON]

Cheering you on,
Sarah Chen
Founder, ProductivityPro

P.S. Hit reply and let me know what productivity challenge you're most excited to solve!
```

### Campaign Analytics Template:
- Open Rate Benchmarks by Industry
- Click-through Rate Optimization Suggestions  
- Engagement Scoring Methodology
- Revenue Attribution Framework
- A/B Testing Results Documentation

## Tips & Best Practices

### Maximizing Engagement
- **Timing Optimization**: Schedule emails based on your audience's time zone and behavior patterns
- **Frequency Balance**: Space emails 2-3 days apart for nurture sequences, daily for launch campaigns
- **Value-First Approach**: Ensure each email provides standalone value, not just sales pitches
- **Storytelling Integration**: Weave narrative elements throughout the sequence to maintain interest

### Technical Optimization
- **Subject Line Testing**: Always generate 3-5 subject line options and test performance
- **Mobile Preview**: Preview emails on mobile devices where 60%+ of emails are opened
- **Link Tracking**: Implement UTM parameters for accurate campaign attribution
- **Deliverability Best Practices**: Maintain clean lists and monitor spam scores

### Content Strategy
- **Progressive Disclosure**: Reveal information gradually to maintain curiosity and engagement
- **Social Proof Placement**: Include testimonials and case studies strategically throughout
- **Objection Handling**: Address common concerns and hesitations proactively
- **Clear Next Steps**: Every email should have one primary call-to-action

## Troubleshooting

### Common Issues & Solutions

**Q: Generated emails feel too generic or robotic**
A: Provide more specific details about your target audience, brand voice, and unique value propositions. Include customer language and pain points from actual conversations.

**Q: Sequence length doesn't match my campaign goals**
A: Specify your desired sequence length and campaign objectives explicitly. Consider your sales cycle length and audience engagement patterns.

**Q: Content doesn't align with my brand voice**
A: Set the EMAIL_BRAND_VOICE environment variable and provide examples of your existing content. Include specific tone guidelines and words/phrases to avoid.

**Q: Integration with email service provider is challenging**
A: The skill generates platform-agnostic content. Use the web_search tool to find specific import instructions for your ESP (Mailchimp, ConvertKit, etc.).

**Q: Personalization tokens aren't working**
A: Ensure your email service provider supports the merge tags used (typically [First Name], [Company], etc.). Adjust the generated content to match your ESP's syntax.

### Performance Optimization
- Monitor open rates above 25% and click rates above 3%
- Test send times and frequency adjustments if engagement drops
- Segment underperforming subscribers for re-engagement campaigns
- Regularly update content based on customer feedback and market changes

### Advanced Customization
Use the exec tool to create custom templates, integrate with external APIs for dynamic content, or set up automated A/B testing workflows based on your specific requirements and technical infrastructure.
```