---
name: interview-debrief
description: "Go through an interview that has just finished and sort out what happened: the questions asked and how fully they were answered, which of them were prepared for and which came from the submitted documents, the reverse questions still unanswered, what the employer said about conditions and whether any of it was in writing, and when a result was promised. Use when a user has just come out of an interview and wants to record it while it is fresh or to work out what to fix before the next round; do not use to judge how it went, to estimate whether they will pass, or to read anything into the interviewer's manner."
license: MIT
metadata:
  author: ficilcom
---

# 面接の振り返り

終わった面接について、聞かれた質問、答えられた度合い、逆質問の結果、企業側が述べた条件、次の連絡の予定を整理し、次に処理すべきことに変える。手応えの評価、合否の見込み、面接官の様子からの推測は行わない。

## 進め方

1. **当日中に書き出す。** 質問の言い回しと相手の発言は数日で薄れる。日が経っている場合は、経過日数を記録し、細部の再現度が落ちている前提で扱う。**思い出せないことは「思い出せない」と記録し、それらしく再構成しない。**
2. 聞かれた質問を、覚えている言い回しのまま並べる。要約に置き換えない。各質問について、事実で答えられたか（`full` / `partial` / `none`）、準備していたか、提出書類の記述についての質問かを記録する。
3. 逆質問と、得られた答えを記録する。後日回答と言われたもの、答えが得られなかったものを分ける。
4. 企業側が述べたことを記録する。**誰が言ったか**と、**書面で示されたかどうか**を必ず添える。求人票の記載と食い違う説明は、食い違いとして残す。その場で原因を推測しない。
5. `python3 scripts/review_interview.py <input.json>` で、答えきれなかった質問の原因別の内訳、未解決の逆質問、口頭のみの条件、結果連絡の予定日の超過を機械的に出す。入力形式は [振り返りの進め方](references/debrief-method.md#スクリプト入力) を見る。
6. 答えきれなかった質問を原因で分ける。**提出書類の記述を聞かれて答えきれなかったものが最も重い。** 同じ書類で次の面接を受けるなら、同じ場所で同じことが起きる。書類の見直しは `entry-sheet-review`、素材の不足は `career-inventory` と `interview-prep` に戻す。
7. 労働条件に関わる発言を切り出し、`offer-terms-check` に渡す論点として残す。**口頭で聞いた条件を確定した条件として扱わない。**
8. [報告書形式](references/report-format.md) に従って出す。**既定では結果をファイルに保存しない。**

## 判断上の制約

- **手応え、印象、雰囲気を評価しない。** 面接官の表情、相槌、時間の長短、逆質問の受け方から合否を読み取らない。読み取れないものを記録すると、次の判断が歪む。
- **合否、通過の見込み、次に進める可能性を予測しない。** 「良い反応だった」「厳しそうだ」といった表現を使わない。
- 思い出せない部分を埋めない。記憶が曖昧な質問を、ありそうな質問文に整えない。整えた記録は次の準備をずらす。
- 面接官の人物評を書かない。氏名、容姿、私生活、経歴の詮索を記録に残さない。公開されている役員情報や企業が公式に紹介している範囲を超えない。
- 口頭で受けた説明を、確定した労働条件として記録しない。書面かどうかを必ず区別する。求人票との食い違いは、どちらが適用されるかを確認する論点として残し、原因を推測で埋めない。
- 結果の連絡が予定日を過ぎた場合、**催促が有利になるか不利になるかを予測しない。** 問い合わせるかどうかは利用者が決める。文面の下書きは作れるが、送信はしない。
- 反省点を人格の問題に還元しない。「準備不足だった」で止めず、素材の不足か、話す順序の問題か、書類のずれかに分ける。
- 同じ企業の複数回の面接を振り返る場合も、前回の記録を利用者が渡した範囲でのみ使う。こちらで蓄積して参照しない。

## 個人情報と権限境界

このスキルは記録の整理のみを行う。**採用担当者・面接官・エージェントへの連絡、結果の問い合わせ、日程の確定、選考の辞退を自動実行しない。** 問い合わせや辞退の文面を下書きした場合も、送信先・内容・時期を示して利用者の明示的な承認を得る。

**既定では振り返りをファイルに保存しない。** 出力は会話の中で返す。複数社を並行しているなどの理由で保存が必要な場合は、利用者から明示的に依頼されたときに限り、保存先と内容を示して承認を得る。保存する場合も、面接官の氏名・人物評・私生活に関する記述、およびこの面接の振り返りに不要な他社の選考状況は書き込まない。
