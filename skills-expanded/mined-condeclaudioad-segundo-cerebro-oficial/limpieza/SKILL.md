---
name: limpieza
description: Auditoría quincenal del cerebro — busca contradicciones, duplicados, temas viejos, links rotos, afirmaciones sin fuente y RAW sin procesar, y deja hasta 7 preguntas con opciones para que la persona decida qué borrar, mantener o actualizar. No borra nada sin respuesta. También aplica las respuestas cuando la persona escribe "limpieza <fecha>: L1 borrar, L2 mantener…". Usar con /limpieza.
argument-hint: "[vacío para auditar, o las respuestas: \"L1 borrar, L2 actualizar a …\"]"
---

# /limpieza — más contexto no es mejor contexto

Lo viejo y lo duplicado ensucia las respuestas. Pero **lo viejo no es automáticamente inútil**: por eso esta skill pregunta y no borra.

## Modo A · Auditar (sin argumento)

1. Listá lo que lleva **más de 30 días sin tocarse** en `WIKI/`, `MEMORIA/`, `SKILLS/` y `RUTINAS/` (`git log -1 --format=%cs -- <archivo>`).
2. Buscá:
   - **Contradicciones** entre temas o entre una memoria y un tema (con fecha y fuente de cada lado).
   - **Duplicados**: lo mismo dicho en dos lugares.
   - **Desactualizado**: algo que una decisión posterior ya reemplazó.
   - **Links rotos** dentro del repo.
   - **Afirmaciones sin fuente** en WIKI.
   - **RAW sin procesar** (no citado en WIKI ni changelog).
   - **Rutinas sin log reciente** o skills que nadie usó.
3. Escribí `OUTPUTS/AAAA-MM-DD-health-check.md` con lo encontrado y, al final, la sección **Preguntas de limpieza**: **hasta 7**, numeradas `L1`…`L7`:

   ```
   L1 · <qué> · <dónde> · opciones: borrar / mantener / actualizar a "<propuesta>" · (reco: …)
   ```

   Y la línea para contestar: `limpieza <d/m>: L1 borrar, L2 mantener, L3 actualizar a …`
4. Enlazalo desde `WIKI/index.md`, entrada arriba en `changelog/`. **No borres ni edites nada de lo que preguntás.**

## Modo B · Aplicar respuestas

1. Abrí el health check de esa fecha y releé cada pregunta contestada. Si pasaron más de 15 días, verificá que siga igual antes de tocar.
2. **borrar** → antes, `grep -rn "<nombre>"` en todo el repo y arreglá los links que quedarían rotos. Después `git rm` (o borrá el pasaje). Queda recuperable en la historia de git.
3. **actualizar** → cambialo a lo que dijo, con la fecha.
4. **mantener** → nada; se marca para no volver a preguntarlo en 90 días.
5. Marcá cada pregunta: `✅ contestada <d/m>: borrar | actualizar | mantener`. Lo no contestado se vuelve a preguntar la próxima quincena, una sola vez más.
6. Entrada arriba en `changelog/` + commit.

## Cadencia

Días 1 y 15 de cada mes. Si querés que se audite solo, la rutina `bibliotecario-nocturno` ya lo hace esos días (ver `RUTINAS/`). La respuesta siempre es tuya.
