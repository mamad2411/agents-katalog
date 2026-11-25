---
name: publicist-japan-compliance
description: Japan press release compliance and legal guardrails, APPI, 特定電子メール法, 景品表示法, 業法, PRSJ指針, 日本心理学会指針. Use as mandatory compliance gate for all Japan earned media activities.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Japan compliance & legal guardrails, Japan market

**Scope**. Mandatory compliance checks for ALL Japan earned media activities. Pair with `publicist-japan` + all platform skills.

## Legal framework (must recheck at task time)

| Law/Regulation | Scope | Key Requirement | Escalation Trigger |
|---|---|---|---|
| **APPI** (個人情報保護法) | 記者/編集者/運営者の個人情報 | 目的特定・最小必要・告知・第三者提供制限・越境移転規制 | 海外CRM/モデル/メールに記者データ入力 |
| **特定電子メール法** | 商業性メール | 送信者表示・オプトアウト・事前同意(原則)・例外判定 | ピッチメールが「商業」と判定される場合 |
| **景品表示法** | 表示・広告 | 優良誤認・有利誤認・根拠なし実証不可 | 誇大表現/「No.1」「初」無根拠 |
| **業法** (金商法/薬機法/医療法/建設業法等) | 業界固有 | 事前確認・免許・届出・表現制限 | 金融/医療/薬事/建設/不動産/人材紹介等 |
| **PRSJ広報活動指針** | PR倫理 | 真実性・責任・公正・透明性・法令遵守 | 全活動の基準 |
| **日本心理学会研究リリース指針** | 学術/研究系 | 方法・限界明示・過大主張禁止・利益相反開示 | 研究成果プレスリリース |

## Personal information (APPI), journalist data

### What constitutes PI (個人情報)
- 記者/編集者: 氏名、所属、担当分野、連絡先(メール/電話/内線)、SNS、経歴、取材履歴、嗜好
- **判断基準**. 「特定の個人を識別できる情報」, 単体で識別不可でも組合せで識別可 = PI

### Cross-border transfer triggers
| Scenario | Status | Required Path |
|---|---|---|
| 海外CRM (Salesforce/HubSpot/Notion/Airtable) に記者名簿格納 | **越境移転** | 標準合同契約締結 + 個人情報保護委員会届出 + 本人個別同意 |
| 海外メール (Gmail/Outlook) で記者とやり取り | **越境移転** | 同上 |
| 海外LLM (OpenAI/Claude/Gemini) に記者プロフィール/過去稿入力 | **越境移転** | 同上 |
| 海外監視ツール (Meltwater/Cision/Muck Rack) 利用 | **プロセッサー越境** | 提供者の標準合同契約・認定確認 + DPA締結 |
| 国内ツール (飞书/钉钉/Line Works/自社オンプレ) | **非越境** | 追加手続き不要 (推奨) |

### Keep journalist data in Japan
記者データは日本国内のツールで管理し、越境移転を避ける。

## 特定電子メール法, pitch email compliance

### 商業性判定 (ガイドライン)
- **商業メール**. 営利目的の広告宣伝・勧誘
- **グレーゾーン**. 取材依頼メール, 「営利目的の勧誘」と解釈されるリスク
- **安全側**. 全ピッチメールを「商業メール」として扱い、要件充足させる

### Mandatory requirements
1. **送信者表示**. 氏名/名称、住所、電話番号、問い合わせ窓口
2. **オプトアウト**. 受信拒否の方法明示 (返信/リンク/電話)
3. **事前同意 (原則)**. 明示的オプトイン取得, 取材依頼では実質困難
4. **例外適用狙い**. 「取引関係存する者」への継続的送信, 初回ピッチでは使えない

### Practical template (compliant)
```
件名: 【取材依頼】〇〇について / 株式会社〇〇 田中太郎
本文:
田中太郎 様
株式会社〇〇 広報 田中太郎と申します。
[取材趣旨・価値・形式・日程候補]
---
【送信者情報】
株式会社〇〇 代表取締役 山田花子
東京都千代田区〇〇 〇〇ビル 5F
TEL: 03-xxxx-xxxx
本メールの配信停止は、このメールに「配信停止」とご返信ください。
```
**全ピッチメールに送信者情報+オプトアウト文言を必須付与**

## 景品表示法, claim substantiation

### 禁止表示
| Type | Example | Required Evidence |
|---|---|---|
| **優良誤認** | 「業界No.1」「日本初」「世界最高水準」 | 客観的調査データ(第三者機関/公的統計/自社調査で手法開示) |
| **有利誤認** | 「最安値」「最大割引」「期間限定半額」 | 価格比較対象・期間・条件の明示 |
| **実証なし** | 「効果実証済み」「専門家推奨」「90%が満足」 | 試験方法/サンプル/統計的有意性/第三者検証 |

### Safe claim language
- 避ける表現: 「業界初のAI搭載」
- 根拠を示した表現: 「弊社調べ(2024年○月、対象:〇〇社)では、同機能搭載製品として初めての発売となります」
- 避ける表現: 「医師が推奨」
- 発言者と所属を示した表現: 「〇〇医師(〇〇大学〇〇科)より、『本製品は〇〇の観点から有用』とのコメントをいただいております」

## Industry-specific regulations (業法), quick reference

| Sector | Key Law | Common Pitfalls |
|---|---|---|
| **金融/投資** | 金商法 | 確実利益保証/リスク軽視/未登録勧誘/パフォーマンス誇大 |
| **医療/健康** | 薬機法/医療法 | 効能効果保証/医師免許なし診断/未承認薬機/美容医療広告規制 |
| **食品/サプリ** | 食品表示法/健増法/景表法 | 機能性表示食品届出なし/疾病治療効果暗示/「無添加」根拠なし |
| **化粧品** | 薬機法/化粧品基準 | 医薬品的効能/「ナノ」「幹細胞」無根拠/動物実験表記 |
| **不動産** | 宅建業法 | 重要事項説明漏れ/誇大広告/二重価格/未完成物件完成保証 |
| **人材/派遣** | 職安法/派遣法 | 手数料不明示/虚偽求人/派遣先責任曖昧 |
| **建設/工務店** | 建設業法 | 許可番号未表示/請負契約不備/下請け適正化 |

**Rule**. 業法該当セクター → `NEEDS_REVIEW` + 該当業法専門弁護士確認必須

## PR ethics & professional standards

### PRSJ 広報活動指針 (抜粋)
1. **真実性**. 虚偽・誇大・隠蔽なき正確な情報提供
2. **責任**. 発言・行動の責任主体明確化
3. **公正**. 利害関係者間の公平・差別なき対応
4. **透明性**. クライアント・利益相反・スポンサーシップ開示
5. **法令遵守**. 全関連法令・ガイドライン順守

### 日本心理学会 研究プレスリリース指針
- 方法・対象・限界・統計的有意性・効果量・再現性・利益相反・倫理審査, 全て明記
- 「画期的」「世界初」「画期的治療」等の過大表現禁止
- メディア向け: 専門用語平易化・誤解防止・バランス提示

## Compliance checklist (per pitch/release)
- [ ] **APPI**. 記者データ越境なし / 国内ツール完結 / 個別同意記録
- [ ] **特定電子メール法**. 送信者情報+オプトアウト文言全メール付与
- [ ] **景品表示法**. 全クレーム根拠資料紐付け / 誇大表現排除
- [ ] **業法**. 該当セクター確認 / 専門弁護士 `NEEDS_REVIEW` 完了
- [ ] **PRSJ指針**. 真実/責任/公正/透明/法令, 全項目クリア
- [ ] **分類表示**. `editorial` / `企業供稿` / `付费合作` / `分发` 明示
- [ ] **AI標識** (該当する場合): 明示・非表示の標識 (参照 `publicist-japan-ai-compliance`)

## Avoid
- 記者の個人情報だから名簿売買してよいと考えると、APPIに違反する。
- 取材依頼は商業メールではないと決めつけると、法的リスクがある。
- 根拠なく競合より優れていると主張すると、景品表示法上の優良誤認に当たる。
- 金融商品の元本保証や確実な高利回りをうたうと、金商法に違反する。
- 化粧品に「シワが消える」と表示すると、薬機法上の医薬品的効能に当たる。
- 研究成果を「世界初の画期的治療法」と誇張すると、日本心理学会の指針に反する。

## References
- `https://www.ppc.go.jp/en/legal/`, PPC APPI英語版
- `https://www.japaneselawtranslation.go.jp/en/laws/view/3767/en`, 特定電子メール法英訳
- `https://www.caa.go.jp/policies/policy/consumer_policy/`, 消費者庁 景表法
- `https://prsj.or.jp/pr-guideline/`, PRSJ指針
- `https://psych.or.jp/jpamember/press_release_guidelines/`, 日本心理学会指針
- `skills/publicist-japan/references/law-and-ethics.md`
- `skills/publicist-japan/references/sources.md`

## What this skill does not do
- NG No legal advice (escalate to Japan-qualified counsel)
- NG No automated compliance checker
- NG No MCP/CLI tools (reference only)
