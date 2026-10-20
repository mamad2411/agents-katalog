# GEMINI.md — Dashboard de Análisis de Retención Estudiantil

## Contexto del proyecto

Sistema web de análisis de datos estudiantiles basado en el dataset **"Predict Students' Dropout and Academic Success"** (UCI ML Repository, DOI: 10.24432/C5MC89).

El objetivo es construir un dashboard interactivo en **HTML/CSS/JS puro** (sin frameworks) que permita al público general explorar los datos y obtener conclusiones visuales sobre factores que influyen en el abandono escolar, el perfil del estudiante exitoso y el impacto socioeconómico en el rendimiento académico.

---

## Stack tecnológico

- **Backend de datos:** Python 3 (solo para preprocesamiento, no hay servidor)
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **Gráficas:** [Chart.js](https://www.chartjs.org/) desde CDN
- **Sin frameworks, sin Node.js, sin bundlers**
- El sistema corre abriendo `index.html` directamente en el navegador

---

## Estructura de carpetas

Crea exactamente esta estructura desde el inicio:

```
proyecto/
├── CLAUDE.md                  ← este archivo
├── data/
│   ├── data.csv               ← dataset original (ya existe, no modificar)
│   └── data.json              ← generado por process/script.py
├── process/
│   └── script.py              ← script de limpieza y generación de JSON
├── index.html                 ← dashboard principal
├── styles.css                 ← estilos globales
└── js/
    ├── data-loader.js         ← carga y expone data.json al resto de módulos
    ├── charts.js              ← todas las gráficas de los módulos 1–4
    └── predictor.js           ← lógica del módulo 5 (predictor de riesgo)
```

---

## Paso 1 — Script Python (`process/script.py`)

Este script debe ejecutarse **una sola vez** para generar `data/data.json`. Debe hacer lo siguiente:

### 1.1 Leer el CSV
```python
import pandas as pd, json, numpy as np
df = pd.read_csv('data/data.csv', sep=';')  # el separador es punto y coma
```

### 1.2 Decodificar columnas categóricas

Aplica estos mapeos para reemplazar los códigos numéricos por etiquetas legibles:

```python
MAPS = {
    'Marital status': {1:'Soltero',2:'Casado',3:'Viudo',4:'Divorciado',5:'Unión libre',6:'Separado'},
    'Application mode': {
        1:'1ª fase general',2:'Decreto 612/93',5:'1ª fase Azores',7:'Otro título superior',
        10:'Decreto 854-B/99',15:'Internacional',16:'1ª fase Madeira',17:'2ª fase general',
        18:'3ª fase general',26:'Decreto 533-A/99 b2',27:'Decreto 533-A/99 b3',
        39:'Mayor 23 años',42:'Transferencia',43:'Cambio carrera',44:'Técnico especializado',
        51:'Cambio institución',53:'Ciclo corto',57:'Cambio inst. internacional'
    },
    'Course': {
        33:'Biocombustibles',171:'Diseño y Multimedia',8014:'Trabajo Social (noche)',
        9003:'Agronomía',9070:'Diseño Comunicación',9085:'Enfermería Veterinaria',
        9119:'Ing. Informática',9130:'Equinicultura',9147:'Administración',
        9238:'Trabajo Social',9254:'Turismo',9500:'Enfermería',9556:'Higiene Oral',
        9670:'Publicidad y Marketing',9773:'Periodismo',9853:'Educación Básica',
        9991:'Administración (noche)'
    },
    'Daytime/evening attendance': {1:'Diurno',0:'Nocturno'},
    'Previous qualification': {
        1:'Bachillerato',2:'Licenciatura',3:'Grado',4:'Maestría',5:'Doctorado',
        6:'Ed. superior incompleta',9:'12° no completado',10:'11° no completado',
        12:'Otro 11°',14:'10° año',15:'10° no completado',19:'Ed. básica 3er ciclo',
        38:'Ed. básica 2do ciclo',39:'Esp. tecnológica',40:'Grado 1er ciclo',
        42:'Técnico superior',43:'Maestría 2do ciclo'
    },
    'Nacionality': {
        1:'Portugués',2:'Alemán',6:'Español',11:'Italiano',13:'Holandés',14:'Inglés',
        17:'Lituano',21:'Angoleño',22:'Caboverdiano',24:'Guineano',25:'Mozambicano',
        26:'Santotomense',32:'Turco',41:'Brasileño',62:'Rumano',100:'Moldavo',
        101:'Mexicano',103:'Ucraniano',105:'Ruso',108:'Cubano',109:'Colombiano'
    },
    'Gender': {1:'Masculino',0:'Femenino'},
    'Scholarship holder': {1:'Con beca',0:'Sin beca'},
    'Debtor': {1:'Con deuda',0:'Sin deuda'},
    'Tuition fees up to date': {1:'Al corriente',0:'En mora'},
    'Displaced': {1:'Desplazado',0:'Local'},
    'International': {1:'Internacional',0:'Local'},
    'Educational special needs': {1:'Sí',0:'No'},
    'Daytime/evening attendance': {1:'Diurno',0:'Nocturno'},
}
for col, mapping in MAPS.items():
    if col in df.columns:
        df[col] = df[col].map(mapping).fillna(df[col])
```

### 1.3 Calcular estadísticas agregadas

El JSON debe contener las siguientes secciones:

```python
output = {
    # Datos crudos decodificados (lista de registros)
    "records": df.to_dict(orient='records'),

    # Módulo 1 — Resumen general
    "summary": {
        "total": int(len(df)),
        "by_target": df['Target'].value_counts().to_dict(),
        "by_course": df.groupby('Course')['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "age_distribution": df['Age at enrollment'].value_counts().sort_index().to_dict(),
        "by_gender": df.groupby('Gender')['Target'].value_counts().unstack(fill_value=0).to_dict(),
    },

    # Módulo 2 — Factores de abandono
    "dropout_factors": {
        "by_attendance": df.groupby('Daytime/evening attendance')['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "by_scholarship": df.groupby('Scholarship holder')['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "by_debtor": df.groupby('Debtor')['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "by_tuition": df.groupby('Tuition fees up to date')['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "grade_vs_approved": df[['Curricular units 1st sem (grade)',
                                  'Curricular units 1st sem (approved)','Target']].to_dict(orient='records'),
    },

    # Módulo 3 — Perfil comparativo (promedios por Target)
    "profiles": df.groupby('Target')[[
        'Curricular units 1st sem (grade)',
        'Curricular units 2nd sem (grade)',
        'Curricular units 1st sem (approved)',
        'Curricular units 2nd sem (approved)',
        'Age at enrollment',
        'Admission grade',
        'Previous qualification (grade)',
    ]].mean().round(2).to_dict(),

    # Módulo 4 — Impacto socioeconómico
    "socioeconomic": {
        "by_mothers_edu": df.groupby("Mother's qualification")['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "by_fathers_edu": df.groupby("Father's qualification")['Target'].value_counts().unstack(fill_value=0).to_dict(),
        "correlation_matrix": df[[
            'Unemployment rate','Inflation rate','GDP',
            'Curricular units 1st sem (grade)','Curricular units 2nd sem (grade)',
            'Scholarship holder encoded','Debtor encoded'
        ]].assign(
            **{
                'Scholarship holder encoded': df['Scholarship holder'].map({'Con beca':1,'Sin beca':0}),
                'Debtor encoded': df['Debtor'].map({'Con deuda':1,'Sin deuda':0}),
            }
        ).corr().round(3).to_dict(),
        "gdp_dropout": df.groupby('GDP')['Target'].apply(
            lambda x: round((x=='Dropout').sum()/len(x)*100, 1)
        ).to_dict(),
    },

    # Módulo 5 — Umbrales para el predictor de riesgo (calculados desde los datos)
    "risk_thresholds": {
        "grade_1st_sem_dropout_mean": round(float(df[df['Target']=='Dropout']['Curricular units 1st sem (grade)'].mean()), 2),
        "grade_1st_sem_graduate_mean": round(float(df[df['Target']=='Graduate']['Curricular units 1st sem (grade)'].mean()), 2),
        "approved_1st_sem_dropout_mean": round(float(df[df['Target']=='Dropout']['Curricular units 1st sem (approved)'].mean()), 2),
        "approved_1st_sem_graduate_mean": round(float(df[df['Target']=='Graduate']['Curricular units 1st sem (approved)'].mean()), 2),
        "dropout_rate_debtor": round(float((df[df['Debtor']=='Con deuda']['Target']=='Dropout').mean()*100), 1),
        "dropout_rate_no_debtor": round(float((df[df['Debtor']=='Sin deuda']['Target']=='Dropout').mean()*100), 1),
        "dropout_rate_scholarship": round(float((df[df['Scholarship holder']=='Con beca']['Target']=='Dropout').mean()*100), 1),
        "dropout_rate_no_scholarship": round(float((df[df['Scholarship holder']=='Sin beca']['Target']=='Dropout').mean()*100), 1),
        "dropout_rate_evening": round(float((df[df['Daytime/evening attendance']=='Nocturno']['Target']=='Dropout').mean()*100), 1),
        "dropout_rate_daytime": round(float((df[df['Daytime/evening attendance']=='Diurno']['Target']=='Dropout').mean()*100), 1),
    }
}

with open('data/data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2, default=str)

print("data.json generado correctamente.")
```

**Ejecutar con:** `cd proyecto && python process/script.py`

---

## Paso 2 — `index.html`

Estructura base del dashboard. Debe incluir:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Análisis de Retención Estudiantil</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- Navbar con las 5 secciones -->
  <nav id="navbar">
    <span class="nav-brand">Análisis Estudiantil</span>
    <div class="nav-links">
      <a href="#modulo1" class="nav-link active">Resumen</a>
      <a href="#modulo2" class="nav-link">Abandono</a>
      <a href="#modulo3" class="nav-link">Perfiles</a>
      <a href="#modulo4" class="nav-link">Socioeconómico</a>
      <a href="#modulo5" class="nav-link">Predictor</a>
    </div>
  </nav>

  <main>
    <!-- Módulo 1: Resumen general -->
    <section id="modulo1" class="module">
      <h2>Resumen general</h2>
      <div class="kpi-grid" id="kpi-cards"></div>
      <div class="charts-grid">
        <div class="chart-card"><canvas id="chart-target"></canvas></div>
        <div class="chart-card"><canvas id="chart-courses"></canvas></div>
        <div class="chart-card"><canvas id="chart-age"></canvas></div>
        <div class="chart-card"><canvas id="chart-gender"></canvas></div>
      </div>
    </section>

    <!-- Módulo 2: Factores de abandono -->
    <section id="modulo2" class="module">
      <h2>Factores de abandono</h2>
      <div class="insight-bar" id="insight-dropout"></div>
      <div class="charts-grid">
        <div class="chart-card"><canvas id="chart-attendance"></canvas></div>
        <div class="chart-card"><canvas id="chart-scholarship"></canvas></div>
        <div class="chart-card"><canvas id="chart-debtor"></canvas></div>
        <div class="chart-card"><canvas id="chart-scatter"></canvas></div>
      </div>
    </section>

    <!-- Módulo 3: Perfil comparativo -->
    <section id="modulo3" class="module">
      <h2>Perfil comparativo</h2>
      <div class="insight-bar" id="insight-profile"></div>
      <div class="charts-grid">
        <div class="chart-card chart-card--wide"><canvas id="chart-radar"></canvas></div>
        <div class="chart-card"><canvas id="chart-sem-grades"></canvas></div>
      </div>
      <div id="profile-table"></div>
    </section>

    <!-- Módulo 4: Impacto socioeconómico -->
    <section id="modulo4" class="module">
      <h2>Impacto socioeconómico</h2>
      <div class="insight-bar" id="insight-socio"></div>
      <div class="charts-grid">
        <div class="chart-card"><canvas id="chart-mothers-edu"></canvas></div>
        <div class="chart-card"><canvas id="chart-gdp"></canvas></div>
        <div class="chart-card chart-card--wide" id="heatmap-container"></div>
      </div>
    </section>

    <!-- Módulo 5: Predictor de riesgo -->
    <section id="modulo5" class="module">
      <h2>Predictor de riesgo de abandono</h2>
      <p class="module-desc">Ajusta las características de un estudiante hipotético y el sistema calculará su nivel de riesgo basado en patrones estadísticos del dataset.</p>
      <div class="predictor-layout">
        <div class="predictor-form" id="predictor-form"></div>
        <div class="predictor-result" id="predictor-result"></div>
      </div>
    </section>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <script src="js/data-loader.js"></script>
  <script src="js/charts.js"></script>
  <script src="js/predictor.js"></script>
</body>
</html>
```

---

## Paso 3 — `js/data-loader.js`

Carga el JSON y lo expone globalmente:

```javascript
let DATASET = null;

async function loadData() {
  const res = await fetch('data/data.json');
  DATASET = await res.json();
  document.dispatchEvent(new Event('data-ready'));
}

loadData();
```

---

## Paso 4 — `js/charts.js`

Debe escuchar el evento `data-ready` e inicializar todos los módulos:

```javascript
document.addEventListener('data-ready', () => {
  initModule1();
  initModule2();
  initModule3();
  initModule4();
});
```

### Paleta de colores (usar siempre esta)

```javascript
const COLORS = {
  Graduate: '#1D9E75',   // teal
  Dropout:  '#D85A30',   // coral
  Enrolled: '#7F77DD',   // purple
  neutral:  '#888780',
};
```

### Módulo 1 — funciones requeridas

- `renderKPIs()` — 4 cards: Total estudiantes, % Graduate, % Dropout, % Enrolled
- `chartTarget()` — pastel con los 3 grupos (Graduate/Dropout/Enrolled)
- `chartCourses()` — barras horizontales top-10 carreras con más alumnos
- `chartAge()` — histograma de edad al ingreso (bins de 5 años)
- `chartGender()` — barras agrupadas por género y Target

### Módulo 2 — funciones requeridas

- `chartAttendance()` — barras agrupadas: Diurno vs Nocturno, desglosado por Target
- `chartScholarship()` — barras: Con beca vs Sin beca por Target
- `chartDebtor()` — barras: Con deuda vs Sin deuda por Target
- `chartScatter()` — dispersión: eje X = nota 1er sem, eje Y = unidades aprobadas, color = Target
- `renderInsightDropout()` — texto con el factor de mayor riesgo calculado dinámicamente

### Módulo 3 — funciones requeridas

- `chartRadar()` — radar con 6 dimensiones, una línea por cada Target (Graduate, Dropout, Enrolled). Normalizar valores al rango 0–1 antes de graficar.
- `chartSemGrades()` — líneas dobles: promedio de notas sem 1 vs sem 2 por Target
- `renderProfileTable()` — tabla HTML con estadísticas clave por Target (media, mediana de notas y unidades aprobadas)

### Módulo 4 — funciones requeridas

- `chartMothersEdu()` — barras horizontales: nivel educativo madre, apiladas por Target (top 8 niveles)
- `chartGDP()` — línea: GDP en eje X, % dropout en eje Y
- `renderHeatmap()` — heatmap HTML puro (tabla con celdas coloreadas según valor de correlación, sin librería externa). Usar escala de color: correlación negativa = coral, cero = gris, positiva = teal.

---

## Paso 5 — `js/predictor.js`

### Descripción

Formulario interactivo que calcula un puntaje de riesgo (0–100) basado en los umbrales estadísticos del JSON. Sin IA, solo aritmética ponderada.

### Variables del formulario

| Input | Tipo | Etiqueta |
|---|---|---|
| `grade` | slider 0–20 | Promedio de notas (1er semestre) |
| `approved` | slider 0–10 | Unidades aprobadas (1er semestre) |
| `attendance` | toggle | Turno: Diurno / Nocturno |
| `scholarship` | toggle | ¿Tiene beca? |
| `debtor` | toggle | ¿Tiene deuda con la institución? |
| `tuition` | toggle | ¿Pagos al corriente? |

### Lógica del puntaje de riesgo

```javascript
function calculateRisk(inputs, thresholds) {
  let risk = 0;

  // Factor notas (peso 40)
  const gradeRange = thresholds.grade_1st_sem_graduate_mean - thresholds.grade_1st_sem_dropout_mean;
  const gradeScore = Math.max(0, Math.min(1, (thresholds.grade_1st_sem_graduate_mean - inputs.grade) / gradeRange));
  risk += gradeScore * 40;

  // Factor unidades aprobadas (peso 25)
  const appRange = thresholds.approved_1st_sem_graduate_mean - thresholds.approved_1st_sem_dropout_mean;
  const appScore = Math.max(0, Math.min(1, (thresholds.approved_1st_sem_graduate_mean - inputs.approved) / appRange));
  risk += appScore * 25;

  // Factor deuda (peso 15)
  if (inputs.debtor) risk += 15;

  // Factor turno nocturno (peso 10)
  if (inputs.attendance === 'Nocturno') risk += 10;

  // Factor sin beca (peso 10)
  if (!inputs.scholarship) risk += 10;

  return Math.round(Math.min(100, Math.max(0, risk)));
}
```

### Visualización del resultado

Mostrar un semáforo visual con tres estados:

- **0–33** → Riesgo bajo (verde) — "El perfil del estudiante es similar al de quienes se gradúan"
- **34–66** → Riesgo medio (amarillo) — "Algunos factores de riesgo presentes. Monitoreo recomendado"
- **67–100** → Riesgo alto (rojo) — "Perfil con alta coincidencia con estudiantes que abandonaron"

Incluir debajo del semáforo una lista de los factores que más están contribuyendo al riesgo.

---

## Paso 6 — `styles.css`

### Requisitos de diseño

- Fondo: `#f8f7f4` (gris cálido muy claro)
- Tipografía: `system-ui, -apple-system, sans-serif`
- Navbar fijo en la parte superior, fondo blanco, borde inferior sutil
- Cada `section.module` con `padding: 3rem 2rem`, `max-width: 1200px`, `margin: 0 auto`
- `.kpi-grid`: grid de 4 columnas en desktop, 2 en tablet, 1 en móvil
- `.charts-grid`: grid de 2 columnas en desktop, 1 en móvil
- `.chart-card`: fondo blanco, border-radius 12px, padding 1.5rem, borde `1px solid #e5e3de`
- `.chart-card--wide`: ocupa 2 columnas
- `.insight-bar`: borde izquierdo 4px coral, fondo coral muy claro, padding 1rem, margin-bottom 1.5rem
- Scroll suave entre secciones: `scroll-behavior: smooth`
- El navbar resalta el link activo mientras el usuario scrollea (usar Intersection Observer)

---

## Reglas generales de desarrollo

1. **Siempre empezar por `process/script.py`** — sin `data.json` nada funciona.
2. **No usar `alert()`, `console.error` visible al usuario** — manejar errores silenciosamente o con mensajes en el DOM.
3. **Todos los datos vienen de `data.json`** — ningún valor hardcodeado en el JS.
4. **Los colores siempre del objeto `COLORS`** — Graduate=teal, Dropout=coral, Enrolled=purple.
5. **Responsive** — el dashboard debe verse bien en móvil (una columna) y desktop (dos columnas).
6. **Sin dependencias externas excepto Chart.js** desde CDN de jsdelivr.
7. **Cada gráfica debe tener título** configurado en las opciones de Chart.js.
8. **El heatmap de correlaciones** se hace en HTML puro (tabla), no con Chart.js.
9. **El predictor recalcula en tiempo real** con evento `input` en todos los controles.
10. **El navbar activo** se actualiza con `IntersectionObserver` al hacer scroll.

---

## Orden de desarrollo recomendado

```
1. process/script.py         → ejecutar y verificar data.json
2. index.html                → estructura completa con todas las secciones
3. styles.css                → layout, navbar, cards, grid
4. js/data-loader.js         → carga del JSON
5. js/charts.js              → módulo 1 (KPIs + 4 gráficas)
6. js/charts.js              → módulo 2 (factores de abandono)
7. js/charts.js              → módulo 3 (perfiles comparativos)
8. js/charts.js              → módulo 4 (socioeconómico + heatmap)
9. js/predictor.js           → módulo 5 (predictor con semáforo)
10. styles.css               → ajustes finales responsive
```

---

## Dataset — referencia rápida

- **Archivo:** `data/data.csv`
- **Separador:** punto y coma (`;`)
- **Instancias:** 4,424 estudiantes
- **Variable objetivo:** columna `Target` con valores `Graduate`, `Dropout`, `Enrolled`
- **Sin valores nulos** (preprocesado)
- **Fuente:** UCI ML Repository — https://doi.org/10.24432/C5MC89
- **Licencia:** CC BY 4.0