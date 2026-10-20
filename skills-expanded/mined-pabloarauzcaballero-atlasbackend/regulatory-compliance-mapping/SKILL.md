---
name: regulatory-compliance-mapping
description: Método para bajar normativa de protección de datos y salud a controles de ingeniería verificables — identificar los marcos aplicables con el responsable legal, matriz requisito → control técnico → evidencia → dueño, privacidad por diseño y por defecto, evaluación de impacto, registro de tratamientos, gestión de brechas y revisión periódica. Usar al arrancar un producto o módulo que trate datos personales o clínicos, al recibir un requisito "de cumplimiento", al preparar una auditoría o evaluación de impacto, y al responder "¿esto cumple?" sin inventar la respuesta.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Mapeo de normativa a controles

Esta skill **no dice qué exige la ley**: eso lo determina el responsable legal / de privacidad de
la empresa para cada jurisdicción y actividad. Lo que da es el **método** para convertir lo que
ese responsable determine en controles técnicos con evidencia, y para que ninguna afirmación de
cumplimiento salga del equipo sin respaldo. Aplicá `anti-hallucination-guard`: una obligación
legal citada de memoria vale lo mismo que una API inventada.

## 1. Postura por defecto

1. **Nadie del equipo técnico afirma «cumple con X»**. El equipo afirma «implementa el control C,
   con esta evidencia, que el responsable legal mapeó al requisito R». La diferencia es toda.
2. Ante duda de aplicabilidad, diseñá para la vara más exigente que sea razonable: el costo de
   subir controles después es mayor que el de tenerlos.
3. Los marcos de referencia sirven como **catálogo de controles**, no como afirmación de que
   aplican. Ejemplos habituales para datos de salud: GDPR (categoría especial de datos de salud,
   art. 9; protección de datos desde el diseño y por defecto, art. 25; registro de actividades de
   tratamiento, art. 30; notificación de brechas, art. 33; evaluación de impacto, art. 35);
   HIPAA (reglas de privacidad, seguridad y notificación de brechas, 45 CFR Parte 164);
   OWASP ASVS para controles de aplicación (`security-guardrails`). La normativa nacional
   aplicable a la empresa y a sus clientes: **la identifica el responsable legal**.

## 2. Paso 1 — Inventario de tratamientos

No se puede mapear lo que no se conoce. Por cada flujo que toque datos personales:

| Campo | Ejemplo |
|---|---|
| Tratamiento | «Agenda de citas con especialidad» |
| Finalidad | Prestación del servicio de salud |
| Categorías de datos | Identificación, contacto, dato de salud (especialidad, motivo) |
| Categorías de titulares | Pacientes, profesionales |
| Origen | Titular; profesional; integración X |
| Destinatarios | Profesional tratante, organización, proveedor de email |
| Transferencias a terceros / otro país | Proveedor de correo (país, contrato) |
| Plazo de conservación | *Lo define el responsable legal* |
| Base o justificación del tratamiento | *Lo define el responsable legal* |
| Sistemas y repos involucrados | API, web, mobile, jobs |
| Dueño técnico | Equipo/persona |

Este inventario **es** el insumo del registro de actividades de tratamiento que muchos marcos
exigen (p. ej. GDPR art. 30). Vive versionado junto al modelo de datos, se actualiza en el mismo
PR que agrega un campo o un flujo (`data-privacy-sensitive` §1, `technical-docs-and-adr`).

## 3. Paso 2 — Matriz requisito → control → evidencia → dueño

El artefacto central. Una fila por requisito **entregado por escrito por el responsable legal**
(id, texto, fuente, fecha). Sin fila de origen, no hay control «de cumplimiento»: es una mejora
técnica común.

| REQ | Requisito (texto del responsable legal) | Control técnico | Dónde vive | Evidencia verificable | Dueño | Estado |
|---|---|---|---|---|---|---|
| R-07 | «Registrar todo acceso a datos clínicos» | Evento de auditoría en cada lectura | `audit-trail-history` | Query de eventos por paciente + test de integración | Backend | IMPLEMENTADO |
| R-12 | «El titular puede revocar el consentimiento» | Revocación con efecto inmediato | `data-privacy-sensitive` | Test otorgar→leer→revocar→denegado | Backend | IMPLEMENTADO |
| R-19 | «Notificar brechas en el plazo Z» | Runbook + detección | `incident-response-postmortem` | Simulacro con tiempos | SRE + Legal | PARCIAL |

Estados: `NO_INICIADO · PARCIAL · IMPLEMENTADO · VERIFICADO · NO_APLICA (con justificación del
responsable legal)`. `VERIFICADO` exige evidencia pegada según `evidence-and-verification`.

Reglas:
- Un requisito puede necesitar varios controles; un control puede cubrir varios requisitos.
  La matriz es N:M, no una lista.
- «Control organizativo» (política, capacitación, contrato) también tiene fila y dueño, aunque
  no sea código.
- Cada control apunta a la skill de la casa que lo detalla: privacidad (`data-privacy-sensitive`),
  consentimiento y minimización (`data-privacy-sensitive`), rastro de acceso (`audit-trail-history`), acceso
  (`authz-access-control`, `authn-identity`), aislamiento (`multi-tenancy`), auditoría
  (`audit-trail-history`), respaldo (`backup-restore-dr`), secretos
  (`environment-secrets-config`), seguridad de aplicación (`security-guardrails`).

## 4. Paso 3 — Privacidad por diseño y por defecto, como práctica

No es un documento: es una lista de decisiones que se toman **antes** de escribir el código.

1. **Minimización**: ¿qué campo puedo no pedir? ¿qué endpoint puede devolver menos?
2. **Por defecto lo más restrictivo**: visibilidad privada, notificaciones neutras, exportes
   desactivados, retención mínima; el usuario o el administrador amplían explícitamente.
3. **Separación**: identificación separada de datos clínicos donde sea viable; seudonimización
   en analítica.
4. **Transparencia técnica**: se puede responder «qué datos tenemos de esta persona, quién los vio
   y por qué» con una consulta, no con una investigación de dos semanas.
5. **Derechos del titular** como funcionalidad (acceso, rectificación, supresión/bloqueo,
   portabilidad, oposición — cuáles aplican: responsable legal), con flujo, autorización y
   registro; no como ticket manual a base de datos.
6. **Terceros**: todo proveedor que reciba datos personales tiene contrato de tratamiento vigente
   antes de la primera llamada. Sin contrato, el dato no sale (`data-privacy-sensitive` §3).

## 5. Paso 4 — Evaluación de impacto

Cuando un tratamiento es de alto riesgo (datos de salud a escala, perfilado, nuevas tecnologías,
vigilancia — el criterio final es del responsable legal), se hace **antes** de tratar. Estructura
mínima, alineada con lo que exige GDPR art. 35(7) como referencia:

1. Descripción sistemática del tratamiento y sus finalidades.
2. Necesidad y proporcionalidad.
3. Riesgos para las personas (no para la empresa): reidentificación, acceso indebido, pérdida,
   discriminación, daño por error clínico.
4. Medidas para mitigar cada riesgo → filas nuevas en la matriz de §3.

El equipo técnico aporta 1, 3 y 4 con precisión; el responsable legal firma. Amenazas técnicas
con `threat-modeling`.

## 6. Paso 5 — Brechas

1. **Definición operativa** acordada con el responsable legal de qué es una brecha (acceso
   indebido, pérdida, alteración, divulgación) y qué eventos técnicos la disparan.
2. **Detección**: alertas sobre accesos anómalos, break-glass, exportes masivos, fallas de
   autorización repetidas (`backend-observability`, `security-testing`).
3. **Runbook** con roles, reloj (el plazo de notificación lo fija la norma aplicable — p. ej.
   GDPR art. 33 habla de 72 horas desde que se tiene conocimiento; la vigente para la empresa la
   confirma el responsable legal), contención, preservación de evidencia y comunicación —
   `incident-response-postmortem`.
4. **Registro de brechas** obligatorio aunque no se notifique: hechos, efectos, medidas.
5. **Simulacro** al menos anual con tiempos medidos. Sin simulacro, el runbook es ficción.

## 7. Paso 6 — Revisión periódica y cambio

- La matriz se revisa: en cada cambio normativo comunicado por el responsable legal, en cada
  módulo nuevo que trate datos, en cada incidente, y con calendario fijo.
- Un PR que agrega campo, flujo, tercero o export incluye la actualización del inventario (§2)
  y, si toca un control, su fila en la matriz. Checklist en `code-review-standard`.
- Auditorías externas: el paquete de evidencia se genera desde la matriz, no se arma a mano la
  semana anterior.
- Decisiones de «no aplica» y de aceptación de riesgo: firmadas por el responsable, con fecha y
  vencimiento (`technical-docs-and-adr`).

## Anti-patrones

- «Somos compatibles con HIPAA/GDPR» en un README sin matriz ni responsable.
- Requisitos legales inferidos por el equipo (o por un modelo de lenguaje) de un artículo de blog.
- Cumplimiento como proyecto de fin de año en vez de práctica por PR.
- Evidencia = capturas de pantalla viejas en una carpeta.
- Control implementado sin dueño: nadie lo mantiene, nadie lo prueba.
- Tratar el consentimiento como base universal de todo tratamiento (cuál aplica: responsable legal).

## Checklist

- [ ] Marcos y normativa aplicables identificados **por escrito** por el responsable legal.
- [ ] Inventario de tratamientos completo y versionado junto al modelo.
- [ ] Matriz requisito → control → evidencia → dueño → estado, con origen por fila.
- [ ] Cada control enlaza a la skill que lo detalla y a su prueba.
- [ ] Defaults restrictivos y minimización aplicados en el diseño.
- [ ] Derechos del titular implementados como flujos con registro.
- [ ] Terceros con contrato antes de recibir datos.
- [ ] Evaluación de impacto hecha para tratamientos de alto riesgo, firmada.
- [ ] Runbook de brechas con reloj, registro y simulacro ejecutado.
- [ ] Revisión periódica calendarizada; «no aplica» y aceptaciones de riesgo firmadas con vencimiento.

## Evidencia / Definition of Done

Para afirmar que un requisito está `VERIFICADO`:

1. **Fila de la matriz** con id, texto y fuente entregados por el responsable legal.
2. **Evidencia técnica literal** del control: salida de test, consulta, respuesta HTTP, captura
   de configuración (`evidence-and-verification`).
3. **Aprobación registrada** del responsable legal sobre el mapeo (quién, fecha, versión).
4. Sin (1) o (3): el estado máximo es `IMPLEMENTADO`, nunca `VERIFICADO`, y el reporte lo dice así.
