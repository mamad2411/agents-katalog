---
description: Excel 2021/2024 前提と、VBA でのウィンドウ枠固定（FreezePanes）の必須手順
globs: "**/*VBA*.txt,**/master_xlsm_VBA.txt,**/生産管理_AI配台テスト_xlsm_VBA.txt"
alwaysApply: false
---

# Excel / VBA（このプロジェクト）

## バージョン前提

- 利用 Excel は **Microsoft Excel 2021 または 2024** とする（互換性・ダイアログ・オブジェクトモデルの前提）。

## ウィンドウの固定（FreezePanes）を VBA で行うとき

見出し行（例: 1行目）をスクロール固定する処理では、**次の順序を必ず守る**。この順を崩すと、1行目が見えないまま固定されるなど不具合が出る。

1. **固定の解除**  
   - `ActiveWindow.FreezePanes = False`  
   - あわせて `ActiveWindow.Split = False`（分割が残っていると挙動が乱れることがある）

2. **A1 を選択し、表示位置をリセット**  
   - `Range("A1").Select`（または同等）  
   - `ScrollRow = 1` / `ScrollColumn = 1` で左上に戻す  
   - 必要に応じて `Application.GoTo Range("A1"), True` で画面内にスクロール  
   - 反映待ちに `DoEvents` を挟んでもよい

3. **見出し行の固定**  
   - Excel の仕様上、**固定したい行の直下のセル**をアクティブにする（1行目固定なら **`A2.Select`**）  
   - その後 `ActiveWindow.FreezePanes = True`

複数ブックを開いている場合は、対象シートのブックをアクティブにしてから上記を行う。

今後、出勤簿・マスタ等の VBA で FreezePanes を追加・変更するときは、この手順に合わせて実装・レビューすること。
