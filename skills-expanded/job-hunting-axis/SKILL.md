---
name: job-hunting-axis
description: "Turn vague preferences about employers into criteria that can actually be used to choose between them: for each one, what would have to be seen to confirm it, whether it comes from firsthand experience or from an untested assumption, whether it is a must, a nice-to-have, or something to avoid, and which pairs of criteria pull against each other while both being treated as required, then test the set against real candidates. Use when a new graduate is working out what to select employers on, when someone who has decided to move needs criteria for where to apply, or when a stated axis like \"a place I can grow\" needs to be made checkable; do not use to recommend an industry, job, or employer, to score or rank candidates, or to judge someone's stated preferences."
license: MIT
metadata:
  author: ficilcom
---

# 就活・転職の軸づくり

応募先を選ぶ基準を、**実際に候補を選り分けられる形**にする。各基準について「何を見れば確認できるか」「何に基づく基準か」を決め、両立しにくい組み合わせを見つけ、候補に当てて確かめる。業界・職種・企業の推薦、候補の順位付け、適性の診断は行わない。

## 進め方

1. **いま思っていることを、言葉のまま先に出してもらう。** 整った形を最初から求めない。「成長できる環境」「風通しが良い」で構わない。ここで言い換えを急がない。
2. 各基準について、**何を見れば確認できるかを決める。** これがこのスキルの中心である。確認方法が言えない基準は、候補を選ぶのに使えない。**基準として悪いのではなく、確認方法がまだ決まっていないだけ**として扱う。捨てさせない。
3. 確認する場所を分ける。公開情報で見るもの（`company-research`）、求人票・労働条件で見るもの（`job-posting-analysis`、`offer-terms-check`）、面接で聞くもの（`interview-prep`）。**どこで確認するかまで決めて、初めて軸になる。**
4. 各基準を `must`（満たされなければ受けない）／ `want`（あると良い）／ `avoid`（あったら受けない）に分ける。**`avoid` を必ず聞く。** 欲しいものだけでは、外すべき候補を判別できない。
5. 各基準が何に基づくかを記録する。自分の経験か、人から聞いたことか、想像か。**新卒では想像に基づく基準が多くなるのが自然であり、それを甘いと評価しない。** やることは、確かめる方法を決めることだけである。
6. `python3 scripts/check_axis.py <input.json>` で、確認方法のない基準、想像に基づく基準、`avoid` の欠落、両立しにくい必須の組み合わせ、候補ごとの未確認の割合を機械的に出す。入力形式は [軸の作り方](references/building-the-axis.md#スクリプト入力) を見る。
7. 候補3〜5社に当てて確かめる。**全社が同じ判定になる軸は、選ぶのに使えていない。** 判定できない軸は、確認方法が足りない。**未確認の多い候補を、不適合として外さない。**
8. [報告書形式](references/report-format.md) に従って出す。**軸が変わることを失敗として扱わない。** 候補を見て変わるのは確かめた結果である。変えた場合は理由を記録する。

## 判断上の制約

- **どの業界・職種・企業を選ぶべきかを推薦しない。** 「あなたには◯◯業界が向いている」と書かない。示せるのは、基準が使える形になっているか、候補が基準を満たすかまでである。
- **候補に適合度の点数をつけない。順位をつけない。おすすめを出さない。** 外すかどうかは利用者が決める。
- **軸の当否を評価しない。** 「その軸は甘い」「もっと具体的にすべきだ」と書かない。確認方法があるかどうかだけを見る。抽象的な言葉は、確認方法を作る対象であって、直させる対象ではない。
- **「やりたいことが見つかっていない」を問題として扱わない。** 見つかっていない状態から始めるのが普通である。避けたいことから始めてよい。
- 性格や適性を診断しない。向いている職種を断定しない。診断ツールの結果を、こちらで解釈し直さない。
- **大学名、学部、学歴、年齢を根拠にした候補の絞り込みをしない。** 「その学歴なら」といった前提を持ち込まない。
- 「大手か中小か」「安定か成長か」「give か take か」といった二項対立に押し込まない。利用者の言葉のまま扱う。
- 内定の見込み、選考の難易度、倍率を見積もらない。候補の絞り込みの根拠にしない。
- 想像に基づく基準を否定しない。同時に、確かめないまま必須として扱わない。**確かめる方法を決めるところまでを扱う。**
- 家族、友人、大学、周囲の期待を、判断材料として代弁しない。利用者が自分から挙げた場合のみ、事実として扱う。
- 現職の経験に基づく軸が、1社の経験の一般化になっていないかを見る。ただし**一般化していると断定しない。** 確認する論点として残す。

## 個人情報と権限境界

このスキルは基準の整理と候補との突き合わせのみを行う。**応募の送信、求人サイトやATSへの登録、エージェントへの連絡、企業へのエントリー、説明会やインターンの申し込みを自動実行しない。** 実行が必要な段階では、送信先・内容・時期を示して利用者の明示的な承認を得る。

軸づくりでは、家庭の事情、健康状態、経済状況、価値観といった、応募書類には不要な情報が出てくることがある。**利用者が自分から話した範囲を超えて聞き出さない。** 家族構成、収入、病名、信条を、基準の整理に必要のない範囲まで集めない。

利用者が明示的に求めない限り、軸や候補の一覧をファイルに残さない。他者（友人、同期、同じ選考を受けている人）の選考状況や志望先を、この作業に持ち込まない。
