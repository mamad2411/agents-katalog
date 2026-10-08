# AGENTS.md — 撮る単語帳 Mobile

このディレクトリはExpo / React Native版「撮る単語帳」の正本です。

## 最初に読むファイル

1. `README.md`
2. `../toru-tango/IOS_MIGRATION_SPEC.md`
3. `../toru-tango/CODEX_HANDOFF.md`
4. `../toru-tango/backend/README.md`

## 固定方針

- Expo SDK 57 / React Native / TypeScript / Expo Routerを維持する。
- Web版を正本に戻さず、iOS版はこのディレクトリで継続する。
- OpenAI APIキーをアプリ、GitHub、`.env.example`へ書かない。
- AI作問は `EXPO_PUBLIC_AI_API_URL` からCloudflare Workerへ接続する。
- AI API失敗時の端末内簡易作問を削除しない。
- 既存カードと履歴を破壊するデータ移行を行わない。
- Bundle IDはユーザー確認なしに変更しない。
- 既存ファイルを全面置換する前に差分を確認する。

## 作業開始時

```bash
npm install
npm run typecheck
npm run lint
npm run doctor
```

失敗した検査は原因を修正してから次へ進む。package-lock.jsonが未作成なら、依存関係確定後に生成してコミットする。

## 次の優先作業

1. CIの初回結果を確認してTypeScript・ESLint・Expo Doctorを修正する。
2. iPhone実機またはEAS preview buildで主要4画面を確認する。
3. 教材写真からのOCR導線を実装する。高精度OCRが間に合わない場合は初回TestFlightで手入力導線を明確化する。
4. 1024pxアイコンと起動画面を追加し、app configへ設定する。
5. Cloudflare Workerを公開してAI作問を実接続する。
6. EAS production buildとTestFlight提出の設定を仕上げる。

## 完了条件

- `npm run typecheck` 成功
- `npm run lint` 成功
- `npm run doctor` 重大エラーなし
- カード追加・編集・削除・学習・履歴・バックアップ復元が実機で動作
- API未設定、権限拒否、不正JSON、空データでクラッシュしない
- EAS production build成功
- App Store Connectへビルドをアップロード済み
