---
name: expand-capability
description: 対応表（`docs/device/capabilities/`）の「できそう」な端末機能を priority 順に自動で消化する自律ループ。issue ツリー起票（1 レイヤ = 1 子 issue = 1 PR、約 2h）→ implement-issue-tree で実装 → PR 仕上げ → マージ → 次の機能、を指定件数ぶん回す。「端末機能を進めて」「対応表を回して」「次の 3 件だけやって」「tts を実装して」で使用（件数を省くと 5 件）。実装そのものは implement-issue-tree へ委譲する。
model: opus
user-invocable: true
---

# expand-capability

端末機能の対応表を「できそう」から「できている」へ上げるループを、**人間の起動 1 回で指定件数ぶん自律的に**回します。

対象の選定・並列度の判断・マージまでを自動で行い、**止まる条件に当たったときだけ人間へ戻します**。

**このリポジトリ専用のローカル skill です。** upstream 由来ではないため `skills-lock.json` には登録しません
（`sync-skills-lock` の対象外）。

## 前提

- SSOT は `docs/device/capabilities/<id>.json`（1 機能 1 ファイル）。`_meta.json` は共通定義
- `docs/device/capabilities.md` と `capabilities.html` は生成物で、**git に入れない**（並列の PR どうしの競合を避けるため）。
  見るときは `node scripts/device/build-capabilities.mjs` で手元に生成する。CI は `--check` で SSOT を検査する
- 機能ごとの実装 issue は親なしで置く（目印 `<!-- capability: <id> -->` で探す）。**1 機能 = 1 issue ツリー**（親 = 機能、子 = レイヤ）で、
  **1 子 issue = 1 PR ≈ 2h** を目安に切る（Phase 10 の #827 配下 #828〜#832 が前例）
- 着手順は各機能ファイルの `priority`（昇順）。**`priority` が無い機能は後回し判断済みで候補外**
- `bundle` は橋渡し経路の束（下敷きの提示に使う）。`_meta.json` の `bundleLabels` が取り得る値
- `order`（表示順）/ `priority`（着手順）/ `bundle`（束）はいずれも計画用メタデータで、生成物へは出さない
- 起動前に `caffeinate -dims -t 43200` を Bash の `run_in_background` で回し、Mac のスリープを止める
  （スリープで実装 agent が "computer went to sleep" で止まり、子が `failed` になる。9 周目に 2 回）。全 run が終わったら TaskStop で止める

## 設計方針

**実装そのものをこの skill で行いません。** worktree 隔離・push 前 review・CI 監視は
`implement-issue-tree` の実績ある機構へ委譲します。この skill が担うのはその前後
（対象選定・起票・PR 仕上げ・マージ・表の更新確認）です。
並列度も implement-issue-tree に任せます（子 issue の `dependsOn` で順序が決まる）。

## 引数

| 指定 | 挙動 |
|------|------|
| なし | `priority` 昇順に **5 件**（既定） |
| 数値（例 `5`） | その件数 |
| `all` | 候補が尽きるまで |
| 機能 id（例 `tts`） | その 1 件だけ |
| 機能 id のカンマ区切り（例 `url-scheme,contacts,calendar`） | その機能だけ。3 件までは同時に回す（Step 3「機能をまたぐ並列」） |

件数指定（数値・`all`・既定）のときも、同時に回すのは 3 件までです。

## ループ構造

```text
対象を選ぶ → 起票 → implement-issue-tree → PR 仕上げ → マージ → 表の更新確認
   ↑                                                              ↓
   └────────────────── 件数に達するまで繰り返す ──────────────────┘
```

各機能について Step 1〜8 を回し、件数に達するか**止まる条件**に当たるまで続けます。
1 機能は 3〜5 本の PR になり、Step 4〜8 は **子 issue の PR ごと**に行います。
**機能は最大 3 件まで同時に回せます**（Step 3「機能をまたぐ並列」）。
終了時は「報告の形式」の節に従って一覧で報告します。

### 止まる条件

| 事象 | 挙動 |
|------|------|
| **P0・セキュリティ・設計変更を伴う指摘・fix ループが直せず残った指摘** | **止めて人間へ報告**（自己解決しない） |
| P1（上記に当たらないもの） | fix ループに任せる。直近 28 PR で codex 指摘 92 件中 78 件が P1 で、大半は自動修正で解消した（#940） |
| codex が 5 巡しても収束しない | 止める。「巡」は Step 4 でこの skill が行った push の回数（既に直っていてスレッドを resolve するだけのものは数えない）。5 回 push しても未解決スレッドが残るなら 6 回目を push せず止める。implement-issue-tree 内の fix ループは自身の上限（6 回）で止まるので別勘定 |
| CI が落ち続ける・実装が詰まる | 止める |
| 連続 2 件失敗 | 止める（implement-issue-tree の halt と同じ思想） |
| `.github/` を触る PR | **マージせず**次の機能へ進む（報告に残す） |
| 人手の確認（Mac 目視・実機）が要る | **止めない**。Step 7 の確認用 issue（Step 2 で先に起票、実装ツリーの外）に溜めて次へ |
| 兄弟 PR との競合が base 取り込みの上限（implement-issue-tree の `baseMergeCount` 3 回）に達した | 止める（以後は自動で取り込まれない。Step 4「兄弟 PR の競合」） |
| 残置 worktree の容量・ディスク空きのゲートで新規着手が止まった | Step 9 の片付けをしてから同じ `parent` で再実行する。片付けても止まるなら止める |
| 指定件数に達した / 候補が尽きた | 正常終了 |

## フロー

### Step 1: 対象を選ぶ

機能 id を渡された場合はそれを使います。指定がなければ **`priority` 昇順で未完了のもの**を取ります。

「未完了」= `possible` の OS が 1 つ以上残っている機能です。`approval`（OS ベンダーへの申請・承認が要る）
が付いたセルは数えません（`deferred`＝⏸保留、依存・提供状況の都合で止めているセルも同じ）。申請できる状態になったら、生成した `capabilities.md` の「申請待ち」節から見直して `approval` を外します（保留は「保留」節から見直して `deferred` を外す）。`priority` が無い機能は
後回し判断済み（2 OS しか揃わない・別 Extension が要る・上流待ち 等）なので候補に入れません。

```bash
python3 -c "
import json, glob
rows = []
for f in sorted(glob.glob('docs/device/capabilities/[!_]*.json')):
    d = json.load(open(f))
    if 'priority' not in d: continue
    todo = [k for k, v in d['platforms'].items() if v.get('status') == 'possible' and not v.get('approval') and not v.get('deferred')]
    if todo: rows.append((d['priority'], d['id'], d.get('bundle', '(束なし)'), todo))
for p, i, b, todo in sorted(rows):
    print(f'{p:3} {i:20} {b:18} {len(todo)} OS {todo}')
"
```

**2 周目以降は、Step 9 で保持した「見送り済み」id を候補から除きます。**
`.github/` ガード等でマージを見送った機能は main 上で `possible` のまま残るため、
除外しないと毎周回そのまま再選択されます。
またこの一覧はローカルの JSON を読むので、**Step 9 で main を取り込んだ後**に実行します。

後回しにした機能へ着手したくなった場合は、**先に `priority` を付ける**こと
（その判断自体が着手順の変更なので、対応表に残す）。

### Step 2: issue ツリーを起票する

**`priority` が付いている機能は着手順が承認済み**なので、個別の承認は取らずに起票します
（`priority` を付ける行為そのものが着手の承認にあたる）。
候補外（`priority` 無し）の機能へ着手する場合のみ、ユーザーへ確認します。

**親 = 機能 issue、子 = レイヤ issue** の 2 階層で起票し、`sub_issues` API で紐付けます。

**親（機能 issue）は先に起票済みのことがあります。** 本文に `<!-- capability: <id> -->` を持つ
親 issue があれば、新しく作らずにその本文を下記「親 issue に含めるもの」で書き足し、
子だけを起票して紐付けます。親は他の issue の子にしません。2 件以上見つかったら取り違えの恐れがあるので止めて人間へ戻します。
無ければ、タイトル `feat(device): <機能名> を使えるようにする（<id>）`（末尾の `（<id>）` で下の検索が引く）、
本文先頭に `<!-- capability: <id> -->`、続けて「親 issue に含めるもの」を書いて、親なしで起票します。

```bash
# タイトル末尾の（<id>）で候補を引き、本文の目印で完全一致を確かめる（無ければ空）
gh issue list --state open --search "${ID} in:title" --limit 30 --json number,body \
  | jq -r --arg m "<!-- capability: ${ID} -->" '.[]|select((.body // "")|contains($m))|.number'
```

5 OS を 1 PR に詰めると diff が 20 ファイル超になり codex の指摘が積まれる（#860 は 23 ファイル・5 件）ため、
**1 子 issue = 1 PR ≈ 2h** の粒度で切ります。

既定の分割（`possible` でない OS と、`approval` 付きの申請待ちセル・`deferred` 付きの保留セルは含めない）:

| 子 | 中身 | 担当 builder | JSON の更新 | 依存 |
|----|------|-------------|------------|------|
| (a) コア + デスクトップ | `fandhe-device` の trait + デスクトップ実装 + 型サンプル画面（画面レジストリ登録）+ **失敗系テスト**（Mac 目視とキャプチャは Step 7 の確認用 issue） | core-builder | macos / windows → `done` | — |
| (b) モバイル | iOS（ObjC + `extern "C"`）と Android（JNI）の橋渡し | platform-builder | ios / android → `done` | `dependsOn: (a)` |
| (c) Web | `fandhe-web-dom` の配線 | web-builder | web → `done` | `dependsOn: (a)` |

(c) は **JS API 1 つを呼ぶだけで済む**機能（例: `navigator.clipboard`）なら (a) へ併合してよい。
(b) は**既定で iOS と Android に分けます**（PR が小さいほど codex の往復が減る。7 周目は 3 機能とも分けて
iOS / Android とも 1 PR 3〜4h に収まった）。両方とも数行で済む機能だけ 1 本にまとめます。
Windows がプロセス間転送・レジストリ等で 2h を明らかに超える場合は (a) から分けます。
判断はここで行い、子 issue の本文に「(c) を (a) へ併合」等と残します。

親 issue に含めるもの:

- 対象 JSON の現状（各 OS の `status` / `api` / 権限・注意）を転記する
- 実装方針は `_meta.json` の `notes.implementationSteps`（5 段）を参照させ、
  **何段目を新たに踏むか**を書く（描画プリミティブ追加が不要なら明記する）
- 同じ `bundle` の実装済み機能を**下敷きとして明示**する（例: `one-shot` なら `clipboard` の
  `crates/fandhe-device/src/clipboard.rs`）。横展開であることを実装側へ伝えるため
- **人手の確認（Mac 目視・iOS / Android / Windows の実機確認）は完了条件に含めない**ことを明記する。
  Step 7 の確認用 issue（実装ツリーの外）で追う
- 契約表 `.claude/rules/device-bridge-contracts.md` の該当類型を参照させる（転記しない。
  rules は実装 agent へ自動注入される）

各子 issue に含めるもの:

- 対象レイヤと対象 OS。受け入れ条件は「**`possible` かつ `approval`・`deferred` なしだった対象 OS だけ** を `done` に更新し `impl` に
  実装パスを入れる」「他の OS のセル（申請待ちを含む）は触らない」「`--check` が通る」
- (b)(c) は本文に **`dependsOn: #<(a) の番号>`** を明記する（implement-issue-tree が読む）
- **子より先に Step 7 の確認用 issue を起票**し、その番号を下の `implStatus` と `dependsOn` に使う。
- (a) には失敗系テストを受け入れ条件に含める。macOS のセルは `detail` を「できている（Mac 目視待ち）」、
  `implStatus` を「Mac 目視待ち（#<確認用 issue>）」とし、表のセルで目視前だと分かるようにする。
  目視が済んだら確認用 issue 側で両方を書き直す
- 人手の確認が済まないと着手できない子があれば、その子の本文に `dependsOn: #<確認用 issue>` を書く
  （implement-issue-tree はツリー外の open な issue に依存する子だけを `blocked` で飛ばし、残りを進める）

**兄弟 PR が同じ行を触らないための条件**（7 周目の手作業の競合 5 件のうち 4 件は、iOS と Android の PR が
共通ファイルの `#[cfg(any(target_os = ...))]` と fallback 行をそれぞれ広げたものだった）:

- (a) は **全対象 OS の骨格を先に置く**。`fandhe-egui-proxy` の dispatch（`#[cfg(...)]` の分岐・
  `not(any(...))` の fallback 行・`device.rs` の `pub mod` 列）を全対象 OS の最終形で書き、まだ実装しない OS は
  `fandhe_device::<feature>::Unsupported...` を返す薄い関数 1 つのスタブを OS 別モジュールに置く。
  後続の子は自分の OS のモジュールだけを埋め、dispatch・fallback 行・`pub mod` 列を触らない。
  スタブは嘘の成功ではない（明示の `Unsupported` を返す）。スタブの OS は対応表で `possible` のまま、`impl` に書かない。
  スタブを置いた OS のクロスビルド（`cargo build --target ...` / `cargo ndk`）を (a) の受け入れ条件にする
  （CI が見るのはホストと Android だけで、iOS・Windows のスタブは CI で検証されない）
- (a) は **共通コア画面（`crates/fandhe-core/src/screens/`）の状態・定数・文言を全対象 OS 分**定義する。
  OS 固有の操作 UI（登録・解除ボタン等）も含む。後続の子は共通コア画面を触らない
  （url-scheme では Windows と Web が別設計の登録状態を同時に足して衝突した。#1241）
- Android の子は Java を**機能ごとのヘルパークラス**に分け、`MainActivity` への追記を呼び出し・登録の最小限に留める
  （機能をまたいだ競合は `MainActivity.java` と `android.rs` の追記だった）

子 issue の起票・既存の使い回し・親への紐付けは `scripts/device/capability-child-issues.mjs` が行います。
本文の目印 `<!-- capability-child: <id>/<層> -->` で既存を探すので、何度呼んでも同じ番号を返します。
分け方（上の判断）はスクリプトに持たせず `--layout` で渡し、対象 OS を漏れなく・重複なく覆っていなければ止まります。
上の受け入れ条件はスクリプトの本文テンプレートに入っています。**先に Step 7 の確認用 issue を作っておく**こと
（スクリプトはその番号を本文に埋める）。

```bash
node scripts/device/human-check-issue.mjs "${ID}" "${BODY}" || exit 1          # 確認用 issue（Step 7）
node scripts/device/capability-child-issues.mjs "${ID}" --layout a,b-ios,b-android,c --dry-run
node scripts/device/capability-child-issues.mjs "${ID}" --layout a,b-ios,b-android,c || exit 1
```

### Step 3: implement-issue-tree で実装する

**`parent` には、Step 2 で起票した機能 issue（親）の番号を渡します。**

```json
{
  "scriptPath": ".claude/skills/implement-issue-tree/scripts/implement-issue-tree.js",
  "args": {
    "parent": "<Step 2 で起票した機能 issue の番号>",
    "branch": "main",
    "parallel": 3,
    "externalChecks": [{ "app": "cursor", "context": "Cursor Bugbot" }],
    "autoMerge": false,
    "repo": "Fandhe-AI/fandhe-multi-platform"
  }
}
```

機能 issue は子（レイヤ）を持つので **verify-close ノード**になり、子が `implement` として走ります
（`scripts/implement-issue-tree.js` の `kind: children.length > 0 ? 'verify-close' : 'implement'`）。
順序は子 issue 本文の `dependsOn` で決まり、(a) 完了後に (b)(c) が並列に走ります。
**`parallel: 3` は固定**でよく、並列度をこの skill で判断する必要はありません。

#### 機能をまたぐ並列（最大 3 機能）

複数の機能を同時に回すときは、**機能ごとに別の implement-issue-tree を同時に起動**します（`parent` は各機能 issue）。
機能 issue は親なしなので、複数機能を束ねる親は作りません。
状態ファイル（`_/issue-trees/<parent>.json`）は `parent` ごとなので衝突しません。7 周目（url-scheme・contacts・
calendar、12 PR）は直列の見込み 12h 超に対し約 7h50m で終えました。

- **同時に回すのは 3 機能まで**
- **残置 worktree の容量上限を引数で上げる**。implement-issue-tree の容量ゲートは、兄弟 run の worktree も数えたうえで
  新規着手 1 件ごとに約 25 GiB を予約する。実消費は 1 worktree 約 5.6 GB で、既定の 50 GiB では 3 run 目が必ず止まる
  （7 周目で 1 run が空振りした）。同時に回す機能数に応じて `maxResidualWorktreeBytes` を渡す。
  run の実行中にマージする（Step 8）と worktree が 16 個前後まで増え、9 周目は 150 GiB でも予約が上限に当たった
  （実使用は 24 GiB）。
  skill 本体は変えない（共有の upstream skill のため）

  | 同時に回す機能 | `maxResidualWorktreeBytes` |
  |---------------|---------------------------|
  | 1 | 指定しない（既定 50 GiB） |
  | 2 | `107374182400`（100 GiB） |
  | 3 | `214748364800`（200 GiB） |

  ディスクの実空き容量のゲートは別にある。実空きが足りないなら上げても止まるので、`df -h .` で 200 GiB 以上空いていることを先に確かめる
- **run が終わるたびに Step 9 の手順で worktree を片付けてから**、次の run を起動する
- マージは機能をまたいで 1 本ずつ行い、そのたびに他の open な PR の `mergeable` を見る（Step 8）
- **run の終了通知を待たずにマージする**（Step 8「マージ待ち」）。run 側は外でマージされた PR を MERGED と見て
  正常に終える（already-merged 経路）ので、run の実行中にマージしてよい

複数機能を束ねる親を渡すと、implement-issue-tree はルート配下の**全子孫**を再帰取得して実装するため、
別機能の open issue もすべて巻き込まれます（`parallel` は同時実行数であって
対象件数の制限ではありません）。「1 機能を選び、その対象と方針の承認を得る」という
この skill の契約が壊れます。

`implement-issue` ではなく implement-issue-tree を使うのは、worktree 隔離・push 前 review・
CI 監視・fix ループ・`dependsOn` の順序制御を再実装せずに済むためです。

**`autoMerge: false` では全件 `blocked` で終端するのが正常です。** 失敗ではありません
（マージは Step 8 でこの skill が行う設計）。レポートの `blocked` を見て異常と判断しないでください。

(b)(c) は (a) のマージ後にしか着手できません（trait と画面が main に無いため）。run は (a) のマージを 2 通りで検知します。
(a) の PR を監視中なら監視自身が MERGED を見て (a) を完了にし（already-merged 経路）、
(a) が `blocked` で終わった後は、他の子が走っている間は折々に（最短 60 秒間隔・`PREREQ_RECHECK_MIN_MS`）、
実行中の子が 0 件になった時点でもう一度だけ、前提の完了を確かめます（`scripts/implement-issue-tree.js` の
`if (running.size === 0) break` の直前）。それでも未マージなら run は終わります。したがって:

- **(a) を run の実行中に Step 8「マージ待ち」でマージすれば、同じ run のまま (b)(c) へ進みます。**
  (b)(c) も条件を満たした PR から run の実行中にマージし、全子が run の終了前に merged になれば verify-close が
  親も閉じます（10 周目の device-info #1131 は run 1 本で親まで閉じた）。1 機能につき run は 1 回です
- (a) のマージが間に合わず、run が (a) の PR を `blocked` で返して終わったら、(a) をマージしてから
  **同じ `parent` で implement-issue-tree を再実行**します（closed の子は自動でスキップされ、(b)(c) だけが走る）

run の終了通知を待ってマージすると、(a) のマージが必ず間に合わず run が 2 回になり、先に揃った (b)(c) の PR も待たされます。

run が終わった時点で未マージの子が残っていれば（最後の PR を run の終了後にマージした等）、親は open のまま残ります。
**親は追加の run を起動せず、次の手順でこの skill が閉じます**（verify-close の中身は子の closed 確認・
完了条件のチェック・サマリーのコメント・close の gh 操作だけで、追加の run は 1 回で 20 agent 超・
100 万 token 超を使う。8 周目の実測）。

1. `gh api "repos/{owner}/{repo}/issues/${FEATURE}/sub_issues" --jq '[.[]|.state]'` で子がすべて `closed` か確かめる
   （取得に失敗したら閉じない）
2. Step 9 の手順で main を取り込んでから（取り込まないとローカルの JSON は `possible` のまま）、Step 5 の確認
   （対象 OS が `done`・`impl` あり・`--check` 通過）を行う
3. 親本文の完了条件にチェックを付け、マージ済み PR の一覧をコメントしてから `gh issue close ${FEATURE}` する

子の数が 4〜5 本（(b) を iOS / Android に分けた・Windows を分けた）でも、(a) のマージ後に残りが並列に走るので、
1 機能につき run は 1 回、(a) のマージが間に合わなければ 2 回です（競合の解消・Review の不収束で再実行した分は除く）。

**機能 id を指定されたランは、指定された機能だけ**を回します（候補一覧から足さない）。

### Step 4: PR を仕上げる

Step 4〜8 は **子 issue の PR ごと**に行います（1 機能で子の数だけ。3〜5 回）。

implement-issue-tree は CI 通過後の codex-review 指摘を残したまま終わるため、ここを引き取ります。

**CI の pass だけで判断しません。** 未解決レビュースレッドも必ず見ます。

```bash
gh pr checks <N> --json name,bucket --jq '.[]|"\(.bucket)\t\(.name)"'
```

レビュースレッドは **`hasNextPage` が false になるまで全ページ取得**します。先頭 50 件だけを見ると、
解決済みが溜まった PR で 51 件目以降の未解決を取りこぼし、「未解決 0」と誤報告します。

```bash
cursor=""
while :; do
  page=$(gh api graphql -f query='
    query($o:String!,$r:String!,$n:Int!,$c:String){repository(owner:$o,name:$r){pullRequest(number:$n){
      reviewThreads(first:100, after:$c){
        nodes{id isResolved path line comments(first:1){nodes{author{login} body}}}
        pageInfo{hasNextPage endCursor}}}}}' \
    -F o={owner} -F r={repo} -F n=<N> -F c="${cursor}") || { echo "スレッド取得に失敗"; exit 1; }
  # `echo` ではなく `printf '%s'` を使う。レビュー本文に含まれる `\n` を echo が
  # 実際の改行へ展開してしまい、JSON が壊れて jq が parse error になる。
  printf '%s' "${page}" | jq -r '.data.repository.pullRequest.reviewThreads.nodes[]|select(.isResolved==false)'
  # pageInfo はパスを明示する（`..` の再帰探索は他の箇所を拾い得るうえ、式を誤ると
  # 空文字になって「全ページ取得済み」と誤判定する）。取得・解析に失敗したら
  # 完了扱いにせず異常終了する（未解決の取りこぼしを "0 件" と誤報告しないため）。
  info=$(printf '%s' "${page}" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo
    | .hasNextPage, (.endCursor // "")') || { echo "pageInfo の解析に失敗"; exit 1; }
  has=$(printf '%s\n' "${info}" | sed -n 1p)
  cursor=$(printf '%s\n' "${info}" | sed -n 2p)
  case "${has}" in
    true)  ;;
    false) break ;;
    *)     echo "pageInfo.hasNextPage が想定外: ${has}"; exit 1 ;;
  esac
done
```

指摘は **コードで裏を取ってから** 直します。指摘の前提そのものが誤っていることがあり、
前ラウンドで既に直っていてスレッドだけが残っている場合もあります。

修正 → push → `resolveReviewThread` → CI 再待ち を、CI 全 pass かつ未解決 0 になるまで繰り返します。

**P0・セキュリティ・設計変更を伴うもの・fix ループが直せず残ったものは人間へ上げて止まります。**
それ以外の P1（修正方針が明確で設計変更を伴わないもの）は裏取りのうえ自己判断で直して構いません。

#### 兄弟 PR の競合

生成物をコミットしなくても、兄弟 PR（同じ機能の別 OS・機能をまたいだ Android 同士等）は共通ファイルで競合します。
1 本マージするたびに、残りの open な PR の `mergeable` を確かめます（`UNKNOWN` は数十秒で確定する）。

`CONFLICTING` になったら **main で手で解かず、その機能の `parent` で implement-issue-tree を再実行**します。

- 再開の条件は、状態ファイルの項目が `blocked`（または `monitoring`）で `pr` と `branch` を持っていること。
  **状態ファイルの項目とその worktree を消さずに**再実行する（消すと再開できず、実装からやり直しになる）
- 再開した監視が競合を見つけると base 取り込みを試み、解けない競合は fix 担当へ回して解消・ビルド・テスト・push まで行う。
  fix の回数（上限 6）を 1〜2 回使う
- base の取り込みは PR ごとに 3 回まで（`baseMergeCount`）。上限に達したら止まる条件に当たる
- 解消の push で codex が PR 全体を見直し、新しい指摘が出ることがある（7 周目の #1235）。fix ループがそのまま引き取る
- **同じ `parent` の run が実行中なら、終わるのを待ってから再実行する**。状態ファイル `_/issue-trees/<parent>.json` に
  多重起動の排他は無く、並行させると書き込みがぶつかる。実行中の run が競合した PR を監視していれば、その run が
  base 取り込みで解くこともある（8 周目の #1260 は待ち時間 約 2h）。待つ間は、その PR を Step 8 の待機スクリプトの
  `KNOWN_CONFLICTING` に入れて回し直す（入れないと同じ `CONFLICTING` がすぐ出て終わる。入れても、run が競合を解いて
  条件を満たせば `READY` は出る）
- **人の判断待ちで止めた子（状態 `failed`）は、再実行で実装から着手し直される**。再実行の前に、その子の本文に
  `dependsOn: #<判断を追うツリー外の open な issue>` を書いて `blocked` で飛ばさせる（本文の「実装しない」等の
  文言は Plan が命令として扱わないため保証にならない）。判断で見送ると決めたら、子は not planned で閉じ、
  後続の調査はツリー外の別 issue にする（open のままだと verify-close が親を閉じない。8 周目の #1253 → #1267）

手で解くのは、再実行が止まる条件に当たったときだけです。その場合は解消後に、対象の全ターゲットで
clippy（ホスト・`aarch64-apple-ios`・`cargo ndk`・Windows・wasm32 のうち触ったもの）と、
Java を触ったら `gradle :app:compileDebugJavaWithJavac` を通してから push します。

### Step 5: 表の更新を確認する

`no` / `n-a` の OS と `approval` 付きの申請待ちセル、`deferred` 付きの保留セルは**対象外**です（申請待ち・保留は `possible` と `approval` / `deferred` を保ったまま残す）。`done` になっているべきなのは、**その子 issue の対象 OS** だけです
（(a) なら macos / windows。(a) の PR で ios が `possible` のままなのは正常だが、(b) の PR で ios が
`possible` のままなら実装漏れ）。

マージ前に見るので、**ローカルの作業ツリーではなく PR の head** の JSON を読みます（run の実行中は
ローカルの main に PR の変更が無く、対象 OS も `possible` のままに見える）。

```bash
# PR の head を専用の ref に取る（FETCH_HEAD は複数 ref を取ると先頭の main を指すため使わない）
git fetch -q origin main "+pull/<N>/head:refs/remotes/pr/<N>" || exit 1
head=$(git rev-parse "refs/remotes/pr/<N>") || exit 1

# 各 OS の状態と impl。対象 OS が done か、それ以外が書き換わっていないかを見る
git show "${head}:docs/device/capabilities/<id>.json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for k, v in d['platforms'].items():
    print(k, v['status'], v.get('impl', '(impl なし)'))
"

# no / n-a のセルが書き換わっていないことを、main との merge-base からの差分で確認する
git diff "$(git merge-base origin/main "${head}")" "${head}" -- docs/device/capabilities/<id>.json
```

SSOT の検査（スキーマ・実装パス・Android 権限）は、CI の必須チェック「capabilities 対応表の検査」が PR の head で
`node scripts/device/build-capabilities.mjs --check` を実行しています。生成物はコミットしません。

### Step 6: キャプチャを保存する

人間が表を見るだけで「この機能で何ができるか」を掴めるようにするため、Mac の正常系を 1 枚残します。
**Mac 目視と同じときに、Step 7 の確認用 issue で撮ります**（実装の PR では撮らない。目視を待って止めないため）。
目視・キャプチャ・`implStatus` の書き直しを 1 本の小さな PR にまとめ、確認用 issue の Mac の項目に
チェックを付けます。**確認用 issue を閉じるのは、チェックリストの全 OS が済んだときだけ**です
（`dependsOn` でこの issue を待つ子は、閉じた時点で着手されるため）。

- 置き場は `docs/device/captures/<id>.png`。**幅 800px 程度**に抑える（1 枚 50〜150KB が目安。
  100 機能で 5〜15MB に収めるため）
- 型サンプルが動いている画面を撮る。`sips -Z 800 <元> --out docs/device/captures/<id>.png` で縮小できる
- `docs/device/capabilities/<id>.json` に `capture` を足す（値は `captures/<id>.png`）。
  任意フィールドなので、撮れない機能があっても検証は通る

```bash
sips -Z 800 /tmp/shot.png --out docs/device/captures/<id>.png
ls -lh docs/device/captures/<id>.png   # 50〜150KB に収まっているか
node scripts/device/build-capabilities.mjs
```

棚用 HTML にはサムネイルが出て、クリックで原寸を開けます。**画像は base64 埋め込みせず相対参照する**ため
（100 機能で HTML が 10MB を超えるため）、HTML を配る際は `captures/` ディレクトリを添えてください。
md 側はリンクになります。

### Step 7: 人手の確認を実装ツリーの外へ切り出す

**Step 2 で子 issue を起票する前に**、その機能の人手の確認を **1 機能 1 issue** で起票します
（(a) の `implStatus` と、確認待ちの子の `dependsOn` がこの番号を参照するため、先に番号を確定させる）。
親なしで起票し（`device-check-pending` ラベルでまとめる）、
**機能 issue の子にはしません**（子にすると verify-close が確認を待ち、機能のクローズが止まる）。
起票は **1 機能につき open なもの 1 件だけ**です。本文の目印 `<!-- human-check: <id> -->` で open な既存を探し、あれば使い回します
（閉じた後に対象 OS が増えたときは新しく起票する）
（Step 4〜8 は子 PR ごとに繰り返すが、そこでは確認用 issue に PR 番号を書き足すだけ）。

- タイトル: `chore(device): <機能名> の人手の確認（<id>）`、ラベル `device-check-pending`
  （ラベルはリポジトリに先に作っておく。無いと起票が失敗して止まる）
- 本文: 先頭に目印 `<!-- human-check: <id> -->`（スクリプトが足す）。対象 OS（Step 2 で `possible` かつ `approval`・`deferred` なしの OS）の分だけ
  チェックリストを持つ
  - [ ] Mac 目視（正常系・失敗系。契約表の 6 類型）とキャプチャ保存（Step 6）
  - [ ] iOS 実機 / [ ] Android 実機 / [ ] Windows 実機
- 各子の PR をマージしたら、確認用 issue に PR 番号を書き足す。(b) モバイルの PR には従来どおり
  `device-check-pending` ラベルを付ける。書き足しは `scripts/device/human-check-add-pr.mjs` で行う
  （本文を手で上書きしない。同じ PR を二度呼んでも行は増えない）

```bash
node scripts/device/human-check-add-pr.mjs "${CHECK}" "${PR}" "(b) iOS、#${CHILD}。実機で見ること" || exit 1
```

確認は `/shoot` の人間束で、open な確認用 issue（`gh issue list --label device-check-pending --state open`）を上から順にまとめて処理します。

起票・使い回し・不足したチェック項目の追記は `scripts/device/human-check-issue.mjs` が行います。何度呼んでも同じ番号を返し、
gh の取得に失敗したら起票せずに止まります。本文ファイルにはチェックリストだけを書きます（目印はスクリプトが足す）。

```bash
node scripts/device/human-check-issue.mjs "${ID}" "${BODY}" --dry-run   # 何をするかだけ見る
n=$(node scripts/device/human-check-issue.mjs "${ID}" "${BODY}") || exit 1   # 標準出力の最終行が番号
```

### Step 8: マージする

**次の 5 条件をすべて満たしたらマージします。** 満たさなければマージせず、止まる条件に従います。

| 条件 | サーバー側の強制 | 確認 |
|------|----------------|------|
| CI にブロッカーなし（fail / pending / cancel が 0 件） | ruleset（required status checks 10 件） | 下記 `checks` |
| 未解決レビュースレッド 0 | ruleset（`required_review_thread_resolution`） | Step 4 のページング手順 |
| P0・セキュリティ・設計変更を伴う指摘・fix ループで直せず残った指摘が出ていない | **なし** | Step 4 の判断 |
| **CODEOWNERS 対象パスを変更していない** | **なし** | 下記 `owned` |
| `mergeable == MERGEABLE`（main との競合なし） | なし | 同スクリプト |

条件確認は `scripts/pr/guarded-merge.sh <PR 番号>` で行います。**このスクリプトはマージを実行しません。**
`sha=... checks=... unresolved=... codeowners=... mergeable=...` を出し、条件を満たせば実行すべき
`gh pr merge <番号> -R <repo> --squash --delete-branch --match-head-commit <sha>` を最終行に出します。
すべての確認を同一 head SHA に束縛し、取得失敗は fail-closed で「条件未達」にします。手順は SKILL.md に
二重管理せず、スクリプトを SSOT とします。

マージはその `gh pr merge` を**そのまま直接打ちます**（変数展開・行継続・別オプションを混ぜない）。
`.claude/settings.json` の `PreToolUse` hook がそれを検知し、**origin/main にある** `guarded-merge.sh`
で再検証して、条件未達・`--match-head-commit` の SHA 不一致・許可外のオプション（`--admin` 等）・
`-R` の不一致は deny します。作業ツリーのスクリプトを書き換えても hook 側の判定は変わりません。

#### マージ待ち（run の終了を待たない）

run を起動したら、その run の子 issue 番号で `scripts/device/wait-pr-ready.sh` を **Bash の `run_in_background`** で回します。
子に紐づく open な PR を 60 秒ごとに `guarded-merge.sh` で確かめ、条件を満たした PR（`READY`）か main と競合した PR
（`CONFLICTING`）が出た時点で 1 行ずつ出して終わります。終わったら通知が来ます。

```bash
scripts/device/wait-pr-ready.sh 1247 1248 1249                 # 機能をまたぐときは全機能の子をまとめて渡す
KNOWN_CONFLICTING="1260" scripts/device/wait-pr-ready.sh 1247 1248 1249  # 報告済みの競合を出し直さない（Step 4）
```

- `READY` が出たら、Step 4 の判断（P0・セキュリティ・設計変更の指摘が出ていないか）と Step 5（表の更新確認）を
  済ませてから、`guarded-merge.sh <PR>` をもう一度実行し、最終行の `gh pr merge` を直接打つ。
  Step 6 のキャプチャと Step 7 の確認用 issue への追記はマージ後でよい
- `READY` 直後の `guarded-merge.sh` が一度だけ「条件未達」を返すことがある（10 周目に 3 回。数十秒後の再実行で通った）。
  数十秒おいて `guarded-merge.sh` を再実行する。続けて未達なら、出力の内訳（`checks=` 等）を見て止まる条件に従う
- `CONFLICTING` が出たら Step 4「兄弟 PR の競合」
- hook が checks の pending（Bugbot の再実行）でマージを止めたら、`gh pr checks <PR> --watch` で終わるのを待ってから
  `guarded-merge.sh` をやり直す。run の監視は Bugbot が指摘 0 件でレビューを投稿しないとき `@cursor review` で
  明示レビューを依頼するので、`READY` の後に Bugbot が走り直すことがある（9 周目に 3 回）。deny は安全側の正常動作
- 処理したら同じコマンドで回し直す。**run の終了通知では子を外さない**（run は `blocked` で終わるのが正常で、
  その時点の未マージの PR こそマージ待ちの対象）。マージ・クローズ済みの PR は open でなくなるので自然に外れる。
  子をすべて閉じたら回さない（回していれば TaskStop で止める）。競合を待っていた run が終わったら、その PR を
  `KNOWN_CONFLICTING` から外して回し直す（残すと、run の外で再び競合しても `TIMEOUT` まで気づけない）
- `TIMEOUT`（既定 4 時間）は回し直す。`GH_FAILED` は `gh auth status` を確かめてから回し直す
- **このスクリプトはマージしない。** マージを待機側のコマンドへ書かないこと（hook は Bash で直接打った `gh pr merge` しか検査しない）。
  待機のコマンド文（コメントを含む）に `gh` と `merge` の語を並べて書くと、hook がマージとみなして止める
- run の実行中に外でマージしても、run 側は MERGED を見て merged で終える。fix の push とマージがすれ違うと、
  `--delete-branch` で消えたブランチが origin に作り直されて残ることがある。Step 9 の片付けで
  `git ls-remote origin 'refs/heads/*'` を見て、マージ済み PR のブランチが残っていれば消す

マージは機能をまたいでも 1 本ずつ行います。マージで生じた残りの PR の競合は、回し直した待機スクリプトが
`CONFLICTING` で拾います（Step 4「兄弟 PR の競合」）。共通ファイルに触る範囲が狭い PR（Web・Windows 等）から
先に入れると、後続の競合が減ります。マージしたら、確認用 issue に PR 番号を書き足します（Step 7）。

#### CODEOWNERS 対象を除外する理由

`.github/CODEOWNERS` はビルド基盤・マージガードのパス（`/Dockerfile`・`/compose.yaml`・`/Makefile`・
`/.github/`・`/scripts/pr/`・`/.claude/settings.json`）を列挙しています。所有者は付けていない（パスのみ）ため、
これらのパスへの人間レビューは、サーバー側でも CODEOWNERS 経由でも要求されません。
**main の ruleset は `require_code_owner_review: false`** のため、`.github/` だけを見ると、機能実装のついでに
`Makefile` を変更した PR が人間レビューなしにマージされます。

**このガードが唯一の強制点です。** 所有者が無い現状では、サーバー側の `require_code_owner_review` も
対象パスを強制できません。多層防御の一層ではなく最後の砦なので、
**判断に必要な情報が 1 つでも取れなければマージしない**（fail-closed）を徹底します。

main の ruleset（`main-protection`・`enforcement: active`・`bypass_actors` 空）は
required status checks 10 件と `required_review_thread_resolution: true` を**サーバー側で強制**します。
したがって上 2 条件は、この skill の判定を誤っても GitHub がマージを拒否します。

**サーバーが見ていないのは残り 2 条件（P0 / P1 の判断、CODEOWNERS ガード）だけ**です。
ここは skill 側の判断が最後の砦になるため、迷ったらマージせず人間へ回します。

### Step 9: main を最新化して次の機能へ

件数に達していなければ **main を取り込んでから** Step 1 へ戻ります。

```bash
git fetch origin main && git checkout main && git merge --ff-only origin/main
```

再取得しないと、直前にマージした機能がローカルの JSON では `possible` のままに見え、
**同じ機能を重複起票します**。

あわせて、**このループで処理した機能 id を保持**します。main 再取得だけでは足りません。
`.github/` ガード等でマージを見送った機能は main 上で `possible` のまま残るため、
Step 1 が毎周回そのまま再選択してしまいます。

| 記録 | 意味 | 次周回の扱い |
|------|------|------------|
| 完了 | マージ済み | main 再取得で `possible` が消えるため自然に候補外 |
| 見送り | `.github/` ガード等でマージしなかった | **id を保持して候補から除外**し、報告に残す |
| 失敗 | 止まる条件に当たった | ループ自体を終了する |

Step 1 の候補一覧から、保持した「見送り」id を除いて次の対象を選びます。

#### 終わった run の worktree を片付ける

implement-issue-tree は、`blocked` で終わった項目の worktree を残します。この skill が外でマージして issue が
closed になると、次の run はその項目を `skipped` にして状態を更新しないため、worktree は誰も消さずに残り続けます
（7 周目は 3 run で 35 GiB を超え、容量ゲートに当たった）。**完了通知が来た run の worktree** を次の条件で消します。

- 対象は `.claude/worktrees/<その run の Run ID>-*` だけ。実行中の run・手で作った worktree は触らない
- 状態ファイルに記録された worktree で、その issue が open なら残す（再実行で監視を再開するときに使う）
- `--force` を付けない。未コミットの変更がある worktree は削除に失敗して残る
- 状態ファイルを読めない・issue の状態が取れないときは残す（取得失敗を「記録なし」や closed と取り違えない）

```bash
RUN="wf_xxxxxxxx-xxx"   # 完了通知が来た run の Run ID
# グロブを使わず find で列挙する。zsh はグロブの一致が無いと `no matches found` で止まり、
# nullglob を付けると状態ファイルのグロブまで空になって jq が標準入力を待ったまま止まる
states=$(find _/issue-trees -maxdepth 1 -type f -name '[0-9]*.json') || states=""
find .claude/worktrees -maxdepth 1 -type d -name "${RUN}-*" | while IFS= read -r w; do
  # 状態ファイルが無い・読めなければ残す（jq の失敗を「記録なし」と取り違えて消さない）
  [ -n "${states}" ] || { echo "keep ${w}（状態ファイルが無い）"; continue; }
  n=$(printf '%s\n' "${states}" | xargs jq -r --arg p "${PWD}/${w}" \
    '.items|to_entries[]|select(.value.worktree==$p)|.key') \
    || { echo "keep ${w}（状態ファイルを読めない）"; continue; }
  n=$(printf '%s\n' "${n}" | sed -n 1p)
  if [ -n "${n}" ]; then
    st=$(gh issue view "${n}" --json state --jq .state </dev/null) || { echo "keep ${w}（#${n} の状態を取れない）"; continue; }
    [ "${st}" = OPEN ] && { echo "keep ${w}（#${n} は open）"; continue; }
  fi
  git worktree remove -- "${w}" </dev/null && echo "removed ${w}"
done
du -sh .claude/worktrees
```

### Step 10: 指摘を契約表へ還流する

ループ終了時に、その周の PR に付いた codex / Bugbot の指摘を
`.claude/rules/device-bridge-contracts.md` の 8 類型へ当てはめます。

契約表に無い類型、または同じ類型が 2 機能以上で再発したものがあれば、契約表を更新する PR を出します
（`.claude/` 配下なので人間が確認してマージします）。

## 報告の形式

ループ終了時、次を一覧で出します。

```markdown
## 回した機能（N 件）

| 機能 | 子 | issue | PR | 所要 | 状態 |
|------|----|-------|----|------|------|
| tts | (a) コア+デスクトップ | #863 | #866 | 1h40m | マージ済み |
| tts | (b) モバイル | #864 | #867 | 2h10m | マージ済み |
| tts | (c) Web | #865 | #868 | 0h50m | マージ済み |
| file-picker | (a) | #869 | #870 | — | **止まった: P1 指摘 2 件** |

所要は PR の作成からマージまで（目安 2h。継続して超えるレイヤは Step 2 の分割を見直す）。

## 止まった理由

（止まった条件と、人間に判断してほしいこと）

## 人手の確認に溜まったもの（`device-check-pending` の open issue）

| 確認用 issue | 機能 | 必要な確認 |
|-------------|------|-----------|
| #870 | tts | Mac 目視・キャプチャ / iPhone・Android で音が出るか |

## 対応表の現在地

できている N / 全 M 機能（`node scripts/device/build-capabilities.mjs` の集計）

契約表への還流: あり（PR #N）/ なし
```

所要時間は次で取ります。

```bash
gh pr view <N> --json createdAt,mergedAt --jq '[.createdAt,.mergedAt]|map(fromdate)|(.[1]-.[0])/60|floor|"\(./60|floor)h\(.%60)m"'
```

## 実装時に必ず伝えること

implement-issue-tree へ渡す issue・指示には、契約表 `.claude/rules/device-bridge-contracts.md`
を参照させます（失敗系テスト・Mac 目視・FFI 対称性・文書化した契約の遵守は契約表側にある）。

## よくある失敗

| 問題 | 回避策 |
|------|--------|
| `autoMerge: false` の `blocked` を失敗と誤認する | implement-issue-tree 側はマージしない設計。マージは Step 8 でこの skill が行う |
| run の終了通知を待ってからマージする | 先に条件を満たした PR が 12〜54 分待たされ、その間に兄弟 PR との競合が増える（8 周目。#1260 は 3h48m）。Step 8「マージ待ち」で条件を満たした時点でマージする |
| CI が全 pass なのでマージ可能と判断する | 未解決レビュースレッドを GraphQL で必ず併せて確認する |
| codex の指摘を鵜呑みにして直す | 指摘の前提をコードで裏取りする。既に直っていてスレッドが残っているだけのことがある |
| 生成物（`capabilities.md` / `.html`）をコミットする | 生成物は git に入れない（`.gitignore`）。SSOT は `capabilities/<id>.json` だけ |
| 生成物をコミットしないので兄弟 PR は競合しないと考える | 共通ファイル（dispatch の cfg・`device.rs`・`android.rs`・`MainActivity.java`・共通コア画面）で競合する。(a) で骨格を先に置き（Step 2）、残った競合は再実行で解かせる（Step 4） |
| 競合した PR の状態ファイル項目を消して再実行する | 再開できず実装からやり直しになる。`pr` と `branch` を持つ項目は残す（Step 4） |
| 終わった run の worktree を放置して次の run を起動する | 容量ゲートで新規着手が止まる。Step 9 の手順で片付けてから起動する |
| 再実行が `state-unverified` で全件空振りする | 状態ファイルの項目の照合（読み込み時のハッシュ）が 2 巡しても合わなかった。7 周目は、容量ゲートで止まった run が長い note 付きで書いた未着手項目が原因だった。`cp` で控えを取り、**`pr` が 0 か無く・`branch` が空で・worktree の実体が無い項目だけ** `jq 'del(.items["<n>"])'` で消して再実行する。ファイル全体の照合が合わないと言われた場合（implement-issue-tree は `mv <file> <file>.aside` を指示する）は、退避すると open な PR を持つ項目の記録も失われるため、止めて人間へ報告する |
| 正常系だけ確認して完了にする | 失敗系（OS 機能が使えないとき）を確認しないと、嘘の成功を返す実装が通る |
| 人手の確認（Mac 目視・実機）を待って PR を止める | 完了条件に含めない。Step 7 の確認用 issue（`device-check-pending` ラベル）に溜め、まとめる前に `/shoot` で処理する。確認用 issue を機能 issue の子にしない |
| OS 単位で issue を切る | 機能単位の縦串（1 機能 = 1 issue ツリー）で切る。OS 単位だと iOS だけ進む |
| 5 OS を 1 PR に詰める | diff が 20 ファイル超になり codex 指摘が積まれる（#860 は 23 ファイル・5 件）。レイヤ（コア+デスクトップ / モバイル / Web）で子 issue に割り、1 PR ≈ 2h にする |
| (b)(c) を (a) のマージ前に走らせる | trait と画面が main に無く実装できない。run の実行中に (a) を Step 8 でマージすれば同じ run が (b)(c) へ進む。run が終わっていれば同じ `parent` で implement-issue-tree を再実行する |
| 最後の子 PR をマージして機能を完了扱いにする | 親（verify-close）は全子の完了を待つので open のまま残る。Step 3 の手順（子の closed 確認 → Step 5 の確認 → チェックとコメント → `gh issue close`）で親を閉じる |
| P0・セキュリティ・設計変更を伴う指摘を自己判断で処理する | 人間へ上げて止まる。それ以外の P1 は裏取りのうえ直してよい |
| `parent` に複数機能を束ねる親を渡す | 配下の全子孫が実装対象になる。Step 2 で起票した機能 issue（親）の番号を渡す |
| `no` / `n-a` の OS まで `done` にする | 対象は着手時に `possible` だった OS だけ。非対応 OS の実装を試みない |
| レビュースレッドを先頭 50 件だけ見る | `hasNextPage` が false になるまで全ページ取る。解決済みが溜まると未解決を取りこぼす |
| キャプチャを原寸のまま入れる | 幅 800px・50〜150KB に抑える。100 機能でリポジトリが肥大する |
| `gh pr checks` の `skipping` を失敗として扱う | `bucket` は pass / fail / pending / skipping / cancel。skipping まで数えると Cursor Bugbot が skipping の PR で件数が 0 にならず永久にマージへ到達しない。ブロッカーは fail / pending / cancel のみ |
| ガード・前提条件をそれが守るコマンドより後に書く | **skill の手順は書いた順に実行される。** ガードは前に置き、できれば分岐の中へ入れて到達不能にする。後ろに置くと、ガードが唯一の強制点（CODEOWNERS 等）の場合に素通りする |
| 1 周したら main を取り込まずに次の対象を選ぶ | 直前にマージした機能がローカルでは `possible` のままで重複起票する |
| 見送った機能を候補から外さない | CODEOWNERS ガード等で見送った機能は main 上でも `possible` のまま。id を保持して除外しないと毎周回再選択される |
| ガードが迂回できる形で書く | ガードは (a) **守る対象を漏れなく列挙する** — 設定ファイル（CODEOWNERS 等）から動的に読み、解釈できない入力は fail-closed で「対象」へ倒す。(b) **確認時点の状態に束縛する** — 確認とコマンド実行の間に状態が変わる余地を残さない（head SHA を固定し `--match-head-commit` へ渡す）。(c) **判断材料が PR 側で改変されうるなら base 側から取る** — CODEOWNERS を PR の作業ツリーから読むと、PR がそれを空にしてガードを緩められる。`git show <固定した base の SHA>:<path>` で取り、取得できなければ停止する。変更ファイル一覧も同様に固定 SHA 間の `git diff` から取る。ただし取り方も正確に: **`git diff -z --no-renames` を使い、事前に base を fetch する** — `--name-only` はシェル経由で非 ASCII パスを引用符付きで出し、リネームは移動先しか返さず、古い remote-tracking ref は merge-base をずらす（`gh pr view --json files` は cli が `files(first:100)` 固定で 101 件目以降を落とすため使わない） |
| CODEOWNERS 対象パスを触る PR を自動マージする | CODEOWNERS はサーバー側で強制されていない（ruleset の `require_code_owner_review: false`、所有者なし）。skill 側でガードし人間へ回す。対象は `.github/` だけでなく `/Dockerfile`・`/compose.yaml`・`/Makefile`・`/scripts/pr/`・`/.claude/settings.json` も含む（`.github/CODEOWNERS` から読む） |
| `priority` の無い機能へ勝手に着手する | 後回し判断済みの候補外。着手するならまず `priority` を付け、その判断を対応表に残す |
| スニペットを実行せずに SKILL.md へ載せる | 三点リーダの誤記や `echo` による JSON 破壊が混入し、読んだ側は失敗に気づけないまま先へ進む。載せる前に実データで走らせて確認する |

## 関連

- `implement-issue-tree` — 実装の実行機構（この skill が呼び出す）
- `create-issue` — issue 起票の規約
- `/shoot` — `device-check-pending` ラベルに溜めた人手の確認をまとめて処理する
