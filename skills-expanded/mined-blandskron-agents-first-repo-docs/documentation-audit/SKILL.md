---
name: documentation-audit
description: Audita documentación, prompts, ejemplos, skills y sitio estático para detectar contradicciones, rutas rotas, contenido duplicado y afirmaciones sin evidencia. Úsala antes de un merge o release que cambie documentos, catálogo o portal, y cuando se pida revisar consistencia documental, enlaces, anclas o trazabilidad antes de publicar.
license: MIT
allowed-tools: Read Grep Glob Bash(npm run validate:*) Bash(npm run quality:*)
metadata:
  framework: "agents-first"
  asset-id: "documentation-knowledge.documentation-audit"
  asset-version: "1.1.0"
  domain: "documentation-knowledge"
  status: "stable"
  repo-compatibility: "tool-agnostic"
  canonical: "library/domains/documentation-knowledge/skills/documentation-audit/SKILL.md"
---

# Skill: Documentation Audit

Usa esta skill cuando se modifiquen documentos, prompts, ejemplos, skills o la página estática del repositorio.

## Objetivo

Detectar contradicciones, rutas rotas, contenido duplicado y afirmaciones sin evidencia antes de publicar documentación.

## Problema que resuelve

La documentación puede ser legible y aun así dirigir a archivos inexistentes, repetir fuentes o presentar supuestos como realidad.

## Cuándo utilizarla

- Al modificar documentación, prompts, ejemplos, skills o el sitio.
- Antes de un merge o release que cambie el catálogo.

## Cuándo no utilizarla

- Como sustituto de pruebas funcionales del software documentado.

## Entradas esperadas

- Archivos Markdown modificados.
- Archivos estáticos modificados.
- Objetivo del cambio.

## Dependencias

- Acceso de lectura a los documentos y rutas referenciadas.
- Reglas del repositorio.
- Servidor HTTP cuando la documentación se publica como sitio.

## Casos de uso

- revisión pre-merge;
- cambio de taxonomía;
- publicación de documentación;
- migración de rutas.

## Resultado esperado

Un reporte con alcance, hallazgos, correcciones, validaciones y pendientes.

## Restricciones

- No inventar comandos, rutas, resultados ni referencias.
- No imprimir secretos encontrados durante la revisión.
- No eliminar contenido útil sin migrarlo.

## Procedimiento

1. Revisa que `AGENTS.md` siga siendo breve, operativo y enlazado.
2. Verifica que `README.md` siga orientado a humanos.
3. Comprueba que el prompt maestro no asuma stack ni agente específico.
4. Revisa que `docs/agent/` conserve el set documental completo del ejemplo profesional.
5. Confirma que las rutas mencionadas existan.
6. Busca secretos, tokens o datos reales en ejemplos.
7. Verifica que cualquier cambio relevante esté registrado en `docs/CHANGELOG.md`.

8. Comprueba metadatos e índices del catálogo cuando cambie `library/`.

## Buenas prácticas

- Revisar primero el diff y después el documento completo.
- Citar la ruta exacta que respalda cada hallazgo.
- Separar errores bloqueantes de mejoras editoriales.

## Checklist

- Ejecutar validación de enlaces Markdown.
- Revisar bloques de código Markdown.
- Servir el sitio por HTTP local si cambió `index.html` o archivos en `assets/` y `pages/`.

- [ ] Los enlaces internos resuelven.
- [ ] Los bloques Markdown están cerrados.
- [ ] Los IDs del catálogo son únicos.
- [ ] No hay comandos o archivos inventados.
- [ ] Changelog e índices reflejan cambios semánticos.
- [ ] El sitio se validó por HTTP si cambió su superficie.

## Errores frecuentes

- Revisar enlaces mediante expresiones regulares sin resolver rutas relativas.
- Marcar como válida una referencia porque existe el directorio, no el archivo.
- duplicar explicaciones extensas en índices.

## Documentos relacionados

- [Guía de contribución de activos](../../docs/CONTRIBUTING_ASSETS.md)
- [Pruebas documentales](../../docs/agent/TESTS.md)

## Prompts compatibles

- [Auditoría documental agents-first](../../prompts/agents-first-documentation-review.prompt.md)

## Skills relacionadas

- [GitHub Pages release](../../library/domains/delivery-platform/skills/github-pages-release/SKILL.md)

## Ejemplo

Resolver cada enlace relativo desde el directorio del documento y devolver archivo, destino y causa para cualquier fallo.

## Procedencia

Proyección generada del activo canónico [`library/domains/documentation-knowledge/skills/documentation-audit/SKILL.md`](../../library/domains/documentation-knowledge/skills/documentation-audit/SKILL.md).

No edites este archivo: modifica la fuente en `library/` y ejecuta `npm run build:skills`.
La puerta de calidad falla si esta proyección queda desactualizada.
