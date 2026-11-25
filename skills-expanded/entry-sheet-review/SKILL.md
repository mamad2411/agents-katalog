---
name: entry-sheet-review
description: Review and revise Japanese job-application documents (entry sheets, rirekisho, shokumu-keirekisho) by checking each answer against the question asked, the stated character limit, and the evidence the applicant can actually support, then propose concrete rewrites the applicant decides on. Use when a user wants an ES or resume answer critiqued, tightened, or drafted from their own experience; to assemble a whole shokumu-keirekisho from an experience inventory, use resume-draft instead; do not use to invent experience, to judge pass or fail probability, or to submit an application.
license: MIT
metadata:
  author: ficilcom
---

# エントリーシート・応募書類の添削

新卒の就職活動と中途の転職応募の両方で、応募書類の各設問について「設問に答えているか」「事実で裏づけられているか」「制限文字数に収まっているか」を分けて確認し、利用者が選べる具体的な改稿案を出す。合否の予測、経験の創作、応募の代行は行わない。

## 進め方

1. [受け取りと確認事項](references/intake-and-method.md) を先に読み、利用者が渡した原稿と募集要項を質問より先に確認する。設問文、制限文字数、提出期限、応募区分（新卒・中途）、応募企業と職種を固定する。募集要項が手元にない項目は `unknown` として扱い、推測で埋めない。
2. `python3 scripts/check_entry_sheet.py <input.json>` で設問ごとの文字数、長い文、数値の有無、冗長表現の候補を機械的に測る。入力形式は [受け取りと確認事項](references/intake-and-method.md#スクリプト入力) を見る。文字数の数え方が未確認のうちは、上限ぎりぎりへの調整を確定させない。
3. 各設問について、まず「設問に答えているか」を判定する。設問が聞いていること（行動か、動機か、志望理由か、再現性か）と、原稿が実際に書いていることのずれを明示する。文章のうまさより先にこのずれを直す。
4. 主張ごとに、利用者が示した事実、利用者の記憶による報告、推定、不明を区別する。数値・期間・役割・成果は出典を確認し、確認できないものを断定形に書き換えない。原稿にない経験、実績、資格を提案として作らない。
5. 改稿は「削る」「言い換える」「事実を足す」に分けて提示する。削減案は削る根拠（重複、抽象語、設問と無関係）を添える。事実を足す案は、利用者に確認する質問の形で出し、こちらで埋めない。
6. [報告書形式](references/report-format.md) に従って、設問ごとの判定・優先度・改稿案・利用者への確認事項を出す。最終稿は利用者が選んだ案から組み立て、変更点と残った不明点を明記する。

## 判断上の制約

- 経験、数値、役職、資格、志望動機を創作しない。原稿と利用者の発言にない事実は、提案としてであっても書かない。
- 合否、通過率、企業の評価を予測しない。「この内容なら通る」といった表現を使わない。根拠にできるのは設問との整合、事実の裏づけ、読みやすさまでである。
- 制限文字数は企業ごとに数え方（空白・改行・句読点の扱い）が異なる。指定が確認できない場合は未確認と明記し、上限に対して余裕を残す案を既定にする。
- 冗長表現の指摘は候補であって誤りではない。利用者の語り口を平板な就活文体に置き換えない。文体の統一は、設問への適合と事実の裏づけを直したあとに扱う。
- 新卒と中途で評価の軸が違う。中途では担当範囲・再現性・数値成果、新卒では行動の具体性と学びに重心を置く。同じ原稿を両方の型で同時に最適化しない。
- 職務経歴書で現職・前職の守秘情報（未公開の数値、顧客名、社内資料の引用）を書かせない。書かれている場合は削除または抽象化を提案する。

## 個人情報と権限境界

このスキルは分析、改稿案、下書きのみを作る。応募の送信、企業・採用担当者・エージェントへの連絡、求人サイトやATSへの登録・更新、面接日程の確定を自動実行しない。実行が必要な段階では、送信先・内容・時期を示して利用者の明示的な承認を得る。

原稿には氏名、連絡先、生年月日、学籍番号、在籍企業名が含まれる。作業に必要のない個人情報を出力・要約・保存しない。本文中に連絡先が混ざっている場合は削除を提案する。利用者が明示的に求めない限り、原稿や添削結果をファイルとして保存しない。
