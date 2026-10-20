---
name: ux-clarity-usability
description: Claridad y usabilidad de una interfaz — que se entienda sin esfuerzo. Cubre la acción primaria única por pantalla, reducción de carga cognitiva, affordances y significantes, prevención de errores, reconocer en vez de recordar, feedback inmediato, divulgación progresiva y las 10 heurísticas de Nielsen aplicadas con ejemplos. Usar al diseñar o revisar cualquier flujo o pantalla, cuando un usuario "no sabe qué hacer" o "se pierde", y antes de dar por terminada una vista con la que alguien va a operar.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Claridad y usabilidad — que se entienda sola

Una pantalla clara se usa sin leer un manual y sin pensar. Esto no es estética
(`frontend-beautiful-ui`) ni jerarquía visual (`visual-hierarchy-composition`): es que la
persona sepa **qué puede hacer, qué está pasando y qué pasó**.

## 1. La prueba de los 3 segundos

Un usuario nuevo, en 3 segundos y sin leer todo, debería saber: dónde está, cuál es la
acción principal, y qué mirar primero. Si no, la pantalla está indecisa. Una vista =
una tarea primaria; si hay dos acciones igual de importantes, decidí cuál gana o partí
la vista.

## 2. Carga cognitiva: sacá trabajo de la cabeza del usuario

- **Reconocer > recordar**: mostrá las opciones, no obligues a memorizar. Un campo que
  pide "el código del último paso" cuando podrías mostrarlo es carga innecesaria.
- Valores por defecto sensatos: el camino común no debería requerir decisiones.
- Agrupá y ocultá lo avanzado (divulgación progresiva): mostrá lo esencial primero y
  revelá el resto bajo demanda ("Opciones avanzadas"), no todo de golpe.
- Cortá pasos y campos: cada campo de un formulario es una fricción; pedí solo lo que
  necesitás ahora.

## 3. Affordances y significantes

- Lo clicable parece clicable; lo no clicable, no. Un texto azul subrayado invita a
  clic; una tarjeta con `cursor: pointer` y sin feedback confunde.
- El significante (la pista visual) debe coincidir con la acción real: un ícono de
  basura borra, no archiva.
- Estados visibles: hover, foco, activo, deshabilitado, seleccionado — si un control no
  reacciona al mouse ni al teclado, el usuario duda si funciona.

## 4. Feedback: nunca dejar a oscuras

- Toda acción confirma qué pasó: un guardado muestra "guardado", no silencio.
- Respuesta inmediata (< ~100 ms percibido) para clics; para esperas más largas, estado
  de carga con la forma del resultado (ver `frontend-ux-states`).
- El sistema comunica su estado: qué está sincronizando, qué falló, qué quedó pendiente.

## 5. Prevención de errores > mensajes de error

El mejor error es el que no ocurre:

- Deshabilitá o escondé lo que no aplica en el estado actual en vez de dejar que falle.
- Restringí la entrada al formato válido (selector de fecha en vez de texto libre).
- Confirmá lo destructivo e irreversible; permití deshacer lo reversible (ver
  `ux-writing-microcopy` para el copy de estas confirmaciones).
- Preservá el trabajo: nunca borres lo que el usuario escribió por un error de validación.

## 6. Las 10 heurísticas de Nielsen (checklist aplicable)

1. Visibilidad del estado del sistema — ¿la UI dice qué está pasando?
2. Correspondencia con el mundo real — lenguaje del usuario, no jerga técnica del backend.
3. Control y libertad — salidas claras, deshacer, cancelar; nada de callejones sin salida.
4. Consistencia y estándares — lo mismo se ve y se llama igual en todo el producto.
5. Prevención de errores — ver §5.
6. Reconocer antes que recordar — ver §2.
7. Flexibilidad y eficiencia — atajos para expertos sin estorbar al novato.
8. Diseño estético y minimalista — cada elemento extra compite con lo relevante.
9. Ayudar a reconocer y recuperarse de errores — mensaje claro + cómo salir (`ux-writing-microcopy`).
10. Ayuda y documentación — accesible en contexto cuando hace falta.

## 7. Cómo detectar una pantalla confusa

- No podés nombrar la acción primaria en una frase.
- Hay que explicarla en persona para que alguien la use.
- Dos elementos parecen hacer lo mismo, o el mismo concepto se llama distinto en dos lados.
- El usuario pregunta "¿y ahora qué?" o "¿se guardó?".
- Un test rápido con alguien ajeno tarda o se equivoca en la tarea principal.

## Checklist

- [ ] Una tarea primaria por pantalla, evidente en 3 segundos.
- [ ] Defaults sensatos; lo avanzado, oculto hasta pedirlo.
- [ ] Lo interactivo se ve interactivo y tiene estados (hover/foco/activo/disabled).
- [ ] Toda acción da feedback; el sistema comunica su estado.
- [ ] Errores prevenidos donde se puede; lo destructivo se confirma, lo reversible se deshace.
- [ ] Lenguaje del usuario, consistente en todo el producto.
- [ ] Pasé las 10 heurísticas de Nielsen sobre el flujo real.
