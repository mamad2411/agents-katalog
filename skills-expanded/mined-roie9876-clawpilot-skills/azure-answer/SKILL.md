---
name: azure-answer
description: "Answer Azure pricing, capability, SKU, and service comparison questions backed by verified web data and optional CLI output. Triggers include: 'azure answer', 'azure pricing', 'azure service', 'compare azure services', 'azure capabilities', 'azure SKU', 'azure cost', 'which azure service', or any factual question about Azure services, pricing, or features."
---

# /azure-answer — Verified Azure Q&A

Answer factual questions about Azure services — pricing, capabilities, SKU
comparisons, and service selection — using live web search data and optional
Azure CLI verification. Every claim is backed by a cited source so the user
can trust and forward the answer.

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. The only shell command is `az` (Azure CLI), which works identically across OSes once installed. See `_shared/PLATFORM.md` for the full reference.

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Check if `az` exists | `command -v az \|\| echo missing` | `Get-Command az -ErrorAction SilentlyContinue` |
| Run `az` command | `az version` | `az version` (same) |
| Install Azure CLI | macOS: `brew install azure-cli` · Linux: see Azure docs | Windows: `winget install Microsoft.AzureCLI` |

Default to POSIX commands; use PowerShell on Windows native (not WSL/Git Bash).

## Core Principles

- **Never fabricate Azure information.** Every pricing figure, SKU name, capability claim, and service limit must be backed by a cited source (URL or CLI output). Do not rely on training data alone for facts that change frequently (pricing, quotas, region availability).
- **Verify before answering.** Always search the web or query the CLI before composing the answer. Training data may be months out of date — Azure pricing and features change constantly.
- **Refuse gracefully when data cannot be verified.** If web search returns nothing relevant and CLI is unavailable, do NOT guess. Provide a direct link to the relevant Azure documentation or pricing page instead.
- **Preserve source language.** Section headings are always English. If the user asks in Hebrew, respond in Hebrew — but keep technical terms (service names, SKU identifiers, CLI commands) in their original English form. Do not translate content between languages.
- **Scope boundary.** This skill answers: pricing questions, service capability checks, service comparisons, SKU recommendations, region availability, and quota/limit lookups. It does NOT provide: implementation guidance, architecture reviews, debugging help, or deployment instructions — redirect those to appropriate skills or general assistance.

## Prerequisite Auto-Install

Before running, verify all dependencies are present. **Install anything missing automatically.**

### No Required Sibling Skills

This skill is standalone — it has no required sibling skill dependencies. However,
it is part of the customer skills repository. If any other skills are needed later,
they can be installed from `https://github.com/roie9876/clawpilot-skills`.

### Optional Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) | Required? |
|------|---------------|-----------------|-----------------|-------------------|-----------|
| Azure CLI | `az version` | `az version` | `brew install azure-cli` | `winget install Microsoft.AzureCLI` | ⚠️ Optional |

If `az` is not installed or not logged in, the skill degrades gracefully to
web-search-only mode with a note that CLI verification was skipped.

If `az` is installed but not logged in, run `az login` before proceeding.

---

## Step 1: Classify the Question

Categorize the user's question into one of these types:

| Category | Examples |
|----------|---------|
| **Pricing** | "How much does Azure OpenAI GPT-4o cost?", "Azure Functions pricing tiers" |
| **Service Comparison** | "Azure SQL vs Cosmos DB for transactional workloads", "AKS vs Container Apps" |
| **Capability Check** | "Does Azure Cognitive Search support vector search?", "Can App Service run .NET 9?" |
| **SKU Recommendation** | "Which VM size for a 16GB RAM workload?", "Best App Service plan for 10 RPS" |
| **Region / Availability** | "Is GPT-4o available in Sweden Central?", "Which regions have Azure OpenAI?" |
| **Out of Scope** | "How do I deploy to AKS?", "Debug my Bicep template", "Design my architecture" |

**If out of scope:** Respond with a brief explanation: "This is an implementation/architecture question — /azure-answer covers pricing, capabilities, and service comparisons. I can help with this directly as a general question instead." Then stop.

## Step 2: Search for Current Data

Use web search to find current, authoritative data. Prefer Microsoft sources.

### Primary: Web Search

Run one or more targeted searches using `search-the-web` or `google_search`:

**Query templates by category:**

| Category | Query Pattern |
|----------|--------------|
| Pricing | `"Azure {service} pricing {current-year}" site:azure.microsoft.com` |
| Comparison | `"Azure {serviceA} vs {serviceB} {use-case}"` |
| Capability | `"{service} {capability}" site:learn.microsoft.com` |
| SKU | `"Azure {service} SKU sizes specifications" site:learn.microsoft.com` |
| Region | `"Azure {service} region availability" site:learn.microsoft.com` |

**Source quality rules:**

- **Require** at least one result from `microsoft.com`, `learn.microsoft.com`, or `azure.microsoft.com`. These are the authoritative sources for Azure information.
- **Accept** supplementary data from reputable tech sites (e.g., `techcommunity.microsoft.com`, `devblogs.microsoft.com`) but always cross-reference against official docs.
- **Reject** results older than 12 months for pricing data — Azure pricing changes frequently.
- If results are thin, use `fetch_page` to read the most promising URL and extract specific figures.

**If no relevant results are found:**

Do NOT proceed to composing an answer. Skip to Step 5 (Handle Failure Gracefully).

## Step 3: Verify with CLI (Optional)

When the `az` CLI is available on the system, supplement web data with live queries for higher confidence. This step is optional — the skill works without CLI access.

**Check CLI availability first:**

```bash
# macOS / Linux / WSL / Git Bash
az version 2>/dev/null && echo "CLI available" || echo "CLI not available"
```

```powershell
# Windows PowerShell
if (Get-Command az -ErrorAction SilentlyContinue) { az version; "CLI available" } else { "CLI not available" }
```

If available, use targeted commands based on question category:

| Category | CLI Command |
|----------|-------------|
| VM Sizing | `az vm list-sizes --location {region} --output table` |
| Cognitive Services SKUs | `az cognitiveservices account list-skus --output table` |
| App Service Runtimes | `az functionapp list-runtimes --output table` or `az webapp list-runtimes` |
| Region Availability | `az account list-locations --output table` |
| Resource Providers | `az provider show --namespace {provider} --query "resourceTypes[].locations"` |
| Current Pricing | Not available via CLI — rely on web search |

### CLI Error Handling

| Error | Behavior |
|-------|----------|
| `az: command not found` | CLI not installed. Skip CLI verification entirely. Continue with web data only. |
| `Please run 'az login'` | Not authenticated. Note "CLI available but not logged in — skipped CLI verification" in the answer. Continue with web data. |
| Command times out (>15s) | Kill the command. Note "CLI query timed out" and continue with web data. |
| Command returns error | Note the specific error. Continue with web data — do not retry. |
| Empty result set | The query ran but returned nothing. Note "CLI returned no results for {query}" and rely on web data. |

## Step 4: Compose the Answer

Format the answer with these required sections:

### Answer Body

- Lead with a **direct answer** to the user's question in 1-3 sentences.
- Follow with **supporting detail** — tables for pricing/comparisons, bullet points for capabilities.
- Use tables for any comparison or pricing data — they are easier to scan and forward.

### Sources Section (Required)

List all sources that contributed to the answer:

```
**Sources:**
1. [Azure {Service} Pricing](https://azure.microsoft.com/...) — accessed {date}
2. [Learn: {Service} Overview](https://learn.microsoft.com/...) — accessed {date}
3. `az vm list-sizes --location westeurope` — queried {date}
```

Every factual claim in the answer must trace back to a numbered source.

### Freshness Disclaimer (Required)

Always include at the end:

```
> ⚠️ **Verified on {YYYY-MM-DD}.** Azure pricing and features change frequently.
> Confirm current figures at the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
> before making commitments.
```

### Confidence Indicator (Required)

Rate the answer confidence:

| Level | Criteria | Display |
|-------|----------|---------|
| **High** | Multiple authoritative sources agree, data is <3 months old | 🟢 High confidence |
| **Medium** | Single authoritative source, or data is 3-12 months old | 🟡 Medium confidence |
| **Low** | Training data only, no live verification succeeded | 🔴 Low confidence — treat as unverified |

If confidence is **Low**, prepend a prominent warning: "⚠️ I could not verify this against current sources. The information below is from training data and may be outdated."

## Step 5: Handle Failure Gracefully

If web search returns nothing relevant AND CLI is unavailable or unhelpful:

**Do NOT guess or rely on training data without flagging it.**

Instead, respond with:

```
I couldn't verify current Azure data for this question.

**Check these resources directly:**
- [{Most relevant Azure docs page}]({URL})
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Azure Updates](https://azure.microsoft.com/updates/) — for recent changes

If you can share a more specific service name or scenario, I can try a narrower search.
```

Choose the most relevant docs page URL based on the question category:

| Category | Fallback URL |
|----------|-------------|
| Pricing | `https://azure.microsoft.com/pricing/` |
| VM/Compute | `https://azure.microsoft.com/pricing/details/virtual-machines/` |
| AI/Cognitive | `https://azure.microsoft.com/pricing/details/cognitive-services/` |
| Databases | `https://azure.microsoft.com/products/category/databases/` |
| General | `https://learn.microsoft.com/azure/` |

## Error Handling

| Failure Mode | Behavior |
|-------------|----------|
| `search-the-web` / `google_search` returns no results | Try alternate query phrasing (drop `site:` filter, broaden terms). If still nothing → go to Step 5. |
| `search-the-web` / `google_search` returns results but none from Microsoft | Use the non-Microsoft results with a lower confidence rating. Note "No official Microsoft source found" in the answer. |
| `fetch_page` fails on a URL | Skip that source. Continue with remaining results. Note the gap if it was a key source. |
| `az` CLI not available | Skip Step 3 entirely. Rely on web search data alone. |
| `az` CLI returns auth error | Note "CLI not authenticated" in the answer. Continue with web data. |
| User question is ambiguous | Ask one clarifying question before searching: "Did you mean {service A} or {service B}?" or "Which region are you targeting?" |
| Multiple conflicting sources | Report all figures with their sources. Note the discrepancy and recommend the user verify with the pricing calculator. |
