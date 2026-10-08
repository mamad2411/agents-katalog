---
name: modo-produccion
description: Revisa una app/landing, detecta problemas típicos, propone mejoras y aplica correcciones con un checklist fijo para dejarlo listo para enseñar o publicar.
---

# Modo Producción (QA + Fix)

## Cuándo usar esta habilidad
- Cuando ya tienes algo generado (landing/app) y quieres dejarlo “presentable”.
- Cuando algo funciona “a medias” (móvil raro, imágenes rotas, botones sin acción, espaciados feos).
- Antes de enseñarlo a un cliente, grabarlo o publicarlo.

## Inputs necesarios (si faltan, pregunta)
1) Qué archivo es el principal (por ejemplo `index.html` o ruta del proyecto).
2) Objetivo de la revisión: “lista para enseñar” o “lista para publicar”.
3) Restricciones: no cambiar branding / no cambiar copy / no tocar estructura, etc.

## Checklist de calidad (orden fijo)

### A) Funciona y se ve
- Abre la preview / localhost sin errores.
- Imágenes cargan y no hay rutas rotas.
- Tipografías y estilos se aplican correctamente.

### B) Responsive (móvil primero)
- Se ve bien en móvil (no se corta, no hay scroll horizontal).
- Botones y textos tienen tamaños legibles.
- Secciones con espaciado coherente.

### C) Copy y UX básica
- Titular claro y coherente con la propuesta.
- CTAs consistentes (mismo verbo, misma intención).
- No hay texto “placeholder” tipo lorem ipsum.

### D) Accesibilidad mínima
- Contraste razonable en textos.
- Imágenes con alt.
- Estructura de headings (h1, h2) lógica.

## Workflow
1) Diagnóstico rápido: lista de problemas en 5–10 bullets (priorizados).
2) Plan de arreglos: “qué cambio y por qué” (máximo 8 cambios).
3) Aplicar cambios: modifica los archivos necesarios.
4) Validación: vuelve a abrir preview y confirma checklist.
5) Resumen final: cambios hechos + qué queda opcional para mejorar.

## Reglas
- No cambies el estilo de marca si existe un skill de marca activo.
- No rehagas todo: corrige lo mínimo para ganar calidad rápido.
- Si hay un conflicto entre “bonito” y “claro”, prioriza claridad.

## Output (formato exacto)
Devuelve siempre:
1) Diagnóstico (priorizado)
2) Cambios aplicados (lista corta)
3) Resultado: “OK para enseñar” / “OK para publicar” + notas
