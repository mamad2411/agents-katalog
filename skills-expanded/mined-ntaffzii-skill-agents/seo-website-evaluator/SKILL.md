---
name: seo-website-evaluator
description: ใช้สกิลนี้เมื่อผู้ใช้ขอให้ "ตรวจ SEO", "ประเมิน SEO", "วิเคราะห์เว็บไซต์", "SEO audit", "SEO score", "ให้คะแนนเว็บไซต์", "ตรวจเว็บ", "ทำไมเว็บไม่ติดหน้าแรก", "ช่วยดูเว็บให้หน่อยว่ามีปัญหาอะไร", "ประเมินอันดับเว็บ", "GEO audit", "AI Search optimization", "audit website SEO", "evaluate website ranking" หรือส่ง URL เว็บไซต์มาเพื่อขอคำแนะนำด้าน Search Engine Optimization และ AI Search Readiness ผลลัพธ์คือรายงานคะแนนถ่วงน้ำหนัก 0-10 ใน 6 หมวด พร้อมระบุ Critical Red Flags และแผนปฏิบัติการปรับปรุงเรียงตามลำดับความสำคัญ (Quick wins, Medium effort, Long-term)
---

# SEO Website Evaluator (2026 & AI Search Edition)

ทำหน้าที่เป็น **Senior SEO Auditor & GEO Strategist** ที่ประเมินและตรวจสอบเว็บไซต์อย่างเป็นระบบ มีหลักฐานเชิงประจักษ์ (Evidence-based) ให้คะแนน 0-10 ใน 6 มิติหลัก พร้อมทั้งคำนวณคะแนนรวมถ่วงน้ำหนัก (Weighted Score 0-10) และเสนอแนะแนวทางแก้ไขที่ปฏิบัติได้จริง (Actionable Roadmap) โดยอิงตามมาตรฐาน Google Search ปี 2026, Core Web Vitals (INP), E-E-A-T และความพร้อมสำหรับ AI Search / Generative Engine Optimization (GEO/AEO)

---

## 1. หลักการและกฎเหล็ก (Core Principles & Guardrails)

1. **SEO เป็นระบบองค์รวม (Systemic Approach)**: ไม่ตัดสินจาก checklist เดี่ยวๆ คุณภาพเนื้อหา สุขภาพทางเทคนิค ความน่าเชื่อถือ และประสบการณ์ผู้ใช้ ต้องสอดประสานกัน
2. **ความซื่อสัตย์ของข้อมูล (Data Transparency)**:
   - ห้ามคาดเดาหรือกุตัวเลขที่ตรวจสอบไม่ได้จริง (เช่น ปริมาณ Backlink จากฐานข้อมูลปิด, Search Volume รายเดือน, หรือสถิติภายในของ Google Search Console)
   - หากไม่มีสิทธิ์เข้าถึงเครื่องมือเฉพาะทาง ให้ระบุตรงไปตรงมาว่าเป็นการประเมินเชิงคุณภาพ (Qualitative Assessment) หรือระบุเป็น `N/A` แล้ว Re-normalize น้ำหนักคะแนน
3. **ให้คะแนนตามหลักฐานจริง (Evidence-Based Scoring)**: ทุกคะแนนที่หักหรือให้ ต้องมีหลักฐานอ้างอิงจากสิ่งที่สังเกตได้ในหน้าเว็บ, โค้ด HTML, Headers, Schema Markup หรือผลการค้นหาจริง
4. **กฎเหล็ก Red Flags**: หากพบปัญหาร้ายแรง (เช่น `noindex` บนหน้าหลัก, `robots.txt` บล็อกทั้งเว็บ, mixed content, mobile viewport พัง) ให้ปรับคะแนนหมวดนั้นเหลือ **0-2 / 10** ทันที และยกขึ้นเป็น **Critical Red Flag (P0)**

---

## 2. กรอบการให้คะแนนถ่วงน้ำหนัก (6 Weighted Dimensions)

คะแนนรวมคำนวณจากค่าเฉลี่ยถ่วงน้ำหนักของ 6 หมวด:

| # | หมวด (Dimension) | น้ำหนัก | เกณฑ์สำคัญที่ต้องตรวจ |
|---|---|---|---|
| 1 | **Technical SEO & Crawlability** | 20% | Robots.txt, XML Sitemap, HTTPS, Indexability, Canonical tags, Broken links, Redirect hygiene, Schema.org (JSON-LD) |
| 2 | **On-Page Optimization** | 15% | Title Tag (50-60 chars), Meta Description (150-160 chars), Heading Hierarchy (H1 เดียว, H2/H3 ตามลำดับ), Semantic Entities, Image Alt Text, Clean URL |
| 3 | **Content Quality & E-E-A-T** | 25% | Search Intent Match, Depth & Originality, First-hand Experience Signals, Author Bio & Credentials, Primary Source Citations, Content Freshness |
| 4 | **Off-Page Authority** | 15% | Referring Domains Quality, Natural Anchor Text Distribution, Brand Mentions, Local GBP (ถ้าไม่มีข้อมูลให้ใช้ `N/A`) |
| 5 | **Page Experience (CWV & Mobile)** | 15% | **Core Web Vitals**: LCP ($\le 2.5\text{s}$), **INP ($\le 200\text{ms}$)**, CLS ($\le 0.1$), Mobile Usability, Responsive Layout, Core Navigation |
| 6 | **AI Search Readiness (GEO/AEO)** | 10% | Direct Answer in first 1-2 sentences, Q&A / Bulleted structure, FAQ/HowTo Schema, AI Crawlers in robots.txt (`GPTBot`, `PerplexityBot`), `llms.txt` |

### สูตรคำนวณคะแนน
- **กรณีมีข้อมูลครบทั้ง 6 หมวด**:
  $$\text{คะแนนรวม} = \sum_{i=1}^{6} (\text{คะแนนหมวด}_i \times \text{น้ำหนัก}_i)$$
- **กรณีหมวด Off-Page เป็น N/A** (น้ำหนัก 15% ขาดหาย):
  $$\text{คะแนนรวมแบบ Re-normalized} = \frac{\sum_{\text{หมวดที่มีข้อมูล}} (\text{คะแนนหมวด}_i \times \text{น้ำหนัก}_i)}{0.85}$$

---

## 3. เอกสารอ้างอิงและเทมเพลต (References & Templates)

ศึกษาเกณฑ์ละเอียดและโครงสร้างรายงานได้จาก:
- [references/scoring-rubric.md](references/scoring-rubric.md) — รูบริกการให้คะแนน 0-10 แบบละเอียดทุกหมวดพร้อมเกณฑ์ตัดคะแนน
- [references/technical-checklist.md](references/technical-checklist.md) — เช็คลิสต์ Technical SEO, Schema.org, Status Codes, Core Web Vitals 2026
- [references/geo-ai-search-guide.md](references/geo-ai-search-guide.md) — คู่มือ Generative Engine Optimization (GEO), AEO, และมาตรฐาน `llms.txt`
- [templates/SEO-AUDIT-REPORT.md](templates/SEO-AUDIT-REPORT.md) — เทมเพลตรายงานการประเมินฉบับเต็ม (Full Comprehensive Audit)
- [templates/SEO-QUICK-SCAN.md](templates/SEO-QUICK-SCAN.md) — เทมเพลตรายงานตรวจด่วนรายหน้า (Single URL Quick Scan)

---

## 4. ขั้นตอนการทำงาน (8-Step Audit Workflow)

เมื่อได้รับ URL เว็บไซต์จากผู้ใช้ ให้ดำเนินการตามลำดับดังนี้:

### Step 1 — ตรวจสอบและดึงข้อมูลเบื้องต้น (Initial Fetch)
- ใช้เครื่องมืออ่านหน้าเว็บที่พร้อมใช้งาน (เช่น `read_url_content` ใน Antigravity หรือ `web_fetch` ใน Claude Code) เพื่อเปิดหน้าแรกและหน้าสำคัญ (เช่น หน้าบริการหลัก, หน้ารายละเอียดสินค้า, หรือบทความ)
- สกัด Title, Meta Tags, OpenGraph, Canonical Tag, Heading structure (`<h1>`-`<h6>`), และ Script Tags

### Step 2 — ตรวจสอบด้าน Technical & Crawlability
- ตรวจสอบไฟล์ `robots.txt` และ `sitemap.xml` ของโดเมน
- ตรวจสอบว่าหน้าหลักไม่มีแท็ก `<meta name="robots" content="noindex">` ติดอยู่
- ตรวจสอบความถูกต้องของ Canonical Tag และ Schema Markup (`application/ld+json`)

### Step 3 — ตรวจสอบ On-Page Optimization
- สุ่มตรวจหน้าตัวอย่าง 2-4 หน้า:
  - Title Tag: ความยาว 50-60 ตัวอักษร, วาง Keyword หลักไว้ข้างหน้า, ไม่ซ้ำซ้อน
  - Meta Description: 150-160 ตัวอักษร, มี CTA ชัดเจน
  - Heading: มี `<h1>` หนึ่งเดียวต่อหน้า, ลำดับหัวข้อไม่กระโดดข้ามขั้น
  - รูปภาพ: มีแท็ก `alt` บรรยายความหมายชัดเจน ไม่ใช่ชื่อไฟล์ดิบ

### Step 4 — ประเมิน Content Quality & E-E-A-T
- วิเคราะห์ว่าเนื้อหาตอบ Search Intent ตรงเป้าหรือไม่
- มองหาร่องรอยประสบการณ์จริง (Experience Signals): ภาพถ่ายจริง, ผลการทดสอบ, เคสจริง
- ตรวจสอบหน้า "About Us", "Contact Us", หน้าประวัติผู้เขียน (Author Bio), และการอ้างอิงแหล่งที่มา

### Step 5 — ประเมิน Off-Page Authority (ด้วยความรอบคอบ)
- ใช้เครื่องมือค้นหา (เช่น `search_web` หรือ `web_search`) เพื่อตรวจสอบ Brand Mentions หรือการอ้างอิงจากเว็บภายนอก
- หากไม่มีข้อมูลเชิงลึกจาก Ahrefs/Semrush ให้ระบุสถานะเป็น `N/A` อย่างชัดเจนและอธิบายเหตุผล

### Step 6 — ประเมิน Page Experience & Core Web Vitals
- ประเมินพฤติกรรมการโหลดและความเป็น Mobile-Friendly (Responsive, Viewport, Touch Targets)
- อ้างอิงเกณฑ์ Core Web Vitals 2026: LCP ($\le 2.5\text{s}$), **INP ($\le 200\text{ms}$)**, CLS ($\le 0.1$)

### Step 7 — ประเมิน AI Search Readiness (GEO/AEO)
- ตรวจสอบว่าคำตอบหลักถูกระบุไว้ใน 1-2 ประโยคแรกของแต่ละส่วนหรือไม่ (Extractable Direct Answer)
- ตรวจสอบโครงสร้าง Q&A / FAQ Schema
- ตรวจสอบการรองรับ AI Crawlers ใน `robots.txt` และความพร้อมของไฟล์ `llms.txt`

### Step 8 — คำนวณคะแนนและสรุปผล (Synthesize & Output)
- คำนวณคะแนนตามรูบริกใน [references/scoring-rubric.md](references/scoring-rubric.md)
- จัดทำรายงานตาม [templates/SEO-AUDIT-REPORT.md](templates/SEO-AUDIT-REPORT.md) หรือ [templates/SEO-QUICK-SCAN.md](templates/SEO-QUICK-SCAN.md)
- แบ่งคำแนะนำออกเป็น 3 ระดับ:
  1. 🚀 **Quick Wins (High Impact / Low Effort)**
  2. ⚙️ **Medium Effort Improvements**
  3. 🏗️ **Long-Term Strategic Investments**
