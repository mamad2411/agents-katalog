---
description: CH9329 のパケット生成・チェックサム・JP109 キーマップ・シリアル送信を実装／修正するときの制約。PacketBuilder / KeyMap / SerialDevice / TextSenderService に触れる作業で参照する
alwaysApply: false
---

# CH9329 Protocol

一次資料（外部）: [マルツ掲載の解説書 PDF](https://www.marutsu.co.jp/contents/shop/marutsu/datasheet/minnanolab_MR-CH9329EMU.pdf)（詳細は `docs/` のプロトコル仕様）

## 接続

- USB 接続版 = 仮想 COM。既定ボーレート **9600**（変更時は本体設定も必要）
- 送信はバイト列。コマンド後に返信 7 バイトあり（MVP では読み捨て可）

## キー入力パケット

- 形式: `57 AB` + addr(`00`) + cmd + len + data + checksum
- 通常キー: コマンド **`0x02`**、データ長 `0x08`（本文の「0x01」表記は誤記扱い。表とサンプル例に従う）
- **押す → 離す（全キー 0）** をワンセットにする
- checksum = ヘッダ〜データまでの総和の下位 1 バイト

## キーマップ

- **日本語 109 配列**の HID 用法キーコード（マニュアル付録）
- ASCII は文字 →（修飾キー + キーコード）へ変換。Shift 要否をキーマップに含める
- 未対応文字は送信せず、呼び出し側へ明確に失敗を返す

## 実装方針

- パケット生成とシリアル I/O を分離する
- 文字間ディレイは設定可能にし、既定は **20 ms**（`docs/02-protocol-ch9329.md` の値。実機検証で変えるときは仕様も更新する）
- キーコードは `docs/02-protocol-ch9329.md` の表を唯一の正とする。コード側にだけ独自の値を足さない
