---
name: trial-work-design
description: "Design what an employer will have a candidate do during an Otameshi Tenshoku trial: turn a business problem into a bounded paid assignment or an unpaid learning visit, with scope, completion criteria, candidate hours, company staff hours, duration, compensation and change conditions, and check the planned cost against the budget. Use when a hiring manager, recruiter or small-business owner wants to decide what work to offer, how much time it takes, what it costs, or how to adjust a plan when materials are late or the scope grows; do not use to write the public listing (trial-listing-draft), to reply to applicants (applicant-reply), to state market rates, legal, tax or service conditions from memory, or to post, contact or contract on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：受け入れる仕事の設計

企業が何に対していくら支払い、どの程度の仕事を期待できるかを検討できる計画を作る。解決したい課題を、候補者が期間内に完結できる有償業務か、未経験者向けの無償の見学・学習に変え、範囲、完了基準、候補者の実働、企業担当者の工数、期間、報酬、変更条件を揃える。専任の採用担当者、現場のマネージャー、小規模企業の経営者のいずれからでも、課題のメモ、予算、受け入れ体制の発言から着手する。候補者の適性や採用の成否の判定、相場・法令・サービス条件の記憶による断定、掲載や連絡の代行は行わない。

## 進め方

1. 解決したい課題、今回確かめたい能力・協働、予算、期限、受け入れ担当者の時間、候補者の作業経験と稼働時間を利用者の発言から拾う。不足を全件質問して止めず、仮案と、判断を変える少数の確認事項を返す。
2. 任せる作業に対する候補者の経験と、企業が提供する支援を確認する。肩書きや年数だけで区切らない。未経験者には見学・学習・模擬課題の無償体験を候補にし、経験者には経験を活かす有償業務を提案する。**企業の実務を担うなら未経験でも有償枠にする。** 無償体験を有償業務への応募の必須条件にしない。
3. 依頼に応じて必要な参照だけを読む。

| 依頼 | 参照と成果物 |
| --- | --- |
| 未経験者の見学・学習を受け入れたい | [学習体験](references/learning-trial.md)：学習目的、活動、時間、担当者、説明と振り返りの計画 |
| 有償の仕事を設計・調整したい | [有償業務](references/paid-work.md)：範囲、完了基準、仕事量、期間、企業の準備、報酬、変更条件 |
| 料金・契約・支払い・無償掲載可否が判断に関わる | [公式情報の確認](references/source-checks.md)：出典と時点、説明の差、確認先と質問 |

4. 作業と時間が置けたら、`python3 scripts/plan_trial_work.py <input.json>` で、候補者の実働と企業担当者の工数、期間に配置したときの週あたりの実働、予定費用と予算との差を機械的に出す。入力形式は [有償業務](references/paid-work.md#スクリプト入力) を見る。**予算に合わせて実働を削らず、説明や会議を無償枠へ移して帳尻を合わせない。** 予算が足りなければ範囲縮小・予算増額・期間変更を並べ、期間だけ延ばしても総額が変わらないことを示す。
5. 資料の遅れ、追加の修正、範囲の拡大など計画の変更は、既存の範囲との差、追加の実働・費用・日程を示し、候補者に提示する前の案として返す。待ち時間の扱いは契約と拘束の実態で確認し、候補者だけに遅れを負わせない。
6. 計画の各条件を企業案／候補者希望／提示済み／双方合意／未確認に分け、合意には根拠を添える。計画が固まったら、募集文は `trial-listing-draft`、社内の予算説明は `trial-budget-brief`、契約条件の明示は `trial-contract-terms` に渡せる形で、範囲・時間・報酬・変更条件を一覧にして締める。導入されていなくても、この計画だけで受け入れ準備は進められる。

## 判断上の制約

- 予算に合わせて業務を具体化するが、企業の満足や採用結果を支払いの恣意的な条件にしない。未経験を理由に実務を無償化しない。
- 未確認の条件をゼロ・適合・合意済みに置き換えない。サービス条件、相場、法令・税務は必要時に一次情報を確認し、個別の専門的判断や採用の成否を断定しない。
- 売上や件数など候補者が制御できない結果を完了基準にしない。「納得するまで」のような上限のない修正条件は、確認できる品質と有限の修正範囲に具体化する。
- 企業担当者の説明・レビュー・振り返りの時間を計画から落とさない。候補者の実働と企業の工数は別の数字として持ち、合算しない。
- このスキルだけで使える。募集文、応募者対応、契約条件、振り返りの各スキルがなくても、今回の仕事の設計は完結する。

## 個人情報と権限境界

このスキルは相談・分析・計画の作成のみを行う。求人の掲載・更新、応募者管理の更新、候補者への連絡、日程確定、契約・採用通知、キャンセル、支払い、レビュー公開は、操作を依頼されても利用者本人が行う。対象・下書き・希望時期・操作の影響・未確認条件を示して引き渡す。ログイン情報を求めない。

候補者の氏名、連絡先、職歴、選考状況、企業や顧客の秘密は必要最小限だけ扱う。候補者を比較する場合は仮名を使い、他候補者の情報や内部評価メモを計画に混ぜない。利用者が明示的に求めない限り入力・計画・結果をファイル保存しない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
