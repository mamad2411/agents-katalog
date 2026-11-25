---
name: project-layout
description: リポジトリの標準構成（README / LICENSE / CONTRIBUTING / AGENTS.md / CLAUDE.md / docs/public / docs/internal/adr / docs/internal/specs / CONTEXT.md など）と、ADR・仕様書・用語集・公開ドキュメントの置き場の決め方を定める参照用のスキル。ADR や仕様書や用語集をどこに書くか・どこから読むかを決めるとき、リポジトリの構成が標準に沿っているかを確かめるとき、「置き場」「標準構成」「project layout」に言及したときに使う。ファイルを作るのは init-project。
---

リポジトリの標準構成と、文書の置き場の決め方を定める。ファイルは作らない（作るのは `init-project`）。
機械可読の定義は同じディレクトリの [layout.json](./layout.json)。理由は dotagents の ADR 0024 / 0025。

## 置き場の決め方

文書を読む・書く前に、置き場を次の順で決める。

1. **指示ファイルの規約:** プロジェクトの `AGENTS.md`（または `CLAUDE.md`）に「置き場の規約」があれば、それに従う。
2. **既存のディレクトリ:** 無ければ、すでにあるディレクトリを使う。ADR は `docs/internal/adr/`、`docs/adr/` の順に探す。
3. **既定:** どちらも無ければ下の表の既定の置き場に、最初に書く内容ができたときに作る。

| 文書 | 既定の置き場 | 作るとき |
|---|---|---|
| ADR（MADR 形式） | `docs/internal/adr/NNNN-kebab-case-title.md` | 戻しにくい設計判断をしたとき |
| 仕様書 | `docs/internal/specs/` | 最初の仕様書を書くとき |
| 用語集 | ルートの `CONTEXT.md`（複数コンテキストならルートの `CONTEXT-MAP.md` が所在を指す） | 最初の用語が決まったとき |
| 外部に公開するドキュメントのソース | `docs/public/` | — |

空のファイルを先に作らない。

用語集が単一か複数のコンテキストかは、次の順で推定する。書式は `glossary` スキル。

- ルートに `CONTEXT-MAP.md` があれば複数コンテキスト。マップが各コンテキストの `CONTEXT.md` の所在を指す
- ルートの `CONTEXT.md` だけなら単一コンテキスト
- どちらも無ければ、最初の用語が決まったときにルートの `CONTEXT.md` を作る

複数コンテキストのとき、今の話題がどのコンテキストに属するかは推定し、分からなければ聞く。

## 標準のツリー

```
<repo>/
├── README.md / LICENSE（既定は MIT）/ CONTRIBUTING.md
├── AGENTS.md               # 「置き場の規約」節を持つ
├── CLAUDE.md               # `@AGENTS.md` の 1 行
├── .gitignore / .gitattributes / .editorconfig
├── docs/
│   ├── public/             # .gitkeep のみ。ジェネレータは前提にしない
│   └── internal/
│       └── adr/0001-record-architecture-decisions.md
└── .claude/.gitignore      # `*` / `!.gitignore`
```

要否がプロジェクトで分かれるファイル（`layout.json` の `optional`）: `SECURITY.md`、`CODE_OF_CONDUCT.md`、
`SUPPORT.md`、`CHANGELOG.md`、issue テンプレート、PR / MR テンプレート、`CODEOWNERS`。issue / PR テンプレートと
`CODEOWNERS` の置き場はホスティング（GitHub / GitLab）で変わる。Markdown の文書はどちらでもルートに置く
（GitHub は `.github/` → ルート → `docs/` しか探さないので、`docs/public/` には置かない）。

含めないもの: 言語別のファイル（`Cargo.toml` など）、CI と依存更新の設定。
