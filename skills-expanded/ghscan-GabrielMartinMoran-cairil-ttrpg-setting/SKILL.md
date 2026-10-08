---
name: settlement-builder
description: Use this skill whenever you create or expand a city, town, district, dungeon hub, or other location for this campaign. It defines the structure, tables, and playable details. Always pair it with `vault-conventions`.
---

# Generación de Ciudades y Asentamientos (Estilo Arcana)

Load `vault-conventions` first so filenames, emoji policy, wikilinks, and shared
vault rules stay aligned.

Objetivo: recurso "listo para jugar" que combine narrativa inmersiva con utilidad mecánica.

## Filosofía de diseño

- **Estructura visual:** encabezados, listas y tablas obligatorios
- **NPCs vivos:** cada local tiene dueño con Nombre, Raza y **una peculiaridad** concreta
- **Economía realista:** tabla de precios obligatoria en todo comercio
- **Capas de profundidad:** secretos, rumores, subsuelo si aplica

## Estructura obligatoria

### A. Encabezado y contexto

```markdown
---
tipo: lugar
nombre: [Nombre]
region: [región]
campania: [nombre]
---

## Música
[link o mood]

![](url_imagen_panorámica)

## Información general
[descripción breve de estética y atmósfera]

### Historia/Rumor
[hecho histórico o rumor que define el lugar — puede ser falso]

### Población
### Gobierno
### Economía

### Curiosidades
- [hook 1]
- [hasta 10 hooks]

### Seguridad
[nombre del capitán + composición de patrullas]

### Trato a aventureros
[renombre, gremios, actitud general]
```

### B. Disposición — dividir en distritos/zonas con descripción breve antes de listar locales

### C. Localizaciones — dentro de cada zona:

```markdown
#### [Tipo]: [Nombre del Local]
![](url)

**Descripción:** [sensorial: olores, luz, ambiente]

**NPC:** [Nombre] ([Raza], [Rol]).
* *Detalle:* [rasgo único concreto]

| Producto / Servicio | Precio |
| :--- | :--- |
| [Item] | [X] po/pp/pc |
```

**Reglas de precios:**
- Tabernas: comida (humilde/modesta/fina), bebida, alojamiento
- Herrerías: calidad (barato/rompible vs caro/garantizado)
- Tiendas de magia: caras por defecto
- Establos: alquiler vs compra

### D. Templos — deidad, arquitectura, líder

### E. Subsuelo/Crimen (opcional) — facciones, líderes, mercados negros

## Moneda

- `pc` = Cobre, `pp` = Plata, `po` = Oro (estándar en Arcana)
