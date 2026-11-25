---
name: trial-budget-brief
description: "Prepare the internal case for hosting an Otameshi Tenshoku trial: total what it costs the company with candidate pay, staff hours and platform or incidental fees kept apart, compare it with the budget, state what remains if no hire follows, and lay out the risks, stop conditions, decision owners and deadlines. Use when a hiring manager needs approval or budget from a decision maker, a recruiter has to explain the plan to the team that will host, or a small-business owner wants to see the full cost including their own time before posting; do not use to design the work (trial-work-design), to write the listing (trial-listing-draft), to predict whether a hire will follow, to state platform fees, agency fees or market rates from memory, or to submit the request or post the listing on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：社内説明と予算の説明資料

おためし転職の受け入れを社内で通すための資料を作る。候補者への支払い、企業担当者の工数、掲載料などの周辺費用を分けて合計し、現金で出る額と社内工数を金額化した額を予算と突き合わせ、採用に至らなかった場合に残るもの、リスクと止める条件、判断者と期限を揃える。決裁者向け、受け入れる現場向け、経営者自身向けのどれにも、計画のメモと予算の発言から着手する。採用の成否の予測、掲載料・紹介手数料・相場の記憶による断定、申請や掲載の代行は行わない。

## 進め方

1. 誰に説明するか（決裁者、受け入れる現場、経営者自身）と、何を決めてもらうか（予算、掲載、受け入れ開始、担当者の時間確保）を利用者の発言から読む。読み手ごとに先に答える問いは [社内説明の組み立て方](references/brief-method.md) を見る。**小規模企業で決裁者と受け入れ担当が同じ人なら、資料は短くする。ただし経営者自身の時間も社内工数として数え、省かない。**
2. `trial-work-design` の計画があれば、目的、範囲、実働、単価、期間、変更条件をそこから写す。なければ利用者の発言から埋め、計画がない項目は空欄のまま確認事項にする。
3. 受け入れ担当者の工数を役割ごとに見積もる。説明、資料準備、合同レビュー、振り返り、質問対応を分ける。金額化は社内に原価の基準があるときだけ行い、なければ時間のまま示す。
4. 掲載料、交通費、備品などの周辺費用を、公式の料金表示・見積書・社内の見込み・未確認に分けて集める。サービスの料金は記憶で置かず、企業向けサイトの現在の表示か、利用者が貼った本文で確認する。確認できないものは未確認のまま残す。
5. `python3 scripts/summarize_trial_cost.py <input.json>` で、候補者への支払いの幅、社内工数、周辺費用、現金の額と社内工数込みの額、予算との差、比較可能な他手段を機械的に出す。入力形式は [社内説明の組み立て方](references/brief-method.md#スクリプト入力) を見る。社内の数字をファイルに残さないため、入力は標準入力から渡すのを既定にする。既存の予算枠がなく申請額を決める資料なら、予算を入れず現金の額を申請額として示す。**現金と社内工数を混ぜず、未確認の費用があるうちは総額を確定額として書かない。**
6. [報告書形式](references/report-format.md) に従って、一枚目、目的と範囲、費用の内訳、採用に至らなかった場合に残るもの、リスクと止める条件、他手段との比較、判断事項を出す。総額が予算を超えるなら、範囲を減らす案と予算を増やす案を並べ、利用者が選ぶ。

## 判断上の制約

- 採用できる見込みを根拠にしない。採用に至らなかった場合に残るもの（成果物、フィードバック、受け入れ手順、募集文の改善点）を、それ自体の価値として書く。
- 社内工数の原価、掲載料、紹介手数料、媒体の掲載料を記憶で置かない。確認済みの金額だけを並べ、ない選択肢は名前と「確認中」にとどめる。
- 予算に合わせて工数を削らない。説明や会議を無償枠に移して帳尻を合わせない。期間だけ延ばしても総額は減らない。
- 中止しても候補者の実施済みの実働は支払う前提で、止める条件と精算を書く。企業の満足や採用結果を支払いの条件にしない。
- 資料に候補者の氏名、職歴、選考状況を入れない。必要なら仮名と、職務に関係する経験の有無だけにする。
- このスキルだけで使える。計画、募集文、契約条件の各スキルがなくても、今回の社内説明は完結する。

## 個人情報と権限境界

このスキルは社内説明資料の作成のみを行う。稟議・申請の提出、求人の掲載、候補者への連絡、契約の締結は、操作を依頼されても利用者本人が行う。提出前に、宛先、決めてもらうこと、期限、未確定の金額を示して引き渡す。

社内の予算、原価の基準、決裁者の氏名、候補者の情報は、資料に必要な範囲を超えて扱わない。利用者が明示的に求めない限り、入力・資料・結果をファイル保存しない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
