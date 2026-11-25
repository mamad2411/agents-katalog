---
name: second-opinion
description: "Buyuk kararlar icin paralel fork + blank subagent calistir, cevaplari karsilastir. Triggers: second opinion, ikinci gorus, fork karsilastir, convergence check, fork vs fresh."
argument-hint: "[karar sorusu / karsilastirma konusu]"
---

# /second-opinion — Fork vs Fresh Convergence Check

Kritik karar anlarinda (mimari, refactor kapsami, riskli degisiklik) ayni soruyu iki farkli baglam uzerinden sor: bir **fork** (ana session nuansini tasir) ve bir **blank subagent** (on yargisiz bakis). Iki cevabi karsilastir, converge/diverge noktalarini cikar.

## Ne zaman kullan

- Geri donusu zor mimari karar (DB secimi, monorepo vs multi, state mgmt)
- Buyuk refactor kapsam / sirası / break points
- Trade-off analizi (hiz vs dogruluk, maliyet vs esneklik)
- Strateji degisikligi (build vs buy, pivot, kill feature)

Kucuk kararlar icin kullanma — dispatch veya direkt yanit yeterli.

## Fork vs Blank tradeoff

Detay icin bkz: `dispatch` skill → "Fork vs Normal Subagent Decision". Ozet:

| Fork gucu | Blank gucu |
|-----------|-----------|
| Tum session nuansini bilir, tekrar anlatmaya gerek yok | On yargisiz, temiz bakis |
| Mid-session constraint'leri hatirlar | Author biasi sizmaz |
| Cache hit yuksek, hizli | Baseline "disaridan gelsem ne derdim" |

Ikisinin kesisimi = yuksek guven. Divergence = dikkat cekici sinyal.

## Pre-flight

- `CLAUDE_CODE_ENABLE_FORK_SUBAGENT=1` set olmali (Phase 1'de yapildi)
- Env eksikse: **fallback** — iki blank subagent calistir ve cikti basinda WARNING yaz: `WARNING: fork env missing, ran 2x blank subagents (reduced nuance).`

## Akis

### 1. Soru hazirlama

Kullanicidan gelen karar konusunu **tek bir net soruya** indirge. Ornek: "Auth icin Firebase mi custom JWT mi? Musteri B2B SaaS, 3 kisilik ekip, 6 ay runway."

### 2. Paralel dispatch

Agent tool'u **ayni mesajda iki kez** cagir — biri fork, biri blank. Her ikisine ayni prompt:

```
QUESTION: {tek satir karar sorusu}
CONTEXT: {2-5 satir somut kisit: ekip, tech stack, deadline, budget}

OUTPUT FORMAT:
1. Recommendation: {secim, 1 satir}
2. Reasoning: {3-5 madde}
3. Risks: {2-3 madde}
4. Confidence: {low|medium|high}
```

Fork subagent icin ek satir: `MODE: fork (you inherit parent session nuance).`
Blank subagent icin ek satir: `MODE: fresh (no prior context, evaluate from scratch).`

### 3. Rapor formati

Iki cevap gelince ana session bu 3 bolumlu raporu uret:

```
## Fork view (nuanced)
- Recommendation: ...
- Key reasoning: ...
- Risks: ...
- Confidence: ...

## Fresh view (unbiased)
- Recommendation: ...
- Key reasoning: ...
- Risks: ...
- Confidence: ...

## Synthesis
- Agreement: {iki cevabin ortustugu noktalar}
- Divergence: {ayristigi noktalar + muhtemel sebep: "fork session bagimli / fresh sinirli bilgi"}
- Jarvis recommendation: {tek satir, gerekce 1-2 cumle}
```

## Ornek kullanimlar

1. **Mimari karar:** "ClaudeHQ session persistence icin SQLite mi JSON dosyalari mi?" → fork (mevcut ekosistemi bilir) + fresh (generic best-practice) → synthesize.
2. **Refactor kapsami:** "Forge skill'i 500 satir, parcalayayim mi yoksa in-place mi?" → fork (neden buyudugunu bilir) + fresh (ideal seperation of concerns).
3. **Trade-off:** "Yeni freemium tier'a Groq mu HF Inference mi koyalim?" → fork (quota gecmisini, maliyetleri bilir) + fresh (pure tech kiyas).

## Kurallar

- Max 4 tool call (2 dispatch + rapor olustur)
- Ayni sorunun iki cevabini **yan yana** goster, birinin iceride digerini ezmesine izin verme
- Divergence varsa kullaniciya sor — otomatik olarak fork'u tercih etme
- Review/security review icin ASLA fork kullanma (bkz dispatch skill hard guard)

## When NOT to Use
- Trivial karar (1-10 satir kod, config degisikligi)
- Cevap objektif olarak bellidir (spec okumak yeter)
- Subagent token butcesi dusuk → tek blank dispatch yeterli

## Red Flags
- Iki cevap birebir ayni → prompt cok kisitli, yeniden sor
- Iki cevap da "bilmiyorum/depends" dedi → soruyu somutlastir
- Fork cevabi sadece onceki session'i tekrar ediyor → blank'a daha fazla context ver

## Error Handling
- Fork env eksik → 2x blank fallback + WARNING banner
- Subagent'lardan biri timeout → tek cevabi goster, diger icin retry
- Divergence > agreement → kullaniciya karar birak, Jarvis secmesin

## Verification
- [ ] Iki ayri cevap alindi
- [ ] 3 bolumlu rapor uretildi (fork / fresh / synthesis)
- [ ] Agreement ve divergence acikca yazildi
- [ ] Fork env durumu belirtildi (enabled / fallback)
