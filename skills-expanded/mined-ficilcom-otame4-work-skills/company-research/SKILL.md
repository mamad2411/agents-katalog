---
name: company-research
description: Research a specific company before applying or interviewing by gathering facts from primary and official sources, recording the source and date behind every claim, and keeping anonymous or unverifiable material clearly separated from confirmed fact. Use when a user asks what a company actually does, how it makes money, what its published conditions are, whether a posting matches the company's own disclosures, or what to verify before an interview; do not use to predict hiring outcomes, to repeat review-site content as fact, or to bulk-crawl sites that prohibit automated access.
license: MIT
metadata:
  author: ficilcom
---

# 企業研究

応募先の企業について、出典を明示できる事実だけを集め、確認できたこと・報道にとどまること・未確認のこと・不明なことを分けて示す。企業の良し悪しの断定、選考通過の予測、口コミの事実化は行わない。

## 進め方

1. **最初に情報取得の可否を確かめる。** Web検索やページ取得のツールが使える環境かを確認し、使えない場合は利用者にURLか本文を貼ってもらう手動モードに切り替える。**取得手段がないまま、記憶から企業情報を書かない。** 会社名・事業内容・業績・従業員数を推測で答えることは、このスキルの最も重大な失敗である。
2. 対象を一意に固定する。同名企業、グループ会社、持株会社と事業会社の取り違えを防ぐため、正式商号、法人番号または本社所在地、募集元がどの法人かを先に確定する。ここが曖昧なまま調査を進めない。
3. 利用者が何を判断したいのかを聞く。応募するか、面接で何を聞くか、内定を受けるか、志望動機を書くかで、必要な深さと論点が変わる。全項目を等しく調べて時間を使わない。
4. [出典の階層と当たり先](references/source-tiers.md) の順で集める。一次資料と会社の公式情報を先に当たり、報道は補助、口コミ・まとめ記事・SNSは最後に「未確認の論点」としてのみ扱う。主張ごとに出典URL、公開日、取得日を必ず記録する。
5. 集めた主張を JSON にして `python3 scripts/check_source_coverage.py <input.json>` にかけ、証拠水準、鮮度、網羅の穴、出典間の矛盾を機械的に確認する。入力形式は [出典の階層と当たり先](references/source-tiers.md#スクリプト入力) を見る。
6. 求人票・スカウトメールの記載と、会社の公式情報を突き合わせる。事業内容、設立年、従業員数、勤務地、雇用形態の食い違いは、そのまま面接で確認すべき論点になる。食い違いの原因を推測で埋めない。
7. [報告書形式](references/report-format.md) に従って出す。確認済みの事実、報道どまり、未確認、不明を分け、各事実に出典と時点を添え、最後に「まだ確認できていないので面接で聞くこと」を残す。

## 判断上の制約

- **記憶から企業の事実を書かない。** 取得できなかった項目は `unknown` とし、空欄を埋めない。有名企業でも同じ扱いにする。
- 転職口コミサイト、まとめ記事、匿名の書き込み、SNSの投稿を確認済みの事実として扱わない。「そういう指摘がある」という論点としてのみ残し、一次情報で裏が取れるかを別に確認する。
- 利用規約で自動アクセスを禁止しているサイトを機械的に巡回しない。取得は公開ページの個別参照と検索にとどめる。ログインが必要な領域、有料会員向けの内容、robots.txt が拒否している経路に入らない。
- 業績数値には必ず決算期と、連結か単体かを添える。異なる期・異なる集計範囲の数値を並べて比較しない。
- 訴訟、行政処分、労働法令違反、希望退職などのネガティブ情報は、行政の公表資料か報道で確認できるものだけを、時点と出典を付けて示す。噂を根拠に企業を評価しない。
- 従業員数、平均年収、離職率は集計時点と定義（連結/単体、正社員のみか、有価証券報告書上の定義か）で大きく変わる。定義が確認できないものは比較に使わない。
- 企業の将来性、安定性、「やめた方がいい」といった総合評価を断定しない。示すのは事実、出典、時点、そして利用者が確認すべき論点までである。

## 個人情報と権限境界

このスキルは公開情報の調査と整理のみを行う。企業、採用担当者、現職・退職者への問い合わせ、SNSでのコンタクト、応募の送信、面接日程の確定を自動実行しない。それらが必要な段階では、送信先・内容・時期を示して利用者の明示的な承認を得る。

特定の個人（面接官、社員）の経歴、SNS、私生活を調べない。公開されている役員情報や、企業が公式に紹介している社員インタビューの範囲を超えない。利用者の応募状況や個人情報を、調査のために外部へ送らない。
