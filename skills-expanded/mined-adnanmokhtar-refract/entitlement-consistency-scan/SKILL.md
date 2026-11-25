---
name: entitlement-consistency-scan
description: "Plan entitlement detector: pricing copy vs billing vs gates, unknown gate keys, hard-coded plan names and price ids."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: entitlement-consistency-scan

## Premise

The pricing page is a contract, and the code holds the same facts in up to four other places: the billing config (Stripe lookup keys, price ids), the entitlement catalog (a const list, an enum, a seed), every gate that checks a key, and the UI that hides or shows a feature. When two of them disagree, one is lying:

- The page promises 10 seats and the gate allows 5.
- `@RequireFeature('advanced-reports')` names a key the catalog spells `advanced_reports`. Depending on the guard, the paid feature is free for everyone or dead for everyone.
- `if (plan === 'pro')` grants a feature, so the next plan added (`pro_annual`) silently loses it.
- `price_1Nabc…` is pasted into checkout, so the flow works in test mode and breaks in live mode, where the id is different.

**Every finding cites both ends:** the two sources of one plan fact (copy line and config line, gate line and catalog line) at `<file:line>`, or one source and "no counterpart after the written search". It also cites the guard that judges the key, the oracle that failed or the test that would settle it, and the fix. A grep hit is a candidate, never a finding by itself. "Entitlements are consistent" is never printed without the class-coverage block (§ Output).

**Catalog first, guards second, gates last.** A gate key can be judged only against the catalog its guard reads. On a measured monorepo, two global guards split the keys between them: one judged coarse module keys, the other extension slugs, and each returned `true` for the other's keys. A naive "key not in the catalog" join reported 22 gated handlers as ungated ([`precedents/product.md`](../../../../snippets/precedents/product.md) § 18). The proof is a catalog-driven matrix test, plan × key → gate decision, which closes the whole class at once (`proof-oracles.md` § Product, V418–V421). A candidate with no harness is **Unconfirmed**, with that test written out ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all four hold:

1. **The fact is a plan fact.** A price, a limit (seats, projects, orders, storage), an included feature, or a key that decides access. Rate limits, batch sizes and pagination caps are not (grep 1a reads all `MAX_*`; read each).
2. **Every source is read.** For a value: every place the plan states it. For a gate key: the catalog, and **every** global guard, middleware and policy registry, with what each admits (grep 0b, § 18). A key the coarse guard skips may be the slug guard's.
3. **No design choice explains it.** Grandfathered plans and documented fair-use caps (§ 20), a central plan map that *is* the entitlement layer (§ 19), ids in seeds and tests (§ 21), and marketing rounding of an exact number (§ 22) all fail here.
4. **The oracle fires, or would.** A two-ended static diff is enough for §1 and §6 literals. Gate behaviour (§2, §4, §5) needs the matrix test: a plan without the key is refused by the server, and the UI hides the feature.

## Boundaries

- **Money:** prices computed, rounded, prorated, refunded, converted → business `pricing-rule-scan`. Tax and issued documents → `tax-invoice-scan`. Both apply when the business pack is installed. §1 here compares the *stated* price across sources and never recomputes it. Without business, list a computation defect tagged `money (owner pack business not installed)`.
- **The server does not enforce what the UI hides** (a client-only gate), and **limit counters that race** (two requests both under the cap) → security (`@api-security-reviewer`, `logic-race-scan`), when installed. §5 here owns the inverse dead end: the UI shows what the server refuses. Without security, list client-only keys tagged `authz (owner pack security not installed)`.
- **Feature flags** (rollout, kill switches, stale flags) → devops `progressive-delivery`, when installed. A flag used as an entitlement (LaunchDarkly or Statsig targeting by plan) is read here as a gate; its lifecycle is devops'. Without devops, flag lifecycle is unreported here.
- **A permission check** (`can_manage_ads`, a role) is not an entitlement. Authorization correctness is security's (when installed; without it, a permission defect is tagged `authz (owner pack security not installed)`). This skill reads a permission only when a plan decides it.
- **Pricing-page copy completeness** (missing translations) → frontend `i18n-scan`, when the frontend pack is installed; without it, unreported here. §1 reads catalogs for *numbers* only (§ 22).

## Adapt to the codebase — the lanes

Read the billing and entitlement libraries **and their versions** (grep 0a), and print the lanes in the header.

| Lane | Catalog (0c) | Gates (2) | Billing wiring (6) | Compile-time control |
|---|---|---|---|---|
| **Home-grown TS** (Nest, Express, Next) | `export const MODULE_KEYS = [...] as const`, `enum Plan`, `type Plan = 'free' \| …`, `plans.ts` / `plans.json` | `@Require<Module|Feature|Plan>('k')` + the `APP_GUARD`s that read the metadata; `hasFeature('k')`, `useEntitlement('k')`, `useModuleEnabled('k')`, `<FeatureGate feature="k">`, route-registry fields (`module: 'k'`) | price ids in config | the decorator or hook parameter typed as the catalog union (`(module: ModuleSlug \| ModuleKey)`): a typo fails `tsc` |
| **Stripe** (Billing, Entitlements) | Products / Prices with `lookup_key`; Entitlement Features with their own `lookup_key` | `active_entitlements` lookups; `entitlements.active_entitlement_summary.updated` handlers (the summary carries at most 10 entitlements; the rest are paged through `entitlements.url`) | `price_…` / `prod_…` literals; `lookup_keys[]` resolution | — |
| **Paddle / Chargebee / Lemon Squeezy** | plan and price ids in config | the SDK's subscription status read in a guard | `pri_01…` / `pro_01…` (Paddle) literals | — |
| **Laravel** (Cashier) | `config/plans.php`, an enum | `Gate::define`, `subscribed('default')`, `onPlan('pro')`, policies | `price_…` in config or `.env` | — |
| **Django / DRF** | `TextChoices`, settings dicts | `@plan_required`, permission classes that read the plan, `dj-stripe` models | `price_…` in settings | — |
| **Rails** | `PLANS = {}`, `enum plan:` | `before_action :require_plan`, Pundit policies, `plan.pro?` | `pay` / Stripe ids in credentials | — |
| **Vendor entitlement layers** (Stigg, Schematic, LaunchDarkly / Statsig used for plans) | the vendor's catalog, outside the repo | the SDK's `getEntitlement` / `checkFlag` calls | — | the vendor's typed client, where generated |

A vendor catalog that lives outside the repo (Stripe Features, Stigg) is `NOT-RUN (auth)` without a test-mode key. §2 then joins the gates against the repo's mirror of it, and says so.

## Pre-flight greps

Run as **one** bash script from the repo root (bash 3.2: no `mapfile`). Every `rg` names its path. An `rg` exit 2 is `blocked (rg exit 2)`, never zero hits. Grep 0 decides the lanes and the guards. Grep **N** feeds **§N**.

```bash
ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.turbo,coverage,.venv,venv,__pycache__,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,stories,seeds,seeders,migrations,migration,db/migrate}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,test-data,fixture,fixtures}.*' -g '!**/{test_*,*_test,conftest}.*' -g '!**/*.d.ts' -g '!**/*.min.*' -g '!**/{docs,ai,.claude,.git,scripts}/**')
C=(-g '*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,py,rb,go,php,dart,kt,java,cs}')
NC='^[^:]+:\d+:\s*(?://|\*|/\*|#|<!--)'
P='free|basic|starter|standard|pro|premium|plus|business|team|enterprise|growth|scale|hobby|personal|professional|ultimate|trial'
g() { out=$("$@" 2>&1); ec=$?; [ $ec -eq 2 ] && { echo "blocked (rg exit 2): $out" | head -3; return; }; printf '%s\n' "$out" | rg -v --pcre2 "$NC" | head -60; }
# 0a. Billing and entitlement libraries (the lanes).
g rg -n --no-heading --pcre2 -g '**/{package.json,requirements*.txt,pyproject.toml,Gemfile,composer.json}' -g '!**/node_modules/**' '"(?:stripe|@stripe/[\w-]+|@paddle/[\w-]+|paddle-sdk|chargebee(?:-typescript)?|@lemonsqueezy/[\w.-]+|recurly|@schematichq/[\w-]+|@stigg/[\w-]+|@launchdarkly/[\w-]+|launchdarkly-[\w-]+|statsig-[\w-]+|@statsig/[\w-]+|laravel/cashier[\w-]*|dj-stripe)"\s*:|^\s*(?:stripe|dj-stripe|chargebee|paddle-python-sdk)\b|^\s*gem\s+["\x27](?:pay|stripe)["\x27]' "${ROOTS[@]}"
# 0b. Every global guard, middleware and policy registry: read each one and write down which keys it admits (§ 18).
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" '\bprovide:\s*APP_GUARD\b|@UseGuards\(\s*\w*(?:Plan|Entitle|Module|Feature|Subscri)\w*|\bGate::define\(|before_action\s+:\w*(?:plan|subscri|entitle|feature)\w*|@\w*(?:plan|subscription|entitlement|feature)_required\b|\bapp\.use\(\s*\w*(?:[Pp]lan|[Ee]ntitle|[Ff]eature|[Ss]ubscri)\w*' "${ROOTS[@]}"
# 0c. Catalogs: const lists, enums, unions and plan files. Two catalogs of one fact are a §1 row even when equal today.
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" '^\s*(?:export\s+)?(?:const|let|var)\s+(?:[A-Z][A-Z0-9_]*_)?(?:PLANS?|TIERS?|MODULES?|FEATURES?|ENTITLEMENTS?|ADDONS?|SLUGS|MODULE_KEYS|FEATURE_KEYS|PLAN_KEYS)\b\s*(?::[^=\n]+)?=\s*(?:Object\.freeze\(\s*)?(?:\[|\{|new\s+Set\()|^\s*(?:export\s+)?enum\s+\w*(?:Plan|Tier|Feature|Entitlement|Module|Addon)\w*\s*\{|^\s*(?:export\s+)?type\s+\w*(?:Plan|Tier|Feature|Entitlement|Module|Addon)\w*\s*=\s*[\x27"]|^\s*class\s+\w*(?:Plan|Tier|Feature|Entitlement)\w*\((?:str,\s*)?(?:Enum|StrEnum|TextChoices|IntegerChoices)\)' "${ROOTS[@]}"
g rg --files -g '**/{plans,entitlements,tiers,features}.{ts,js,mjs,json,yml,yaml}' -g '**/{pricing,plans}*.{json,mdx,md}' -g '**/billing.{ts,js,json,yml,yaml}' -g '!**/node_modules/**' -g '!**/{test,tests,__tests__,fixtures,docs,ai,deploy,k8s,charts,helm,infra,terraform}/**' "${ROOTS[@]}"
# 1. Plan facts with numbers: 1a limits in code (incl. plan-keyed maps), 1b numbers in pricing copy and catalogs.
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" '\b(?:MAX|LIMIT)_(?:\w+_)?(?:PROJECTS?|SEATS?|USERS?|MEMBERS?|STORES?|PRODUCTS?|ORDERS?|WORKSPACES?|LOCATIONS?|STORAGE_(?:GB|MB)|TEAM_MEMBERS?)(?:_PER_\w+)?\s*[:=]\s*\d|\b(?:max|limit|included)(?:Seats|Projects|Users|Members|Stores|Products|Orders|Workspaces|Locations)\s*[:=]\s*(?:\d|Infinity|null|-1)|\{\s*[\x27"]?(?:'"$P"')[\x27"]?\s*:\s*\d[\d_]*\s*,\s*[\x27"]?(?:'"$P"')[\x27"]?\s*:' "${ROOTS[@]}"
g rg -n --no-heading -i --pcre2 -g '**/{pricing,plans,plan,billing}*.{json,ts,tsx,js,mdx,md,yml,yaml,vue,svelte,html}' -g '**/{locales,locale,i18n,messages,translations}/**/*.{json,yml,yaml}' -g '!**/node_modules/**' -g '!**/{test,tests,__tests__,fixtures,docs,ai}/**' '(?:\bup to\s+)?\b(?:\d[\d,.]*\s*k?|unlimited)\s+(?:projects?|seats?|users?|members?|GB|TB|requests?|orders?|products?|stores?|workspaces?|team members?|locations?)\b|[$€£]\s?\d+(?:[.,]\d{2})?\s*/\s*(?:mo|month|yr|year|user|seat)\b' "${ROOTS[@]}"
# 2. Gate keys, server (2s) and client (2c), as sorted key lists; §2 joins them to the catalog, §5 to each other.
SK=$(rg -o --no-filename --no-line-number --pcre2 -r '$1$2' "${C[@]}" "${X[@]}" '@Require(?:Module|Feature|Plan|Entitlement|Subscription|Addon)\s*\(\s*[\x27"`]([\w:.-]+)|\b(?:hasFeature|hasEntitlement|checkEntitlement|requireFeature|requirePlan|isEntitled|can_use_feature|has_feature|has_entitlement|feature_enabled|subscribed|onPlan)\s*\(\s*(?:[\w.]+\s*,\s*)?[\x27"`]([\w:.-]+)' "${ROOTS[@]}"); [ $? -eq 2 ] && echo 'blocked (rg exit 2): 2s'
CK=$(rg -o --no-filename --no-line-number --pcre2 -r '$1$2$3' "${C[@]}" "${X[@]}" '\b(?:useEntitlement|useFeature|useModuleEnabled|useFeatureEnabled|usePlanFeature|canUseFeature)\s*\(\s*[\x27"`]([\w:.-]+)|<\w*(?:Feature|Entitlement|Plan|Module)Gate\b[^>]*?\b(?:feature|entitlement|plan|module|slug|name)\s*=\s*\{?\s*[\x27"`]([\w:.-]+)|\b(?:module|requiredModule|entitlement|requiredEntitlement|requiredPlan|requiredFeature)\s*:\s*[\x27"`]([a-z][\w:.-]*)[\x27"`]' "${ROOTS[@]}"); [ $? -eq 2 ] && echo 'blocked (rg exit 2): 2c'
printf 'server keys: %s\n' "$(printf '%s\n' "$SK" | sort -u | tr '\n' ' ')"; printf 'client keys: %s\n' "$(printf '%s\n' "$CK" | sort -u | tr '\n' ' ')"
echo '-- client-only (security, routed):'; comm -13 <(printf '%s\n' "$SK" | sort -u) <(printf '%s\n' "$CK" | sort -u)
echo '-- server-only (§5: does the UI show it?):'; comm -23 <(printf '%s\n' "$SK" | sort -u) <(printf '%s\n' "$CK" | sort -u)
# 3. Plan names compared in feature checks (outside the central plan map, § 19).
g rg -n --no-heading -i --pcre2 "${C[@]}" "${X[@]}" "\\b(?:plan|tier|subscription(?:\\.plan)?|planId|plan_id|planName|plan_name|planKey|plan_key|planSlug|plan_slug|tierName|currentPlan|current_plan)(?:\\??\\.\\w+)?\\s*(?:===?|!==?|==|!=)\\s*[\"\\x27](?:$P)[\"\\x27]|[\"\\x27](?:$P)[\"\\x27]\\s*(?:===?|!==?|==|!=)\\s*\\w*(?:plan|tier)\\b|\\b(?:plan|tier)\\w*\\s+(?:not\\s+)?in\\s*[\\[(]\\s*[\"\\x27](?:$P)[\"\\x27]|\\[\\s*[\"\\x27](?:$P)[\"\\x27](?:\\s*,\\s*[\"\\x27](?:$P)[\"\\x27])*\\s*\\]\\.includes\\(\\s*\\w*(?:plan|tier)|\\bplan\\.(?:$P)\\?|\\bPlan\\.(?:$P)\\b\\s*[=!]=" "${ROOTS[@]}"
# 4. Catalog keys with no gate reference. Set CAT_FILES to the catalog files 0c found (read them first).
CAT_FILES=()   # e.g. (packages/contracts/src/plans.ts)
[ ${#CAT_FILES[@]} -gt 0 ] && for k in $(rg -o --no-filename --no-line-number --pcre2 -r '$1' '^\s*[\x27"]([\w:.-]+)[\x27"],?\s*$' "${CAT_FILES[@]}" | sort -u); do
  printf '%-28s %s\n' "$k" "$(rg -l --pcre2 "${C[@]}" "${X[@]}" "(?:@Require\\w*\\(|\\buse\\w*(?:Enabled|Entitlement|Feature)\\(|\\b(?:has|check|require|is)\\w*(?:Feature|Entitle\\w*|Plan|Module)\\(|\\b(?:module|feature|slug|entitlement|plan)\\s*[:=])\\s*\\{?\\s*[\\x27\"]$k[\\x27\"]" "${ROOTS[@]}" | wc -l | tr -d ' ')"; done
# 6. Billing wiring: 6a provider ids in runtime source (Stripe ids carry a digit and a capital; Paddle ids start 01), 6b sync handlers.
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" '[\x27"`](?:(?:price|prod|plan)_(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Z])[A-Za-z0-9]{8,}|(?:pri|pro|sub)_01[a-z0-9]{20,})[\x27"`]' "${ROOTS[@]}"
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" 'entitlements\.active_entitlement_summary\.updated|active_entitlement_summary|customer\.subscription\.(?:updated|deleted)|subscription_(?:updated|cancelled|canceled)' "${ROOTS[@]}"
```

A finding is a hit **plus** both ends read **plus** every guard that judges the key. Three blind spots are structural, so work around them rather than trust a quiet grep:

- **A gate built from data.** A route registry's `module:` field, a nav item's `feature`, a `requiredPlan` column: 2c reads the one-line `key: 'value'` form. Read the registry the router maps over once.
- **A catalog outside the repo** (Stripe Features, a vendor dashboard). It is `NOT-RUN (auth)`. Join against the repo's mirror, and name it.
- **Limits enforced in SQL or a policy engine** (a `CHECK`, a row-count trigger, OPA). Read the migration or the policy for the number.

**Measured** (2026-10-19). Across the 23 fixture roots, 0 exit-2 runs.

- 0a: `ci-defects` (a `stripe` dependency, 1 line).
- 0b: `backend-defects` (a quota `APP_GUARD`, 1) and `port-pair` (3 auth guards).
- 0c: 1 line each in `brittle-suite` and `quality-mix`. In `quality-mix` it is a `type Plan = 'free' | …` union, read by §3.
- 1a: `quality-mix` 2. One is a plan-keyed seat map `{ free: 1, trial: 5, … enterprise: 500 }`. The other is a hard-coded `planPrices={{ starter: 1_900, … }}` in the web app's pricing tab, a §1 source to diff against the billing config.
- 3: `quality-mix` 2. `account.plan === 'enterprise'` in the usage-quota check is outside the plan map, so it is an EN §3 candidate. `plan !== 'free' || plan !== 'trial'` sits in the plan module itself (§ 19); its always-true logic is code-quality's seeded QM-CS-06, corroborated here.
- Every other grep returned 0 on every fixture.

The first versions were noisier, on the fixtures or the real repo below:

- 0c: `MAX_LANDING_FEATURES = 6` and a DI `Symbol('TENANT_MODULES')` (the right-hand side must now be a list or map), and it missed `MODULE_KEYS` (the name pattern consumed its first letter).
- 1a: 42 report counters such as `orders: 0` (the bare-key form is gone).
- 6a: `'price_required'`, a validation code (an id now needs a digit and a capital).
- 0c files: a cutover plan YAML and a Kubernetes `pricing.yaml`.

On a real NestJS + React monorepo (read-only, 0.8 s for the whole block):

- **0a: 0.** There is no billing SDK: packages are prepaid credits.
- **0b: 11 `APP_GUARD`s.** Two judge modules: the coarse-key guard in settings and the extension-slug guard in platform, each skipping the other's keys (§ 18).
- **0c: 11 lines.** The coarse `MODULE_KEYS` is declared twice, in the contracts package and the API's domain catalog. The web app re-declares the 13 purchasable `MODULE_SLUGS`. All copies are equal today: §1 Hardening rows, one source each.
- **1b: 7 lines.** The package card advertises "Unlimited Stores" on every package, and 1a finds no store limit: consistent.
- **2: 71 gate sites.** 2s gives 9 server keys. 2c gives 10 client keys: 8 from hooks and `<ModuleGate slug>`, and 2 more from the route registry's `module:` field. The first 2c, anchored to a whole line, missed the registry's inline `module: 'whatsapp_chat'` and caught a class name. The decorator is typed `(module: ModuleSlug | ModuleKey)`, a compile-time control for §2 typos.
- **Server-only keys** are the four coarse keys, frozen on with no tenant toggle, so they are never refused (§5: N/A).
- **Client-only keys** are five. Two are portal slugs that the slug guard enforces through its portal map (read). Three are merchant-portal feature slugs, routed to security as possible UI-only gates, unverified.
- **3: 0. 6a: 0. 6b: 0.**
- **The loop (4)** over the 23 catalog keys found 8 with no gate reference. Five are coarse keys frozen on (Hardening). Three are purchasable extensions (`ads`, `ai_assistant`, `whatsapp_cloud`), so they are EN §4 candidates, unverified. Read step: `ads` is gated by permissions only, and `ai_assistant`'s only surface is a "Coming soon" package card (`feature-surface-scan` §4).

On `benchmarks/fixtures/launch-gaps` (2026-10-19, 0.2 s, `CAT_FILES` = its `modules.ts`), all 12 EN seeds print. 0b lists the two entitlement `APP_GUARD`s; 1a and 1b both ends of the seat and price disagreements; 2 the fail-open typo `advanced-reports` and the fail-closed `giftcards` among the server-only keys, beside `advanced_reports` and `loyalty_points` (§5); 3 both plan-name checks; 4 `ai_assistant 0` and `api_access 0`; 6a three price-id lines; 6b the summary handler. The split-guard decoy (`whatsapp_inbox`) prints in both key lists and the guard table clears it. The client-only list holds the routed `bulk_import` and `gift_cards`, the other end of the typo.

## The 3,000-hit path

1. **Write the guard table first.** List each global guard with the key family it judges and what it returns for a key it does not know. Every §2 row is decided against this table, never against one catalog.
2. **Write the source table.** For each plan fact (plan × resource), list every source that states it: copy, billing, catalog, seed, code constant. Two sources make one §1 group, however many lines they span.
3. **Group gates by key.** One key, many sites: one decision.
4. **Rank.** Rank first prices and paid limits (§1), fail-open keys (§2: a typo that the guard passes), and paid add-ons with no gate (§4), then UI dead ends (§5) and hard-coded plan names (§3).
5. **Read the top 30 groups**, both ends of each.
6. **Prefer the runtime bulk oracle at scale.** One parametrised test that walks the catalog (plan × key → server decision and UI visibility) settles every §2, §4 and §5 row at once (V419).
7. **Ledger the rest** as `Live, unreviewed (k groups / n hits)`, never `checked`.

## Scans for

| § | Class | Research id | Default severity |
|---|---|---|---|
| 1 | One plan fact (price, limit, included feature) with different values in two sources; two catalogs of one fact | PR-EN-1 | high on a price or a paid limit; medium on an included feature; Hardening for two equal copies |
| 2 | A gate names a key the catalog its guard reads does not hold | PR-EN-2 | high when the guard fails open on an unknown key; medium when it fails closed |
| 3 | A plan name hard-coded in a feature check outside the central plan map | PR-EN-3 | medium |
| 4 | A catalogued or advertised entitlement no gate enforces; a catalog key nothing reads | PR-EN-4 | medium; high for a paid add-on |
| 5 | The UI shows a feature the server refuses for the plan (a dead end after an upgrade prompt or on a lower plan) | PR-EN-5 | medium |
| 6 | Billing wiring: provider ids hard-coded in runtime source; an entitlement sync that reads the summary without paging or has no revoke path | PR-EN-6 | medium; high when the sync has no revoke path |

### 1. One plan fact, two values

**Class** PR-EN-1 · **Severity** high on a price or a paid limit; medium on an included feature; Hardening for two equal copies.

```
BAD:   marketing/pricing.json  "growth": { "seats": 10, "price": 99 }
       config/billing.ts       growth: { seats: 5, lookupKey: 'growth_monthly' }     // the gate reads 5
GOOD:  one plan module both the page and the gate import; the page renders from it
```

**Read the code:**

- Which source does the gate read, and which does the page render?
- Is the difference a grandfathered plan or a fair-use cap documented in the terms (§ 20)?
- Is "10k" the rounded form of 10,000 (§ 22)?
- For two equal copies of a catalog: does a test pin them together (a contract-not-redeclared test)? If so, it is Hardening; otherwise, the next edit splits them.

**Finding when** two sources state different values for one plan × resource.

**Proof:** a two-ended diff cites both lines (tier S). The matrix test asserts the page's number equals the gate's for every plan (V418).

### 2. Gate key outside the catalog

**Class** PR-EN-2 · **Severity** high when the guard fails open on an unknown key; medium when it fails closed.

```
BAD:   @RequireFeature('advanced-reports')   // catalog: 'advanced_reports'; the guard returns true for unknown keys
GOOD:  @RequireFeature(Feature.AdvancedReports)   — the key typed as the catalog union, so a typo fails tsc
```

**Read the code:**

- Which guard reads this metadata? Does another guard claim the key's family (§ 18)?
- What does each guard return for a key it does not know? Fail-open is high; fail-closed means the paid feature is dead.
- Is the parameter typed as the catalog union? Then a literal typo cannot compile, and the class is `controlled`.

**Finding when** no guard's catalog holds the key.

**Proof:** a catalog-driven test enumerates every gate key against the union of the guards' catalogs (V419). Typing the key as the union makes it a compile error (tier T).

### 3. Plan name in a feature check

**Class** PR-EN-3 · **Severity** medium.

```
BAD:   if (account.plan === 'enterprise') return { admitted: true };   // usage/quota.ts — outside the plan map
GOOD:  if (entitlements.has(account, 'unmetered_usage')) …           // the plan map grants the key
```

**Read the code:** Is this file the central plan map, the one place plans become keys (§ 19)? Is it a migration, a seed, an analytics label or an admin display? None of those are checks.

**Finding when** a feature decision outside the plan map names a plan.

**Proof:** a test that adds a plan to the catalog with the entitlement, and expects access, fails (V420).

### 4. Entitlement no gate enforces

**Class** PR-EN-4 · **Severity** medium; high for a paid add-on.

```
BAD:   MODULE_SLUGS includes 'ai_assistant' (purchasable) — no @ModuleGate('ai_assistant'), no client gate
GOOD:  every purchasable key has a server gate on every route that serves the feature, or is documented as cosmetic
```

**Read the code:**

- Is the feature gated by another mechanism? A permission is not an entitlement (§ Boundaries).
- Is it unreleased? Then its surface is `feature-surface-scan` §4.
- Is the key consumed by another service?
- Does a pricing bullet name a feature no key represents?

**Finding when** a paid key or advertised feature is reachable on a plan that does not include it.

**Proof:** the matrix test, run as a plan without the key, calls the feature's routes and expects 403 (V419).

### 5. UI shows what the server refuses

**Class** PR-EN-5 · **Severity** medium.

```
BAD:   <Button onClick={openExports}>Export</Button>     // no useEntitlement('exports'); POST /exports has @RequireFeature('exports')
GOOD:  the UI reads the same key: hidden, or shown with the upgrade path, on plans without it
```

**Read the code:** Does the UI gate through data (a route registry's `module:`, a nav config)? 2c reads the one-line form. Is the server key frozen on for every tenant (never refused)? Is the 403 caught and turned into an upgrade prompt on purpose?

**Finding when** a plan without the key sees the control and hits the refusal with no path forward.

**Proof:** an e2e or component test, run as that plan, expects the control hidden or the upgrade path shown (V419, tier L or U).

### 6. Billing wiring

**Class** PR-EN-6 · **Severity** medium; high when the sync has no revoke path.

```
BAD:   stripe.checkout.sessions.create({ line_items: [{ price: 'price_1NzQx2…', quantity: 1 }] })
       on 'entitlements.active_entitlement_summary.updated': grant(event.data.object.entitlements.data)   // ≤ 10; no revoke
GOOD:  stripe.prices.list({ lookup_keys: ['growth_monthly'] }) or per-mode config;
       the handler pages through `entitlements.url` and revokes keys absent from the summary
```

**Read the code:**

- Is the literal in a seed, a test or a per-mode config file (§ 21)?
- Does the handler page past the first 10 entitlements?
- Does it remove keys that disappeared, on downgrade and cancellation?
- Is there a `customer.subscription.deleted` path?

**Finding when** runtime code holds a mode-specific id, or the sync can grant and never revoke.

**Proof:** a static fact for a literal. For the sync, a Stripe test-mode trigger with more than 10 features, then a cancellation: `NOT-RUN (auth)` without a test key (V421).

## Proof

The oracles, failing first and green after the fix, are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Product: V418 (two-ended plan fact), V419 (catalog-driven gate matrix), V420 (plan-name independence), V421 (billing wiring).

The matrix test is the class's closing move: one parametrised test over plan × catalog key, asserting the server decision, the UI visibility, and the page's stated value. A fix that edits one gate and leaves the matrix unwritten closes a site, not the class.

The fix's regression set covers every variant (`/product-fix`):

- a limit, a price, an included feature, "unlimited" against a cap, and per-locale pricing copy;
- a typo that fails open, a typo that fails closed, and a key from the other guard's family;
- `===`, `in [...]`, `switch(plan)` and enum members;
- a gate only in the UI, and a gate on only one of two routes that serve the feature.

Any change to what a plan grants or costs is stop-and-ask.

## Output

```
entitlement-consistency-scan — lanes: home-grown TS (decorator + 2 APP_GUARDs), stripe 18.5 (apps/api/package.json)
Guards: CoarseModuleGuard (MODULE_KEYS, passes unknown), ExtensionGuard (MODULE_SLUGS, passes unknown) — split (§ 18)

Findings: 2 · Unconfirmed: 1

1. marketing/plans.json:14    ×  apps/api/src/billing/plans.ts:22                         [report-with-fix]   high
   §1 paid limit disagrees — the pricing page says growth includes 10 seats; the seat gate reads plans.ts
   growth.seats = 5. Proof: two-ended diff (both lines read); matrix test growth × seats expects 10 (fails).
   Fix: render the page from plans.ts; one value (stop and ask which number is the contract).
2. apps/api/src/reports/reports.controller.ts:31                                         [report-with-fix]   high
   §2 fail-open typo — @ModuleGate('advanced-reports'); neither guard's catalog holds it (MODULE_KEYS has
   'reports', MODULE_SLUGS has 'advanced_reports'), and both return true for unknown keys: every tenant gets the paid
   report. Proof: catalog test over every gate key (fails on this key). Fix: 'advanced_reports'; type the
   decorator parameter as ModuleSlug | ModuleKey.
3. apps/api/src/usage/limits.ts:15                                                       [report-flagged]    medium
   §3 plan name in a feature check — account.plan === 'enterprise'. Unproven link: whether a second unmetered plan
   is planned. Settling test: add 'enterprise_annual' with unmetered_usage to the catalog; expect admission.

Verification: 23 candidates → 2 findings · 1 unconfirmed · 6 hardening (equal catalog copies, coarse keys frozen
on) · 14 refuted (12 permission checks, 2 seed ids)

Class coverage:
  §1  value disagreement     checked (4 sources × 3 plans → 1 finding, 2 hardening)
  §2  gate key not in catalog checked (guard table: 2 guards; 71 sites / 13 keys → 1 finding)
  §3  plan name in a check   checked (2 hits → 1 unconfirmed; 1 inside the plan map)
  §4  ungated entitlement    checked (23 catalog keys → 0 findings; 5 frozen-on hardening, 3 read)
  §5  UI shows, server refuses checked (4 server-only keys → 0; frozen on)
  §6  billing wiring         checked (0 id literals; 1 sync handler → paging read, revoke present) · live: NOT-RUN (auth)
```

`[report-with-fix]`: both ends are read, every guard is accounted for, the oracle failed, and the fix is local. `[report-flagged]`: one link is unproven (a guard not read, a vendor catalog out of reach, an intended plan), and the row names it and the settling test.

The coverage block lists **all six** classes on every run:

- `checked (k hits → m findings)` when the greps ran on a present lane;
- `controlled (<typed key>)` when the gate parameter is the catalog union;
- `N/A (<reason>)` when there are no plans, no gates or no billing;
- `blocked (<reason>)` on an `rg` exit 2 or an unread guard;
- `NOT-RUN (auth)` for a vendor catalog or a live check.

## False positives / precedents

The verifier reads [`precedents/product.md`](../../../../snippets/precedents/product.md) § 18–22 and § 36–38 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Split guards** (§ 18). Read every guard first.
- **The central plan map is the entitlement layer** (§ 19). Plan names in migrations, seeds and labels are not checks.
- **Grandfathered and fair-use limits** (§ 20).
- **Billing ids in seeds and tests** (§ 21).
- **Marketing copy is read for numbers only** (§ 22).
- **Frozen-on keys.** A coarse key no tenant can switch off is never refused. Its missing UI gate is not §5, and its missing gate is Hardening, not §4.
- **Permissions are not entitlements.** A `can_*` check that no plan decides is security's.

## When to run

- On a diff that touches pricing copy, a plan file, billing config, a catalog, a guard, a gate decorator or hook, or a billing webhook.
- On every whole-repo `/audit-requirements --repo`, reporting all six classes. `launch-readiness` reads the ledger for PRR-EN-1.
- Before a pricing change, a new plan, or a switch from test-mode to live-mode billing.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/product.md`](../../../../snippets/precedents/product.md). Under `/audit-requirements --repo`, that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any §2, §4 or §5 row written before the guard table: every global guard, the key family it judges, and its answer for an unknown key.
- Halt on any row without both ends, or without "no counterpart after the written search" and the search written out.
- Do not call a vendor API with a live key, or any key the user did not provide for this run. Without a test-mode key, the live half is `NOT-RUN (auth)`.
- Do not propose a change to what a plan grants or costs. Stop and ask; the owner decides which source is the contract.
- Do not write into the scanned repo. The greps and loops read only.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/audit-requirements --repo` (this pack) dispatches this skill and folds its coverage block into the class ledger. `/product-fix` closes the findings failing-first with the matrix test.
- `feature-surface-scan` (this pack) owns the placeholder an unreleased entitlement shows. `launch-readiness` (this pack) reads EN rows for PRR-EN-1.
- Business `pricing-rule-scan` and `tax-invoice-scan` (when installed) own money. Security `@api-security-reviewer` and `logic-race-scan` (when installed) own client-only gates and limit races. Devops `progressive-delivery` (when installed) owns flags used for rollout.
