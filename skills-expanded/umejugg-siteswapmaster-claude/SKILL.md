# umejugg-siteswapmaster（Web / umejugg.com/siteswapmaster/）

高精度なジャグリング・サイトスワップのシミュレーション、生成、接続、変換、解析を行う Web アプリです。

## ファイルごとのバージョン管理

JS / CSS などのファイルは**ファイル単位でバージョン管理**しています。バージョンは以下の2か所に記載されているため、**修正した際は必ず両方を更新**してください。

1. **各ファイルの先頭**にバージョンを記載
   - CSS: コメントで記載（例: `/* simulation.css ver 9.3.2 */`）
   - JS: クラスの `static VERSION` プロパティ、もしくはファイル冒頭の定数（例: `static VERSION = "1.5.6";`、`const PROCESSOR_VERSION = '1.1.4';`）
2. **`README.md` の「現在のバージョン」表**に最新版を反映

## `simulation.js` / `simulation.min.js` の変更方針

`simulation.js` および `simulation.min.js`（シミュレーター・コアエンジン）は、**ユーザーから明示的な指示がない限り、中身を変更しない**方針で実装してください。これらに依存する他ファイル側で対応する形を基本とします。
