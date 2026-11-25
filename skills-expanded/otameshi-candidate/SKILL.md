---
name: otameshi-candidate
description: Help job seekers use Otameshi Tenshoku to prepare profiles and applications, clarify trial conditions, plan learning visits or paid trial work, and reflect on the experience. Use when a candidate wants to apply for, prepare for, negotiate the scope of, or review an otameshi work experience; do not use to predict whether they will be hired or to judge their aptitude, to state fees, contract terms, or service conditions from memory, or to submit an application, update a profile, or send a message on their behalf. Employer-side requests belong to the employer skills (trial-work-design, trial-listing-draft, applicant-reply and others).
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：求職者の準備と振り返り

体験で何を確かめ、どの範囲の仕事をいつまでに行い、その結果から何を判断するかを具体化する。求人本文、本人の経験・希望、チャットの抜粋、体験メモから、今必要な原稿や計画を作る。適性や採用見込みの判定、報酬・契約・サービス条件の記憶による断定、応募や送信の代行は行わない。

## 進め方

1. 利用者が求職者であること、応募前・条件調整・実施準備・振り返りのどこにいるか、欲しい成果物を会話から読む。曖昧な場合だけ確かめる。全履歴書や全項目の回答を求めず、結論を変える不足情報を少数尋ね、作れる部分と未確認事項を先に返す。
2. 今回行う作業ごとに、経験したこと、未経験の部分、必要な説明や支援を確認する。肩書きや年数だけで経験者／未経験者を決めない。未経験の分野は見学・学習・模擬課題の無償体験を候補にする。経験を活かす仕事は有償枠を提案し、**未経験でも企業の実務を担う場合は有償枠を提案する。** 本人が有償実務を希望しているときに無償参加を前提条件にしない。
3. 作業に必要な参照だけを読む。

| 依頼 | 参照と成果物 |
| --- | --- |
| 無償体験を考えたい・準備したい | [学習体験](references/learning-trial.md)：学習目的、活動、時間、企業の支援、質問 |
| 有償の求人に応募したい・条件を調整したい | [有償業務](references/paid-work.md)：対象業務と経験の接点、仕事量・期間・報酬の確認表、調整案 |
| 体験後に判断したい・返信したい | [振り返り](references/debrief.md)：期待と観察事実、未確認事項、次の行動、返信案 |
| サービスの料金・契約・支払い・キャンセル・無償掲載可否が判断に関わる | [公式情報の確認](references/source-checks.md)：出典と時点、説明の差、確認する相手と質問 |

4. 有償業務の条件が揃ってきたら、`python3 scripts/check_trial_terms.py <input.json>` で、実働の合計、期間に配置したときの週あたりの実働、予定額と換算時給、未確認の条件を機械的に出す。入力形式は [有償業務](references/paid-work.md#スクリプト入力) を見る。**求職者の実働と企業担当者の工数は別に数え、無償の作業を予定額に含めない。** 単価が提示されていなければ相場で埋めず、確認質問にする。
5. プロフィール文・応募文は、本人が示した経験、今回の業務との接点、希望する体験、提供可能な時間から依頼に合う長さで作る。企業の募集要件と本人の経験を混ぜず、不明な資格・実績・稼働条件を補わない。未確認の条件は質問にし、本人が選んでいない希望条件は原稿外の提案にする。
6. 私的な整理と相手に送る下書きを分けて返す。条件調整では「企業の提示」「本人の希望」「提案」「双方の合意」「未確認」を区別し、合意の根拠になる本文や発言を添える。承認・同意を表す返信は本人が決めた場合だけ下書きする。

## 判断上の制約

- 依頼された原稿または計画を中心に、判断前に確認すること、次に誰が何をするかを添える。毎回すべての段階の報告書を出さない。
- 報酬額、契約形態、法令、サービス条件を記憶で断定しない。未確認をゼロ・不適合・合意済みに置き換えない。
- 通過率、採用の見込み、適性、入社すべきかを断定しない。体験で確認できた範囲と、追加で確かめたいことを示す。
- このスキルだけで完結する。一般的な自己分析・企業研究・内定比較へ話が広がった場合、導入済みなら既存の関連スキルを案内できるが、利用を前提にしない。

## 個人情報と権限境界

初版は相談・分析・原稿作成・運用準備のみ。応募、プロフィール登録・更新、チャット送信、日程確定、契約承諾、キャンセル、レビュー公開は、利用者から操作を依頼されても本人が行う。対象・下書き・希望時期・操作の影響・未確認条件を示して本人に引き渡す。ログイン情報を求めない。

氏名、連絡先、在籍企業や顧客の非公開情報などを必要以上に集めず、相手への原稿に内部メモや他社の選考状況を混ぜない。利用者が明示的に求めない限り、原稿・入力・結果をファイルに残さない。求められた保存も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
