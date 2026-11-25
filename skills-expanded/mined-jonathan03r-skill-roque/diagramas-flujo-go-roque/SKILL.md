---
name: diagramas-flujo-go-roque
description: Usar cuando el usuario pida un diagrama de flujo de Go o cuando, al terminar una funcionalidad Go, su flujo real ayude a explicar el comportamiento implementado.
---

# Diagramas de flujo Go estilo Roque

Crear diagramas de flujo fieles al código Go y fáciles de leer. Usar estética Excalidraw limpia, etiquetas en español y guardar imagen PNG junto con la fuente editable.

## Cuándo usar

- Cuando el usuario pida un diagrama de flujo de una funcionalidad Go.
- Al terminar una funcionalidad Go, si el flujo explica una operación de usuario, reglas de negocio, integración externa, importación/exportación o decisiones relevantes. En ese caso, crear y mostrar el diagrama como parte de la entrega.
- No crear diagramas para helpers aislados, cambios puramente internos o flujos sin valor explicativo. Si el beneficio es dudoso, sugerirlo al usuario antes.

## Leer el flujo real

1. Leer `AGENTS.md` y las instrucciones del proyecto. Para Go, leer también `go-feature-architecture` si está disponible.
2. Revisar el código actual de la funcionalidad y seguir el recorrido desde su entrada real hasta su respuesta o efecto: export C, handler, caso de uso, servicio, almacenamiento o integración externa, según aplique.
3. Incluir ramas que cambien el resultado, los errores relevantes y los retornos tempranos. Omitir detalles internos que no ayuden a entender el flujo.
4. No inventar pasos. Si el código no permite confirmar una regla, marcarla como pendiente de confirmar o dejarla fuera.

## Diseño

- Escribir todos los textos visibles en español. Se pueden incluir nombres reales de funciones o archivos como referencia secundaria, nunca como sustituto de explicar el paso.
- Usar figura de palitos para una persona o actor que inicia, revisa o confirma una acción. No poner personas decorativas si el flujo es automático.
- Usar inicio/fin redondeados, procesos en cajas, decisiones en rombos, datos/archivos con símbolos claros y flechas direccionales. Rotular las salidas de decisiones con opciones como «Sí» y «No».
- Mantener dirección principal de izquierda a derecha o de arriba abajo, alineación consistente, espacio suficiente y pocas líneas cruzadas.
- Mantener estilo Excalidraw sobrio: trazo bajo (roughness 0 o 1), tipografía legible, fondo claro y paleta pequeña con significado consistente. No llenar el lienzo de iconos, sombras ni colores decorativos.
- Dividir en más de un diagrama si un único lienzo deja texto pequeño o vuelve confuso el recorrido.

## Archivos y entrega

- Respetar la carpeta de documentación que ya defina el proyecto. Si no existe una convención, usar `docs/diagramas/`.
- Guardar el PNG con nombre descriptivo, por ejemplo `docs/diagramas/flujo-descarga-sire.png`, y guardar al lado la fuente editable `.excalidraw`.
- Exportar desde Excalidraw o mediante un exportador disponible. No instalar herramientas o dependencias ni ejecutar `npx skills add` sin autorización explícita.
- Revisar visualmente el PNG: textos legibles, flechas conectadas y sin recortes ni cruces evitables. Confirmar que el `.excalidraw` conserva el diagrama editable.
- Al responder, explicar qué flujo representa, enlazar la imagen y la fuente, y mostrar la imagen con una ruta absoluta cuando la interfaz lo permita. No decir que el PNG está listo si solo se generó la fuente editable.
