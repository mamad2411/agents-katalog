# SALES_AGENTS.md

# Sales Agents Guidelines and Best Practices

## 1. Lead Discovery & Enrichment (Top of Funnel)

### Core Tools
- **CRM (System of Record)**: Use tools like Salesforce, HubSpot, or Pipedrive to maintain a single source of truth for contacts, companies, and deal stages.
- **Data Enrichment APIs**: Integrate with services like Clearbit, Apollo, or ZoomInfo to auto-fill firmographics, roles, tech stack, and buying signals.
- **Social + Web Signals**: Monitor LinkedIn scraping, job postings, funding news, and website changes for context on relevance and timing.

### AI Capabilities
- **ICP Matching & Lead Scoring**: Implement algorithms to match leads with Ideal Customer Profiles and score them based on potential value.
- **Auto-Qualification**: Automate the qualification process by assessing budget, authority, and timing.
- **Persona Inference**: Distinguish between decision-makers and influencers to tailor outreach effectively.

## 2. Outreach & Personalization (Prospecting)

### Core Tools
- **Email & Calendar Access**: Utilize Gmail or Outlook APIs for sending, reading, and scheduling emails autonomously.
- **Sequencing Tools**: Employ tools like Outreach or Salesloft to manage multi-touch, multi-channel follow-ups.
- **Website & Content Awareness**: Stay updated with blog posts, case studies, and pricing pages to enable hyper-personalized messaging.

### AI Capabilities
- **Personalized Cold Emails**: Craft emails that are specific to the recipient's role and pain points.
- **Dynamic Follow-Ups**: Implement follow-up strategies based on email opens and replies.
- **Objection-Aware Messaging Variants**: Prepare messaging that addresses common objections proactively.

## 3. Conversation & Qualification (Mid-Funnel)

### Core Tools
- **Chat Interface**: Use website chat, Slack, WhatsApp, or SMS to qualify leads in real-time.
- **Conversation Memory**: Leverage a vector database (e.g., Pinecone, Weaviate, FAISS) to maintain long-term context across interactions.
- **Call Transcription**: Optionally integrate with Zoom or Google Meet for transcribing calls to enhance analysis.

### AI Capabilities
- **Discovery Questioning**: Utilize frameworks like BANT or MEDDICC for effective lead qualification.
- **Intent Detection**: Implement systems to detect lead intent and qualify them accordingly.
- **Automatic Meeting Booking**: Facilitate seamless meeting scheduling or handoff to human agents.

## 4. Deal Support & Closing

### Core Tools
- **Proposal & Document Generation**: Use tools like Google Docs, PandaDoc, or Notion for generating tailored proposals instantly.
- **Pricing & CPQ Logic**: Implement a rules engine or CPQ system to prevent pricing errors.
- **Contract & E-Signature**: Utilize services like DocuSign or Stripe to streamline contract management and e-signatures.

### AI Capabilities
- **Proposal Personalization**: Tailor proposals based on industry or use case.
- **Objection Handling**: Prepare responses for common objections related to pricing or competitors.
- **Close-Readiness Detection**: Assess when a deal is ready to close based on various signals.

## 5. Intelligence, Feedback & Optimization (Post-Sale)

### Core Tools
- **Analytics & BI**: Use tools like Looker or Metabase to track conversion rates and identify drop-offs.
- **Conversation Intelligence**: Implement Gong-style analysis to learn which messages convert best.
- **Customer Success Signals**: Monitor usage data, NPS, and churn indicators to enable upsell and renewal opportunities.

### AI Capabilities
- **Win/Loss Analysis**: Analyze outcomes to understand what drives success or failure.
- **Messaging Optimization**: Continuously refine messaging strategies based on performance data.
- **Continuous Fine-Tuning**: Regularly update prompts and flows based on feedback and results.

## 6. Core “Glue” Tools (Non-Negotiable)

### Essential Tools
- **LLM (Reasoning + Generation)**: Utilize large language models for messaging and decision-making.
- **Workflow Orchestration**: Implement tools like Temporal, Zapier, or n8n for reliable multi-step actions.
- **Permissions & Guardrails**: Establish systems to prevent errors in emails and pricing.
- **Audit Logs**: Maintain logs for trust and compliance.
- **Human-in-the-Loop**: Ensure escalation processes for high-risk deals.

## Recommended MVP Tool Stack

If starting from scratch, consider the following lean but powerful tool stack:
- **CRM**: HubSpot or Salesforce
- **Email + Calendar API**
- **Data Enrichment API**
- **LLM + Prompt Framework**
- **Simple Workflow Orchestrator**
- **Vector Memory for Conversations**

This setup provides 70–80% of sales value with minimal complexity while allowing for future enhancements and polishing.