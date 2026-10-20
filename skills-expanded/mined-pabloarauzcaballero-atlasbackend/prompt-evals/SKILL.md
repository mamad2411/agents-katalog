---
name: prompt-evals
description: Gate de evaluación para cambios en skills, prompts, subagentes y CLAUDE.md — set dorado de casos por skill, pruebas de disparo (se activa cuando debe y no cuando no debe), regresión al editar, rúbricas, LLM-como-juez con sus sesgos, comparación A/B con varianza y criterio de merge. Usar antes de mergear cualquier edición a una description o al cuerpo de una skill, al agregar una skill que compite con otra, al cambiar de modelo, o cuando alguien dice "lo mejoré" sin casos que lo respalden.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Evals de prompts — gate de merge

Editar un prompt sin casos es editar código sin tests: no sabés qué rompiste. Este gate convierte
"me parece que quedó mejor" en una comparación reproducible. Un cambio de prompt **no se mergea**
sin la evidencia de la sección final.

## 1. Qué se evalúa

| Pregunta | Tipo de prueba | Falla típica |
|---|---|---|
| ¿Se carga cuando debe? | Disparo positivo | Description vaga, vocabulario distinto al del pedido |
| ¿Se queda quieta cuando no debe? | Disparo negativo | Description demasiado amplia, énfasis en mayúsculas |
| ¿Gana la skill correcta entre vecinas? | Disparo por confusión | Fronteras no declaradas entre skills hermanas |
| Una vez cargada, ¿cambia la conducta? | Comportamiento (set dorado) | Reglas motivacionales, ejemplos pobres |
| ¿Sigo pasando lo que pasaba? | Regresión | Arreglar un caso rompiendo otros |

## 2. Set dorado por skill

Vive junto a la skill (`evals/cases.yaml` o equivalente; definí el formato una vez para todo el repo).
Mínimo de la casa: **8 positivos de disparo, 8 negativos, 3 de confusión por cada vecina, 5 de comportamiento.**

```yaml
- id: trig-pos-03
  kind: trigger_positive
  prompt: "el listado de pacientes tarda 9 segundos con 50 mil filas, fijate qué pasa"
  expect_skill: code-efficiency
- id: trig-neg-02
  kind: trigger_negative
  prompt: "renombrá esta variable a algo más claro"
  expect_not: code-efficiency
- id: beh-04
  kind: behavior
  prompt: "agregá cache a este endpoint"
  fixture: fixtures/endpoint-sin-medicion/
  must: ["pide o toma una medición antes de proponer cache", "define invalidación"]
  must_not: ["agrega cache sin medir"]
```

Reglas para escribir casos:
1. Salen de **pedidos reales** (historial, issues, carriles), con su redacción imperfecta. Un caso escrito por quien escribió la skill usa las mismas palabras que la description y siempre pasa.
2. Cada bug de prompt encontrado en uso se convierte en caso antes de arreglarlo (igual que un test de regresión).
3. Los negativos más valiosos son los **casi-positivos**: pedidos del mismo dominio que corresponden a otra skill.
4. `must`/`must_not` observables en la salida o en las acciones (herramientas usadas, archivos tocados), no intenciones.
5. Los fixtures son mínimos y sintéticos. Nunca datos reales de personas (ver `data-privacy-sensitive`).

## 3. Ejecución

- Corré cada caso en **sesión limpia**, no interactiva (`claude -p` o el harness del repo), con el mismo modelo, esfuerzo y conjunto de skills instalado que producción. El disparo depende de qué otras skills compiten: probar una skill sola da falsos positivos.
- El disparo se observa en la **traza** (qué skill se invocó), no preguntándole al modelo si la usaría.
- La salida es no determinista: corré cada caso **N veces** (mínimo de la casa: 5) y reportá tasa de acierto, no un pasa/no pasa de una corrida.
- Registrá costo: tokens de descriptions cargadas por sesión y tokens del cuerpo al invocarse. Una skill que mejora 2 % y duplica el contexto permanente no es una mejora.

## 4. Cómo se califica

Preferí, en este orden:

1. **Chequeo por código**: skill invocada, archivo creado, comando ejecutado, JSON válido contra esquema, regex sobre la salida. Barato, estable, sin sesgo.
2. **Rúbrica binaria** por criterio (cumple / no cumple), cada criterio independiente y redactado como hecho verificable. Evitá escalas 1–10: nadie calibra igual un 6.
3. **LLM-como-juez**, solo para lo que 1 y 2 no alcanzan.

### Sesgos del juez y su mitigación

| Sesgo | Mitigación |
|---|---|
| Posición (prefiere la primera o la última opción) | Evaluar cada par en ambos órdenes; contar solo veredictos consistentes |
| Verbosidad (premia lo más largo) | Rúbrica que penaliza relleno; criterios binarios, no "calidad general" |
| Auto-preferencia (favorece su propio estilo) | Juez de otro modelo o configuración cuando se pueda; ciego a cuál es A y cuál es B |
| Aquiescencia (acepta afirmaciones sin evidencia) | Pedir cita textual de la salida que justifica cada veredicto |
| Deriva del juez | Congelar prompt y modelo del juez; versionarlos junto con los casos |

Calibrá el juez: tomá ~20 salidas, calificalas a mano, y medí acuerdo juez-humano. Si no coincide
razonablemente con vos, el juez está midiendo otra cosa: arreglá la rúbrica antes de confiar en él.
El juez recibe la rúbrica y la salida, **nunca** la pista de cuál variante es la nueva.

## 5. Comparación A/B

1. Misma batería, mismo modelo, mismo N, mismas skills vecinas. Una sola variable cambia.
2. Reportá por caso y agregado: tasa A, tasa B, diferencia.
3. Con N chico, diferencias pequeñas son ruido. Regla de la casa: si la diferencia agregada no supera la variación que ves entre dos corridas idénticas de A contra A, **no hay evidencia de mejora**. Medí ese piso de ruido al menos una vez por batería.
4. Mirá los casos que cambiaron de signo, no solo el promedio: un +5 % que rompe un caso de seguridad no entra.
5. Al cambiar de modelo, re-corré todo: las descriptions calibradas para un modelo sobre- o sub-disparan en otro (ver `prompt-engineering` §8).

## 6. Criterio de merge

Un cambio a un prompt entra si y solo si:

- **Cero regresiones** en casos marcados `blocking` (seguridad, privacidad, acciones destructivas, gates de evidencia).
- Disparo negativo no empeora: la tasa de falsos disparos es ≤ a la de la versión anterior.
- El caso que motivó el cambio ahora pasa de forma estable (≥ 4 de 5 corridas, o el umbral que fije el repo).
- El agregado no baja más que el piso de ruido.
- Costo de contexto permanente (descriptions) no sube sin justificación escrita.

Si el cambio es solo editorial (typos, reordenar sin alterar reglas), alcanza con disparo + casos `blocking`.

## 7. Qué registrar

Por corrida: commit del prompt, id de la batería, modelo y esfuerzo, N, lista de skills instaladas,
resultado por caso, costo en tokens, versión del juez si lo hubo, fecha. Sin esto el resultado no
es reproducible ni comparable con la próxima edición. Guardá las salidas crudas de los casos que
fallan: son el insumo del arreglo (ver `root-cause-debugging`: una causa por vez).

## Anti-patrones

- Probar con el mismo pedido que usaste para escribir la description.
- Una sola corrida por caso; concluir de un 1/1.
- Juez que sabe cuál variante es "la nueva".
- Casos que verifican redacción exacta en vez de conducta.
- Arreglar el prompt para un caso y no re-correr el resto.
- Borrar o relajar un caso que falla para poder mergear (equivale a `test.skip`).
- Medir calidad e ignorar costo de contexto.

## Checklist

- [ ] La skill tiene set dorado con el mínimo de la casa, salido de pedidos reales.
- [ ] Casos de confusión contra cada skill vecina declarada en la description.
- [ ] Sesión limpia, con las skills vecinas instaladas, mismo modelo que producción.
- [ ] N ≥ 5 por caso; piso de ruido A-vs-A medido.
- [ ] Calificación por código donde se puede; juez ciego, calibrado y versionado donde no.
- [ ] Casos `blocking` sin regresión; falsos disparos no aumentan.
- [ ] Costo de contexto registrado antes y después.

## Evidencia / DoD

Para afirmar "el cambio de prompt está listo para merge" pegá, literal:

1. Comando de ejecución de la batería y commit evaluado (A y B).
2. Tabla por tipo de caso: aciertos/N de A y de B, y el piso de ruido medido.
3. Lista de casos que cambiaron de signo, con id, y la salida cruda de los que empeoraron.
4. Estado de los casos `blocking`: todos con su tasa.
5. Tokens de descriptions por sesión antes y después.
6. **No cubierto**: qué conductas de la skill no tienen caso todavía.

Sin los seis puntos el veredicto es BLOCKED, no PASS (ver `evidence-and-verification`).
