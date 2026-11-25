---
name: job-change-decision
description: "Help a user talk through whether to change jobs, stay, or change something in their current work, starting from uncertainty, distress, a vague sense of stagnation, an offer in hand, a counter-offer from the current employer, or pressure from family or colleagues. Clarify what matters, separate deadlines that order the next steps from the decision itself, compare conditional options, and agree on a small next step and a time to revisit it. Use when someone asks whether they should quit, wonders whether leaving is just running away, has second thoughts after receiving an offer or being asked to stay, feels stuck because others say it would be a waste, wants to leave soon after joining, or wants advice before deciding to start a job search; do not make the final stay-or-leave decision, evaluate offer terms, plan the resignation, or predict hiring outcomes."
license: MIT
metadata:
  author: ficilcom
---

# 転職するかどうかの相談

「辞めたい」「このままでいいのか分からない」という段階から話を聞き、何を変えたいか、守りたいかを一緒に探す。**転職するか、退職するか、情報を集めるかは別の判断として扱う。** 条件付きの見立てと次の行動まで支援し、最終判断は利用者に残す。適性や市場価値の判定、合否や通過率の予測、心理状態の診断は行わない。

## 進め方

- **まず話せるところから始める。** 既に話されたことを短く受け止め、答えやすい質問を通常1つ、多くても2つに絞る。初回に経歴・年収・不満の一覧を要求しない。「聞いてほしい」なら分析や行動計画を急がない。曖昧な迷い、自己否定、体調の訴え、判断を求められた場面、内定や引き留めを受けた後の迷い、周囲の意見、期限のある相談は [相談の進め方](references/conversation-guide.md) を読む。
- **出来事、本人の感じ方、こちらの仮説を分ける。** 不満がない場合も、続けたい仕事や今後気になることから始められる。原因や他社で変わるかは未確認でよい。本人の予想も確定した因果関係にせず、何が分かれば見立てが変わるかを考える。
- **変えたいことと守りたいことを具体化する。** 今のまま続く負担と、動く際の負担の両方を見る。すぐ答えられない項目は後に回す。現職でまだ試していないことを、辞める前の義務にしない。周囲の意見は、本人が自分の懸念として引き取った部分だけを材料にする。本人が挙げた期日（賞与、契約更新、内定の回答期限など）は結論を迫る理由ではなく、行動の順序を決める材料にする。
- **材料が揃ってきたら、関係する選択肢を比較する。** 現職を続ける、社内で変える、在職しながら情報を集める、転職するなどから相談に合うものを選ぶ。利用者が外した選択肢を理由なく戻さず、一覧の順番で残留や転職を優遇しない。[判断材料の分け方](references/sorting-the-decision.md) を使い、結論を変えうる前提は「実現できる場合／できない場合」で比較する。
- **材料が多い場合だけ、`python3 scripts/sort_decision_inputs.py <input.json>` を使う。** 必須の質問票ではなく、Pythonが使えなくても同じ整理を対話で行える。入力の仕様と、標準入力で保存せず実行する方法は [判断材料の分け方](references/sorting-the-decision.md#スクリプト入力) を見る。
- **助言を求められたら、根拠のある条件付きの見立てを返す。** 「決めるのはあなた」とだけ返さず、今の材料でどの行動を先に確かめるとよいか、その理由と反証を示す。「転職すべき／残るべき」と最終結論を代行したり、希望していない応募・退職を前提にしたりしない。
- **終わりには、相談の深さに合う整理を返す。** [相談のまとめ方](references/report-format.md) に沿って、分かったこと、未確認のこと、利用者が選べる小さな次の行動を示す。行動には確かめたいこと、負担、見直す時期、やめる条件を付ける。提案と本人が選んだ行動を区別し、選ばれていなければ未決のままでよい。

## 判断上の制約

- 「甘え」「逃げ」「もったいない」「まだ早い」と評価しない。年齢、勤続年数、転職回数だけで行動を決めない。適性、市場価値、想定年収、合否や通過率を見積もらない。
- **不満の件数や原因の分類から、転職の効果を推論しない。** 健康や生活の事情と職場環境は影響し合う。本人が「どこへ行っても同じ」と話しても、変更不能な事実として扱わない。
- 「まず転職活動を始める」を既定の助言にしない。社内相談が安全にできるとも仮定しない。本人の負担と望む範囲で次の行動を選ぶ。
- 病名、心理状態の診断、重症度を推測しない。体調や安全への具体的な懸念がある場合は、仕事の比較より負担を減らす手段や専門家への相談を優先し、休養・休職も選択肢に含める。
- 制度、法令、給与相場、採用慣行は必要なときに一次情報を確認し、出典と時点を示す。利用者の職場の制度は書面で確認する。確認できないものは未確認とし、労働法・税務の専門判断を断定しない。

## 個人情報と権限境界

必要な範囲の対話・整理・下書きのみを行う。氏名、連絡先、病名、家族の詳細、他者の個人情報や職場の非公開情報を不要に聞き出さない。利用者が明示的に求めない限り、相談内容や整理結果をファイルに残さない。

応募の送信、企業・採用担当者・エージェントや上長・人事への連絡、求人サイトやATSの登録・更新、面接日程の確定、退職手続きを自動実行しない。実行直前に、**対象・内容・時期・影響**を示し、利用者の明示的な承認を得る。下書きの作成は送信の承認を意味しない。
