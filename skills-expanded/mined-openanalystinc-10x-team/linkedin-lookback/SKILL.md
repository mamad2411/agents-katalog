# LinkedIn Lookback Integration Skill

## Overview

Integrates the LinkedIn Lookback Chrome extension with 10x-Team marketing automation system to create intelligent lead tracking, automated follow-up workflows, and prospect enrichment pipelines.

## What is LinkedIn Lookback?

LinkedIn Lookback is a Chrome extension that silently tracks your LinkedIn activity:
- **Profile Views**: Records when you visit someone's LinkedIn profile
- **Connection Requests**: Logs when you send connection requests
- **Messages Sent**: Tracks when you send LinkedIn messages
- **Profile Data**: Extracts name, headline, company, title, education, location, connection degree
- **Prospect Matching**: Identifies interactions with target prospects from imported CSV lists
- **Local Storage**: All data stored locally in browser IndexedDB (privacy-first)

GitHub Repository: https://github.com/kvivek0591/linkedin-lookback

## Integration Benefits

### 1. **Lead Intelligence Pipeline**
- Track profile visits automatically
- Identify warm leads based on interaction frequency
- Auto-qualify leads using engagement signals
- Trigger personalized outreach campaigns

### 2. **Smart Follow-up Automation**
```
Profile Visit → Wait 24h → Send Connection Request
Connection Accepted → Wait 48h → Send Intro Message
Message Sent → No Reply in 5d → Escalate to Email Campaign
```

### 3. **Prospect Enrichment**
- Combine Lookback data with Exa AI discovery
- Enrich profiles with company data, tech stack, recent posts
- Build comprehensive prospect profiles
- Identify decision-maker patterns

### 4. **Campaign Attribution**
- Track which LinkedIn activities lead to conversions
- Measure ROI of LinkedIn outreach
- Identify best-performing profiles/companies
- Optimize targeting based on data

### 5. **Anti-Spam Protection**
- Check interaction history before outreach
- Prevent duplicate connection requests
- Maintain professional reputation
- Track outreach cadence and frequency

## Architecture

```
LinkedIn Lookback Extension (Browser)
    ↓
IndexedDB (Local Storage)
    ↓
Data Sync Scripts (Node.js)
    ↓
10x-Team Workflows
    ↓
├─ Lead Qualification (lead-qualifier agent)
├─ Automated Outreach (linkedin-adapter + gmail-adapter)
├─ Prospect Enrichment (discovery-engine via Exa AI)
└─ Campaign Tracking (analytics-analyst agent)
```

## Installation

### Step 1: Install LinkedIn Lookback Extension

1. Clone the repository:
```bash
git clone https://github.com/kvivek0591/linkedin-lookback.git
```

2. Load in Chrome:
   - Go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `linkedin-lookback` folder

### Step 2: Activate the Skill

In Claude Code:
```bash
/linkedin-lookback
```

This will:
- Set up data sync infrastructure
- Create automation workflows
- Configure prospect enrichment
- Enable campaign tracking

## Usage

### Slash Commands

#### `/lookback:sync`
Sync activity data from LinkedIn Lookback extension to 10x-Team system.

**What it does:**
- Exports data from browser IndexedDB
- Imports into 10x-Team database
- Identifies new leads and prospects
- Triggers automated workflows

**Example:**
```bash
/lookback:sync
```

#### `/lookback:enrich [profile_url]`
Enrich a LinkedIn profile with additional data using Exa AI discovery.

**Parameters:**
- `profile_url`: LinkedIn profile URL (optional, enriches all recent profiles if omitted)

**What it does:**
- Fetches profile data from Lookback
- Discovers additional context via Exa AI
- Extracts company info, tech stack, recent posts
- Updates prospect database

**Example:**
```bash
/lookback:enrich https://linkedin.com/in/john-doe
```

#### `/lookback:campaign [activity_type]`
Create automated outreach campaign from Lookback activity data.

**Parameters:**
- `activity_type`: `profile_view` | `connection_request` | `message_sent` | `all`

**What it does:**
- Filters activities by type
- Segments leads based on engagement
- Creates personalized outreach sequences
- Sets up follow-up automation

**Example:**
```bash
# Create campaign from all profile views
/lookback:campaign profile_view

# Create campaign from connection requests
/lookback:campaign connection_request
```

#### `/lookback:stats [period]`
View LinkedIn activity statistics and insights.

**Parameters:**
- `period`: `today` | `week` | `month` | `all`

**What it does:**
- Shows activity breakdown (views, connections, messages)
- Prospect interaction rate
- Top companies/titles engaged
- Conversion metrics

**Example:**
```bash
/lookback:stats week
```

#### `/lookback:check [profile_url]`
Check if you've previously interacted with a LinkedIn profile.

**Parameters:**
- `profile_url`: LinkedIn profile URL

**What it does:**
- Searches Lookback history
- Shows all previous interactions
- Displays last contact date
- Recommends follow-up actions

**Example:**
```bash
/lookback:check https://linkedin.com/in/jane-smith
```

## Automation Workflows

### Workflow 1: Profile Visit → Connection Request
```yaml
Trigger: Profile visit detected
Wait: 24 hours
Check: Not already connected
Action: Send personalized connection request
Template: LinkedIn message template with {name}, {company}, {title} variables
Rate Limit: 20 connections/day
```

### Workflow 2: Connection Accepted → Intro Message
```yaml
Trigger: Connection request accepted
Wait: 48 hours
Check: No prior messages sent
Action: Send introduction message
Template: Personalized intro with value proposition
Rate Limit: 50 messages/day
```

### Workflow 3: No Reply → Email Escalation
```yaml
Trigger: LinkedIn message sent
Wait: 5 days
Check: No reply received
Action: Send email via Gmail
Template: Multi-touch email sequence
Integration: gmail-adapter
```

### Workflow 4: Warm Lead Identification
```yaml
Trigger: Multiple profile visits (3+ times)
Analysis: Engagement pattern recognition
Scoring: Lead qualification via lead-qualifier agent
Action: Add to high-priority outreach list
Notification: Alert to review prospect
```

### Workflow 5: Prospect Enrichment Pipeline
```yaml
Trigger: New prospect interaction
Step 1: Extract profile data from Lookback
Step 2: Enrich via Exa AI (company, tech stack, recent posts)
Step 3: Scrape additional data (GitHub, Twitter, personal site)
Step 4: Generate prospect intelligence report
Step 5: Store in CRM/database
```

## Data Schema

### Activities Table
```typescript
interface Activity {
  id: number;                          // Auto-increment ID
  timestamp: string;                   // ISO date string
  activity_type: 'profile_view' | 'connection_request' | 'message_sent';
  linkedin_url: string;                // Normalized LinkedIn URL
  profile_name: string;                // Full name
  headline: string;                    // LinkedIn headline
  current_title: string;               // Job title
  company: string;                     // Current company
  school: string;                      // Education
  location: string;                    // Geographic location
  connection_degree: '1st' | '2nd' | '3rd'; // Connection degree
  is_known_prospect: boolean;          // Matched from prospect list
  prospect_email: string | null;       // Email if known prospect
  metadata: {
    page_url: string;                  // Page URL when logged
    username: string;                  // LinkedIn username
  };
}
```

### Prospects Table
```typescript
interface Prospect {
  linkedin_url: string;                // Primary key
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  company: string;
  state: string;
  imported_at: string;                 // Import timestamp
  enriched_data?: {                    // Added by enrichment
    tech_stack?: string[];
    company_size?: string;
    funding_stage?: string;
    recent_posts?: Post[];
    github_url?: string;
    twitter_url?: string;
    personal_website?: string;
  };
}
```

## Scripts

### `sync-lookback-data.js`
Exports activity data from LinkedIn Lookback extension IndexedDB and imports into 10x-Team database.

**Usage:**
```bash
node .claude/skills/linkedin-lookback/scripts/sync-lookback-data.js
```

**Process:**
1. Connects to browser IndexedDB
2. Exports activities and prospects
3. Validates and normalizes data
4. Imports into 10x-Team database
5. Triggers workflow automations

### `enrich-prospects.js`
Enriches prospect data using Exa AI and other data sources.

**Usage:**
```bash
# Enrich specific profile
node .claude/skills/linkedin-lookback/scripts/enrich-prospects.js --url https://linkedin.com/in/john-doe

# Enrich all recent profiles
node .claude/skills/linkedin-lookback/scripts/enrich-prospects.js --recent 7d
```

**Process:**
1. Fetches profiles from database
2. Discovers company data via Exa AI
3. Scrapes additional sources (GitHub, Twitter)
4. Extracts tech stack, funding, team size
5. Generates prospect intelligence report
6. Updates database with enriched data

### `campaign-generator.js`
Creates automated outreach campaigns from Lookback activity data.

**Usage:**
```bash
# Create campaign from profile views
node .claude/skills/linkedin-lookback/scripts/campaign-generator.js --type profile_view

# Create campaign from specific company
node .claude/skills/linkedin-lookback/scripts/campaign-generator.js --company "Acme Corp"
```

**Process:**
1. Filters activities by criteria
2. Segments leads based on engagement
3. Generates personalized message templates
4. Creates campaign workflow
5. Sets up automation triggers
6. Configures rate limits and scheduling

### `interaction-checker.js`
Checks if you've previously interacted with a LinkedIn profile.

**Usage:**
```bash
node .claude/skills/linkedin-lookback/scripts/interaction-checker.js --url https://linkedin.com/in/jane-smith
```

**Output:**
```
Profile: Jane Smith (jane-smith)
Company: Acme Corp
Title: VP of Marketing

Previous Interactions:
  ✓ Profile view: 2026-01-15 (7 days ago)
  ✓ Profile view: 2026-01-10 (12 days ago)
  ✓ Connection request: 2026-01-16 (6 days ago)
  ✗ Message sent: Never

Recommendation: Connection pending - wait for acceptance before messaging
```

## Integration with 10x-Team Agents

### Lead Qualifier Agent
- Receives activity data from Lookback
- Scores leads based on engagement signals
- Identifies decision-makers and key stakeholders
- Prioritizes high-value prospects

### Attraction Specialist Agent
- Analyzes profile view patterns
- Identifies content that attracts target audience
- Optimizes LinkedIn presence for visibility
- Recommends content strategy

### Email Wizard Agent
- Triggered when LinkedIn messages go unanswered
- Creates email follow-up sequences
- Personalizes based on LinkedIn data
- Tracks multi-channel engagement

### Campaign Manager Agent
- Orchestrates multi-touch campaigns
- Coordinates LinkedIn + Email + Twitter outreach
- Monitors campaign performance
- Adjusts strategy based on metrics

### Funnel Architect Agent
- Maps LinkedIn activity to sales funnel
- Identifies conversion bottlenecks
- Optimizes engagement sequences
- Improves lead velocity

## Best Practices

### 1. **Respect LinkedIn Limits**
- Max 20 connection requests/day
- Max 50 messages/day
- Avoid aggressive automation
- Maintain human-like patterns

### 2. **Personalization is Key**
- Use profile data for context
- Reference shared connections
- Mention company/industry
- Show genuine interest

### 3. **Multi-Touch Strategy**
- Don't rely on single channel
- Combine LinkedIn + Email + Twitter
- Space out touchpoints (24-48h)
- Track response rates

### 4. **Data Privacy**
- All data stored locally
- No external servers
- User controls tracking
- GDPR compliant

### 5. **Quality over Quantity**
- Focus on high-value prospects
- Build genuine relationships
- Provide value first
- Track engagement quality

## Troubleshooting

### Extension Not Tracking
1. Check if extension is enabled: `chrome://extensions`
2. Verify tracking toggle is ON in extension popup
3. Refresh LinkedIn page
4. Check browser console for errors

### Sync Failing
1. Ensure extension is installed and active
2. Check IndexedDB browser permissions
3. Verify Node.js environment setup
4. Review sync script logs

### Automation Not Triggering
1. Confirm workflows are enabled
2. Check rate limits not exceeded
3. Verify integration credentials (Gmail, LinkedIn)
4. Review automation logs

## Security & Privacy

- ✅ All data stored locally in browser
- ✅ No external servers or third-party tracking
- ✅ User controls all data exports
- ✅ Can clear data anytime
- ✅ Does not read message content
- ✅ Only captures publicly visible profile data
- ✅ GDPR and privacy law compliant

## References

- [LinkedIn Lookback GitHub](https://github.com/kvivek0591/linkedin-lookback)
- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [LinkedIn Rate Limits](./references/linkedin-rate-limits.md)
- [Automation Best Practices](./references/automation-best-practices.md)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub issues: https://github.com/kvivek0591/linkedin-lookback/issues
3. Contact 10x-Team support
4. Consult automation logs

## Contributing

To contribute improvements:
1. Fork the LinkedIn Lookback repository
2. Create feature branch
3. Test thoroughly with 10x-Team integration
4. Submit pull request
5. Update documentation

## License

LinkedIn Lookback Extension: MIT License
10x-Team Integration: MIT License

---

**Last Updated:** 2026-01-22
**Version:** 1.0.0
**Status:** Production Ready
