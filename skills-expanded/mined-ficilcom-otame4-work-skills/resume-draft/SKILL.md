---
name: resume-draft
description: Assemble a Japanese shokumu-keirekisho (career history document) from an experience inventory, choosing between reverse-chronological, chronological, and skills-based layouts, mapping the target posting's requirements to the experiences that can support them, and drafting the summary, work history, skills, and self-PR so that each sentence stays within what its evidence supports and confidential details are abstracted. Use when a user wants to write or rebuild a whole shokumu-keirekisho for a specific posting or as a general version, or wants to decide which experiences to include and in what order; do not use to invent experience, numbers, titles, or qualifications, to predict whether it will pass screening, to fill in a rirekisho form, or to submit it anywhere.
license: MIT
metadata:
  author: ficilcom
---

# 職務経歴書の組み立て

棚卸しした経験から、応募先に出す職務経歴書を1通組み立てる。形式を選び、求人の要件と載せる経験を対応させ、職務要約・職務経歴・活かせる経験と知識・資格・自己PRの下書きを、各経験の裏づけに合った書き方で作る。経験や数値の創作、書類選考の通過の予測、応募の代行は行わない。

## 進め方

1. **素材がそろっているかを先に確かめる。** 在籍期間と、期間ごとの経験（状況・行動・結果・役割・裏づけ）が必要である。`career-inventory` の結果があればそれを使う。なければ、在籍期間を先に並べてもらい、経験が薄い期間は `career-inventory` で洗い出してから戻ることを勧める。素材が一部足りないまま下書きに進む場合は、足りない箇所を［要確認］として空けておく。**素材が足りない箇所を文章で埋めない。**
2. 応募先を固定する。求人票の必須要件・歓迎要件を原文で受け取る。応募先が決まっていない場合は汎用版として作り、その旨を明記する。求人票の読み解きそのものは `job-posting-analysis` の範囲である。
3. [組み立ての進め方](references/drafting-method.md) に従って形式を選ぶ。応募先や媒体に指定があればそれを優先する。職歴の長さ、転職回数、応募職種と直近の仕事の近さで選び、選んだ理由を1行で残す。
4. 要件ごとに、それを示せる経験を対応させる。**対応する経験がない必須要件を、言い換えや誇張で埋めない。** 近い経験があるかを利用者に聞く、載せずに面接で説明する、の選択肢を並べ、利用者が決める。
5. `python3 scripts/check_resume_plan.py <input.json>` で、要件ごとの対応、載せる経験の裏づけと役割、確認できていない数値、抽象化していない守秘情報、在籍期間の空白と重なり、選んだ形式での並び順を機械的に確認する。入力形式は [組み立ての進め方](references/drafting-method.md#スクリプト入力) を見る。
6. 下書きを作る。各経験は、裏づけと役割に合わせて書き方を変える（記憶だけの数値は断定しない、チームの成果は自分の担当部分と分ける）。守秘情報は規模感を保って特定できない形にし、できないものは載せない。
7. 職務要約と自己PRは、**本文に載せた事実だけから**組み立てる。本文にない強みや人物像を要約に書かない。
8. [報告書形式](references/report-format.md) に従って、前提、要件との対応表、下書き、利用者に確認すること、提出前の見直しを出す。

## 判断上の制約

- **経験、数値、役職、資格、ツール名を創作しない。** 利用者の素材と発言にないものを、提案としても書かない。足りない箇所は質問として返す。
- **求人の言葉に合わせて事実を広げない。** 要件の語句を入れるために、担当範囲、規模、期間、役割を実際より大きく書かない。言い換えてよいのは、同じ事実を相手に通じる言葉にするところまでである。
- 書類選考の通過、評価、企業の印象を予測しない。根拠にできるのは要件との対応、事実の裏づけ、読みやすさまでである。
- 形式、枚数、見出しの慣行は企業や媒体で違う。応募先の指定を優先し、指定が分からない場合は未確認と書く。一般的な枚数を断定しない。
- 在籍期間の空白や短期離職を、事実と違う形で目立たなくしない。期間をずらす、在籍を省く案を出さない。書き方と面接での説明は `interview-prep` に渡す。
- 現職・前職の守秘情報（未公開の数値、顧客名、契約条件、社内資料の内容）を書かせない。抽象化しても特定できる場合は載せない案を出す。
- 強み、適性、市場価値を判定しない。自己PRは利用者が選んだ事実の並べ方であって、こちらの評価ではない。
- 履歴書の様式への記入は扱わない。職歴の年月が履歴書と食い違わないかだけを確認事項に残す。

## 個人情報と権限境界

このスキルは職務経歴書の下書きのみを作る。**応募の送信、求人サイトやATSへの登録・更新、エージェントへの提出、企業への連絡を自動実行しない。** 提出や登録が必要な段階では、送信先・内容・時期を示して利用者の明示的な承認を得る。

職務経歴書には、氏名、連絡先、生年月日、在籍企業、評価、給与が関わる。**氏名・住所・連絡先の欄は空欄のまま出し、こちらで埋めない。** 作業に必要のない個人情報（家族構成、健康状態、信条）を聞かない。利用者が明示的に求めない限り、下書きや素材をファイルに残さない。
