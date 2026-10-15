---
name: redstone-basics
description: レッドストーン基礎回路。自動化に使用（mc_execute用）
---
## 基本素材
- redstone_dust（回路）、lever/button（入力）、redstone_torch（信号反転）
- piston（ブロック移動）、observer（変化検知）、hopper（アイテム輸送）

## よく使う回路
- NOT: redstone_torch + dust（信号反転）
- クロック: observer x2 向かい合わせ（無限パルス）
- Tフリップフロップ: lever→NOT→piston制御

## 自動収穫（サトウキビ等）
1. サトウキビの後ろにobserver設置
2. observer → piston（横向き）
3. piston が2段目を押して収穫
4. 下にhopper → chest で自動回収

## 重要ルール
- レッドストーンは15ブロックまで信号伝達
- 延長はrepeaterで（4ブロックごとに1個）
- 回路は地面か壁に設置（空中不可）
