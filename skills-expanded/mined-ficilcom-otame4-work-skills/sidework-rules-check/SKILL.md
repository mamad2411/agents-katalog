---
name: sidework-rules-check
description: "Check whether a user may start side work alongside their current job, by reading the employer's own rules and contract clause by clause: whether side work is prohibited, needs prior permission, or only a notification, and which duties the planned side work could touch (non-compete, confidentiality, exclusive attention to the main job, use of company assets and information, combined working hours). Separate what is confirmed in a document from what is hearsay, and produce the questions to ask the employer plus the facts an application or notification will need. Use when someone with a main job is considering side work, freelance or gyomu-itaku work, a second part-time job, or paid trial work for another company, and needs to know what their own employer's rules require first; do not use to rule on whether a clause is lawful or enforceable, to help conceal side work from an employer or avoid filing obligations, to predict whether permission will be granted, or to submit the application or contact the employer."
license: MIT
metadata:
  author: ficilcom
---

# 副業の可否と手続きの確認

いま勤めている先の定めに照らして、**その副業を始めてよいか**を項目ごとに確認する。就業規則・雇用契約・誓約書のどこに何が書かれているかを根拠付きで記録し、禁止・許可制・届出制・規定なしを区別し、競業、秘密保持、職務専念、会社の設備と情報、本業と合わせた稼働時間のうち、計画している副業が触れるものを出す。規定の適法性や有効性の判定、許可が下りるかの予測、会社に知られない方法の設計、申請の代行は行わない。

## 進め方

1. **根拠を最初に確定する。** 「うちは副業禁止と聞いている」「同僚がやっている」は根拠にしない。就業規則、副業に関する規程、雇用契約書、入社時の誓約書のうち、**実際に本文を読んだもの**を記録する。読めていない場合は、それ以降の全項目が未確認であることを先に伝え、どこで閲覧できるか（社内ポータル、人事、事業場に備え付けられた正本）を確かめる手順に進む。
2. 立場を固定する。民間企業の雇用労働者か、公務員か、すでに個人事業主か、学生かで、適用される定めが違う。**公務員は法律に基づく制限があるため、民間の就業規則の話に混ぜない。** 根拠規定と所属先の運用を別々に確認する。
3. 副業の型を固定する。他社に雇われる（雇用）か、業務委託・請負か、自分の事業か、資産運用かで、労働時間の通算、社会保険、確定申告の論点が変わる。**契約の名称ではなく働き方の実態で扱いが変わりうる**ため、名称だけで確定させない。
4. [副業の規定と抵触しうる義務](references/rules-and-obligations.md) の一覧に沿って、項目ごとに**記載の有無**と**出典**を記録する。規定の文言は原文で写す。「副業は原則禁止」と要約すると、但し書きと許可の条件が落ちる。**読んでいない項目を「規定なし」に丸めない。** 見て記載がなかった項目だけを `missing` にする。
5. 計画している副業の中身を、義務ごとに突き合わせる。取引先や同業他社が相手か、本業で知った情報を使うか、勤務時間や会社の設備・アカウントを使うか、本業の繁忙期と重なるか。**該当するかどうかを推測で決めず、確認すべき質問に変える。**
6. `python3 scripts/check_sidework_rules.py <input.json>` で、確認できている項目、根拠のない項目、本業と副業を合わせた週の稼働、申請に必要な情報の欠落を機械的に確認する。入力形式は [副業の規定と抵触しうる義務](references/rules-and-obligations.md#スクリプト入力) を見る。
7. [報告書形式](references/report-format.md) に従って、確認表、抵触しうる論点、合計の稼働時間、会社に聞く質問、申請・届出に書く材料を出す。質問は「始める前に確認するもの」と「始めてから確認してよいもの」に分ける。

## 判断上の制約

- **規定の適法性や有効性を判定しない。** 「副業禁止は無効」「この規定は違法」と断定しない。争いのある論点は、社内の相談窓口、労働基準監督署の総合労働相談コーナー、弁護士や社会保険労務士への相談を選択肢として残す。
- **会社に知られない方法を設計しない。** 住民税の徴収方法、社会保険の届出、確定申告の書き方を、発覚を避ける目的で組み立てない。何が勤務先に伝わるかは確認事項として扱い、申告や届出の義務を回避する手順は作らない。利用者が隠す前提で聞いてきた場合も、正規の手続きと規定の確認に戻す。
- 公務員は法律に基づく制限があり、民間の就業規則とは別の判断になる。許可・承認の要否と根拠規定は、所属先の公表資料と規程で確認する。国家公務員と地方公務員、常勤と非常勤でも扱いが違いうるため、ひとまとめにしない。
- **制度は時点で変わる。** 参照資料の一覧は確認の起点であって、現行制度の保証ではない。労働時間の通算、社会保険の適用、確定申告の要否に判断が及ぶ場面では、厚生労働省・日本年金機構・国税庁の公表資料で現在の内容を確認し、確認できない場合は未確認と書く。記憶で断定しない。
- 労働時間の通算や社会保険の扱いは、契約の名称ではなく働き方の実態で変わりうる。「業務委託だから通算されない」と断定しない。実態に争いがありうる場合は、確認先を示すところまでにする。
- 就業規則に副業の記載がないことを、許可されていることと同じに扱わない。示すのは、現時点で確認できていないという事実と、誰にいつ聞くかまでである。
- 許可が下りるか、届出が受理されるか、前例があるかを予測しない。申請文の下書きは作れるが、通るかどうかは書かない。
- 収入の見込みから、税額や申告の要否を確定的に計算しない。金額の区切りは条件付きで、所得の区分と住民税の扱いが別にある。
- 稼働時間の合計は、健康と本業への影響を見るための数え上げであり、上限規制の適否の判定ではない。参照する水準は利用者が一次情報で確認した値を使い、こちらで補わない。

## 個人情報と権限境界

このスキルは規定の確認と、質問・申請材料の準備のみを行う。**会社への副業申請・届出の提出、上長や人事への連絡、副業先への応募・連絡・契約の締結を自動実行しない。** 申請文や質問の文面を下書きした場合も、提出先・内容・時期・影響を示して利用者の明示的な承認を得る。申請は一度出すと取り消せず、検討段階であることが勤務先に伝わるため、代行しない。

就業規則、社内規程、誓約書は勤務先の非公開情報であることがある。確認に必要な条文の範囲を超えて出力・要約・保存しない。副業先の名称、報酬額、取引先名、同僚の事例も、確認に必要な範囲を超えて扱わない。利用者が明示的に求めない限り、規定の内容や確認結果をファイルに残さない。
