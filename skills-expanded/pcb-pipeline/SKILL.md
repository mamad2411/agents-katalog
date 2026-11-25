---
name: pcb-pipeline
description: Design a printed circuit board end to end - circuit description (atopile .ato), part selection, placement, KiCad layout, Freerouting autorouting, DRC, gerbers, BOM and pick-and-place for a PCB fab such as JLCPCB. Works for any copper layer count. Use when asked to design, lay out, route, check or order a circuit board, when working with .ato / .kicad_pcb / .dsn / .ses files, when running ato build / freerouting / kicad-cli, or when preparing manufacturing and assembly files.
metadata:
  version: "2.0.0"
---

# 回路から基板を作る

回路を書き、部品選定と ERC を atopile に、配線を Freerouting に、DRC と出力を
KiCad に任せて、製造業者への発注ファイルまで持っていくための手順書。
電源、アナログ、マイコン周りなど回路の種類と、2 層・4 層・6 層などの層数を問わない。

このパイプラインは道具どうしの相性が悪い箇所が多い。**知らずに踏むと必ず時間を
失う落とし穴**を先に読むこと。

## 向く基板と向かない基板

向く: 部品数 〜150 程度、0.5mm ピッチまでの表面実装、信号が数十 MHz 以下、
電源・アナログ・マイコン周り・センサ。電源段や微小信号のように形が効く所は
手で決めた固定配線とベタで押さえ、残りをルータに任せる。

向かない部分があるときは、**その部分だけ手で決めて固定し、残りを自動にする**。
決め方は毎回調べる (→「回路の種類ごとの知見」)。

| 向かないもの | 理由 | どうするか |
| --- | --- | --- |
| 差動ペア、インピーダンス制御 (USB 2.0 HS 以上、Ethernet、LVDS) | Freerouting は等長・結合・インピーダンスを見ない | 業者のスタックアップで線幅・間隔を計算し、固定配線にする |
| BGA | ファンアウトとエスケープを解けない | KiCad で手配線するか、この手順を使わない |
| 高電圧 (商用電源、数百 V) | 沿面・空間距離をルータは知らない | 規格の距離をネットクラスと禁止領域 (スリット) で与える |
| RF 整合、アンテナ | 形そのものが回路 | モジュールを使い、メーカーの推奨レイアウトを固定配線・禁止領域で写す |

## 工程は 3 段

```
前段 (回路と部品)     ato build → 部品と BOM の確認
配置と配線 (KiCad)    配置 → pre → 配線前 DRC → 剥がす → DSN → Freerouting → SES → post
                     → 部品番号 → DRC
製造 (業者ごと)       製造能力の確認 → ガーバー → BOM と実装座標 → 発注前の確認
```

段の間で受け渡すのは、**ネットの載った .kicad_pcb** と **型番の入った BOM** だけ。
前段を atopile 以外 (KiCad の回路図、SKiDL など) に替えても、この 2 つを作れれば
後ろの段はそのまま使える。atopile 固有なのは、部品を `atopile_address` (インスタンス名)
で引くところで、無ければ部品番号で引く。前段を替えるときは、その道具の版と癖を
調べてから始める。

順番には理由がある。

- **設計規則は配線の前**。既定のままだと電源も信号も 0.2mm で引かれる。
  ネットクラスを設定してから DSN を出す。→ `references/design-rules.md`
- **大事な線は先に手で決めてロックする**。ロックしない既存配線はルータが引き直す。
  固定配線は KiCad で引くのではなく設定ファイル (`board/finish.py`) に書く。
  pre は毎回それを消して引き直す。→ `references/finish-config.md`
- **配線禁止領域は配線の前**。アンテナの下、ベタの上、ケルビン線の間など。
- **引き直す前に剥がす**。前回の配線とベタが残っていると、ルータはそれを
  既存配線と面として受け取り、接続を諦める。
- **信号層のベタは配線の後、使う層すべてに**。先に埋めると信号の通り道が無くなる。
  片面だけだと反対の層の切れ端が届かず DRC が未接続にする。内層の面は配線の前
  (電源層にしておけばルータは信号を引かない)。
- **部品番号はベタの後**。配線とベタには触らず、シルクだけを動かす。
- **DRC は必ず最後**。`--exit-code-violations` を付けて、違反で止まるようにする。
  ルータのクリアランス違反 0 は配線完了を意味しない。未接続 0 で初めて完了。

`examples/Makefile` が全体を繋いだひな形。プロジェクトの直下に写して、
`SKILL ?=` にこの SKILL.md があるディレクトリの絶対パスを書き、`FAB` を合わせる。
場所は入れ方とエージェントで変わる (`~/.claude/skills/`, `~/.agents/skills/`,
プラグインのキャッシュの下など) ので、自分がこのファイルを読んだ場所を書く。
変数のまま (`${CLAUDE_SKILL_DIR}` など) ではなく、展開した絶対パスにする。

## 基板ごとに書くもの

スクリプトは基板に依存しない。基板ごとに書くのは次の 3 つだけ。

| ファイル | 中身 | 見本 |
| --- | --- | --- |
| `board/placement_<build>.txt` | 部品の座標。インスタンス名で書く | `references/finish-config.md` |
| `board/finish.py` | 層数、内層の面、取付穴、配線前の銅、固定配線、禁止領域、ファンアウト、ベタ、ステッチング | `examples/dcdc-4layer/finish.py` (4 層), `examples/electrode-2layer/finish.py` (2 層・特殊な銅) |
| 回路図スクリプト (任意) | 記号の配置。接続はネット表と照合される | `examples/dcdc-4layer/draw_schematic.py` |

`finish.py` は Python の設定ファイルで、表で書けない形は `pre_hook` / `post_hook`
に `scripts/pcbkit.py` の部品を使って書く。層は `"F.Cu"`, `"In1.Cu"` のように名前で
指定するので、層数を変えても書き方は同じ。

## 道具と版

| 段 | 役割 | 実体 | 注意 |
| --- | --- | --- | --- |
| 前段 | 回路記述・部品選定 | atopile 0.15.8 | CLI 最終版。0.16 以降はウェブアプリで、この版は今後更新されない |
| 配置と配線 | 基板・DRC・ガーバー | KiCad 10 | `kicad-cli` に DSN 書き出しは無い |
| 配置と配線 | DSN / SES、基板の編集 | KiCad 同梱 Python の `pcbnew` | macOS は Python 3.9。新しい構文は使えない |
| 配置と配線 | 自動配線 | Freerouting 2.1.0 | 2.4 は Java 25 必須 |

macOS と Linux で動く。場所が既定と違えば環境変数で差し替える。

| 変数 | 既定 |
| --- | --- |
| `KICAD_PYTHON` | macOS は KiCad.app 同梱、Linux は `import pcbnew` できる python3 |
| `KICAD_APP` | `/Applications/KiCad/KiCad.app` (macOS) |
| `KICAD_FOOTPRINT_DIR` | KiCad.app 内、`/usr/share/kicad/footprints` など |
| `FREEROUTING_JAR` | `~/tools/freerouting-2.1.0.jar` |

```sh
uv tool install "atopile==0.15.8"
curl -sL -o ~/tools/freerouting-2.1.0.jar \
  https://github.com/freerouting/freerouting/releases/download/v2.1.0/freerouting-2.1.0.jar
ato auth login
```

`ato auth login` はブラウザが開く対話式で自動化できない。人に頼む。
これを済ませるまで部品選定は `Sign-in required` で止まる。

## 先に知るべき落とし穴

**KiCad 10 が書いた基板を atopile は読めない**。ネット番号が廃止されて参照が
`(net "名前")` だけになり、ビア保護設定の書式も変わった。`ato build` の前に
毎回 `scripts/sanitize_pcb.py` を通す。文脈ごとに綴りが違うので正規表現では直せない。

**atopile はフットプリントを書き直す**。カスタムパッドのプリミティブは消える。
円環電極のような特殊な銅はフットプリントに置けない。配線後にゾーンとして
基板に足す (`post_hook`)。→ `examples/electrode-2layer/finish.py`

**部品構成を変えたらレイアウトを作り直す**。atopile が部品を差し替えると、
差し替わった部品のネットが基板に載らないことがある。黙って未接続になるので
気づきにくい。部品を変えたらレイアウトを捨てて再生成し、配置し直す (`make fresh`)。
作り直すと部品番号が振り直されるので、**配置表は部品番号ではなく atopile の
インスタンス名で書く**。番号で書くと別の部品が置かれ、DRC は通ってしまう。

**`.package` は効かない**。受動部品のサイズ指定は選定側が無視する。0402 と
書いて 1206 が来る。値だけ書くと 2W のリード抵抗まで来る。受動部品もすべて
`lcsc_id` で型番を指定し、ビルド後に BOM のフットプリント列を見る。

**atopile は同じ部品のパッドに同じ uuid を付ける**。KiCad の DRC が違反の相手を
別の部品として報告する。`scripts/dedupe_uuids.py` を通す (`make build` と pre が流す)。

**EasyEDA のフットプリントは 3D モデルと実装属性が壊れていることがある**。
モデルのオフセットが数 mm ずれて部品が隣の部品の下に潜って見える、SMD なのに
属性が through_hole、など。DRC は通る。`scripts/check_models.py` で出し、
フットプリントを直すのではなく別の型番の部品に替える (取り込み直すと戻る)。

**LED とダイオードは型から選定できない**。`is_pickable` トレイトを持っていない。
部品なしで黙ってビルドが通る。`ato create part -s <LCSC番号>` で実体部品を作る。

**pcbnew を編集した後の参照は死ぬ**。ゾーンを 1 つ消しただけで、その後の
`GetDrawings()` が例外になり、進めるとセグメンテーション違反で落ちる。
`scripts/pcbkit.py` の `Ctx` は編集前に数値を読んで控える作りになっている。
フックを書くときもこれに従う。→ `references/pcbnew.md`

**Freerouting のパス上限は効かず、SES は完走したときしか出ない**。未配線が一定数で
止まったら構造的に引けない所がある。配線前に DRC を回して潰す。ほかにも、
信号層のベタを障害物にしない、表の禁止領域の下の裏面配線を SES から落とす、
重複片や行き止まりを残す、などの癖がある。post が掃除する。→ `references/routing.md`

**ネットクラスのクリアランスを部品のピン間隔より大きくしない**。0.5mm ピッチの
IC ならパッド間は 0.22mm。これを超えるとそのピンから線が出せず、ルータは黙って諦める。

**内層を面にする多層基板では、面のネットのパッドをルータに任せない**。パッドごとに
ビアを打つファンアウト (`FANOUT`) を配線前に済ませる。→ `references/multilayer.md`

詳細は `references/` に分けてある。

- `references/finish-config.md` — `board/finish.py` に書けるものと、配置表の書き方
- `references/design-rules.md` — ネットクラス、線幅、Freerouting への伝わり方
- `references/atopile.md` — 構文、トレイト、部品選定、再生成の規則
- `references/pcbnew.md` — SWIG の罠、API の癖、使える断片
- `references/routing.md` — Freerouting のヘッドレス実行、配線前後の順序、2.1.0 の癖と掃除
- `references/multilayer.md` — 内層を面にする多層基板を完走させる手順
- `references/circuits/` — 回路の種類ごとの配置と配線の知見
- `references/fab/` — 製造業者に依らない確認事項と、業者ごとの知見 (JLCPCB)

## 回路の種類ごとの知見

部品の配置と配線の形は、回路の種類で決まる。書いてあるのは今のところ 2 つ。

- `references/circuits/power.md` — スイッチング電源 (ホットループ、SW ノード、ゲート、ケルビン接続)
- `references/circuits/low-current.md` — 微小電流・高インピーダンス (リーク、ガード、露出電極)

**ここに無い種類の回路を含むなら、配置を決める前に調べる**。例: USB・高速デジタル、
RF・無線モジュール、ADC の基準電圧とアナログ GND、モータ駆動、商用電源の絶縁、
水晶発振子、熱設計。調べる先は、使う IC のデータシートの "Layout guidelines" と
評価ボードのレイアウト、メーカーのアプリケーションノート、規格。調べた結果は
配置表と `finish.py` のコメントに根拠として残し、他の基板でも使える知見なら
`references/circuits/` に 1 ファイル足す。手順は `references/circuits/README.md`。

## 検証

**目で見ないと分からない失敗が多い**。各段階で確認する。

```sh
kicad-cli pcb render --side top -o out/top.png board.kicad_pcb   # 実際に画像を見る
kicad-cli pcb drc --severity-error --exit-code-violations board.kicad_pcb
```

`scripts/netlist_diagram.py` がネットと接続先の表を出す。部品が黙って未接続に
なっていないか、ここで見る。全パッドがどこかのネットに乗っているかを毎回確認する。
1 ピンだけのネットは最後に列挙されるので、意図した開放かを 1 本ずつ確かめる。

**配線の前にも DRC を回す**。部品の重なりや固定配線の位置ずれはここで出る。
配線は 1 回数分かかり、ルータはこれらを黙って「引けない」にする。

**部品どうしの干渉は DRC では見つからない**。EasyEDA 由来のフットプリントには
コートヤードが無い。`make check` (`check_overlap.py`, `check_models.py`) で出し、
3D レンダで端子台や電解コンデンサの下に部品が潜っていないかを見る。

**部品番号が部品に隠れていても DRC は黙っている**。3D レンダで全部読めるかを見る。

回路図は atopile が出さない。必要なら描いて、描いた接続をネット表と 1 ピンずつ
突き合わせて、食い違ったら描画を失敗させる。→ `scripts/schematic.py`

## 発注

業者を問わない確認事項は `references/fab/README.md`。業者ごとの知見は
`references/fab/<業者>.md` にあり、いまは `jlcpcb.md` だけ。

**業者の製造能力に収まっているかは別に確かめる**。プロジェクトの DRC が通っても、
シルク文字の高さなどは見ていない。業者の下限を書いた `.kicad_dru` を基板のコピーに
当てて DRC する (JLCPCB は `references/fab/jlcpcb-*.kicad_dru`)。

**JLCPCB 以外の業者に出すときは、発注の前に調べる**。製造能力 (線幅・間隔・ビア・
シルク)、受け付けるガーバーとドリルの形式、実装の BOM と実装座標の列名、部品の
調達方法 (業者の在庫から選ぶか、型番で調達か)。分かったら `references/fab/<業者>.md`
と `.kicad_dru` を書き、`scripts/fab_files.py` の `FABS` に書式を足す。

`make fab` が `FAB` の書式で BOM と実装座標を書く。**`make all` はこれを含まない**。
部品を変えたら流し直し、BOM の型番が `lcsc_id` と一致するかを見る。
ガーバーは製造レイヤだけで、銅層は基板の層数から決まる (`scripts/gerber_layers.py`)。

極性のある部品で、フットプリントにもデータシートにも極性の記載が無いものは
実装対象から外し、手で付ける (`HAND_SOLDER`)。実装後に気づいても直せない。
