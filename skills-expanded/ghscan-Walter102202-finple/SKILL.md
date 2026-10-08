---
name: fintech_inversiones
description: Activar cuando el usuario describa una inversión, plataforma de crowdfunding, asesoría crediticia o de inversión, custodia digital, exchange de criptoactivos local, rendimientos prometidos por una fintech, sistema de finanzas abiertas (Open Finance), o duda sobre si una plataforma está autorizada por la CMF. Palabras gatillo: fintech, plataforma de inversión, crowdfunding, P2P, asesoría financiera, exchange, custodia, open finance, RPSF, rendimiento garantizado.
---

# Skill — Fintech, inversiones y servicios financieros tecnológicos

Cuando esta Skill esté activa, sigue este protocolo.

## 1. Triage

Necesitas saber:
- **Nombre exacto** de la plataforma o fintech.
- **Servicio** que está usando: crowdfunding, asesoría crediticia, asesoría de inversión, custodia, intermediación, sistema alternativo de transacción.
- **Monto invertido** y rendimiento prometido (banderas rojas: > 20% mensual, "garantizado", urgencia).
- ¿Está la plataforma **registrada en RPSF (CMF)**? — siempre verificar.
- Origen del contacto (red social, recomendación, llamada en frío).

## 2. Marco normativo aplicable

- **Ley 21.521 (Fintec)**, vigente 3 feb 2023 — marco general de servicios financieros tecnológicos: crowdfunding, asesoría crediticia, custodia, sistema de finanzas abiertas. https://www.bcn.cl/leychile/navegar?idNorma=1187323
- **NCG 502 CMF (2024)** — Registro de Prestadores de Servicios Financieros (RPSF) y obligaciones operacionales. https://www.cmfchile.cl/normativa/ncg_502_2024.pdf
- **NCG 514 CMF (2024)** — Sistema de Finanzas Abiertas (Open Finance), portabilidad de datos financieros. https://www.cmfchile.cl/normativa/ncg_514_2024.pdf
- **Manual SIF (CMF, ene 2025)** — requisitos de ciberseguridad para fintech.

## 3. Plazos críticos a verificar con search_corpus

- Plazos de inscripción y autorización RPSF (Ley 21.521).
- Plazos de implementación del Sistema de Finanzas Abiertas (NCG 514, fase 24-36 meses).
- Plazos de respuesta de la fintech a un reclamo del cliente.

## 4. Autoridad correspondiente

- **Fintech registrada en RPSF y problema regulatorio** → **CMF** (cmfchile.cl/atencion-al-publico).
- **Plataforma NO registrada que ofrece servicios regulados** → posible operación ilegal: alerta CMF + denuncia.
- **Promesa de rendimiento irreal o esquema piramidal sospechoso** → derivar a Skill \`fraude_suplantacion\` y revisar **alertas CMF al público** llamando \`fetch_official_source({ url: "https://www.cmfchile.cl/portal/principal/613/w3-propertyvalue-43545.html", reason: "buscar alertas vigentes contra <entidad>" })\` y buscar el nombre de la entidad en la respuesta.

## 5. Protocolo obligatorio antes de responder

1. Si el usuario menciona una plataforma específica, **revisa primero el RPSF** llamando \`fetch_official_source({ url: "https://www.cmfchile.cl/institucional/estadisticas/seg_rgpsf.php", reason: "verificar si <plataforma> está inscrita en el RPSF" })\` y busca el nombre textualmente en el resultado. Si no aparece, comunícalo claro: "no encuentro a <plataforma> en el RPSF de la CMF".
2. \`search_corpus({ query: "<servicio que pregunta>", area: "fintech_inversiones" })\` para anclar el marco normativo.
3. Si necesitas el articulado exacto de la Ley 21.521, llama \`read_bcn_law({ idNorma: "1187323" })\`.
4. Solo entonces redacta Fase 5.

## 6. Banderas rojas que SIEMPRE debes señalar

- Rentabilidad fija o garantizada > 1% mensual sin riesgo: estadísticamente imposible — advertir.
- Plataforma no encontrada en RPSF que dice ofrecer "inversiones reguladas".
- Pagos por canales no oficiales (transferencias a personas naturales, criptos a wallets no identificadas).
- Presión por urgencia ("último día").

## 7. Corpus indexado adicional

Documentos NCG CMF disponibles en el corpus (recuperables vía `search_corpus({ area: "fintech_inversiones" })` o `read_ncg`):

- **NCG 502 CMF (RPSF)** — `read_ncg("502")` para el detalle por numerales.
- **NCG 514 CMF (Sistema de Finanzas Abiertas)** — `read_ncg("514")`.
