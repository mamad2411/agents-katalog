---
name: interview-prep
description: "Prepare for a Japanese job interview by working from the documents already submitted: find where an interviewer will dig in (claims the applicant cannot back up, work described in the first person plural, outcomes with no measure, gaps or overlaps in the employment history, must-have requirements the documents never answer), and turn them into questions to prepare evidence for. Use when a user has an interview scheduled and wants to know what will be asked and what to have ready, or wants to prepare reverse questions from earlier company research; do not use to predict whether they will pass, to write answers containing experience they did not report, or to schedule or contact anyone."
license: MIT
metadata:
  author: ficilcom
---

# 面接の準備

提出済みの応募書類と求人票を起点に、面接で深掘りされる箇所を特定し、そこで示す**事実**を利用者と詰める。合否の予測、経験の創作、模範解答の代筆は行わない。

## 進め方

1. **提出済みの書類を先に確認する。** 面接は書類の答え合わせから始まる。書類を見ずに想定質問を作らない。書類が手元にない場合は、貼ってもらうか、提出内容を思い出せる範囲で確認し、確認できない部分を `unknown` のまま進める。
2. 面接の条件を固定する。応募区分（新卒・中途）、段階（カジュアル面談・一次・二次・最終）、面接官の立場、形式と日時。**段階が分からない場合は一次を基準にする。** 準備の重心は [深掘りされる箇所](references/probe-points.md#段階による違い) を見る。
3. 書類の主張ごとに、利用者が**根拠を説明できるか**を確認する。説明できない主張が残っている場合、それは想定質問より前に処理する問題である。提出前なら書類を直し、提出済みなら事実の範囲でどう言い直すかを先に決める。
4. `python3 scripts/find_probe_points.py <input.json>` で、根拠が確認できていない主張、主語がチームのままの記述、数値のない成果、職歴の空白と重なり、書類が答えていない必須要件を機械的に洗い出す。入力形式は [深掘りされる箇所](references/probe-points.md#スクリプト入力) を見る。
5. 箇所ごとに、示す事実を利用者と詰める。担当範囲は「決めたこと」「手を動かしたこと」「他者がやったこと」に分ける。**素材が足りない箇所は、利用者への質問として残す。推測で埋めた回答案を作らない。**
6. 現職・前職の守秘に触れる箇所は、話す範囲の線引きを先に決める。未公開の数値、顧客名、契約条件、社内資料の内容を含む回答案を作らない。
7. 逆質問は、`company-research` の「面接で確認すること」と `job-posting-analysis` の「確認すべき質問」を引き継ぐ。調べれば分かることを聞く形にしない。労働条件の書面確認は `offer-terms-check` に回す。
8. [報告書形式](references/report-format.md) に従って、先に直すこと、掘られる箇所と準備、定番の論点、逆質問、利用者への確認事項を出す。

## 判断上の制約

- **合否、通過率、面接官の評価を予測しない。** 「この答え方なら通る」「印象が良い」といった表現を使わない。示せるのは、書類との整合、事実の裏づけ、話す順序までである。
- **経験、数値、役職、資格を創作しない。** 書類と利用者の発言にないことは、回答案としても書かない。数値が思い出せない場合は、数値を使わない言い方を用意する。
- 回答の全文を丸暗記用に書かない。話す順序と、そこで示す事実までにする。利用者の語り口を平板な面接文体に置き換えない。
- スクリプトが出す `priority` は準備の順序であり、`likely_question` は問い方の型である。実際に出る質問の予言として扱わない。想定した質問が出なかった場合に備え、素材を質問の形に縛らない。
- 新卒と中途で見られるものが違う。中途は担当範囲・再現性・数値、新卒は行動の具体性と学びに重心がある。同じ準備を両方の型で同時に最適化しない。
- 転職理由を、前職の批判で組み立てない。同時に、事実に反する前向きな理由を作らない。利用者が実際に何を求めて動いているかから組み立てる。
- 現職・前職の守秘情報を含む回答案を作らない。「話せません」と答えることを減点として扱わない。
- 面接官個人の経歴、SNS、私生活を調べない。企業が公式に出している情報の範囲を超えない。
- 逆質問を「聞くべき質問」の一覧として量産しない。利用者が実際に確認したい論点から作る。

## 個人情報と権限境界

このスキルは準備の整理と質問の洗い出しのみを行う。**面接日程の確定と変更、企業・採用担当者・エージェントへの連絡、選考の辞退、応募の送信を自動実行しない。** 日程調整や辞退の文面を下書きした場合も、送信先・内容・時期を示して利用者の明示的な承認を得る。

応募書類には氏名、連絡先、学歴・職歴、在籍企業名が含まれる。準備に必要のない個人情報を出力・要約・保存しない。他社の選考状況を、この面接の準備に必要な範囲を超えて扱わない。利用者が明示的に求めない限り、準備内容や書類の写しをファイルに残さない。
