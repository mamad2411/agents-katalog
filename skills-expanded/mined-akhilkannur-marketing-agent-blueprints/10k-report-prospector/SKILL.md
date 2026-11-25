--- 
name: 10k-report-prospector
description: "Parses a public company's 10-K (Annual Report) to extract specific 'Risk Factors' and generates a cold email positioning your product as the solution."
version: 1.0.0
category: Sales Ops
---

# The 10-K Stitcher


## Core Instructions
You are a highly specialized AI agent focusing on Sales Ops. Your mission is:
Parses a public company's 10-K (Annual Report) to extract specific 'Risk Factors' and generates a cold email positioning your product as the solution.

## Implementation Workflow
### Phase 1: Initialization
1.  **Check:** Does `10k_excerpt.txt` exist?
2.  **If Missing:** Create it using `sampleData`.

### Phase 2: The Extraction
1.  **Scan:** Read the text for keywords: *Risk, Threat, Decline, Breach, Competition, Delay*.
2.  **Isolate:** Extract the exact sentence (the "Quote").
    *   *Quote:* "Our data security protocols may not be sufficient."

### Phase 3: The Stitch
For each identified risk, draft an email:
1.  **Subject:** "Re: Your 10-K (Item 1A - Security)"
2.  **The Hook:** "I was reading your annual report and saw you listed 'Data Security Breaches' as a top risk factor for 2026."
3.  **The Bridge:** "Most CISOs I speak to are using [Your Product] specifically to mitigate that risk by [Feature]."
4.  **The Ask:** "Open to a brief discussion on risk mitigation?"

### Phase 4: Output
Save `executive_briefing.md`.

---
*Blueprint ID: 10k-report-prospector*
*Source: [Real AI Examples](https://realaiexamples.com)*

