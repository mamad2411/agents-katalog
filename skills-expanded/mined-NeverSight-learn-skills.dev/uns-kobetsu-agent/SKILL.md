---
name: uns-kobetsu-agent
description: >
  Agente autónomo para el flujo completo de generación de contratos個別契約書 de UNS-Kikaku.
  Este agente orquesta todo el proceso: desde la selección de empresa y empleados hasta la
  generación de PDFs, validación legal, y gestión de la app Electron. Usa este agente
  SIEMPRE que el usuario pida: (1) Generar un contrato completo, (2) Modificar la app
  Kobetsu de forma integral, (3) Ejecutar el flujo completo de個別契約書, (4) Resolver
  problemas complejos que involucren múltiples partes del sistema, (5) Crear nuevas
  funcionalidades end-to-end. Triggers: generar contrato, workflow kobetsu, flujo completo,
  proceso個別契約書, automatizar contrato, agente kobetsu, kobetsu workflow, contract automation,
  full process, end-to-end kobetsu.
---

# UNS Kobetsu Agent — Orquestador de Contratos

Agente autónomo que gestiona el ciclo completo de generación de contratos de派遣.

## Ecosistema de Skills

Este agente coordina los siguientes skills del ecosistema UNS:

| Skill | Rol | Cuándo Usarlo |
|---|---|---|
| `uns-kobetsu-app` | Arquitectura y código de la app | Modificar código, debug, extender app |
| `uns-kobetsu-pdf-engine` | Layout y constantes de PDF | Cambiar formato, agregar secciones |
| `uns-kobetsu-generator` | Lógica de generación de contratos | Calcular tarifas, validar requisitos |
| `uns-kobetsu-keiyaku` | Datos legales del contrato | Verificar cumplimiento legal |
| `uns-db-genzai` | Schema de empleados派遣 | Consultas de empleados |
| `uns-employee-manager` | Hub de gestión de empleados | Búsqueda, alertas, reportes |
| `uns-visa-manager` | Gestión de visas | Verificar visas antes de contrato |
| `uns-arari-calculator` | Cálculo de粗利 | Evaluar rentabilidad |
| `uns-36kyotei-checker` | Verificar horas extra | Compliance laboral |

## Workflow Principal: Generar Contrato

### Paso 1: Recopilar Información
```
¿Qué necesito?
├── Empresa派遣先 (company_name)
├── Fábrica (factory_name)
├── Departamento (department)
├── Línea (line)
├── Empleados seleccionados
├── Fecha inicio (start_date)
└── Fecha fin (end_date)
```

### Paso 2: Validar Datos
```
Verificaciones automáticas:
├── ¿Empresa existe en client_companies? → SQL: SELECT * FROM client_companies WHERE line=?
├── ¿Empleados activos? → status = '在職中'
├── ¿Visas vigentes? → visa_expiry > start_date
├── ¿Período ≤ 3 años? → 派遣法 Art. 26
├── ¿36協定 cumplido? → horas extra < 45h/mes
└── ¿Tarifas configuradas? → hourly_rate > 0
```

### Paso 3: Calcular Fechas y Tarifas
```javascript
// Fechas
contract_date = workdayOffset(start_date, -2)    // -2 días hábiles
notification_date = workdayOffset(start_date, -3) // -3 días hábiles

// Tarifas
基本 = hourly_rate
残業 = Math.round(hourly_rate * 1.25)
休日 = Math.round(hourly_rate * 1.35)
60h超 = Math.round(hourly_rate * 1.50)

// Tipo de empleo
antigüedad = (start_date - hire_date) en días
tipo = antigüedad > 1095 ? '無期雇用' : '有期雇用'
```

### Paso 4: Generar Documentos
```
Documentos a generar:
├── 個別契約書 (kobetsu) → 1 PDF por contrato
├── 派遣先通知書 (tsuchisho) → 1 PDF con tabla de empleados
└── 派遣元管理台帳 (daicho) → 1 PDF por empleado
```

### Paso 5: Verificar Output
```
Checklist de verificación:
├── ¿PDF generado sin errores?
├── ¿Todos los campos obligatorios presentes?
├── ¿Tarifas correctas?
├── ¿Fechas correctas?
├── ¿Nombres en katakana correctos?
└── ¿Firma con datos de UNS correctos?
```

## Workflow: Modificar la App

### Antes de modificar código:
1. **Leer** el skill `uns-kobetsu-app` para entender la arquitectura
2. **Leer** `CLAUDE.md` en la raíz del proyecto para contexto
3. **Identificar** qué archivo modificar:
   - Frontend → `src/renderer/index.html`
   - Backend/DB → `src/main/main.js`
   - Datos → `src/main/seed-data.js`
   - PDFs → `src/main/main.js` (funciones generate*)

### Para cambios en PDF layout:
1. **Leer** el skill `uns-kobetsu-pdf-engine` para constantes
2. **Verificar** anchos de columna suman 555
3. **Probar** generando un PDF después del cambio
4. **Verificar** que todo cabe en 1 página A4

### Para cambios en datos:
1. **Modificar** `seed-data.js` (agregar/editar registros)
2. **Borrar** `data/kobetsu.db`
3. **Reiniciar** la app con `npm start`

## Workflow: Debug

### Error de módulo nativo
```bash
# Síntoma: NODE_MODULE_VERSION mismatch
npx @electron/rebuild
```

### Error de base de datos
```bash
# Síntoma: tabla no existe o datos incorrectos
del data\kobetsu.db   # Windows
npm start             # Re-crea automáticamente
```

### Error de PDF
```
# Síntoma: caracteres rotos
→ Verificar que fonts/NotoSansJP-Regular.ttf existe (9.6MB)

# Síntoma: texto cortado o fuera de celda
→ Reducir fontSize o aumentar ancho de columna
→ Usar lineBreak: false para celdas de una línea

# Síntoma: contenido en 2 páginas
→ Reducir RH (row height) de 12 a 11 o 10
→ Reducir font sizes
→ Comprimir secciones legales
```

## Datos de UNS-Kikaku (constantes)

```
Empresa: ユニバーサル企画株式会社
Dirección: 〒461-0025 愛知県名古屋市東区徳川2-18-18
Representante: 代表取締役　中山　雅和
Licencia: 派　23-303669
Teléfono: 052-938-8840
Responsable: 営業部　取締役 部長　中山　欣英
```

## Decisiones del Agente

| Situación | Acción |
|---|---|
| Usuario pide generar contrato | Ejecutar workflow principal completo |
| Usuario pide cambiar formato PDF | Leer `uns-kobetsu-pdf-engine`, modificar `main.js` |
| Usuario pide agregar empresa | Modificar `seed-data.js`, resetear DB |
| Usuario pide verificar compliance | Usar `uns-36kyotei-checker` + `uns-visa-manager` |
| Usuario pide calcular rentabilidad | Usar `uns-arari-calculator` |
| Error en la app | Seguir workflow de debug |
| Usuario pide nueva funcionalidad | Leer `uns-kobetsu-app`, planificar, implementar |

## Integración con Otros Sistemas UNS

```
                    ┌─────────────────┐
                    │  Kobetsu Agent  │ ← ESTE AGENTE
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  ┌─────┴─────┐      ┌──────┴──────┐      ┌─────┴─────┐
  │ Kobetsu   │      │ PDF Engine  │      │ DB        │
  │ App       │      │ (Layout)    │      │ Connector │
  └─────┬─────┘      └─────────────┘      └─────┬─────┘
        │                                        │
  ┌─────┴─────┐                            ┌─────┴─────┐
  │ seed-data │                            │ UNS-DBUNIX│
  │ (SQLite)  │                            │ (Postgres)│
  └───────────┘                            └───────────┘
```
