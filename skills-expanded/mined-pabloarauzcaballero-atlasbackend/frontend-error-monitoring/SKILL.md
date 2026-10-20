---
name: frontend-error-monitoring
description: Monitoreo de errores del cliente web — `ErrorHandler` global de Angular, captura de errores de render, de promesas no manejadas y de red, correlación con el backend por request id, reporte a una herramienta con source maps, breadcrumbs de la sesión, y la regla de no loguear datos sensibles. Usar al montar el reporte de errores de la app, al decidir qué se captura y qué se manda, al correlacionar un error del front con su traza en el backend, o al revisar por qué los errores de producción "no se ven".
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Monitoreo de errores del cliente

Un error que el usuario ve y vos no, no existe hasta que rompe la confianza. El cliente debe
capturar sus fallos, reportarlos con contexto suficiente para reproducirlos, y hacerlo sin
filtrar datos sensibles.

## 1. Capturar todo, en un solo lugar

Registrá un `ErrorHandler` global de Angular para los errores de render/DI, y enganchá los
dos canales que Angular no cubre solo: promesas rechazadas y errores globales.

```typescript
@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  private reporter = inject(ErrorReporter);
  handleError(error: unknown): void {
    this.reporter.capture(error);      // no re-lanzar hacia el usuario
    console.error(error);               // en dev
  }
}
// provideAppInitializer / main.ts:
// window.addEventListener('unhandledrejection', e => reporter.capture(e.reason));
// window.addEventListener('error', e => reporter.capture(e.error));
```

Los errores de red los mapea la capa de datos del cliente: decidí
cuáles son esperados (un 404 de "no existe") y no valen reporte, y cuáles son fallos reales.

## 2. Correlacionar con el backend

- La capa de datos agrega un request id / `traceparent` a cada llamada (ver
  `backend-observability`). Cuando falla una request, incluí ese id en el reporte del front.
- Así un error visto en el cliente se une a su traza en el servidor: dejás de adivinar.

## 3. Qué mandar — y qué NO

- Mandá: tipo de error, stack, ruta, versión/commit desplegado, request id, navegador, y
  breadcrumbs (últimas acciones/rutas).
- **No mandes datos sensibles ni datos personales**: no incluyas el body de la respuesta, valores de
  formularios con datos de pacientes, tokens ni la URL con parámetros sensibles. Scrubbeá
  antes de enviar (ver `data-privacy-sensitive`). Esto aplica también a la herramienta de terceros:
  configurá su masking.

## 4. Source maps y versión

- Subí los source maps a la herramienta de reporte (privados, no servidos al público) para
  ver stacks legibles en producción.
- Etiquetá cada reporte con el commit/versión desplegado, para saber si un error es nuevo o de
  una versión vieja (ver `github-releases-versioning`).

## 5. Breadcrumbs y experiencia del usuario

- Registrá breadcrumbs (navegación, clics clave, llamadas de red) para reconstruir cómo llegó
  el usuario al error — sin capturar el contenido sensible que tipeó.
- Ante un error irrecuperable, mostrale al usuario un estado de error digno (no una pantalla en
  blanco ni un stack): mensaje claro + acción de recuperar/reintentar (ver `frontend-ux-states`).

## 6. Umbral y ruido

- No todo `console.error` es un incidente. Definí qué severidad reporta y alertá por síntomas
  (tasa de errores, no cada ocurrencia). Agrupá por huella para no ahogarte en duplicados.
- Revisá la cola de errores como parte del ciclo, no solo cuando alguien se queja.

## Anti-patrones

- No tener `ErrorHandler` global: los errores mueren en la consola del usuario.
- Mandar el body de la respuesta o los valores del formulario "para tener contexto" (datos sensibles).
- Stacks ofuscados en producción por no subir source maps.
- Reportar cada error como alerta individual (ruido → se ignora todo).
- Tragar el error (`catch {}`) y no reportarlo ni mostrar nada.

## Checklist

- [ ] `ErrorHandler` global + captura de `unhandledrejection` y `error`.
- [ ] Errores de red esperados filtrados; fallos reales reportados.
- [ ] Cada reporte lleva request id/commit para correlacionar con el backend.
- [ ] Sin datos sensibles, tokens ni bodies sensibles en el reporte; masking configurado.
- [ ] Source maps privados subidos; reportes etiquetados por versión.
- [ ] Breadcrumbs sin contenido sensible; estado de error digno para el usuario.
- [ ] Alerta por tasa/síntoma, agrupada por huella.
