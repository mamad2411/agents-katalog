---
name: patent-research
description: "When to activate: patent research, prior art search, freedom to operate, patent landscape, USPTO, EPO, WIPO, patent claims analysis, IP strategy, patent filing"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: research
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Patent Research Patterns

## Patent Databases

### Primary Databases
| Database | Coverage | Best For |
|----------|----------|---------|
| **USPTO Patent Full-Text** | US patents 1976+ | US-only prior art |
| **Google Patents** | Global, 120M+ documents | Quick broad search |
| **Espacenet (EPO)** | 130M+ worldwide | European & global |
| **WIPO PatentScope** | PCT applications | International filings |
| **Lens.org** | Free, 120M+, exportable | Research & analytics |
| **Derwent Innovation** | Paid, curated | Deep analytics |
| **PatSnap** | Paid | Portfolio analytics |

### Database Selection Guide
```
Quick prior art check → Google Patents
US freedom-to-operate → USPTO + Google Patents
European clearance → Espacenet
International PCT → WIPO PatentScope
Landscape analysis → Lens.org (free) or Derwent (paid)
Academic + patent combined → Lens.org
```

## Search Strategy

### Keyword Development
1. **Core concept** — describe the invention in plain language
2. **Synonyms** — every term the examiner might use
3. **Technical terms** — field-specific nomenclature
4. **Functional terms** — what it does (not what it is)

```
Example: Wireless charging for EVs

Core: "wireless charging" + "electric vehicle"
Synonyms: "inductive charging", "contactless charging", "resonant charging"
Technical: "magnetic resonance", "WPT" (wireless power transfer)
Functional: "charging without cable", "charging while parked"
```

### Classification Codes
Use CPC (Cooperative Patent Classification) to find related patents:

```
Search process:
1. Go to Google Patents
2. Search keyword
3. Note CPC codes on relevant results
4. Filter search by CPC code to find entire class

Common CPC groups:
G06F — Digital computing
H04W — Wireless communication networks
A61B — Diagnostic/surgical instruments
B60L — Electric propulsion for vehicles
```

### Boolean Search Construction
```
USPTO Full Text Search:
SPEC/(("machine learning" OR "neural network" OR "deep learning") 
AND ("fraud detection" OR "anomaly detection"))
AND APD/20200101->20240101

Google Patents:
"machine learning" "fraud detection" (neural OR deep) before:2024 after:2019
assignee:Google OR assignee:Meta

Espacenet CQL:
ta="machine learning" AND ta="fraud detection" AND pd=[20200101 TO 20241231]
```

## Patent Anatomy

### Key Patent Sections
| Section | Purpose | Read First? |
|---------|---------|------------|
| **Claims** | Legal scope of protection | YES — defines what's protected |
| **Abstract** | 150-word summary | For quick triage |
| **Description/Specification** | How invention works | After claims |
| **Drawings** | Visual explanation | With specification |
| **Prior Art** | What they cited | Find related art |

### Reading Claims
```
Independent claim (broadest):
"A method comprising:
  receiving, by a processor, input data;
  applying, by the processor, a neural network to the input data;
  generating an output classification."

Dependent claim (narrower):
"The method of claim 1, wherein the neural network comprises
  at least three hidden layers."

Claim elements to note:
- Preamble: "A method" / "A system" / "A device"
- Transition: "comprising" (open, can add elements) vs
              "consisting of" (closed, no additional elements)
- Body: each limitation narrows the claim
```

## Freedom-to-Operate (FTO) Analysis

### FTO Process
```
1. Define the product/process being cleared
   - Document each technical feature
   - Note materials, methods, configurations

2. Identify relevant patents
   - Search by keyword + classification
   - Search by assignee (competitors)
   - Search by inventor

3. Screen for live patents
   - Check legal status (expired, active, abandoned)
   - US patents expire 20 years from filing
   - Maintenance fees required (3.5, 7.5, 11.5 years)

4. Claim chart analysis
   - Map each claim element to your product
   - Literal infringement: element-by-element match
   - Doctrine of equivalents: substantially same function/way/result

5. Determine risk level
   - High: all elements read on your product
   - Medium: some elements read, design-around possible
   - Low: clear non-infringement argument

6. Document opinion
   - Written FTO opinion from patent attorney (privilege)
```

### Claim Chart Template
```
Patent: US10,XXX,XXX
Claim 1: "A method comprising..."

| Claim Element | Your Product Feature | Reads On? | Notes |
|---------------|---------------------|-----------|-------|
| receiving input data | API endpoint receives JSON | YES | Literal |
| applying neural network | ML model inference | YES | Literal |
| generating classification | Returns label/score | YES | Literal |

Overall: Potential infringement — consult attorney
```

## Patent Landscape Analysis

### Landscape Report Components
1. **Filing trends** — volume over time, growth areas
2. **Top assignees** — who owns the most patents
3. **Key inventors** — prolific individual inventors
4. **Geographic coverage** — where patents are filed
5. **Technology clustering** — CPC code distribution
6. **Citation analysis** — foundational/influential patents
7. **White spaces** — areas with few patents (opportunities)

### Visualization Tools
- Lens.org → built-in charts, free
- PatSnap → commercial landscape maps
- Tableau/Python → custom visualizations from exported data

```python
# Lens.org bulk export → Python analysis
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('lens_export.csv')
df['year'] = pd.to_datetime(df['Filing Date']).dt.year

# Filing trend
df.groupby('year').size().plot(kind='bar', title='Patent Filings by Year')
plt.savefig('filing_trend.png')

# Top assignees
df['Assignee'].value_counts().head(20).plot(kind='barh')
plt.savefig('top_assignees.png')
```

## IP Strategy Decisions

### Build vs. License vs. Design Around
| Situation | Recommended Action |
|-----------|-------------------|
| Core technology, patentable | File provisional → full application |
| Competitor has blocking patent | License, design around, or challenge |
| Patent expires in <3 years | Wait or design around temporarily |
| Non-practicing entity (troll) | Defend with prior art; consider IPR |
| Open source dependency | Verify patent grant in license |

### Patent Filing Decision Checklist
- [ ] Is the invention novel (new)?
- [ ] Is it non-obvious to someone skilled in the field?
- [ ] Is there utility / commercial application?
- [ ] Do we have a written description + claims ready?
- [ ] Have we done a patentability search?
- [ ] Do we want US only or PCT international filing?
- [ ] Is a provisional application needed to establish priority date?
- [ ] What is the budget? (US utility: $15-30K+)
