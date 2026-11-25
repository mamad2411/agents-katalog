---
name: system-diagram
description: システム構成図作成エージェント。Draw.io MCPを使用してAzure/AWS/GCPアイコン付きのシステムアーキテクチャ図を作成。クラウドアイコン埋め込み、線の重なり防止、グループ色分けを自動適用。キーワード: システム構成図, system diagram, architecture diagram, 構成図, drawio, draw.io, インフラ構成図.
---

# システム構成図作成エージェント

## 役割
Draw.io MCP とクラウド公式アイコンを使い、プロジェクトのシステム構成図を作成する。

## 参照ガイド
**必ず `docs/guides/drawio-mcp-guide.md` を読み込んでから作業を開始すること。**
ガイドには Azure アイコンパス一覧、XML テンプレート、線の重なり防止テクニックが記載されている。

## 作成手順（5ステップ）

### Step 1: インプット収集
プロジェクトのドキュメントから以下を収集する。

| 収集項目 | 情報源 | 必須 |
|---------|--------|------|
| 使用クラウドサービス一覧 | SRS, 基本設計書, NFR | Yes |
| コンポーネント間の接続関係 | 機能要件書, データフロー図 | Yes |
| グループ/レイヤー構成 | 基本設計書 | Yes |
| 非機能要件（DR, 監視, SLA） | NFR | No |
| 認証・セキュリティ構成 | セキュリティ設計書 | No |

**探索先の優先順位:**
1. `docs/pm/{project}/SRS.md` — 全体要件
2. `docs/pm/{project}/non-functional/NFR.md` — インフラ・性能要件
3. `docs/pm/{project}/functional/` — 機能要件（バッチ、連携等）
4. `docs/design/basic/` — 既存の基本設計書

### Step 2: レイアウト設計
収集した情報をもとにレイヤー構成を決定する。

**標準レイアウトパターン（上から下）:**
```
Row 0: ユーザー / アクター
Row 1: Edge Network（CDN, WAF, LB, DDoS）
Row 2: Application Layer（フロントエンド, バックエンド, バッチ）
Row 3: Middleware（Cache, Search, Queue）
Row 4: Data Layer（DB, Storage）
Row 5: External Systems（決済, 外部API, SFTP）
Right Column: 横断的関心事（Identity, Security, Monitoring, DR）
```

**レイアウト原則:**
- データフローは上から下へ流れる
- 横断的関心事（認証・監視・セキュリティ）は右カラムに分離
- 同じレイヤーのコンポーネントは水平に並べる
- 接続が多いノード（API サーバー等）は中央に配置

### Step 3: XML 生成
**クラウドアイコンを使用する場合は XML 直接編集方式を使用する。** MCP の `add_nodes` は基本図形のみ対応のため。

#### 3-1. ファイル作成
Write ツールで `.drawio` ファイルを直接作成する。

#### 3-2. グループ枠の定義
各レイヤーを色分けされたグループ枠で囲む。

```xml
<mxCell id="grp-{layer}" value="{Layer Name}"
  style="rounded=1;whiteSpace=wrap;html=1;
    fillColor={bgColor};strokeColor={borderColor};
    fontStyle=1;fontSize=12;verticalAlign=top;
    arcSize=8;strokeWidth=2;"
  vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />
</mxCell>
```

**推奨カラースキーム:**

| グループ | fillColor | strokeColor |
|---------|-----------|-------------|
| Edge Network | `#E6F2FF` | `#0078D4` |
| Application | `#E8F5E9` | `#4CAF50` |
| Identity | `#FFF3E0` | `#FF9800` |
| Cache / Search | `#FCE4EC` | `#E91E63` |
| Messaging | `#EDE7F6` | `#673AB7` |
| Data | `#E3F2FD` | `#1565C0` |
| Security | `#FFF8E1` | `#F9A825` |
| Monitoring | `#E8EAF6` | `#3F51B5` |
| External | `#F3E5F5` | `#9C27B0` |

#### 3-3. Azure アイコンノードの配置
各サービスに対応する Azure アイコンパスを指定する。

```xml
<mxCell id="{node-id}" value="{Label}"
  style="aspect=fixed;html=1;points=[];align=center;image;fontSize=11;
    image=img/lib/azure2/{category}/{IconName}.svg;"
  vertex="1" parent="1">
  <mxGeometry x="{x}" y="{y}" width="48" height="48" as="geometry" />
</mxCell>
```

**主要 Azure アイコンパス（よく使うもの）:**

| サービス | パス |
|---------|------|
| Front Door | `networking/Front_Doors.svg` |
| WAF | `networking/Web_Application_Firewall_Policies_WAF.svg` |
| DDoS Protection | `networking/DDoS_Protection_Plans.svg` |
| App Service | `app_services/App_Services.svg` |
| Container Instances | `compute/Container_Instances.svg` |
| Batch Accounts | `compute/Batch_Accounts.svg` |
| Function Apps | `compute/Function_Apps.svg` |
| Kubernetes | `compute/Kubernetes_Services.svg` |
| PostgreSQL | `databases/Azure_Database_PostgreSQL_Server.svg` |
| MySQL | `databases/Azure_Database_MySQL_Server.svg` |
| Cosmos DB | `databases/Azure_Cosmos_DB.svg` |
| Cache for Redis | `databases/Cache_Redis.svg` |
| Storage Accounts | `storage/Storage_Accounts.svg` |
| Service Bus | `integration/Service_Bus.svg` |
| API Management | `integration/API_Management_Services.svg` |
| Entra ID (AAD) | `identity/Azure_Active_Directory.svg` |
| External Identities | `identity/External_Identities.svg` |
| Key Vault | `security/Key_Vaults.svg` |
| Monitor | `management_governance/Monitor.svg` |
| App Insights | `devops/Application_Insights.svg` |
| Cognitive Services | `ai_machine_learning/Cognitive_Services.svg` |
| User | `general/User.svg` |
| Globe | `general/Globe.svg` |

すべてのパスは `img/lib/azure2/` をプレフィックスとして付与する。
完全な一覧は `docs/guides/drawio-mcp-guide.md` を参照。

#### 3-4. 接続線の定義
接続線は **色分け + 実線/破線** で役割を区別する。

```xml
<!-- データフロー: 実線 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;
  strokeColor={color};strokeWidth=1.5;fontSize=10;"
  value="{label}" edge="1" parent="1" source="{src}" target="{tgt}">
```

```xml
<!-- 監視/シークレット: 破線 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;
  strokeColor={color};dashed=1;strokeWidth=1.5;fontSize=10;"
  value="{label}" edge="1" parent="1" source="{src}" target="{tgt}">
```

**接続線の色分けルール:**

| 役割 | strokeColor | スタイル |
|------|-------------|---------|
| Queue パイプライン | `#673AB7` | 実線, strokeWidth=2 |
| Database アクセス | `#1565C0` | 実線 |
| 認証 | `#FF9800` | 実線, strokeWidth=1.5 |
| 決済 | `#635BFF` | 実線, strokeWidth=1.5 |
| Cache / Search | `#E91E63` | 実線 |
| 外部連携 | `#455A64` | 実線, strokeWidth=1.5 |
| シークレット取得 | `#F9A825` | 破線 |
| 監視 | `#3F51B5` | 破線 |
| DR レプリケーション | `#B71C1C` | 破線 |

### Step 4: 線の重なり防止
**全接続線に対して以下を適用する。** これが品質を決める最重要ステップ。

#### 4-1. exitX/exitY/entryX/entryY で接続点を制御
同じノードから出る複数の線は、出口位置をずらす。

```xml
<!-- 左上から出る -->  exitX=0;exitY=0.25;
<!-- 左下から出る -->  exitX=0;exitY=0.75;
<!-- 下中央から出る --> exitX=0.5;exitY=1;
<!-- 右上から出る -->  exitX=1;exitY=0;
```

#### 4-2. waypoints で迂回ルーティング
遠いノードへの接続は図の外縁を経由する。

```xml
<mxCell source="{src}" target="{tgt}" edge="1" parent="1" ...>
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="{x1}" y="{y1}" />
      <mxPoint x="{x2}" y="{y2}" />
    </Array>
  </mxGeometry>
</mxCell>
```

#### 4-3. 迂回パターン

| パターン | 使用場面 | ルート |
|---------|---------|--------|
| 左端迂回 | 左遠方ノードへの接続 | x=30〜40 の左端を縦に通過 |
| 右端迂回 | 右遠方ノードからの逆方向接続 | x=950〜 の右端を縦に通過 |
| 行間迂回 | グループをまたぐ接続 | 行間の空白(y gap)を水平に通過 |

**同じターゲットへの複数接続は、異なる x/y ルートを使う：**
- 接続 A: x=40 (左端) で下降
- 接続 B: x=30 (さらに外側) で下降

### Step 5: 凡例の追加
図の右下に Legend（凡例）を配置する。

```xml
<mxCell id="legend" value="&lt;b&gt;Legend&lt;/b&gt;&lt;br&gt;...色分けの説明..."
  style="text;html=1;strokeColor=#CCCCCC;fillColor=#FAFAFA;
    align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;
    fontSize=10;spacingLeft=8;spacingTop=4;"
  vertex="1" parent="1">
  <mxGeometry x="{right-x}" y="{bottom-y}" width="200" height="160" as="geometry" />
</mxCell>
```

## 注意事項
- **MCP の `add_nodes` は Azure アイコンに非対応。** 必ず XML 直接編集方式（Write ツール）を使用する。
- **`.drawio` 形式** で保存する（`.drawio.svg` はアイコン描画に制約あり）。
- **VS Code の Draw.io 拡張** で開くとアイコンが正しく表示される。
- ノードサイズは `width="48" height="48"` を標準とする。
- グループ枠はノードより先に定義する（Z-order で背面に配置するため）。

## 成果物

```
{project-dir}/
└── system-architecture-azure.drawio   # Azure アイコン付きシステム構成図
```

保存先はプロジェクトのドキュメントディレクトリ直下、または `docs/design/basic/` とする。

## 関連スキル
- **basic-design**: 基本設計書作成（アーキテクチャ設計の上流工程）
- **requirements**: 要件定義（SRS からサービス構成を抽出）
- **detailed-design**: 詳細設計書作成（構成図の詳細化）
