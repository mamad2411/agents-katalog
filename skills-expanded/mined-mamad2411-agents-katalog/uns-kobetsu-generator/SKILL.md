---
name: uns-kobetsu-generator
description: >
  Generador de個別契約書 (contratos individuales de派遣) según la労働者派遣法第26条.
  Implementación real basada en Electron + SQLite + PDFKit con datos de 76 empresas y
  392 empleados. Usar SIEMPRE que necesites: crear contratos de派遣, calcular tarifas
  de派遣, validar requisitos legales, generar PDFs de個別契約書, entender el flujo de
  datos desde DB hasta PDF, o debuggear problemas de generación de contratos.
  Triggers: 個別契約書, kobetsu, contrato派遣, dispatch contract, 派遣法26条, worker
  assignment, generar contrato, tarifas派遣, calcular tarifa, kobetsu PDF.
---

# UNS 個別契約書 Generator — Implementación Real

Sistema de generación de contratos individuales de派遣 implementado en la app Kobetsu.

## Arquitectura de Datos

### Flujo: DB → Data Object → PDF

```
client_companies (SQLite)          data object (JavaScript)         PDF (PDFKit)
┌─────────────────────┐    IPC    ┌──────────────────────┐   fn   ┌──────────────┐
│ company_name        │ ───────→ │ data.company_name    │ ────→ │ Título celda │
│ company_address     │          │ data.companyDetails  │       │ Grid denso   │
│ commander_dept/name │          │ data.hourly_rate     │       │ 1 página A4  │
│ hourly_rate         │          │ data.start_date      │       │              │
│ ... (48 campos)     │          │ data.employees[]     │       │              │
└─────────────────────┘          └──────────────────────┘       └──────────────┘
```

### Datos del Seed: 76 Empresas

Cada empresa tiene una combinación única de `company_name + line`. Claves compactas:
```
cn = company_name      ca = company_address     cp = company_phone
fn = factory_name      fa = factory_address     fp = factory_phone
dp = department        ln = line (CLAVE ÚNICA)
hr = hourly_rate       br = billing_rate        pm = profit_margin
cd = commander_dept    cna = commander_name     cph = commander_phone
sd = supervisor_dept   sna = supervisor_name    sph = supervisor_phone
ccd = complaint_client_dept  ccn = complaint_client_name  ccp = complaint_client_phone
cud = complaint_uns_dept     cun = complaint_uns_name     cup = complaint_uns_phone
chd = complaint_uns_handler_dept  chn = complaint_uns_handler_name  chp = complaint_uns_handler_phone
jd = job_description   wh = work_hours          bt = break_time
oh = overtime_hours    ood = overtime_outside_days
cal = calendar         rd = restriction_date
cod = cutoff_day       pd = payment_day         ba = bank_account
tu = time_unit
```

### Datos del Seed: 392 Empleados Activos
```
en = employee_number   fn = full_name           kn = katakana_name
sx = sex               nt = nationality         bd = birth_date
hr = hourly_rate       br = billing_rate        pm = profit_margin
dc = dispatch_company  dp = department          ln = line
jd = job_description   hd = hire_date           ahd = actual_hire_date
ve = visa_expiry       vt = visa_type
pc = postal_code       ad = address             ap = apartment
hi = health_insurance  ni = nursing_insurance   pn = pension
sc = standard_compensation
```

## Requisitos Legales (派遣法第26条)

Todo 個別契約書 DEBE incluir estos 11 elementos:

| # | Elemento | Campo DB | Sección PDF |
|---|---|---|---|
| 1 | 業務内容 | `job_description` | 【派遣内容】 |
| 2 | 就業場所 | `factory_name` + `factory_address` | 【派遣先】就業場所 |
| 3 | 指揮命令者 | `commander_dept/name/phone` | 【派遣先】指揮命令者 |
| 4 | 派遣期間 | `start_date` ～ `end_date` | 【派遣内容】派遣期間 |
| 5 | 就業日・時間 | `calendar`, `work_hours`, `break_time` | 【派遣内容】就業日/時間 |
| 6 | 安全衛生 | (texto fijo legal) | Sección legal |
| 7 | 苦情処理 | `complaint_*` campos | 【派遣先/元】+ legal |
| 8 | 派遣料金 | `hourly_rate` × multipliers | 【派遣料金】 |
| 9 | 契約解除措置 | (texto fijo legal) | Sección legal |
| 10 | 紹介予定派遣 | (無 por defecto) | Sección legal |
| 11 | 待遇決定方式 | (労使協定方式) | Sección legal |

## Cálculo de Tarifas

```javascript
const rate = data.hourly_rate; // De la configuración de empresa

// Tarifas calculadas automáticamente
const 基本      = rate;
const 残業125   = Math.round(rate * 1.25);
const 休日135   = Math.round(rate * 1.35);
const 超過150   = Math.round(rate * 1.50);

// Ejemplo: rate = 1872
// 基本: ¥1,872  残業: ¥2,340  休日: ¥2,527  60h超: ¥2,808
```

### Costos Sociales (会社負担)
```
健康保険:    5.00%
厚生年金:    9.15%
雇用保険:    0.95%
労災保険:    0.30%
子育て拠出金: 0.36%
─────────────────
Total:      15.76%
```

### Fórmula de Margen
```
粗利 (margen bruto) = billing_rate - hourly_rate
粗利率 = (billing_rate - hourly_rate) / billing_rate × 100
```

## Cálculo de Fechas

```javascript
function workdayOffset(dateStr, days) {
  let d = new Date(dateStr);
  let count = 0;
  const direction = days > 0 ? 1 : -1;
  const target = Math.abs(days);
  while (count < target) {
    d.setDate(d.getDate() + direction);
    const dow = d.getDay();
    if (dow !== 0 && dow !== 6) count++; // Excluir sáb/dom
  }
  return d.toISOString().slice(0, 10);
}

// contract_date = start_date - 2 días hábiles
// notification_date = start_date - 3 días hábiles
```

## Tipo de Empleo

```javascript
const hireDate = new Date(employee.hire_date || employee.actual_hire_date);
const startDate = new Date(data.start_date);
const daysSinceHire = (startDate - hireDate) / (1000 * 60 * 60 * 24);

const employmentType = daysSinceHire > 1095
  ? '無期雇用派遣労働者'    // Indefinido (>3 años)
  : '有期雇用派遣労働者';   // Temporal (≤3 años)
```

## Textos Legales Fijos

Los siguientes textos son constantes en todo個別契約書 de UNS:

- **安全・衛生**: 派遣先及び派遣元事業主は、労働者派遣法第44条から第47条の2までの規定により...
- **便宜供与**: 派遣先は、派遣労働者に対して利用の機会を与える給食施設、休憩室...
- **苦情処理方法**: (1) 派遣元事業主における苦情処理担当者が... (2) 派遣先における... (3) 密接な連携...
- **契約解除措置**: （１）事前申し入れ （２）就業機会の確保 （３）損害賠償等
- **紹介予定派遣**: 無
- **待遇決定方式**: 協定対象派遣労働者（労使協定方式）

## Datos Fijos de UNS-Kikaku (乙)

```
会社名: ユニバーサル企画株式会社
住所: 〒461-0025 愛知県名古屋市東区徳川2-18-18
代表者: 代表取締役　中山　雅和
許可番号: 派　23-303669
TEL: 052-938-8840
派遣元責任者: 営業部　取締役 部長　中山　欣英
```
