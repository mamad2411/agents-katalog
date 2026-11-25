---
name: job-posting-analysis
description: "Read a Japanese job posting closely and report what it actually states: base pay separated from fixed overtime allowance, the range converted to an hourly basis, required versus preferred requirements, and the terms left ambiguous. Use when a user wants a 求人票 or job description examined before applying, wants two postings compared on the same basis, or wants questions prepared about pay and working conditions; do not use to judge whether the user will be hired, to infer duties the posting does not state, or to evaluate the employer's reputation."
license: MIT
metadata:
  author: ficilcom
---

# 求人票の読み解き

求人票に**書いてあること**と**書いていないこと**を分け、提示年収の中身（固定残業代を含むか、賞与を含むか）を分解し、要件と条件の曖昧な箇所を確認すべき質問に変える。採用可能性の予測、職種名からの業務内容の推測、企業評価は行わない。

## 進め方

1. 求人票の**原文**を確認する。要約や転載ではなく、応募する媒体に載っている記載を見る。利用者が本文を貼れない場合はURLを取得する。取得手段がない場合は、記載を推測せず、確認できない項目を `unknown` のまま進める。
2. 同じ企業の求人が媒体によって条件が違うことがある。複数の媒体に出ている場合は差分を取る。差分は面接で確認すべき論点になる。
3. [記載の読み方](references/reading-the-posting.md) に従って、雇用形態、就業場所、労働時間制度、給与、要件、業務内容を記載どおりに書き出す。**職種名から業務内容を補完しない。** 「エンジニア」「企画」「コンサルタント」は企業ごとに指す範囲が違う。
4. 給与と労働時間を JSON にして `python3 scripts/analyze_job_posting.py <input.json>` にかける。固定残業代を分離した基本給、みなし残業を含めた想定労働時間での時給換算、レンジの開き、記載の欠落が出る。入力形式は [記載の読み方](references/reading-the-posting.md#スクリプト入力) を見る。
5. 要件を必須と歓迎に分け、利用者の経歴と突き合わせる。**充足しない必須要件があっても応募の可否を判定しない。** 日本の求人票では必須要件が実際には目安のことも多い。示すのは充足状況と、職務経歴書で何を示せば埋まるかまでである。
6. [報告書形式](references/report-format.md) に従って、記載の要約、給与の分解、要件の充足状況、曖昧な条件、確認すべき質問を出す。

## 判断上の制約

- **提示年収をそのまま額面の実力と扱わない。** 固定残業代を含む提示か、賞与を含む提示か、上限が何年目で誰に適用されるかで、実際の基本給は大きく変わる。分解できない場合は「分解不能」と書く。
- 年収レンジの上限を期待値として扱わない。下限が適用される条件が書かれていないことは、それ自体が確認事項である。
- 業務内容、残業実態、評価制度、昇給幅を、書かれていない範囲まで推測しない。「たぶんこうだろう」を報告書に入れない。
- 「みなし残業」「裁量労働制」「年俸制」「固定残業手当」は別の制度であり、併記されている場合は適用関係を確認する。制度の当否を法的に断定しない。
- 労働条件の適法性を判定しない。気になる記載は、労働条件通知書での確認事項として示すか、労働基準監督署・専門家への相談を選択肢として残す。
- 企業の評判、離職率、社風を求人票から推測しない。それは `company-research` スキルの範囲であり、求人票の文面からは読み取れない。
- 複数の求人を比較する場合は、同じ基準（固定残業代を除いた基本給、想定労働時間込みの時給）に揃える。提示年収のまま並べない。

## 個人情報と権限境界

このスキルは求人票の分解と質問の準備のみを行う。応募の送信、企業や採用担当者への問い合わせ、エージェントへの連絡、面接日程の確定を自動実行しない。実行が必要な段階では、送信先・内容・時期を示して利用者の明示的な承認を得る。

利用者の経歴を要件の突き合わせに使う場合も、必要な範囲を超えて収集・保存・出力しない。利用者が明示的に求めない限り、求人票や突き合わせ結果をファイルに残さない。
