---
name: formation-designer
description: oh-my-opencode formation (agent-model configuration) design and creation guide. Use when creating new formations, modifying existing formations, adding new providers/models, or reviewing formation design decisions. Covers multi-axis model classification (Reasoning, Cost, Speed, Instruct, Style, Multimodal), agent-model matching principles, naming conventions, and cost optimization strategy.
metadata:
  internal: true
  tags: [opencode, configuration, model-selection]
---

# Formation Designer

oh-my-opencode のフォーメーション（エージェント-モデル構成）を設計・作成するための方針とリファレンス。

## Core Insight: Models Are Developers

AI モデルはチームの開発者と同じ。同じ指示でも Claude と GPT では解釈が根本的に異なる。「賢いか否か」ではなく「思考スタイルの適合性」がエージェントへの配置基準。

- **Claude 系** (Claude, Kimi K2.5, GLM-5): mechanics-driven。複雑で詳細なチェックリスト型プロンプトに忠実に従う。オーケストレーション向き。
- **GPT 系** (GPT-5.4, Codex): principle-driven。簡潔な原則とゴールから自律的に動く。ルールが多すぎると矛盾面が増えてドリフトする。深い技術作業向き。

## Model Classification

ユーザーが利用可能なモデルの属性分類。単一のティアではなく、複数軸の属性でモデルを評価し、スロット側の要件とマッチングする。

### Attribute Definitions

- **Reasoning**: 複雑なタスクの自律的遂行能力。多段推論・曖昧な指示からの判断力。
  - S+: 最高峰。自律的な深掘り・矛盾検出まで可能
  - S/S-: フロンティア級。高度な戦略的推論
  - A: 十分な推論力。大半のタスクを自力で遂行可能
  - B: 中程度。定型的なタスクや明確な指示には対応可能
  - C: 低。単発の決まった指示のみ遂行可能。多段推論は不向き
- **Cost**: API 利用料・サブスクリプション消費の相対コスト。
  - High / Med / Low
- **Speed**: レスポンス速度。
  - VFast / Fast / Med
- **Instruct**: 複雑・長文プロンプトへの忠実度。チェックリスト型指示の追従性。
  - S / High / Med / Low
- **Style**: 思考スタイル。エージェント配置の適合性に影響。
  - Claude-like: mechanics-driven。詳細なチェックリスト型プロンプトに忠実。オーケストレーション向き。
  - GPT-like: principle-driven。簡潔な原則から自律的に動く。深い技術作業向き。
- **Multimodal**: 単に画像入力に対応しているかではなく、`multimodal-looker` として実用的に機能するかどうか。視覚理解に加えて、レイアウト・デザイン品質・UI の良し悪しを判断できるかを重視する。
  - Yes / No

### Model Attribute Table

| Model | Reasoning | Cost | Speed | Instruct | Style | Multimodal |
|-------|-----------|------|-------|----------|-------|------------|
| `gpt-5.3-codex` | S+ | High | Med | High | GPT-like | Yes |
| `gpt-5.4` | S | High | Med | High | GPT-like | Yes |
| `claude-opus-4.6` | S- | High | Med | S | Claude-like | Yes |
| `glm-5` | A | Low | Fast | Med | Claude-like | Yes |
| `mimo-v2-pro` | A | Low | Fast | Med | Claude-like | Yes |
| `claude-sonnet-4.6` | A | Med | Fast | High | Claude-like | Yes |
| `gpt-5.4-mini` | B | Med | Fast | Med | GPT-like | Yes |
| `gpt-5.3-codex-spark` | B | High | VFast | Med | GPT-like | No |
| `glm-5-turbo` | B | Low | VFast | Med | Claude-like | No |
| `haiku` | B | Low | VFast | Med | Claude-like | No |
| `kimi-k2.5` | C | Low | Fast | Low | Claude-like | Yes |
| `minimax-m2.7` | C | Low | Fast | Low | - | No |

> **方針**: High コストモデル（GPT, Anthropic）の使用を最小限に抑え、Reasoning A-B かつ Cost Low のモデルでコストパフォーマンスを最大化する。

## Agent-Model Matching Principles

### Stable Slots (全フォーメーション共通で変更しない)

| Agent / Category | Requirement (provider-agnostic) | Reason |
|-----------------|----------------------------------|--------|
| **prometheus** | Reasoning **S 以上**, Instruct **High+**, variant `xhigh`. **Fallback: S 級以上のモデルのみ** | 計画は妥協できない。利用可能な手札の中で最上位モデルを使う。fallback 先が弱いモデルでは計画品質が崩壊する。 |
| **momus** | Reasoning **S+ 優先 / S 以上必須**, Instruct **High+**, variant `xhigh` | レビュー品質の一貫性確保。 |
| **hephaestus** | Reasoning **S+ 優先 / S 以上必須**, Style **GPT-like 優先**, variant `xhigh`. **Fallback: S 級以上のモデルのみ** | Deep worker は自律実装能力が最優先。fallback で低tier モデルに落ちると実装品質が保証できない。 |
| Category: **review** | Reasoning **S+ 優先 / S 以上必須**, Instruct **High+**, variant `xhigh` | レビューは品質最優先。 |

> 現行リポジトリでは上記要件を満たすモデルとして OpenAI (`gpt-5.4`, `gpt-5.3-codex`) が使われているが、OpenAI / Claude が利用不可な環境では「利用可能な手札の中で要件を満たす最高モデル」に置換する。

### Variable Slots (利用可能なプロバイダーに応じて変動)

これらのスロットは要件を満たす中で最も安価なモデルを割り当てるコスト最適化枠。
選択手順: **要件で絞る → Cost が最も低いモデルを選ぶ → 同 Cost なら Reasoning が高い方**。

**Utility Agents (Speed 重視・Reasoning は B 以上で十分):**

| Agent | Role | Requirements |
|-------|------|-------------|
| **librarian** | 仕様調査 | Reasoning B+, Cost Low 優先 |
| **explore** | 探索 | Reasoning B+, Speed Fast+, Cost Low 優先 |

**Orchestrators (Instruct 重視。Claude-like は優先だが必須ではない):**

| Agent | Role | Requirements |
|-------|------|-------------|
| **sisyphus** | メインオーケストレータ | Instruct High+ 優先, Reasoning A+。Style Claude-like を優先し、利用不可なら GPT-like の最上位モデルを使用。**Fallback: S 級以上のモデルのみ**（オーケストレーション品質を維持するため低tier モデルへの fallback は禁止）。 |
| **atlas** | 実行コンダクタ | sisyphus と同等の要件（Instruct High+ 優先, Reasoning A+, Claude-like 優先）。**Fallback: 指定しない**。atlas は fallback を使用しない方針とする。fallback は便利だが、atlas で fallback が発動した場合のデメリットが目立つため、fallback なしで運用する。 |
| **sisyphus-junior** | 軽量オーケストレータ | Reasoning B+, Instruct Med+, Cost Low。ZAI 構成でのみ追加。 |

**Intelligence-sensitive (Reasoning S 級が必要):**

| Agent | Role | Requirements |
|-------|------|-------------|
| **oracle** | 相談役 | Reasoning S+ or S。Cost は問わない。 |
| **metis** | 抜け漏れ検出 | Reasoning S+ or S。Instruct High+。 |
| **multimodal-looker** | 視覚処理 | Multimodal Yes 必須。`multimodal-looker` として実用的に作用できるモデルを選ぶ。Reasoning 高い順 (opus-4.6 > codex > glm-5/mimo)。 |

**Category Variable Slots:**

| Category | Requirements |
|----------|-------------|
| **ultrabrain** | Reasoning S 以上必須 |
| **deep** | Reasoning S 以上必須 |
| **visual-engineering** | Multimodal Yes を優先。視覚理解だけでなくデザイン判断が強いモデルを選ぶ (opus-4.6 > sonnet-4.6 > glm-5/mimo > 5.4-mini) |
| **unspecified-high** | Reasoning S- 以上 |
| **unspecified-low** | Reasoning A-B, Cost Low-Med |
| **quick** | Cost Low + Speed VFast-Fast 最優先。Reasoning C でも可 |
| **writing** | Instruct High+ 推奨, Reasoning A-B |
| **research** | Reasoning A-B, Speed Fast+ |
| **refactor** | Reasoning A-B, Cost Low-Med |

## Formation Design Rules

### 1. Naming Convention

フォーメーション名は**使用するプロバイダー**で命名する。抽象ラベル (`normal`, `default`) は禁止。

| Provider | Token |
|----------|-------|
| OpenAI | `openai` |
| ZAI | `zai` |
| GitHub Copilot | `copilot` |
| OpenCodeZen | `opencode` |
| Kimi | `kimi` |

複数プロバイダーは `-` で連結: `openai-copilot-opencode-kimi.jsonc`

### 2. Stable Slots Are Requirement-Fixed, Not Vendor-Fixed

Stable Slots (prometheus, momus, hephaestus, review) はベンダー固定ではなく要件固定。常に Reasoning S 級の最上位モデルを割り当てる。
現行フォーメーションでは OpenAI モデルがこの要件を満たすため結果的に選ばれているが、OpenAI / Claude が利用不可な環境では、利用可能な手札の中で要件を満たす最高モデルを選ぶ。

### 3. Secondary Providers Fill Cost-Optimization Slots

追加プロバイダーのモデルは Variable Slots に優先配置する。高コストな OpenAI モデルの使用を最小限に。

### 4. Fallback Policy

**一般原則**: プライマリが低コストモデルの場合でも、フォールバックチェーンには Reasoning S 級モデルを最低1つ含める。

**エージェント固有の fallback 制約:**

| Agent | Fallback Policy | Reason |
|-------|----------------|--------|
| **sisyphus** | S 級以上のモデルのみ | オーケストレーション品質を維持するため。低tier モデルへの fallback は禁止。 |
| **prometheus** | S 級以上のモデルのみ | 計画品質は妥協できない。fallback 先が弱いモデルでは計画が崩壊する。 |
| **hephaestus** | S 級以上のモデルのみ | 自律実装能力が最優先。低tier モデルでは実装品質が保証できない。 |
| **atlas** | **fallback を指定しない** | fallback は便利だが、atlas で fallback が発動した場合のデメリットが目立つため、fallback なしで運用する。 |

> **重要**: sisyphus, prometheus, hephaestus の fallback には、Reasoning S 級以上のモデルを指定すること。tier の低いモデルを fallback に指定してはならない。強いモデルにのみ fallback されるべきであり、弱いモデルは fallback 先にはなれない。

### 5. sisyphus-junior は ZAI 含む構成でのみ追加

ZAI プロバイダーが利用可能な構成でのみ `sisyphus-junior` を追加する。

### 6. Variant Discipline

| Variant | Use Cases |
|---------|-----------|
| `xhigh` | 大半のエージェント・カテゴリ。深い推論が必要な場面。 |
| `medium` | オーケストレータ (sisyphus, atlas)、高スループットカテゴリ。 |
| `max` | 特別な場合のみ (visual-engineering で opus-4.6 を使う場合など)。 |

### 7. Structural Constants

全フォーメーションで以下を共通に含める:

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/dev/assets/oh-my-opencode.schema.json",
  "claude_code": { "agents": false },
  "autoupdate": true,
  "model_fallback": true,
  "lsp": {
    "markdown": {
      "command": ["marksman", "server"],
      "extensions": [".md", ".mdx"]
    }
  },
  "disabled_hooks": ["comment-checker"]
}
```

### 8. Prompt Append Rules

- 4 つのエージェント (sisyphus, hephaestus, prometheus, atlas) は外部ファイル (`file://~/.config/opencode/prompts/*.append.md`) を使用
- その他のエージェント・カテゴリはインライン文字列で言語指示を設定:
  `"検討や作業は英語で、ユーザーへの回答やドキュメンテーションは日本語でお願いします。"`
- librarian のみ追加で context7 利用指示を含める

### 9. Provider Constraint: Anthropic via Copilot Only

Anthropic モデル (Claude) は直接利用できない。GitHub Copilot 経由 (`github-copilot/claude-opus-4.6`, `github-copilot/claude-sonnet-4.6`) でのみ利用可能。

## Cost Optimization Strategy

### Priority Order for Model Selection

1. **Cost Low から埋める**: Variable Slots には Cost Low かつスロット要件を満たすモデルを最優先で配置
2. **Cost Med で補完**: Cost Low で要件を満たすモデルが不足する場合に Cost Med モデルを使用
3. **Cost High は Stable Slots と Intelligence-sensitive のみ**: Reasoning S 級が必要な場面に限定
4. **フォールバックで保険**: プライマリが Cost Low モデルでも、フォールバックに Reasoning S 級モデルを含めて品質保証

### Provider Availability Assessment

新しいフォーメーション作成時に確認する事項:

1. どのプロバイダーの API/サブスクリプションが有効か
2. 各プロバイダーの rate limit / concurrency limit
3. 無料枠 (`*-free`) モデルの利用可否
4. マルチモーダル対応モデルの有無

## Formation Creation Checklist

### Pre-Creation

- [ ] 利用可能プロバイダーの特定
- [ ] フォーメーション名の決定 (プロバイダートークン `-` 連結)
- [ ] 既存の類似フォーメーションをテンプレートとして選択

### Agent Assignment

- [ ] Stable Slots (prometheus, momus, hephaestus) に Reasoning S 級の最上位モデルを設定
- [ ] Utility Agents (librarian, explore) に要件を満たす Cost Low モデルを設定
- [ ] Orchestrators (sisyphus, atlas) に Instruct High+ + Reasoning A+ のモデルを設定（Claude-like 優先）
- [ ] Intelligence-sensitive (oracle, metis) に Reasoning S 級モデルを設定
- [ ] multimodal-looker に Multimodal Yes（= looker として実用可能）かつ Reasoning 最高のモデルを設定
- [ ] ZAI 含む場合は sisyphus-junior を追加

### Category Assignment

- [ ] review に Reasoning S 級かつ Instruct High+ の最上位モデルを設定
- [ ] ultrabrain, deep に Reasoning S 以上のモデルを設定
- [ ] visual-engineering に Multimodal Yes かつデザイン判断の強いモデルを設定
- [ ] unspecified-high に Reasoning S- 以上のモデルを設定
- [ ] quick, unspecified-low, writing, research, refactor にスロット要件を満たす Cost Low-Med モデルを設定

### Validation

- [ ] 全 Stable Slots が正しいか確認
- [ ] フォールバックチェーンに Reasoning S 級モデルが含まれているか確認
- [ ] sisyphus, prometheus, hephaestus の fallback が S 級以上のモデルのみで構成されているか確認（低tier モデル混入禁止）
- [ ] atlas に fallback が指定されていないことを確認
- [ ] variant が適切か確認 (xhigh / medium / max)
- [ ] prompt_append が全エージェント・カテゴリに設定されているか確認
- [ ] Structural Constants が含まれているか確認
- [ ] `omo-profile show <name>` で表示確認

## Existing Formation Patterns

### Agent Model Assignment Summary

| Agent | OpenAI-only | +Copilot | +OpenCode | +ZAI | +Kimi |
|-------|------------|----------|-----------|------|-------|
| sisyphus | gpt-5.4 | gpt-5.4 | mimo-v2-pro | glm-5-turbo | gpt-5.4 |
| hephaestus | codex | codex | codex | codex | codex |
| oracle | codex | codex | codex | gpt-5.4 | codex |
| librarian | 5.4-mini | sonnet-4.6 | mimo-v2-pro | codex-spark | 5.4-mini |
| explore | 5.4-mini | sonnet-4.6 | mimo-v2-pro | glm-5-turbo | 5.4-mini |
| prometheus | gpt-5.4 | gpt-5.4 | gpt-5.4 | gpt-5.4 | gpt-5.4 |
| momus | codex | codex | codex | codex | codex |

### Category Model Assignment Summary

| Category | OpenAI-only | +Copilot | +OpenCode | +ZAI | +Kimi |
|----------|------------|----------|-----------|------|-------|
| review | codex | codex | codex | codex | codex |
| ultrabrain | gpt-5.4 | gpt-5.4 | gpt-5.4 | codex | gpt-5.4 |
| deep | gpt-5.4 | gpt-5.4 | gpt-5.4 | codex | gpt-5.4 |
| quick | spark | spark | spark | glm-5-turbo | k2p5 |
| unspecified-low | spark | sonnet-4.6 | spark | glm-5-turbo | k2p5 |
| unspecified-high | gpt-5.4 | opus-4.6 | gpt-5.4 | codex | gpt-5.4 |
| writing | 5.4-mini | sonnet-4.6 | 5.4-mini | glm-5 | k2p5 |

## References

- [Agent-Model Matching Guide](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/guide/agent-model-matching.md) -- oh-my-openagent 公式のマッチングガイド
- `formations/` -- 既存フォーメーションの source of truth
- `bin/omo-profile` -- プロファイル切り替えメカニズム
- `AGENTS.md` -- リポジトリ全体の方針
