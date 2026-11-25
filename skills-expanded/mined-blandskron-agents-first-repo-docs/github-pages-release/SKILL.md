---
name: github-pages-release
description: Valida que un sitio estático esté listo para publicarse en GitHub Pages. Comprueba rutas, recursos, navegación y contenido servido desde un subdirectorio antes de publicar. Úsala antes de una release del portal, al cambiar rutas o assets, o cuando una publicación en GitHub Pages falle o muestre enlaces y recursos rotos.
license: MIT
allowed-tools: Read Grep Glob Bash(npm run smoke:*) Bash(npm run quality:*)
metadata:
  framework: "agents-first"
  asset-id: "delivery-platform.github-pages-release"
  asset-version: "1.1.0"
  domain: "delivery-platform"
  status: "stable"
  repo-compatibility: "tool-agnostic"
  canonical: "library/domains/delivery-platform/skills/github-pages-release/SKILL.md"
---

# Skill: GitHub Pages Release

## Objetivo

Producir evidencia de que un sitio estático funciona desde la ruta y configuración que el repositorio declara.

## Problema que resuelve

Una página puede funcionar al abrir un archivo local y fallar en GitHub Pages por rutas, base path, carga dinámica o recursos ausentes.

## Cuándo utilizarla

Al cambiar `index.html`, assets, páginas parciales o documentos cargados por el sitio.

## Cuándo no utilizarla

Cuando el proyecto no usa GitHub Pages o requiere un pipeline de build diferente.

## Entradas esperadas

- raíz publicable;
- configuración de Pages documentada;
- archivos modificados;
- comandos reales disponibles.

## Dependencias

- Un servidor HTTP local disponible.
- Navegador para validación interactiva cuando el alcance lo requiera.
- Configuración real de publicación.

## Casos de uso

- validar un portal documental;
- revisar una migración de rutas;
- preparar un release de assets estáticos.

## Resultado esperado

Estado `Listo` o `No listo`, con URLs probadas, respuestas, errores y pendientes.

## Restricciones

- No desplegar ni cambiar configuración remota sin autorización.
- No inventar comandos de build.
- No declarar éxito a partir de abrir archivos con `file://`.

## Procedimiento

1. Confirma la fuente y ruta de publicación.
2. Detecta si existe build; no asumas uno.
3. Sirve la salida mediante HTTP local con una herramienta disponible.
4. Verifica el documento raíz y todos los assets referenciados.
5. Recorre navegación, hashes y páginas dinámicas.
6. Prueba carga de Markdown o manifiestos remotos al frontend.
7. Comprueba acciones de copia y estados de error.
8. Revisa escritorio y un viewport móvil.

## Buenas prácticas

- Validar rutas con el mismo base path que tendrá Pages.
- Registrar errores de consola y solicitudes 404.
- Probar una carga limpia para evitar falsos positivos de caché.

## Checklist

- [ ] La raíz responde `200`.
- [ ] CSS, JS, imágenes y páginas parciales responden `200`.
- [ ] No hay errores JavaScript bloqueantes.
- [ ] Navegación por hash funciona.
- [ ] Contenido canónico y catálogo cargan.
- [ ] Copia usa el texto visible.
- [ ] La interfaz es usable en móvil y escritorio.

## Errores frecuentes

- Validar solo `index.html`.
- Ignorar rutas sensibles a mayúsculas.
- Depender de un servidor con fallback que Pages no ofrece.
- Publicar contenido fallback como si fuera canónico.

## Documentos relacionados

- [Runbook del repositorio](../../docs/agent/RUNBOOK.md)
- [Pruebas documentales](../../docs/agent/TESTS.md)

## Prompts compatibles

- [Release readiness](../../library/domains/delivery-platform/prompts/release-readiness-review.prompt.md)

## Skills relacionadas

- [Auditoría documental](../../library/domains/documentation-knowledge/skills/documentation-audit/SKILL.md)

## Ejemplo

Servir la raíz, verificar `200` para el shell, páginas parciales y Markdown cargado, recorrer hashes y reportar cualquier `404` sin desplegar.

## Procedencia

Proyección generada del activo canónico [`library/domains/delivery-platform/skills/github-pages-release/SKILL.md`](../../library/domains/delivery-platform/skills/github-pages-release/SKILL.md).

No edites este archivo: modifica la fuente en `library/` y ejecuta `npm run build:skills`.
La puerta de calidad falla si esta proyección queda desactualizada.
