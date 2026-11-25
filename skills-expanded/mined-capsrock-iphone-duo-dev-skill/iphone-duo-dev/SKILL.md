---
name: iphone-duo-dev-skill
description: iOS アプリを iPhone Duo（Apple の折りたたみ iPhone）に対応させるときの手順と落とし穴。Xcode 27.2・iOS 27.2 以降が対象。リサイズできるレイアウト、折り目の領域、縦向きのツールバーとタブバー、split view と arrangement view、Duo のシミュレータのランタイム、2027年4月から App Store Connect で必須になる iPhone Duo のスクリーンショットを扱う。iPhone Duo、折りたたみの iPhone、内側・外側の画面、折り目やヒンジ、ArrangementView、ReservedRegion、縦向きのバーの話が出たとき、折りたたみ端末で表示がおかしい理由を聞かれたときに使う。Duo の名前が出なくても、既存の iPhone アプリをリサイズに対応させる、size class を取り入れる、広い画面向けに NavigationSplitView を足す、Duo 向けのスクリーンショット・提出・フィーチャーの推薦を準備する、といった作業にも使う。どれも同じ作業だから。
---

# iPhone Duo への対応

iPhone Duo は、中央のヒンジでつながった2つの画面を持つ。閉じているときに使う小さめの外側の画面と、開いたときの 7.6 インチの内側の画面。どちらにも前面カメラがあり、内側のカメラは使っているあいだしか見えない。開く・閉じる・途中まで折る・回す、に合わせて、表示は画面のあいだを移る。

ここに書くことすべての前提：**これは新しいプラットフォームではない。** ウインドウの大きさが大きく変わる iPhone である。Apple もはっきりそう言っている。iPad と Mac で動くアプリ、iPhone ミラーリングでリサイズに対応したアプリなら、もうほとんど済んでいる。作業のほとんどはレイアウトをリサイズに対応させることで、iPad 対応と同じ作業になる。

このスキルは **Xcode 27.2 以降、iOS 27.2 SDK 以降** を前提にする。

## 使う場面

- 既存の iOS アプリを iPhone Duo に対応させる
- 内側の画面・Split View・折ったときにレイアウトが崩れる原因を調べる
- iPhone で size class、`NavigationSplitView`、リサイズできるレイアウトを取り入れる
- 折り目を扱う：`ReservedRegion`、`ArrangementView`、ヒンジの状態
- システムが横へ移すツールバーとタブバーを整える
- iPhone Duo のスクリーンショット、提出、フィーチャーの推薦を準備する

## ビルドの条件

**CI も含めて、Xcode 27.2 以降でビルドする。** Duo の画面を全部使えるかどうかは、リンクした SDK で決まる（講演 *Prepare your app for iPhone Duo*、00:30〜01:18）：

| ビルドに使ったもの | 結果 |
|---|---|
| Xcode 26 以前（iOS 27 より前の SDK） | 動く。閉じたときはステータスバーとカメラの左側の領域を使い、開いたときは見慣れた大きさと縦横比で出る。ステータスバーとカメラの下までは広がらない |
| iOS 27.0 SDK | 内側の画面で、ステータスバーの領域の左まで広がる |
| iOS 27.1 SDK 以降 | 画面の端まで広がり、標準のナビゲーションとツールバーのボタンが、ステータスバーの下に縦に並ぶ |

古い Xcode に固定した Xcode Cloud のワークフローは、ビルドも通るしテストも通る。そのうえで、全画面のレイアウトにならないバイナリを黙って作る。表示名ではなく、固定している版を確かめる。

`UIRequiresFullScreen` は今も効くが、開閉するとアプリはやはりリサイズされる（04:37）。逃げ道にはならない。このキーは iOS 26 で非推奨にもなっている。

iOS 27.1 SDK でビルドしたまま、画面の半分の幅にとどまる方法も無い。フォーラムで Apple の技術者が「No you cannot」と答え、iPhone だけのアプリも含めて、どのアプリも実行時にどんな scene の大きさにも合わせることを求めている（Apple Developer Forums の iPhone Duo SwiftUI Q&A、thread 847836）。

Duo のシミュレータのランタイムとその見つけ方、シミュレータでできないこと、Xcode Cloud、App Store のスクリーンショット、フィーチャーは `references/environment.md` にある。

## 効くレイアウトの決まり

### idiom や向きではなく、size class で決める

| 状態 | 横 | 縦 |
|---|---|---|
| 外側の画面、縦向き | compact | regular |
| 外側の画面、横向き | compact | compact |
| 内側の画面 | regular | regular |

レイアウトは2つで全部の姿勢を覆える：**外側の画面は compact の幅、内側の画面は regular の幅。** 姿勢ごとにレイアウトを作らない。姿勢は連続していて、姿勢ごとのレイアウトは操作要素を跳ね回らせる。

レイアウトを `UIDevice.userInterfaceIdiom` や `UIInterfaceOrientation` で分けない。当てになるのは size class と、入れ物自身の bounds だけ。横向き専用の見た目にしたいときも、向きではなく**使える幅**で決める。ウインドウは横向きで、しかも細いことがある。

向きについて、Apple はめずらしく言い切っている（講演 *Prepare your app for iPhone Duo*、03:42〜04:51）：

> The inner display doesn't honor your supported interface orientations.

（内側の画面は、アプリが対応する向きを守らない。）

> iPhone Duo respects your supported interface orientations, but your app will scale on the inner display, including in Split View multitasking.

（iPhone Duo は対応する向きを尊重するが、内側の画面では、Split View を含めてアプリが拡大縮小される。）

つまり、縦向きだけのアプリも逃れられない。拡大縮小されるだけで、size class はどちらにしても regular/regular になる。外側の画面はふつうの iPhone と同じように振る舞う。人はテントのように立てて置くので、Apple は Duo を「横向きに対応する絶好の機会」と呼んでいる。ゲームは向きを1つに固定してよいが、HIG はどの姿勢でも画面を埋め、黒帯を入れるより縦横比を変えるほうを選ぶよう求めている。

`UIScreen.main` は使わない。iOS 26 で非推奨になっていて、画面が2つある端末ではどちらを指すかがあいまいになる。environment、trait collection、scene の bounds を使う。どうしても画面が要るときは window scene から読み（`UIWindowScene.screen`）、`UIScreen.main.scale` の代わりに `traitCollection.displayScale` を使う。

### コードの中から探して直すもの

Apple の Duo のページ（developer.apple.com/iphone-duo/ の *Three steps to prepare your app for iPhone Duo*）は、探して直す書き方を挙げている：

| 探すもの | 直し方 |
|---|---|
| `UIScreen.main.bounds` | `view.bounds` か `window.bounds`。SwiftUI は `GeometryReader` か `onGeometryChange` |
| 起動時や `viewIsAppearing` で一度だけ読んだ大きさ | 折ると使っている途中で大きさが変わる。大きさに頼るレイアウトは `layoutSubviews` か `viewDidLayoutSubviews` で、変わったときの処理は `viewWillTransition(to:with:)` でやる |
| `UIScreen.main.scale` | UIKit は `traitCollection.displayScale`、SwiftUI は `@Environment(\.displayScale)` |
| `UIWindow(frame: UIScreen.main.bounds)` | `UIWindow(windowScene:)` |
| 保存した `UIScreen` | 持っておかない。要るときに `view.window?.windowScene?.screen` で読む |
| `UIDevice.current.orientation`、`statusBarOrientation`、`interfaceOrientation`（`windowScene.effectiveGeometry.interfaceOrientation` も） | これに頼るレイアウトを消す。横長かどうかは、使える場所の幅と高さを比べる（view controller なら `view.bounds`、view なら `superview.bounds`、SwiftUI なら `GeometryReader` の大きさ） |
| `userInterfaceIdiom == .phone`／`.pad` | idiom でレイアウトを選ばない。使える場所で選ぶ |
| `horizontalSizeClass == .regular` を iPad とみなすコード、iPhone はいつも compact という思い込み | その iPad のレイアウトが iPhone でも動くようになる。内側の画面では、iPad のレイアウトを自然に延ばした見た目になるべきである |
| `bounds.height == 844` のような端末の大きさの比較、既知の iPhone の寸法の一覧 | Duo には合わない。消す |
| `.scaleAspectFill`／`.aspectRatio(contentMode: .fill)` の全面の画像や動画 | 広い画面では大事なところが切れることがある。size class か縦横比で fill と fit を選ぶか、焦点を決める |

画面の角に合わせるには、iOS 26 の Concentricity の API を使う。Duo の画面の形にも対応した：SwiftUI は `ConcentricRectangle`、UIKit は `UICornerConfiguration`（04:18）。

### セーフエリアは左右で違う

これは、シミュレータでは見つかり、ウインドウのリサイズでは見つからない崩れ方である。バーが片側の縁に沿って出るので、向かい合う辺のインセットが違う。レイアウトマージンと content inset も同じく違う。

```swift
// 誤り — 左右のインセットが同じだと仮定している
let width = view.bounds.width - view.safeAreaInsets.left * 2

// 正しい — 辺ごとに扱う
let width = view.bounds.inset(by: view.safeAreaInsets).width
```

よくやらかすのは縦向き固定のアプリ。上下のインセットしか通ってこなかったので、コードのどこにも左右のインセットを考えて書いたところが無い。

**画面の中央にそろえたレイアウトを、まず見直す。** 横の操作要素があるので、ほとんどの内容は隠れないようにずらす必要がある。横のセーフエリアのインセットにそろえていれば、ずれは自動で付く。全画面の中央にそろえたままでよいのは、スクロールしない没入型の、見た目が主の画面で、右の操作要素に操作できる要素がふさがれないと分かっているときだけ（講演 *Design for iPhone Duo*、06:28〜07:15、講演 *Strike a pose with adaptive layouts on iPhone Duo*、16:15）。全幅の背景やヘッダーと、インセットの中でスクロールする内容を組み合わせてもよい。そのときは、操作できる要素をすべてスクロールする領域の中に置く。

操作要素と前面の内容はセーフエリアの中に置き、背景はセーフエリアの外、バーの後ろまで広げる。SwiftUI は初めから内容をセーフエリアの中に置くので、気をつけて扱うのは背景のほう（`ignoresSafeArea()` は背景の層だけに付ける）。

UIKit では、iOS 27.1 以降、ふつうの `UIView` の既定のレイアウトマージンは 0 になる。view controller は今もルートの view に `systemMinimumLayoutMargins` を与える。それを受け継ぐべきサブビューには `preservesSuperviewLayoutMargins = true` が要る（iOS 27.2 のリリースノート、186294594）。

### 大きさは画面ではなく入れ物を基準にする

```swift
// 誤り — ウインドウの大きさが変わると、画面の寸法は意味を持たない
let width = UIScreen.main.bounds.width * 0.4

// 正しい — 入れ物が大きさを提案するので、それを使う
GeometryReader { proxy in
    Rectangle().frame(width: proxy.size.width * 0.4)
}
```

悪いのは `GeometryReader` ではなく、**画面**を読むこと。入れ物を基準にした比率の余白は問題ない。ただ、ずっと大きな画面では高さの割合が大きな空きになる。見た目が変わってもよいなら、固定の格子の間隔と、伸び縮みする Spacer を使うほうがよい。`containerRelativeFrame(_:alignment:)` は、いちばん近い入れ物（`NavigationStack`、`NavigationSplitView` の列、`TabView` のタブ、scroll view や list）の大きさからセーフエリアのインセットを引いた値で測る。比率を計算するためだけに置いた `GeometryReader` は、これでそのまま置き換えられる。もっと近い入れ物が無いとき、iOS では画面が基準になる。

### システムの入れ物を使う

`NavigationStack`、`NavigationSplitView`、`TabView`、シート、ポップオーバー、アラート、メニューは、リサイズ、折り目を避けること、カメラに隠れることを、もう扱っている。自前の入れ物を使うと、それを全部作り直すことになる。Duo の不具合のほとんどは、標準の入れ物なら正しくやっていたことを自前のレイアウトのコードがやっているところで起きる。

例外はスクロールする内容。list・table・scroll view・collection view は折り目のところで中身を分けないので、途中まで折ると行が折り目にまたがることがある。たいていはそれでよい。読みにくい・使いにくいときだけ、division の領域を読んで自分で並べる。

### 内側の画面では、違う機能ではなく、より深い階層を見せる

お手本はメール。閉じているときは一覧**か**メッセージのどちらか、開くと両方が並ぶ。`NavigationSplitView` は内側の画面で広がり、外側の画面では1列にたたまれる。ほかの端末で regular と compact のあいだですでにやっているのと同じ振る舞いである。

Apple は、内側の画面でただ引き延ばした iPhone のアプリにしないよう求め、3つのやり方を挙げている（講演 *Design for iPhone Duo*、07:34〜08:33）：

- **Split view** — アプリの階層のいくつかの段を同時に出す。外側と内側の画面で階層を変えない。
- **広い画面に合わせて内容を並べ直す** — ミュージックのように、縦に積んだレイアウトを、横に場所があるときは2列にする。
- **タブバーを内側の画面でサイドバーにする** — どのアプリにも合うわけではなく、ヘルスケアのような情報の多いアプリに向く。

機能と状態は、画面と姿勢が変わっても同じに保つ。作業の途中で端末を開いた人は、続きの場所に、同じ操作要素がそろった状態で着くべきである。開閉は size class と trait の変化として届き、scene が切れるわけでもアプリが終わるわけでもない。メモリ上の状態、入力中の文字、スクロールの位置、動画の再生は、ふつうはそのまま残る（Apple Developer Forums の *A Summary of the iPhone Duo Group Lab*）。

## バーは横へ移る

外側の画面と、内側の画面の一部の view で、システムはナビゲーションバー・ツールバー・タブバーを、片側の縁に沿った縦向きのバーへ移す。例外は内側の画面の縦向きで、横向きのバーのままになる。

**バーの中身がナビゲーションの入れ物に載っていれば**、これは何もしなくても得られる。SwiftUI なら `NavigationStack` か `NavigationSplitView` に付けた `.toolbar { }`、UIKit なら `UINavigationController` の中の view controller に設定したツールバーの項目。自分で置いた `UIToolbar` や、自作の下のバーの `HStack` は加わらない。

**タイトルだけでアイコンの無いツールバーの項目は、縦向きのバーに出ない。custom view で作った項目も出ない。** どの項目にもタイトルとシンボルの両方を付ける。縦向きのバーではシステムがアイコンを選び、オーバーフローのメニューではタイトルを使う。

```swift
ToolbarItem(placement: .topBarTrailing) {
    Button { showFilter = true } label: {
        Label("Filter", systemImage: "line.3.horizontal.decrease")
    }
}
```

バーの振る舞いを調整する前に `references/bars.md` を読む。並べる順、オーバーフローの優先度、シートと split view の例外、使える版つきの API の一覧がある。

## 折り目

折り目の API は層になっている。問題を解ける中でいちばん上の層を使う。ヒンジの角度から自分でレイアウトを計算するのは、ほとんどの場合、層の選び方が間違っている。

| 層 | 得られるもの |
|---|---|
| システムの部品 | アラート、シート、メニュー、split view — コードを書かなくても合わせてくれる |
| Arrangement view | `HStack`／`ZStack` の形をした、折り目に合わせる入れ物 |
| Reserved region | 避けるべき領域の矩形 |
| ヒンジ | 生の折り角 — レイアウトではなく、動きのある効果のため |

途中まで折ると、折り目の領域が内側の画面を分ける。iOS はこれとカメラを **reserved region** として表す：`division`（折り目が内容を分ける）と `occlusion`（ハードウェアが内容を隠す）。

デザインの決まり：**操作要素を折り目に置かない。** 操作しない内容はまたがってよい。画面の中央にある大きなタップできる要素（ボタンを兼ねたヒーロー画像、タップすると音を鳴らすキャラクター）は、本のように持つとちょうど折り目に来る。折った姿勢で試すまで、この不具合は見えない。

標準の部品は自分で動く。自前のレイアウトは領域を問い合わせる。既定では動いている（アクティブな）領域だけが返る：

```swift
GeometryReader { proxy in
    let folds = proxy.reservedRegions(kind: .division)
    // frame はこの view の座標で、領域の margins をすでに含む
}
```

`ReservedRegion`、`ArrangementView`、ヒンジの型は、どれも iOS 27.1 から。それより低い deployment target では `if #available(iOS 27.1, *)` で分ける。古い OS には、扱うべき折り目が無い。

`ReservedRegion` の API、`ArrangementView`、姿勢の指針は `references/reserved-regions.md` を読む。

## 対応のチェックリスト

上から順に進める。最初のまとまりは壊れるところ、次は大きな画面でよくするところ、最後はそれを全部確かめる方法。

**壊れるところを直す**

1. CI も含めて Xcode 27.2 以降でビルドする。
2. システムの入れ物を作り直している自前の入れ物を、`NavigationStack`、`NavigationSplitView`、`TabView`、シート、ポップオーバーに置き換える。Duo の不具合のほとんどは、標準の入れ物なら正しくやっていたことを自前のレイアウトのコードがやっているところで起きる。
3. 「コードの中から探して直すもの」の表を上から探す（`UIScreen.main`、向き、idiom、端末の寸法、全面の画像）。
4. 画面の中央にそろえたレイアウトを見直し、2列にするか、横のインセットに合わせてずらす。
5. どの画面も幅の変化に耐えるようにする。compact と regular の両方の幅で確かめる。
6. セーフエリアは辺ごとに扱い、Split View の左側と右側の両方で試す。
7. ツールバーの項目にタイトルとシンボルの両方を付け、バーがナビゲーションの入れ物から出ていることを確かめる。
8. 操作要素を折り目から外し、自前のレイアウトでは `ReservedRegion` を使う。
9. 作業の途中で折る・開く・回すをしても、状態と再生が残ることを確かめる。
10. 「透明度を下げる」をオンにして見直す。この設定では、縦向きのバーに不透明な背景が付く。

**大きな画面を活かす**

1. シート、ポップオーバー、全画面のカバーを見直す。7.6 インチの画面で全画面のカバーは、たいてい選び方を誤っている。
2. 階層が自然に一覧と詳細に分かれるところでは、`NavigationSplitView` を考える。
3. 内側の画面で大きな Dynamic Type を確かめる。広い画面だと大きな文字がずっと使いやすくなるので、それを必要とする人がここに来る。

**確かめる**

1. Duo のシミュレータの前に、リサイズで崩れを探す。Apple が挙げる道具は、Device Hub のリサイズできる iOS のシミュレータ、macOS 27 の iPhone ミラーリング（ウインドウを縦横とも極端な大きさまで変える）、Duo のシミュレータ。全部の体験を確かめられるのは Duo のシミュレータだけ（*Three steps to prepare your app for iPhone Duo*）。
2. どの画面も、すべての姿勢と両方の画面で見て回る。シミュレータなら、AXe が Device Hub を開かずに姿勢を動かして撮れる — `axe hinge set open|closed|tabletop|<角度>`、`axe rotate left|right`、`axe displays`、`axe screenshot`。詳しいことと落とし穴は [`ios-simulator-automation`](https://github.com/capsrock/ios-simulator-automation-skill) にある。
3. VoiceOver は実機で確かめる。Device Hub の中では、アクセシビリティの道具が Duo のシミュレータの画面を読めない（Xcode 27.2 のリリースノート、187148389）。
4. App Store Connect 用の iPhone Duo のスクリーンショットを撮る。外側と内側の画面のサイズは `references/environment.md` にある。

## よくある間違い

**向きを固定すれば守られると思う。** 守られない。内側の画面は、宣言した向きを「回転しない」という形で守り、そのうえでアプリを拡大縮小する。size class は regular/regular のまま。縦向きだけにとどまっても、見た目が悪くなるだけで免除にはならない。本当の作業は幅への対応である。

**すべての姿勢に合わせてデザインする。** 特定の姿勢を深く作り込むのは、本当にアプリのためになるところだけにする（寝かせて置いたとき、メディアプレーヤーが操作要素を下半分に移す、など）。そのときも、操作要素と階層は同じに保つ。

Apple の講演も同じことを言っている。姿勢ごとに専用のレイアウトを作らず、外側の compact の幅と内側の regular の幅の2つの size class に合わせる。固定の幅、ブレークポイント、特定の画面に結びついた寸法を避け、レイアウトマージンと横のセーフエリアのインセットで組む。考える価値のある例外は、机に置いて手を離して使う姿勢だけで、メディアを上に、タップする操作要素を下の安定した台に置く。そのときも、ほかの姿勢と同じ操作要素とおおまかな階層を保ち、機能を特定の姿勢に結びつけない（講演 *Design for iPhone Duo*、03:38〜04:46）。

**持ち方は1つだと思う。** カメラ側を下にして立てる人も、外側の画面を下にして立てる人もいる。どちらでも同じように動くべきである。

**`ArrangementView` をほかの入れ物と入れ子にする。** arrangement view は内容を並べるもので、ナビゲーションは扱わない。list・scroll view・grid の中に入れない（view の一部に届かなくなることがある）。中に `NavigationSplitView` や `TabView` を入れない。`NavigationStack` の中に置くのは Apple 自身の講演の例である。navigation split view で外から囲むことについては Apple の文書どうしで言っていることが違う。それは `references/reserved-regions.md` にある。

**システムのバーの置き方を上書きする。** 縦向きのバーは Duo の中心の型である。`.toolbarVerticalBehavior(.disabled)` は、本当に端まで使うスクロールしない画面（動画プレーヤー、計算機）のためにあり、見慣れた見た目を保つためのものではない。

**起動するから大丈夫だと思う。** 縦向き固定でリサイズしないアプリも動く。7.6 インチの画面で拡大縮小されるか、黒帯が付くだけである。それこそが、この作業で避けたい結果である。

## 参照

- `references/bars.md` — 縦向きのバー、ツールバーの置き方とオーバーフロー、シートと split view の例外、API の一覧
- `references/reserved-regions.md` — 折り目とカメラの領域、`ReservedRegion`、`ArrangementView`、姿勢、複数のウインドウ
- `references/environment.md` — Duo のシミュレータのランタイム、シミュレータの制限、Xcode Cloud、App Store のスクリーンショットとフィーチャー、ブラウザを使わずに Apple の一次資料を読む方法
