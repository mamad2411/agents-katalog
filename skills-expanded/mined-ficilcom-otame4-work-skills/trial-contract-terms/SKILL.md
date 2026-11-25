---
name: trial-contract-terms
description: "Check, from the employer's side, what has been put in writing before a paid Otameshi Tenshoku assignment starts under gyomu-itaku: item by item whether the deliverable, delivery date, fee and how it is calculated, payment due date, who pays, out-of-scope work, revision limits, company support, rights, confidentiality and termination are stated in a contract, purchase order or email rather than in chat or by word of mouth, count the days from delivery to payment, and find pay tied to satisfaction or hiring, unpaid or unlimited revisions and one-sided termination. Use when a hiring manager, recruiter or small-business owner is about to offer terms to a candidate, has been asked by a candidate what is still unwritten, or needs the conditions written for a platform contract screen; do not use to judge whether the terms are lawful or the fee fair, to compute withholding or consumption tax, for employment contracts, or to sign, send or conclude the contract on the user's behalf."
license: MIT
metadata:
  author: ficilcom
---

# おためし転職：発注側の契約条件の明示

有償のおためし業務を業務委託で発注する企業の側から、給付の内容、受領期日、報酬と算定方法、支払期日、支払主体、範囲外、修正の上限、企業の支援、権利、秘密保持、中途解除が、着手前に契約書・発注書・電子メールで候補者に示されているかを項目ごとに確かめ、受領から支払期日までの日数を数え、成果や採用判断を支払いの条件にする定め、無償や上限のない修正、企業側だけの解除を候補者に提示する前に直す。専任の採用担当者、現場のマネージャー、小規模企業の経営者のいずれからでも、計画のメモと条件の下書きから着手する。条件の適法性や報酬の妥当性の判定、源泉徴収・消費税の計算、雇用契約の扱い、契約の送付・署名・締結の代行は行わない。

## 進め方

1. **契約の型を最初に固定する。** 業務委託か雇用かで確認する項目がまるごと変わる。雇用なら労働条件の明示が論点になるため、この確認表を使わず確認先を示す。名称が「業務委託」でも、時間で拘束し指揮命令する計画は扱いが変わりうるため、計画（あれば `trial-work-design` のもの、なければ利用者への聞き取り）で就業場所・時間の拘束、指示の受け方、代替の可否などの実態を確かめ、**名称だけで確定させない。** 疑いがあるときは確認先を示すところまでにする。
2. 条件を何に書いているか（契約書、発注書、メール、サービスの契約画面、チャット、口頭、未着手）を確かめる。**チャットや口頭で伝えた条件を「明示した」と扱わない。** チャットで伝えた条件があるなら、それは「未着手」ではなく「書面でない出所」として記録する。 サービスの契約画面が書面に準じるかは [公式情報の確認](references/source-checks.md) で確かめる。
3. [発注側が着手前に明示する取引条件](references/required-terms.md) の一覧に沿って、項目ごとに記載の有無と出所を記録する。文言は原文で写す。「納得するまで」「随時」は、記載ではなく範囲が閉じていない条件として扱う。**見ていない項目を「記載なし」に丸めない。**
4. `python3 scripts/check_contract_terms.py <input.json>` で、明示の状況、予定額、支払期日までの日数、支払条件、修正と解除の定め、提示前に直す点を機械的に出す。入力形式は [発注側が着手前に明示する取引条件](references/required-terms.md#スクリプト入力) を見る。条件の内容をファイルに残さないため、入力は標準入力から渡すのを既定にする。支払期日の上限として入れる日数は、一次情報で確認した値だけにする。
5. 支払期日の上限、支払主体、労働者性、税の扱いが判断に関わる場合は、[公式情報の確認](references/source-checks.md) で現在の内容を確認する。確認できない項目は未確認のまま残し、そこに依存しない部分の下書きは作る。
6. [報告書形式](references/report-format.md) に従って、確認表、報酬と支払い、支払までの日数、修正と解除、提示前に直すこと、候補者に送る条件の文面の下書きを出す。着手前に書面で確定させるものと、進めながら決めてよいものを分ける。

## 判断上の制約

- **適法性を判定しない。** 取引条件の明示、支払期日、減額の禁止などの定めは時点で変わる。参照資料の一覧は確認の起点であって、現行制度の保証ではない。記憶で断定しない。
- **成果への満足や採用の判断を支払いの条件にしない。** 実施済みの実働と検収済みの給付に対する支払いを、評価や採用判断と分ける。中止しても実施済みの実働は支払う前提で精算を書く。
- 修正は回数と時間の上限で閉じ、超える分は追加の発注にする。合意した範囲の修正を無償にしない。
- 中途解除の定めを企業側だけに置かない。候補者側の解除と予告も書く。
- 相場や慣行で条件を補わない。単価がなければ `trial-work-design` に戻して決める。源泉徴収、消費税、経費の扱いは書くが、税額や手取りを計算しない。
- 募集文と契約条件が食い違うなら、差分を示して利用者が直す。候補者に不利な条件を通す交渉の見込みを書かない。
- このスキルだけで使える。計画、募集文、応募者対応の各スキルがなくても、今回の条件の明示は完結する。

## 個人情報と権限境界

このスキルは条件の確認と文面の下書きのみを行う。**候補者への条件の送付、契約書の送付や署名、電子契約やサービス上の契約手続きへの同意、支払いの実行を自動実行しない。** 文面を下書きした場合も、送付先・内容・時期・影響を示して利用者の明示的な承認を得る。契約の締結は取り消しが難しいため、代行しない。

候補者の氏名、住所、口座、請求に関する情報、企業の非公開情報は、確認に必要な範囲を超えて扱わない。利用者が明示的に求めない限り、条件の内容や確認結果をファイルに残さない。保存を求められた場合も公開リポジトリを避け、`private/` 以下かリポジトリ外で扱う。
