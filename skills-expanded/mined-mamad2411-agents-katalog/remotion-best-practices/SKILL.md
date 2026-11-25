---
name: remotion-best-practices
description: Remotion（ReactでプログラマティックにビデオとアニメーションGIFを作成するフレームワーク）のベストプラクティスを提供するスキル。Remotionコードを扱う際に使用してください。
---

## 使用するタイミング
Remotionのコードを扱う際は常にこのスキルを参照し、ドメイン固有の知識を取得してください。

## オプション：1フレームレンダーチェック
CLIを使って単一フレームをレンダーすることで、レイアウト・色・タイミングの確認を行えます。
単純な編集・リファクタ・Studioや事前のレンダーで十分な確信がある場合はスキップ可能です。

```bash
npx remotion still [composition-id] --scale=0.25 --frame=30
```

30fpsでは `--frame=30` が1秒地点（フレームはゼロベース）。

## 各ルールファイルの読み込み

各トピックの詳細なルールとコード例は対応するルールファイルを参照してください：

- [rules/animations.md](rules/animations.md) - Remotionの基本アニメーション
- [rules/assets.md](rules/assets.md) - 画像・動画・音声・フォントのインポート
- [rules/audio.md](rules/audio.md) - 音声の使用（インポート・トリミング・音量・速度・ピッチ）
- [rules/compositions.md](rules/compositions.md) - コンポジション、Still、フォルダ、デフォルトPropsの定義
- [rules/fonts.md](rules/fonts.md) - GoogleフォントとローカルフォントのRemotionへの読み込み
- [rules/images.md](rules/images.md) - Imgコンポーネントを使った画像の埋め込み
- [rules/sequencing.md](rules/sequencing.md) - 遅延・トリミング・デュレーション制限のシーケンシングパターン
- [rules/subtitles.md](rules/subtitles.md) - キャプション・字幕の処理
- [rules/text-animations.md](rules/text-animations.md) - テキストアニメーションパターン
- [rules/timing.md](rules/timing.md) - interpolate・Bézierイージング・スプリングによるタイミング
- [rules/transitions.md](rules/transitions.md) - シーントランジションパターン
- [rules/videos.md](rules/videos.md) - 動画の埋め込み（トリミング・音量・速度・ループ・ピッチ）

## キャプション
キャプション・字幕を扱う場合は [./rules/subtitles.md](./rules/subtitles.md) を参照してください。

## FFmpegの使用
動画のトリミングや無音検出など一部の動画操作にはFFmpegを使用してください。

## 音声ビジュアライゼーション
スペクトルバー・波形・低音反応エフェクトなどの音声可視化が必要な場合は
[./rules/audio.md](./rules/audio.md) を参照してください。
