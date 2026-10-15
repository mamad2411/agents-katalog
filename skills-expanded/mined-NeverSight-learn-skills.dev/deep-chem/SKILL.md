---
name: deep-chem
description: |
  化工 / 生物基材料 / 聚合物 / 生命科学产业的多维度深度研究 Claude Code Skill。
  覆盖学术文献、专利、市场数据、产能产量、产业链、标准法规与 AI 驱动材料发现。
  新增生命科学/生物制药/细胞基因治疗维度。Built on academic-search for CDP infrastructure.

  Chemical / Bio-Based Materials / Polymer / Life Sciences Industry Multi-Dimensional Deep Research.
  Covering academic literature, patents, market data, production capacity, supply chains,
  standards/regulations, and AI-driven materials discovery. Now with biopharma/CGT dimension.

  Mehrdimensionale Tiefenforschung für Chemie- / Biobasierte Materialien / Polymer- / Biowissenschaften.
  Deckt Literatur, Patente, Marktdaten, Produktionskapazitäten, Lieferketten, Normen
  und KI-gestützte Materialentdeckung ab. Jetzt mit Biopharma/CGT-Dimension.

  触发词 / Triggers / Auslöser:
  化工产业研究、生物基材料、聚合物市场、产能产量、产业链分析、
  材料专利、AI材料设计、技术路线、竞争格局、上市公司年报、
  生物制药、生物类似药、单抗、ADC、细胞基因治疗、CHO培养、CDMO
metadata:
  version: "0.2.0"
  depends-on: ["academic-search"]
---

# deep-chem

> **化工 / 生物基材料 / 聚合物 / 生命科学产业的多维度深度研究 Claude Code Skill**
>
> *Chemical / Bio-Based Materials / Polymer / Life Sciences Industry Multi-Dimensional Deep Research*
>
> *Mehrdimensionale Tiefenforschung für Chemie- / Biobasierte Materialien / Polymer- / Biowissenschaften*

---

基于 `academic-search` CDP 基础设施。超越文献——整合市场数据、专利、标准、产能产量、产业链与 AI 驱动材料发现。新增生物制药/CGT/生物工艺维度。

Built on `academic-search` for CDP infrastructure. Goes beyond literature — integrates market data, patents, standards, production capacity, supply chains, and AI-driven materials discovery. Now with biopharma / CGT / biologics dimension.

Auf `academic-search` für CDP-Infrastruktur aufgebaut. Geht über Literatur hinaus — integriert Marktdaten, Patente, Normen, Produktionskapazitäten, Lieferketten und KI-gestützte Materialentdeckung. Jetzt mit Biopharma / CGT / Biologics-Dimension.

---

## Preamble: Network Environment Detection / 网络环境检测 / Netzwerkumgebung

### 国内用户 / Users in China / Nutzer in China

| Source / 源 / Quelle | Access / 访问 / Zugang | Method / 方法 / Methode |
|--------|--------|--------|
| OpenAlex | ✅ 直连 / Direct / Direkt | `curl` REST API |
| CNKI 知网 | ✅ 直连 / Direct (NO VPN!) / Direkt (KEIN VPN!) | CDP browser |
| Google Scholar | ❌ 需 VPN / VPN required / VPN erforderlich | CDP + manual fallback |
| Overseas sites / 海外站 / Ausländische Seiten | ❌ 需 VPN / VPN required / VPN erforderlich | `curl --proxy socks5h://127.0.0.1:10808` |

**⚠️ CNKI 禁止 VPN / CNKI must NOT use VPN / CNKI darf KEIN VPN verwenden** — VPN triggers HTTP 418 anti-bot.

### 国际用户 / International Users / Internationale Nutzer

All sources directly accessible. / 所有源可直接访问。 / Alle Quellen direkt zugänglich.

---

## Quick Routing / 快速路由 / Schnellnavigation

```
用户需求 / User Request / Benutzeranfrage
├─ "最新论文" / "latest papers" / "neueste Arbeiten" → W1: OpenAlex
├─ "高引综述" / "high-citation reviews" / "Hochzitierte Übersichten" → W2: GS CDP (需VPN)
├─ "知网" / "CNKI" / "CNKI" → W3: CNKI CDP (禁止VPN!)
├─ "年报" / "annual report" / "Geschäftsbericht" → W4: PyMuPDF + W5b: Batch Scraping
├─ "市场" / "market" / "Markt" → W6: Industry Intel
├─ "专利" / "patents" / "Patente" → W7: Patent Search
├─ "AI+材料" / "AI+materials" / "KI+Materialien" → W8: AI + Materials
├─ "生物药" / "biopharma" / "Biopharma" → W1 → W4 → W6 → merge
│   ├─ 上游: CHO细胞培养 / 细胞系工程
│   ├─ 下游: 连续流纯化 / 病毒清除
│   ├─ AI: PINN混合建模 / 数字孪生
│   ├─ 分析: 糖基化 / 质量源于设计(QbD)
│   └─ 产业: CDMO格局 / 生物类似药
└─ "产业全景" / "industry panorama" / "Branchenpanorama" → ALL → merge
```

---

## Workflow W1: OpenAlex API Search

无 CDP / 无 API Key / 无速率限制。
No CDP required. No API key. No rate limit.
Kein CDP erforderlich. Kein API-Schlüssel. Keine Ratenbegrenzung.

```bash
curl -s "https://api.openalex.org/works?filter=title_and_abstract.search:KEYWORD,publication_year:2023-2026&sort=cited_by_count:desc&per_page=20&select=id,doi,title,publication_date,cited_by_count,authorships,open_access" \
  -H "User-Agent: deep-chem/0.2.0 (mailto:your@email.com)" \
  -o /tmp/oa_results.json
```

**Traps / 陷阱 / Fallen**: OA-01 (学术期刊限定 / only academic journals / nur akademische Zeitschriften), OA-02 (2022前覆盖稀疏 / pre-2022 sparse / vor 2022 lückenhaft), OA-03 (100k/天限制 / 100k/day limit / 100k/Tag-Limit)

---

## Workflow W2: Google Scholar CDP Search

需 CDP + VPN（国内用户）。中文引用提取见 [[scholar-chinese-citations]]。
Requires CDP + VPN (China users). See [[scholar-chinese-citations]] for Chinese citation regex.
Erfordert CDP + VPN (China-Nutzer). Siehe [[scholar-chinese-citations]] für chinesische Zitations-Regex.

```bash
PROXY="http://127.0.0.1:3456"
T=$(curl -s "$PROXY/new?url=https://scholar.google.com/scholar?q=KEYWORD&as_ylo=2023&hl=en" \
  | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).targetId")
sleep 3

curl -s -X POST "$PROXY/eval?target=$T" -d '
JSON.stringify(Array.from(document.querySelectorAll(".gs_r.gs_or.gs_scl")).map(el => ({
  allText: el.textContent.slice(0, 600)
})))' -o /tmp/gs_results.json

# Python解析 — 同时匹配 "Cited by X" 和 "被引用次数：X"
# Python parsing — matches both "Cited by X" and "被引用次数：X"
# Python-Parsing — erkennt sowohl "Cited by X" als auch "被引用次数：X"

curl -s "$PROXY/close?target=$T"
```

**Traps**: GS-01~04 (全角冒号 / full-width colon / vollbreiter Doppelpunkt, `<a>` 标签引用 / `<a>` tag citations / `<a>`-Tag-Zitate, JS filter 失效 / JS filter failure / JS-Filter-Versagen, VPN IP 被屏蔽 / VPN IP blocked / VPN-IP blockiert)

---

## Workflow W3: CNKI 知网 CDP Search

**⚠️ 禁止 VPN — 仅直连。** VPN triggers HTTP 418。
**⚠️ NO VPN — direct connection only.** VPN löst HTTP 418 aus.
**⚠️ KEIN VPN — nur Direktverbindung.** VPN löst HTTP 418 aus.

```bash
PROXY="http://127.0.0.1:3456"

# 1. HTTP 主页 (避免 SSL CNKI-01) / HTTP homepage (avoid SSL CNKI-01) / HTTP-Startseite (SSL CNKI-01 vermeiden)
CNKI=$(curl -s "$PROXY/new?url=http://www.cnki.net" \
  | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).targetId")
sleep 5

# 2. location.href 跳转 KNS8 (不用 /navigate — CNKI-02)
curl -s -X POST "$PROXY/eval?target=$CNKI" -d \
  'location.href = "https://kns.cnki.net/kns8s/defaultresult/index?korder=SU&kw=URL_ENCODED_KEYWORD"' > /dev/null
sleep 8

# 3. 提取 (KNS8 选择器, 2026-05 验证) / Extract (KNS8 selectors, validated 2026-05) / Extrahieren (KNS8-Selektoren, validiert 2026-05)
curl -s -X POST "$PROXY/eval?target=$CNKI" -d '
JSON.stringify({
  totalCount: document.querySelector("#countPageDiv .countText")?.textContent?.trim(),
  papers: Array.from(document.querySelectorAll(".result-table-list tbody tr")).map(tr => ({
    title:   tr.querySelector("td.name a")?.textContent?.trim(),
    authors: tr.querySelector("td.author")?.textContent?.trim(),
    source:  tr.querySelector("td.source a")?.textContent?.trim(),
    date:    tr.querySelector("td.date")?.textContent?.trim(),
    cites:   tr.querySelector("td.quote a")?.textContent?.trim()
  }))
})' -o /tmp/cnki_results.json

curl -s "$PROXY/close?target=$CNKI"
```

**⚠️ 翻页陷阱 / Pagination trap / Paginierungsfalle**: `.page-next` 可能返回第1页相同结果 (KNS8 bug, 2026-05)。

**Traps**: CNKI-01~08 (SSL, `/navigate`, CAPTCHA, URL编码, 10页限制, KNS8搜索框, 翻页失效, VPN触发418)

参考 / Reference / Referenz: [[cnki-kns8-selectors]]

---

## Workflow W4: PyMuPDF Industrial PDF Extraction

年报 / 专利全文提取。
Annual report / patent full-text extraction.
Geschäftsbericht / Patent-Volltextextraktion.

```python
import fitz, tempfile, os

doc = fitz.open("report.pdf")
out = os.path.join(tempfile.gettempdir(), 'pdf_output.txt')

with open(out, 'w', encoding='utf-8') as f:
    for i in range(len(doc)):
        f.write(f'\n===== PAGE {i+1} =====\n')
        f.write(doc[i].get_text())
        f.flush()  # 大PDF内存安全 / Memory safety / Speichersicherheit

doc.close()
# 绝不 print() 中文 — 始终写 UTF-8 文件 (PDF-01)
# NEVER print() Chinese — always write to UTF-8 file (PDF-01)
# NIEMALS print() für Chinesisch — immer in UTF-8-Datei schreiben (PDF-01)
```

**Traps**: PDF-01 (禁止print / no print / kein print), PDF-02 (年报无TOC / no TOC in reports / kein TOC in Berichten), PDF-03 (500+页OOM / 500+ page OOM / 500+ Seiten OOM)

参考 / Reference / Referenz: [[pymupdf-industrial]]

---

## Workflow W5: Multi-Source Merge & Dedup

三源去重合并。Three-source dedup & merge. Drei-Quellen-Deduplizierung.

详见 / See / Siehe: [[merge-dedup]]

---

## Workflow W5b: Annual Report Batch Scraping / 年报批量爬取

A股(巨潮) / 港股(披露易) / 美股(SEC EDGAR) 年报批量下载与分析。
Batch download & analysis of annual reports from A-share (CNinfo), HKEX, and SEC EDGAR.

**工具选型 / Tool Selection:**

| 市场 / Market | 首选工具 / Tool | 说明 / Note |
|------|----------|------|
| A股 / A-share | AKShare + 巨潮API | 全A股公告，含年报/半年报/季报 / All filings |
| 港股 / HKEX | ScrapeHKEX + Selenium | 披露易ESG报告 + 年报 / HKEX filings |
| 美股/中概股 / US/ADR | secedgar | SEC EDGAR 20-F/10-K 下载 |

**PyMuPDF 年报全文提取** → 见 / See / Siehe: [[pymupdf-industrial]]
**完整手册** → 见 / See / Siehe: [[annual-report-scraping]]

---

## Validated Scenarios / 已验证场景 / Validierte Szenarien

| # | 场景 / Scenario / Szenario | 维度 / Dimensions / Dimensionen | 数据量 / Data / Daten |
|---|------|------|:---:|
| 1 | **PA11/PA1010 长碳链生物基聚酰胺** 三源检索<br>*PA11/PA1010 long-chain bio-based polyamide three-source search*<br>*PA11/PA1010 langkettiges biobasiertes Polyamid Drei-Quellen-Recherche* | 文献/专利预判/产业链/产能<br>*Literature/patent forecast/supply chain/capacity*<br>*Literatur/Patentprognose/Lieferkette/Kapazität* | 50 篇<br>*50 papers*<br>*50 Arbeiten* |
| 2 | **华峰化学 241 页年报** PyMuPDF 全量提取<br>*Huafon Chemical 241-page annual report PyMuPDF full extraction*<br>*Huafon Chemical 241-Seiten Geschäftsbericht PyMuPDF-Extraktion* | 工业PDF/产能/财务/供应链<br>*Industrial PDF/capacity/finance/supply chain*<br>*Industrie-PDF/Kapazität/Finanzen/Lieferkette* | 458 KB 文本<br>*458 KB text*<br>*458 KB Text* |
| 3 | **RSC Lab on a Chip OA 论文** PyMuPDF (44c 连续流)<br>*RSC Lab on a Chip OA paper PyMuPDF (44c continuous-flow)*<br>*RSC Lab on a Chip OA-Papier PyMuPDF (44c kontinuierlich)* | 学术OA PDF/微流控纯化/智能下游<br>*Academic OA PDF/microfluidic purification/intelligent DSP*<br>*Akademische OA-PDF/Mikrofluidik/Intelligentes DSP* | 22 页, 4.1 MB<br>*22 pp, 4.1 MB*<br>*22 S, 4,1 MB* |
| 4 | **Frontiers CGT 4.0 OA 论文** PyMuPDF (4c)<br>*Frontiers CGT 4.0 OA paper PyMuPDF (4c)*<br>*Frontiers CGT 4.0 OA-Papier PyMuPDF (4c)* | 学术OA PDF/CGT/自动化传感器<br>*Academic OA PDF/CGT/automation sensors*<br>*Akademische OA-PDF/CGT/Automatisierungssensoren* | 6 页, 854 KB<br>*6 pp, 854 KB*<br>*6 S, 854 KB* |
| 5 | **PHA 聚羟基脂肪酸酯** 产业全景<br>*PHA polyhydroxyalkanoates industry panorama*<br>*PHA Polyhydroxyalkanoate Branchenpanorama* | 文献/市场/降解标准/产能/生态竞争<br>*Literature/market/degradation standards/capacity/ecosystem*<br>*Literatur/Markt/Abbaunormen/Kapazität/Ökosystem* | 85 篇命中<br>*85 hits*<br>*85 Treffer* |
| 6 | **AI + 聚合物材料设计** 交叉前沿<br>*AI + polymer materials design frontier*<br>*KI + Polymer-Materialdesign Grenzbereich* | 文献/ML方法/材料信息学/产业应用<br>*Literature/ML methods/materials informatics/industry*<br>*Literatur/ML-Methoden/Materialinformatik/Industrie* | 291 篇命中<br>*291 hits*<br>*291 Treffer* |
| 7 | **生物基材料产业全景** 三维交叉<br>*Bio-based materials industry panorama 3D cross-analysis*<br>*Biobasierte Materialien Branchenpanorama 3D-Kreuzanalyse* | 3方向×10维度综合<br>*3 directions × 10 dimensions*<br>*3 Richtungen × 10 Dimensionen* | 60 篇精选 + 产能 + 标准 + TRL<br>*60 papers + capacity + standards + TRL*<br>*60 Arbeiten + Kapazität + Normen + TRL* |
| 8 | **Google Scholar 中文引用提取**<br>*Google Scholar Chinese citation extraction*<br>*Google Scholar chinesische Zitationsextraktion* | "被引用次数：133" 正则<br>*"被引用次数：133" regex*<br>*„被引用次数：133" Regex* | 全角冒号 Regex<br>*Full-width colon Regex*<br>*Vollbreiter Doppelpunkt Regex* |
| 9 | **CNKI 无 VPN 直连 CDP**<br>*CNKI no-VPN direct CDP pipeline*<br>*CNKI Direktverbindung (ohne VPN) CDP-Pipeline* | KNS8 选择器 + SSL绕过 + 翻页<br>*KNS8 selectors + SSL bypass + pagination*<br>*KNS8-Selektoren + SSL-Umgehung + Paginierung* | 140 条命中<br>*140 hits*<br>*140 Treffer* |
| 10 | **Windows 11 UTF-8 编码根治**<br>*Windows 11 UTF-8 permanent fix*<br>*Windows 11 UTF-8 permanente Lösung* | Python / PowerShell / Git Bash<br>*Python / PowerShell / Git Bash*<br>*Python / PowerShell / Git Bash* | 永久修复<br>*Permanent fix*<br>*Permanente Lösung* |
| 11 | **生物制药产业全景** 上游+下游+AI+CDMO<br>*Biopharma industry panorama upstream+downstream+AI+CDMO*<br>*Biopharma Branchenpanorama Upstream+Downstream+AI+CDMO* | 文献/工艺/AI/糖基化/竞争格局/交叉材料<br>*Literature/process/AI/glycosylation/competitive landscape/cross-materials*<br>*Literatur/Prozess/AI/Glykosylierung/Wettbewerb/Cross-Materialien* | 41 篇命中 / TOP 15<br>*41 hits / TOP 15*<br>*41 Treffer / TOP 15* |
| 12 | **WuXi Biologics 263页年报** PyMuPDF提取<br>*WuXi Biologics 263pp annual report PyMuPDF*<br>*WuXi Biologics 263 S. Geschäftsbericht PyMuPDF* | 工业PDF / 产能 / 财务 / CDMO格局<br>*Industrial PDF / capacity / finance / CDMO landscape*<br>*Industrie-PDF / Kapazität / Finanzen / CDMO-Landschaft* | 5年财务表<br>*5-year financial tables*<br>*5-Jahres-Finanztabellen* |
| 13 | **Samsung Biologics 财务验证**<br>*Samsung Biologics financial verification*<br>*Samsung Biologics Finanzverifizierung* | 跨市场年报(港/韩) + Wikipedia<br>*Cross-market reports (HKEX/KRX) + Wikipedia*<br>*Marktübergreifende Berichte (HKEX/KRX) + Wikipedia* | 2023-2024 营收/利润<br>*2023-2024 revenue/profit*<br>*2023-2024 Umsatz/Gewinn* |

### 四方向验证详情 / Four-Direction Validation Details / Details der vier Richtungen

```
方向1 / Direction 1 / Richtung 1: PA11 生物基聚酰胺 / Bio-Based Polyamide / Biobasiertes Polyamid
  ├─ OpenAlex: 27 hits → 20 篇 (2023-2026) / 20 papers / 20 Arbeiten
  ├─ Google Scholar CDP: 10 篇 (跨年代经典, 最高133c) / 10 papers (cross-decade, top 133c) / 10 Arbeiten (epochenübergreifend, max. 133c)
  ├─ CNKI CDP: 140 hits → 20 篇 (学位论文+中文期刊) / 20 papers (theses+CN journals) / 20 Arbeiten (Dissertationen+CN-Zeitschriften)
  └─ 合并 / Merged / Zusammengeführt: 50 篇唯一文献 / 50 unique papers / 50 eindeutige Arbeiten

方向2 / Direction 2 / Richtung 2: PHA 聚羟基脂肪酸酯 / Polyhydroxyalkanoates / Polyhydroxyalkanoate
  ├─ OpenAlex: 85 hits → 15 篇 TOP / 15 top papers / 15 Top-Arbeiten
  ├─ 方向 / Directions / Richtungen: 微生物生产 / 提取工艺 / 生物复合 / 食品包装 / 海洋降解
  │   Microbial production / extraction / biocomposites / food packaging / marine degradation
  │   Mikrobielle Produktion / Extraktion / Biokomposite / Lebensmittelverpackung / Meeresabbau
  └─ 产能 / Capacity / Kapazität: Danimer ~3万吨/年, 宁波天安 ~2万吨/年, 微构工场 ~1万吨/年

方向3 / Direction 3 / Richtung 3: AI + 聚合物材料 / AI + Polymer Materials / KI + Polymerwerkstoffe
  ├─ OpenAlex ×2: 269+22 hits → 25 篇 TOP / 25 top papers / 25 Top-Arbeiten
  ├─ 方向 / Directions / Richtungen: 复合材料ML / 膜设计ML / 高分子逆向设计 / 聚合物信息学
  │   Composite ML / membrane design ML / polymer inverse design / polymer informatics
  │   Verbundwerkstoff-ML / Membrandesign-ML / Polymer-Inversdesign / Polymerinformatik
  └─ 代表 / Representatives / Vertreter: BASF/Dow/3M 自建AI材料平台 / in-house AI materials platforms / eigene KI-Materialplattformen

方向4 / Direction 4 / Richtung 4: 生物制药 / 生物工艺 / Biopharma / Bioprocess / Biopharma / Bioprozess
  ├─ OpenAlex: 41 hits → 15 篇 TOP (2023-2025) / 15 top papers / 15 Top-Arbeiten
  ├─ 上游 / Upstream / Upstream: CHO细胞建模(9c) / 凋亡自噬调控 / 培养基数据库(MediaAssist)
  │   CHO cell modeling / apoptosis-autophagy regulation / MediaAssist culture medium DB
  │   CHO-Zellmodellierung / Apoptose-Autophagie-Regulation / MediaAssist-Kulturmedium-DB
  ├─ 下游 / Downstream / Downstream: 微流控连续流(44c) / 病毒过滤(Planova) / CRISPR支原体检测
  │   Microfluidic continuous-flow / virus filtration (Planova) / CRISPR mycoplasma detection
  │   Mikrofluidischer kontinuierlicher Fluss / Virenfiltration (Planova) / CRISPR-Mykoplasmen-Nachweis
  ├─ AI: PINN混合建模(13c) / CGT 4.0(4c) / 深度学习SERS监测
  │   PINN hybrid modeling / CGT 4.0 / deep learning SERS monitoring
  │   PINN-Hybridmodellierung / CGT 4.0 / Deep-Learning-SERS-Überwachung
  ├─ 分析 / Analytics / Analytik: N-糖基化制备技术(13c) — 生物类似药一致性关键
  │   N-glycan preparation techniques — biosimilar comparability key
  │   N-Glykan-Präparationstechniken — Biosimilar-Vergleichbarkeit Schlüssel
  └─ 产业 / Industry / Industrie: 全球CDMO ~$200B, Lonza/WuXi/Samsung主导, ADC最热赛道
      Global CDMO ~$200B, Lonza/WuXi/Samsung lead, ADC hottest track
      Globales CDMO ~$200B, Lonza/WuXi/Samsung führend, ADC heißeste Spur
```

---

## Traps Quick-Ref / 陷阱速查 / Fallen-Schnellreferenz

共 **30** 个已知陷阱 (7类)。
**30** cataloged traps across 7 categories.
**30** katalogisierte Fallen in 7 Kategorien.

| # | 陷阱 / Trap / Falle | 影响 / Impact / Auswirkung |
|---|------|--------|
| 1 | `print()` 中文 → 崩溃 / crash / Absturz | 所有 Python 工作流 |
| 2 | PS 5.1 而非 7+ | `[建议]` 解析为数组操作符 |
| 3 | CNKI + VPN → HTTP 418 | CNKI 完全封锁 |
| 4 | CDP `/navigate` 用于 CNKI | URL 参数被截断 |
| 5 | GS 引用 Regex 无全角冒号 | 丢失所有中文界面结果 |
| 6 | CNKI `.page-next` 失效 | 翻页静默失败 |
| 7 | Google Scholar 无 VPN (国内) | 网站不可达 |

完整目录 / Full catalog / Vollständiger Katalog: [[traps-catalog]]

---

## 覆盖维度 / Dimensions Covered / Abgedeckte Dimensionen

| 维度 / Dimension | 工具/源 / Tools/Sources / Werkzeuge/Quellen |
|------|------|
| 📚 文献 / Literature / Literatur | OpenAlex + Google Scholar + CNKI (三源合并) |
| 📄 工业PDF / Industrial PDFs / Industrielle PDFs | PyMuPDF (年报/专利) |
| 🏭 市场/产能 / Market/Capacity / Markt/Kapazität | defuddle + WebSearch + CNKI |
| 🔬 专利 / Patents / Patente | Google Patents + CNKI 专利库 |
| 📏 标准/法规 / Standards / Normen | GB/T, ISO, EU, 中国限塑令, FDA/EMA |
| 🔗 产业链 / Supply Chain / Lieferkette | 研报 + 行业协会 + 年报 |
| 🤖 AI+材料 / AI+Materials / KI+Materialien | OpenAlex + GS (ML材料设计) |
| 🧬 生物制药 / Biopharma / Biopharma | OpenAlex + GS + CNKI (CHO/纯化/AI/CGT/CDMO) |

---

## Reference Files / 参考文档 / Referenzdokumente

| 文件 / File / Datei | 内容 / Content / Inhalt |
|------|------|
| [[traps-catalog]] | 30个已知陷阱 (7类) / 30 traps / 30 Fallen |
| [[cnki-kns8-selectors]] | CNKI KNS8 DOM 选择器 / selectors / Selektoren |
| [[scholar-chinese-citations]] | GS 中文引用提取 / Chinese citation extraction / Chinesische Zitationsextraktion |
| [[windows-utf8-fix]] | Windows UTF-8 根治 / permanent fix / permanente Lösung |
| [[pymupdf-industrial]] | PyMuPDF 工业 PDF 指南 / industrial PDF guide / Industrie-PDF-Anleitung |
| [[merge-dedup]] | 多源去重合并 / multi-source dedup / Multi-Quellen-Deduplizierung |
| [[annual-report-scraping]] | 上市公司报告爬取 (A股/港股/美股) / Annual report scraping / Geschäftsbericht-Scraping |

---

*deep-chem v0.2.0 · Built on academic-search · Validated on Windows 11*
*化工 / 生物基材料 / 聚合物 / 生命科学产业 · Chemical / Bio-Based / Polymer / Life Sciences Industry · Chemie / Biobasierte Materialien / Polymer- / Biowissenschaften*
