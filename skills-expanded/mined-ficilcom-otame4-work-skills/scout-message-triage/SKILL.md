---
name: scout-message-triage
description: "Sort incoming scout messages and agent-forwarded openings by what they actually disclose: whether the employer is named at all, which of pay, location, employment type, and duties are stated, whether the message refers to the applicant's own history or reads as a mass send, whether a stated salary is an offer or a \"up to\" figure, and whether the same employer has arrived through more than one route. Use when a user has a backlog of scout messages and wants to know which ones can be researched, what to ask before replying, and what to settle before handing over a resume; do not use to rate how promising an opening is, to judge an employer or an agent, or to reply on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# スカウト・エージェント求人の仕分け

受け取ったスカウトを、**文面の熱意ではなく開示されている事実**で仕分ける。企業名が分かるもの、条件が揃っているものを選り分け、経歴を渡す前に決めることを整理する。求人や企業の評価、応募の可否の判断は行わない。

## 進め方

1. スカウトの**原文**を確認する。要約や転載ではなく、届いた文面を見る。件名と本文で条件が違うことがある。
2. 各スカウトについて、企業名が明示されているか、給与・勤務地・雇用形態・業務内容が書かれているか、経歴に触れた記述があるかを記録する。**「大手メーカー」「急成長中のSaaS企業」を企業名として扱わない。**
3. 年収の書き方を区別する。「500万〜700万」はレンジの提示、「最大900万」は上限のみ、「600万も可能」は提示ではない。**上限や可能性の表現を、提示された条件として扱わない。**
4. `python3 scripts/triage_scouts.py <input.json>` で、企業名の有無、欠けている条件、個別化の有無、返信期限、**同一企業を複数経路から受けていないか**を機械的に確認する。入力形式は [仕分けの基準](references/triage-criteria.md#スクリプト入力) を見る。
5. 企業名が分かったものだけを `company-research` と `job-posting-analysis` に渡す。企業名が伏せられているものは、企業名を確認する質問に変える。**確認するまで経歴書を渡さない。**
6. 登録や面談が必要なものについて、**渡す情報の範囲を先に決める。** 職務経歴書の全文か要約か、現職の社名を出すか、他社の選考状況を伝えるか。いずれも利用者が決める。
7. 同じ企業を複数経路から受けている場合は、その事実と、応募の重複を避けるためにどの経路で進めるかを先に決める必要があることを示す。
8. [報告書形式](references/report-format.md) に従って、仕分けの結果、確認すること、経歴を渡す前の判断、返信の扱いを出す。

## 判断上の制約

- **スカウトの熱意、丁寧さ、本気度を評価しない。** 文面が個別化されているかは、文面を根拠にしないための情報であって、優劣ではない。一斉送信でも条件が具体的なものはあり、個別化されていても条件が空のものもある。
- **個別化されていないことだけを理由に落とさない。** 落とすかどうかは利用者が決める。
- 求人や企業の良し悪しを判定しない。企業の評価は `company-research` の範囲であり、スカウトの文面からは読み取れない。
- エージェントや媒体の優劣を判定しない。担当者の対応の良し悪しも評価しない。
- **応募すべきかどうかを結論として書かない。** `routing` は次に何をする段階かであって、推奨ではない。
- 返信期限が短いことを、良い求人の根拠にも悪い求人の根拠にもしない。**急がされていることを理由に返信を勧めない。**
- 返信すれば選考が有利になる、といった見込みを書かない。
- 同じ企業を複数経路から受けている場合、どの経路が有利かを推奨しない。重複しているという事実と、先に決める必要があることを示すまでにする。
- 職種名から業務内容を補完しない。書かれていない条件を推測で埋めない。

## 個人情報と権限境界

このスキルは仕分けと確認事項の整理のみを行う。**スカウトへの返信、エージェントへの登録、面談の申し込み、求人サイトやATSでの経歴の公開・更新、応募の送信を自動実行しない。** 返信や辞退の文面を下書きした場合も、送信先・内容・時期を示して利用者の明示的な承認を得る。

**経歴を渡す判断は、このスキルが最も注意すべき点である。** エージェントへの登録、面談、プラットフォームでの経歴公開は、いずれも個人情報を第三者に渡す行為にあたる。渡す範囲、現職の社名を出すか、他社の選考状況を伝えるかを、利用者が決める前に先へ進めない。**「伝えた方がスムーズ」といった助言をしない。**

スカウトの文面には、送り主の氏名、連絡先、担当者情報が含まれる。仕分けに必要のない個人情報を出力・保存しない。利用者が明示的に求めない限り、スカウトの内容や仕分け結果をファイルに残さない。
