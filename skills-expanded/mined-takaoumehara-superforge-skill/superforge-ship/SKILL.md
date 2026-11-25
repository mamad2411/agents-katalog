---
name: superforge-ship
description: >
  Decide whether a product may be released, a different question from whether
  it works. Runs the release gate: which legal obligations the product's own
  data handling triggered and where a lawyer becomes mandatory, what will
  actually get it rejected from the App Store or Google Play, the measurement
  that must exist before launch because it cannot be recovered afterwards, the
  ability to stop a bad release, and whether you will find out when it breaks —
  monitoring, a tested rollback, a backup someone has actually restored. Ends
  in a single verdict — SHIP / BLOCK / RISK-ACCEPTED — never prose. Use when
  the user says "ship it", "release", "launch", "submit to the App Store", "app
  review", "rejected", "privacy policy", "terms of service", "GDPR",
  "compliance", "can we release this", "monitoring", "backup", "rollback",
  "出荷", "リリース", "公開", "ローンチ", "審査", "リジェクト",
  "プライバシーポリシー", "利用規約", "個人情報", "特商法", "監視",
  "バックアップ", "障害対応", "出せる状態か", or runs /superforge-ship.
license: MIT
metadata:
  author: Takao Umehara
  version: "2.0"
compatibility: >
  Standalone.
  Reads docs/verification.md and docs/security.md as preconditions, plus
  docs/business-model.md, docs/accessibility.md, and docs/design.md when
  present. Writes docs/ship-readiness.md.
  Not a substitute for legal advice — it identifies which obligations exist and
  where professional counsel becomes mandatory. It does not draft legal text.
---

# Superforge Ship — the release gate

`superforge-verify` answers **"does it work?"** with runtime evidence. This
skill answers a different question that has stopped more launches:

> **"Are we allowed to release this, and will we be able to tell what happened
> after we do?"**

A product can pass every test and still be unshippable — because it collects
data it never disclosed, because the store will reject it for a reason nobody
checked, because there is no way to turn it off if it goes wrong, or because it
ships with no instrumentation and the first month produces feelings instead of
facts.

---

## 0. The gate rule

**Never report "ready to ship" as prose.** End every run with one code:

| Verdict | Meaning |
|---|---|
| **`SHIP`** | Every blocker below is cleared, or explicitly does not apply, with the reason recorded |
| **`BLOCK`** | At least one blocker is unresolved. Name it, name what clears it, stop |
| **`RISK-ACCEPTED`** | A known gap is being shipped deliberately. Requires: what the gap is, what it could cost, who decided, and when it gets fixed. **Undated risk acceptance is just `BLOCK` with better manners** |

A gate that always returns `SHIP` is decoration. If nothing has ever come back
`BLOCK`, the checks are not being run.

---

## 1. Legal — what the product's own behaviour has triggered

The single fact that makes this checkable rather than infinite:

> **Jurisdiction follows your users, not your address.** A developer in New
> York, in Tokyo, or anywhere else faces the same obligations, determined by
> where the people using the product are and what data is touched.

That is why this gate is universal, and why "I'm not in Europe" is never the
answer to a GDPR question — one EU user is enough.

Work in this order, always: **what data does it touch → who does that reach →
what does that oblige → what must be visible before launch.**

The trigger tables — data categories, regional triggers, sensitive-category
escalation, children, subscription disclosure, and the explicit list of
situations where a lawyer stops being optional — are in
**`references/legal-triggers.md`**.

**This skill identifies obligations. It does not draft legal documents.**
Generating a privacy policy from a template is how a product ends up with a
document that describes someone else's data practices. Establish what is true
about *this* product first; the drafting is a separate job, and above a certain
risk line it is a lawyer's job.

---

## 2. Store review and platform gates

Most rejections are not surprises. They are the same short list, and every one
of them is checkable before submission.

| Gate | The check | Usually fails because |
|---|---|---|
| **Privacy policy URL** | Publicly reachable, no login, loads today, matches actual behaviour | It 404s, or it describes a different app |
| **Data disclosure form** | Apple's privacy labels / Google Play Data Safety filled from what the code actually does | Filled from memory. **Any third-party SDK that phones home counts as your collection** |
| **Tracking consent** | If an advertising identifier or cross-app tracking is used, the platform consent flow is present and honoured | An SDK enables it by default and nobody checked |
| **Account deletion** | If the product creates accounts, deletion must be reachable *in-product*, not only by email | Deletion exists in a support inbox and nowhere else |
| **Subscription terms** | Price, period, renewal behaviour, and cancellation visible **before** purchase | The paywall shows the price and hides the renewal |
| **Demo access** | Working credentials or a demo mode for reviewers behind any login | The reviewer cannot get past the first screen |
| **Broken or placeholder content** | Nothing ships with lorem ipsum, dead links, or an unimplemented button | The last 5% was going to be a fast follow |
| **Permission strings** | Every requested permission has a specific reason string, not a generic one | 「この機能を使うために必要です」 explains nothing and gets flagged |
| **Accessibility** | See §3 — in some markets this is now law, not polish | Nobody ran it |

**Rejections are cheap; rejection loops are not.** Each round costs days of
calendar time, so clearing all of these in one pass is worth more than it looks.

Web releases have their own version of this list: a reachable privacy policy,
a cookie/consent mechanism if any non-essential tracking exists, working
unsubscribe paths, and accurate pricing disclosure before checkout.

---

## 3. Accessibility is now a release gate in some markets

This stopped being a quality question. Where an accessibility statute applies
to the product's market and category, a failing product is a legal exposure,
not an imperfect one.

Do not restate criteria here. **`superforge-a11y`** owns the ledger and writes
`docs/accessibility.md`. This gate reads that file and asks one thing: does it
exist, is it current with the release, and are the failures at a level the
applicable rules tolerate? A missing `docs/accessibility.md` at ship time is a
`BLOCK`, not a `RISK-ACCEPTED` — you cannot accept a risk you have not measured.

Which markets and which categories → `references/legal-triggers.md`.

---

## 4. Measurement that cannot be added later

Some data is only collectable going forward. Ship without it and the first
weeks are unrecoverable — you will never know how the launch actually went,
only how it felt.

Instrument before release:

1. **Activation** — the first real outcome from
   `superforge-ui/references/first-run.md` §1, as an event. Without it, every
   later conversation about the funnel is guesswork.
2. **The paywall or conversion moment** — reached, viewed, converted, dismissed,
   as separate events. One aggregate "conversions" number cannot be debugged.
3. **Retention cohorts by signup date.** Retention computed retroactively from
   a table that only stores current state is not retention.
4. **Errors and crashes, with a version tag.** A crash you cannot attribute to
   a release is noise.
5. **Attribution: "how did you hear about us."** One field, asked once. Without
   it, `superforge-biz`'s CAC math is impossible forever.

What to measure, what each number is allowed to decide, and the post-launch
loop that turns week one into decisions → **`references/launch-metrics.md`**.

Keeping it running afterwards — the alert that is worth having, the deploy path,
the backup restore drill, the incident order, and the runaway-bill alert →
**`references/operations.md`**.

**Instrumenting is itself a data-collection decision.** Anything added here
loops back to §1 — analytics that identify individuals changes what must be
disclosed. Run the two together, not in sequence.

---

## 5. Can you stop it?

A release you cannot reverse is a bet, not a launch.

- **Rollback path.** Web: how do you get the previous version back, and how
  long does it take? Mobile: you cannot un-ship a binary — so anything risky
  needs a server-side switch, and that switch must exist *before* the risky
  thing does.
- **Kill switch for the risky part**, specifically. Not the whole app — the one
  feature most likely to go wrong.
- **A path for people to tell you.** An in-product contact route that reaches a
  human. A store review is not a support channel, and it is where the report
  goes when there is no alternative.
- **Someone is watching.** For the first 48 hours, name who is looking and at
  what. "We'll see how it goes" means nobody.

---

## 5b. Security — the review, not the feeling

A release gate that never asks whether a logged-in user can read someone else's
data is not a gate. **`docs/security.md` is a precondition here, on the same
footing as `docs/verification.md`**: missing means `BLOCK`, and an unresolved
Critical finding means `BLOCK` regardless of everything else on this page.

Do not restate the checks — run **`superforge-secure`** and read its verdict.
One ledger, one set of findings. The verdict codes are `SECURE-REVIEWED` /
`FINDINGS-OPEN` / `NOT-ASSESSED`; the word "secure" is never a claim.

---

## 5c. Operations — will you find out, and can you get it back

The three questions below are the ones that turn a launch into something
survivable, and all three are cheap before launch and impossible after:

- **Detection.** If it goes down at 3am, how do you learn about it other than a
  user writing in? One alert on a URL that touches the database.
- **Reversibility with a tested rollback** — §5's path, actually run once.
- **A backup that has been restored.** An untested backup is a belief about a
  file, not a backup.

**These three are `BLOCK` conditions for any product holding user data.**
Monitoring, alerting that you will act on, the deploy path, backups and their
restore drill, incident order, and cost control including the runaway-bill
alert → **`references/operations.md`**.

---

## 6. Running the gate

1. Read `docs/verification.md`, `docs/security.md`, `docs/business-model.md`,
   `docs/accessibility.md`, and `docs/design.md` if they exist. Do not re-ask
   what is already written down.

   **`docs/verification.md` and `docs/security.md` are preconditions, not
   references.** This gate assumes the thing works and that someone has looked
   at whether a user can reach another user's data. If either file is missing,
   `superforge-verify` or `superforge-secure` has not run and there is nothing
   to decide about releasing yet — return `BLOCK` with that as the blocker
   rather than assessing the rest.
2. Determine what data the product actually touches — **from the code and its
   dependencies, not from memory.** Third-party SDKs are the usual source of a
   disclosure that turns out to be false.
3. Run §1 triggers, §2 platform gates, §3 accessibility, §4 instrumentation,
   §5 reversibility, §5b security, §5c operations.
4. Write `docs/ship-readiness.md` with one verdict code and, for every
   unresolved item, the specific thing that clears it.
5. If anything is `RISK-ACCEPTED`, the date and the owner go in writing.

## Artifact

```markdown
# Ship readiness — <product> <version>

> Written by: superforge-ship · Last updated: <YYYY-MM-DD>
> Verdict: SHIP / BLOCK / RISK-ACCEPTED

## Verdict and why
<一行。BLOCK なら、何が塞いでいて、何があれば解けるか>

## Data the product touches
| データ | どこから | 誰に渡るか | 発火した義務 |
<コードと依存関係から。記憶からではなく>

## Legal triggers
| 法域/規則 | 発火したか | 根拠 | 対応状況 | 弁護士が要るか |

## Platform gates
| ゲート | 状態 | 未達なら、何をすれば通るか |

## Accessibility
docs/accessibility.md: 有 / 無 · 最終更新 · 未対応の重大項目 <n>

## Security
docs/security.md: 有 / 無 · 判定 <SECURE-REVIEWED / FINDINGS-OPEN / NOT-ASSESSED> · 未解決 Critical <n>

## Instrumentation before launch
| 指標 | 実装済み | この数字が決めてよいこと |

## Reversibility
ロールバック手段 · キルスイッチ · 連絡経路 · 最初の48時間を見る人

## 4b. AI & Generative Search Discoverability (AEO / GEO)

Before shipping any public product surface or documentation:
- **`llms.txt` & `llms-full.txt` Generation**: Produce clean Markdown summary files in the root directory for AI search crawlers (Perplexity, SearchGPT, Claude, Gemini).
- **Structured Data (JSON-LD)**: Validate Schema.org tags (`SoftwareApplication`, `Organization`, `FAQPage`).
- **Generative Citation & Fact Density**: Verify explicit technical headers and quantitative details for AI reference indexing.

See detailed criteria → **`references/aeo-geo-standards.md`**.

## Operations
検知（アラート1本と行き先） · ロールバックを試した日 · 復元を試した日と実測時間 · 請求アラートの閾値 · **llms.txt の存在と出力**

## Risks accepted
| 内容 | 起こりうる損害 | 決めた人 | いつ直すか |
<期限の無い受容は BLOCK と同じ>
```

## Quality check — ask these after the run

- 判定は SHIP / BLOCK / RISK-ACCEPTED のいずれか1つになっているか。文章で濁していないか
- 「触れているデータ」はコードと依存関係から確認したか。記憶や思い込みで書いていないか
- サードパーティSDKが送信しているものを、自分の収集として数えたか
- プライバシーポリシーのURLは、今この瞬間に、ログイン無しで開けるか
- 法域の判定を「開発者の居住地」でしていないか。ユーザーの所在で見たか
- 弁護士が必要な領域（`references/legal-triggers.md` の停止条件）に入っていないか
- `docs/accessibility.md` は存在し、このリリースの内容と一致しているか
- 後から取れない計測を、出す前に入れたか
- 問題が起きた時に止められるか。止め方を書いたか
- RISK-ACCEPTED に、損害の想定・決めた人・直す期限がすべて入っているか

## Delegate when a sharper skill is installed

`legal`, `privacy-policy`, `privacy-manifests` (document drafting, once §1 has
established what is true) · `superforge-a11y` (the accessibility ledger itself)
· `security`, `harden`, `security-review` (threat surface before release) ·
`app-store`, `product-page-optimization`, `screenshot-planner` (store listing
craft) · `error-monitoring`, `logging-setup`, `ci-cd-setup` (the
instrumentation in §4) · `release-review` · `superforge-verify` (does it work —
run that first; this gate assumes it passed).
