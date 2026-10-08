# terrain-kit

three.js (WebGPU + TSL) 向けの、オープンワールド地形 + 大量植生ライブラリ。

Heightmap を基礎に、地形の同期クエリ・`meshwalk` 用の collision geometry・決定論的な草木の instancing を提供する。

## 一次資料（まずこれを読む）

| ファイル | 内容 |
|---|---|
| `docs/superpowers/specs/2026-08-21-terrain-kit-design.md` | v1 設計仕様。全 22 セクション。**設計上の疑問はここに答えがある** |
| `docs/superpowers/plans/2026-08-21-terrain-kit-core.md` | 段階1〜3 の実装計画。Task 1〜6 は TDD ステップまで詳細化済み。Task 7〜14 は見出しのみ |

spec の §22 に 10 段階の実装順序がある。段階3（`getHeight` ↔ collision geometry の一致）と段階5（demo 上を歩ける）がマイルストーン。

## 依存

- `three@0.185.1` — `three/webgpu` と `three/tsl` の sub-path export を使う
- `meshwalk@1.1.1` — `StaticBody.addFromGeometry( geometry, matrix? )` / `world.add` / `world.remove` / `world.update( dt )` / `CharacterController({ radius, height })`。TPS ヘルパー（`KeyboardControls` / `ThirdPersonCameraControls`）も同梱。`camera-controls` を依存に持つ
- **vite で `three` → `three/webgpu` を完全一致エイリアスする必要がある。** meshwalk と camera-controls は `three` をベアインポートするので、エイリアスしないと three が2コピーになり meshwalk 内の `instanceof Mesh` が黙って false になる。**文字列指定だと前方一致で `three/webgpu` 自体が `three/webgpu/webgpu` に壊れる**ので `find: /^three$/` を使う

## 実装状況

| | 状態 |
|---|---|
| 段階1〜3（`core` 全体） | ✅ 完了 |
| 段階4（three 層 / TerrainRenderer / CDLOD / demo） | ✅ 完了 |
| 段階7（TerrainMaterial）| ✅ 完了。**段階5・6 より先に前倒し**（PBR テクスチャが用意されたため） |
| 段階5（meshwalk で歩く）| ✅ **完了。マイルストーン合格** |
| 段階6（Worker）| ✅ **完了。マイルストーン合格（バイト一致）** |
| 段階8（Vegetation） | **Task 21〜25 完了。草が生えている。Task 26（Worker 化）が残り** |
| 段階9〜10 | 未着手 |

**252 テスト PASS、型エラーなし。** `npm run dev` → `http://localhost:5273/`

`src/core/` の全ファイルが実装済み: `hash` / `blueNoise` / `types` / `tileGrid` / `interpolate` / `normal` / `surfaceRule` / `providers/*` / `TileStore` / `query` / `buildTerrainGeometry` / `index`。

**段階3 のマイルストーンは合格済み** — `getHeight` と collision geometry が 128 三角形 × 5 点で `1e-5` 以内に一致する。

### 段階5 の検証結果（2つ目のマイルストーン、合格）

`player.groundHeight - query.getHeight()` を実測:

| 状態 | 差 |
|---|---|
| 静止（20.8° / 41.1° の斜面）| **0**（厳密） |
| 歩行中（150フレーム、滑りなし）| 最大 0.0251 |

歩行中の差は**測定側のフレーム内タイミング差**で、幾何のずれではない（1フレームの高さ変化が中央値 7cm なのでその範囲内）。静止時に厳密 0 なので、補間が1箇所にしか実装されていないことが実機で確認できた。

**調査中に踏んだ2つの誤り（繰り返さないこと）:**
- 「カプセル半径ぶんのオフセットでは？」と仮説を立てたが**外れ**。静止時は全傾斜で厳密 0 で、`groundHeight` は地形表面そのもの
- 44.7°（`slopeLimit` 付近）で測ると滑るため、静止待ちの間にプレイヤーが移動し、**古い座標で `getHeight` を読む**測定バグになる。同一瞬間・同一座標で読むこと

**接地は meshwalk のみが行う。`getHeight` は接地経路に一切入っていない。**

### MeshWalk collider streaming HUD 用語

demo の collider 表示は、次の意味で読むこと。

- **`pending`**: 未完了のタイル総数（待機中 + 処理中）
- **`in-flight`**: Worker で処理を開始し、まだ完了していないタイル数
- **`collider`**: MeshWalk への登録が完了したタイル数

したがって、`pending = in-flight + 待機中` であり、`collider` は `pending` に含まれない。
移動中は範囲外の collider が先に外され、新しいタイルが pending に追加されるため、
一時的に collider 数が減って pending が増えることがある。停止後も pending が減らない場合は、
`in-flight` と HUD の `collider err` を確認する。

毎フレーム呼ぶのは `player.move( velocity )` と `mwWorld.update( dt )` の2つだけで、`player.position.y` に書き込むコードは存在しない。`MeshwalkTerrainBinding` も collider を付け外しするだけ（`StaticBody.addFromGeometry` に `lod: 0` の本物の地形三角形を渡す）で、高さを書き戻さない。

したがって `groundHeight` は meshwalk 自身がカプセル vs 三角形の交差から出した値で、それが `getHeight()` と静止時に厳密一致した、というのが上のマイルストーンの意味。**同じ量を2箇所で独立に計算して一致した**（不変条件 A の検証）であって、片方がもう片方を参照しているのではない。

**スポーンと `teleport()` は `getHeight` を使う。** 一度 `maxHeight + 2` から落とす方式に変えたが、73m 上空から降ってくるのが邪魔なので戻した。

これは検証を壊さない。`player.position.y` に書き込むのは初期化と `teleport()` の瞬間だけで、**毎フレームの接地経路には入らない**（`tick` は `player.move()` と `mwWorld.update( dt )` しか呼ばない）。HUD の `delta` は独立に計算した2つの値の比較のまま。

**やってはいけないのは `tick` の中で `player.position.y = getHeight(...)` とすること。** それをやると比較する2つの量が同一実装を参照して、マイルストーンが自明な恒等式に退化する。

`groundHeightFor()` は getHeight を読む前に `heights.acquire( tx, tz )` で待つ。TerrainRenderer 経由の acquire は非同期なので、待たずに読むと null が返り、以前の `?? 0` は「高度 0 から落下」を静かに選んでいた。

実測（tick が1回も回る前）: `position.y` = `getHeight()` = -7.6143 で差は厳密 0、`isGrounded` は true、`velocity.y` は 0。

### キャラクターコントローラの確定値

| | 値 | 根拠 |
|---|---|---|
| `PLAYER_RADIUS` | 0.25 | 直径 50cm。Box3 実測で一致 |
| `PLAYER_HEIGHT` | 1.7 | **全高**（足元〜頭頂）。`_collisionDetection` の実装から確認 |
| `camera.position` の種 | `( 0, 0, 8 )` | meshwalk `5_terrain` 例と同じ距離 |

- `height` の意味: `segment = height - radius * 2` / `capsule.start = position.y + radius` なので**カプセル下端 = `position.y`（足元）**、上端 = `position.y + height`
- **移動ベクトルを自分で三角関数展開しないこと。** README の `.set( input.x, 0, - input.y ).applyAxisAngle( Y_AXIS, tps.frontAngle )` を使う。展開して符号を2箇所間違え、W/S が逆になった
- **`ThirdPersonCameraControls` の `trackObject` には `playerObject` をそのまま渡す。** `update` が `trackObject.position`（ローカル座標）を読むので、子を渡すと原点付近を追ってカメラが真上に張り付く。注視点を上げる子も不要（内部で `offset = (0, 2, 0)` が加算される）
- **`camera.position` を初期化前に設定しないと真上から見下ろす退化状態になる。** `CameraControls` は construct 時の `camera.position` から距離・角度を導出する

次の作業は**段階8 の Task 26（`vegetation` job の Worker 化）**。計画は `docs/superpowers/plans/2026-08-21-terrain-kit-vegetation.md`。

Task 26 は段階6 の harness に job 種別を1つ足すだけで、バイト一致の型は既に確立している。ただし配置には weight map / density map / profile map が必要なので、`TileMapId` を `'heights' | 'holes'` から広げるか、コピー経路として `inline` に同梱する判断が要る。

**未決の課題:**

- **密度の最終調整。** 現在 grass 最大 14.61 本/m²・中央値 3.32 本/m²。濃さは `MAX_PER_CHUNK` で調整する（下記「密度の決め方」参照）
- **`blueNoise` が species を区別しない**（spec §11.3 のとおり）。`cellSize` が同じ2種は採択が完全に入れ子になり「必ず同じ cell に同居する」。現在は 1.5 / 3 / 6 / 12 → 0.15 / 1.2 / 6 / 12 と全species で別値にして回避している。**`cellSize` を揃えないこと。** 消したければ `blueNoise( cx + ox, cz + oz )` の形で species ごとにテーブルを平行移動する（トーラスなのでスペクトルは保たれる）が、**同じ seed から別の世界になる**変更なのでアセットが焼かれる前に決めること
- **spec §7.2 の uv 定義が古い。** タイルローカルの texel 中心整合と書いてあるが、実装は world XZ 正規化（`src/nodes/terrainMaterial.ts` の `weightUv`）。**実装が権威。** 段階8 完了時に spec を直す

### 段階6 の検証結果（3つ目のマイルストーン、合格）

**不変条件 C: 複数の経路が作る geometry はバイト一致する。** in-thread / Worker+SAB / Worker+copy の3経路。

`demo` の `terrainKit.compareGeometry( tx, tz, lod )` が実機での確認手段。4タイル × LOD0〜4 = 20 通りを両経路で確認して全て `identical`。収束後の総三角形数も3経路とも **441,344** で一致した。

| 経路 | 条件 | 確認方法 |
|---|---|---|
| in-thread | `?worker=0` | `compareGeometry` は `nothing to compare` を返す |
| Worker + SAB | `crossOriginIsolated === true` | タイルの `buffer` が `SharedArrayBuffer`。`entry` チャンクの取得数 = pool size |
| Worker + copy | COEP なし（`SharedArrayBuffer` が undefined）| 同じ 20 通りが `identical` |

**バイト比較を緩めてはいけない。** node 側のテストで `u[0] ^= 1`（非正規化数 `1.4e-45`）でも4テストが落ちることを確認済み。`toBeCloseTo` に置き換えると存在理由が消える。

**`src/core/` が three を import しない制約が、ここで実利になった。** Worker チャンクは **5.7KB**（three ゼロ）。core が three に触れていたら Worker バンドルが 1MB 級になる。`npm run build:demo` で `demo/dist/assets/entry-*.js` が独立チャンクとして出ることが確認手段。

**Vite の Worker 解析はリテラル形式でないと効かない。** `new Worker( new URL( '../src/worker/entry.ts', import.meta.url ), { type: 'module' } )` の形が必須で、URL を変数に入れると解析されずビルドで壊れる（dev では動くので気付きにくい）。

**SAB は絶対にプールしない。** タイルごとに新しい `SharedArrayBuffer` を割り当てる。使い回すと、release されたバッファが in-flight のジョブが見ている view を書き換える。`TileStore` の `allocator` オプションが唯一の差し込み口で、`_place` が長さ不一致を投げる。

**メインスレッドが権威。Worker は read-only の lens しか持たない**（spec §3.2）。`TileLens` は所有権を持たず、`registerTile` / `releaseTile` の台帳だけ。

**サイレントな性能劣化に注意。** allocator を渡し忘れると `transport` は `'sab'` と報告されたまま全タイルがインライン転送になり、**出力は正しく性能だけ落ちる**。`WorkerPool.onFallback` / `inlineFallbackCount` がこれを検出するために存在する。demo の HUD の `fallbacks` が 0 でなければ配線ミス。

**踏んだ落とし穴:**
- **`settle()` を同期ループにしてはいけない。** Worker 経路の geometry は `message` イベントで届くので、1度もイベントループに戻らないループの中では**1枚も受け取れない**。同期版は 200 回まわして 36/256 枚しか揃わないのに `200` を返す（「頑張った」に見えて実際は何も進んでいない）。`await new Promise( r => setTimeout( r, 0 ) )` を挟んだら 44 回（256÷6 の理論下限）で収束した
- **`syncWorkerTiles()` は `terrain.update( camera )` の前に呼ぶ。** 後だと登録前にジョブが飛んで `runJob` が投げる
- **`.test-build/` が古いと e2e テストが嘘をつく。** `handler.ts` に1ビットの破壊を入れて再ビルドせずに `npx vitest run test/worker/e2e.test.ts` すると 3/3 PASS する。`assertBuildFresh()`（`src/core` と `src/worker` の最新 mtime を `.test-build/` と比較）が防いでいる。`tsconfig.worker.json` は `noEmitOnError: true` でないと型エラーがあっても JS を吐く
- **`TerrainRenderer` を node でテストできる。** 「three を import しているから無理」は誤り。`three/webgpu` は node で import できて、GPU デバイスは不要
- **非同期化で効いているガードは `pendingGeneration !== null` のスキップ**（`update` が pending のタイルを飛ばす）。これがタイルごとに in-flight 1件を保証するので、generation 照合は実際には発火しない。測定で確認済み: 照合だけ外すと PASS、スキップだけ外すと 2 FAIL。**pending 中の再発行を許す変更を入れたら、そこで初めて generation 照合が効き始める**


### 段階8 の検証結果（Task 21〜25。草が生えている）

計画は `docs/superpowers/plans/2026-08-21-terrain-kit-vegetation.md`。残りは Task 26（`vegetation` job の Worker 化）。

> **不変条件 D: chunk サイズを変えても、配置されるインスタンスが1本も変わらない。**

`chunkSize = tileSize` と `tileSize / 4` で同じインスタンス集合になることを検証済み。cell 座標は world 基準の絶対整数（`floor( worldX / cellSize )`）で、ハッシュも blue noise もそれだけを入力にする。chunk は「どの cell 範囲を今回作るか」の窓にすぎない。

ガードを3通りに壊して実測した:

| 壊し方 | 結果 |
|---|---|
| ハッシュに `chunk.cx` を混ぜる | 不変条件 D のテストが FAIL |
| cell 座標を chunk 相対にする | 重複を検出して FAIL |
| 半開区間を閉区間にする | **既存テストでは検出できなかった** |

**3つ目のために専用のテストがある。** cell 中心 `( cx + 0.5 ) * cellSize` は `cellSize` 2 / 6 では奇数側に来るので、16 や 64 の倍数である chunk 境界に一度も乗らない。だから閉区間に変えても通ってしまう。`chunk 境界に cell 中心が乗っても重複しない` が chunkSize 16 に対して cellSize 32 を使って中心を境界に乗せている。**`cellSize` が chunk サイズの偶数倍になる species を足したときに効くテスト。**

### 密度の決め方（1地点で判断しないこと）

`blueNoise` は一様（`P( x < t ) = t` を実測）なので **採択率 = 最終密度**そのもので、`本/m² = 最終密度 / cellSize²` と単純に決まる。

**世界データの密度は場所で大きく違う。1箇所だけ見て `cellSize` を決めると必ず外す。** 実際に両方向で間違えた:

| 場所 | DensityMap | profile |
|---|---|---|
| spawn 付近 | **0.063** | `sparse`(grass mix 0.22) / `scrub`(0.45) |
| grass レイヤーの重み ≥ 0.7 の領域（世界の 47%）| **0.962** | 平均 mix 込みで 0.753 |

spawn だけ見て「草が生えない」と判断し、次に良い場所だけ見て `cellSize` を詰めすぎた。**全 chunk の分布を測ること。**

現在の設定での実測（32m chunk、112 chunk）:

| | 値 |
|---|---|
| grass 最大 | 14.61 本/m² |
| 中央値 | 3.32 本/m² |
| 最大/中央値 | 4.4 倍 |
| `MAX_PER_CHUNK` が効いた chunk | **71 / 112** |

振れの主因は `DensityMap` の変動、次に profile の `mix`。`SurfaceRuleSet` の寄与は小さい。濃さを抑えたいときは `MAX_PER_CHUNK` を下げる（8000 で最大 7.0・中央値 0.78・総本数 126,699）。**間引きは priority 昇順の先頭 N 本を取るので chunk 内で空間的に一様**で、偏りは出ない。

### 遠方カリングは GPU にしか効かない

| | GPU | メモリ |
|---|---|---|
| 距離カリング（`maxDistance`）| 減る | **減らない** |
| 密度 LOD（`count` を減らす）| 減る | **減らない** |

`instanceMatrix` は生成時に `data.count` ぶん確保済みなので、描画を切っても減らない。**密度を上げるとメモリが先に壁になる**（18.8 本/m² で半径 192m なら 2,177k 本 = 133MB）。だから遠い chunk は**生成する本数自体**を距離の2乗で間引いている（`maxPerChunk`）。world data は priority 昇順なので、先頭 N 本を取るのは「同じ世界の間引き」で別の配置にはならない。

実測（描画距離 40 / 56 / 96 / 320m）: 確保 458,901 本 / 28MB、描画 40,606 本、描画三角形 1.98M。

**判定は chunk 単位なので、半対角ぶん外側まで描かれる。** 32m chunk なら 22.6m。実測で grass 96m 設定時の最遠が 112.5m、bush 240m 設定時が 248.9m だった（超過は全て 22.6m 以内）。インスタンス単位の判定は不変条件 B 違反なので消せない。詰めたいなら `maxDistance` を下げるか `chunkDivisor` を上げる（chunk を小さくすると超過は減るが `InstancedMesh` が増える）。

**LOD を多段にするのは、段ごとに別 geometry を用意してから。** `VegetationRenderer` は (chunk × species × lod × part) ごとに `InstancedMesh` を作り、それぞれ full count で確保するので、同じ geometry で段を増やすと同じデータのぶんだけメモリが増える（3段なら3倍）。geometry LOD は段階9。

### 実機でしか出ない不具合を3つ踏んだ

**node のテストでは原理的に捕まらない類型。** 段階8 で3つ出たので類型として残す。

1. **`count = 0` の `InstancedMesh` を可視のままにすると WebGPU が落ちる**

   ```
   GPUValidationError: Binding size for [Buffer "bindingBuffer..._UniformBuffer_..._(vertex)"] is zero.
   ```

   three の WebGPU バックエンドは**可視な** `InstancedMesh` に対して `bindGroup_object` を作るので、インスタンス 0 だとサイズ 0 の uniform binding になる。**`count` を 0 にしたら `visible = false` にする。** 0 本の species には `InstancedMesh` を作らない（永久に count 0 なので）。node では「count が 0 なら visible が false」という不変条件としてテストしてある。

2. **KTX2 の GLB は `setKTX2Loader` が無いと初期化ごと失敗する**

   ```
   THREE.GLTFLoader: setKTX2Loader must be called before loading KTX2 textures
   ```

   `assets/vegetation/tree/*_compressed.glb` は KTX2（`KHR_texture_basisu`）。basis transcoder（`basis_transcoder.js` 56KB + `.wasm` 515KB）を `/basis/` で配信して `KTX2Loader` を渡す必要がある（`vite.config.ts` のプラグインが `node_modules/three/examples/jsm/libs/basis/` から配信している）。

3. **量子化された attribute に `applyMatrix4` は成立しない**

   `poplar1_compressed.glb` は `KHR_mesh_quantization` を使っていて `position` が**正規化 `Int16Array`**（実寸はノードの scale / translation で復元）。`geometry.applyMatrix4()` は「正規化値を読む → 行列を掛ける → 正規化 Int16 の setter で書き戻す」ので **±1 にクランプされる**。13m の木が 2m の立方体に潰れ、幹と葉が重なった暗い塊になった。

   **行列を焼く前に `position` / `normal` / `tangent` を Float32 へ de-quantize する**（`partsFromScene` がやっている）。判定は「`normalized === true` または `Float32Array` でない」。

### GLB は Mesh ごとにパーツへ分ける

木は幹と葉が**別 Mesh・別マテリアル**（`poplar_foliage` / `poplar_bark`、`leaves` / `tree`）。先頭 Mesh だけ使うと**葉だけ描いて幹を捨てる**。マテリアルが別なのでマージもできない。

`VegetationLodDef.parts` に `(geometry, material)` を並べ、パーツごとに `InstancedMesh` を作って同じインスタンス変換を共有する。**パーツごとにそれぞれの `matrixWorld` を焼くこと**（先頭の行列を使い回すと幹と葉の相対位置がずれる）。

### `GLTFLoader` が node で動かないなら、純粋関数に切り出す

パーツ分割を入れた直後、`loadVegetationLods` を先頭 Mesh だけに戻しても**テストが1件も落ちなかった**。`vegetationAssets.ts` が丸ごと未テストだったのが、この不具合を通した直接の理由。

**「node で動かないからテストできない」ではなく「テストの切り方が悪い」。** Mesh 収集と行列の焼き込みを `partsFromScene( scene, label )` として `GLTFLoader` から切り離し、合成シーンで検証している。量子化 attribute も合成できるので、上記3番目もこれで守られている。

### palette PNG のインデックスを値として読まない

`vegetation-profile-map.png` は `generateAssets` が `encodeGray8` で書いた grayscale のはずが、**外部の PNG 最適化ツールがロスレスに palette（color type 3）へ変換していた**。

このファイルの palette は `index k → rgb( k, k, k )` の恒等写像なので、インデックス直読みでも**たまたま**正しい値になる。しかし palette の並び順は最適化ツールの自由（出現頻度順など）で、並べ替えられた瞬間にインデックス ≠ ID になる。**profile ID の割り当ては公開仕様**なので、それは「同じ seed から静かに別の世界が出る」事故。

`decodePng` は `PLTE` を引いて R 成分を返す。非恒等な palette で落ちるテストがある（インデックス直読みに戻すと落ちる）。

## 解決済み: blueNoise のテスト設計の落とし穴

**実装は最初から正しかった。テストが間違っていた。**（作業中に「実装が blue noise になっていない」と誤って結論した経緯があるので記録する。）

最初のテストは閾値 0.25 で採択した点の最近傍距離の分散を白色ノイズと比較していたが、**64×64 グリッドに 1024 点はグリッドが飽和する密度**で、blue noise でも最小間隔を保てず 1024 点中 559 点が隣接する。両者とも最近傍距離が 1 に張り付き、指標の判別力が消える。白色ノイズの分散が低く出るのは「一様に悪い」だけ。

実測値（トーラス距離、`平均NN / 分散 / 最小 / 隣接対`）:

| threshold | blue noise | white noise |
|---|---|---|
| 0.03 | 4.76 / 0.23 / 4.00 / **0** | 2.96 / 2.08 / 1.00 / 15 |
| 0.0625 | 3.23 / 0.20 / 2.00 / **0** | 2.00 / 0.86 / 1.00 / 82 |
| 0.125 | 2.08 / 0.17 / 1.00 / 20 | 1.52 / 0.38 / 1.00 / 243 |
| 0.25 | 1.30 / 0.145 / 1.00 / 559 | 1.20 / **0.119** / 1.00 / 699 |

**教訓: blue noise の性質は低密度側で測る。** 密度 LOD で `count` を削ったときに効くのもそちらなので、テストする密度としても正しい。現在のテストは閾値 `1/16` と `1/32` で、平均間隔・分散・隣接対数・最小間隔を検証する。距離はタイル可能性に合わせて**トーラス上**で測る（端で偽の孤立が出るため）。

なお `extreme()` に `exclude` 引数を足して「除去したクラスタ自身を最大ボイド候補から外す」修正も入れてある。これは Ulichney の手順に沿った正しい形だが、**出力は 17 桁まで変わらなかった**（安定化ループは同じ緩和パターンに収束する）。挙動を変えないので、この箇所を疑って時間を使わないこと。

## 静的アセットのパイプライン

`npx vite-node tools/generateAssets.ts` で `assets/generated/` に生成する。

| ファイル | 役割 |
|---|---|
| `heightmap.png` + `heightmap.json` | 地形の形。**16bit** グレースケール |
| `surface-weight-map-0/1.png` | Terrain Layers のブレンド。1枚 RGBA = 4 レイヤー |
| `vegetation-density-map.png` | 植生の**総量**（スカラー）。消費は段階8 |
| `vegetation-profile-map.png` | その場に生える植生の**組み合わせ**への参照（ID）。消費は段階8 |
| `maps.json` | **レイヤー順序・チャンネル割当の唯一の定義**。demo 側で二重に持たない |

高さと傾斜は「塗るときの入力」として使うが、焼いた後はただのデータで、実行時の権威はこれらのファイル。

**16bit が必須。** 量子化ステップ 0.00124m（8bit なら 0.320m で斜面に段差が見える）。ブラウザの `createImageBitmap` / canvas は 16bit PNG を 8bit に落とすので、`src/io/png.ts` に自前のエンコーダ/デコーダを持つ。`CompressionStream` が node とブラウザ両方にあるので生成器と実行時で同一実装。

`SurfaceWeightMap` の alpha も重みに使う。自前デコーダを通すので premultiply の影響を受けない。**レイヤー N は `files[N>>2]` のチャンネル `[N&3]`** で、7枚目以降も PNG を足すだけ。

**Vegetation は `type`（1点1種類）ではなく `profile`（組み合わせへの参照）**（spec §11.5b）。1点1種類だと「木の下に下草がある」が構造的に書けない。`最終密度 = DensityMap × profile.mix[species] × SurfaceRuleSet`。**profile ID の割り当ては公開仕様**で、変えると同じ seed から別の世界になる（`CHANNEL` と同じ扱い）。追加は末尾に。レシピ表は `maps.json` が唯一の定義。

## 実装中に spec を修正した2点

どちらも実装して初めて気付いた曖昧さ。spec・計画とも更新済み。

1. **`SurfaceRule` の `falloff === 0`**（spec §9.2）— smoothstep 経由だと `1 - smoothstep( max, max, max ) === 0` となり、`min` 側は含むのに `max` 側は含まない非対称になっていた。閉区間 `[min, max]` の明示判定に分岐させた。**GPU 側の TSL 実装も同じ分岐を持たせること**（`falloff` は定数なのでコンパイル時に解決される）
2. **`uv` の定義**（spec §7.2）— world XZ 正規化 → タイルローカルの texel 中心整合 `( col + 0.5 ) / ( N + 1 )`。§10.8 で weight map をタイルごとのテクスチャに決めた時点で world 基準の理由が消えていた。この定義なら `texture( weightMap, uv )` が provider のサンプル値をそのまま返す

## 実装して分かった spec の誤り（修正済み）

1. **texture array は「最適化」ではなく必須条件だった**（spec §10.5 / §17）— WebGPU は fragment ステージあたり **テクスチャ 16・サンプラー 16** が既定上限。6 レイヤー × 3 マップ = 18 binding で**検証エラーになり何も描かれない**。`requiredLimits` で上げようとすると**デバイス生成が失敗して three が WebGL にフォールバックし、WebGL2 の `MAX_TEXTURE_IMAGE_UNITS(16)` で同じ壁に当たる**（実測確認済み）。5 レイヤー以上では配列テクスチャ以外に道がない
2. **normal map を v1 に上げた** — 全レイヤーに `normal.png` があるため。triplanar normal は whiteout blend で実装。危惧していたほどの不確実性はなかった
3. **macro variation を手続き的ノイズにした** — テクスチャで持つと macro 自体が周期を持ち、対策が対策になっていなかった

## タイリング対策（spec §10.6）

「タイルに並んでいる」印象の主因は、同じ模様が出ることより**直線状に整列していること**。コストのクラスで選ぶ。

| 対策 | クラス | 6 layer でのコスト |
|---|---|---|
| domain warp | 共有 | **0 sample** |
| 手続き的 macro variation | 共有 | **0 sample** |
| 非調和 `sizeMeters` | — | **0** |
| 2スケール合成 | レイヤーごと | +18 sample |
| stochastic / hex-tile | レイヤーごと | +114 sample（非現実的）|

`color` と `normal` は**同じ warp を共有しなければならない**（別々に歪めると陰影と模様がずれる）。`triplanarBasis` に warp を持たせて構造的に保証している。

demo 左下のチェックボックスで各対策を切り替えて比較できる。

## 破ってはいけない制約

spec の Global Constraints から、特に事故りやすいもの。

- **`src/core/` は `three` を import しない。** DOM API も使わない。決定論を GPU なしに node でテストできることが、このライブラリのテスト戦略の全て
- **`CHANNEL`（`src/core/hash.ts`）は公開仕様。** 値を変えると同じ seed から別の世界が生成される。回帰テストがあるので、落ちたら値を直すのではなく変更をやめる
- **ハッシュの入力に chunk 座標を含めない。** world セル座標のみ。含めると `chunkSize` を変えた瞬間に世界中の草が別配置になる（元の設計指針ドキュメントの例からは意図的に変更している）
- **高さの補間は bilinear ではなく barycentric。** collision geometry と同じ三角形分割を使う。bilinear だとキャラクターが地面に沈む/浮く
- **テストの許容誤差を緩めて通すのは禁止。** 特に「平面を厳密に再現する」（数学的に厳密一致するので、ずれるなら式のバグ）と「白色ノイズより均一」（機能の存在理由そのもの）
- **profile ID の割り当ては公開仕様。** `assets/generated/maps.json` の `vegetationProfileMap.profiles` が唯一の定義。順序を変えない。追加は末尾のみ。**palette PNG のインデックスを ID として読まない**（`PLTE` を引く。並び順は最適化ツールの自由）
- **`count = 0` の `InstancedMesh` を可視のままにしない。** WebGPU が「サイズ 0 の uniform binding」で検証エラーを出す
- **量子化された attribute に `applyMatrix4` しない。** 正規化 Int16 に書き戻すとクランプされてジオメトリが潰れる。焼く前に Float32 へ de-quantize する
- **`InstancedMesh` の密度 LOD で `count` 以外を触らない。** `instanceMatrix` を作り直すと「残る草が動く」ので密度切替がポップする

## 不変条件 E: CPU と GPU が同じ量を別々に計算しない

段階8 で新しく前線になった箇所。**GPU（`src/nodes/`）が権威で、CPU をそれに合わせる。**

`src/core/vegetation/sampleField.ts` が CPU 側の唯一の実装。合わせている規約:

| field | GPU | CPU |
|---|---|---|
| `height` | `positionWorld.y` | `query.getHeight` |
| `slope` | `acos( clamp( normalWorld.y, -1, 1 ) )` | `query.getSlope`（`slopeFromNormalY` が同じ式）|
| `layerWeight` | `terrainMaterial` 内部。world XZ 正規化 uv | 同じ uv でバイリニア |
| `map` / `exclusion` | `texture( maps[ key ], mapUv )` | 同上 |
| `noise` | throw（v2）| **同じく throw** |

**`exclusion` のチャンネルは `'r'` 固定。** GPU が `field.kind === 'exclusion' ? 'r' : field.channel` とハードコードしている。CPU 側の `maps` を `Record<string, Rgba8Map>`（チャンネルを持たない）にして、分岐しうる形を構造的に潰してある。

**`layerWeight` だけは GPU と形が違う。真似しないこと。** `surfaceRulesNode` は `layerWeight` で throw するが、これは「マテリアル自身のレイヤー重みに使うと自己参照になる」という理由で、値の定義が無いからではない（実際の解決は `terrainMaterial` 内部）。**CPU を throw にすると「レイヤーに応じて草を生やす」という段階8 の主要ユースケースが書けなくなる。**

**`layerWeight` の uv は world XZ 正規化。** spec §7.2 はタイルローカルの texel 中心整合と書いているが、あれは §10.8 で weight map をタイルごとのテクスチャにする前提の記述。実装は world 全体の 1枚を `weightUv = vec2( ( worldX - origin.x ) / size, ( worldZ - origin.z ) / size )` で引いている（`src/nodes/terrainMaterial.ts`）。**実装が権威。** spec のこの箇所は要修正。

### 一致させられない2箇所（既知の差）

`texture()` はテクスチャ側の設定にも依存するので、バイリニアの式を合わせても残る差がある。weight map は `RepeatWrapping` / `LinearMipMapLinearFilter` / `generateMipmaps = true`。

| | GPU | CPU | 影響範囲 |
|---|---|---|---|
| wrap | `RepeatWrapping` | clamp | **world 端の半 texel だけ。** bilinear の裾が範囲外に出たとき GPU は反対側の端と混ぜる。1024² / 1024m なら約 0.5m の帯 |
| mip | 画面空間の微分で mip を選ぶ | 常に mip 0 | 遠景・浅い角度 |

**mip 側は原理的に一致させられない**（CPU の配置に画面空間の微分が存在しない）。wrap 側は weight map を `ClampToEdgeWrapping` にすれば消えるが、world 全体を1枚で覆うので実害は端の 0.5m に限られる。

「草が砂の上に生えている」を追うときは、まずこの2つでないことを確認してから式を疑う。

## 設計の中心: 不変条件 A

> 同じ量を2箇所に実装しない。

| 量 | 単一の実装 | 利用者 |
|---|---|---|
| 高さの補間 | `core/interpolate.ts` の `sampleTriangle` | `getHeight()` と collision geometry ビルダー |
| slope / height の判定 | `SurfaceRule` データ | CPU の植生配置と GPU のマテリアル |
| 法線 | `core/normal.ts` の中心差分 | geometry の `normal` 属性と `getNormal()` |

**`Task 4` の `sampleTriangle` が最重要。** 高さ・法線・geometry ビルダーの3者がこの1関数を通ることが「キャラクターが地面に沈まない」の唯一の根拠。

## 環境上の注意

- `npm install` で `esbuild@0.21.5` の postinstall が allow-scripts ポリシーによりブロックされる。**警告は出るが vitest は正常に動く**ので無視してよい
- `rtk` フックが `git` / `npm` コマンドを書き換える。vitest の出力が要約される場合、full log のパスが表示されるのでそれを読む
- **`assets/surface/`（約52MB、第三者 PBR）は `.gitignore` 済みで、demo の動作には必須。** クローンしただけでは demo が動かない。**圧縮はユーザーが自分で行う予定なので、こちらから変換・最適化を提案・実行しない。** 出典は ambientCG（5セット、CC0）と LotPixel（sand）
- `assets/generated/`（3.6MB、世界データそのもの）と `assets/vegetation/`（52KB、OpenGameArt）はコミット済み
- `assets/grass_02/`（TGA）と `assets/mayflower.glb` は未使用・未追跡。TGA は非圧縮なので使うなら変換が必要

## 作業のやり方で踏んだ失敗（繰り返さないこと）

段階6〜8 で実際にやった失敗。技術的な内容ではなく手順の話。

- **`git add <file>` でユーザーの作業を巻き込んだ。** `demo/main.ts` をコミットしたとき、そのファイルにユーザーの作業中の変更（KTX2 の配線）が入っていて、片方だけがコミットされて **HEAD が型チェックを通らない状態**になった（`Expected 2 arguments, but got 3`）。**コミット前に `git status` を見て、自分が触っていないファイルが混ざっていないか確認する。** `git add -A` は当然だめだが、ファイル指定でも中身が混ざる
- **破壊テストで「注入が適用されたこと」を確認しないと嘘をつく。** `sed` / 置換がタブ幅の不一致でマッチせず、無改変のファイルに対して「テストが通った = 空振りではない」と誤って報告しかけた。**置換の成否を assert して、注入後のファイルを grep で確認してから測る**
- **1地点の観測で調整値を決めた。** 密度を spawn 付近だけ見て「薄い」と判断し、次に良い場所だけ見て `cellSize` を詰めすぎた。**分布を測る**
- **見積りを実測の代わりにした。** 「最終密度は20倍振れる、最大40本/m²」と報告したが実測は 4.4倍・14.6本/m²。cap が先に効いていることを計算に入れていなかった。**数字を出す前に測る**
- **`settle()` のような検証ヘルパを同期ループで書いた。** Worker 経路の geometry は `message` イベントで届くので、1度もイベントループに戻らないループの中では**1枚も受け取れない**。200回まわして 36/256 枚しか揃わないのに `200` を返していた（「頑張ったが足りない」に見えて実際は何も進んでいない）
- **plan に書いた割り切りを実物で確認しなかった。** 「複数 Mesh を持つ GLB は先頭だけ使う（マージは v2）」と決めたが、木の GLB は全部2 Mesh で幹と葉が分かれていた。**割り切りを決める前にアセットの中身を見る**

### codex に委譲するときの境界

実装と node での検証は codex に任せられる。**ただし codex はブラウザを持っていない。**

段階8 で出た不具合3つ（`GPUValidationError`、`setKTX2Loader`、量子化 attribute のクランプ）は**すべてブラウザでしか出ない**。node のテストが全部緑でも実機が壊れていることがあるので、ブラウザ確認の担当を必ず決めること。

また codex の報告は鵜呑みにしないこと。実際にあったこと:

- plan のコードから `() =>` を落として転記し、それを「plan の誤り」として報告してきた（plan は正しかった）
- 指示した破壊テスト1件だけを測って「vacuous でない」と報告したが、plan が明示的に警告していた別の失敗モードがノーチェックだった
- 逆に、私のテスト件数の予測が3回外れているのを正しく指摘してきたこともある

**報告された数字は自分で再実測する。**

## タブがバックグラウンドだと rAF が止まる

demo の HUD が `fps 0 (tab hidden: rAF 停止中)` を出す。ブラウザ自動化でスクリーンショットを撮る以外の操作をしていると、タブが前面に来ないので:

- `terrain.update()` / `vegetation.update()` が呼ばれず、`count` が 0 のまま（`instanceCount` が 0 に見える）
- `setTimeout` が 1 秒にスロットルされるので `settle()` が 40 秒かかり、CDP の 45 秒制限に当たる
- HUD の fps は測定に使えない

**フレーム時間の測定はできない。** `renderer.render()` も `renderAsync()` も CPU 側のコマンド生成しか測っておらず GPU の実行を待たない（22.5M 三角形と 6.0M 三角形で 31.6ms 対 30.1ms とほぼ差が出なかった）。信頼できるのは描画インスタンス数と三角形数まで。

## v2 に先送りしたもの

spec §2 に理由付きの一覧がある。特に:

- RoadSystem（Spline）— `exclusion` SurfaceField を差し込み口として予約済み。`pathway` レイヤーは現在未使用
- Cliff Mesh / 洞窟 — hole マスクを下地として実装済み
- 改変差分（伐採など）— 決定論的インスタンス ID の算出規則を v1 で固定する
- chunk streaming、Biome、GPU-driven placement、Runtime Virtual Texture（フル版）、top-K blend、hybrid projection、草の踏み倒し
- タイリング対策の stochastic / hex-tile sampling（+114 sample で非現実的）

（normal map と texture array はここから v1 に移動した。上記「実装して分かった spec の誤り」を参照。）
