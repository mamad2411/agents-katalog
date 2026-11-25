---
name: mapear-negocio
description: Mapea el negocio de la persona en marketing, ventas y producto, ubica cada proceso en Nivel 1 (hablar con la IA), Nivel 2 (skill) o Nivel 3 (rutina), dice qué queda siempre en sus manos y elige los 3 procesos que más rinden si suben un nivel. Usar con /mapear-negocio, "qué automatizo primero", "mapeá mi negocio".
---

# /mapear-negocio — proceso por proceso, en qué nivel va la IA

Un negocio son tres cosas: **marketing** (traer ojos que se conviertan), **ventas** (que paguen y vuelvan a pagar) y **producto** (lo que entregás, mejorado con lo que dicen los que pagan). El marketing potencia las ventas y las ventas potencian el producto. Por eso el que le mete 50 funciones a un producto sin clientes hizo todo al revés.

## 1 · Leé antes de preguntar

`WIKI/negocio.md`, `WIKI/yo.md`, `MEMORIA/` y lo que haya en `OUTPUTS/`. Fijate la **etapa**:
- **Sin oferta validada** → el foco es el **testeo diario**: una oferta por día, bien hecha, sabiendo qué testeás. La IA trabaja sobre todo en buscar y lanzar.
- **Con oferta validada** → el foco es **marketing**: creativos, landing, checkout, escala, backend. La IA trabaja en producir y escalar.

## 2 · Listá los procesos

Proponé la lista con lo que ya sabés y pedile que marque cuáles hace (en bloque, con opciones). Referencia de procesos típicos — usá solo los que apliquen y sumá los suyos:

**Marketing:** buscar ofertas o ideas que ya venden · crear creativos · lanzar y escalar campañas · abrir cuentas o canales nuevos cuando uno toca techo · contenido orgánico · email marketing · creadores y referidos.
**Ventas:** landing y checkout · upsells y downsells · recuperar checkouts abandonados · responder mensajes y leads · cobros, tarjetas rebotadas y disputas.
**Producto:** soporte · escuchar a los clientes (tickets, encuestas, bajas) · construir y arreglar · que nada se apague en silencio (vigilar que lo automático siga corriendo).

## 3 · Para cada proceso

| Proceso | Cada cuánto hoy | Nivel hoy | Nivel objetivo | Qué hace la IA | Qué queda en tus manos |
|---|---|---|---|---|---|

Para el nivel objetivo usá las tres preguntas de `CLAUDE.md` (frecuencia → ¿necesito verlo antes? → ¿se escribe como "si X, hacé Y"?). Patrones que suelen aparecer:
- Crear creativos o guiones → **N2**: la IA produce, vos aprobás uno por uno.
- Escalar campañas con reglas de ROAS → **N3**: la IA cumple tus reglas cada 15-30 minutos; vos escribís las reglas y mirás que se cumplan.
- Responder mensajes → **N2**: la IA lee el historial y deja la respuesta en tu voz; vos apretás enviar.
- Cobros y disputas → **N3** de lectura: detecta y avisa cada mañana; cómo se defiende cada caso es tuyo.
- Construir funciones → **N1/N2**: cada problema es distinto; qué se construye y probarlo antes de que lo vea un cliente es tuyo.

**La columna "qué queda en tus manos" nunca queda vacía.** Si no encontrás qué decide la persona, el proceso no está bien entendido.

Si te falta un dato para ubicar un proceso, **preguntá con opciones y tu recomendación**. No inventes frecuencias.

## 4 · Los 3 que más rinden

Marcá los 3 procesos que más tiempo devuelven si suben un nivel (frecuencia × tiempo por vez × qué tan estable es el método). Para cada uno: qué nivel, qué hace falta y el comando (`/crear-skill` o `/crear-rutina`).

**Empezá por el primero en la misma sesión** si la persona dice que sí. Un mapa sin el primer paso dado es un documento más.

## 5 · Guardá

- `OUTPUTS/AAAA-MM-DD-mapa-negocio.md`: la tabla completa + los 3 elegidos + lo que faltó saber.
- `WIKI/mapa-de-procesos.md`: el estado vivo (se actualiza cada vez que un proceso sube de nivel).
- `WIKI/index.md`: convertí la fila de `mapa-de-procesos.md` en link y sacá el "(nace con…)". Entrada arriba en `changelog/`.

## El patrón que vas a ver

La IA ejecuta en las tres áreas. Marketing suele tener más rutinas porque es lo que más se repite. Producto, más Nivel 1, porque cada problema es distinto. Y en todas, la decisión es de la persona.
