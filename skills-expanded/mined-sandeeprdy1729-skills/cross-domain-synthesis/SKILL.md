---
name: cross-domain-synthesis
description: >
  Cross-domain synthesis skill. Combines knowledge from completely different fields
  to generate novel, practical insights — not analogies for their own sake, but
  structural borrowings where the mechanism in domain A directly solves the problem
  in domain B. Activates when the user wants unconventional approaches, is stuck
  in their domain's standard thinking, or explicitly wants to borrow from another
  field. Finds the structural isomorphism — not just a surface metaphor.
  Use when user says: cross-domain, think outside my field, what would X think,
  borrow from another discipline, combine these fields, unconventional approach,
  think like a biologist / game designer / architect, apply X to Y, what does
  another field say about this, novel approach, think differently, synthesize across
  domains, first principles from another field.
  Do NOT activate for: domain-specific questions where conventional expertise
  is what the user actually needs, requests that are already cross-domain framed.
  First response: "Cross-Domain Synthesis active. Describe your problem. I'll
  identify which domains have solved structurally similar problems and extract
  mechanisms you can actually apply."
license: Apache 2.0
---

# Cross-Domain Synthesis

"Think outside the box" is the most useless advice in problem-solving. It says
where not to look, not where to look.

Cross-domain synthesis is specific: find the field that has already solved your
problem under a different name, extract the mechanism (not the metaphor), and
apply it directly. Evolutionary biology solved distributed consensus before computer
science named it. Game design solved engagement loops before B2B SaaS needed them.
Urban planning solved pedestrian throughput before stadium architects did.

The skill is knowing which domain to borrow from and how to transplant the mechanism
without losing its function in translation.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/synthesize <problem>` | Find the domains that have solved this problem and extract mechanisms |
| `/map <domain>` | Map a specific domain's core mechanisms to the user's problem space |
| `/bridge <domain-a> <domain-b>` | Find structural isomorphisms between two domains |
| `/mechanism <name>` | Extract a specific mechanism from its source domain for application |
| `/rotate <problem>` | Reframe the problem using 5 different domain lenses |
| `/apply <mechanism> <context>` | Apply a specific borrowed mechanism to the current context |
| `/tension` | Find where the borrowed mechanism breaks down in the new domain |
| `/combine <domain-a> <domain-b> <problem>` | Force-combine two domains' approaches to a single problem |
| `/invert` | Ask what the opposite of the standard approach in this domain looks like |
| `/analogize <a> <b>` | Find structural analogies between two concepts, explicit about where they break |

---

## HIGH-LEVEL WORKFLOW

```text
User describes a problem
    │
    ├─ Phase 1: Problem Abstraction
    │     Strip the problem to its structural essence, removing domain-specific language
    │
    ├─ Phase 2: Domain Matching
    │     Identify fields that have solved the structural problem
    │
    ├─ Phase 3: Mechanism Extraction
    │     Pull the specific mechanism, not just the analogy
    │
    ├─ Phase 4: Translation
    │     Map the mechanism to the user's domain explicitly
    │
    ├─ Phase 5: Tension Analysis
    │     Find where the transplant breaks down — what doesn't transfer
    │
    └─ Phase 6: Application Design
          Design the concrete application in the user's domain
```

---

## PHASE 1 — PROBLEM ABSTRACTION

Domain-specific language conceals structural patterns. Strip it.

### Abstraction process

1. **Identify the core tension.** What two forces are in conflict? (e.g., speed vs. reliability, individual autonomy vs. collective coordination)
2. **Name the structural type.** What class of problem is this?
3. **State the constraint.** What can't change?
4. **State the success condition.** What does solved look like at the structural level?

### Problem type taxonomy

| Structural type | Domain-neutral description | Example domains with solutions |
| --- | --- | --- |
| **Coordination** | Many agents must reach consistent state without central control | Distributed systems, evolutionary biology, urban planning, labor organizing |
| **Allocation** | Scarce resources must be distributed among competing demands | Economics, ecology, immune systems, operating systems |
| **Signal/noise** | Meaningful signal must be extracted from high-noise environment | Neuroscience, radar, epidemiology, financial markets |
| **Trust under adversarial conditions** | Cooperation must be maintained when defection is possible | Game theory, evolutionary biology, cryptography, international relations |
| **Complexity management** | A system must remain comprehensible as it grows | Architecture, linguistics, software engineering, organizational design |
| **Feedback and stability** | A system must self-correct without overcorrecting | Control systems, ecology, macroeconomics, immune response |
| **Emergence** | Macro-patterns must arise from micro-interactions | Statistical mechanics, urban design, market design, cellular biology |
| **Exploration vs. exploitation** | Resources must be split between exploiting known solutions and finding better ones | Evolutionary strategy, clinical trials, venture capital, foraging theory |

### Abstraction output format

```text
PROBLEM ABSTRACTION

Domain-specific statement: [user's original problem]

Structural type: [from taxonomy]
Core tension: [force A] vs. [force B]
Constraint: [what cannot change]
Success condition: [what solved looks like structurally]

Domain-neutral restatement:
"How do you [achieve X] when [constraint] while [tension exists]?"
```

---

## PHASE 2 — DOMAIN MATCHING

Given the domain-neutral problem, find fields where this has been solved.

### Domain matching rules

1. **Match on mechanism, not metaphor.** "A company is like an organism" is a metaphor. "Both face the exploration-exploitation tradeoff and solve it with differentiated subunits" is a mechanism.
2. **Prefer unexpected domains.** The user's adjacent domains are already known to them. Reach further.
3. **Require the domain to have operationalized a solution** — not just conceptualized the same problem.
4. **Rank by transplantability**: how many constraints need to change for the mechanism to work in the new domain?

### Domain catalog (non-obvious cross-domain sources)

| When you have this problem... | Look at these domains |
| --- | --- |
| Distributed consensus | Swarm intelligence, mycorrhizal networks, immune system coordination |
| User engagement / retention | Behavioural ecology (foraging), casino design, social grooming in primates |
| Information overload | Sensory filtering in neuroscience, editorial curation, oral traditions |
| Organizational scaling | Urban planning (street grids), military logistics, mycelium networks |
| Trust in anonymous systems | Medieval merchant guilds, reputation markets, biological signaling theory (handicap principle) |
| Preventing cascade failures | Power grid design, pandemic modeling, forest fire management |
| Quality without central enforcement | Evolutionary fitness, peer review, immune self-tolerance |
| Pricing and incentive design | Auction theory, ecological niche theory, mechanism design |
| Technical debt | Archaeological stratigraphy, urban blight cycles, deferred immune response |
| Cold start / network effects | Invasion ecology, language spread, Schelling point theory |

---

## PHASE 3 — MECHANISM EXTRACTION

A mechanism is a causal process that produces a result. An analogy is not a mechanism.

### Mechanism extraction format

```text
MECHANISM: [name]
Source domain: [field]
Problem it solves: [domain-neutral description]

How it works:
  1. [Step 1 — causal description]
  2. [Step 2 — causal description]
  3. [Step 3 — causal description]

Key conditions for it to work:
  · [condition 1]
  · [condition 2]

What it produces:
  [The output / result of the mechanism]

Where it breaks down (in its source domain):
  [Failure conditions in the original domain]
```

### Mechanism quality test

A mechanism is extractable if:
- You can describe each step without using domain-specific vocabulary
- You can state what inputs the mechanism requires
- You can state what outputs it produces
- You can state the conditions under which it fails

If you can't do all four, you have an analogy, not a mechanism. Go deeper.

---

## PHASE 4 — TRANSLATION

Map the extracted mechanism to the user's domain.

### Translation format

```text
TRANSLATION: [mechanism] → [user's domain]

Mechanism component → User domain equivalent:
  [Agent/entity in source] → [equivalent in user's domain]
  [Resource in source]    → [equivalent in user's domain]
  [Feedback signal]       → [equivalent in user's domain]
  [Selection pressure]    → [equivalent in user's domain]

Translated mechanism:
  "In [user's domain], this means: [1–3 sentences, concrete]"

Required conditions in user's domain:
  · [condition 1 — does it exist?]
  · [condition 2 — does it exist?]

What the user must provide / create:
  · [what doesn't yet exist in user's domain that the mechanism requires]
```

---

## PHASE 5 — TENSION ANALYSIS

Mechanisms don't transplant perfectly. Name where the import breaks.

### Tension types

| Tension type | Example |
| --- | --- |
| **Missing prerequisite** | Evolutionary selection requires reproduction — what's the equivalent? |
| **Timescale mismatch** | Ecological succession takes centuries; the startup doesn't have that |
| **Resource mismatch** | The mechanism requires a resource the domain doesn't have (energy, information, slack) |
| **Incentive inversion** | In source domain, the mechanism works because agents benefit from compliance. In target domain, they benefit from defection. |
| **Observability gap** | The mechanism requires feedback signals the user's domain can't measure |
| **Ethical constraint** | The mechanism works in source domain but raises problems in human contexts |

### Tension format

```text
TRANSPLANT TENSIONS

Tension 1: [type]
  Description: [what breaks]
  Severity: [blocks mechanism / requires modification / minor workaround]
  Resolution: [how to adapt the mechanism to work despite this tension]

Tension 2: ...

Net verdict: [fully transplantable / needs adaptation / inspirational only]
```

---

## PHASE 6 — SYNTHESIS OUTPUT FORMAT

When `/synthesize` is called, deliver:

```text
CROSS-DOMAIN SYNTHESIS: [user's problem]

STRUCTURAL TYPE: [problem class]

─── SOURCE DOMAIN 1: [name] ────────────────────────────────
Mechanism: [name]
Why it applies: [1 sentence]
Translated: [2–3 sentences: what this means concretely for the user's problem]
Tension: [1 sentence: where it breaks]

─── SOURCE DOMAIN 2: [name] ────────────────────────────────
...

─── SYNTHESIS ───────────────────────────────────────────────
[If the mechanisms from multiple domains can be combined:]
Combined approach: [2–3 sentences: what using both looks like]

Most transplantable mechanism: [name]
Why: [1 sentence]
First concrete step to apply it: [1 sentence]
```
