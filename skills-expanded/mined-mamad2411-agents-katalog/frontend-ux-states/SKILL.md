---
name: frontend-ux-states
description: Estados obligatorios de cualquier vista o componente que trae/muta datos — carga, vacío, error, parcial, éxito, sin permiso y offline — más patrones de feedback, redacción de errores y confirmación destructiva. Usar al construir cualquier pantalla o componente que dependa de una llamada a red, al revisar un flujo antes de darlo por terminado, o cuando un bug reportado es "la pantalla queda rara" en algún caso límite.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Estados de UI — lo que toda vista real tiene que resolver

Una vista que solo maneja el "camino feliz" (datos ya cargados, sin errores) no está
terminada. Antes de dar un componente por listo, recorré esta lista de estados y
decidí explícitamente qué hace cada uno — no lo dejes en blanco por omisión.

## 1. Los estados obligatorios

| Estado | Cuándo ocurre | Tratamiento mínimo |
|---|---|---|
| Carga inicial | Primera petición, sin datos previos en pantalla | Skeleton con la forma del contenido final, o spinner si no hay forma que anticipar |
| Carga en segundo plano | Refetch/paginación con datos previos visibles | Indicador no bloqueante (barra fina, spinner chico en el borde); no tapar el contenido existente |
| Vacío | La petición tuvo éxito pero no hay datos | Mensaje que explica el porqué + acción para salir del estado (crear, cambiar filtro, invitar) — nunca una pantalla en blanco |
| Error | La petición falló (red, servidor, timeout) | Mensaje en lenguaje humano + acción de reintentar; nunca el error crudo del backend |
| Parcial / degradado | Algunos datos llegaron, otros fallaron (ej. un widget del dashboard) | Mostrar lo que sí llegó; marcar solo la parte fallida, no tirar toda la vista |
| Éxito | Datos completos y correctos | El camino feliz — el que casi siempre se diseña primero |
| Sin permiso | El usuario no tiene acceso a esta vista/acción | Mensaje explícito de por qué no puede, no un 404 genérico ni la acción deshabilitada sin explicación |
| Offline / sin conexión | Se perdió la red durante el uso | Aviso persistente pero no bloqueante; encolar acciones si aplica, o bloquear con mensaje claro |

Checklist rápido al revisar un componente: si solo puede mostrar "éxito" y "cargando",
faltan al menos vacío, error y sin permiso.

## 2. Skeletons vs. spinners

- Skeleton (placeholder con la forma aproximada del contenido final) cuando la carga
  dura lo suficiente como para percibirse Y ya sabés la forma que va a tener el
  contenido (lista, tarjeta, tabla) — reduce la sensación de espera y evita el salto
  de layout cuando llega el dato real.
- Spinner genérico cuando la forma del resultado es impredecible (una acción puntual,
  un submit) o la espera es tan corta que un skeleton solo agrega ruido visual.
- Nunca combines spinner Y skeleton para la misma carga — elegí uno.
- El skeleton respeta las mismas dimensiones que el contenido final para no causar
  layout shift al reemplazarlo (ver `frontend-performance`, CLS).

## 3. UI optimista vs. pesimista

- Optimista: aplicar el cambio en la UI antes de que el servidor confirme (like,
  marcar como leído, reordenar). Usalo cuando la operación casi siempre tiene éxito
  y el costo de un rollback visual es bajo. Siempre con revert automático + aviso
  si el servidor rechaza.
- Pesimista: esperar confirmación del servidor antes de reflejar el cambio. Usalo
  para operaciones con consecuencias (pagos, envíos, borrados) donde mostrar un
  éxito falso es peor que la espera.
- Nunca dejes un cambio optimista sin manejo de fallo — si no revertís visualmente,
  el usuario queda con un estado que miente sobre lo que pasó en el servidor.

## 4. Redacción de errores y microcopy

- El mensaje dice qué pasó, en qué afecta al usuario, y qué puede hacer — nunca
  solo el código o la excepción cruda.
- Nunca exponer detalles internos (stack trace, nombre de tabla, SQL, mensaje del
  proveedor cloud) en el mensaje visible al usuario — eso es información de logs,
  no de UI (y también un problema de seguridad, ver `security-guardrails`).
- Tono consistente con el resto del producto; sin culpar al usuario ("Hiciste mal
  el formulario" → "Revisá el formato del email").
- Errores de validación de formulario: específicos por campo, no un banner genérico
  arriba de todo el formulario que obliga a adivinar cuál campo falló (ver
  `frontend-accessibility` para cómo asociarlos accesiblemente).

```text
❌ "Error 500: Internal Server Error"
❌ "Algo salió mal"
✅ "No pudimos guardar los cambios. Revisá tu conexión e intentá de nuevo."
   [Reintentar]
```

## 5. Feedback: toast vs. inline vs. modal

- Toast/snackbar: confirmaciones no críticas de acciones que el usuario ya inició
  y espera que funcionen ("Guardado", "Copiado al portapapeles") — desaparece solo,
  no bloquea, no requiere respuesta.
- Inline: feedback ligado a un elemento concreto de la pantalla (error de un campo,
  estado de un ítem de lista) — se queda mientras la condición exista.
- Modal/diálogo: solo cuando la acción es irreversible, cara de deshacer, o requiere
  una decisión antes de continuar. Un modal para "Guardado con éxito" es fricción
  innecesaria — eso es un toast.

## 6. Undo vs. confirmación destructiva

- Para acciones reversibles y baratas de deshacer (archivar, borrar un ítem de lista,
  mover a papelera): ejecutá inmediato y ofrecé "Deshacer" en un toast con ventana de
  tiempo — menos fricción que interrumpir con un diálogo.
- Para acciones irreversibles o caras (borrado permanente, envío de dinero, cierre de
  cuenta): confirmación explícita antes de ejecutar, con el nombre/cantidad concreta
  del recurso afectado en el texto del diálogo, no un "¿Estás seguro?" genérico.
- Nunca uses undo-toast para algo que en realidad no se puede deshacer — es peor
  que confirmar de más: genera confianza falsa.

## 7. Validación de formularios

- Validá en el momento adecuado: al salir del campo (`blur`) para errores de formato,
  no en cada tecla (interrumpe mientras el usuario todavía está escribiendo); en el
  submit, revalidá todo antes de enviar.
- Una vez que un campo mostró error, revalidalo en vivo mientras el usuario corrige,
  para confirmar apenas se resuelve — no lo hagas esperar hasta el próximo submit.
- Deshabilitar el botón de submit sin explicación de por qué es peor que dejarlo
  habilitado y mostrar los errores al hacer click — un botón deshabilitado sin
  contexto no comunica qué falta.

## 8. Divulgación progresiva

- No mostrós toda la complejidad de entrada: la configuración avanzada, los filtros
  raros usados por el 5%, los detalles técnicos van detrás de un "Más opciones" o
  una sección colapsable — la vista por defecto resuelve el caso común.
- Cada nivel de divulgación agrega información, nunca la contradice ni obliga a
  deshacer lo elegido en el nivel anterior.

## Checklist de estados faltantes (correr sobre cada vista/componente nuevo)

- [ ] ¿Qué se ve en la primera carga, antes de tener datos?
- [ ] ¿Qué se ve si la petición no trae resultados (lista vacía, búsqueda sin match)?
- [ ] ¿Qué se ve si la petición falla, y hay forma de reintentar?
- [ ] ¿Qué pasa si solo una parte de los datos falla?
- [ ] ¿Qué ve un usuario sin permiso para esta vista/acción?
- [ ] ¿Qué pasa si se pierde la conexión a mitad de una acción?
- [ ] ¿Los mensajes de error son legibles por un humano y accionables?
- [ ] ¿Las acciones destructivas piden confirmación o dan undo, según su costo real de deshacer?
- [ ] ¿El feedback usa el canal correcto (toast/inline/modal) para su nivel de importancia?
