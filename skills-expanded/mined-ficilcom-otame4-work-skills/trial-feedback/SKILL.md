---
name: trial-feedback
description: "Debrief a finished Otameshi Tenshoku trial from the employer's side: set the observed facts against the completion criteria agreed before the start, keep expectations added afterwards, second-hand or off-the-job observations and the company's own late or missing support apart, settle the hours actually worked separately from any evaluation, and draft feedback to the candidate that states facts, support gaps and what happens next without promising a hire or continuation the company has not decided. Use when a hiring manager, recruiter or small-business owner wants to review a trial, decide what to tell the candidate, or work out the settlement after a shortfall; do not use to judge the candidate's aptitude or predict a hire, to cut pay or demand unpaid rework because of dissatisfaction, to compare candidates, or to send the feedback, pay, or update records on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：企業の振り返りとフィードバック

終わったおためし業務を、開始前に合意した完了基準と観察事実の突き合わせ、後から足した期待、企業の支援の遅れや未提供、実施済みの実働に対する精算に分けて整理し、候補者に送るフィードバック案と受け入れ担当者用のメモを作る。専任の採用担当者、現場のマネージャー、小規模企業の経営者のいずれからでも、実施メモと成果物の確認結果から着手する。候補者の適性や採用の成否の判定、満足度を理由にした減額や無償のやり直し、候補者どうしの比較、送信・支払い・記録更新の代行は行わない。

## 進め方

1. 開始前に合意した業務範囲と完了基準を手元に置く。`trial-work-design` の計画と `trial-contract-terms` の条件があればそれを使い、なければ利用者の発言から「事前に合意していたこと」と「後から思ったこと」を分けて聞く。
2. [振り返りの整理の仕方](references/debrief-method.md) に従って、観察事実、事前の期待、支援と制約、精算と次の対応の4つに分ける。観察には誰が何で確認したかを付け、伝聞と印象は根拠にしない。職務と無関係な事柄は外す。
3. `python3 scripts/review_trial.py <input.json>` で、事前の基準ごとの結果と観察数、後から足した期待、支援の遅れが関わる未達、実施済みの実働に対する精算額、フィードバック案に混ぜてはいけないものを機械的に出す。入力形式は [振り返りの整理の仕方](references/debrief-method.md#スクリプト入力) を見る。実施メモをファイルに残さないため、入力は標準入力から渡すのを既定にする。**精算は評価と分けて数える。**
4. 成果不足がある場合は、実施済み・未完了・追加希望に分け、企業の支援の遅れや説明不足が関わっていないかを先に確かめる。減額は書面の検収基準に沿う場合にしか成り立たない。無償の見学・学習は成果で評価せず、学んだこと・質問・理解を振り返る。
5. [報告書形式](references/report-format.md) に従って、事前の基準と結果、基準外の観察事実、支援と制約、精算、担当者用のメモ、候補者に送るフィードバック案、送る前に確認することを出す。メモとフィードバック案は必ず分ける。次の対応が決まっていなければ、いつまでに返すかを書く。

## 判断上の制約

- 短い体験や一度の失敗から性格・適性・将来の活躍を断定しない。職務と無関係な属性で評価も順位付けもしない。
- 後から足した期待を評価の根拠にしない。次回の計画の改善点として分ける。未確認を未達にしない。
- 企業の支援の遅れや未提供が関わる未達を、候補者だけの責任にしない。
- 実施済みの実働は、成果への満足や採用判断にかかわらず精算する。減額は書面の検収基準に沿う場合だけで、無償のやり直し、賃金ゼロ、無期限の延長を提案しない。
- 企業が決めていない継続や採用を通知にしない。決まるまでは事実のフィードバックと次の確認にとどめる。
- 候補者どうしを比較しない。複数の候補者がいる場合は1人ずつ同じ形で整理し、仮名で扱う。
- レビューの公開は、公開範囲と変更可否を公式情報で確認し、候補者を必要以上に特定しない下書きにとどめる。
- このスキルだけで使える。計画、契約条件、応募者対応の各スキルがなくても、今回の振り返りは完結する。

## 個人情報と権限境界

このスキルは振り返りの整理とフィードバック案の作成のみを行う。候補者へのフィードバックの送信、報酬の支払い、採用・継続・見送りの通知、応募者管理の更新、レビューの公開は、操作を依頼されても利用者本人が行う。送信前に、宛先、下書き、送る時期、精算の条件を示して引き渡す。ログイン情報を求めない。

候補者の氏名、連絡先、職歴、選考状況、企業や顧客の秘密は必要最小限だけ扱う。他候補者の情報と内部の評価メモをフィードバック案に混ぜない。利用者が明示的に求めない限り、実施メモ・下書き・結果をファイル保存しない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
