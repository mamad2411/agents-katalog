---
name: pleadings-review
description: >
  Review statements of claim, defences, replies, and counterclaims for
  compliance with the Rules of the High Court (Cap 4A, O.18) and Rules of
  the District Court (Cap 336H, O.18). Flags defects, non-compliance, and
  drafting weaknesses. Produces a compliance report with proposed amendments.
argument-hint: "[paste or attach the pleading]"
---

# /litigation-legal:pleadings-review

1. Load `CLAUDE.md` for the pleadings framework (RHC O.18 / RDC O.18).
2. Ask for the pleading to review and the stage of proceedings.
3. Walk the review checklist below.
4. Produce a compliance report with flags (`[verify]`, `[review]`) and redline suggestions.

## Review Checklist

### 1. Formal Requirements (O.18, r.6–8)

- [ ] Is the pleading titled with the correct court (CFI / DC)?
- [ ] Is the action number correctly stated?
- [ ] Are the parties correctly named and described?
- [ ] Does the pleading state the relief/defence sought?
- [ ] Is the pleading divided into numbered paragraphs?
- [ ] Are dates, amounts, and references properly particularised?

### 2. Statement of Claim (Plaintiff)

**Substantive compliance:**
- [ ] Does the SoC plead ALL material facts (not evidence)?
- [ ] Are the elements of each cause of action pleaded?
- [ ] Is the cause of action clearly identifiable?
- [ ] Are all losses/damages pleaded and quantified (where possible)?
- [ ] Is interest claimed? Basis stated?
- [ ] Has the contract (if applicable) been identified?
- [ ] Have the breached terms been specified?
- [ ] Are all necessary parties joined? (O.15)

**Common defects to flag:**
- [ ] Bare conclusion without material facts (O.18, r.25)
- [ ] Scandalous or unnecessary matter (O.18, r.19(b))
- [ ] Ambiguous or inconsistent allegations
- [ ] Failure to plead a condition precedent (O.18, r.14)
- [ ] Failure to plead a claim for special damages

### 3. Defence (Defendant)

**Substantive compliance:**
- [ ] Does the Defence respond to EACH allegation (admit, deny with reasons, or require proof)?
- [ ] Are denials specific and reasoned? (O.18, r.13 — general traverse is insufficient)
- [ ] Are set-offs and counterclaims pleaded?
- [ ] Are affirmative defences (limitation, illegality, accord and satisfaction) pleaded?
- [ ] Is contributory negligence pleaded? (O.18, r.9)
- [ ] Are all conditions precedent admitted or denied?

**Common defects to flag:**
- [ ] Bare denial without specification (non-compliance with O.18, r.13(3))
- [ ] Evasive denial (e.g., "the defendant does not admit" without stating the true position)
- [ ] Failure to plead a positive case when required (e.g., alibi in a commercial case)
- [ ] Contradictory defences
- [ ] Scandalous or irrelevant matter

### 4. Reply (Plaintiff)

- [ ] Does the Reply respond to new matters raised in the Defence?
- [ ] Is the Reply confined to answering the Defence — not re-pleading the SoC?
- [ ] If no Reply is filed, is that intentional? (Matters in the Defence not responded to are deemed denied — O.18, r.14(4))

### 5. Counterclaim & Defence to Counterclaim

- [ ] Does the counterclaim arise out of the same transaction or facts? (If not, it may be struck out or ordered separately — O.15, r.5)
- [ ] Is the counterclaim properly pleaded as a separate claim?
- [ ] Has the plaintiff properly responded to the counterclaim?

### 6. Striking Out Grounds (O.18, r.19)

Check whether any part of the pleading could be struck out on the grounds that it:
- [ ] Discloses no reasonable cause of action or defence
- [ ] Is scandalous, frivolous, or vexatious
- [ ] May prejudice, embarrass, or delay the fair trial
- [ ] Is otherwise an abuse of process

### 7. Specific Issues Under HK Practice

- [ ] Is the pleading consistent with the Limitation Ordinance (Cap 347) — filed within the applicable period?
- [ ] Is interest claimed under the High Court Ordinance (Cap 4, s.48 or s.49) or under contract?
- [ ] Are statutory references correct (Cap references)?
- [ ] If an equitable claim is made, is it properly pleaded? (O.18, r.8 — must specify the equitable ground)

## Output

| Section | Compliance | Issues | Action |
|---|---|---|---|
| Formal requirements | ✅ / ⚠️ / 🔴 | [List] | [Fix] |
| Cause of action / defence | ✅ / ⚠️ / 🔴 | [List] | [Fix] |
| Specific allegations | ✅ / ⚠️ / 🔴 | [List] | [Fix] |
| Striking out risk | 🟢 / 🟡 / 🔴 | [List] | [Address] |

Append redline suggestions for each flagged defect.


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
