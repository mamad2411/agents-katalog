---
name: meta_ecosystem_omniscient_master
description: META ECOSYSTEM OMNISCIENT MASTER
---

# META ECOSYSTEM OMNISCIENT MASTER

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **META ECOSYSTEM OMNISCIENT MASTER**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/win claude/META_ECOSYSTEM_OMNISCIENT_MASTER.md`

## 🧠 Master Agent Prompt & Capabilities

# META ECOSYSTEM OMNISCIENT MASTER
# RJ Business Solutions — Complete Facebook/Instagram/WhatsApp/Messenger Platform Intelligence
# Created: July 2026 | Version: 1.0

---

## PART 1: OFFICIAL META DEVELOPER DOCUMENTATION HUB

### Core Portals
- Main Portal: https://developers.facebook.com/
- Graph API Overview: https://developers.facebook.com/docs/graph-api/overview
- Graph API Reference: https://developers.facebook.com/docs/graph-api/reference
- Graph Explorer: https://developers.facebook.com/tools/explorer/
- API Versioning: https://developers.facebook.com/docs/graph-api/guides/versioning
- Changelog: https://developers.facebook.com/docs/graph-api/changelog
- Rate Limiting: https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- Webhooks: https://developers.facebook.com/docs/graph-api/webhooks
- Batch Requests: https://developers.facebook.com/docs/graph-api/making-multiple-requests
- Permissions Reference: https://developers.facebook.com/docs/permissions/reference
- App Review: https://developers.facebook.com/docs/app-review

### Facebook Marketing API
- Marketing API: https://developers.facebook.com/docs/marketing-apis
- Campaign Structure: https://developers.facebook.com/docs/marketing-api/campaign-structure
- Ad Insights: https://developers.facebook.com/docs/marketing-api/insights
- Business Asset Management: https://developers.facebook.com/docs/marketing-api/business-asset-management
- Automated Ads: https://developers.facebook.com/docs/marketing-api/automated-ads-management
- Lead Ads API: https://developers.facebook.com/docs/marketing-api/guides/lead-ads
- Lead Ads Webhooks: https://developers.facebook.com/docs/marketing-api/guides/lead-ads/retrieving

### Official SDKs
- Python Business SDK: https://github.com/facebook/facebook-python-business-sdk (`pip install facebook-business`)
- Node.js Business SDK: https://github.com/facebook/facebook-nodejs-business-sdk (`npm install facebook-nodejs-business-sdk`)
- iOS SDK: https://github.com/facebook/facebook-ios-sdk
- Android SDK: https://github.com/facebook/facebook-android-sdk

---

## PART 2: MESSENGER PLATFORM — COMPLETE AUTOMATION

### Documentation
- Platform Overview: https://developers.facebook.com/docs/messenger-platform
- Send API: https://developers.facebook.com/docs/messenger-platform/reference/send-api
- Webhook Reference: https://developers.facebook.com/docs/messenger-platform/reference/webhook-events
- Messenger Profile API: https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api

### Message Types
- Quick Replies: https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
- Buttons: https://developers.facebook.com/docs/messenger-platform/send-messages/buttons
- Templates: https://developers.facebook.com/docs/messenger-platform/send-messages/templates
- Persistent Menu: https://developers.facebook.com/docs/messenger-platform/send-messages/persistent-menu
- Get Started Button: https://developers.facebook.com/docs/messenger-platform/discovery/welcome-screen
- Persona API: https://developers.facebook.com/docs/messenger-platform/send-messages/personas
- Customer Chat Plugin: https://developers.facebook.com/docs/messenger-platform/discovery/customer-chat-plugin
- Handover Protocol: https://developers.facebook.com/docs/messenger-platform/handover-protocol
- Built-in NLP: https://developers.facebook.com/docs/messenger-platform/built-in-nlp

### Messenger Webhook Handler (Node.js — Production Ready)
```javascript
const express = require('express');
const app = express();
app.use(express.json());

const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN;

// Webhook Verification
app.get('/webhook', (req, res) => {
  if (req.query['hub.verify_token'] === VERIFY_TOKEN) {
    res.send(req.query['hub.challenge']);
  } else {
    res.sendStatus(403);
  }
});

// Receive messages
app.post('/webhook', (req, res) => {
  const { object, entry } = req.body;
  if (object === 'page') {
    entry.forEach(event => {
      const messaging = event.messaging[0];
      if (messaging.message) {
        handleMessage(messaging.sender.id, messaging.message);
      }
    });
  }
  res.sendStatus(200);
});

// Send message
async function sendMessage(senderId, message) {
  await fetch(`https://graph.facebook.com/v18.0/me/messages?access_token=${PAGE_ACCESS_TOKEN}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient: { id: senderId }, message })
  });
}
```

---

## PART 3: INSTAGRAM API — COMPLETE BUSINESS AUTOMATION

### Documentation
- Graph API Overview: https://developers.facebook.com/docs/instagram-api
- Content Publishing: https://developers.facebook.com/docs/instagram-api/guides/content-publishing
- Media API: https://developers.facebook.com/docs/instagram-api/reference/ig-user/media
- Insights API: https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights
- Business Discovery: https://developers.facebook.com/docs/instagram-api/guides/business-discovery
- Hashtag Search: https://developers.facebook.com/docs/instagram-api/guides/hashtag-search
- Mentions: https://developers.facebook.com/docs/instagram-api/guides/mentions
- Comments Moderation: https://developers.facebook.com/docs/instagram-api/guides/comment-moderation
- Stories API: https://developers.facebook.com/docs/instagram-api/guides/stories

### Instagram Messaging API
- Messaging Overview: https://developers.facebook.com/docs/messenger-platform/instagram
- Instagram DMs: https://developers.facebook.com/docs/messenger-platform/instagram/features
- Ice Breakers: https://developers.facebook.com/docs/messenger-platform/instagram/features/ice-breakers
- Private Replies: https://developers.facebook.com/docs/messenger-platform/instagram/features/private-replies

---

## PART 4: WHATSAPP BUSINESS API — ENTERPRISE AUTOMATION

### Documentation
- Platform Overview: https://developers.facebook.com/docs/whatsapp
- Cloud API (Recommended): https://developers.facebook.com/docs/whatsapp/cloud-api
- Send Messages: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages
- Message Templates: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
- Webhooks: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks
- Media Messages: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media
- Interactive Messages: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#interactive-messages
- Phone Number Management: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers
- Commerce API: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/sell-products-and-services

### WhatsApp Cloud API Quick Start (Python)
```python
import requests

PHONE_NUMBER_ID = "your_phone_number_id"
ACCESS_TOKEN = "your_access_token"

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    return requests.post(url, headers=headers, json=data).json()
```

### BSP Partners
- 360Dialog: https://docs.360dialog.com/ | https://hub.360dialog.com/
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp

---

## PART 5: CLOUDFLARE WORKER — WEBHOOK INFRASTRUCTURE

### Central Webhook Handler (Complete Production Code)
```javascript
// Deploy at: workers.cloudflare.com
// Handles Messenger + Instagram + WhatsApp webhooks

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

const VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN_HERE';

async function handleRequest(request) {
  const url = new URL(request.url);

  // Webhook Verification (GET)
  if (request.method === 'GET') {
    const mode = url.searchParams.get('hub.mode');
    const token = url.searchParams.get('hub.verify_token');
    const challenge = url.searchParams.get('hub.challenge');
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      return new Response(challenge, { status: 200 });
    }
    return new Response('Forbidden', { status: 403 });
  }

  // Webhook Events (POST)
  if (request.method === 'POST') {
    const body = await request.json();
    if (body.object === 'page') {
      await handleMessengerWebhook(body);
    } else if (body.object === 'instagram') {
      await handleInstagramWebhook(body);
    } else if (body.object === 'whatsapp_business_account') {
      await handleWhatsAppWebhook(body);
    }
    return new Response('EVENT_RECEIVED', { status: 200 });
  }
}

async function handleMessengerWebhook(body) {
  for (const entry of body.entry) {
    for (const event of entry.messaging) {
      const senderId = event.sender.id;
      const message = event.message;
      if (message && message.text) {
        const keywordMatch = await checkKeywords(message.text);
        if (keywordMatch) {
          await triggerKeywordFlow(senderId, keywordMatch);
        } else {
          await triggerAIEnsemble(senderId, message.text);
        }
        await logInteraction(senderId, message.text);
      }
    }
  }
}

async function checkKeywords(text) {
  // Query Cloudflare D1 Database
  const keywords = await KEYWORD_DB.prepare(
    "SELECT * FROM keywords WHERE ? LIKE '%'||keyword||'%'"
  ).bind(text.toLowerCase()).all();
  return keywords.results.length > 0 ? keywords.results[0] : null;
}
```

### Cloudflare Resources
- Workers: https://developers.cloudflare.com/workers/
- D1 Database: https://developers.cloudflare.com/d1/
- KV Storage: https://developers.cloudflare.com/kv/
- Durable Objects: https://developers.cloudflare.com/durable-objects/
- Cron Triggers: https://developers.cloudflare.com/workers/configuration/cron-triggers/

---

## PART 6: D1 DATABASE SCHEMA (Complete)

```sql
-- Users Table
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT UNIQUE NOT NULL,
  platform TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  phone_number TEXT,
  email TEXT,
  lead_score INTEGER DEFAULT 0,
  idempotency_key TEXT UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Keywords Table
CREATE TABLE keywords (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword TEXT NOT NULL,
  intent TEXT NOT NULL,
  action TEXT NOT NULL,
  priority INTEGER DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Interactions Table
CREATE TABLE interactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT NOT NULL,
  message TEXT,
  response TEXT,
  intent TEXT,
  sentiment REAL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);

-- Conversations Table
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT NOT NULL,
  conversation_state TEXT DEFAULT 'active',
  current_flow TEXT,
  metadata TEXT,
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_interaction DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);

-- Leads Table
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT NOT NULL,
  lead_source TEXT,
  service_interest TEXT,
  qualification_score INTEGER,
  crm_synced BOOLEAN DEFAULT FALSE,
  crm_id TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);

-- Follow-Ups Table
CREATE TABLE follow_ups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT NOT NULL,
  scheduled_time DATETIME NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  retry_count INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);

-- Stripe Checkout Sessions
CREATE TABLE checkout_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id TEXT NOT NULL,
  stripe_session_id TEXT UNIQUE,
  product_id TEXT,
  amount INTEGER,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(sender_id)
);

-- Indexes
CREATE INDEX idx_users_sender ON users(sender_id);
CREATE INDEX idx_interactions_sender ON interactions(sender_id);
CREATE INDEX idx_keywords_keyword ON keywords(keyword);
CREATE INDEX idx_follow_ups_scheduled ON follow_ups(scheduled_time, status);
```

### Keyword Seed Data (All Niches)
```sql
-- Credit Repair
INSERT INTO keywords (keyword, intent, action, priority) VALUES
  ('credit', 'purchase', 'checkout', 1),
  ('score', 'purchase', 'checkout', 1),
  ('dispute', 'legal', 'legal_playbook', 2),
  ('collections', 'legal', 'legal_playbook', 2),
  ('bankruptcy', 'legal', 'legal_playbook', 2);

-- Real Estate
INSERT INTO keywords (keyword, intent, action, priority) VALUES
  ('buy', 'purchase', 'checkout', 1),
  ('sell', 'purchase', 'checkout', 1),
  ('property', 'info', 'ai_response', 2),
  ('mortgage', 'info', 'ai_response', 2),
  ('viewing', 'support', 'calendar_booking', 1);

-- Tax Services
INSERT INTO keywords (keyword, intent, action, priority) VALUES
  ('tax', 'purchase', 'checkout', 1),
  ('irs', 'legal', 'legal_playbook', 2),
  ('audit', 'legal', 'legal_playbook', 2),
  ('refund', 'info', 'ai_response', 3),
  ('filing', 'purchase', 'checkout', 1);

-- Insurance
INSERT INTO keywords (keyword, intent, action, priority) VALUES
  ('quote', 'purchase', 'checkout', 1),
  ('claim', 'support', 'ai_response', 2),
  ('policy', 'info', 'ai_response', 2),
  ('coverage', 'info', 'ai_response', 2);
```

---

## PART 7: KEYWORD TRIGGER ENGINE (Python — Production)

```python
# keyword_engine.py — FastAPI microservice, port 8001
from typing import Dict, Optional
import json

class KeywordTriggerEngine:
    def __init__(self, db_connection, ai_client):
        self.db = db_connection
        self.ai = ai_client

    async def analyze_message(self, message: str, sender_id: str) -> Dict:
        # Layer 1: Direct keyword match (fast)
        direct_match = await self.check_direct_keywords(message)
        if direct_match:
            return {
                'match_type': 'direct',
                'intent': direct_match['intent'],
                'action': direct_match['action'],
                'confidence': 1.0
            }
        # Layer 2: NLP intent classification
        intent = await self.classify_intent(message)
        # Layer 3: Context-aware (conversation history)
        context = await self.get_conversation_context(sender_id)
        enriched = await self.contextual_analysis(message, context)
        return {
            'match_type': 'nlp',
            'intent': enriched['intent'],
            'action': enriched['action'],
            'confidence': enriched['confidence'],
            'entities': enriched['entities']
        }

    async def classify_intent(self, message: str) -> str:
        """Intent categories: purchase_intent, information_seeking,
        support_request, legal_dispute, objection_handling, scheduling"""
        prompt = f"""Classify intent: "{message}"
        Categories: purchase_intent, information_seeking, support_request,
        legal_dispute, objection_handling, scheduling
        Respond with ONLY the category name."""
        response = await self.ai.messages.create(
            model="claude-opus-4-8",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
```

---

## PART 8: STRIPE CHECKOUT ENGINE

```javascript
// stripe_checkout_engine.js
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const PRODUCTS = {
  credit_repair:   { price_id: 'price_credit_monthly',      amount: 9900  },
  real_estate:     { price_id: 'price_re_consultation',      amount: 29900 },
  tax_filing:      { price_id: 'price_tax_standard',         amount: 14900 },
  insurance_quote: { price_id: 'price_insurance_free',       amount: 0     }
};

async function createCheckoutSession(senderId, serviceType) {
  const product = PRODUCTS[serviceType];
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: product.price_id, quantity: 1 }],
    mode: 'payment',
    success_url: `${process.env.BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.BASE_URL}/cancel`,
    client_reference_id: senderId,
    metadata: { sender_id: senderId, service_type: serviceType }
  });
  return session;
}
```

- Stripe Dashboard: https://dashboard.stripe.com/
- Checkout Docs: https://stripe.com/docs/payments/checkout
- Webhooks: https://stripe.com/docs/webhooks

---

## PART 9: MASTER EMPIRE AI ENSEMBLE

```python
# master_ai_ensemble.py — Multi-model consensus response
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

class MasterEmpireAIEnsemble:
    def __init__(self):
        self.claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.gemini = genai.GenerativeModel('gemini-pro')

    async def generate_response(self, message: str, context: dict, service_type: str) -> dict:
        # Get from all three models in parallel
        responses = await asyncio.gather(
            self.get_claude_response(message, context, service_type),
            self.get_gpt4_response(message, context, service_type),
            self.get_gemini_response(message, context, service_type)
        )
        # Synthesize best response
        final = await self.synthesize_responses(responses)
        return await self.apply_service_personality(final, service_type)

    async def apply_service_personality(self, response: dict, service: str) -> dict:
        personalities = {
            'credit_repair': { 'cta': '📊 Ready to see your free credit analysis?', 'emoji': '💪' },
            'real_estate':   { 'cta': '🏡 Want to schedule a property viewing?',    'emoji': '🏠' },
            'tax_services':  { 'cta': '📋 Ready to maximize your tax refund?',       'emoji': '💰' },
            'insurance':     { 'cta': '🛡️ Get your free quote in 2 minutes?',       'emoji': '✅' }
        }
        p = personalities.get(service, personalities['credit_repair'])
        response['text'] = f"{p['emoji']} {response['text']}\n\n{p['cta']}"
        return response
```

---

## PART 10: LEGAL DISPUTE PLAYBOOKS

### Credit Dispute Flow (FCRA-Compliant)
```python
async def credit_dispute_flow(context: dict) -> dict:
    steps = [
        {
            'step': 1,
            'message': 'I understand you want to dispute items on your credit report.\n\n'
                       '1. Which credit bureau? (Experian, Equifax, TransUnion)\n'
                       '2. What type of item? (Late payment, collection, charge-off)\n'
                       '3. Account name/creditor?',
            'collect': ['bureau', 'item_type', 'creditor']
        },
        {
            'step': 2,
            'message': 'Generating your dispute letter with:\n'
                       '✅ FCRA Section 609/611 language\n'
                       '✅ Documentation requests\n'
                       '✅ 30-day response deadline requirement',
        },
        {
            'step': 3,
            'message': '📄 Your dispute package is ready:\n'
                       '1. Dispute letter (PDF)\n'
                       '2. Mailing instructions\n'
                       '3. Tracking template\n'
                       '4. 30-day follow-up schedule',
        }
    ]
    return {'playbook': 'credit_dispute', 'steps': steps, 'legal_basis': 'FCRA 609/611'}
```

### FDCPA Violation Flow (Collection Harassment)
- Relevant statutes: 15 USC 1692, FDCPA Sections 806, 807
- Documents generated: Cease & Desist letter, CFPB complaint, State AG complaint

### Other Playbook Types
- `real_estate_contract` — Contract dispute documentation
- `tax_audit` — IRS audit response + representation guidance
- `insurance_claim_denial` — Claim denial appeal process

---

## PART 11: GOHIGHLEVEL CRM SYNC

```javascript
// gohighlevel_sync.js
const GHL_BASE = 'https://services.leadconnectorhq.com';

async function syncLead(leadData) {
  const contact = {
    firstName: leadData.first_name,
    lastName: leadData.last_name,
    email: leadData.email,
    phone: leadData.phone_number,
    source: 'Meta Messenger Bot',
    tags: [leadData.service_interest, `score_${leadData.lead_score}`, leadData.platform],
    customFields: [
      { key: 'sender_id',          value: leadData.sender_id },
      { key: 'lead_source_detail', value: 'Automated DM Campaign' },
      { key: 'qualification_score',value: String(leadData.lead_score) },
      { key: 'first_message',      value: leadData.first_message },
      { key: 'purchase_intent',    value: leadData.purchase_intent ? 'Yes' : 'No' }
    ]
  };
  const response = await fetch(`${GHL_BASE}/contacts/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.GHL_API_KEY}`,
      'Content-Type': 'application/json',
      'Version': '2021-07-28'
    },
    body: JSON.stringify(contact)
  });
  return response.json();
}

// Workflow map: service → GHL workflow ID
const WORKFLOW_MAP = {
  'credit_repair': 'workflow_credit_onboarding',
  'real_estate':   'workflow_property_consultation',
  'tax_services':  'workflow_tax_intake',
  'insurance':     'workflow_quote_generation'
};
```

- GHL API Docs: https://highlevel.stoplight.io/
- GHL Webhooks: https://highlevel.stoplight.io/docs/integrations/docs/webhooks.md

---

## PART 12: META MESSENGER API CLASS (Python — Multi-Channel)

```python
# meta_messenger.py — Handles Messenger, Instagram DMs, WhatsApp

class MetaMessengerAPI:
    def __init__(self, page_access_token: str):
        self.access_token = page_access_token
        self.base_url = 'https://graph.facebook.com/v18.0'

    async def send_text_message(self, recipient_id: str, text: str) -> dict:
        return await self._send({'recipient': {'id': recipient_id}, 'message': {'text': text}})

    async def send_quick_replies(self, recipient_id: str, text: str, quick_replies: list) -> dict:
        return await self._send({
            'recipient': {'id': recipient_id},
            'message': {'text': text, 'quick_replies': quick_replies}
        })

    async def send_button_template(self, recipient_id: str, text: str, buttons: list) -> dict:
        return await self._send({
            'recipient': {'id': recipient_id},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {'template_type': 'button', 'text': text, 'buttons': buttons}
                }
            }
        })

    async def send_generic_template(self, recipient_id: str, elements: list) -> dict:
        return await self._send({
            'recipient': {'id': recipient_id},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {'template_type': 'generic', 'elements': elements}
                }
            }
        })

    async def send_media(self, recipient_id: str, media_type: str, media_url: str) -> dict:
        return await self._send({
            'recipient': {'id': recipient_id},
            'message': {
                'attachment': {
                    'type': media_type,
                    'payload': {'url': media_url, 'is_reusable': True}
                }
            }
        })

    async def _send(self, payload: dict) -> dict:
        import aiohttp
        url = f"{self.base_url}/me/messages"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, params={'access_token': self.access_token}) as r:
                return await r.json()
```

---

## PART 13: AUTOMATED FOLLOW-UP SYSTEM (Hourly Cron)

```python
# cron_follow_ups.py — Runs hourly via Cloudflare Cron Triggers or schedule lib

class AutomatedFollowUpSystem:
    async def run_hourly_follow_ups(self):
        """Main cron job — every hour"""
        # Get pending follow-ups due now
        pending = await self.db.execute(
            "SELECT * FROM follow_ups WHERE status='pending' AND scheduled_time<=? ORDER BY scheduled_time ASC",
            (datetime.now().isoformat(),)
        )
        for fu in pending:
            await self.send_follow_up(fu)
        # Check stale (24h no response)
        await self.check_stale_conversations()
        # Re-engage cold (3d no response, score>50)
        await self.reengage_cold_leads()

    async def reengage_cold_leads(self):
        templates = {
            'credit_repair': "Hi {name}! 💳 We helped someone raise their score 120pts in 90 days. Want to see if we can do the same for you?",
            'real_estate':   "Hey {name}! 🏡 Market just shifted — now's a great time to buy. 3 new listings match your criteria.",
            'tax_services':  "Hi {name}! 📊 Tax season approaching fast. Average person overpays $1,000. Let's fix that.",
            'insurance':     "Hey {name}! 🛡️ Found you could save $400/year with better coverage. Want to see the comparison?"
        }
```

### Cron Deployment Options
- **Cloudflare Cron Triggers** (recommended): https://developers.cloudflare.com/workers/configuration/cron-triggers/
- **GitHub Actions** (free): `.github/workflows/follow-ups.yml` with `schedule: cron('0 * * * *')`
- **Railway Scheduler**: `schedule = "0 * * * *"`
- **Heroku Scheduler**: https://devcenter.heroku.com/articles/scheduler

---

## PART 14: NICHE DM CAMPAIGN TEMPLATES

### CREDIT REPAIR CAMPAIGN
```
Ad: "Increase Your Credit Score by 100+ Points"
Body: "Bad credit holding you back? 10,000+ helped. Click for FREE credit analysis."
CTA: "Send Message"

FLOW:
Step 1 → "What's your main goal?"
  Quick replies: Buy a house | Get car loan | Credit cards | Lower interest rates

Step 2 → [After selection] Collect: credit score (approx), collections Y/N, late payments Y/N

Step 3 → "Based on your situation, you qualify for our service!
  ✅ Dispute inaccurate items (avg 40% removal)
  ✅ Negotiate pay-for-delete
  ✅ Build positive payment history
  $99/month — cancel anytime. Ready to start?"
  Buttons: [Yes, Let's Do It! 💳] [Tell Me More] [Not Right Now]

Step 4a → Trigger Stripe checkout (credit_repair_monthly)
Step 4b → Stats + guarantee + "I'm Ready"
Step 4c → Capture email, schedule 3-day follow-up

Follow-up sequence: Day 1 (voice+text) → Day 3 (testimonial) → Day 7 (discount) → Day 14 (final)
```

### REAL ESTATE CAMPAIGN
```
Ad: "Your Dream Home is Waiting"
CTA: "Get Free Analysis"

BUY FLOW:
Collect: location/zip, budget, bedrooms, timeline
→ Send 3-card carousel of matching properties
→ Book viewings via Calendly

SELL FLOW:
Collect: address, bed/bath, sqft, upgrades
→ AI-generated CMA (estimated value, days on market)
→ "I can help you price/stage/market. Schedule consultation?"

Lead Scoring:
  Budget >$300K: +20pts | Timeline <6mo: +30pts | Pre-approved: +40pts
```

### TAX SERVICES CAMPAIGN
```
Ad: "Maximize Your Tax Refund — Average Client Gets $3,200 Back"

FLOW:
Step 1 → "Which describes you?"
  Quick replies: W-2 Employee | Self-Employed/1099 | Small Business | IRS Problems

W-2 Path: Collect filing status, own/rent, kids, student loans
1099/Biz Path: Collect biz type, revenue, recordkeeping status, quarterly estimates
IRS Path → Trigger legal playbook
  Collect: letter type, audit status, back taxes owed, years unfiled

Pricing:
  Simple W-2: $149 | 1099/Schedule C: $299
  Small Business: $499+ | IRS Resolution: $995+
  All include: audit protection, free amendments, year-round support
```

### INSURANCE CAMPAIGN
```
Ad: "Save $400/Year on Insurance — Free Quote in 2 Minutes"

FLOW:
Step 1 → Type: Auto | Home | Life | Health | Business
Step 2 → Collect coverage details, current provider, premium
Step 3 → AI comparison + savings estimate
Step 4 → Book call with licensed agent | Get instant quote link
```

---

## PART 15: FULL SYSTEM ARCHITECTURE

```
SYSTEM FLOW:
Hourly Cron → Send Follow-Ups
                    ↓
Meta Platform → Webhook Event
                    ↓
Cloudflare Worker (Central Hub)
         ┌──────────┬──────────┬──────────┐
         ↓          ↓          ↓          ↓
   Keyword      AI Ensemble  Lead       Bot Response
   Engine       (Claude+GPT  Details    Handler
   (port 8001)  +Gemini)     Capture    
         └──────────┴──────────┴──────────┘
                    ↓
            Message Router
       ┌────────────┼────────────┐
       ↓            ↓            ↓
  Stripe        Legal        GoHighLevel
  Checkout      Playbooks    CRM Sync
       └────────────┴────────────┘
                    ↓
            Meta Send API
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
 Messenger      Instagram      WhatsApp
    DMs            DMs           Cloud
```

### Environment Variables Required
```bash
PAGE_ACCESS_TOKEN=      # Meta Page Access Token
VERIFY_TOKEN=           # Your custom webhook verify string
ANTHROPIC_API_KEY=      # Claude API
OPENAI_API_KEY=         # GPT-4
GOOGLE_API_KEY=         # Gemini
STRIPE_SECRET_KEY=      # Stripe
GHL_API_KEY=            # GoHighLevel
GHL_PIPELINE_ID=        # GHL Pipeline ID
GHL_STAGE_NEW_LEAD=     # GHL Stage ID
ELEVENLABS_API_KEY=     # ElevenLabs Voice
BASE_URL=               # Your worker/server URL
```

---

## PART 16: OPEN-SOURCE FRAMEWORKS

### Messenger / Multi-Platform
- Bottender (Node.js): https://github.com/Yoctol/bottender — Messenger, WhatsApp, LINE, Telegram, Slack
- BotMan (PHP): https://github.com/botman/botman
- fbmessenger (Python): https://github.com/rehabstudio/fbmessenger

### WhatsApp Automation
- whatsapp-web.js: https://github.com/pedroslopez/whatsapp-web.js (15K+ stars, Node.js)
- Baileys (TypeScript): https://github.com/WhiskeySockets/Baileys

### Instagram Python
- instagrapi: https://github.com/adw0rd/instagrapi (`pip install instagrapi`)
- instaloader: https://github.com/instaloader/instaloader

---

## PART 17: DEPLOYMENT (Railway One-Click)

```yaml
# railway.toml
[[services]]
name = "webhook-worker"
source = "./cloudflare-worker"

[[services]]
name = "keyword-engine"
port = 8001
healthcheckPath = "/health"

[[services]]
name = "ai-ensemble"
port = 8002
healthcheckPath = "/health"

[[services]]
name = "cron-follow-ups"
schedule = "0 * * * *"

[env]
DATABASE_URL = "${{DATABASE_URL}}"
ANTHROPIC_API_KEY = "${{ANTHROPIC_API_KEY}}"
STRIPE_SECRET_KEY = "${{STRIPE_SECRET_KEY}}"
META_ACCESS_TOKEN = "${{META_ACCESS_TOKEN}}"
GHL_API_KEY = "${{GHL_API_KEY}}"
```

```bash
npm install -g @railway/cli
railway login
railway up
railway variables set ANTHROPIC_API_KEY=your_key
```

---

## PART 18: COMPLIANCE & POLICIES

- Platform Terms: https://developers.facebook.com/terms
- Platform Policy: https://developers.facebook.com/docs/development/policies
- Data Use Policy: https://www.facebook.com/privacy/policy/
- Automated Messages Policy: https://developers.facebook.com/docs/messenger-platform/policy-overview
- WhatsApp Commerce Policy: https://www.whatsapp.com/legal/commerce-policy
- WhatsApp Business Policy: https://www.whatsapp.com/legal/business-policy

### Key Compliance Notes
- Message 24-hour window rule for Messenger (standard messages)
- Must use approved Message Tags for out-of-window messaging
- WhatsApp templates require pre-approval by Meta
- TCPA compliance for SMS follow-ups (US)
- CAN-SPAM for email captures
- FDCPA / FCRA compliance for credit-related messaging

---

## PART 19: ANALYTICS & KPIs

```yaml
Response Metrics:
  - Average response time: <2 seconds
  - Message delivery rate: >99%
  - Webhook processing: <500ms

Engagement Metrics:
  - Conversation start rate: 40-60%
  - Conversation completion: 60-80%
  - Button click-through: 25-40%

Conversion Metrics:
  - Lead capture rate: 30-50%
  - Checkout initiation: 15-25%
  - Checkout completion: 60-80%
  - Cost per lead: $5-15
  - Cost per acquisition: $30-100

Business Metrics:
  - Average deal size: $500-2,000
  - Customer LTV: $2,000-5,000
  - ROI: 300-500%
  - Payback period: 30-60 days
```

### Analytics Tools
- Dashbot: https://www.dashbot.io/ (chatbot analytics)
- Chatbase: Conversational interface analytics
- Meta Page Insights API: https://developers.facebook.com/docs/graph-api/reference/insights

---

## PART 20: LEARNING ROADMAP

### Week 1: Foundation
- Meta Developer Account + App creation
- Facebook Page + Instagram Business Account
- Deploy Cloudflare Worker
- D1 Database setup + schema migration
- Test echo bot end-to-end

### Week 2: Core Features
- Keyword engine with D1 integration
- AI ensemble (Claude + GPT-4)
- Stripe checkout flow
- Basic message templates (quick replies, buttons, carousels)

### Week 3: Advanced Automation
- Legal playbook system
- GHL CRM integration + workflows
- ElevenLabs voice message generation
- Hourly follow-up cron
- Instagram + WhatsApp multi-channel support

### Week 4: Niche Campaigns
- Credit repair campaign
- Real estate campaign
- Tax services campaign
- Insurance campaign
- A/B test message variants

### Week 5-6: Scale
- Load testing
- Sentry monitoring + Cloudflare Analytics
- Rate limit handling
- Error recovery + dead letter queue
- Multi-region Cloudflare deployment

---

## PART 21: RJ BUSINESS SOLUTIONS — META STACK INTEGRATION

### RJ Tech Integration Points
- **Frontend**: Next.js 16.2 — webhook dashboard, conversation viewer, analytics
- **Backend**: Hono 4.12.23 on Cloudflare Workers — API proxy + streaming
- **DB**: Cloudflare D1 (edge) + Supabase (main CRM data)
- **AI**: Claude Opus 4.8 (ensemble lead) + GPT-4 (backup) + Gemini (consensus)
- **Voice**: ElevenLabs via `rj-elevenlabs-agent` — voice follow-ups, voice DMs
- **Payments**: Stripe (all checkout sessions)
- **CRM**: GoHighLevel (all leads synced)
- **Memory**: @rj/memory Layer 03 Semantic — store conversation facts per lead
- **Queue**: Cloudflare Queues for async follow-up processing

### RJ Service → Meta Campaign Mapping
| Service | Ad Objective | CTA | Checkout Product |
|---------|-------------|-----|-----------------|
| Custom AI Agent Dev ($15K-$50K) | Lead Generation | "Book Strategy Call" | calendar_booking |
| Multi-Agent Orchestration ($75K-$250K) | Lead Generation | "Get Custom Quote" | quote_form |
| Enterprise Agent Platform ($250K-$1M+) | Lead Generation | "Schedule Enterprise Demo" | calendar_booking |
| Agent Consulting ($10K-$35K) | Messages | "Start Free Audit" | checkout |
| Agent Training ($5K-$25K/cohort) | Messages | "Reserve Your Spot" | checkout |

---

*META_ECOSYSTEM_OMNISCIENT_MASTER.md | RJ Business Solutions | July 2026*
*Covers: Messenger + Instagram + WhatsApp + Meta Ads + Cloudflare Workers + D1 + Stripe + GHL CRM*
*Niche campaigns: Credit Repair, Real Estate, Tax Services, Insurance, AI Services*

