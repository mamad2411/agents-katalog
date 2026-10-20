---
name: ux-writing-microcopy
description: El texto como parte de la interfaz — botones que nombran la acción, títulos y estados vacíos que orientan, mensajes de error accionables y sin culpar al usuario, tono y voz consistentes, etiquetas de formulario, confirmaciones destructivas y español claro con consideración de i18n. Usar al DECIDIR qué dice un botón, label, mensaje de error, estado vacío, confirmación o notificación, al traducir jerga técnica del backend a lenguaje humano, o cuando un flujo confunde por lo que dice y no por cómo se ve. No hace falta para aplicar un texto que ya viene decidido.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# UX writing y microcopy — el texto también es interfaz

El copy de la UI se usa, no se lee: guía la acción. Un buen texto evita un rediseño.
Complementa a `frontend-ux-states` (qué estado se muestra) y a `ux-clarity-usability`
(que el flujo se entienda). Acá se define **qué dicen** esos estados y controles.

## 1. Principios

- **Claro antes que ingenioso**: la persona quiere terminar la tarea, no admirar el copy.
- **Breve y específico**: cada palabra se gana su lugar; cortá relleno ("por favor tenga
  en cuenta que...").
- **Lenguaje del usuario**, no del sistema: "No pudimos guardar los cambios", no
  "Error 500: null constraint violation".
- **Orientado a la acción y en su idioma**: verbo que dice qué pasa.
- **Consistente**: un concepto, una palabra en todo el producto (no mezclar
  "cita"/"turno"/"consulta" para lo mismo — decidí y respetá).

## 2. Botones y acciones

- El botón nombra su acción, no "Aceptar/OK": `Guardar cambios`, `Enviar solicitud`,
  `Eliminar paciente`. Al leer solo el botón se sabe qué va a pasar.
- Primera persona/impersonal consistente; verbo en infinitivo o imperativo, elegí uno.
- El botón primario = la acción que la pantalla quiere; el secundario, en tono menor
  ("Cancelar" nunca compite visualmente con "Guardar").

```
❌  [ Aceptar ]   [ Cancelar ]      (¿aceptar qué?)
✅  [ Eliminar cita ]   Cancelar
```

## 3. Mensajes de error accionables

Un buen error responde tres cosas: **qué pasó**, **por qué**, **qué hago ahora**. Y nunca
culpa al usuario ni muestra el error crudo del backend.

```
❌  "Entrada inválida."
❌  "Error: ECONNREFUSED"
✅  "No pudimos guardar la cita: ese horario ya está ocupado. Elegí otro horario."
```

- Ubicá el error donde ocurre: el de un campo, junto al campo (ver `frontend-forms-ux`);
  el general, arriba del formulario, no en un toast que desaparece.
- Ofrecé la salida: reintentar, corregir el dato, contactar soporte.
- Tono neutro: "El correo no es válido", no "Ingresaste mal el correo".

## 4. Estados vacíos y de carga

- El vacío orienta y ofrece la primera acción: "Todavía no tenés citas. Creá la primera."
  — nunca una pantalla en blanco (ver `frontend-ux-states`).
- Distinguí "vacío porque es nuevo" de "vacío porque el filtro no encontró nada": el
  segundo sugiere ajustar el filtro.
- Títulos que dicen qué es la pantalla, no saludos huecos ("Bienvenido a tu dashboard").

## 5. Etiquetas de formulario

- Label visible y estable (no solo placeholder, que desaparece al escribir y no es
  accesible — ver `frontend-accessibility`).
- Decí qué formato esperás cuando importa ("Fecha (DD/MM/AAAA)") y marcá lo opcional, no
  lo requerido, si la mayoría es requerida.
- Texto de ayuda breve bajo el campo, no un tooltip escondido, para lo que necesita contexto.

## 6. Confirmaciones destructivas

- El diálogo nombra el objeto y la consecuencia: "¿Eliminar la cita de María López del
  12/03? Esta acción no se puede deshacer."
- El botón de confirmar nombra la acción destructiva (`Eliminar`), no "Sí"; el de escape,
  claro (`Cancelar`).
- Reservá la confirmación para lo irreversible; para lo reversible, actuá y ofrecé
  deshacer (menos fricción, ver `ux-clarity-usability` §5).

## 7. Tono, voz e i18n

- Definí una voz (cercana pero profesional, en un producto de salud: seria, respetuosa,
  sin chistes con datos clínicos) y sostenela.
- Nada de humor ni ansiedad en contextos sensibles (resultados, pagos, errores clínicos).
- Escribí pensando en traducción: evitá modismos difíciles de localizar, no concatenes
  frases con variables en medio ("Tenés " + n + " citas" se rompe en plurales/género —
  usá cadenas con formato y plurales, ver `frontend-i18n-l10n`).
- No metas texto en imágenes; que todo el copy sea texto real y traducible.

## Checklist

- [ ] Cada botón nombra su acción (nada de "Aceptar/OK" ambiguos).
- [ ] Los errores dicen qué pasó, por qué y qué hacer; sin jerga ni culpa.
- [ ] Los vacíos orientan y ofrecen la primera acción.
- [ ] Labels visibles y estables; formato indicado donde importa.
- [ ] Confirmación destructiva nombra objeto y consecuencia; el botón nombra la acción.
- [ ] Un concepto = una palabra en todo el producto.
- [ ] Copy como texto real y localizable, listo para i18n.
