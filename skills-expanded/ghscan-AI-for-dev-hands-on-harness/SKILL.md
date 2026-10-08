# Los skills: un procedimiento de trabajo y lo que desplazan

::: tip Objetivos de este módulo
- Saber qué es un skill en Pi, qué ve el modelo y qué no ve
- Distinguir entre una competencia que el modelo puede ignorar y una competencia que se le impone
- Escribir un procedimiento de trabajo que produzca un entregable utilizable
- Medir lo que desplaza y no confundir desplazar con mejorar
- Revisar un procedimiento a partir de las ejecuciones leídas y verificar la revisión mediante una nueva matriz
:::

El módulo anterior ha repasado lo que se gana al hacerlo mejor: elegir un modelo, ajustar un cursor, escribir un ticket, mantener un archivo de reglas. Terminó con una constatación. En las configuraciones que reciben el ticket delimitado, cuatro de cada veinte ejecuciones escriben los tests rojos que el ticket solicita y nunca abren `game/neon.js`: el modelo agota su presupuesto formulando los casos y no logra corregirlos. La única palanca que solucionó este problema consistió en proporcionarle los tests ya escritos, algo que nadie hará en un ticket real.

La pregunta de este módulo es, por lo tanto, si un **procedimiento de trabajo**, escrito una vez y recargado a petición, obtiene el mismo resultado sin proporcionar los tests.

Seguimos el orden habitual: comprender qué es un skill en el harness, escribir uno sobre este tema, medir lo que produce, luego revisarlo y volver a medir.

## Comprender

### Un skill es un archivo Markdown

Un **skill** es un archivo `SKILL.md` situado en un directorio `.pi/skills/<nombre>/` del proyecto, siguiendo el formato del estándar abierto [Agent Skills](https://agentskills.io). Se compone de un frontmatter, que incluye como mínimo un nombre y una descripción, y un cuerpo que contiene las instrucciones. No hay código, ni registro, ni configuración que prever: basta con depositar el archivo.

Aquí tienes un skill completo, deliberadamente minúsculo:

```markdown
---
name: revue-rapide
description: Relit les modifications en cours du dépôt. Utiliser quand l'utilisateur demande une relecture avant de commiter.
---

# Revue rapide

1. Lance `git diff` et lis toute la sortie.
2. Relève ce qui peut casser un test existant, puis ce qui manque de test.
3. Rends deux listes : « à corriger avant le commit » et « peut attendre ».
```

La idea es la de un procedimiento de trabajo que escribes una vez y que el agente recarga a petición, en lugar de volver a escribirlo en cada prompt. Ocupa un lugar aparte en el harness: `AGENTS.md` entra en el contexto en cada turno y, por lo tanto, tiene un coste en cada turno, mientras que un skill está diseñado para entrar solo cuando la tarea lo requiera.

### Qué ve el modelo

Hay un punto mecánico que comprender bien, ya que condiciona todo lo demás. Pi inyecta en el system prompt, **en cada turno**, el nombre, la descripción y la ruta de cada skill disponible:

```
The following skills provide specialized instructions for specific tasks.
Use the read tool to load a skill's file when the task matches its description.

<available_skills>
  <skill>
    <name>revue-rapide</name>
    <description>Relit les modifications en cours du dépôt...</description>
    <location>/chemin/vers/.pi/skills/revue-rapide/SKILL.md</location>
  </skill>
</available_skills>
```

El **cuerpo** del `SKILL.md` no está allí. Entra en el contexto a través de uno de los dos siguientes caminos, y la diferencia entre ambos es el tema de este módulo.

El primero es que el modelo **decide** abrirlo con la herramienta de lectura, basándose únicamente en la descripción. La documentación de Pi lo dice en los mismos términos, añadiendo que « models don't always do this ».

El segundo es que el usuario escriba `/skill:revue-rapide` en su mensaje, en cuyo caso Pi **despliega** el archivo en el lado del cliente y pega su cuerpo en el primer turno. El modelo ya no tiene que decidir nada.

Hay dos consecuencias prácticas. La descripción es lo único en lo que se basa el primer camino, por lo que todo el cuidado puesto en el cuerpo no sirve de nada mientras no se active. Y un skill casi no cuesta nada mientras no se utilice, lo que hace tentador acumularlos. Ten en cuenta, sin embargo, que cada descripción añadida entra en el contexto en cada turno y que veinte skills acaban formando un preámbulo considerable.

::: info Ejercicio (en clase)
Verifica esta mecánica por ti mismo, en tu clon de NÉON.

1. Crea `.pi/skills/revue-rapide/SKILL.md` con el contenido anterior, modifica una línea de un archivo del juego y luego abre una sesión.
2. Exporta la sesión con `\export` y busca el bloque `<available_skills>` en el system prompt: el nombre, la descripción y la ruta están ahí, el cuerpo no.
3. Pide « relis lo que acabo de modificar » sin nombrar el skill, y observa si el modelo lee `SKILL.md` por su cuenta: la llamada a la herramienta de lectura es visible en la sesión.
4. Abre una sesión nueva y escribe `/skill:revue-rapide`. Esta vez el cuerpo se pega en tu primer mensaje y ya no hay ninguna decisión que observar.

Acabas de recorrer los dos caminos. El primero se basa enteramente en la descripción, el segundo no la necesita.
:::

## Reconstruir

### Lo que una procedura debe producir

La competencia que estamos escribiendo responde a la brecha medida en el módulo anterior y, por lo tanto, tiene dos objetivos. El primero es que el agente **descomponga** el síntoma reportado por el jugador en fallos distintos, en lugar de detenerse en la primera explicación que justifique lo que ve. El segundo es que **mantenga la distancia**, es decir, que corrija cada fallo hasta que esté en verde en lugar de detenerse una vez escritos los casos rojos.

La competencia `playtest` está escrita para eso. Le da al agente un rol, el del playtester que sabe que un síntoma no es un bug, un punto de referencia de coordenadas para que los signos de velocidad no se deduzcan, una tabla con diez familias de fallos para revisar una por una, y la obligación de cuantificar cada disparador a partir de las constantes del archivo en lugar de describirlo.

<<<@/../scripts/trysquare-campaign/briques/skills/playtest/SKILL.md{md}

Dos decisiones de redacción merecen ser destacadas, ya que se pueden trasladar a cualquier procedimiento.

El entregable es un archivo cuya forma está impuesta. El paso 4 impone la forma de `.scratch/to_fix.md`, un bloque por defecto, con su causa localizada hasta la línea, su invariante violado, su disparador cifrado, su caso de prueba, la salida de fallo real copiada de la terminal, y la corrección ingenua que este caso rechaza. Un agente que produce este archivo necesariamente ha realizado el trabajo que el archivo describe.

El procedimiento también describe lo que rechaza. El paso 3 pide pasar cada caso a rojo dos veces, una vez sobre el código de hoy y una vez sobre la corrección ingenua, lo que prohíbe las pruebas que solo verifican que algo ha cambiado. Es la contrapartida directa de lo que el módulo anterior midió, donde algunas correcciones pasaban las cuatro caras y fallaban en la esquina.

::: info Ejercicio (en clase)
Escribe la descripción antes de leer la nuestra, luego compara. Es la única línea del archivo que el modelo leerá con seguridad, y su formulación requiere, por tanto, el mayor cuidado.

Un criterio útil: ¿tu descripción dice **cuándo** usarla, o solo **qué** hace el procedimiento? Ambas formulaciones se parecen al releerlas, pero solo la primera ayuda al modelo a decidir si abrir el archivo.
:::

### Cómo entra la competencia en la medición

Las dos configuraciones con competencia de la matriz reciben el siguiente prompt:

<<<@/../scripts/trysquare-campaign/briques/issue1-simple-prompt-with-skill.md

Hay que notar tres cosas. La solicitud es la solicitud descuidada del módulo anterior. El `/skill:playtest` al principio hace que el cuerpo del archivo se desarrolle del lado del cliente, por lo que la competencia es **impuesta** en lugar de propuesta. Y la lectura de `ISSUES.md` está prohibida, para que el procedimiento trabaje sobre el síntoma del jugador y no sobre un ticket ya redactado.

La columna `skill_invoque` vale, por tanto, 20/20 en estas dos configuraciones por construcción, y 0/20 en todas las demás. Registra un hecho sobre la sesión sin medir una decisión del modelo, y nada de lo que sigue trata sobre la cuestión de si una buena descripción desencadena la acción.

## Qué dice la medición

Las configuraciones con competencia se comparan con aquellas que reciben el ticket enmarcado, con el mismo `AGENTS.md` y razonamiento. En `gemma-4-31b`, veinte repeticiones:

| configuración                    | `in_scope` | `tests_ajoutes` | bloques | ángulos | salida | vecinas |
| -------------------------------- | ---------- | --------------- | ------- | ------ | ------ | -------- |
| `+agents+well_crafted`           | 19/20      | 17/20           | 11/20   | 12/20  | 9/20   | 9/20     |
| `+agents+skill`                  | **6/20**   | **8/20**        | 16/20   | 7/20   | 13/20  | 14/20    |
| `+agents+add_tests+well_crafted` | 20/20      | 17/20           | 18/20   | 18/20  | 18/20  | 18/20    |
| `+agents+add_tests+skill`        | **9/20**   | **7/20**        | 13/20   | 12/20  | 13/20  | 13/20    |

De esto extraemos tres conclusiones, de las cuales dos están establecidas y una no.

**La habilidad desplaza las pruebas fuera de la suite.** `tests_ajoutes` pasa de 17/20 a 8/20, es decir, una diferencia de -47 puntos cuyo intervalo excluye el cero. No es un fallo: el procedimiento pide explícitamente que los casos residan en `.scratch/to_fix.md`, y el agente obedece. La métrica cuenta los casos añadidos a `game/neon.test.js`, por lo que registra exactamente lo que la habilidad ha decidido hacer: los casos existen, pero en un lugar donde la suite de pruebas del repositorio nunca los buscará.

**La habilidad deja sus borradores atrás.** `in_scope` cae de 19/20 a 6/20, es decir, -68 puntos, también confirmado. La columna `touched` nombra a los culpables: `.scratch/to_fix.md` permanece en once ejecuciones de veinte, acompañado de `.scratch/repro.test.js`, `.scratch/test_collision.js` o `.scratch/probe.js`. Sin embargo, el paso 6 de `SKILL.md` ordena eliminar todos los archivos creados. Por lo tanto, la instrucción de limpieza se sigue en menos de una de cada tres ejecuciones.

**Sobre la corrección en sí, no hay nada confirmado.** El criterio pasa de 11/20 a 16/20 frente al ticket estructurado, pero su intervalo contiene el cero. La columna del rincón va en sentido contrario, 12/20 frente a 7/20, y su intervalo también contiene el cero. Las veinte ejecuciones no permiten concluir que el procedimiento ayude ni que perjudique.

::: warning Lo que la diferencia con la base no dice
La síntesis muestra `+agents+skill` con +29 puntos en el criterio frente a `nothing`, una diferencia confirmada, y sería tentador tomarlo como el resultado del módulo.

Esta configuración difiere de la base por **cuatro cosas a la vez**: el razonamiento avanzado, el archivo de reglas, la habilidad y una extensión de búsqueda web. Las tres primeras tienen cada una su propia configuración en la matriz, la habilidad no tiene ninguna, por lo que nada permite atribuirle una parte de esos veintinueve puntos.

La única diferencia legible para la habilidad es la que la compara con el ticket estructurado, arriba mencionada, y no es concluyente sobre la corrección. Aislar el factor requeriría una configuración más, con solicitud ignorada, razonamiento avanzado, archivo de reglas y nada más. Esta no ha sido medida.
:::

### La habilidad frente a la pila mejor equipada

La configuración `+agents+add_tests+skill` se analiza frente a `+agents+add_tests+well_crafted`, de la cual solo difiere por la sustitución del ticket estructurado por la habilidad:

| columna          | ticket estructurado | habilidad | diferencia |
| ---------------- | ------------------- | ---------- | ----------- |
| `in_scope`       | 20/20               | 9/20       | -55 pts `*` |
| `tests_ajoutes`  | 17/20               | 7/20       | -50 pts `*` |
| `rebond_angles`  | 18/20               | 12/20      | -30 pts `*` |
| `rebond_briques` | 18/20               | 13/20      | -25 pts `o` |

Tres desviaciones establecidas, todas negativas. En esta tarea, con este modelo, la procedura de trabajo no sustituye ventajosamente a un ticket correctamente redactado, y la columna de la esquina lo dice más claramente: es la que el ticket describe y la que la skill, que no tiene permiso para leer `ISSUES.md`, debe encontrar por sí misma.

`sonde_intacte` es 20/20, por lo que ninguna ejecución ha modificado la sonda que tenía delante.

### Lo que la skill cuesta

| configuración                    | tokens de entrada | turnos | duración |
| -------------------------------- | ----------------- | ------ | --------- |
| `+agents+well_crafted`           | 413 335            | 30     | 378 s     |
| `+agents+skill`                  | **921 783**       | 49     | 575 s     |
| `+agents+add_tests+well_crafted` | 558 473            | 31     | 590 s     |
| `+agents+add_tests+skill`        | **811 584**        | 44     | 540 s     |

Frente a la base, `+agents+skill` cuesta +908 622 tokens de entrada, +47 turnos y +560 segundos, estando establecidas las tres desviaciones. Es la configuración más cara de toda la matriz.

::: warning Estas columnas de coste deben leerse con la reserva del módulo anterior
Las dos configuraciones de skill representan por sí solas 632 de los 1 151 reintentos de la matriz ILaaS, 345 una y 287 la otra. Un reintento vuelve a ejecutar el turno con todo el contexto acumulado, por lo que estas columnas miden en parte nuestra propia carga sobre el proveedor.

El orden de magnitud sigue siendo legible en la matriz `deepseek-v4-flash`, que cuenta con treinta y siete reintentos en total y donde `+agents+skill` emplea una mediana de 1 068 segundos frente a los 553 de `+agents+well_crafted`. Una procedura en seis pasos que impone una búsqueda documental, diez familias que instruir y un bucle TDD es un trabajo largo, y la medición no dice más que eso.
:::

## Revisar la procedura, y luego volver a medir

Una procedura de trabajo es texto versionado que produce efectos medibles, y por lo tanto se revisa como el código: un diagnóstico extraído de las ejecuciones, una corrección y una nueva medición. Las columnas fallidas de la matriz tienen cada una una causa que se puede leer en las ejecuciones analizadas una a una.

**Las pruebas nacen en el lugar equivocado.** El paso 3 dice que los casos residen en `.scratch/to_fix.md`, y es el paso 5 el que los hace migrar hacia `game/neon.test.js`. Esta migración es el paso que el modelo falla: diez de cada veinte ejecuciones terminan en « 6 casos, como en el patrón », habiendo corregido el agente el código basándose en sus borradores y considerando el trabajo terminado.

**La instrucción de limpieza a veces destruye el entregable.** « Elimina todos los archivos que hayas creado » quedó en letra muerta en las trece ejecuciones que dejaron archivos, y dos ejecuciones, por el contrario, la aplicaron al pie de la letra: `game/neon.test.js`, que el agente acababa de rellenar, ya no existe en el árbol medido.

**Una referencia fantasma crea archivos.** El paso 3 pide ejecutar cada caso «desde la sonda del paso 1», mientras que el paso 1 es la investigación documental y no crea ninguna sonda. Esta instrucción huérfana, remanente de una versión anterior del archivo, impulsa a las ejecuciones a inventar lo que falta: los archivos `probe.js`, `repro.test.js` y `test_ghost.js` que rellenan la columna `touched` son el rastro de ello.

La matriz `deepseek-v4-flash` completa el diagnóstico: la misma competencia obtiene allí `tests_ajoutes` con 20/20. El contenido del procedimiento es, por lo tanto, suficiente para un modelo que tenga el presupuesto para ejecutarlo; en `gemma-4-31b`, es el protocolo mismo el que agota dicho presupuesto.

### La revisión: `playtest-court`

La versión revisada conserva lo que contiene la información: el rol, el sistema de coordenadas, la tabla de las diez familias y la obligación de cifrar cada disparador desde las constantes. Elimina el resto, y cada recorte responde a un defecto detectado en las ejecuciones. Los casos se escriben directamente en rojo en `game/neon.test.js` y el procedimiento ya no crea ningún archivo, lo que elimina tanto la migración fallida como la necesidad de limpieza. El paso de búsqueda web desaparece, ya que las sesiones solo mostraban una única llamada. El doble rojo y el bloque de doce campos son sustituidos por un requisito de una sola línea: el caso verifica el comportamiento esperado en valores, nunca simplemente que «algo ha cambiado». El archivo pasa de seis pasos a cuatro y de 182 líneas a 86.

<<<@/../scripts/trysquare-campaign/briques/skills/playtest-court/SKILL.md{md}

### Lo que dice la segunda matriz

El escenario `issue1-skills` pone a prueba las dos competencias frente a frente, en `AGENTS.md`, con razonamiento y modelo idénticos, veinte repeticiones por celda, sirviendo la original como referencia para las desviaciones. Reside en su propio archivo para no afectar a las matrices archivadas del módulo, y su hipótesis, `hypotheses/issue1-skills.md`, fue escrita antes de la medición. En `gemma-4-31b`:

| columna          | `playtest` | `playtest-court` | desviación             |
| ---------------- | ---------- | ---------------- | ---------------------- |
| `in_scope`       | 9/20       | **20/20**        | +53 pts `*` [+32, +74] |
| `tests_ajoutes`  | 13/20      | **20/20**        | +32 pts `*` [+11, +53] |
| `rebond_briques` | 14/20      | 17/20            | +11 pts `o`            |
| `rebond_angles`  | 4/20       | 8/20             | +19 pts `o`            |

En `deepseek-v4-flash`, `in_scope` pasa de 15/20 a 20/20, es decir, +25 puntos establecidos [+10, +45], y ninguna columna de corrección se mueve: la desviación en el criterio es de +0 puntos.

Extraemos tres conclusiones de esto.

**Los dos desplazamientos establecidos de la primera versión desaparecen.** El perímetro está completo en las cuarenta ejecuciones de competencia corta, y todas las pruebas van a la suite del repositorio. Los modelos son los mismos, solo ha cambiado el protocolo: cuando el entregable se escribe directamente en su lugar, ya no hay migraciones que fallar ni limpieza que realizar. Un procedimiento que realmente necesitara archivos intermedios mantendría el problema completo, y el módulo sobre permisos mostrará cómo un hook que rechaza un `git commit` mientras el borrador esté en el árbol garantiza lo que una frase solo puede sugerir.

**La corrección sigue sin moverse de forma establecida.** +11 puntos en el criterio y +19 en el coin, con intervalos que contienen cero en ambos casos. El coin sigue siendo la columna más baja de gemma, con 8/20, lejos de los 14/20 que el prompt encuadrado obtenía en el módulo anterior: la revisión ha reparado el protocolo del procedimiento, pero no ha sustituido el ticket.

**El coste baja, y la diferencia es legible en flash.** Su matriz contiene veintitrés repeticiones, un total del mismo orden que las treinta y siete que el módulo anterior consideraba legibles, y la competencia corta consume una mediana de 12 861 tokens de entrada frente a 34 764, 692 segundos frente a 1 054, y la diferencia de turnos es de -27 con un intervalo de [-47, -16]. La matriz gemma va en la misma dirección pero contiene 490 repeticiones, por lo que sus columnas de coste mantienen la reserva habitual: la hipótesis predecía esta bajada, y esta matriz no puede confirmarla.

::: warning La celda replicada no ha arrojado las mismas cifras
`+agents+skill` remedido en gemma da 9/20 en el perímetro, 13/20 en las pruebas añadidas y 14/20 en el criterio, mientras que la campaña del módulo daba 6, 8 y 16. Misma configuración, mismo commit, mismo modelo: es la dispersión del módulo anterior, vista una vez más. Es también por esto que el escenario vuelve a medir la original en la misma matriz en lugar de copiar sus cifras anteriores, y por lo que las diferencias de esta sección solo comparan celdas medidas conjuntamente.
:::

El archivo de estas dos matrices está en `scripts/trysquare-campaign/results-2026-08-13/`.

## Lo que un skill no garantiza

Todo lo que las dos matrices acaban de mostrar se debe a una sola propiedad: un skill solo tiene texto. La instrucción de limpieza ignorada, el borrador que nunca se migró a la suite, la referencia fantasma seguida al pie de la letra: en cada caso, el procedimiento pedía algo que nada obligaba al modelo a hacer. Un skill no tiene ni esquema de entrada, ni función de ejecución, ni barrera de permisos. La literatura sobre las herramientas de agentes describe la anatomía de una herramienta: a saber, un nombre, una descripción leída por el modelo, un esquema de entrada, una función de ejecución y un permiso entre la validación y la ejecución; y un skill solo implementa los dos primeros elementos.

Pi tiene un segundo mecanismo para el resto. Una **extensión** es un módulo TypeScript ubicado en `.pi/extensions/`, que llama a `pi.registerTool({ name, ... })`: una herramienta real, con un esquema JSON validado, una función que tú has escrito y la posibilidad de interceptar las llamadas a herramientas para insertar un permiso. Ya te has encontrado con una sin saberlo: la herramienta de búsqueda web que pedía la primera versión del procedimiento es una extensión, cargada por el bloque `extension` del escenario. El módulo sobre los permisos se basará en este mecanismo para transformar las instrucciones en garantías.

::: danger Un campo documentado no es necesariamente leído
Si a pesar de todo buscas un mecanismo de permisos del lado del skill, se lee a menudo que un skill declara las herramientas que permite mediante un campo `allowed-tools` en su frontmatter. La documentación incluida con Pi 0.80.6 lo describe efectivamente en su tabla del frontmatter:

```
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental). |
```

El tipo que lee el código es este:

```ts
export interface SkillFrontmatter {
    name?: string;
    description?: string;
    "disable-model-invocation"?: boolean;
    [key: string]: unknown;
}
```

Este tipo solo contiene tres campos, y la cadena `allowed-tools` no aparece en ninguna parte del código compilado del paquete, mientras que `disable-model-invocation` sí se lee. El `[key: string]: unknown` acepta silenciosamente todo lo que añadas, sin usarlo nunca ni avisarte.

Es la misma trampa que el `--thinking max` del módulo anterior, aunque más engañosa todavía, ya que la fuente que te induce al error es aquí la propia documentación de la herramienta. Un skill no tiene ningún mecanismo de permisos propio y, si quieres uno, necesitas una extensión.
:::

## Lo que este módulo aún no sabe

Dos preguntas siguen abiertas y es mejor nombrarlas claramente que creer que están resueltas.

**¿Una buena descripción la activa?** Nuestras configuraciones imponen la competencia mediante `/skill:`, por lo que las matrices miden un procedimiento aplicado y nunca un procedimiento elegido. La cuestión reside en la mecánica descrita anteriormente, es medible con la columna `skill_invoque` que ya existe para ello, y requiere una configuración donde la competencia se cargue por su nombre sin estar desarrollada en el prompt.

**¿Aporta la competencia algo a demanda igual?** Sigue faltando el testigo, es decir, la misma configuración sin la competencia. La segunda matriz no lo ha añadido: compara dos versiones del procedimiento entre sí, no el procedimiento frente a su ausencia.

::: info Ejercicio (autónomo)
Añade al escenario una configuración `+agents+skill_par_nom`, idéntica a `+agents+skill` pero cuyo prompt no contiene el `/skill:`, permaneciendo la competencia cargada por el bloque `harness`. Reinicia y lee `skill_invoque`.

Medirás lo único que este módulo afirma sin haberlo establecido, y no habrás tocado ni la herramienta, ni el validador, ni las otras configuraciones.
:::

## Generalizar

**Un skill es un procedimiento de trabajo, no una herramienta.** No tiene ni esquema de entrada, ni función, ni permisos, y el único mecanismo del que dispone es el texto. Lo que sabe hacer es imponer un orden de trabajo y una forma de entregable, lo cual es útil y no debe confundirse con la ejecución de un código que tú controles.

**La descripción es la única cosa que se lee con seguridad.** El cuerpo solo entra en el contexto si el modelo decide abrirlo o si el usuario lo despliega con `/skill:`. Una descripción que dice qué hace el procedimiento, en lugar de cuándo usarlo, se dirige a la decisión incorrecta.

**Un procedimiento desplaza el trabajo antes de mejorarlo.** Los dos efectos establecidos de la primera versión son desplazamientos: las pruebas van a un archivo de borrador en lugar de al resto del repositorio, y los borradores permanecen en el árbol. La revisión elimina estos dos desplazamientos, y el efecto sobre la corrección sigue siendo no concluyente en ambas versiones. Antes de preguntar si una pieza mejora el resultado, mira primero a dónde envía el trabajo.

**Una instrucción de limpieza no garantiza la limpieza.** El paso final de nuestro `SKILL.md` pide retirar los archivos creados, y once ejecuciones de cada veinte los dejan. La revisión que cubrió el alcance no reforzó la instrucción, sino que eliminó la necesidad de limpieza: un procedimiento que no crea nada no tiene nada que limpiar. Cuando los archivos intermedios son realmente necesarios, aquello que debe suceder aunque el modelo no lo piense requiere un mecanismo que no dependa de él.

**Cada paso intermedio es un escalón que el modelo puede saltarse.** Las pruebas nacían en un borrador antes de migrar al resto del repositorio, y esta migración es el paso que se perdió diez veces de cada veinte. Escribir el entregable directamente en su lugar eliminó el escalón, y las dos columnas afectadas pasaron a 20/20 en los dos modelos.

**Un procedimiento se revisa como el código, con las ejecuciones en mano.** El diagnóstico no proviene de las columnas agregadas sino de las ejecuciones leídas una por una: la migración fallida, la instrucción aplicada al pie de la letra y la referencia fantasma dictaron cada recorte, y una nueva matriz verificó la revisión en lugar de creer en ella.

**Un campo documentado no es necesariamente leído.** `allowed-tools` figura en la documentación entregada con Pi y no aparece en ninguna parte de su código. El código es la única fuente que no se equivoca, y la verificación se resuelve con un `grep`.

**Una pieza de harness se mide frente a lo que reemplaza, nunca frente a la nada.** En esta tarea, reemplazar el ticket delimitado por el procedimiento hace perder treinta puntos en los casos límite y cincuenta en las pruebas añadidas, algo que no se ve en una comparación contra la base.

## Entregable

Tres piezas.

**1. La competencia**, en `.pi/skills/<nombre>/`, con su descripción escrita por ti y un entregable cuya forma está impuesta por el cuerpo. Si la has revisado, ambas versiones permanecen versionadas: la matriz que las compara no se entiende sin ellas.

**2. El directorio de matriz** producido por `trysquare run`, con la configuración de competencia leída frente a la que reemplaza y no frente a la base.

**3. La línea « herramientas » de la ficha de decisión**:

| palanca                           | efecto medido | ¿adoptado? | por qué |
| -------------------------------- | ------------ | -------- | -------- |
| skill (Markdown)                 |              |          |          |
| descripción del skill             |              |          |          |
| competencia impuesta por `/skill:` |              |          |          |
| forma del entregable impuesta        |              |          |          |
| entregable directo o vía borrador |              |          |          |
| extensión (herramienta real)           |              |          |          |

::: tip Criterio de éxito
Sabes citar un efecto de tu competencia que esté establecido, un efecto que no lo esté, y decir qué falta para decidir sobre el segundo.

Este criterio requiere haber leído una configuración frente a la referencia correcta. Por lo tanto, no puede satisfacerse de memoria.
:::

## Las trampas

**Leer una configuración de competencia frente a la base.** Difiere de ella por varias cosas a la vez, y la diferencia publicada frente a `nothing` mezcla todas las palancas de la pila. La referencia útil es la configuración de la cual solo difiere en la competencia.

**Confundir una competencia impuesta con una competencia propuesta.** El `/skill:` del prompt desarrolla el cuerpo del lado del cliente, y una columna de invocación llena no dice entonces nada de lo que el modelo habría elegido.

**Cuidar el cuerpo de `SKILL.md` descuidando la descripción.** El cuerpo solo se lee si la descripción ha activado su lectura.

**Hacer que los tests se escriban en otro lugar que no sea la suite.** Un caso de prueba que reside en un archivo de trabajo no será ejecutado por nadie después de la salida del agente, y la migración prometida hacia la suite es precisamente el paso que el modelo omite.

**Confiar en una instrucción de limpieza.** Se sigue en menos de una de cada tres ejecuciones, lo que queda en el árbol hace fallar el perímetro de toda la configuración, y la corrección robusta no es una mejor instrucción sino un procedimiento que no crea nada.

**Revisar sin volver a medir.** Una revisión que responde punto por punto al diagnóstico sigue siendo una hipótesis hasta que una matriz la haya verificado. La nuestra también predecía una reducción de costes en gemma, y esa matriz no puede confirmarlo, ya que sus repeticiones hacen que las columnas de costes sean ilegibles.

**Acumular skills.** Cada uno cuesta poco mientras no se utilice, pero sus descripciones entran todas en el contexto en cada turno.

## Para ir más allá

- [Agent Skills](https://agentskills.io), el estándar abierto que implementa Pi, y su página sobre la integración en un system prompt.
- Anthropic, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
- Schick et al., [Toolformer](https://arxiv.org/abs/2302.04761), sobre la idea de que un modelo aprenda cuándo y cómo llamar a una herramienta.
- Yao et al., [ReAct: Reasoning + Acting](https://arxiv.org/abs/2210.03629), el bucle que alterna razonamiento y acción.
- La [documentación de las extensiones de Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md), para el componente que ofrece garantías donde el skill ofrece sugerencias.
