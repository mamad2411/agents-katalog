---
name: publicist-japan-kishaclub
description: Use Japan's Kisha Club system for press-release drops, briefed distribution, press conferences, coordinating firms, and membership or access decisions.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Kisha Club (記者クラブ), Japan market

**Scope**. Japan's unique press club system for press release distribution and press conferences. Pair with `publicist-japan`.

## Club system overview
- **~800 clubs nationwide** -- each tied to a ministry, agency, industry body, or major corporation
- **Japanese unique** -- no direct equivalent overseas (White House press corps is different)
- **Core function**. Journalists share a physical base (記者室) inside the institution for efficient, fair information gathering
- **Membership**. Newspapers, TV, wire services (通信社) -- freelancers, web media, foreign media often excluded
- **Criticism**. Closed/cartel-like; recent オープン化 pressure but slow progress

## Club types & major examples

| Type | Major Clubs | Typical Use |
|---|---|---|
| **業界・経済団体** | 兜倶楽部(上場/証券/運用)、東商記者クラブ(流通/小売/通販/食品)、重工業研究会(鉄鋼/化学/非鉄/製薬/化粧品)、本町記者会(医療/薬剤)、日銀金融記者クラブ(銀行/保険)、自動車産業記者会 | Corporate earnings, new products, financial policy, industry regulation |
| **官公庁** | 永田クラブ(内閣記者会)、霞クラブ、各省庁記者クラブ | Policy announcements, administrative guidance, stats releases |
| **政党** | 平河クラブ(与党)、野党クラブ | Party policy, election pledges |
| **地方・府県** | 都道府県庁記者クラブ(大阪/愛知/福岡等) | Regional policy, local corporate news, disaster response |
| **外国特派員** | 日本外国特派員協会(FCCJ) | Foreign media access |

## 投げ込み (Press release drop) -- core distribution method

### Pre-requisite: eligibility check
- **Industry body membership required** -- e.g., 東商記者クラブ needs 東京商工会議所会員
- **Non-member companies** --> often rejected for commercial announcements
- **Public agencies** --> only high-public-interest releases accepted
- **Verify**. Check `広報・マスコミハンドブック (PR手帳)` or call 幹事社

### Step-by-step process

#### 1. Identify target club
- Match release topic to club jurisdiction (industry/ministry/region)
- One release may need multiple club drops

#### 2. Contact 幹事社 (Rotating Secretariat)
- **Role**. Club operations coordinator, external liaison
- **Confirm**. 投げ込み方法 (physical/email), 必要部数 (member count + buffer), 可能日時, 郵送可否, 挨拶可否
- **Note**. Rules vary by club -- never assume

#### 3. Execute drop
| Method | Procedure |
|---|---|
| **物理持参** (traditional) | 指定部数持参 --> 受付/幹事社に渡す --> 各社棚/ポストに配置 --> 幹事社にお礼 |
| **メール一括配信** (post-COVID standard) | 幹事社から配信先リスト入手 --> 件名/本文簡潔 + PDF添付 --> 送信 --> 完了確認連絡 |

#### 4. Optional enhancements
- **レク付き配布** (Briefing + Drop): 説明付き配布 -- 幹事社了承必須、記者と直接コミュニケーション可能
- **記者会見** (Press Conference): 企業トップ(役員以上)が直接発表 -- 幹事社承諾必須、主要クラブ(兜/東商/日銀)で開催多い

## Pitch protocol for club context

### Physical drop etiquette
- **名刺交換**. 幹事社/受付担当者と -- 「顔が見える関係」構築の機会
- **補足資料**. 写真、会社案内、サンプル -- 手渡し可能なら持参
- **部数**. 加盟社数 + 予備 2-3部

### Email drop etiquette
- **件名**. `[クラブ名] 投げ込み：[件名]` -- 20字以内で「何/なぜ今」
- **本文**. 簡潔なリード + PDF添付 + ブリーフィング希望明記
- **差出人**. 個人名 + 会社名 (「株式会社〇〇 広報 田中太郎」)

## Compliance & restrictions

### Access restrictions
- NG フリーランス/ウェブメディア/外国メディア --> 多くのクラブで加盟不可
- NG 非会員企業 --> 業界団体クラブ利用不可
- NG 営利目的リリース --> 官公庁クラブで拒否されること多い
- OK **併用必須**. クラブ外メディア(フリーランス/ウェブ/専門誌)へ個別配信も並行

### Anti-patterns
- NG 幹事社確認なしで独自判断投げ込み
- NG 指定部数不足 / 過剰
- NG ルール無視 (郵送不可クラブに郵送、挨拶禁止クラブで挨拶)
- NG クラブ依存のみ -- 個別メディアアプローチと併用が鉄則

## References
- `wiki/public-relations/japan-press-clubs-and-foreign-access.md`
- `wiki/public-relations/japan-pr-wire-and-release-quality.md`
- PR TIMES MAGAZINE "記者クラブとは？活用方法や投げ込みの仕組み"
- 共同通信PRワイヤー "記者クラブとは？組織の役割と投げ込み方法を解説"
- LC広報 note "第26回:記者クラブの仕組みと活用方法"
- 日本新聞協会 "記者クラブに関する編集委員会の見解" (2002/2006)

## What this skill does not do
- NG No club membership database (verify per club)
- NG No automated drop (physical/email requires human coordination)
- NG No guaranteed coverage (drop != article)
- NG No MCP/CLI tools (reference only)
