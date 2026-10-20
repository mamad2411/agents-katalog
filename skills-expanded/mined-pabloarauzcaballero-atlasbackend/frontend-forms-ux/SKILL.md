---
name: frontend-forms-ux
description: UX de formularios — cuándo validar, errores claros y accionables por campo, preservar lo escrito ante fallo, estados de envío sin doble submit, formularios largos por pasos, autosave de borradores y accesibilidad. Usar al diseñar o revisar cualquier formulario (alta de usuario/profesional, agenda, cotización), cuando un formulario "frustra" o pierde datos, o al decidir cómo mostrar los errores de validación y del servidor.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# UX de formularios

La mecánica (tipado, validadores, mapeo de errores) la fija el framework del repo. Acá va la
experiencia: que el usuario complete el formulario rápido, entienda los errores y no pierda lo
que escribió. Un formulario mal resuelto es donde más se cae la conversión.

## 1. Validar en el momento correcto

- No grites errores mientras el usuario todavía está escribiendo un campo por primera vez.
  Validá **al salir del campo** (`blur`) para el primer error, y a partir de ahí en cada cambio.
  En Angular, `updateOn: 'blur'` para el primer paso.
- La validación de éxito puede mostrarse en vivo (p.ej. "usuario disponible") si ayuda.
- No deshabilites el botón de enviar de entrada: dejá que el usuario intente y mostrá qué falta
  (un botón gris sin explicación confunde). Alternativa válida: habilitado + resumen de errores al enviar.

## 2. Errores claros, por campo y accionables

- El mensaje va **junto al campo**, no solo en un resumen arriba.
- Decí qué hacer, no solo qué está mal: "Ingresá un correo válido, ej. nombre@dominio.com",
  no "Valor inválido". Sin culpar al usuario (ver `ux-writing-microcopy`).
- Al enviar con errores, llevá el foco al primer campo con error y mostralo.
- Errores del servidor (422): mapealos al campo correspondiente, no a un toast genérico
  (ver `error-handling-contract`).

## 3. Nunca perder lo escrito

- Si el envío falla (red, 422, 500), **conservá todos los valores**. Reconstruir el formulario
  vacío tras un error es la peor ofensa.
- Avisá antes de abandonar un formulario con cambios sin guardar (guard de navegación).
- Para formularios largos, considerá autosave de borrador (local o en servidor) y restaurarlo
  al volver — con cuidado de no persistir datos sensibles en el cliente (ver `data-privacy-sensitive`).

## 4. Estado de envío, sin doble submit

- Al enviar: deshabilitá el botón y mostrá estado de carga; reactivalo al terminar.
- Prevení el doble submit (clic doble / reintento): en la UI y con clave de idempotencia en el
  backend (ver `concurrency-and-locking`).
- Confirmá el éxito de forma inequívoca (mensaje, navegación, o el dato ya reflejado).

## 5. Formularios largos por pasos

- Partí formularios largos en pasos con progreso visible; validá cada paso antes de avanzar.
- Permití volver atrás sin perder datos; resumen final antes de confirmar.
- Agrupá campos relacionados; una sola columna suele leerse mejor que dos.
- Pedí lo mínimo: cada campo extra baja la tasa de completado.

## 6. Accesibilidad y detalle

- Cada control con `<label>` asociado; error vinculado con `aria-describedby` y el campo
  marcado `aria-invalid` (ver `frontend-accessibility`).
- `type`/`inputmode`/`autocomplete` correctos (email, tel, one-time-code) para teclado y autollenado.
- Target táctil suficiente; no dependas solo del color rojo para señalar error (ícono + texto).

## Anti-patrones

- Validar en cada tecla desde el primer carácter (ansiedad).
- Error genérico ("Error al guardar") sin decir qué campo ni qué hacer.
- Vaciar el formulario tras un fallo de envío.
- Botón de enviar que dispara dos veces y crea el recurso duplicado.
- Formulario gigante de una sola pantalla con 30 campos.

## Checklist

- [ ] Primer error al `blur`, no en cada tecla; foco al primer error al enviar.
- [ ] Errores por campo, accionables; 422 del servidor mapeado al campo.
- [ ] Los datos se preservan ante cualquier fallo de envío; aviso al abandonar con cambios.
- [ ] Botón con estado de carga y sin doble submit (UI + idempotencia).
- [ ] Formularios largos por pasos con progreso y vuelta atrás.
- [ ] Labels, `aria-invalid`/`aria-describedby`, `inputmode`/`autocomplete`, error no solo por color.
