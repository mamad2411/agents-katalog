# Classification Overlay Prompt Contract

親エージェントまたはサブエージェントが、`skill_miner_prepare.py` の **1 候補につき 1 ファイル** の classification overlay JSON を生成する際の入出力仕様である。LLM 呼び出しは `skill_miner_proposal.py` 内には含めず、この contract に従った JSON をファイルとして渡す。

**対象候補の絞り込み**: 全 `ready` / `needs_research` に対して必ず overlay を作る必要はない。`classify-target-selection.md` を参照し、曖昧候補だけを分類する。`triage_status: rejected` の候補は原則この contract の対象外（overlay を作らない）。

詳細な分類境界は `classification.md`、proposal 全体は `proposal-json-contract.md` を参照する。

## 入力（各候補について読むフィールド）

`prepare.json` の `candidates[]`、または `skill_miner_proposal.py --classification-targets-only` の `classification_targets[].candidate` から、対象 `candidate_id` のオブジェクトを 1 件選び、少なくとも以下を根拠に分類する。

| フィールド | 用途 |
|-----------|------|
| `candidate_id` | overlay の `candidate_id` と一致させる必須キー |
| `label` | 候補の表示名・要約 |
| `triage_status` | `ready` / `needs_research` / `rejected`（**rejected は原則 overlay を作らない** — 他候補も `classify-target-selection.md` で省略可） |
| `proposal_ready` | 正式提案に載るか |
| `suggested_kind` | Python `infer_suggested_kind` の事前付与（空の場合あり）。尊重するか override するかを判断する |
| `confidence` / `confidence_reason` | 観測の強さ |
| `evidence_items[]` | タイムスタンプ・ソース・要約（**分類判断の主根拠**） |
| `intent_trace` | 意図のトレース（補助） |
| `common_task_shapes` / `artifact_hints` / `rule_hints` | 手順・成果物・ルールの手がかり |
| `representative_examples` | あれば代表例 |
| `constraints` / `acceptance_criteria` | 制約・受け入れ条件 |
| `support` | 出現度・ソース多様性（補助） |
| `research_brief` | `needs_research` のときの論点（補助） |

**優先ルール**: 判断は `evidence_items` と `label` を中心にし、raw 履歴の再読込はしない（prepare contract のみ）。

`classification_targets[].candidate` は **prompt 入力用のスナップショット**で、上表のキーだけを保持する。内部の merge 状態や補助メタは外側の `reason_codes` / `heuristic_kind` などで見える化し、candidate 本体には混ぜない。

## 出力 JSON contract（1 ファイル = 1 候補）

トップレベルは **JSON object**。配列のみの JSON は無効として扱われ、当該ファイルはスキップされる。

```json
{
  "candidate_id": "<prepare と同一の ID>",
  "classification": {
    "llm_suggested_kind": "CLAUDE.md | skill | hook | agent",
    "llm_reason": "1-3 文。なぜこの分類か（日本語または英語可）",
    "confidence": "high | medium | low",
    "why_not_other_kinds": ["任意: 他分類でない理由を短く"]
  }
}
```

### フィールド規約

- **`llm_suggested_kind`**（必須に近い）  
  4 値のいずれか。`plugin` は使わない。  
  Python 側の事前 `suggested_kind` と同じでもよい（明示的に確定したことになる）。
- **`llm_reason`**（必須に近い）  
  override 時は必ず内容のある説明。Heuristic と同じ结论でも、検証メモとして 1 文あってよい。
- **`confidence`**（任意）  
  付与してよい。現行の `skill_miner_proposal.py` は **confidence 値に応じて guardrail を変えない**（観測・説明用）。proposal の `classification_guardrail_signals.llm_confidence` にエコーされる。
- **`why_not_other_kinds`**（任意）  
  文字列の配列。空配列可。

互換エイリアス（読み取り側が受理）: `classification` 内の `suggested_kind` / `kind` を `llm_suggested_kind` の代替として解釈される場合がある。新規生成では `llm_suggested_kind` を推奨する。

## 4 分類の定義（要約）

| 分類 | 適用の形 | 目安 |
|------|------------|------|
| `CLAUDE.md` | リポジトリ内のルール・原則として毎回従わせる | 手順より「守るべきルール」が中心 |
| `skill` | 入出力と手順が明確な再利用ワークフロー | 人が呼び出す多段フロー |
| `hook` | タイミングで自動実行する機械的処理 | 判断不要・副作用が読みやすい |
| `agent` | 継続的な役割・振る舞いが価値の中心 | 単一フローに落ちない「立ち位置」 |

境界の詳細・例は `classification.md` を正とする。

## Guardrail（生成側の注意）

提案スクリプト側で最終調整が入る。特に **`agent` は証跡が弱いと `skill` 等へ落とされる**ことがある。無理に `agent` にせず、根拠が薄いときは `confidence: low` としつつ保守的な分類に寄せてよい。

## Few-shot 例

### 例 1: Heuristic が `skill`、LLM が `CLAUDE.md` に寄せる

**状況**: `suggested_kind` が `skill`、証跡は「毎 PR で findings-first を求める」が繰り返されている。

```json
{
  "candidate_id": "c-pr-001",
  "classification": {
    "llm_suggested_kind": "CLAUDE.md",
    "llm_reason": "Evidence shows repeated repo-wide review norms, not a multi-step tool workflow. Better as a documented rule.",
    "confidence": "medium",
    "why_not_other_kinds": ["Not a single automated hook; not a persistent role across unrelated tasks."]
  }
}
```

### 例 2: 空の `suggested_kind`、テスト実行パターンを `hook` と判断

**状況**: `suggested_kind` が空、`task_shape` が `run_tests` 中心で、人の判断がほぼ不要。

```json
{
  "candidate_id": "c-test-002",
  "classification": {
    "llm_suggested_kind": "hook",
    "llm_reason": "Repeated mechanical test runs before close; fits an automated gate more than a manual skill.",
    "confidence": "high",
    "why_not_other_kinds": ["Not primarily declarative repo rules (CLAUDE.md). Not a multi-step guided workflow (skill)."]
  }
}
```

### 例 3: LLM が `agent` を試みるが証跡は弱い（`confidence: low`）

**状況**: ラベルは「レビュー担当のように振る舞う」だが、セッション証跡は 2–3 件に留まる。

```json
{
  "candidate_id": "c-role-003",
  "classification": {
    "llm_suggested_kind": "agent",
    "llm_reason": "User repeatedly asks for a standing reviewer mindset across tasks; role consistency is the main value.",
    "confidence": "low",
    "why_not_other_kinds": ["Not a fixed checklist skill; not a single hook trigger."]
  }
}
```

（※ この例ではスクリプトの guardrail により `skill` 等へ落ちる可能性がある。観測が増えたら再分類する想定。）

### 例 4: LLM が `hook`、guardrail が `CLAUDE.md` に戻す（ルールだけ先に付いたケース）

**状況**: `rule_hints` に `tests-before-close` があり、ヒューリスティックは `CLAUDE.md` 寄り。LLM は「ゲートだから hook」としたが、混在 task_shape やツール証跡が弱いと script 側で `CLAUDE.md` に落ちることがある。

```json
{
  "candidate_id": "c-gate-004",
  "classification": {
    "llm_suggested_kind": "hook",
    "llm_reason": "Automated verification before merge.",
    "confidence": "medium",
    "why_not_other_kinds": ["Not a standing role (agent). Not a multi-step manual skill."]
  }
}
```

生成側は `evidence_items` で **run_tests が先頭の機械的パターン**か、**tests-before-close + 十分な観測**かを確認するとよい。

### 例 5: LLM が `agent`、guardrail が `skill` に落とす（証跡不足）

**状況**: ラベルだけ「ヘルパー agent」風だが、`intent_trace` が 1 行だけ、`total_packets` も少ない。

```json
{
  "candidate_id": "c-weak-005",
  "classification": {
    "llm_suggested_kind": "agent",
    "llm_reason": "Feels like a helper role.",
    "confidence": "low",
    "why_not_other_kinds": []
  }
}
```

**観測**: proposal JSON の `classification_trace` に `guardrail` ステップが付き、`classification_guardrail_signals.agent_role_consistency` が `false` になりやすい。

## ファイル配置と proposal への渡し方

- パス例: `$SESSION_TMP/classifications/<candidate_id>.json`
- `skill_miner_proposal.py` に **`--classification-file` を候補ごとに繰り返し**渡す:

```bash
python3 .../skill_miner_proposal.py \
  --prepare-file "$SESSION_TMP/prepare.json" \
  --classification-file "$SESSION_TMP/classifications/c1.json" \
  --classification-file "$SESSION_TMP/classifications/c2.json" \
  ...
```

不正な JSON のファイルは読み飛ばされ、その候補は **heuristic のみ**で proposal が組み立てられる。
