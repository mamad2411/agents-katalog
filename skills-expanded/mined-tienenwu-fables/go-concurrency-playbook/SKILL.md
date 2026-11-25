---
name: go-concurrency-playbook
description: Use when designing or debugging high-concurrency Go services, especially worker pools, backpressure, bounded channels, errgroup/WaitGroup, rate limits, load shedding, circuit breakers, GOMAXPROCS, or connection pools; also for load-time OOM, rising goroutines, lock contention, p99 spikes, retry storms, pprof, singleflight, semaphore, or production-only collapse.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/go-concurrency/SKILL.md) · 繁體中文（正本 / canonical）

# Go 高併發判準手冊

前置：單機正確性（error 三選一、goroutine 洩漏三典型、nil interface、context 規則、channel vs mutex、專案結構）見 backend-server 的 `references/go.md`，本手冊不重複。本手冊從「單機跑對了」往上接「同時湧入一萬個請求時還撐得住」。

## 核心原則

1. **併發是設計決策，不是加速鈕**：開 goroutine 前先問「瓶頸真的在這嗎」。沒有瓶頸證據就加併發，只是把 bug 變並行 bug。
2. **任何無界的緩衝都是延後爆炸的 OOM**：生產速度可能超過消費速度的每一個邊界，都要有界 + 「滿了怎麼辦」的明確決策（block / drop / reject 擇一）。
3. **高併發問題先看「等待」不是看 CPU**：排查順序是 goroutine profile（洩漏/阻塞）→ 鎖競爭 → CPU → trace（排程）。多數「慢」是在等鎖、等下游、等排程，不是算得慢。
4. **「感覺慢」禁止直接改**：先 profile 拿到證據再動手；憑感覺加 goroutine / 加 cache / 換資料結構，多半改錯地方還更慢。
5. **上線才爆的問題驗證只能用壓測**：單機低流量對「洩漏、鎖競爭、池飽和、GOMAXPROCS 錯配」零證據力——這些要在目標 RPS 的壓力下才現形。

## 開工分流

| 情境 | 路徑 | 先讀 |
|------|------|------|
| 想「開幾個 goroutine 加速」 | 先確認瓶頸與是否需要併發，再決定 pool | references/concurrency-patterns.md §1 |
| 要開 worker pool / 限並發 / fan-out | 定 worker 數與界限，選對原語 | references/concurrency-patterns.md |
| 多個子任務要並行 + 錯誤傳播/取消 | errgroup，不是裸 WaitGroup | references/concurrency-patterns.md §3 |
| 高併發讀同一 key + 回源貴 | singleflight 防 cache stampede | references/concurrency-patterns.md §5 |
| 接 channel/queue、怕 OOM、設 timeout | 有界 + 背壓 + timeout 預算逐層遞減 | references/backpressure-limits.md |
| 加 rate limit / 限流 / 熔斷 / 降載 | 選型與「是否真需要」判準 | references/backpressure-limits.md |
| 服務變慢、要調效能 | 先 profile 拿證據，別先改 | references/performance-profiling.md |
| 懷疑鎖競爭 / GC 壓力 | mutex/block profile、修法優先序 | references/performance-profiling.md |
| 出 release / 上高流量前 | 逐條跑必查清單（壓測是硬條件） | references/release-checklist.md |

## 紅線（絕對禁止）

- **禁止用無界 channel / 無界 queue / 無限 `go func()` 當緩衝**——生產快於消費時記憶體無上限成長，尖峰直接 OOM，且 OOM 前 GC 壓力先讓全服務變慢。
- **禁止內層 timeout ≥ 外層 timeout**——內層等好等滿，外層早已放棄回錯，內層還在跑＝做白工＋佔用資源，取消語意全失效。
- **禁止「感覺慢」就直接改效能**——沒有 profile 證據的優化是猜測，改錯地方浪費時間還可能更慢。
- **禁止 worker 數 / 連線池大小拍腦袋填 100**——超過下游（DB max_connections、上游 API 限額）容量的並發只會製造排隊與逾時，數字要從下游容量反推。
- **禁止在高併發程式碼省略 `-race` 驗證**——data race 在低流量偶發、在高流量必現且不可重現，`-race` 是唯一能穩定抓到的手段。
- **禁止重試不加退避與 jitter**——下游一抖，所有 client 同步重試形成重試風暴，把短暫故障放大成雪崩。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| goroutine 數隨時間單調上漲不回落 | 洩漏（缺 ctx 出口 / 沒人讀的 channel） | go.md §2 洩漏三典型 + profiling §1 |
| 加了 pool 反而更慢或更容易逾時 | worker 數超過下游容量，卡在排隊 | patterns §2 重定 worker 數 |
| 記憶體緩慢上漲最後 OOM | 某個 channel/queue 無界，或洩漏 | backpressure §1 補界限 |
| 每加一個 timeout/重試就冒新逾時 | timeout 層級沒對齊，內層 > 外層 | backpressure §3 重排預算 |
| 縮小臨界區後鎖競爭還在 | 鎖粒度錯（該分片沒分片） | profiling §3 修法優先序 |
| p99 尖峰但 CPU 沒滿 | 在等鎖/等下游/等排程，不是算得慢 | profiling 從 goroutine/block profile 重查 |
| 下游恢復後服務仍雪崩 | 重試風暴 / 沒熔斷 | backpressure §4 退避+jitter+熔斷 |

## references 索引

- `references/concurrency-patterns.md` — 何時「不要」開 goroutine、worker pool sizing、errgroup vs WaitGroup、pipeline/fan-out、semaphore 限並發、singleflight。決定併發結構前讀。
- `references/backpressure-limits.md` — 有界 channel 與滿了怎麼辦、rate limit 選型、timeout 預算層級、load shedding/circuit breaker 何時真需要、連線池 sizing。接邊界、設限流前讀。
- `references/performance-profiling.md` — pprof 排查順序、-race、鎖競爭修法優先序、GC/sync.Pool 判準、benchmark 正確姿勢。調效能前讀。
- `references/release-checklist.md` — 壓測、automaxprocs、ulimit、四金指標、graceful shutdown 排空、重試風暴防護。上高流量前逐條打勾。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
