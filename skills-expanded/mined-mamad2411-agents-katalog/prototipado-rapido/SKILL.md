---
name: prototipado-rapido
description: Maquetas tipo wireframe (estilo boceto - cajas grises, placeholders con X, tipografia a mano, sin color de marca) para que el cliente VEA la idea de un requerimiento antes de que se construya - cuando aplica (funcionalidad nueva con cambios en pantalla, proyecto nuevo, cotizacion; nunca bugs), fidelidad baja o media, como se eligen las pantallas clave, el kit de componentes HTML autocontenido con navegacion entre pantallas, captura con Playwright MCP para incrustar en el documento y la propuesta, validacion con el cliente y lo que un prototipo NO es (no es diseño final, no es compromiso de implementacion). Cargala al prototipar.
---

# Prototipado rapido — maquetas para ver la idea (Mesa de Servicios)

Una maqueta vale mas que tres rondas de preguntas: cuando el cliente VE una pantalla de
boceto, dice "si, asi" o "no, el total va arriba" en segundos. El prototipo de la Mesa es
eso: **wireframes de baja o media fidelidad**, al estilo de Mockflow o Balsamiq — cajas
grises, imagenes como un rectangulo con una X, texto de relleno, tipografia "a mano", sin
colores de marca ni pulido visual — navegables entre pantallas, para validar la IDEA del
requerimiento o ilustrar una propuesta. No es el diseño final (eso lo hace el equipo de
diseño del dev-team cuando el trabajo ya esta aprobado) y no compromete una implementacion.

## Cuando aplica (y cuando no)
| Caso | ¿Prototipo? |
|---|---|
| PRY con cambios en pantalla (nueva pantalla, nuevo flujo, cambio visible de un formulario o listado) | **Si** |
| Proyecto nuevo | **Si** (las 3-6 pantallas que cuentan la historia) |
| CTZ (cotizacion) | **Si** — la propuesta se entiende mucho mejor con maquetas |
| PRY sin cambio de pantalla (regla de negocio, proceso interno, integracion) | No; a lo sumo un diagrama de flujo simple |
| BUG | **No** — un bug se documenta con evidencia de lo que pasa, no se maqueta |

## Fidelidad
- **Baja** (default): estructura y jerarquia. Cajas, etiquetas, botones con nombre, placeholders.
  Responde "¿que hay en la pantalla y en que orden?".
- **Media**: ademas, textos reales del negocio (nombres de campos, estados, mensajes) y datos de
  ejemplo del cliente. Responde "¿se entiende el flujo con mis datos?". Se usa cuando la baja ya
  fue validada o cuando la propuesta lo amerita.
- Nunca alta: sin paleta de marca, sin iconografia final, sin animaciones. Si el cliente pide
  "como se veria de verdad", eso es diseño y va al dev-team despues de la aprobacion.

## Que pantallas maquetar
Las **pantallas clave** del flujo deseado (de `solicitud.md` / `preguntas.md`), no todas:
la de entrada, la del paso decisivo (donde el usuario toma la decision o completa el dato
critico) y la de resultado. Entre 3 y 6 pantallas por prototipo. Cada pantalla tiene un
nombre de negocio ("Bandeja de operaciones pendientes", "Aprobar operacion") y un proposito
de una linea.

## El kit (HTML autocontenido)
Se parte de `templates/prototipo/maqueta-base.html`: un solo archivo, sin dependencias
externas, con el estilo boceto (fuente manuscrita con fallback, bordes irregulares, gris) y
componentes listos:
- Contenedores: barra superior, menu lateral, tarjeta, seccion
- Controles: boton, campo de texto, selector, casilla, radio, interruptor, fecha
- Datos: tabla, listado, tarjeta de totales, etiqueta de estado (pendiente/aprobado/rechazado)
- Placeholders: imagen (caja con X), texto de relleno, grafico (caja con lineas)
- Navegacion: cada pantalla es una `<section data-pantalla="…">`; los botones con
  `data-ir="…"` cambian de pantalla sin recargar; hay un indice de pantallas visible para
  recorrerlas
- Anotaciones: notas al margen numeradas ("1: aqui el usuario elige el banco") para explicar
  la intencion de cada zona

Convencion de archivos en `.mesa/solicitudes/{ID}/prototipo/`:
```
maqueta.html                 el prototipo navegable (fuente de verdad)
captura-01-{pantalla}.png    una captura por pantalla, numerada en orden del flujo
captura-02-{pantalla}.png
NOTAS.md                     que muestra cada pantalla, que decidio el cliente al verla, version
```

## Captura (Playwright MCP del plugin)
Para incrustar las pantallas en el documento y la propuesta, y para que queden como evidencia
de lo validado: abrir `maqueta.html` con `browser_navigate`, ir a cada pantalla, y
`browser_take_screenshot` a 1280x720 (y 375x812 si el requerimiento es movil). Nombrar
`captura-NN-{pantalla}.png`. Las capturas son del prototipo, no de un sistema real.

## Validacion con el cliente
1. Se presenta la maqueta (archivo HTML que se abre en cualquier navegador, o las capturas).
2. Se recorre pantalla por pantalla preguntando lo concreto: "¿este es el orden en que
   trabajan?", "¿falta algun dato aqui?", "¿quien ve este boton?".
3. Lo que el cliente decide al ver la maqueta se registra en `NOTAS.md` y alimenta
   `preguntas.md` (muchas preguntas se cierran ahi).
4. Si cambia, `v2` de la maqueta; la version validada es la que va al documento.

## Lo que el prototipo NO es
- No es el diseño final ni una promesa de que se vera asi.
- No es una especificacion tecnica: no define datos, servicios ni validaciones internas.
- No reemplaza el documento: lo ilustra.
- No se construye para bugs, ni para pedidos sin cambio visible en pantalla.

## Reglas duras
- Estilo boceto siempre (gris, placeholders, sin marca): si parece terminado, el cliente lo
  toma por terminado.
- Textos y datos de ejemplo en lenguaje del cliente (usa el glosario de faast-brain).
- Nunca datos reales de personas ni cifras reales de clientes en la maqueta: ejemplos ficticios.
- La maqueta vive en `.mesa/solicitudes/{ID}/prototipo/`, versionada con la solicitud; nunca en
  un repo de codigo de producto.
