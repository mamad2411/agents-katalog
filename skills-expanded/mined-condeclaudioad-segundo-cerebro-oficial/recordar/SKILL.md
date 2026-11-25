---
name: recordar
description: Guarda una regla, preferencia o aprendizaje durable en MEMORIA/ con su porqué y cómo se aplica, y la suma al índice. Usar con /recordar, "acordate de esto", "de ahora en más…", "siempre/nunca hagas…", o cuando la persona corrige algo que vale para siempre.
argument-hint: "[la regla]"
---

# /recordar — se explica una vez

1. **¿Es memoria?** Una memoria cambia **cómo se trabaja** (regla, preferencia, aprendizaje, dónde está algo). Un dato del negocio va a `WIKI/`; un entregable, a `OUTPUTS/`. Si no es memoria, decilo y guardalo donde va.
2. **¿Ya existe?** `grep -ril` de las palabras clave en `MEMORIA/`. Si hay una parecida, **actualizala** con la fecha; no crees otra.
3. **Escribila** con el formato de `MEMORIA/README.md`: frontmatter (`name`, `description`, `type`, `fecha`) + la regla en una o dos frases + **Por qué** + **Cómo se aplica**. Si la persona no dijo el porqué, preguntalo en una línea: sin el porqué, la regla se rompe en el primer caso raro.
4. **Índice:** línea arriba en `MEMORIA/README.md` § Índice.
5. **Contradicciones:** si choca con algo de `CLAUDE.md` o de otra memoria, mostrá las dos y preguntá cuál manda.
6. Changelog (una línea) y confirmá en una línea qué quedó guardado.

Nunca guardes el valor de una key o una contraseña. Se guarda dónde está.
