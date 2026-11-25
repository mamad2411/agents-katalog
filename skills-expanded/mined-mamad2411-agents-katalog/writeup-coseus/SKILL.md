<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-coseus
description: CTF writeups and security challenges by coseus.
---

# Writeups by coseus

Source repository: `/repos/coseus`

## Repository Index

- PentestReportTemplate/README.md
- ReportTemplate/README.md

## Writeup Content


### File: PentestReportTemplate/README.md

### Modern, Automated, Enterprise-Grade Reporting for Offensive Security

## 📌 Overview

**Pentest Report Generator – Corporate Edition** este o aplicație completă, extensibilă și modernă pentru generarea de rapoarte profesionale de penetration testing (PDF & DOCX), cu suport pentru:

- Import automat din **Nessus**, **OpenVAS**, **Nmap**, **CSV**, **JSON**
- Editare avansată a finding-urilor, cu **evidence images + code blocks**
- Structură corporată (Deloitte / KPMG style)
- Export PDF cu:
    - **Cover corporate**
    - **Header de pagină cu logo**
    - **Watermark opțional CONFIDENTIAL**
    - **Table of Contents automat**
    - **Findings numerotate 6.1, 6.2…**
    - **Additional reports & scans**
    - **Per-host vulnerability heatmap**
    - **Badges colorate (Critical / High / etc)**

Aplicația folosește **Streamlit** în front-end și **ReportLab** pentru generarea PDF-urilor enterprise-grade.

---

## ✨ Features

### 🔍 Import Findings

- Import automat cu parsing avansat din:
    - ✓ Nessus (.nessus XML)
    - ✓ OpenVAS / Greenbone XML
    - ✓ Nmap XML
    - ✓ CSV custom
    - ✓ JSON custom
- Auto-mapping pentru:
    - Severity
    - Title
    - Host
    - CVSS
    - CVE
    - Description / Impact / Recommendation

### 📝 Findings Editor (Advanced)

- Editare completă pentru fiecare finding
- Adăugare / ștergere **imagini (B64)** cu resize automat
- Code blocks formatate
- Deduplicare imagini
- Filtrare după severitate
- Renumbering automat 6.1, 6.2 …

### 🧩 Additional Reports

- Titlu + Description + Code + Evidențe (imagini)
- Apărute în PDF sub capitolul 7.0

### 📄 Export PDF & DOCX

- Cover corporate
- Watermark CONFIDENTIAL (opțional)
- TOC automat
- Formatting avansat (multiline, indentare exactă)
- Vulnerability Summary (with badges + totals)
- Per-host summary grid
- Technical Findings full-corporate
- Additional Reports corporate layout

---

## 📂 Project Structure

```
pentest_report/
│
├── app.py
├── run.py
├── setup_paths.py
│
├── ui/
│   ├── general_info.py
│   ├── scope_tab.py
│   ├── findings_tab.py
│   ├── additional_reports.py
│   ├── executive_summary_tab.py
│   └── export_tab.py
│
├── report/
│   ├── pdf_generator.py
│   ├── docx_generator.py
│   ├── parsers.py
│   ├── data_model.py
│   ├── numbering.py
│   ├── utils.py
│   └── sections/
│       ├── section_1_0_confidentiality_and_legal.py
│       ├── section_1_1_confidentiality_statement.py
│       ├── section_1_2_disclaimer.py
│       ├── section_1_3_contact_information.py
│       ├── section_2_0_assessment_overview.py
│       ├── section_2_1_assessment_details.py
│       ├── section_2_2_scope.py
│       ├── section_2_3_scope_exclusions.py
│       ├── section_2_4_client_allowances.py
│       ├── section_3_0_finding_severity_ratings.py
│       ├── section_4_0_technical_findings.py
│       ├── section_4_1_additional_reports.py
│       ├── section_5_0_executive_summary.py
│       └── section_5_1_vulnerability_summary.py
│
└── util/
    ├── helpers.py
    └── io_manager.py

```

---

## 🚀 Installation

### 1. Clone the repository

```
git clone https://github.com/<username>/pentest-report-generator
cd pentest-report-generator

```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate

```

### 3. Install dependencies

```
pip install -r requirements.txt

```

---

## ▶️ Running the Application

```
streamlit run app.py

```

## 🖼️ Screenshots

<img width="1370" height="1220" alt="image" src="https://github.com/user-attachments/assets/969d93d2-0fd9-4f5b-abae-c58fc7dce593" />
<img width="1394" height="1115" alt="image 1" src="https://github.com/user-attachments/assets/a368fdce-70c1-4816-a6ef-0d27c48d0939" />
<img width="1470" height="1783" alt="image 2" src="https://github.com/user-attachments/assets/9298096b-bb9c-4dcf-81a8-5275bfa75292" />
<img width="1483" height="948" alt="image 3" src="https://github.com/user-attachments/assets/20bdcdbc-7f93-4809-bd16-bcc1ffc5f253" />
<img width="1542" height="855" alt="image 4" src="https://github.com/user-attachments/assets/8fed0b9b-a948-468e-a3e4-40580570fb20" />
<img width="1540" height="1180" alt="image 5" src="https://github.com/user-attachments/assets/e5009fa5-527f-4812-ac08-d042e3e9cb36" />




### File: ReportTemplate/README.md

# README

**DEZVOLTAREA UNEI APLICAȚII WEB PENTRU GENERAREA AUTOMATĂ A RAPOARTELOR DE PENTEST CU SUPORT PENTRU IMPORT/EXPORT JSON ȘI GENERARE PDF CONFORM STANDARDULUI ISO/IEC 27001**

---

STRUCTURA COMPLETĂ

```bash
pentest_report/
│
├── main.py                
├── requirements.txt
├── run.bat
├── run.sh
├── assets/
│   	├── logo.png
│   	├── cover_logo.png
│   	├── fonts/
│   			├── DejaVuSans-Bold.ttf
│   			├── DejaVuSans-BoldOblique.ttf
├──components/
│   	├── __pycache__
│   	├── legal.py
│   	├── export.py
│   	├── general.py
│   	├── poc.py
│   	├── severity.py
│   	├── scope.py
│   	├── executive.py
│   	├── findings.py
│   	└── methodology_screen.py
│
├── mailer/
│   	├── __pycache__
│   	└── send.py    
│
├── parsers/
│   	├── __pycache__
│   	├── __init__.py
│   	├── nessus.py
│   	├── nmap.py
│   	├── sections/
│   			├── __pycache__
│   			├── __init__.py
│   			├── contact.py
│   			├── cover.py
│   			├── executive.py
│   			├── findings.py
│   			├── legal.py
│   			├── overview.py
│   			├── poc.py
│   			├── scope.py
│   			├── severity.py
│   			├── summary.py
│   			└── toc.py
│   	├── utils/
│   			├── __pycache__
│   			├── __init__.py
│   			├── table.py
│   			├── util.py
│
├── static/
   	└── logo.png
```

Explicatii structura

```bash
pentest_report/
├── main.py                     ← Entry point + inițializare sigură
├── components/                 ← UI modulară
│   ├── general.py              ← Client, Tester, Reset complet
│   ├── scope.py                ← Scope of Testing
│   ├── findings.py             ← Findings cu severity color
│   ├── executive.py            ← Executive Summary
│   ├── poc.py                  ← PoC cu imagini 2x2 + cod
│   ├── export.py               ← Save/Load JSON + PDF
│   └── methodology_screen.py   ← Metodologie
├── parsers/sections/           ← Generare PDF (ReportLab)
│   ├── cover.py                ← Copertă cu logo
│   ├── toc.py                  ← TOC dinamic (6.1 → 7.1)
│   ├── findings.py             ← Tabel findings
│   ├── poc.py                  ← PoC cu imagini base64
│   └── ...
├── assets/fonts/               ← DejaVuSans pentru diacritice ȘȚĂÂÎ
└── static/logo.png             ← Logo client
```

### **FIȘIERELE PRINCIPALE (rădăcină)**

`├── main.py`

**Rol:** Entry-point-ul aplicației Streamlit
**Ce face:**

- Inițializează session_state în siguranță
- Importă toate componentele
- Creează tab-urile: General → Scope → Findings → Executive → PoC → Export
- Pornește serverul cu streamlit run main.py

├── requirements.txt

**Conținut tipic (exemplu real):**

txt

`streamlit==1.39.0
reportlab==4.2.2
Pillow==10.4.0
python-dateutil==2.9.0`

**Rol:** Instalează toate dependențele automat pe Streamlit Cloud

├── run.bat   și   [run.sh](http://run.sh/)

`streamlit run main.py --server.port=8501`

**Rol:** Pornire rapidă locală

assets/ – RESURSE STATICE

```bash
├── assets/
│   ├── logo.png          ← Logo-ul tău (folosit în UI)
│   ├── cover_logo.png    ← Logo mare pentru copertă PDF
│   └── fonts/
│       ├── DejaVuSans-Bold.ttf
│       └── DejaVuSans-BoldOblique.ttf
```

DE CE DejaVuSans?
→ Suport complet pentru diacritice românești: ȘȚĂÂÎ
→ Fără ele → PDF-ul arată: SQL InjecÈie în login
→ Cu ele → SQL Injecție în login

components/ – INTERFAȚA UTILIZATORULUI (UI)

```bash
├── components/
│   ├── general.py          ← Client, Tester, Data, Reset complet, Logo upload
│   ├── scope.py            ← Scope of Testing (text area)
│   ├── findings.py         ← Adăugare/editare findings cu severity color
│   ├── executive.py        ← Executive Summary (rezumat pentru C-level)
│   ├── poc.py              ← Proof of Concept cu imagini + cod terminal
│   ├── export.py           ← Save/Load JSON + Generate PDF
│   ├── severity.py         ← Tabel cu rating-uri (Critical, High, etc.)
│   ├── legal.py            ← Disclaimer legal
│   └── methodology_screen.py ← Metodologie testare (OSSTMM / PTES)
```

Fiecare fișier = un tab curat, modular
Avantaj: Poți lucra independent pe fiecare secțiune

mailer/ – TRIMITE RAPORTUL PRIN EMAIL

├── mailer/
│   └── [send.py](http://send.py/)

Exemplu funcționalitate:

```bash
def send_report(email, pdf_bytes):
    msg = EmailMessage()
    msg['Subject'] = f"Raport Pentest - {st.session_state.project}"
    msg['From'] = "pentest@company.com"
    msg['To'] = email
    msg.add_attachment(pdf_bytes, maintype='application', subtype='pdf', filename='report.pdf')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("user", "pass")
        smtp.send_message(msg)
```

Rol: Trimite raportul direct clientului din app

parsers/ – MOTORUL DE GENERARE PDF

```bash
├── parsers/
│   ├── nessus.py     ← Parsează .nessus → findings automate
│   ├── nmap.py       ← Parsează nmap XML → porturi deschise
│   └── sections/     ← FIȘIERELE CARE CONSTRUIESC PDF-UL
│       ├── cover.py         ← Pagina 1 (copertă cu logo mare)
│       ├── toc.py           ← Table of Contents dinamic (6.1 → 7.1)
│       ├── overview.py      ← Assessment Overview
│       ├── scope.py         ← Scope of Testing
│       ├── severity.py      ← Severity Ratings table
│       ├── executive.py     ← Executive Summary
│       ├── findings.py      ← Tabel cu toate findings-urile
│       ├── poc.py           ← PoC cu imagini 2x2 + cod terminal
│       ├── legal.py         ← Disclaimer
│       ├── contact.py       ← Contact information
│       └── summary.py       ← Conclusion
```

Cel mai important folder – aici se construiește PDF-ul profesional

parsers/utils/ – FUNCȚII AJUTĂTOARE

```bash
│   ├── utils/
│       ├── table.py     ← Stiluri pentru tabele (culori severity)
│       └── util.py      ← Funcții comune (base64 → imagine, culori hex)
```

static/ – RESURSE PUBLICE

```bash
├── static/
    └── logo.png         ← Logo afișat în sidebar Streamlit
```

FLUXUL COMPLET AL APLICAȚIEI (pas cu pas)

```bash
Utilizator
    ↓
main.py → creează tab-urile
    ↓
components/*.py → utilizatorul completează date
    ↓
st.session_state → memorează totul
    ↓
export.py → apasă "Generate PDF"
    ↓
parsers/sections/*.py → construiesc PDF-ul cu ReportLab
    ↓
returnează PDF + JSON backup
    ↓
mailer/send.py → opțional trimite email
```

## **IMPLEMENTARE**

### Import/Export JSON complet (cod real)

```bash
# export.py – Save complet
json_data = {
    "client": st.session_state.client,
    "project": st.session_state.project,
    "findings": st.session_state.findings,
    "pocs": st.session_state.pocs,
    "logo": st.session_state.logo,
    # ... toate câmpurile
}
st.download_button("Save JSON", json.dumps(json_data), "report_data.json")
```

```bash
# export.py – Load complet
for key, value in data.items():
    st.session_state[key] = value
st.rerun()
```

### TOC dinamic (6.1 → 7.1)

```bash
# toc.py – Secțiune 6 doar dacă există findings
if findings:
    data.append(["6", "Technical Findings"])
    for i, f in enumerate(sorted_findings, 1):
        data.append(["", f"  6.{i}  {f['id']} - {f['title']}"])

if pocs:
    data.append(["7", "Proof of Concept"])
    for i, poc in enumerate(pocs, 1):
        data.append(["", f"  7.{i}  {poc['title']}"])
```

### PoC cu imagini 2x2

```bash
# poc.py (ReportLab)
rows = [image_flowables[i:i+2] for i in range(0, len(image_flowables), 2)]
table = Table(rows, colWidths=[3.2*inch, 3.2*inch])
```

---

- **Deploy pe Streamlit Cloud**: [https://pentest-report.streamlit.app](https://pentest-report.streamlit.app/)

---

## ANEXA A – STRUCTURA PROIECTULUI

TOC DINAMIC – 6.1 → 7.1 (cel mai cerut exemplu)

```bash
# parsers/sections/toc.py
def add_toc(pdf, findings=None, pocs=None):
    findings = findings or []
    pocs = pocs or []
    
    data = [["Page", "Section"]]
    
    # Secțiuni fixe
    fixed = ["1 Cover Page", "2 Table of Contents", "3 Legal Disclaimer", 
             "4 Assessment Overview", "5 Executive Summary"]
    for sec in fixed:
        page, text = sec.split(" ", 1)
        data.append([Paragraph(page, pdf.styles['Normal']), Paragraph(text, pdf.styles['Normal'])])

    # 6 Technical Findings + 6.1, 6.2...
    if findings:
        data.append([Paragraph("6", pdf.styles['Normal']), Paragraph("Technical Findings", pdf.styles['Normal'])])
        for i, f in enumerate(sorted(findings, key=lambda x: x.get('severity', '')), 1):
            color = severity_color(f.get('severity', ''))
            title = f"{f['id']} - {f['title'][:50]}..."
            data.append(["", Paragraph(f"  6.{i} <font color='{color}'>{title}</font>", pdf.styles['Normal'])])

    # 7 Proof of Concept + 7.1, 7.2...
    if pocs:
        data.append([Paragraph("7", pdf.styles['Normal']), Paragraph("Proof of Concept", pdf.styles['Normal'])])
        for i, poc in enumerate(pocs, 1):
            title = poc.get('title', f'PoC {i}')[:60]
            data.append(["", Paragraph(f"  7.{i} {title}", pdf.styles['Normal'])])

    table = Table(data, colWidths=[0.9*inch, 5.5*inch])
    table.setStyle(TableStyle([...]))  # stilul tău actual
    pdf.story.append(table)
```

IMPORT JSON COMPLET (NU DOAR FINDINGS!)

```bash
# components/export.py
if uploaded and st.button("Import Project", type="primary"):
    try:
        data = json.load(uploaded)
        
        # Șterge tot înainte
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        
        # Reinițializează doar strictul necesar
        st.session_state.findings = []
        st.session_state.pocs = []
        st.session_state.contacts = [...]
        
        # Încarcă totul
        for key, value in data.items():
            st.session_state[key] = value
            
        st.success("TOATE DATELE ÎNCĂRCATE!")
        st.rerun()
    except Exception as e:
        st.error(f"Eroare: {e}")
```

SALVARE AUTOMATĂ JSON LA FIECARE MODIFICARE

```bash
# La finalul fiecărui tab (ex: findings.py)
if st.button("Save Finding"):
    # ... salvezi finding-ul
    with open("report_data.json", "w", encoding="utf-8") as f:
        json.dump({
            "client": st.session_state.client,
            "findings": st.session_state.findings,
            "pocs": st.session_state.pocs,
            # ... toate câmpurile
        }, f, indent=2, ensure_ascii=False)
    st.success("Salvată automat!")
```

PARSING AUTOMAT NMAP → FINDINGS

```bash
# parsers/nmap.py
def parse_nmap(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    findings = []
    
    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        for port in host.findall('.//port'):
            if port.find('state').get('state') == 'open':
                findings.append({
                    "id": f"VULN-{len(findings)+1:03d}",
                    "title": f"Port deschis {port.get('portid')}",
                    "host": ip,
                    "severity": "Informational"
                })
    return findings
```
