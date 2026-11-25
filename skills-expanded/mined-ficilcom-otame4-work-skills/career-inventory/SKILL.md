---
name: career-inventory
description: Inventory a person's work history as facts before any document is written, listing each period of employment and what they actually did, splitting every experience into situation, their own actions, outcome, and stated role, and recording what each claim rests on (public record, their own records, someone who was there, or memory alone). Use when a user is starting a job search, needs material for a rirekisho, shokumu-keirekisho, or entry sheet, or wants to find which periods of their history they have never written down; do not use to judge their strengths, aptitude, or market value, to name a job they are suited for, or to write finished application copy.
license: MIT
metadata:
  author: ficilcom
---

# 経験の棚卸し

応募書類を書く前に、これまでの経験を**事実として**洗い出す。各経験を状況・自分の行動・結果・役割に分け、その主張が何に基づくのか（公開情報、手元の資料、当時を知る人、記憶だけ）を記録する。強みの判定、適性の診断、完成文の作成は行わない。

## 進め方

1. **在籍期間を先に並べる。** 会社、部署、期間を確定する。ここが埋まらないうちに個別の経験に入らない。新卒の場合は学業、部活・サークル、アルバイト、インターン、個人の活動を並べる。
2. 期間ごとに担当した仕事を並べる。**成果が出たものだけを選ばない。** 日常の業務、うまくいかなかったこと、引き継いだこと、やめたことも並べる。選別は応募先が決まってから行う。
3. [棚卸しの進め方](references/inventory-method.md) に従って、各経験を状況・行動・結果・役割に分解する。**書けない項目があることが結果である。** 埋めるために推測を書かない。「チームで達成した」を「自分が達成した」に書き換えない。
4. 経験ごとに裏づけを確認する。公開されているか、手元の資料で確認できるか、当時を知る人がいるか、記憶だけか。数値については、経験全体とは別に裏づけを確認する。**覚えている数値と確認した数値を混ぜない。**
5. `python3 scripts/check_inventory_coverage.py <input.json>` で、不足している項目、裏づけの弱い経験、棚卸しできていない在籍期間、種類の偏りを機械的に確認する。入力形式は [棚卸しの進め方](references/inventory-method.md#スクリプト入力) を見る。
6. 現職・前職の非公開情報を含む経験に印を付け、抽象化できるかを先に決める。抽象化できないものは、使わない選択肢も残す。
7. [報告書形式](references/report-format.md) に従って、棚卸しの進み具合、経験の一覧、裏づけの確認が必要なもの、利用者への質問を出す。**埋まっていない項目は、埋まっていないまま次に渡す。**
8. 次に渡す先を示す。職務経歴書を組み立てるなら `resume-draft`、設問への回答を書く・直すなら `entry-sheet-review`、面接の準備なら `interview-prep`、求人の要件との突き合わせなら `job-posting-analysis`。

## 判断上の制約

- **強み、適性、向いている職種、性格を判定しない。** 「あなたはこういう人だ」という要約を書かない。性格類型や診断の枠組みに当てはめない。示せるのは、洗い出した事実と、その裏づけと、まだ埋まっていない項目までである。
- **経験、数値、役職、資格を創作しない。** 利用者が話していないことを、補完として書かない。空欄は空欄のまま残す。
- 推測で埋めた案を「たたき台」として出さない。たたき台があると、利用者はそれを事実として確認せずに使う。質問の形で返す。
- 応募書類に使える完成文をここで作らない。棚卸しの成果物は事実の一覧であり、文章に整えるのは別の工程である。先に文章にすると事実の確認が飛ばされる。
- 経験の優劣、市場価値、想定年収を見立てない。「この経験は弱い」「もっとアピールできる」といった評価をしない。
- 役割が曖昧な経験を、書きやすいように役割を上げて記録しない。`unstated` のまま残し、後で確認する。
- 裏づけが記憶だけの経験を否定しない。書けるが、断定形で数値を書かない、という書き方の違いとして扱う。`memory`（記憶だけ）と `unknown`（未確認）を混ぜない。
- 種類の偏りが出た場合、足りない種類の経験を作り出さない。漏れていないかを確認するだけにする。
- 新卒と中途で読まれるものが違う。中途は担当範囲と成果の大きさ、新卒は行動の具体性と学び。新卒の棚卸しで、数値がないことを不足として扱わない。
- 転職すべきかどうかを示唆しない。棚卸しの結果から「今の会社では活かせない」といった含みを持たせない。

## 個人情報と権限境界

このスキルは経験の整理のみを行う。**応募の送信、求人サイトやATSへの経歴の登録・更新、エージェントへの経歴書の提出、企業への連絡を自動実行しない。** 経歴を外部サービスに登録する段階では、送信先・内容を示して利用者の明示的な承認を得る。

棚卸しの内容は、氏名、生年月日、学歴、在籍企業、評価、給与に及ぶ。**作業に必要のない個人情報を集めない。** 家族構成、健康状態、信条、支持政党、出身地は、応募書類に必要な範囲を超えるため聞かない。現職・前職の守秘情報は、外に出せる形に抽象化できるかだけを扱い、内容を書き出して保存しない。

利用者が明示的に求めない限り、棚卸しの結果をファイルに残さない。残す場合も、保存先と内容を示して承認を得る。
