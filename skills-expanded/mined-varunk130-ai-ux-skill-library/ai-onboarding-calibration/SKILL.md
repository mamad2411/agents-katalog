---
name: ai-onboarding-calibration
description: 'Design onboarding experiences that help users build accurate mental models of AI capabilities, set expectations, and discover features progressively. Use when: AI onboarding, progressive disclosure for AI, capability communication, AI mental models, expectation setting, AI feature discovery, first-time AI user experience.'
---

# AI Onboarding & Calibration

Design first-time and ongoing experiences that help users understand what AI can and cannot do, build accurate expectations, and discover capabilities at the right pace. The CALIBRATE framework treats onboarding as a continuous calibration process, not a one-time tutorial.

## Core Principle

AI onboarding is fundamentally different from traditional software onboarding. In traditional software, features are deterministic - a button always does the same thing. In AI products, the same input can produce different outputs, capabilities have fuzzy boundaries, and what the AI "can do" depends on context. **You are not teaching features. You are calibrating a mental model.**

---

## The CALIBRATE Framework

| Letter | Principle | Design Question |
|---|---|---|
| **C** | Communicate Boundaries | Does the user know what the AI is and isn't good at? |
| **A** | Anchor with Examples | Have you shown, not told, what the AI can do? |
| **L** | Layer Complexity | Do simple use cases come first, with advanced capabilities revealed over time? |
| **I** | Invite Experimentation | Is there a safe, low-stakes way to explore what the AI can do? |
| **B** | Build Incrementally | Does the user's understanding deepen with each interaction? |
| **R** | Recalibrate After Failures | When the AI disappoints, does the onboarding help users adjust expectations? |
| **A** | Adapt to Expertise | Does the experience change based on the user's skill level? |
| **T** | Track Understanding | Can you measure whether users have an accurate mental model? |
| **E** | Evolve with the Product | When AI capabilities change, does the onboarding update? |

---

## The Mental Model Gap

The #1 onboarding failure in AI products: users arrive with the **wrong mental model.**

| Mental Model | What Users Expect | What Actually Happens | Design Intervention |
|---|---|---|---|
| **Omniscient AI** | AI knows everything, never wrong | AI has knowledge gaps and can hallucinate | Boundary disclosure: "I work best with X. I struggle with Y." |
| **Search Engine** | AI retrieves existing answers | AI generates novel responses (may be wrong) | Show that AI is creating, not retrieving: "Here's my analysis..." |
| **Human Assistant** | AI understands nuance, reads between lines | AI takes instructions literally | Teach prompting: show how specific instructions improve results |
| **Magic Tool** | One prompt = perfect output | Multiple iterations usually needed | Normalize iteration: "Let's refine this together" |
| **Infallible Calculator** | AI outputs are mathematically certain | AI outputs are probabilistic | Confidence indicators from the very first interaction |

---

## Progressive Disclosure Architecture

### The 3-Zone Model

Organize AI capabilities into three discovery zones:

| Zone | Content | Disclosure Trigger | Percentage of Capabilities |
|---|---|---|---|
| **Core Zone** | The 3-5 things the AI does best - the reason users signed up | Immediate - visible from first interaction | 20% of total capabilities |
| **Growth Zone** | Capabilities users discover through use - "oh, it can do THAT too?" | Contextual - surface when user behavior suggests readiness | 50% of total capabilities |
| **Power Zone** | Advanced features for expert users - complex prompts, system config, integrations | Intentional - user seeks them out, or after demonstrated mastery | 30% of total capabilities |

### Disclosure Triggers

| Trigger Type | Example | Best For |
|---|---|---|
| **Usage milestone** | After 10 conversations: "Did you know you can create custom templates?" | Growth Zone features |
| **Behavioral signal** | User manually repeats a task: "You do this often - want to automate it?" | Power Zone features |
| **Contextual relevance** | User uploads a PDF: "I can also summarize this and extract key points" | Growth Zone features |
| **Failure moment** | User's prompt produces poor results: "Try structuring your request like this for better results" | Prompting education |
| **Time-based** | After 1 week: "Here's what other users find helpful at this stage" | General capability awareness |

---

## The Sandbox Pattern

Before users commit to real tasks, offer a zero-risk exploration environment.

### Sandbox Design Principles

| Principle | Implementation |
|---|---|
| **No real consequences** | Sandbox actions don't affect real data, send real emails, or cost real money |
| **Pre-loaded scenarios** | Provide 3-5 example prompts that showcase different capabilities |
| **Instant gratification** | First sandbox interaction should produce an impressive result in under 10 seconds |
| **Bridge to reality** | Clear path from sandbox to real use: "Ready to try this with your own data?" |
| **Replayable** | Users can return to the sandbox anytime to test new capabilities safely |

---

## First-Interaction Design

The first interaction with an AI product determines whether users come back. Design it deliberately.

### The First 60 Seconds

| Second | What Should Happen | Anti-Pattern |
|---|---|---|
| 0-10 | User understands what to do (single, clear call to action) | A blank chat box with no guidance |
| 10-20 | User takes their first action (types a prompt, selects an option) | A 5-screen tutorial carousel |
| 20-40 | AI produces a visually impressive, useful result | A loading spinner followed by a wall of text |
| 40-60 | User sees a clear path to do it again or try something different | "Is there anything else?" with no suggestions |

### Starter Prompt Patterns

| Pattern | How It Works | Example |
|---|---|---|
| **Fill-in-the-blank** | Template with one variable the user customizes | "Help me write a [type of document] about [topic]" |
| **Choose-your-adventure** | 3-4 clickable starting scenarios | "Analyze data" / "Write content" / "Research a topic" |
| **Show-don't-tell** | Pre-run a demo query with real results visible | "Here's what I did with a sample dataset - try your own" |
| **Mirror the user** | Use onboarding data to personalize the first prompt | "Since you're in marketing, try: 'Create a campaign brief for...'" |

---

## Capability Boundary Communication

### The Can / Might / Can't Framework

For every AI product, maintain a public capability map:

| Category | What to Communicate | Example |
|---|---|---|
| **Can** (reliable) | Tasks the AI consistently does well | "I can summarize documents, translate text, and answer questions about your data." |
| **Might** (variable) | Tasks the AI can attempt but with inconsistent quality | "I can try generating code, but always review the output before running it." |
| **Can't** (limitation) | Tasks the AI should not be used for | "I can't access real-time data, make legal determinations, or guarantee numerical accuracy." |

**Placement:** This map should be accessible (not hidden in a help doc) but not intrusive (not a modal on every session). Best pattern: a collapsible "What I'm good at" panel accessible from the main interface.

---

## Recalibration After Failure

When the AI produces a bad output, the onboarding isn't over - it's entering a critical phase.

### The Recalibration Flow

| Step | Action | User Experience |
|---|---|---|
| 1 | **Acknowledge the failure** | "That wasn't a great answer. Here's why it happened." |
| 2 | **Explain the limitation** | "I'm less reliable with [specific task type] because [honest reason]." |
| 3 | **Teach a workaround** | "For better results with this type of question, try [technique]." |
| 4 | **Update the mental model** | Move this capability from "Can" to "Might" in the user's understanding |
| 5 | **Offer a quick win** | Immediately follow with something the AI does well to restore confidence |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Feature tour on first login | Nobody reads 7-screen tutorials. They want to DO something |
| "AI can do anything" messaging | Creates omniscience mental model → guaranteed disappointment |
| Identical onboarding for all users | A developer and a marketer need completely different first interactions |
| Hiding limitations in fine print | Users discover limitations through failure, not footnotes → trust damage |
| No onboarding for capability updates | Users don't know the AI got better → they avoid features that now work well |
| Treating prompting skill as the user's problem | "You need to learn better prompts" = "Our UX failed" |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design onboarding for new AI product | Full CALIBRATE framework | 3-Zone capability map + first 60-second flow + sandbox |
| Fix "users don't know what it can do" | Capability Boundary (Can/Might/Can't) | Public capability map with access pattern |
| Reduce first-session abandonment | First 60 Seconds template | Redesigned first interaction with starter prompts |
| Handle post-failure trust recovery | Recalibration Flow | 5-step recovery sequence |
| Design for different user expertise | Adapt to Expertise principle | Expertise-aware onboarding branching |

## Integration

Works with: `ai-prompt-ux` (teaching users to prompt effectively), `ai-error-resilience` (recovering from onboarding-phase failures), `ai-conversation-architect` (first conversation design), `ai-trust-transparency` (building initial trust).
