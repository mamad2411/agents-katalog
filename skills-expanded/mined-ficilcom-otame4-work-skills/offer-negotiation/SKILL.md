---
name: offer-negotiation
description: Prepare a request to change the terms of a Japanese job offer before accepting it, sorting what the user wants changed (pay components, start date, work style, location, title, probation) by priority, tying each ask to a basis the user can show (the written offer, the job posting, what was said in interviews, their own records), working the timing back from the acceptance deadline, and drafting the message to the employer or recruiting agent. Use when a user has an offer and wants to ask for higher pay, a later start date, more remote days, or other changed terms, or wants to know how to raise it without losing the offer; do not use to predict whether the request will succeed, to set a target figure from market rates, to fabricate a competing offer, to decide whether to accept, or to send anything to the employer.
license: MIT
metadata:
  author: ficilcom
---

# 内定条件の交渉準備

内定条件について会社に何を依頼するかを項目ごとに整理し、各依頼の根拠を利用者が示せるもの（書面の条件、求人票、面接での説明、本人の記録）に限って対応させ、承諾期限から逆算した段取りと依頼文の下書きを作る。交渉が通るかの予測、相場からの要求額の算出、承諾・辞退の判断、企業やエージェントへの連絡の代行は行わない。

## 進め方

1. **書面で条件を受け取っているかを最初に確認する。** まだなら、交渉の前に書面の提示を求める文面を優先する。書面にない条件を起点に依頼を組み立てると、何が変わったのかを後で確かめられない。書面の項目確認そのものは `offer-terms-check`、複数の内定の比較は `offer-comparison` で行い、その結果があれば引き継ぐ。
2. 依頼したい項目を1つずつ切り出す。年収は総額ではなく、基本給・固定手当・固定残業代・賞与のどれを動かしたいのかまで分ける。各項目に、現在の提示（原文）、希望、優先度（必須・希望・あれば嬉しい）、**断られた場合にどうするか**を置く。最後の1つは利用者が決める。こちらで埋めない。
3. [交渉準備の進め方](references/negotiation-method.md) に従って、各依頼の根拠を種類で分ける。根拠のない依頼は、根拠を探すか、根拠なしの希望として伝えるかを利用者に選んでもらう。**現年収、実績、他社の状況を事実と違う形で書かない。**
4. `python3 scripts/plan_negotiation.py <input.json>` で、提示と希望の差額と年額換算、求人票の提示範囲との位置、根拠のない依頼、優先の付け方、承諾期限までに回答が返るかを機械的に出す。入力形式は [交渉準備の進め方](references/negotiation-method.md#スクリプト入力) を見る。
5. 経路を確定する。企業に直接か、エージェント経由か。経路によって宛先と書き方が変わる。エージェント経由の場合、エージェントに伝える内容と、企業に伝えてほしい内容を分ける。
6. 依頼文を下書きする。入社の意向は事実のとおりに書き、**「この条件なら必ず承諾する」と書くかどうかは利用者が決める。** 書けば取り消しにくい約束になる。他社の社名と提示額は、利用者が伝えると決めた範囲だけにする。
7. [報告書形式](references/report-format.md) に従って、前提、依頼項目の表、根拠、日程、依頼文、回答を受けた後の扱いを出す。回答で条件が変わった場合は、**改めて書面で受け取るまで確定していない**ことを明記する。

## 判断上の制約

- **交渉が通るか、どこまで上がるかを予測しない。** 「この額なら通る」「言えば上がる」と書かない。示すのは、依頼の内容、根拠、差額、日程までである。
- **相場を根拠にした要求額を作らない。** 給与水準の統計や求人の相場は時点と職種の区切り方で変わる。利用者が公開資料を示した場合だけ、出典と時点を付けて根拠に使う。記憶の数字で相場を語らない。
- **根拠を作らない。** 他社の内定、現年収、実績、役職を、事実と違う形や大きく見せる形で書かない。存在しない他社の提示を交渉材料にする案を出さない。
- 交渉すると内定が取り消されるか、関係が悪くなるかを予測しない。懸念として挙がった場合は、依頼の出し方（根拠と優先を明示する、期限を守る）で扱える範囲を示すにとどめる。
- 承諾するか辞退するかを結論として書かない。依頼が断られた場合の行動は、利用者が決めた内容のまま書く。決まっていない場合は、決まっていないことを示す。
- 労働条件の適法性、固定残業代の有効性を判定しない。気になる点は `offer-terms-check` の確認事項に戻す。
- 賞与や手当は基本給に連動して決まることがある。基本給の差額を年額にするときは、月額×12の単純計算であることを明記し、連動分を見込みで足さない。
- 口頭や電話で条件が変わった場合も、改訂された書面を受け取るまで確定として扱わない。

## 個人情報と権限境界

このスキルは依頼内容の整理と文面の下書きのみを行う。**企業・採用担当者・エージェントへの依頼の送信、承諾・辞退の返信、他社への連絡、入社日の確定を自動実行しない。** 文面を下書きした場合も、送信先・内容・時期を示して利用者の明示的な承認を得る。条件付きの承諾を含む文面は、送った後に取り消しにくいことを添えて確認する。

現年収、給与明細、他社の選考状況と提示額は、相手に伝われば戻せない情報である。依頼に必要な範囲を超えて集めず、ある企業への文面に他社の社名や提示額を、利用者が伝えると決めた範囲を超えて書き込まない。利用者が明示的に求めない限り、依頼内容や文面をファイルに残さない。
