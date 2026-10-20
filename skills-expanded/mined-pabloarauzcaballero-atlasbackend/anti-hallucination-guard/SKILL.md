---
name: anti-hallucination-guard
description: Gate contra la invención — obliga a localizar el equivalente existente antes de crear una entidad, enum, tabla, endpoint, evento, cola o componente; a verificar APIs de librerías contra la documentación de la versión instalada; a registrar las ambigüedades en vez de resolverlas por conveniencia; y a no presentar datos ficticios como reales. Usar antes de introducir cualquier pieza nueva, al interpretar un requisito dudoso, al usar una API que no acabás de ver, y al redactar afirmaciones sobre el sistema.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Guardia anti-alucinación

Una pieza inventada cuesta más que una pieza faltante: duplica conceptos, rompe contratos y
obliga a otro a descubrir que lo que "parecía necesario" ya existía con otro nombre. Todo hecho
que afirmes tiene que poder apuntar a una fuente. Lo que no puede, es hipótesis y se etiqueta así.

## Cuándo aplica

- Vas a crear algo con nombre propio: entidad, tabla, columna, enum, DTO, endpoint, evento, cola, servicio, componente, token de diseño.
- Vas a usar una API de librería, un flag de CLI o una opción de configuración que no verificaste en esta sesión.
- El requisito admite más de una lectura.
- Vas a escribir datos de catálogo, seeds o ejemplos que alguien podría tomar por reales.

## 1. Buscar antes de crear

Antes de introducir una pieza, demostrá que no existe. Una búsqueda sola no demuestra nada.

1. Buscá por **nombre y por sinónimos**, en español y en inglés, singular y plural (`cita`, `turno`, `appointment`, `booking`).
2. Buscá por **uso**, no solo por definición: la ruta HTTP, el nombre de tabla, el texto visible en la UI, el nombre del evento.
3. Buscá en **todos los repos del carril**: el contrato puede vivir en la API, su cliente en el front y su modelo en otro repo.
4. Mirá el **modelo fuente de verdad** antes que el código generado (ver `model-driven-schema`).
5. Para catálogos cerrados, verificá si ya hay un value set antes de crear un enum (ver `terminology-value-sets`).
6. Anotá dónde buscaste. "No existe" sin alcance de búsqueda declarado no es un hallazgo.

Si existe algo equivalente: **reusalo o extendelo**. Si hay dos implementaciones posibles, elegí la
coherente con los patrones ya presentes (ver `native-code-patterns`) y dejá la evidencia. Si no hay
patrón, registrá la decisión técnica con alcance mínimo (ver `technical-docs-and-adr`).

❌ Crear `DoctorScheduleDto` porque "hace falta uno" → ya existía `AvailabilitySlotDto` usado por tres endpoints.
✅ "Busqué `schedule|availability|horario|agenda` en `src/**/dto` y en el OpenAPI: existe `AvailabilitySlotDto` (`ruta:línea`). Lo extiendo con `breakMinutes`."

## 2. Prioridad de fuentes de evidencia

Cuando dos fuentes se contradicen, gana la de arriba. Nunca al revés.

1. Requisito o contrato de negocio explícito.
2. Comportamiento y contratos reales del proyecto (OpenAPI, DTOs, schema, modelo).
3. Tests y definiciones de datos existentes.
4. Runtime observado en local/desarrollo (respuesta real, query real, captura).
5. Documentación oficial del framework o proveedor, **de la versión instalada**.
6. Hipótesis documentada: último recurso, y jamás redactada como hecho.

Tu memoria de entrenamiento no figura en la lista: sirve para saber qué buscar, no para afirmar.

## 3. Ambigüedad: se registra, no se resuelve a conveniencia

Una frase ambigua del requisito no es un hecho que podés corregir en silencio. Primero intentá
resolverla con código y runtime. Si sigue abierta, registrala y preguntá o elegí explícitamente:

```text
AMBIGUO: "<frase literal del requisito>"
Lecturas:  (a) ...   (b) ...
Evidencia: <qué encontré a favor de cada una, con ruta>
Decisión:  <pregunto a X | asumo (a) porque ..., reversible en ...>
Impacto:   <qué cambia si la lectura correcta era la otra>
```

No implementes un criterio marcado como ambiguo sin este registro (ver `requirements-and-acceptance`).

## 4. No cambiar la semántica del requisito

Prohibido reescribir lo pedido para que entre en lo fácil de implementar:

- "Overlay" no es "empuja el contenido". "Tiempo real" no es "refresca al recargar".
- "Todos los X" no es "los primeros 20". "Validado en servidor" no es "deshabilité el botón".
- "Datos reales" no es "datos verosímiles".

Si lo pedido es inviable o mucho más caro, **decilo y proponé**; no entregues otra cosa con el mismo nombre.

## 5. APIs de librerías: verificar contra la versión instalada

1. Mirá la versión real en el lockfile / `package.json` / `pubspec.yaml` antes de asumir una API.
2. Verificá firma y nombres en la doc oficial de esa versión, o en los tipos instalados (`node_modules/<pkg>/**/*.d.ts` es fuente válida y local).
3. Si no podés verificar: no lo uses, o marcá explícitamente "sin verificar" y probalo en runtime antes de apoyarte en él.
4. Señales de API inventada: un método que "sería lógico que existiera", una opción que resuelve justo tu problema, un import que el typecheck no resuelve. El typecheck rojo por símbolo inexistente es un hallazgo, no un estorbo que se tapa con `any`.
5. Lo mismo vale para flags de CLI, variables de entorno y claves de config: `--help` y la doc mandan.

## 6. Datos: nada ficticio presentado como real

- Si el requisito exige datos reales (instituciones, especialidades, medicamentos, aseguradoras, divisiones administrativas), no generes valores plausibles. Requerí fuente y registrá procedencia (ver `seed-data-catalogs`).
- No infieras reglas de negocio con consecuencia económica o regulatoria: tasas, plazos, comisiones,
  umbrales de riesgo, catálogos de estados. Se confirman contra el código o con quien las define.
- Los datos de prueba se rotulan como tales y no se mezclan con catálogos.
- Nunca inventes una cita, una URL, un número de norma o una cifra. Sin fuente → no va.

## 7. Afirmación → evidencia mínima

| Si afirmás... | Tenés que poder mostrar... |
|---|---|
| "Ya existe X" | `ruta:línea` de la definición y de un uso |
| "No existe X" | Patrones y rutas donde buscaste, en todos los repos del carril |
| "El endpoint devuelve Y" | Respuesta real o contrato OpenAPI/DTO |
| "La tabla tiene la columna Z" | Modelo fuente / DDL / consulta al catálogo de la base |
| "La librería soporta W" | Doc de la versión instalada o el `.d.ts` |
| "El requisito pide V" | Cita literal del requisito |
| "Así se hace en este repo" | Dos o más ejemplos existentes del patrón |
| "Esto falla por Q" | Reproducción + salida (ver `root-cause-debugging`) |
| "Está implementado / probado" | Peldaño de `evidence-and-verification` con salida literal |

## 8. Lenguaje: hecho vs hipótesis

Hecho: "`ruta:línea` define...". Hipótesis: "Hipótesis (sin verificar): ...". Las palabras
"seguramente", "normalmente", "debería", "suele" en tu propio texto son la señal de que estás
por pasar una probabilidad como hecho: frená y buscá (ver `rationalization-guard`).

## Anti-patrones

- Crear la pieza nueva y "después conectar" con lo que ya había.
- Catálogo paralelo al existente porque no lo encontraste en la primera búsqueda.
- Decir "implementado" cuando solo se tocó la UI y falta contrato/persistencia.
- Decir "probado" sin haber ejecutado la prueba.
- Rellenar un hueco del requisito con lo que "cualquier sistema tendría".
- Tapar un símbolo inexistente con `any`, `// @ts-ignore` o un cast.

## Evidencia / DoD

Por cada pieza nueva introducida, el reporte incluye:

1. Búsqueda realizada (patrones + alcance) y su resultado literal.
2. Pieza equivalente encontrada y por qué se reusó/extendió, o por qué no servía.
3. Fuente de cada API de terceros usada por primera vez (versión + doc o `.d.ts`).
4. Registro de cada ambigüedad con su decisión.
5. Procedencia de todo dato de catálogo agregado.

## Checklist

- [ ] ¿Busqué por nombre, sinónimos, idioma y uso, en todos los repos del carril?
- [ ] ¿Cada pieza nueva tiene justificación de por qué no alcanzaba lo existente?
- [ ] ¿Cada API de terceros está verificada contra la versión instalada?
- [ ] ¿Las ambigüedades están registradas y no resueltas en silencio?
- [ ] ¿Entrego lo que se pidió y no una versión más cómoda con el mismo nombre?
- [ ] ¿Ningún dato inventado figura como real? ¿Sin citas ni cifras sin fuente?
- [ ] ¿Separé en el texto hechos de hipótesis?
