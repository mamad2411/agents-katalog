---
name: sidework-terms-check
description: "Check the terms of a specific side-work assignment offered as gyomu-itaku or freelance work in Japan, item by item: what the client has actually put in writing about the deliverable, the fee, the payment due date, what counts as out of scope, how many revisions are included, who bears expenses, who owns the result, confidentiality, and how either side can end it. Convert the fee into an effective hourly figure over the hours the work will really take including meetings, revisions and unpaid preparation, and count the days from delivery to the payment due date. Use when someone is offered or is discussing a paid side job, a freelance assignment, spot consulting, or paid trial work and wants to know what is still unwritten before starting; do not use to judge whether the fee is fair or the terms lawful, to decide whether to accept, to draft or sign the contract for the user, or to check whether their employer's rules permit side work, which is sidework-rules-check."
license: MIT
metadata:
  author: ficilcom
---

# 副業案件の取引条件の確認

提示された副業の案件について、取引条件が**着手前に書面や電子メールで明示されているか**を項目ごとに確認し、報酬を見込みの総稼働で割った換算時給と、受領から支払期日までの日数に揃え、着手前に確定させるべき条件を出す。対象は業務委託・請負の案件で、勤務先の規程で副業が認められるかは `sidework-rules-check` が扱う。条件が妥当か、適法かの判定、受けるかどうかの判断、契約書の作成・署名の代行は行わない。

## 進め方

1. **契約の型を最初に固定する。** 業務委託・請負か、他社に雇われる（雇用）かで、確認する項目がまるごと変わる。雇用なら労働条件の明示が論点になるため `offer-terms-check` に渡す。名称が「業務委託」でも、時間で拘束され指揮命令を受ける働き方は扱いが変わりうるため、実態を聞き取り、**名称だけで確定させない。**
2. 提示が何で来ているかを確定する。契約書、発注書、メール、チャット、口頭のどれか。**チャットや口頭の言い値を「明示されている」と扱わない。** 書面がない段階では、それ以降の条件がすべて未確定であることを先に伝える。
3. [明示される取引条件の項目](references/required-terms.md) の一覧に沿って、項目ごとに**記載の有無**と**出典**を記録する。文言は原文で写す。「だいたいこのくらい」「相談しながら」は、記載ではなく未確定として扱う。**見ていない項目を「記載なし」に丸めない。**
4. 作業を分解して、見込みの総稼働を出す。本体の作業だけでなく、打合せ、待ち時間、修正、資料の読み込み、移動、請求書の作成を含める。**無償で求められる作業を総稼働から外さない。** 経験になる、実績になる、といった説明を報酬の代わりに数えない。
5. `python3 scripts/check_sidework_terms.py <input.json>` で、明示の状況、換算時給、受領から支払期日までの日数、範囲の開いている項目、週あたりの稼働が出せる時間に収まるかを機械的に出す。入力形式は [明示される取引条件の項目](references/required-terms.md#スクリプト入力) を見る。
6. [報告書形式](references/report-format.md) に従って、確認表、報酬の換算、支払までの日数、未確定の条件、確認する質問を出す。質問は「着手前に書面で確定させるもの」と「進めながら決めてよいもの」に分ける。

## 判断上の制約

- **条件が妥当か、相場に照らして高いか安いかを判定しない。** 単価の相場を記憶で補わない。換算時給は比較のための割り算であり、時間単価の契約を意味しない。
- **適法性を判定しない。** 取引条件の明示、支払期日、受領拒否や減額の禁止などの定めは時点で変わる。参照資料の一覧は確認の起点であって、現行制度の保証ではない。判断に関わる場面は公正取引委員会・中小企業庁・厚生労働省の公表資料で現在の内容を確認し、確認できない場合は未確認と書く。記憶で断定しない。
- 受けるべきか、断るべきかを結論として書かない。複数の案件を比べる場合も、同じ確認表を各案件に作って並べるにとどめ、優劣を断定しない。
- 最低賃金との比較は、雇用と業務委託で適用関係が違うため、地域と時点を確認したうえで参考にとどめる。換算時給が低いことを、そのまま違法とも適法とも書かない。
- **消費税、源泉徴収、経費の扱いを確定的に計算しない。** 提示額を手取りとして扱わない。インボイスの登録の要否や、所得の区分を判断しない。
- 書かれていない条件を、業界の慣行で補わない。知的財産の帰属、秘密保持の範囲、競業の制限、実績として公開できるかは、契約の文言で決まる。「普通はこうなる」と書かない。
- 交渉が通るかを予測しない。確認や条件変更の依頼文は下書きまで作り、送るかどうかは利用者が決める。
- 発注者の評価、将来の継続受注の見込み、支払能力を推測しない。支払が滞ったときの相談先を選択肢として残すにとどめる。

## 個人情報と権限境界

このスキルは条件の確認と質問の準備のみを行う。**発注者への返信、受諾や辞退の連絡、契約書への署名や電子契約への同意、請求書の送付、案件サイトでの応募や契約手続きを自動実行しない。** 返信や確認の文面を下書きした場合も、送信先・内容・時期・影響を示して利用者の明示的な承認を得る。受諾の意思表示は取り消しが難しいため、代行しない。

案件の資料には、発注者の非公開情報や第三者の情報が含まれることがある。確認に必要な範囲を超えて出力・要約・保存しない。本業の勤務先名、取引先名、報酬額、口座や請求に関する情報も、確認に必要な範囲を超えて扱わない。利用者が明示的に求めない限り、案件の内容や確認結果をファイルに残さない。
