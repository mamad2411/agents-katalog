---
name: commit-prep
description: commit前の差分整理、stage対象選定、commit分割相談、commit message作成、またはcommit依頼で使用し、staged / unstaged / untrackedとunrelated changeを分けて論理単位、stage候補、検証状況、日本語件名と必要な本文・英語要約を提案する。明示依頼なしにstage / commitしない。
---

# Commit preparation

成果物は、論理的なcommit単位、staged / unstaged / untrackedの分類、stage候補、commit messageである。
既存verification evidenceを確認し、不足時だけverifyへ戻る。auditやverifyの後に自動起動するSkillではない。

## 固有契約

- staged、unstaged、untrackedを必ず分ける。
- 今回の目的とunrelated changeを同じstage候補へ混ぜない。
- 明示依頼なしに`git add`や`git commit`を実行しない。
- `git add .`を無条件に提案・実行しない。
- 実行していないtest、未確認のIssue完了、未実装の変更をmessageへ書かない。
- commit実行直前にstage対象とstaged diffを再確認する。
- repository固有のcommit規約と直近履歴を優先する。
- 実施済み検証は実行commandと結び付け、pass、fail、warning、partial、environment blocked、not runを分ける。判断は`verify` Skillの契約に従う。

## Preflight

同一作業内のread-only情報は対象と鮮度が十分なら再利用し、次の状態の不足・変化だけを再取得する。
commit実行直前のstage対象・staged diffの再確認は省略しない。

```bash
git status --short --branch
git diff
git diff --cached
git diff --check
```

staged変更があれば必要に応じて`git diff --cached --check`も確認する。untracked fileは対象判断に必要な範囲だけ読む。目的が不明なfileや秘密情報らしきfileは開かず、「内容未確認」として候補から外す。

既存verification evidenceの対象diff / commit、検証範囲、実行後の変更、環境を確認する。
現在のstage候補を十分に覆う新鮮な結果があれば再実行せず、不足・古い結果・未解決riskがある場合だけverifyへ戻す。

## Path classification

各pathを次へ分類する。

- 今回のcommitに必要
- 同じ目的だが別commitが妥当
- unrelatedな既存変更
- generated artifactまたは検証副作用
- 内容未確認
- repository外の通常handoff、または今回のcommit対象外の一時file
- 明示的にrepositoryへ収蔵されたhandoff: 今回のcommit目的との関係を確認して判断

同じfileに今回の変更とunrelated changeが混在する場合は、file単位stageで分離できないことを明記する。依頼なしにinteractive stagingや差分の手作業分割を行わない。

## Commit unit

次を基準に分ける。

- 1つの目的と理由で説明できるか。
- 一方だけrevertしても整合するか。
- code、test、docsが同じ契約変更を表すか。
- review時に意図を独立して判断できるか。
- cleanupやformattingだけの変更が混在していないか。

file数だけで機械的に分けない。同じ契約のcode、test、docsは同一commitが自然な場合がある。

## Stage candidates

pathを明示する。

```text
commit 1:
- path/to/file-a
- path/to/file-b

除外:
- path/to/unrelated-file: 既存のunrelated change
```

stageが明示依頼された場合だけ、対象を絞った`git add -- <path>...`を使う。globやrepository全体を対象にする前に含まれるpathを確認する。

## Commit message

- 直近履歴とrepository規約を確認する。
- 日本語件名を主案とし、`git log --oneline`で目的が分かる具体性を持たせる。
- repositoryが採用している場合だけtype / scope prefixを使う。
- 背景、制約、非目標、検証を残す価値がある場合だけ本文を付ける。
- 英語要約がproject運用で必要または有用な場合は、日本語の補足として提案する。

例:

```text
docs: Codex規約の責務をグローバルとprojectへ分離
```

## Stage / commit実行時

ユーザーが明示した範囲だけ実行する。

1. 対象pathを再提示してstageする。
2. `git status --short --branch`と`git diff --cached`を再確認する。
3. `git diff --cached --check`と実施済み検証を確認する。
4. commitまで依頼されている場合だけcommitする。
5. commit SHAと直後のstatusをread-onlyで確認する。

pushは別の明示依頼として扱う。

## 失敗時

- pathの目的が不明なら「内容未確認」とし、候補から外す。
- diff check失敗は該当pathを報告し、commit準備だけの依頼なら勝手に修正しない。
- staged内容が想定と違えばcommitしない。
- timeoutや部分成功の可能性があれば、同じmutationを繰り返す前に現在状態を確認する。

## 出力

現状、推奨commit単位、stage候補、除外変更、検証状況、message案、未確認を報告する。stage / commitを実行した場合は、実行command、対象path、commit SHA、直後のstatusを追加する。
