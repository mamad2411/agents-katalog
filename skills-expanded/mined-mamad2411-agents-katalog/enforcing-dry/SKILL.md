---
name: enforcing-dry
description: Find and evaluate duplication in code, distinguishing true knowledge duplication (must be unified) from coincidental similarity (must be left alone). Apply Pragmatic Programmer's DRY principle ("every piece of knowledge must have a single, unambiguous, authoritative representation") and Fowler's Rule of Three. Use when reviewing a codebase or diff for duplication, when the same logic appears suspiciously twice, before adding code that resembles existing code, or when proposing an extraction. Skip for changes inside a single file under 200 lines, or when the user has explicitly said "don't worry about duplication right now."
---

# Enforcing DRY

DRY is one of the most misunderstood principles in software. The Pragmatic Programmer's actual definition: **every piece of knowledge must have a single, unambiguous, authoritative representation within a system.** Not "no two pieces of code should look the same." Knowledge, not syntax.

AI's failure mode is to extract on syntactic similarity. Two functions look alike, Claude pulls them into a shared helper, and now every future change has to fight a fake abstraction — because the two callsites encoded *different* knowledge that happened to take the same shape today.

This skill produces two outcomes with equal frequency:
- **"Duplication confirmed — unify."** Same knowledge, multiple representations. Extract.
- **"Looks similar, leave alone."** Coincidental shape, different knowledge. Do not extract.

If the skill always concludes "extract," it's biased and being used wrong.

## Process

For each suspected duplication:

1. **Find it.** If invoked in discovery mode ("find duplication in this codebase"), survey for repeated patterns. If invoked in judgment mode ("are these two duplicates?"), examine the candidates directly.
2. **Ask the knowledge question first, not the code question.** What knowledge does each callsite represent? If the answer is "the same fact about the world / business rule / protocol / format," it's true duplication. If the answer is "they happen to be shaped the same but represent different concepts," it's coincidental.
3. **Apply the Rule of Three.** First appearance: write it. Second: notice the resemblance, leave both. Third: now extract — the pattern is real. Premature extraction (at the second appearance) often unifies things that should have stayed apart.
4. **Categorize the duplication** using the Pragmatic Programmer taxonomy below. Different categories have different fixes.
5. **Propose a specific resolution.** Either "extract `<name>` containing `<knowledge>`, called from `<sites>`" or "leave both — they encode different knowledge: `<X>` here, `<Y>` there." Not vague advice.
6. **For confirmed duplications, hand off to `refactoring-patterns`** with the named transformation (Extract Function, Extract Variable, Combine Functions into Class, etc.).

## The four kinds of duplication

From *The Pragmatic Programmer*. Each has a different fix.

- **Imposed duplication** — the developer feels they have no choice (e.g., the framework requires it, the language has no abstraction mechanism for it). Fix: code generation, metaprogramming, or accept the constraint and document it. Rare.
- **Inadvertent duplication** — the developer didn't realize the knowledge was already represented elsewhere. Often appears across modules whose authors didn't know each other's work. Fix: extract to a single representation, update all callers.
- **Impatient duplication** — the developer copy-pasted because reusing felt like more work. Most common in AI-generated code, since the AI is fast at generating and slow at finding existing code. Fix: extract, but also a process signal — the codebase is too hard to navigate, or AI isn't running `mapping-codebase` first.
- **Interdeveloper duplication** — two parts of the team independently solve the same problem. Fix: communication and shared abstractions; in AI workflows, a maintained `UBIQUITOUS_LANGUAGE.md` and `CONTEXT.md` reduce this dramatically.

When you flag duplication, name the category. It tells the user not just *what* to fix but *what process gap* let it happen.

## Rules

- **Knowledge first, syntax second.** If you cannot say what knowledge each callsite represents, you cannot judge duplication. Read each callsite's purpose before comparing their shape.
- **The same shape is not the same knowledge.** Two `for` loops over arrays calculating averages may look identical but average different things — student grades vs API response times. They evolve independently. Do not unify.
- **The same knowledge is not the same shape.** Two callsites may compute the same business rule with different code (one uses a loop, one uses `reduce`). They are duplicates *of knowledge* and should be unified, even though they look different.
- **Apply the Rule of Three.** Two appearances are not yet duplication; they're a pair. By three, the pattern is established and extraction is justified. Premature extraction creates fake abstractions that future changes fight.
- **Forecast change. If A and B are duplicates today but will evolve in different directions tomorrow, don't unify.** Knowledge that *belongs together* changes together; knowledge that doesn't, doesn't.
- **Name the extracted abstraction in the domain language, not by shape.** A function called `processItems` is a shape-extraction. A function called `applyShippingFee` is a knowledge-extraction. If you can't name it in the domain — using `UBIQUITOUS_LANGUAGE.md` if it exists, otherwise the terminology already established in the surrounding code — you probably haven't found real knowledge. Reconsider extracting.
- **Don't extract across module boundaries lightly.** Two modules sharing a private helper means they share a dependency. Sometimes the right fix is to leave the duplication and let each module own its version. Information sharing has cost.
- **Test-guarded extraction.** Once you decide to unify, run `refactoring-patterns` for the actual transformation. Tests stay green between every step.

## Examples

### True knowledge duplication (extract)

```typescript
// In src/billing/invoice.ts
function calculateInvoiceTax(amount: number, region: string): number {
  if (region === "EU") return amount * 0.21;
  if (region === "US-CA") return amount * 0.0725;
  if (region === "US-NY") return amount * 0.08875;
  return 0;
}

// In src/checkout/cart.ts
function getCartTax(subtotal: number, shippingRegion: string): number {
  if (shippingRegion === "EU") return subtotal * 0.21;
  if (shippingRegion === "US-CA") return subtotal * 0.0725;
  if (shippingRegion === "US-NY") return subtotal * 0.08875;
  return 0;
}
```

**Knowledge represented in both:** the company's regional tax rates. Same fact about the world. If the EU rate changes, both must change. **Extract** to a single source of truth — `taxRateForRegion(region)` in a `tax/` module. Name from the domain. Both callsites use it.

### Coincidental similarity (leave alone)

```typescript
// In src/billing/invoice.ts
function averageInvoiceAmount(invoices: Invoice[]): number {
  return invoices.reduce((sum, i) => sum + i.amount, 0) / invoices.length;
}

// In src/monitoring/metrics.ts
function averageResponseTime(samples: number[]): number {
  return samples.reduce((sum, n) => sum + n, 0) / samples.length;
}
```

These look identical, but the *knowledge* in each is different: one is a billing aggregate over domain entities, the other is a performance metric over numeric samples. They will evolve in different directions — `averageInvoiceAmount` may grow currency handling, prorations, voided-invoice exclusions; `averageResponseTime` may grow percentiles, outlier rejection. **Leave both.** Extracting `average<T>(items: T[], get: (T) => number)` produces an abstraction that pretends these belong together when they don't.

### The hard case: looks the same now, will diverge later

```typescript
// In src/auth/session.ts
function isValidToken(token: string): boolean {
  return token.length === 32 && /^[a-f0-9]+$/.test(token);
}

// In src/api/api-keys.ts
function isValidApiKey(key: string): boolean {
  return key.length === 32 && /^[a-f0-9]+$/.test(key);
}
```

Today these are the same. Tomorrow they will diverge — API keys may add a prefix (`sk_live_...`), session tokens may switch to JWTs. The validation rules are *currently* the same but they encode different knowledge: "what makes a session token valid" vs "what makes an API key valid." **Leave both.** If they evolve identically over time (Rule of Three across multiple changes confirms it), then unify later. Don't unify on the first sight of similar regex.

## Output format

Produce a numbered list of findings. Each finding has the same structure:

```
### Finding N: <one-line title>

**Locations:** `<file:line>`, `<file:line>`, ...

**Knowledge in each location:**
- `<file:line>`: <what knowledge this represents>
- `<file:line>`: <what knowledge this represents>

**Verdict:** Extract / Leave alone / Wait (Rule of Three not yet satisfied)

**Category** (if Extract): Inadvertent / Impatient / Interdeveloper / Imposed

**Rationale:** <one paragraph: why this is or isn't true knowledge duplication, what would happen if it were unified or left>

**If Extract — proposed resolution:**
- Name (in domain language): `<name>`
- Location: `<module>`
- Signature: `<sketch>`
- Callsites updated: `<list>`
- Hand off to `refactoring-patterns` to apply Extract Function or appropriate named transformation.
```

End with a summary line: `Found N suspected duplications. M confirmed for extraction, K marked coincidental, L deferred under Rule of Three.`

## Anti-patterns to refuse

- **Extracting on syntactic similarity without checking knowledge.** Refuse. Always answer "what knowledge does each callsite represent?" before extracting.
- **Extracting at the second appearance.** Refuse. Two is a pair, not a pattern. By three, extract.
- **Naming the extracted abstraction by shape.** Refuse. `processItems` and `handleData` are red flags — they reveal that you don't know what knowledge you've extracted. If you can't name it in the domain, you haven't found duplication of knowledge.
- **Recommending extraction across module boundaries without naming the dependency cost.** Refuse. Shared helpers create coupling. The user must know what they're paying.
- **Always recommending extraction.** Refuse. If every duplication you flag is "extract," you're applying a syntactic rule, not the principle. Good DRY analysis has a substantial "leave alone" rate.

## Integration with other skills

- **`mapping-codebase`** is worth running first if the codebase is unfamiliar — you can't judge inadvertent duplication without knowing what already exists. If you don't run it, do at least a brief survey of the relevant modules before flagging duplication, so "no existing abstraction exists" is a checked claim rather than an assumption.
- **`ubiquitous-language`** provides the domain names for proposed extractions. If a glossary exists, use it.
- **`refactoring-patterns`** executes the named transformation (Extract Function, Combine Functions into Class) once duplication is confirmed.
- **`reviewing-as-staff-engineer`** uses this skill's output as one of its review lenses (design regression — duplication of an existing pattern).

## Post-output instruction

After completing the analysis, state:

> Found N suspected duplications. M confirmed for extraction, K marked coincidental, L deferred under Rule of Three. For confirmed extractions, run `refactoring-patterns` with the named transformation in fresh context.
