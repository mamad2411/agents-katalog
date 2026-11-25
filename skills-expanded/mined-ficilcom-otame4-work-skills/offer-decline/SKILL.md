---
name: offer-decline
description: "Work out the order and the loose ends before turning down an offer or withdrawing from a selection process: whether the offer being kept is actually settled in writing, whether each decline is mid-selection, post-offer, or after acceptance, who besides the employer has to be told when the application came through an agent, a school recommendation, or a referral, which reply deadlines have passed, and what documents, expenses, or borrowed items are still outstanding. Use when a user holds more than one offer and needs to decline the rest, wants to withdraw from a process they are no longer pursuing, or has been asked to turn down other employers as a condition; do not use to decide whether to decline, to rule on what declining after acceptance means legally, or to send any message."
license: MIT
metadata:
  author: ficilcom
---

# 内定・選考の辞退

受ける先が確定しているかを確認したうえで、辞退の段階（選考途中・内定後・承諾後）と経路ごとに、誰へいつ伝えるかを整理し、残っている書類・精算・返却物を洗い出す。辞退の可否の判断、法的な結論、連絡の代行は行わない。

## 進め方

1. **受ける先が確定しているかを最初に確認する。** 確定とは、口頭で入社を伝えたことではなく、**労働条件が書面で確認できている**ことを指す。確定していない状態で内定の辞退を進めようとしている場合は、それを最上位の論点として先に出す。条件の確認は `offer-terms-check` で行う。
2. 辞退の段階を分ける。**選考途中の辞退、内定の辞退（承諾前）、承諾後の辞退は別物である。** 混ぜて扱わない。選考途中の辞退は、受ける先が決まっていなくても進めてよい。
3. 応募の経路を確認する。エージェント経由なら担当者を通す。学校推薦なら**学校の就職課にも連絡し、先に指示を確認する**。社員紹介なら**紹介者にも自分から伝える**。経路が確定していないものは、誰に伝えるかが決まらない。
4. `python3 scripts/check_decline_plan.py <input.json>` で、順序、段階、経路ごとの連絡先、期限の超過、残務を機械的に確認する。入力形式は [辞退の進め方](references/declining.md#スクリプト入力) を見る。
5. 伝える順番を決める。**期限が過ぎている先と、承諾後の辞退を先にする。** 決めたらできるだけ早く伝える。返事を先延ばしにして期限を過ぎさせない。
6. 文面を下書きする。**辞退の理由を詳しく述べる義務はない。** 他社の社名や提示条件を書かない。事実に反する理由を作らない。**下書きまでで、送信しない。**
7. 残っているもの（預けた書類、交通費の精算、借りている物）を、辞退の連絡と同時に確認する項目として並べる。
8. 他社の辞退を求められた場合は、求められた内容・時期・相手を事実として記録する。**応じるかどうかは利用者が決める。**
9. [報告書形式](references/report-format.md) に従って出す。

## 判断上の制約

- **辞退すべきかどうかを結論として書かない。** どの内定を受けるかの比較は `offer-comparison` の範囲であり、そこでも結論は出さない。
- **承諾後の辞退の法的な扱いを断定しない。** 事案によって扱いが分かれる。示せるのは、先方の受け入れ準備が進んでいる段階であるという実務上の事実と、早く直接伝えるという行動までである。心配がある場合は専門家への相談を選択肢として残す。
- **学校推薦の辞退について「できる」「できない」を断定しない。** 学校ごとに扱いが違う。就職課に先に相談する、というところまでを示す。
- 引き止めに応じるべきか、他社の辞退を求められて応じるべきかの結論を書かない。**応じる義務がないという事実**と、その場で結論を出さなくてよいこと、口頭の条件提示は条件ではないことを示すにとどめる。
- 「角が立たない伝え方」「印象を悪くしない言い方」といった見込みを書かない。辞退が今後の応募や業界内の評判に影響するという推測もしない。
- **嘘の辞退理由を作らない。** 言いたくないことは、理由を述べない形で書く。他社の社名や条件を持ち出す必要はない。
- 辞退の連絡が遅れたことを責める書き方をしない。遅れている事実と、いま何をするかを示す。
- 選考途中の辞退を、内定の辞退と同じ重さで扱わない。過剰な手順を求めない。

## 個人情報と権限境界

このスキルは順序の確認と文面の下書きのみを行う。**辞退の連絡、企業・採用担当者・エージェント・学校・紹介者への連絡、選考の取り下げ、承諾の撤回を自動実行しない。** 文面を下書きした場合も、**送信先・内容・時期を示して利用者の明示的な承認を得る。辞退の意思表示は取り消しが難しいため、代行しない。**

辞退の連絡に、**他社の社名、提示条件、選考状況を書き込まない。** 複数社の情報が同時に手元にある状態で作業するため、ある企業向けの文面に別の企業の情報が混ざらないようにする。

利用者が明示的に求めない限り、辞退の計画や各社の選考状況をファイルに残さない。
