# /model set skill
_Asigna un tier específico a una skill de análisis_

## Uso
```
/model set skill <nombre-skill> <tier>
```

## Descripción
Cambia el modelo LLM que usa una skill particular. Esto permite afinar el balance costo/rendimiento: mandar tareas mecánicas a modelos baratos y razonamiento complejo a modelos grosos.

Si la skill no existe, el comando muestra un error con las skills válidas.

## Ejemplos
```
/model set skill data-cleaning T1
/model set skill ml-modeling T4
/model set skill data-visualization T3
/model set skill sql-analysis T2
```

## Ejecución
Al ejecutar este comando, el agente debe ejecutar:
```
python3 scripts/model-commands.py set-skill <nombre> <tier>
```

## Skills disponibles
| Skill | Descripción |
|-------|-------------|
| `data-analysis` | Análisis general con Pandas y NumPy |
| `data-visualization` | Gráficos con Matplotlib, Seaborn, Plotly |
| `data-cleaning` | Limpieza y preparación de datos |
| `ml-modeling` | Modelado con Scikit-learn, XGBoost, SHAP |
| `sql-analysis` | Consultas SQL analíticas |
| `api-integration` | Consumo de APIs REST |
| `time-series-analysis` | Series temporales con Statsmodels, Prophet |
| `web-scraping` | Extracción con BeautifulSoup, Selenium |
| `statistical-testing` | Tests con SciPy, Statsmodels |
| `streamlit` | Dashboards interactivos |
| `notebook-integration` | Jupyter notebooks |
| `data-validation` | Validación con Pydantic, Pandera |
| `git-data` | Git para proyectos de datos |
| `file-formats` | Lectura/escritura de formatos |
| `python-environment` | Gestión de entornos Python |
| `database-connections` | Conexiones a bases de datos |
| `regex-data` | Expresiones regulares para datos |
| `data-profiling` | Perfilado automático de datasets |
| `reporting` | Generación de reportes |
| `etl-pipelines` | Pipelines ETL/ELT |
| `data-verify` | Verificación de resultados |
| `data-archive` | Cierre y versionado de proyectos |
| `data-design` | Diseño de estrategia de análisis |
| `data-question` | Definición de preguntas de negocio |

## Tiers disponibles
| Tier | Modelo | Para qué |
|------|--------|----------|
| T1 | Minimax Free | Tareas mecánicas (limpieza, formateo) |
| T2 | Minimax | Tareas simples con lógica básica |
| T3 | DeepSeek Medium | Default diario — la mayoría de tareas |
| T4 | DeepSeek Pro | Razonamiento y análisis profundos |
| T5 | DeepSeek Pro Max | Máxima complejidad (research, modelos) |

## Ver también
- `/model list` — ver configuración actual de todas las skills y agentes
- `/model reset skill <nombre>` — volver una skill al tier default
- `/model set agent <nombre> <tier>` — cambiar tier de un sub-agente
