---
name: prospect-research-integration
description: When the user wants to build or improve a sales bot's ability to enrich prospect data from multiple sources. Also use when the user mentions "prospect research," "data enrichment," "lead enrichment," "prospect intelligence," or "contact enrichment."
---

# Prospect Research Integration

You are an expert in building sales bots that automatically research and enrich prospect data from multiple sources. Your goal is to help developers create systems that gather intelligence to personalize outreach and qualify leads.

## Why Research Integration Matters

### The Data Gap
```
What you have:
- Name: John Smith
- Email: john@company.com
- Company: Acme Corp

What you need to personalize:
- Role and responsibilities
- Company initiatives
- Recent news/triggers
- Tech stack
- Pain points
- Budget authority
```

### With Research Integration
```
Auto-enriched profile:
- Title: VP of Engineering
- Reports to: CTO
- Team size: 45 engineers
- Recent: Announced series B
- Tech: AWS, React, Python
- Hiring: 12 open roles
- Trigger: New product launch

Now you can personalize.
```

## Data Source Integration

### Source Configuration
```python
class DataSourceManager:
    def __init__(self):
        self.sources = {}
        self.priority_order = []
        self.cache = ResearchCache()

    def register_source(self, source_id, source_config):
        self.sources[source_id] = {
            "connector": source_config["connector"],
            "data_types": source_config["data_types"],
            "rate_limit": source_config.get("rate_limit"),
            "cost_per_lookup": source_config.get("cost", 0),
            "reliability": source_config.get("reliability", 0.8)
        }

    def lookup(self, identifier, data_types_needed):
        """Lookup data from best available sources"""

        results = {}
        sources_used = []

        for data_type in data_types_needed:
            # Find best source for this data type
            source = self.find_best_source(data_type)
            if source:
                # Check cache first
                cached = self.cache.get(identifier, data_type, source)
                if cached and not cached.is_stale():
                    results[data_type] = cached.data
                else:
                    # Fetch fresh
                    data = self.fetch_from_source(source, identifier, data_type)
                    if data:
                        results[data_type] = data
                        self.cache.set(identifier, data_type, source, data)
                        sources_used.append(source)

        return {
            "data": results,
            "sources_used": sources_used,
            "completeness": len(results) / len(data_types_needed)
        }


# Source definitions
source_manager = DataSourceManager()

source_manager.register_source("clearbit", {
    "connector": ClearbitConnector(),
    "data_types": ["company_info", "contact_info", "tech_stack"],
    "rate_limit": 100,
    "cost_per_lookup": 0.10
})

source_manager.register_source("linkedin_api", {
    "connector": LinkedInConnector(),
    "data_types": ["contact_info", "work_history", "connections"],
    "rate_limit": 50,
    "cost_per_lookup": 0.05
})

source_manager.register_source("news_api", {
    "connector": NewsAPIConnector(),
    "data_types": ["company_news", "press_releases"],
    "rate_limit": 1000,
    "cost_per_lookup": 0.01
})
```

### Company Research
```python
def research_company(company_name, domain=None):
    """Gather comprehensive company intelligence"""

    research = {
        "basic_info": {},
        "financials": {},
        "tech_stack": {},
        "news": [],
        "hiring": {},
        "social": {}
    }

    # Basic company info
    basic = source_manager.lookup(
        domain or company_name,
        ["company_size", "industry", "location", "founded"]
    )
    research["basic_info"] = basic["data"]

    # Financial signals
    financials = gather_financial_signals(company_name)
    research["financials"] = {
        "funding": financials.get("recent_funding"),
        "revenue_estimate": financials.get("revenue"),
        "growth_signals": financials.get("growth_indicators")
    }

    # Technology stack
    tech = detect_tech_stack(domain)
    research["tech_stack"] = {
        "detected": tech["technologies"],
        "categories": categorize_tech(tech["technologies"]),
        "relevant_to_us": filter_relevant_tech(tech["technologies"])
    }

    # Recent news
    news = source_manager.lookup(company_name, ["company_news"])
    research["news"] = extract_relevant_news(news["data"], days=90)

    # Hiring signals
    hiring = scrape_job_postings(company_name, domain)
    research["hiring"] = {
        "total_openings": len(hiring),
        "by_department": group_by_department(hiring),
        "growth_areas": identify_growth_areas(hiring),
        "relevant_roles": filter_relevant_roles(hiring)
    }

    return research

def gather_financial_signals(company_name):
    """Gather financial intelligence"""

    signals = {}

    # Check for recent funding
    funding = lookup_crunchbase(company_name)
    if funding:
        signals["recent_funding"] = {
            "amount": funding.amount,
            "round": funding.round_type,
            "date": funding.date,
            "investors": funding.investors
        }

    # Check for IPO/acquisition news
    corporate_events = search_sec_filings(company_name)
    signals["corporate_events"] = corporate_events

    return signals
```

### Contact Research
```python
def research_contact(email=None, name=None, company=None, linkedin_url=None):
    """Gather comprehensive contact intelligence"""

    research = {
        "professional": {},
        "social": {},
        "activity": {},
        "connections": {}
    }

    # Professional info
    if linkedin_url:
        linkedin_data = scrape_linkedin_profile(linkedin_url)
        research["professional"] = {
            "current_role": linkedin_data.get("title"),
            "tenure": calculate_tenure(linkedin_data.get("start_date")),
            "previous_roles": linkedin_data.get("experience", [])[:3],
            "education": linkedin_data.get("education"),
            "skills": linkedin_data.get("skills", [])[:10]
        }

    # Enrich from data providers
    enriched = source_manager.lookup(
        email or linkedin_url,
        ["contact_info", "work_history"]
    )
    research["professional"].update(enriched.get("data", {}))

    # Social activity
    if linkedin_url:
        activity = get_linkedin_activity(linkedin_url)
        research["activity"] = {
            "recent_posts": activity.get("posts", [])[:5],
            "engagement_topics": extract_topics(activity),
            "content_style": analyze_content_style(activity)
        }

    # Mutual connections
    if company:
        research["connections"] = {
            "mutual_connections": find_mutual_connections(linkedin_url),
            "shared_groups": find_shared_groups(linkedin_url),
            "common_background": find_common_background(linkedin_url)
        }

    return research
```

## Trigger Event Detection

### Event Monitoring
```python
class TriggerEventMonitor:
    def __init__(self):
        self.event_types = [
            "funding_round",
            "executive_hire",
            "product_launch",
            "expansion",
            "acquisition",
            "partnership",
            "award",
            "earnings"
        ]

    def monitor_account(self, company, domain):
        """Set up monitoring for trigger events"""

        monitors = []

        # News monitoring
        monitors.append({
            "type": "news",
            "query": f'"{company}" OR site:{domain}',
            "frequency": "daily"
        })

        # Job posting monitoring
        monitors.append({
            "type": "jobs",
            "company": company,
            "frequency": "weekly"
        })

        # LinkedIn monitoring
        monitors.append({
            "type": "linkedin_company",
            "company": company,
            "track": ["posts", "employee_changes"]
        })

        return create_monitors(monitors)

    def process_event(self, event, account):
        """Process detected trigger event"""

        # Classify event
        event_type = classify_event(event)

        # Score relevance
        relevance = score_event_relevance(event, account)

        if relevance > 0.6:
            trigger = {
                "account_id": account.id,
                "event_type": event_type,
                "event_data": event,
                "relevance_score": relevance,
                "detected_at": datetime.now(),
                "recommended_action": get_recommended_action(event_type)
            }

            # Alert for high-priority triggers
            if relevance > 0.8:
                send_trigger_alert(trigger)

            return trigger

        return None


def classify_event(event):
    """Classify event into trigger category"""

    patterns = {
        "funding_round": [
            r"raised.*\$\d+",
            r"series [a-e]",
            r"funding round",
            r"investment from"
        ],
        "executive_hire": [
            r"(hired|appointed|named).*(?:CEO|CTO|VP|Director)",
            r"joins as",
            r"new (?:CEO|CTO|VP)"
        ],
        "product_launch": [
            r"launched",
            r"announces.*product",
            r"introduces",
            r"releases"
        ],
        "expansion": [
            r"expands to",
            r"opens.*office",
            r"enters.*market",
            r"international expansion"
        ]
    }

    for event_type, event_patterns in patterns.items():
        for pattern in event_patterns:
            if re.search(pattern, event.text, re.IGNORECASE):
                return event_type

    return "other"
```

## Data Synthesis

### Profile Builder
```python
class ProspectProfileBuilder:
    def __init__(self):
        self.research_sources = []

    def build_profile(self, prospect_input):
        """Build comprehensive prospect profile"""

        profile = ProspectProfile()

        # Research company
        company_research = research_company(
            prospect_input.company,
            prospect_input.domain
        )
        profile.company = company_research

        # Research contact
        contact_research = research_contact(
            email=prospect_input.email,
            name=prospect_input.name,
            company=prospect_input.company,
            linkedin_url=prospect_input.linkedin
        )
        profile.contact = contact_research

        # Find triggers
        triggers = find_recent_triggers(prospect_input.company)
        profile.triggers = triggers

        # Synthesize insights
        profile.insights = self.synthesize_insights(profile)

        # Score profile completeness
        profile.completeness_score = self.calculate_completeness(profile)

        return profile

    def synthesize_insights(self, profile):
        """Generate actionable insights from research"""

        insights = []

        # Company + contact alignment
        if profile.contact.get("professional", {}).get("tenure"):
            tenure = profile.contact["professional"]["tenure"]
            if tenure < 6:
                insights.append({
                    "type": "new_in_role",
                    "insight": f"Recently started ({tenure} months)",
                    "opportunity": "May be evaluating new tools"
                })

        # Growth signals
        if profile.company.get("hiring", {}).get("total_openings", 0) > 10:
            insights.append({
                "type": "high_growth",
                "insight": f"{profile.company['hiring']['total_openings']} open roles",
                "opportunity": "Scaling team, may need solutions"
            })

        # Funding trigger
        funding = profile.company.get("financials", {}).get("funding")
        if funding and days_since(funding["date"]) < 90:
            insights.append({
                "type": "recent_funding",
                "insight": f"Raised {funding['amount']} {funding['round']}",
                "opportunity": "Budget available for new initiatives"
            })

        # Tech stack fit
        tech = profile.company.get("tech_stack", {}).get("relevant_to_us", [])
        if tech:
            insights.append({
                "type": "tech_fit",
                "insight": f"Using {', '.join(tech[:3])}",
                "opportunity": "Good technical fit"
            })

        return insights
```

### Research Scoring
```python
def score_research_quality(profile):
    """Score the quality and completeness of research"""

    scores = {}

    # Contact completeness
    contact_fields = ["title", "tenure", "previous_roles", "linkedin_url"]
    contact_complete = sum(
        1 for f in contact_fields
        if profile.contact.get("professional", {}).get(f)
    )
    scores["contact"] = contact_complete / len(contact_fields)

    # Company completeness
    company_fields = ["size", "industry", "tech_stack", "funding"]
    company_complete = sum(
        1 for f in company_fields
        if profile.company.get(f) or profile.company.get("basic_info", {}).get(f)
    )
    scores["company"] = company_complete / len(company_fields)

    # Trigger freshness
    if profile.triggers:
        most_recent = max(t["detected_at"] for t in profile.triggers)
        days_old = (datetime.now() - most_recent).days
        scores["triggers"] = max(0, 1 - days_old / 90)
    else:
        scores["triggers"] = 0

    # Overall score
    scores["overall"] = (
        scores["contact"] * 0.3 +
        scores["company"] * 0.4 +
        scores["triggers"] * 0.3
    )

    return scores
```

## Caching & Freshness

### Research Cache
```python
class ResearchCache:
    def __init__(self):
        self.cache = {}
        self.freshness_rules = {
            "company_info": timedelta(days=30),
            "contact_info": timedelta(days=14),
            "tech_stack": timedelta(days=60),
            "news": timedelta(days=1),
            "hiring": timedelta(days=7)
        }

    def get(self, identifier, data_type, source):
        key = f"{identifier}:{data_type}:{source}"
        cached = self.cache.get(key)

        if cached:
            freshness_window = self.freshness_rules.get(
                data_type,
                timedelta(days=7)
            )
            is_stale = datetime.now() - cached["timestamp"] > freshness_window

            return CacheResult(
                data=cached["data"],
                is_stale=is_stale,
                age=datetime.now() - cached["timestamp"]
            )

        return None

    def set(self, identifier, data_type, source, data):
        key = f"{identifier}:{data_type}:{source}"
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now(),
            "source": source
        }
```

## Metrics

### Research Effectiveness
```
Track:
- Profile completeness rate
- Data freshness scores
- Source reliability rates
- Cost per enriched lead
- Research to conversion correlation

Optimize for:
- >80% profile completeness
- <7 day average data age
- Cost efficiency across sources
```

