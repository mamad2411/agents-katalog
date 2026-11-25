---
name: out-of-scope-request-handling
description: When the user wants to build or improve a sales bot's ability to gracefully redirect when prospects ask about unrelated things. Also use when the user mentions "off-topic handling," "out of scope," "unrelated questions," "scope boundaries," or "request redirection."
---

# Out-of-Scope Request Handling

You are an expert in building graceful redirection for sales bots. Your goal is to help developers create bots that handle off-topic requests professionally while maintaining conversation momentum.

## Types of Out-of-Scope Requests

### Support Questions
```
"How do I reset my password?"
"My account isn't working"
"I need help with a feature"

→ Route to support
```

### Unrelated Products/Services
```
"Do you sell office furniture too?"
"Can you help me find a plumber?"
"What's the weather like today?"

→ Clarify scope, redirect gracefully
```

### Inappropriate Requests
```
- Personal information requests
- Illegal activities
- Harassment
- Spam/scam attempts

→ Firm boundary, potential block
```

### Competitor Information
```
"Can you tell me about [Competitor]?"
"Do you know what [Competitor] charges?"

→ Redirect to your value
```

### Career/Non-Sales
```
"Are you hiring?"
"Can I speak to your CEO?"
"What's your company's revenue?"

→ Redirect to appropriate channel
```

## Response Framework

### The REDIRECT Method
```
R - Recognize the request
E - Empathize (don't dismiss)
D - Decline gracefully
I - Indicate the right resource
R - Return to conversation
E - Ensure satisfaction
C - Continue momentum
T - Track for patterns
```

## Handling Specific Scenarios

### Support vs. Sales
```
Prospect: "I'm having trouble logging into my account"

Response:
"I'm actually on the sales team, so I'm not the best
person to help with account issues. But I can definitely
get you to someone who can!

Our support team is super responsive—you can reach them
at support@company.com or through the help button in the app.

While they sort that out, was there anything sales-related
I could help with?"
```

### Unrelated Requests
```
Prospect: "Can you recommend a good restaurant nearby?"

Response:
"Ha! I wish I could help, but I'm just here for [product]
questions. Google or Yelp would probably serve you better there!

Back to [product]—any questions I can actually answer?"
```

### Beyond Bot Scope (But In Company Scope)
```
Prospect: "I want to negotiate my contract terms"

Response:
"Contract negotiations are definitely something we can
help with—but I'll need to bring in someone with the
right authority for that conversation.

Can I have our account manager reach out? They can
discuss terms and make sure we structure something
that works for you."
```

### Competitor Information
```
Prospect: "What does [Competitor] charge?"

Response:
"I actually don't have details on their pricing—I focus
on knowing our product inside and out.

What I can tell you is how we price and what you get
for it. Would that be helpful? Then you'd have solid
info to compare with whatever they quote you."
```

### Inappropriate Requests
```
Prospect: [Inappropriate message]

Response:
"I'm here to help with [product/service] questions.
If there's something I can help you with in that area,
let me know."

[If continues]
"I don't think I'm the right resource for you.
I'm going to close out this conversation."

→ Log and potentially block
```

## Graceful Redirection Patterns

### The Bridge Back
```
Acknowledge → Redirect → Bridge

"That's outside what I can help with directly,
BUT I can point you to [resource].
Meanwhile, you mentioned [earlier topic]—should
we pick up there?"
```

### The Helpful Boundary
```
"I'm specifically here to help with [scope].
For [their request], [alternative resource] would
be your best bet.

Is there anything [scope-related] I can help with?"
```

### The Positive Deflection
```
"Great question, just not my area of expertise!
I'm all about [your scope].

For [their topic], I'd recommend [resource].
Anything [scope-related] on your mind?"
```

## Resource Routing

### Build a Routing Map
```
Request Type → Destination
────────────────────────────────────
Support issues → support@company.com
Billing questions → billing@company.com
Partnership inquiries → partnerships@company.com
Press/media → pr@company.com
Careers → careers.company.com
Legal/contracts → legal@company.com
Executive requests → Escalation queue
General inquiries → info@company.com
```

### Smart Routing Response
```
Detect request type → Pull appropriate routing

"For [billing questions], our billing team is the best
resource: billing@company.com or call 1-800-XXX-XXXX.

They're available [hours] and usually respond within
[timeframe]."
```

## Maintaining Momentum

### Don't Let Off-Topic Derail
```
Bad:
Prospect: "What's your refund policy?"
Bot: [Answers in detail]
...conversation dies

Good:
Prospect: "What's your refund policy?"
Bot: "Good question—I'll make sure you get those details.
Quick answer: 30-day money-back guarantee, no questions asked.
Our support team (support@email) can give you the fine print.

Now, back to your team's needs—you mentioned wanting
to see how [feature] works. Want me to show you?"
```

### Queue Non-Blocking Requests
```
"I've noted your question about [off-topic thing].
I'll make sure the right person follows up on that.

For now, shall we continue where we left off?"
```

## Tracking Out-of-Scope

### Log Patterns
```
Track:
- What off-topic requests come up frequently
- Where in conversation they occur
- Who asks them (new vs. existing customers)
- How you handled them
- Did conversation continue after

Analyze for:
- Missing information on website
- Training gaps
- Product/service gaps
- Routing improvement opportunities
```

### Feedback Loop
```
High-frequency off-topic questions might indicate:
- Need for FAQ/self-service content
- Need for clearer scope communication
- Need for additional bot capabilities
- Need for product changes
```

## Boundaries Configuration

### Define Clear Scope
```
IN_SCOPE = [
    "product information",
    "pricing questions",
    "demo scheduling",
    "feature comparisons",
    "implementation questions",
    "qualification questions"
]

OUT_OF_SCOPE = [
    "technical support",
    "billing/payment issues",
    "account management",
    "legal questions",
    "HR/careers",
    "unrelated topics"
]

ESCALATE = [
    "complaints",
    "contract negotiations",
    "executive requests",
    "press inquiries"
]
```

### Flexibility Guidelines
```
Hard boundaries:
- Support issues → Always redirect
- Legal questions → Always redirect
- Inappropriate → Always block

Soft boundaries:
- Quick factual answers → May provide if simple
- Related tangents → May engage briefly
- Clarifying questions → May answer contextually
```
