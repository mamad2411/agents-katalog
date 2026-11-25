---
name: onboarding-plan
description: Plan the first months at a new Japanese employer after an offer is accepted, listing every expectation and promise made in interviews, the offer, or negotiation with its source, separating what is in writing from what was only said and what has no agreed measure, working out when the probation period ends and whether its criteria and conditions are known, and scheduling who to confirm what with before and after the start date. Use when a user has accepted an offer and wants to prepare for joining, make sure verbal promises such as remote days or a future role are confirmed, or understand what the probation period means for them; do not use to predict whether they will fit in or pass probation, to judge their manager or colleagues, to rule on the legality of probation terms, or to contact the new employer.
license: MIT
metadata:
  author: ficilcom
---

# 入社後の最初の数か月の段取り

入社が決まってから最初の数か月について、面接・内定・条件の交渉で示された期待と約束を出典つきで並べ、書面にないものと測り方が決まっていないものを分ける。試用期間の終わりと条件を確かめ、入社前と入社後のそれぞれで、誰と何を確かめるかの日程を作る。職場に馴染めるかや試用期間の評価の予測、上司・同僚・会社の評価、会社への連絡の代行は行わない。

## 進め方

1. **入社日と、労働条件が書面で確定しているかを最初に確かめる。** 書面がまだなら、入社前の段取りより先に書面を求める。書面の項目確認は `offer-terms-check` の範囲であり、結果があれば引き継ぐ。退職の手続きが残っている場合は `resignation-plan` と日程を揃える。
2. 期待と約束を1件ずつ並べる。担当範囲、最初に任される仕事、評価の基準、将来の役割、勤務形態（在宅日数、勤務時間）、配属、研修。それぞれに**誰が・いつ・どこで言ったか**と、書面にあるかを付ける。交渉で合意した内容はここに入れる。
3. [入社後の段取りの進め方](references/onboarding-method.md) に従って、各項目を「書面にある」「口頭だけ」「測り方が決まっていない」に分ける。出典によって内容が食い違う項目は、どちらが正しいかを推測せず、確かめる項目にする。
4. 試用期間を確かめる。期間、期間中の給与・雇用形態・勤務形態が本採用後と違うか、本採用の判断基準が示されているか。分からない項目は `unknown` のまま残す。
5. `python3 scripts/plan_onboarding.py <input.json>` で、試用期間の終わりの日付、入社までの日数、口頭だけの約束、測り方の決まっていない期待、出典間の食い違い、確かめる場が決まっていない項目、期限を過ぎた入社前の手続きを機械的に出す。入力形式は [入社後の段取りの進め方](references/onboarding-method.md#スクリプト入力) を見る。
6. 確かめる場の案を作る。入社前は採用担当者、入社後は直属の上長が主な相手になる。各場で何を聞くかを、項目ごとの質問の形にする。日付と相手は利用者が決める。**確かめる場が試用期間の終わり近くにしかない状態を避ける。**
7. [報告書形式](references/report-format.md) に従って、日程、期待と約束の一覧、試用期間、入社前にすること、確かめる場と質問、記録として残すことを出す。

## 判断上の制約

- **試用期間を通るか、職場に馴染めるかを予測しない。** 示すのは、期待の中身、測り方、確かめる相手と時期までである。
- **試用期間の定めや本採用の判断の適法性を判定しない。** 条件に気になる点があれば確認事項として示し、労働基準監督署や専門家への相談を選択肢として残す。
- 口頭の約束を確定した条件として扱わない。同時に、入社後に書面化を迫る対立的な文面にしない。上長との最初の面談で、期待を共有する形で確かめる。
- 上司、同僚、会社、社風を評価しない。面接での印象から職場の様子を推測しない。
- 成果目標をこちらで決めない。目標は上長と合意するものであり、ここでは合意すべき項目と聞き方を並べる。「最初の90日で成果を出す計画」のような、成果を約束する計画を作らない。
- **前職の資料、顧客情報、技術情報を新しい職場に持ち込む準備を手伝わない。** 前職の経験は、本人の知識として使う範囲にとどめる。
- 入社前の研修や課題を求められた場合、賃金の扱いと参加の要否を確かめる項目にする。労働時間に当たるかは判断しない。
- 入社手続きに必要な書類は名前を示すにとどめる。期限と要否は会社の案内で確かめる。

## 個人情報と権限境界

このスキルは期待の整理と確認の段取りのみを行う。**新しい勤務先の採用担当者・上長・人事への連絡、面談の日程の確定、入社手続き書類の提出、エージェントへの連絡を自動実行しない。** 質問や依頼の文面を下書きした場合も、送信先・内容・時期を示して利用者の明示的な承認を得る。

入社手続きには、マイナンバー、基礎年金番号、口座情報、扶養家族の情報が関わる。**これらを聞き出さず、出力にも書かない。** 面接で聞いた上長や同僚の名前は、確かめる相手を示す範囲でだけ扱う。利用者が明示的に求めない限り、段取りや記録をファイルに残さない。
