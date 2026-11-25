---
name: agent-refine
description: "Agent sistemini proje bazli refine et — eksik agent tespit, genis olanları böl, yeni agent tanimla, registry guncelle. Triggers: agent-refine, agent refine, agent ekle, agent bol, agent eksik."
argument-hint: "[analiz | split <agent-id> | create <name>]"
---

# /agent-refine — Agent System Refinement

Proje sirasinda agent sistemi eksikliklerini tespit edip otomatik duzeltir.

## Modlar

### 1. Analiz modu (varsayilan)

```
/agent-refine
```

Mevcut projeyi tara, agent-registry.json ile karsilastir:
- Projede kullanilan teknolojiler neler? (pubspec.yaml, package.json, vb.)
- Hangi capability'ler gerekiyor?
- Mevcut agent'lardan hangisi uygun, hangisi eksik?
- Uygun agent var ama kapsamı cok genis mi?

Cikti:
```
## Agent Analiz Raporu — [proje adi]

### Uygun agent'lar
- B15 Mobile Dev (Flutter + Dart uyumlu)
- B5 Database Agent (Firestore)

### Eksik capability'ler
- "stripe-payment" — hicbir agent'ta yok
  Oneri: B4 API Integrator'a "stripe" capability ekle
  VEYA yeni agent: B22 Payment Agent

### Cok genis kapsamli agent'lar
- B2 Backend Coder: 6 capability, 3 dil — REST + GraphQL + migration + dto ayri olabilir
  Oneri: simdilik birak, kullanim arttikca bol
```

### 2. Split modu

```
/agent-refine split B2
```

Belirtilen agent'in capability'lerini analiz et, mantikli alt gruplara bol:
1. Agent .md dosyasini oku
2. Capability cluster'larini belirle
3. Yeni agent .md'ler olustur
4. Registry'yi guncelle
5. Eski agent'in capability'lerini daralt

### 3. Create modu

```
/agent-refine create "Payment Agent"
```

Yeni agent olustur:
1. Uygun ID ata (kategori prefix + siradaki numara)
2. Agent .md dosyasi yaz (template'den)
3. Registry'ye ekle (status: pool)
4. agents/README.md'yi guncelle
5. CLAUDE.md §11 sayilari guncelle

## Kurallar

- Degisikliklerden once mevcut durumu rapor et
- Her yeni/split agent `status: pool` olarak baslar
- Registry JSON ve .md dosyasi senkron olmali — `sync_agents.py --check` calistir
- Git commit olustur: `feat: agent-refine — [ne yapildi]`
- GitHub repo'lari da guncelle (marketplace README agent sayilari)
- Max 15 tool call

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
