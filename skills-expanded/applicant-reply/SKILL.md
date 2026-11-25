---
name: applicant-reply
description: "Reply to an applicant for an employer's Otameshi Tenshoku listing: match the application against the listed requirements item by item on what the applicant actually stated, list the questions still open, and draft an invitation, a request for clarification, a hold notice or a decline that sticks to the listed conditions, keeps other applicants and internal notes out, and presents any new work or dates as a proposal rather than an agreed term. Use when a hiring manager, recruiter or small-business owner has applications to answer, wants to know what to ask before inviting, or has to decline; do not use to judge an applicant's aptitude or predict hiring outcomes, to screen on personal attributes unrelated to the work, to design the work (trial-work-design) or the listing (trial-listing-draft), or to send the message or update applicant records on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：応募者への返信

募集文の要件と応募内容を、応募者が実際に述べたことで突き合わせ、確認が残る点を質問にし、招待・質問・保留・辞退のどれかの返信を作る。返信は募集文の条件の続きとして書き、他候補者の情報と内部メモを混ぜず、募集文にない業務や日程は提案として書く。専任の採用担当者、現場のマネージャー、小規模企業の経営者のいずれからでも、募集文と応募内容の抜粋から着手する。応募者の適性や採用の成否の判定、職務と無関係な属性による選別、送信や応募者管理の更新の代行は行わない。

## 進め方

1. 募集文と受け入れ計画の条件を手元に置く。返信の目的（招待、質問、保留、辞退）が決まっているかを利用者の発言から読み、決まっていなければ照合の結果から候補を示す。返信の期限が迫っているなら、保留の返信を先に作る。
2. [返信の作り方](references/reply-method.md) に従って、募集文の要件を必須と歓迎に分け、要件ごとに応募内容で確認できる範囲を記録する。**応募者が述べていないことを推測で埋めない。** 書かれていないことと持っていないことを分ける。職務と無関係な属性は照合から外す。
3. `python3 scripts/check_applicant_fit.py <input.json>` で、必須要件の確認状況、確認質問にする要件、返信案に混ぜてはいけないもの、合意していない提案、稼働の不足を機械的に出す。入力形式は [返信の作り方](references/reply-method.md#スクリプト入力) を見る。応募内容をファイルに残さないため、入力は標準入力から渡すのを既定にする。利用者が返信の判断に挙げた理由のうち募集文にないもの（年齢などの属性、他候補者との比較）は、入力の `reasoning` に入れて判断から外す。
4. 応募者の稼働や希望で範囲・期間・報酬が変わるなら、`trial-work-design` の計画を作り直してから提案として書く。計画のないまま返信で条件を変えない。導入されていなくても、変更が実働・報酬・期間に及ぶことを示して提案にとどめる。
5. [報告書形式](references/report-format.md) に従って、要件の照合、確認質問、受け入れ担当者用のメモ、返信の下書き、送る前に確認することを出す。メモと下書きは必ず分ける。

## 判断上の制約

- 応募者の適性、能力の評価、採用の見込みを書かない。示すのは要件ごとの確認状況と、確認のための質問までである。
- 職務と無関係な属性（年齢、性別、婚姻、国籍、居住地など）で照合も判断もしない。募集文にそうした要件があれば、募集文の修正点として返す。
- 確認していない必須要件があるうちは辞退の返信を作らない。先に質問を送るか、確認済みの事実だけで判断する。
- 募集文の条件を返信で変えない。変える場合は提案として書き、本人が同意した扱いにしない。
- 応募者の週の稼働が計画より少ないことを辞退の理由にしない。範囲を減らす案か期間を延ばす案を添える。
- 複数の応募者がいる場合は1人ずつ作り、仮名で管理する。候補者どうしの比較を返信に持ち込まない。
- このスキルだけで使える。計画、募集文、契約条件の各スキルがなくても、今回の返信は完結する。

## 個人情報と権限境界

このスキルは照合と返信の下書きのみを行う。応募者へのメッセージ送信、応募者管理の更新、面談日程の確定、辞退や採用の通知は、操作を依頼されても利用者本人が行う。送信前に、宛先、下書き、送る時期、添えた提案の影響を示して引き渡す。ログイン情報を求めない。

応募者の氏名、連絡先、職歴、選考状況は必要最小限だけ扱い、応募者どうしを比較する場合は仮名を使う。他候補者の情報と内部の評価メモを返信案に混ぜない。利用者が明示的に求めない限り、応募内容・下書き・結果をファイル保存しない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
