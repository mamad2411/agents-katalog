---
name: trial-listing-draft
description: "Draft or review an employer's Otameshi Tenshoku listing so a candidate can decide whether to apply: check item by item that the work, deliverable, out-of-scope tasks, required experience, support, hours, schedule, location, compensation, contract form and payment timing are stated, find open-ended, unpaid-company-work, guarantee, personal-attribute and unverifiable wording, and confirm that the hours, weekly availability, period, rate and budget hold together. Use when a hiring manager, recruiter or small-business owner wants a listing written from a plan, wants an existing draft or published listing reviewed before or after posting, or wants to know why applications are not coming; do not use to design the work itself (trial-work-design), to reply to applicants (applicant-reply), to state market rates, legal, tax or service conditions from memory, or to post or update the listing on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：募集文の作成と掲載前の点検

企業の課題と受け入れ計画から、候補者が応募を判断できる募集文を作る。書き手の側から、任せる作業、成果物、対象外、必要な経験、支援、時間、場所、報酬、契約形態、支払時期が書かれているかを項目ごとに確かめ、範囲の閉じていない表現、無償の実務、採用の保証、職務と無関係な属性、根拠のない訴求を見つけ、実働・週の稼働・期間・単価・予算が同時に成立するかを確かめる。応募が集まるかの予測、相場・法令・サービス条件の記憶による断定、企業の魅力や条件の創作、掲載や更新の代行は行わない。

## 進め方

1. 募集の種類（有償業務か無償の見学・学習か）、対象（経験者か未経験者か）、原稿の段階（社内検討用か、掲載用の下書きか、掲載済みの点検か）を利用者の発言と原稿から読む。**企業の実務を担うなら経験にかかわらず有償業務として書く。** 決まっていなければ、それを最初の確認事項にし、決まっている部分から着手する。
2. 実働・期間・報酬の数字があるか確かめる。`trial-work-design` の計画があればそれを使う。なければ、利用者の発言から仮置きし、仮置きであることを本文に持ち込まない。**単価を相場で埋めない。**
3. [募集文に書く項目と表現](references/listing-items.md) の一覧に沿って、既存の原稿があれば項目ごとに記載の有無を記録し、なければ利用者の発言から埋められる項目と埋められない項目を分ける。「一式」「随時」「納得いくまで」は言い換えず、範囲が閉じていない表現として残す。
4. `python3 scripts/check_listing.py <input.json>` で、項目の記載状況、本文の表現、計画の数字の整合、掲載前に解消する点を機械的に出す。入力形式は [募集文に書く項目と表現](references/listing-items.md#スクリプト入力) を見る。**本文全体は出力に載らず、一致した表現だけが返る。**
5. 掲載可否、料金、契約成立、支払主体、募集の表現に関する規制が本文の内容に関わる場合は、[公式情報の確認](references/source-checks.md) で一次情報を確認する。確認できない条件は本文に書かず、確認事項として残す。
6. [報告書形式](references/report-format.md) に従って、項目の記載状況、表現の点検、数字の整合、内部検討用と掲載用に分けた下書き、掲載前に解消することを出す。掲載済みの点検なら、下書きは修正案として出す。

## 判断上の制約

- 候補者が応募を判断できる情報を優先する。企業の魅力を先に書かない。魅力を書くなら、候補者が確かめられる事実（何をしている会社か、誰が受け入れるか、どう支援するか）で書く。
- 利用者の発言と計画にないことを書かない。企業の実績、社風、採用後の条件、候補者の実績を創作しない。
- 実働、週の稼働、期間、単価、予算は同時に成立させる。成立しない組み合わせは、どれを変えるかの選択肢を並べ、利用者が選ぶまで本文に3つを同時に書かない。
- 未経験者向けに無償で提供できるのは見学・説明・架空データによる模擬課題までである。実務を任せるなら有償業務として書く。無償体験を有償業務への応募の前提にしない。
- 採用や継続を保証しない。体験後の判断は双方に残ることを書く。
- 職務と無関係な属性（性別、年齢、婚姻、国籍など）で絞らない。雇用と業務委託で規制の適用は違うが、どちらでも職務要件に置き換える。適用の有無を記憶で断定しない。
- 応募が集まるか、何人来るかを予測しない。点検の結果が良くても、掲載を勧める結論を書かない。
- 社内案・未確認の条件を確定条件として本文に書かない。
- このスキルだけで使える。計画、社内説明、契約条件、応募者対応の各スキルがなくても、今回の募集文は完結する。

## 個人情報と権限境界

このスキルは募集文の作成と点検のみを行う。求人の掲載・更新・取り下げ、応募者への連絡、日程確定は、操作を依頼されても利用者本人が行う。掲載前に、本文、掲載先、掲載期間、未確定の条件を示して引き渡す。ログイン情報を求めない。

募集文には、受け入れ担当者の氏名や連絡先、顧客名、社内の非公開情報を必要以上に入れない。掲載済みの募集文を点検する場合も、本文全体を出力に載せず、一致した表現と直し方だけを返す。利用者が明示的に求めない限り、原稿・入力・結果をファイル保存しない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
