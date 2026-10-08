---
description: スクリプトの入出力を環境のロケールに依らせない書き方である。非 ASCII を出すスクリプトを書くとき、文字コードで落ちたときに使う。
name: script-encoding
---

# script-encoding — ロケールに依らない入出力

日本語や記号を出すスクリプトは、実行環境のロケール次第で落ちる。落ちる環境と落ちない環境があるため、書いた本人の手元では通ってしまう。入出力の符号化を環境に聞かず、スクリプトの側で UTF-8 に決める。

## 何が起きるか

Python は標準入出力の符号化を実行時のロケールから決める。Windows の日本語環境ではこれが cp932 になり、cp932 に無い文字を読み書きした時点で落ちる。

- 落ちるのはパイプ・リダイレクトのときだけ
  - コンソールへ直結していれば UTF-8 が使われる
  - 手で叩くと通り、他のコマンドへ繋いだ瞬間に落ちる
  - エージェントからの実行は常にパイプなので必ず踏む
- コンソールのコードページ（`chcp`）は関係しない
- 引き金は絵文字だけではない
  - `—`（U+2014）のような、日本語の文書にふつうに出る記号が cp932 に無い
- Linux・macOS では既定が UTF-8 なので起きない
  - 対象環境が Linux でも、書き手の手元が Windows なら落ちる

シェル（bash）は文字列をバイト列のまま流すので、この問題は起きない。

## 決まり

非 ASCII を読み書きするなら、符号化を環境に聞かず明示する。

Python では、最初の入出力より前に次を置く。UTF-8 が既定の環境では何も変わらない。

```python
sys.stdin.reconfigure(encoding="utf-8", errors="replace")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
```

ファイルを開くときも同じである。`open()` の既定の符号化もロケールから決まるため、`open(path, encoding="utf-8")` と書く。

呼ぶ側で `PYTHONUTF8=1` や `PYTHONIOENCODING=utf-8` を立てる形は採用しない。呼ぶ人が毎回覚えている必要があり、スクリプトを渡した先では効かない。

## 直ったかを確かめる

手元が UTF-8 だと、直っていなくても通る。ロケールを cp932 に見せかけて確かめる。

```sh
PYTHONIOENCODING=cp932 <ふだんの呼び出し>
```

非 ASCII を含む入力を流し、終了 0 で UTF-8 の出力が出れば直っている。cp932 の変換表は Python に同梱されているので、Linux・macOS でも同じ確認ができる。

## 落ちたときの読み分け

| 症状 | 出どころ |
| --- | --- |
| `UnicodeEncodeError: 'cp932' codec can't encode character` | 出力 |
| `UnicodeDecodeError: 'cp932' codec can't decode byte` | 入力 |
| 落ちずに `\u2705` の形で出る | 標準エラー |

標準エラーは既定が `backslashreplace` であるため、落ちずに読めない形へ化ける。
