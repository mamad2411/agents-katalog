---
name: job-search-plan
description: "Lay out how a job search will actually run alongside a current job: the hours available each week and what they go to, how weekday daytime slots for interviews will be found, which routes to use (direct applications, job boards, scout sites, agents, referrals, public employment services) and what each one discloses to whom, how to keep the search from reaching the current employer through public profiles or workplace equipment, a single tracker of every application's stage, next action, and deadline, and a date and conditions for reviewing, reducing, or pausing the search. Use when someone has decided to start looking, or to gather information while employed, and asks how to fit it in, which routes to use, whether the applications they are running fit the time they have, or how to keep track of them; do not use to decide whether to change jobs, to pick or rate employers or job postings, to predict outcomes, or to send applications, publish profiles, or contact agents on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# 転職活動の段取り

在職しながら転職活動や情報収集を進めると決めた人のために、**時間・経路・現職への配慮・応募の記録・見直しの区切り**を一つの段取りにする。応募先の推薦、求人の評価、合否や通過率の予測、転職するかどうかの判断は行わない。

## 進め方

- **決めていることから始める。** 転職すると決めていなくても、在職しながら情報を集める段取りとして使える。転職するか自体に迷いが戻ったら `job-change-decision` の範囲であり、ここで結論を急がせない。経歴書、志望先の一覧、転職の理由が揃うまで待たず、週に使える時間と、すでに動いていることから聞く。
- **週に使える時間と、平日日中の枠を分けて決める。** 活動ごとの時間を本人の見積もりで置き、合計が使える時間に収まるかを見る。面接など平日日中の枠が要る活動は、有給・半休・時間休などの扱いを本人の職場の就業規則で確認する。枠の作り方は [活動の進め方](references/running-the-search.md#時間の作り方) を読む。虚偽の欠勤理由や、現職の設備・勤務時間の流用を段取りに含めない。
- **経路ごとに、誰に何が開示されるかを確かめる。** 直接応募、求人サイト、スカウトサイト、エージェント、知人の紹介、公的な職業紹介から本人が使うものを選ぶ。公開プロフィールが現職から見えない設定、第三者が間に入る経路の取り決め（同一企業への他経路の応募、辞退の連絡先）を本人が確認する。特定のサービスを推薦しない。経路の違いは [活動の進め方](references/running-the-search.md#経路の使い分け) を読む。
- **応募を1つの表にまとめる。** 企業、経路、段階、次の行動と予定日、相手が示した期限を揃える。同じ企業に複数の経路で進んでいるもの、次の行動が決まっていないもの、期限を過ぎたものを見つける。本数の正解は決めず、時間と負担の範囲で本人が選ぶ。
- **材料が揃ってきたら `python3 scripts/plan_job_search.py <input.json>` で機械的に点検する。** 未確認の欄は省略したまま渡してよく、仮の値を入れた場合はその旨を本人に示す。 時間の合計、平日日中の枠、公開設定と取り決めの確認状況、応募ごとの期限を出す。入力の仕様と、標準入力で保存せず実行する方法は [活動の進め方](references/running-the-search.md#スクリプト入力) を見る。必須の質問票ではなく、対話で同じ整理を行える。
- **見直す日と、減らす・止める条件を決める。** 活動を続けるか、減らすか、止めるかを選び直す区切りを本人と決める。睡眠や体調、現職の業務への影響など、本人が挙げた負担の兆候を止める条件にする。期限は本人と決め、決まっていなければ「提案」と表示する。
- **終わりには [段取りのまとめ方](references/report-format.md) に沿って会話内で返す。** 時間、経路、応募の表、見直しの区切りのうち、その時点で決まったものだけを示し、未確認は未確認のまま残す。

## 判断上の制約

- 応募先、求人、経路の良し悪しを評価しない。求人票の読み解きは `job-posting-analysis`、企業の調査は `company-research`、スカウトの仕分けは `scout-message-triage` の範囲。合否、通過率、活動期間の見込みを示さない。
- 「在職中に活動すべき」「先に辞めるべき」「今すぐ始めるべき」を決めない。並行応募の本数、エージェントの利用、スカウトへの登録を既定にしない。
- 有給の取得理由を偽る、勤務時間中に現職の設備で活動する、現職や顧客の非公開情報を応募資料に使う、といった段取りを作らない。現職の就業規則で確認すべき定め（有給、競業、兼業）は書面で確認し、記憶で断定しない。
- エージェント・紹介の取り決め、求人サイトの公開設定、公的な職業紹介の利用条件は、各サービスの規約や公式情報で確認する。確認できないものは未確認とし、規約の解釈や労働法・税務の判断を専門家の確定判断として示さない。
- 内定の条件確認は `offer-terms-check`、辞退は `offer-decline`、退職の段取りは `resignation-plan` の範囲であり、この表で代行しない。

## 個人情報と権限境界

このスキルは段取りの整理と点検のみを行う。応募の送信、求人サイトやスカウトサイトへの登録・プロフィールの公開設定・更新、エージェントや紹介者への連絡、面接日程の確定、辞退の連絡、有給の申請を自動実行しない。実行が必要な段階では、**対象・内容・時期・影響**を示して利用者の明示的な承認を得る。表に「次の行動」として書くことは、実行の承認を意味しない。

応募の表には企業名や選考状況が並ぶ。氏名、連絡先、現職や顧客の非公開情報、他の応募者の情報を不要に集めない。公開プロフィールの内容は本人が決める。利用者が明示的に求めない限り、表や整理結果をファイルに残さない。残す場合も、保存先と内容を示して承認を得る。
