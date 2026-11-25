---
name: business-docs
description: Generacion de documentacion de NEGOCIO para el Product Owner de dev-team - convierte HUs, epicas, backlog y sprints en documentos profesionales (PDF y DOCX) en lenguaje 100% funcional, desde plantillas. Cubre los tipos de documento (documento de una HU, especificacion funcional de una epica, informe de sprint/backlog, documento de aceptacion/entrega), la regla de oro de redaccion de negocio, la estructura por tipo, los diagramas funcionales permitidos, el anexo tecnico separado, y el pipeline HTML -> soffice -> PDF/DOCX. Cargala cuando el PO deba entregar un documento de negocio (no una nota tecnica).
---

# Documentacion de negocio (Product Owner) — dev-team

El PO redacta TODO en lenguaje funcional de negocio. Esta skill le da herramientas para
entregar ese contenido como DOCUMENTOS presentables (PDF y DOCX) a gente no programadora:
gerencia, cliente, analistas, QA. No reemplaza el tracker (los items siguen viviendo en
GitHub/Azure); complementa: cuando alguien necesita "el documento" de una funcionalidad,
una epica, o el resumen de un sprint, sale de aqui.

Division de roles: la documentacion de NEGOCIO es del **product-owner** (esta skill). La
documentacion TECNICA (README, OpenAPI, ADRs, diagramas de arquitectura, wiki) es del
**tech-writer** (`/dev-team:document`). El tech-writer APOYA al PO en la redaccion rica, pero
el dueño del contenido de negocio es el PO.

## Regla de oro (igual que en el tracker)
El lector NO es programador. Prohibido en el cuerpo del documento: endpoints, URLs, verbos
HTTP, JSON, nombres de tablas/columnas, nombres de servicios/clases/ramas, stacktraces, jerga
("refactorizar", "deployar", "nullable"). Permitido: conceptos y parametros del negocio tal como
los ve el usuario ("fecha de inicio", "monto maximo", "perfil Supervisor", nombres reales de
pantallas y botones). Todo lo tecnico, si es imprescindible, va en un **Anexo tecnico** claramente
separado al final. Test de lectura antes de exportar: ¿lo entiende una persona de negocio a la
primera? ¿cero palabras de codigo en el cuerpo? Si falla, reescribir.

## Tipos de documento
| Tipo | Cuando | Contenido |
|------|--------|-----------|
| **Documento de HU** | Formalizar una historia para revision/aprobacion o entrega | Historia (Como/Quiero/Para), contexto, criterios Gherkin, alcance, DoD, estimacion |
| **Especificacion funcional** | Una epica o un conjunto de HUs (una funcionalidad completa) | Objetivo de negocio, alcance, actores, flujos funcionales, reglas de negocio, HUs incluidas, criterios, fuera de alcance |
| **Informe de sprint / backlog** | Cierre de sprint o estado del backlog para gerencia | Objetivo del sprint, HUs comprometidas vs. completadas, resultado por HU, metricas de negocio, proximos pasos |
| **Documento de aceptacion / entrega** | Entregar una funcionalidad terminada | Que se entrego (en negocio), criterios cumplidos con evidencia, como demostrarlo, pendientes/observaciones |

## Estructura (todas comparten patron)
1. **Portada**: titulo de negocio, proyecto, tipo de documento, version, fecha, autor (del config), estado.
2. **Resumen** (2-4 lineas): que es y para que, en negocio.
3. **Cuerpo segun el tipo** (tabla de arriba). Los criterios de aceptacion SIEMPRE en Gherkin
   ("Dado… cuando… entonces…"), verificables por QA sin leer codigo.
4. **Diagramas funcionales** (opcional, si aclaran): flujo del usuario o de negocio en Mermaid
   (`flowchart`/`journey`), NUNCA un diagrama tecnico de servicios/BD (eso es del tech-writer).
5. **Anexo tecnico** (opcional, separado): SOLO si es imprescindible (referencias al tracker,
   version, enlaces). Nada de codigo en el cuerpo.

## Pipeline de generacion (PDF y DOCX)
La fuente es una plantilla HTML autocontenida (en `templates/doc-negocio/`), que se rellena y
se convierte a los dos formatos con LibreOffice headless (ya disponible para los pases):
```bash
# rellenar la plantilla HTML (reemplazar {{PLACEHOLDERS}}); luego:
soffice --headless --convert-to pdf  --outdir "{salida}" documento.html
soffice --headless --convert-to docx --outdir "{salida}" documento.html
```
- El HTML es la fuente de verdad; PDF (presentar/firmar) y DOCX (editar/compartir) se derivan.
- Si el proyecto tiene una plantilla propia (`config.json` → `doc.templatePath`), partir de ella;
  si no, la del plugin. Mantener acentos y eñes en ambos formatos.
- Salida: `config.json` → `doc.outputDir` (default `.coordination/docs-negocio/`), con nombre
  `{Tipo} - {Titulo} - v{X} - {fecha}.pdf/.docx`.
- Los diagramas Mermaid se renderizan a imagen antes de convertir (o se incluye la version ya
  renderizada) para que el PDF/DOCX los muestre; si no hay renderizador, dejar el diagrama como
  bloque de texto legible y anotarlo.

## Datos y trazabilidad
- El contenido se toma de las HUs reales del tracker y de `.coordination/backlog.md` (no se
  inventan criterios). El documento CITA los IDs del tracker en el anexo, para trazabilidad.
- Autor, proyecto y aprobador salen de `config.json` (`git.identity`, `project`, y `doc.*`),
  nunca escritos a mano.
- Un documento de aceptacion referencia la evidencia de QA (embebida o enlazada), sin duplicarla.

## Reglas
- Cuerpo 100% de negocio; lo tecnico al anexo o fuera. Aplicar el test de lectura antes de exportar.
- No inventar HUs ni criterios: se derivan del tracker/backlog.
- Entregar SIEMPRE en los dos formatos si se pide "documento" (PDF + DOCX), salvo que se pida uno.
- El documento no reemplaza el item del tracker: lo complementa y lo cita.
- Secretos/datos sensibles: nunca en el documento.
