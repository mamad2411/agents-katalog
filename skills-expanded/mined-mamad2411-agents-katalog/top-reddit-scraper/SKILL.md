---
name: Top Reddit Scraper
description: Obtiene las 5 mejores publicaciones de cualquier subreddit elegido por el usuario
---

# Top Reddit Scraper

Esta habilidad te permite obtener las 5 mejores publicaciones de cualquier subreddit de Reddit. Es útil para investigar tendencias, encontrar contenido popular o hacer resúmenes de comunidades.

## Cómo Funciona

Reddit ofrece feeds JSON públicos que no requieren autenticación. Simplemente agregando `.json` al final de cualquier URL de subreddit, podemos obtener los datos estructurados.

## Instrucciones

### Paso 1: Identificar el Subreddit

Cuando el usuario pida información sobre una temática, identifica el subreddit más relevante:

| Temática | Subreddit Sugerido |
|----------|-------------------|
| Programación | r/programming, r/learnprogramming |
| Inteligencia Artificial | r/MachineLearning, r/artificial |
| Tecnología | r/technology |
| Ciencia | r/science, r/askscience |
| Noticias | r/worldnews, r/news |
| Gaming | r/gaming, r/Games |
| Finanzas | r/investing, r/personalfinance |
| Criptomonedas | r/cryptocurrency, r/bitcoin |
| Diseño | r/web_design, r/graphic_design |
| Productividad | r/productivity |

> [!TIP]
> Si el usuario menciona una temática genérica, sugiere varios subreddits relevantes y pregunta cuál prefiere.

### Paso 2: Obtener los Datos

Usa la herramienta `read_url_content` para leer el feed JSON del subreddit:

```
https://www.reddit.com/r/{SUBREDDIT}/top.json?limit=5&t=week
```

**Parámetros disponibles:**
- `limit`: Número de publicaciones (máximo 100)
- `t`: Período de tiempo
  - `hour` - Última hora
  - `day` - Últimas 24 horas
  - `week` - Última semana
  - `month` - Último mes
  - `year` - Último año
  - `all` - Todos los tiempos

### Paso 3: Parsear la Respuesta

La respuesta JSON tiene esta estructura:

```json
{
  "data": {
    "children": [
      {
        "data": {
          "title": "Título del post",
          "author": "nombre_usuario",
          "score": 12345,
          "num_comments": 678,
          "url": "https://...",
          "permalink": "/r/subreddit/comments/...",
          "selftext": "Contenido del post si es texto",
          "created_utc": 1234567890
        }
      }
    ]
  }
}
```

### Paso 4: Formatear y Presentar

Presenta los resultados de forma clara al usuario:

```markdown
## 🔥 Top 5 de r/[subreddit] (Esta Semana)

### 1. [Título del Post](https://reddit.com/permalink)
- 👤 **Autor:** u/username
- ⬆️ **Votos:** 12,345
- 💬 **Comentarios:** 678
- 📝 **Resumen:** [Breve descripción si hay selftext]

---

### 2. [Siguiente Post]...
```

## Ejemplo de Uso

**Usuario dice:** "Dime las mejores publicaciones sobre Inteligencia Artificial"

**Proceso:**
1. Identificar: El subreddit más relevante es `r/MachineLearning` o `r/artificial`
2. Obtener: `https://www.reddit.com/r/MachineLearning/top.json?limit=5&t=week`
3. Parsear: Extraer título, autor, votos, comentarios y enlace
4. Presentar: Formato limpio con markdown

## Consideraciones Especiales

> [!IMPORTANT]
> Reddit tiene rate limiting. Si haces muchas solicitudes seguidas, puede bloquear temporalmente. Espera unos segundos entre solicitudes múltiples.

> [!WARNING]
> Algunos subreddits son NSFW o tienen contenido sensible. Siempre verifica antes de presentar contenido al usuario.

> [!NOTE]
> Los posts pueden contener imágenes, videos o enlaces externos. El scraper solo obtiene metadatos, no el contenido multimedia.

## Variantes de Ordenamiento

Puedes usar diferentes endpoints según lo que busque el usuario:

| Endpoint | Descripción |
|----------|-------------|
| `/top.json` | Más votados |
| `/hot.json` | Populares ahora |
| `/new.json` | Más recientes |
| `/rising.json` | En ascenso |
| `/controversial.json` | Controversiales |

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| Error 403 | El subreddit puede ser privado o no existir |
| Sin resultados | Verifica que el nombre del subreddit sea correcto |
| Contenido vacío | Algunos posts son solo imágenes sin texto |
| Rate limited | Espera 1-2 minutos antes de reintentar |

## Plantilla de Respuesta

Usa esta plantilla para responder al usuario:

```markdown
# 🔥 Top 5 de r/{subreddit}

📅 **Período:** [Última semana/mes/etc]
📊 **Ordenado por:** [Más votados/Populares/etc]

---

## 1. {título}
- 👤 u/{autor} • ⬆️ {votos} • 💬 {comentarios}
- 🔗 [Ver en Reddit](https://reddit.com{permalink})

{resumen si existe}

---

[Repetir para 2-5]

---
💡 *Datos obtenidos de Reddit. Los votos y comentarios pueden variar.*
```
