---
name: ux-writing-es
description: Revisa y reescribe los textos de interfaz en español neutro con tuteo - botones, errores, estados vacíos, formularios, confirmaciones y avisos - detectando voseo, formas de vosotros, inglés residual, mayúsculas de título, signos de apertura faltantes y enlaces no descriptivos. Úsalo cuando la persona pida revisar el copy o microcopy, los textos de un formulario o una pantalla, unificar la voz, o antes de publicar textos nuevos.
argument-hint: "[archivos o carpeta, por defecto src]"
---

# UX writing en español (tuteo neutro)

Escribes para personas de toda Latinoamérica: **tú (nunca voseo ni usted); nada de vosotros ni
regionalismos marcados**. Texto claro, corto y útil. La guía completa con ejemplos está en
[guia-de-voz.md](guia-de-voz.md): léela antes de reescribir.

Si el `CLAUDE.md` del proyecto define otra voz (usted, un país específico, un glosario), **manda
el CLAUDE.md**.

## 1. Detecta lo mecánico
```bash
node ${CLAUDE_SKILL_DIR}/scripts/revisar-texto.mjs <archivos o carpeta>
```
Encuentra voseo (`podés`, `ingresá`, `registrate`), vosotros (`podéis`), `usted` suelto, inglés
residual (`Submit`, `Learn more`, `loguearte`), mayúsculas de título («Crea Tu Cuenta Gratis»),
preguntas o exclamaciones sin `¿` `¡`, enlaces «aquí» y regionalismos. Los **errores** son
seguros; los **avisos** son hipótesis: revísalos uno por uno (por ejemplo, «escribí» puede ser
pasado y estar bien).

## 2. Revisa lo que importa (eso no lo ve el script)
Recorre los textos de la pantalla o del flujo y aplica, en este orden:
1. **¿Se entiende a la primera?** Una idea por frase. Palabras de la persona, no del sistema
   («No pudimos guardar tus cambios», no «Error 500 al persistir la entidad»).
2. **Botones:** dicen la acción con un verbo y, si hace falta, el objeto: «Guardar cambios»,
   «Crear cuenta», «Enviar solicitud». Nunca «Aceptar» o «Sí» cuando la acción es otra. Mismo
   verbo en el botón y en el título del diálogo.
3. **Errores:** qué pasó + cómo seguir, sin culpar: «La contraseña necesita al menos 8
   caracteres». Junto al campo, no solo arriba.
4. **Estados vacíos:** qué es esta pantalla + qué hacer ahora + un botón para hacerlo.
5. **Acciones destructivas:** nombra lo que se pierde: «¿Eliminar el proyecto “Rediseño”? No se
   puede deshacer.» Botón: «Eliminar proyecto».
6. **Formularios:** label visible y corto; ayuda debajo si hace falta; el placeholder no
   reemplaza al label; marca lo opcional, no lo obligatorio (si casi todo es obligatorio).
7. **Consistencia:** un término por concepto en todo el producto. Si el proyecto tiene glosario
   en el `CLAUDE.md`, úsalo; si no, propone uno con los términos que encuentres.
8. **Inclusivo sin trabas:** «Te damos la bienvenida» en vez de «Bienvenido/a»; «las personas
   usuarias» o reformular («quienes usan…») en vez de «los usuarios» cuando importa.
9. **Formato:** mayúscula solo al inicio y en nombres propios; `¿?` y `¡!`; números y fechas en
   el formato del país del público (si es toda Latinoamérica, evita ambigüedades: «3 de marzo»,
   no «03/03»).

## 3. Propón cambios
Tabla corta, de lo más grave a lo menos:

| Dónde (archivo:línea) | Ahora | Propuesta | Por qué |
|---|---|---|---|

- No reescribas por gusto: cada cambio tiene un «por qué» de esta guía.
- **Pregunta antes de cambiar** el tono de marca, nombres de producto o textos legales.
- Si la persona aprueba (o pidió corregir directamente), aplica los cambios y vuelve a correr el
  script: debe quedar en 0 errores.

## Nunca
- Mezclar tú y usted en el mismo producto.
- Traducir literal del inglés («Hacer clic aquí para aprender más»).
- Usar emojis en textos de interfaz salvo que el sistema de marca lo defina.
