---
name: football-betting-analysis
description: >
  Análisis pre-partido de fútbol en 8 capas. Recibe una consulta en lenguaje
  natural, descubre el partido en FlashScore MCP, ejecuta build_match_context.py
  para obtener un contexto normalizado en JSON, y produce un informe estructurado
  con lenguaje probabilístico. Solo para partidos notstarted. No inventa datos,
  no suple la predicción con modelos heurísticos.
---

# Football Betting Analysis

## 1. Overview

Análisis pre-partido de fútbol. Recibe una consulta en lenguaje natural, descubre
el partido en FlashScore MCP, ejecuta el script de preprocesamiento
`build_match_context.py` para obtener un contexto JSON normalizado, y produce un
informe estructurado con lenguaje probabilístico.

**Solo para partidos `notstarted` e `inprogress`.** Para partidos `finished` esta skill no aplica.

El modelo no llama endpoints directamente (salvo para match discovery).
Recibe datos ya limpios, normalizados y consolidados en `final_context`.

El análisis es una interpretación de la evidencia disponible. No es un pick.
No es una garantía. Siempre usa lenguaje como "podría", "señal", "sugiere".
Nunca: "va a ganar", "es fijo", "el over entra seguro".

---

## 2. When to Use / When Not to Use

### Usar cuando:

- El usuario pide análisis pre-partido de un partido específico de fútbol.
- El partido está en estado `notstarted`.

### No usar cuando:

- El partido ya está `finished` → esta skill no aplica.
- La consulta es sobre un torneo o equipo sin partido específico → no procede. Se puede ofrecer buscar partidos próximos de ese equipo.
- `final_context` no pudo generarse.

**Nota arquitectónica:** Esta versión no dispone de predicción basada en modelos
de aprendizaje. Por diseño, la capa predictiva es odds-driven — las probabilidades
numéricas SOLO viennent de odds. Los indicadores solo modulan confianza, no generan
porcentajes.

---

## 3. Fuente de Datos — FlashScore MCP

### Endpoints utilizados

| Endpoint                        | Uso                                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| `Get_Match_Details`             | Evento completo + odds                                                                   |
| `Get_Match_H2H`                 | Head-to-head                                                                             |
| `Get_Match_Stats`               | Llamado en paralelo para cada partido del historial (matches[i]) — solo para construir form.advanced agregado |
| `Get_Match_Lineups`             | Alineaciones si existen + `missingPlayers` con nombre y motivo de ausencia               |
| `Get_Team_Results`              | Match discovery (fallback) + historial de resultados del equipo                          |
| `Get_Team_Fixtures`             | Match discovery (primario) — próximos partidos del equipo                                |
| `Get_Tournament_Standings`      | Contexto de forma/posición en torneo                                                     |
| `Get_Match_Standings_OverUnder` | Standings O/U                                                                            |
| `Get_Tournament_Top_Scorers`    | Goleadores del torneo                                                                    |
| `Get_Match_Standings_Form`      | Forma reciente dentro del partido                                                        |

### Lo que NO existe en FlashScore (y nunca se debe inventar)

| Qué no existe                                     | Consecuencia                                                                                                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alineaciones confirmadas pre-partido              | El endpoint `Get_Match_Lineups` existe, pero las alineaciones confirmadas pueden no estar disponibles aún. Pueden venir vacías. No inventar alineación. Usar `predictedLineups` si está disponible — el script lo procesa automáticamente. |
| Histórico de lesiones pre-existentes              | No existe en la API. No inventar.                                                                                                                       |
| `missingPlayers` sin datos en `Get_Match_Lineups` | Si el endpoint no lo trae → no inventar motivo ni jugador.                                                                                              |

**Comportamiento de `normalize_lineups` en `build_match_context.py`:**

El script procesa las alineaciones en dos niveles de prioridad:

1. **Si `startingLineups` existe (alineaciones oficiales confirmadas):**
   - `starting_lineups` — alineación titular confirmada [API]
   - `missing_players` — jugadores ausentes con motivo [API]
   - `substitutes` — sustitutos disponibles [API]
   - `predicted_lineups` → vacío
   - `unsure_missing` — vacío

2. **Si `startingLineups` NO existe pero `predictedLineups` sí (alineación predicha/no confirmada):**
   - `unsure_missing` — jugadores cuya ausencia no está confirmada [API]
   - `missing_players` → jugadores ausentes con motivo [API]
   - `predicted_lineups` — alineación predicha [API]
   - `starting_lineups` → vacío
   - `substitutes` → vacío

**Nota:** `Get_Match_Lineups` puede aportar `missingPlayers` (nombre + motivo) incluso cuando las alineacionesConfirmadas no existen. Usar ese dato cuando esté disponible.

**Fuente de cada señal en el análisis:**

| Tag      | Significado                                         |
| -------- | --------------------------------------------------- |
| `[API]`  | Dato directo de un endpoint de FlashScore MCP       |
| `[ODDS]` | Calculado de cuotas de mercado                      |
| `[IND]`  | Indicador calculado a partir de los datos de la API |
| `[N/A]`  | Dato no disponible en la API                        |

---

## 4. Pipeline de Análisis

### 4.1 Parsing de la consulta

De la consulta en lenguaje natural extraer:

```
{
  home_team:  string,      // equipo mencionado primero
  away_team:  string,       // equipo mencionado segundo (o null si solo uno)
  date_from:  ISO 8601,    // fecha inicio del rango
  date_to:    ISO 8601,    // fecha fin del rango
  league:     string|null,  // competición mencionada (o null)
  analysis_mode: "prematch"  // único modo soportado
}
```

**Reglas de parsing:**

| Situación                                         | Regla                                                         |
| ------------------------------------------------- | ------------------------------------------------------------- |
| El usuario dice "hoy"                             | `date_from = hoy`, `date_to = hoy`                            |
| El usuario dice "mañana"                          | `date_from = mañana`, `date_to = mañana`                      |
| El usuario dice "este finde"                      | `date_from = viernes`, `date_to = domingo`                    |
| El usuario dice "esta semana" sin día             | `date_from = lunes`, `date_to = domingo`                      |
| Solo un equipo mencionado                         | Buscar el próximo partido de ese equipo en el rango de 7 días |
| Nombres con acento ("Atletico", "Inter")          | Normalizar quitando acentos antes de buscar                   |
| Nombres parciales ("Barça", "Atleti")             | Fuzzy match contra `home_team`/`away_team` del resultado      |
| Competición mencionada ("la league", "champions") | Filtrar por `league_id` tras buscar                           |

| `status = "notstarted"` | `analysis_mode = "prematch"` → proceed |
| `status = "inprogress"` | → Proceed con análisis en vivo. |
| `status = "finished"` | → No aplica. Notificar al usuario. |

**Si solo un equipo matchea pero hay múltiples candidatos del rival:**
→ Clarificación obligatoria. Preguntar: "¿Buscás el [equipo] vs [candidato A] o vs [candidato B]?"

### 4.2 Match Discovery (Fase 1 — SOLO esta fase usa MCP directamente)

**Paso 1 — Búsqueda por API de búsqueda de equipos:**

```
1. Normalizar nombres de ambos equipos (minúsculas, sin acentos, sin puntos)
2. Usar la API de búsqueda:
   GET https://s.livesport.services/api/v2/search/?q=<query>&lang-id=13&type-ids=1,2,3,4&project-id=202&project-type-id=1
3. Filtrar resultados: sport.id=1 (fútbol), type.id=2 (Team)
4. Retorna: team_id, name, url, country, country_id
   → Si 1 resultado: proceed con ese team_id
   → Si >1 resultado: clarificación obligatoria ("¿Buscás [equipo A] o [equipo B]?")
   → Si 0 resultados: ir a paso 5 (fallback a /data/main_teams.csv)
```

**Normalización para la API de búsqueda:**

- Minúsculas
- Quitar acentos: á→a, é→e, í→i, ó→o, ú→u
- Quitar puntos: "Atl." → "Atl"
- Quitar espacios extra

**Paso 2 — Lookup de equipos en /data/main_teams.csv (fallback):**

```
5. Si no se encontró el equipo en la API, buscar en /data/main_teams.csv:
   Normalizar nombres (mismas reglas que arriba)
6. Buscar match exacto en /data/main_teams.csv después de normalizar
   → Si 1 resultado: proceed
   → Si >1 resultado: clarificación obligatoria
7. Si 0 resultados exactos: intentar substring match
   → Si 1 resultado: proceed
   → Si >1 resultado: clarificación obligatoria
8. Si 0 resultados: buscar coincidencias cercanas (similitud string)
   → Calcular similaridad entre nombre buscado y todos los nombres en /data/main_teams.csv
   → Si hay candidatos con similitud ≥ umbral (ej: Levenshtein ratio ≥ 0.6):
      → Si 1 candidato cercano: "¿Quisiste decir [nombre]?"
      → Si >1 candidatos: mostrar top 3: "¿Buscás alguno de estos? [A], [B], [C]"
   → Si ningún candidato cercano: "No encontré '[equipo]'. Verificá el nombre."
```

**Sugerencia de candidatos cercanos:**

- Umbral de similaridad: ratio ≥ 0.6 (Levenshtein o similar)
- Mostrar máximo 3 candidatos ordenados por similaridad descendente
- Incluir el nombre original del CSV (sin normalizar) en la sugerencia

**Paso 3 — Búsqueda por overlap en fixtures:**

```
 9. Get_Team_Fixtures(team_id_home, page=1)
10. Get_Team_Fixtures(team_id_away, page=1)
11. Filtrar fixtures del rango date_from..date_to
12. Buscar partido donde home_team_id o away_team_id de un fixture
    coincida con el team_id del otro equipo (overlap)
    → Si 1 resultado: proceed
    → Si >1 resultado: priorizar por fecha más cercana al rango solicitado
    → Si 0: ir a paso 4
```

**Paso 4 — Fallback a results:**

```
13. Get_Team_Results(team_id_home, page=1)
14. Get_Team_Results(team_id_away, page=1)
15. Buscar overlap (misma lógica que fixtures)
    → Si 1 resultado: proceed
    → Si >1: priorizar por fecha más cercana
    → Si 0: "No encontré el partido [Home] vs [Away] en las fechas indicadas."
```

**Paso 5 — Verificación y extracción:**

```
16. Verificar estado del evento:
    → status = "notstarted" → proceed con análisis pre-partido
    → status = "inprogress" → proceed con análisis en vivo
    → status = "finished" → "El partido ya finalizó. Esta skill es solo pre-partido y en vivo."
17. Extraer IDs:
    → event_id = del evento encontrado
    → home_team_id = del equipo local
    → away_team_id = del equipo visitante
```

**Priorización cuando hay múltiples candidatos:**

1. Si el usuario mencionó liga → priorizar esa liga.
2. Si el usuario mencionó fecha exacta → solo considerar esa fecha.
3. Si hay exactamente 1 partido de cada equipo combinado → usar ese.
4. **Si múltiples partidos del mismo equipo → priorizar el más cercano en el tiempo al rango de fechas de la consulta.** Esto evita clarificaciones innecesarias.
5. Si no, clarificación obligatoria.

### 4.3 Preprocesamiento (Fase 2 — build_match_context.py)

**Esta es la única manera de obtener datos para el análisis. No usar endpoints MCP directamente para obtener datos del partido.**

```
python scripts/build_match_context.py <event_id> <home_team_id> <away_team_id>
```

**Qué hace el script:**

1. Ejecuta todas las llamadas a endpoints de FlashScore internamente
2. Construye H2H desde el historial de resultados de ambos equipos
3. Resume historial de forma (GF, GC, over, BTTS, home/away split) — `form.basic`
4. Extrae y normaliza ausencias desde `Get_Match_Lineups`
5. Valida qué mercados de odds existen realmente y bloquea los que no existan
6. Integra estadísticas avanzadas de cada partido del historial (tiros, posesión, xG, etc.) — solo para construir `form.advanced` (los datos individuales no se emiten en el JSON final)
7. Agrega player stats históricas por equipo (`player_stats.as_historical_home/away`)
8. Incorpora contexto de torneo (posición, forma, over/under standings)
9. Emite warnings de consistencia
10. Consolida toda la información en un único JSON (`final_context`)

**Output del script — `final_context`:**

```
{
  "meta": {
    event_id, home_team_id, away_team_id, generated_at
  },
  "match": {
    event_id,
    home_team: { id, name, event_participant_id },
    away_team: { id, name, event_participant_id },
    tournament: { id, stage_id, name },
    country, referee, timestamp, datetime, status,
    scores: {
      home, away,
      home_total, away_total,
      home_1st_half, away_1st_half,
      home_2nd_half, away_2nd_half,
      home_extra_time, away_extra_time,
      home_penalties, away_penalties
    },
    "lineups": {
      home: {
        formation,              // formación reportada (de predictedFormation)
        lineup_count,           // cantidad de jugadores en alineación
        // -- Si hay alineaciones oficiales (startingLineups existe): --
        starting_lineups: [...],       // alineación titular oficial [API]
        missing_players: [...],        // jugadores ausentes con motivo [API]
        substitutes: [...],            // sustitutos disponibles [API]
        predicted_lineups: [],        // vacío
        unsure_missing: [],           // vacío
        // -- Si NO hay oficiales pero hay predicción (predictedLineups): --
        starting_lineups: [],          // vacío
        missing_players: [],           // vacío
        substitutes: [],               // vacío
        predicted_lineups: [...],      // alineación predicha [API]
        unsure_missing: [...],         // ausencias no confirmadas [API]
      },
      away: { formation, lineup_count, starting_lineups, missing_players, substitutes, predicted_lineups, unsure_missing },
      warnings: string[] | null
    },
    "preview": string | null,  // texto de previa del partido — web scraping de FlashScore (DOM o contentParsed embebido)
    // --- inprogress or finished only ---
    "summary": object | null,    // eventos clave del partido (goles, tarjetas, etc.) [API]
    "commentary": object | null, // narración minuto a minuto [API]
    "match_stats": object | null, // estadísticas del partido (posesión, tiros, xG, etc.) [API]
    "player_stats": object | null, // stats de jugadores del partido actual [API]
    "live_analysis": {           // solo para status = "inprogress"
      total_goals_over_25: { probability, signal, confidence },
      total_goals_under_25: { ... },
      btts_yes: { ... },
      btts_no: { ... },
      next_goal_home: { ... },
      next_goal_away: { ... },
      next_goal_no_more: { ... },  // explicit class — no more goals in the match
      next_corner: { lean, signal, confidence, mode: "signal_only" },
      total_cards: { lean, signal, confidence, mode: "signal_only" },
      1x2_final: { probabilities: { home, draw, away }, model_version, calibrated, inputs_quality, top_factors, prematch_source, confidence, warnings },
      match_minute: int,
      current_score: { home: int, away: int },
      warnings: []
    } | null,
    warnings: string[] | null
  },
  "odds": {
    available_markets: string[],
    odds_home, odds_draw, odds_away,
    odds_over_25, odds_under_25,
    odds_btts_yes, odds_btts_no,
    warnings: string[]
  },
  "implied_probs": {
    prob_home, prob_draw, prob_away,
    prob_over_25, prob_btts_yes
  },
  "h2h": {
    total_matches,
    home_team_wins,   // partidos ganados por el equipo local del análisis
    away_team_wins,   // partidos ganados por el equipo visitante del análisis
    draws,
    home_team_goals_for,   // goles anotados por el equipo local del análisis en H2H
    away_team_goals_for,   // goles anotados por el equipo visitante del análisis en H2H
    total_goals, both_teams_scored,
    matches: [{
      match_id, timestamp,
      home_score, away_score,
      home_team, away_team,
      tournament_id, tournament_name,
      team_is_home, opponent
    }],
    basic_stats: {               // stats básicos del historial H2H
      // home_team = stats of the team that IS home in the CURRENT match (Bayern)
      // away_team = stats of the team that IS away in the CURRENT match (Real Madrid)
      // form_string/points/home_ppg/away_ppg excluded — not meaningful in h2h context
      home_team: {
        wins, losses, draws,
        gf_avg, gc_avg, total_goals
      },
      away_team: {
        wins, losses, draws,
        gf_avg, gc_avg, total_goals
      },
      both_teams_scored,
      over_25_freq, btts_freq,
      total_matches,
      total_goals
    },
    advanced_stats: {             // stats agregadas del historial (de advanced_stats de cada match)
      // For home_team_results / away_team_results: same flat structure
      // For h2h: split by current-match home/away identity
      // Each sub-dict has: { overall: {...}, first_half: {...}, second_half: {...} }
      home_team: {
        overall: { attack: {...}, defense: {...}, control: {...}, set_pieces_and_territory: {...}, discipline: {...}, duels_and_defending: {...}, efficiency: {...}, derived: {...} },
        first_half: { /* mismo formato que overall */ },
        second_half: { /* mismo formato que overall */ }
      },
      away_team: {
        overall: { attack: {...}, defense: {...}, control: {...}, set_pieces_and_territory: {...}, discipline: {...}, duels_and_defending: {...}, efficiency: {...}, derived: {...} },
        first_half: { /* mismo formato que overall */ },
        second_half: { /* mismo formato que overall */ }
      }
    },
    home_team_player_stats: {
      general: { minutes_total, goals_total, assists_total, shots_total, shots_on_target_total, key_passes_total, tackles_won_total, interceptions_total, ball_recoveries_total, yellow_cards_total, red_cards_total, goals_per_90, assists_per_90, shots_per_90, position_distribution, in_base_lineup_count, substitute_count },
      individual: {
        [player_name]: {
          "position": "Goalkeeper" | "Defender" | "Midfielder" | "Forward" | "Unknown",
          offense:    { GOALS, EXPECTED_GOALS, ASSISTS_GOAL, EXPECTED_ASSISTS, SHOTS_TOTAL, SHOTS_ON_TARGET, BIG_CHANCES_CREATED, BIG_CHANCES_MISSED },
          creation:   { KEY_PASSES, FINAL_THIRD_ENTRIES_TOTAL, BOX_ENTRIES, THROUGH_BALLS },
          possession: { TOUCHES_TOTAL, MATCH_MINUTES_PLAYED, PASSES_TOTAL },
          defense:    { DUELS_WON, DUELS_TOTAL, DUELS_EFFICIENCY, TACKLES_WON, INTERCEPTIONS, BALL_RECOVERIES },
          efficiency: { PASSES_ACCURACY, LONG_BALLS_ACCURACY, CROSSES_ACCURACY, DRIBBLES_EFFICIENCY },
          discipline: { FOULS_COMMITTED, FOULS_SUFFERED, CARDS_YELLOW, CARDS_RED, TURNOVERS, ERRORS_LEAD_TO_SHOT, ERRORS_LEAD_TO_GOAL },
          goalkeeping:{ SAVES_TOTAL, GOALS_CONCEDED, GOALS_PREVENTED, EXPECTED_GOALS_ON_TARGET_FACED, BIG_CHANCES_SAVED },
          derived:    { xg_per_shot, goals_minus_xg, xa_minus_assists, duels_win_pct, actions_per_90 }
        }, ...
      }
    },
    away_team_player_stats: { /* misma estructura */ },
    warnings: string[]
  },
  "home_team_results": {
    matches: [{
      match_id, timestamp,
      goals_for, goals_against, total_goals, both_teams_scored,
      tournament_id, tournament_name,
      team_is_home, opponent
    }],
    basic_stats: {               // stats básicos del historial
      all_matches, form_string, points,
      home_gf_avg, home_gc_avg,
      over_25_freq, btts_freq,
      home_ppg, home_gf_avg, home_gc_avg,
      away_ppg, away_team_gf_avg, away_team_gc_avg,
      total_matches, wins, draws, losses,
      goals_for, goals_against, total_goals, both_teams_scored
    },
    advanced_stats: {            // stats agregadas del historial (de advanced_stats de cada match)
      overall: {
        attack: {
          goals_for_avg, xg_for_avg, xgot_for_avg, xa_for_avg,
          shots_for_avg, shots_on_target_for_avg, shots_off_target_for_avg,
          blocked_shots_for_avg, shots_inside_box_for_avg, shots_outside_box_for_avg,
          big_chances_for_avg, touches_in_opposition_box_avg, hit_woodwork_avg
        },
        defense: {
          goals_against_avg, xg_against_avg, xgot_faced_avg,
          shots_against_avg, shots_on_target_against_avg, shots_off_target_against_avg,
          blocked_shots_against_avg, shots_inside_box_against_avg, shots_outside_box_against_avg,
          big_chances_against_avg, touches_in_opposition_box_against_avg,
          goalkeeper_saves_avg, errors_leading_to_shot_avg, errors_leading_to_goal_avg, goals_prevented_avg
        },
        control: {
          possession_avg, passes_accuracy_avg, passes_completed_avg, passes_attempted_avg,
          long_pass_accuracy_avg, long_passes_completed_avg, long_passes_attempted_avg,
          final_third_pass_accuracy_avg, final_third_passes_completed_avg, final_third_passes_attempted_avg,
          accurate_through_passes_avg
        },
        set_pieces_and_territory: {
          corners_for_avg, corners_against_avg, offsides_for_avg, offsides_against_avg,
          free_kicks_for_avg, free_kicks_against_avg, throw_ins_for_avg, throw_ins_against_avg,
          cross_accuracy_avg, crosses_completed_avg, crosses_attempted_avg
        },
        discipline: {
          yellow_cards_avg, red_cards_avg, cards_total_avg, fouls_committed_avg
        },
        duels_and_defending: {
          tackles_success_pct_avg, tackles_won_avg, tackles_attempted_avg,
          duels_won_avg, clearances_avg, interceptions_avg
        },
        efficiency: {
          shot_accuracy_pct, goal_conversion_pct, big_chance_conversion_pct,
          xg_per_shot, shots_on_target_faced_per_goal_against, save_pct,
          finishing_overperformance, conceding_overperformance
        },
        derived: {
          xg_balance_avg, xg_ratio, shots_share, shots_on_target_share,
          big_chances_balance_avg, corners_balance_avg, discipline_balance_avg
        }
      },
      first_half: { /* mismo formato que overall */ },
      second_half: { /* mismo formato que overall */ },
      warnings: []
    },
    player_stats_as_home: {
      general: { minutes_total, goals_total, assists_total, shots_total, shots_on_target_total, key_passes_total, tackles_won_total, interceptions_total, ball_recoveries_total, yellow_cards_total, red_cards_total, goals_per_90, assists_per_90, shots_per_90, position_distribution, in_base_lineup_count, substitute_count },
      individual: {
        [player_name]: {
          "position": "Goalkeeper" | "Defender" | "Midfielder" | "Forward" | "Unknown",
          offense:    { GOALS, EXPECTED_GOALS, ASSISTS_GOAL, EXPECTED_ASSISTS, SHOTS_TOTAL, SHOTS_ON_TARGET, BIG_CHANCES_CREATED, BIG_CHANCES_MISSED },
          creation:   { KEY_PASSES, FINAL_THIRD_ENTRIES_TOTAL, BOX_ENTRIES, THROUGH_BALLS },
          possession: { TOUCHES_TOTAL, MATCH_MINUTES_PLAYED, PASSES_TOTAL },
          defense:    { DUELS_WON, DUELS_TOTAL, DUELS_EFFICIENCY, TACKLES_WON, INTERCEPTIONS, BALL_RECOVERIES },
          efficiency: { PASSES_ACCURACY, LONG_BALLS_ACCURACY, CROSSES_ACCURACY, DRIBBLES_EFFICIENCY },
          discipline: { FOULS_COMMITTED, FOULS_SUFFERED, CARDS_YELLOW, CARDS_RED, TURNOVERS, ERRORS_LEAD_TO_SHOT, ERRORS_LEAD_TO_GOAL },
          goalkeeping:{ SAVES_TOTAL, GOALS_CONCEDED, GOALS_PREVENTED, EXPECTED_GOALS_ON_TARGET_FACED, BIG_CHANCES_SAVED },
          derived:    { xg_per_shot, goals_minus_xg, xa_minus_assists, duels_win_pct, actions_per_90 }
        }, ...
      }
    },
    player_stats_as_away: { /* misma estructura */ },
    warnings: string[] | null
  },
  "away_team_results": {
    matches: [{
      match_id, timestamp,
      goals_for, goals_against, total_goals, both_teams_scored,
      tournament_id, tournament_name,
      team_is_home, opponent
    }],
    basic_stats: {               // stats básicos del historial
      all_matches, form_string, points,
      home_gf_avg, home_gc_avg,
      over_25_freq, btts_freq,
      home_ppg, home_gf_avg, home_gc_avg,
      away_ppg, away_team_gf_avg, away_team_gc_avg,
      total_matches, wins, draws, losses,
      goals_for, goals_against, total_goals, both_teams_scored
    },
    advanced_stats: {            // stats agregadas del historial (de advanced_stats de cada match)
      overall: { /* mismo formato que en home_team_results */ },
      first_half: { /* mismo formato */ },
      second_half: { /* mismo formato */ },
      warnings: []
    },
    player_stats_as_home: {
      general: { minutes_total, goals_total, assists_total, shots_total, shots_on_target_total, key_passes_total, tackles_won_total, interceptions_total, ball_recoveries_total, yellow_cards_total, red_cards_total, goals_per_90, assists_per_90, shots_per_90, position_distribution, in_base_lineup_count, substitute_count },
      individual: {
        [player_name]: {
          "position": "Goalkeeper" | "Defender" | "Midfielder" | "Forward" | "Unknown",
          offense:    { GOALS, EXPECTED_GOALS, ASSISTS_GOAL, EXPECTED_ASSISTS, SHOTS_TOTAL, SHOTS_ON_TARGET, BIG_CHANCES_CREATED, BIG_CHANCES_MISSED },
          creation:   { KEY_PASSES, FINAL_THIRD_ENTRIES_TOTAL, BOX_ENTRIES, THROUGH_BALLS },
          possession: { TOUCHES_TOTAL, MATCH_MINUTES_PLAYED, PASSES_TOTAL },
          defense:    { DUELS_WON, DUELS_TOTAL, DUELS_EFFICIENCY, TACKLES_WON, INTERCEPTIONS, BALL_RECOVERIES },
          efficiency: { PASSES_ACCURACY, LONG_BALLS_ACCURACY, CROSSES_ACCURACY, DRIBBLES_EFFICIENCY },
          discipline: { FOULS_COMMITTED, FOULS_SUFFERED, CARDS_YELLOW, CARDS_RED, TURNOVERS, ERRORS_LEAD_TO_SHOT, ERRORS_LEAD_TO_GOAL },
          goalkeeping:{ SAVES_TOTAL, GOALS_CONCEDED, GOALS_PREVENTED, EXPECTED_GOALS_ON_TARGET_FACED, BIG_CHANCES_SAVED },
          derived:    { xg_per_shot, goals_minus_xg, xa_minus_assists, duels_win_pct, actions_per_90 }
        }, ...
      }
    },
    player_stats_as_away: { /* misma estructura */ },
    warnings: string[] | null
  },
  "standings": {
    teams: { [team_id]: { position, name, points, wins, draws, losses, goals, goal_difference } },
    warnings: string[] | null
  },
  "overunder_standings": {
    teams: { [team_id]: { over, under, average_goals } },
    warnings: string[] | null
  },
  "form_standings": {
    teams: { [team_id]: { points, form_string } },
    warnings: string[] | null
  },
  "top_scorers": {
    home_scorers: [{ name, player_id, team, goals, assists }],
    away_scorers: [...],
    warnings: string[] | null
  },
  "tournament_top_scorers": {
    home_scorers: [...],
    away_scorers: [...],
    warnings: string[] | null
  }
}
```

**Reglas de uso del script:**

- El modelo NO vuelve a llamar endpoints MCP después de recibir `final_context`.
- Todos los datos del análisis vienen del JSON.
- Si el script emite warnings → el modelo debe tomarlos en cuenta y no contradecirlos.
- Si el JSON marca algo como `[N/A]` → el modelo lo usa como `[N/A]`, no intenta inferir el dato.
- El script es determinista: dada la misma entrada, siempre produce la misma salida.
- El modelo no recalcula ni reinterpreta datos ya normalizados salvo para explicar su significado.

**Si el script falla o no puede ejecutarse:**
→ "No pude generar el contexto del partido. Análisis no viable."

---

## 5. Las 8 Capas — Definición Exacta

Cada capa tiene: inputs, cálculos, output obligatorio, degradación.

---

### Capa 1 — Contexto Base

**Inputs:** `odds_home`, `odds_draw`, `odds_away`, `odds_over_25`,
`odds_btts_yes`.

**Cálculos:**

- Probabilidad implícita de mercado: `1 / odds`
- Probabilidad implícita Over 2.5: `1 / odds_over_25`
- Probabilidad implícita BTTS: `1 / odds_btts_yes`
- Sesgo: favorito claro (>60%), favorito leve (50-60%), equilibrado (<50%)

**Output obligatorio:**

```
## 1. Contexto del Partido
- Partido: [Home] vs [Away]
- Competición: [Liga]
- Fecha/hora: [ISO 8601]
- Estado: [notstarted/inprogress]
---
Mercado dice [ODDS]:
- [Home]: [prob]% | Draw: [prob]% | [Away]: [prob]%
- Over 2.5: [cuota] → prob implícita [prob]%
- BTTS: [cuota] → prob implícita [prob]%
---
Indicadores históricos [IND]:
- Indicadores favorecen: [Home/Away/Equilibrado]
- Soporte histórico: [bajo/medio/alto]
Mercado vs datos: [alineados/parcialmente alineados/en conflicto] — [explicación breve]
```

**Degradación:**

- Si no hay odds → no usar diff mercado vs indicadores. Usar solo odds si disponibles.
- Si neither → capa 1 muy degradada.

**Output para `postmatch`:**

```
Mercado esperaba [ODDS]:
- [Home]: [prob]% | Draw: [prob]% | [Away]: [prob]%
- Over 2.5: [cuota] → prob implícita [prob]%
- BTTS: [cuota] → prob implícita [prob]%

Resultado vs expectativa [ODDS]/[IND]:
- El resultado [fue alineado / parcialmente alineado / sorpresivo] con las probabilidades del mercado
```

---

### Capa 2 — Descriptiva de Equipos

**Inputs:** `Get_Team_Results` (historial), `Get_Match_H2H`, `Get_Tournament_Standings` (si aplica), `final["preview"]` (web scraping — texto de previa del partido en FlashScore).

**Cálculos:**

- Puntos últimos N: de resultados del equipo
- Forma: resultados recientes (W/D/L)
- Goles avg: `goals_scored / matches_played` y `goals_conceded / matches_played`
- Over 2.5 freq: contar partidos con total > 2.5 en últimos N
- BTTS freq: contar partidos con gol de ambos en últimos N
- Perfil: según goles generados vs goles reales (sobre/sub-reperformance)
- H2H: de `Get_Match_H2H` si existe

**Output obligatorio:**

```
## 2. [Qué Viene Pasando / Lo Que Está Pasando]

[Adaptar según estado del partido:]
- status = notstarted → "Qué Viene Pasando"
- status = inprogress → "Lo Que Está Pasando" + marcador actual + minuto
- status = finished → "Lo Que Pasó"

[Home] [IND] [marcador si inprogress]:
  Forma: [form_string] — [pts] pts / [N] pts posibles
  Goles: [home_gf_avg]/[home_gc_avg]
  Over 2.5: [X/N] | BTTS: [X/N] (si hay datos)
  En casa: [home_ppg] ppg | [home_goals]GF / [home_goals]GC
  Perfil: [ofensivo/conservador/equilibrado/inestable]

[ away ] [IND]:
  [mismo formato]

H2H [IND]: [X]PJ — [home_team_wins]V-local [draws]E [away_team_wins]V-visitante | goles local [home_team_goals_for] / visitante [away_team_goals_for]
  [score reciente 1]
  [score reciente 2]

Nota: [si la forma se extrajo solo del evento actual (N=1), indicarlo]

[Para notstarted]: Previa del partido [IND]: [texto de previa de FlashScore — si no disponible: "Previa no disponible [N/A]"]
[Para inprogress]: Eventos recientes: [resumen de últimos eventos del partido — de summary.events]
[Para finished]: Resultado final: [home] [H] - [A] [away] | [marcador final]
[Para postmatch — analysis_mode = "postmatch"]:
  El resultado [confirma/rompe] la tendencia reciente de cada equipo
  Resultado vs forma: [el partido fue consistente/inconsistente con la forma previa]

**Nota:** La previa del partido debe ser concisa. Si excede 3-4 oraciones, resumir los puntos más relevantes para el análisis.
```

**Degradación:**

- Si `home_form` viene vacío → solo listar H2H disponible. Forma = N/A.
- Si no hay H2H → omitir sección H2H.
- Siempre incluir la nota si la muestra es N < 5.
- Si `preview` no disponible → texto "Previa no disponible [N/A]".
- Si status = inprogress → usar "Lo que Está Pasando" con marcador y minuto actual.
- Si status = finished → usar "Lo Que Pasó" con resultado final.
- Si `analysis_mode = "postmatch"`: incluir comparación de resultado vs forma previa y vs odds pre-partido.

---

### Capa 3 — Protagonistas

**Regla transversal (nueva):** Capa 3 = solo hechos + contexto mínimo. NO interpretación, NO peso, NO conclusiones, NO lenguaje causal.

```
Capa 3 NO puede contener:
- conclusiones
- inferencias
- lenguaje causal ("porque", "esto implica", "esto sugiere")

Solo descripción estructurada de datos.
```

**Pregunta única:** ¿qué hay? (NO: ¿qué significa?)

**Lógica de dos carriles (siempre intentar ambos):**

- **Carril A:** `Get_Match_Player_Stats` → stats individuales (gol, asistencia, tiros, etc.)
- **Carril B:** `Get_Match_Lineups` → `missingPlayers` (nombre + motivo de ausencia)

Si Carril A falla pero Carril B devuelve `missingPlayers` → usar Carril B.
Si ambos fallan → capa degradada con `[N/A]`.

---

**Carril A — Inputs directos de `Get_Match_Player_Stats`:**
`goals`, `assists`, `shots`, `shots_on_target`, `key_passes`,
`tackles_won`, `interceptions`, `ball_recoveries`, `yellow_cards`,
`red_cards`, `minutes`.

**Reglas — SIN fórmulas heurísticas:**

- No usar pesos (0.3, 0.5, etc.) ni normalizaciones inventadas.
- No calcular "impact score", "impacto ofensivo", ni ninguna métrica compuesta.
- **Sí se permite:** ranking directo por métrica individual (más goles, más pases clave, etc.).
- **Dependencia:** proporción directa de goles/producción del jugador vs total del equipo.

**Regla (nueva):** Los outputs de Capa 3 deben ser puramente descriptivos. No incluir frases como "esto afecta al equipo", "es una baja clave", "pierde poder ofensivo". Toda interpretación va en Capa 5.

**Outputs por jugador (datos directos, sin fórmulas):**

```
[Jugador X] ([pos]):
  Producción:
  - Goles: X
  - Asistencias: X

  Volumen ofensivo:
  - Tiros: X (X a puerta)

  Creación:
  - Pases clave: X

  Disciplina:
  - Amarillas: X | Rojas: X
```

**Top N por equipo (ranking directo por métrica — sin scores compuestos):**

```
Top generadores de gol [IND]:
1. [Jugador A] — [X] goles
2. [Jugador B] — [X] goles

Top creadores [IND]:
1. [Jugador A] — [X] pases clave
2. [Jugador B] — [X] pases clave
```

**Dependencia ofensiva:**

- Calcular: `(goles jugador / total goles equipo) * 100`
- Umbral: >40% → "Dependencia ofensiva alta [IND]"
- Si un equipo tiene >50% de producción en un solo jugador → alertar.

---

**Carril B — Fuentes desde `Get_Match_Lineups`:**

El script `build_match_context.py` procesa las alineaciones en dos niveles de prioridad (definidos en `normalize_lineups`):

- **Nivel 1 — Alineaciones oficiales (`startingLineups` existe):**
  - `missing_players`: lista de jugadores ausentes con `name`, `player_id`, `reason`, `country` [API]
  - `substitutes`: sustitutos disponibles [API]
  - `starting_lineups`: alineación titular oficial [API]
  - `predicted_lineups`: vacío
  - `unsure_missing`: vacío

- **Nivel 2 — Alineación predicha (`startingLineups` NO existe, `predictedLineups` sí):**
  - `unsure_missing`: jugadores cuya ausencia no está confirmada [API]
  - `predicted_lineups`: alineación predicha [API]
  - `missing_players`: vacío
  - `substitutes`: vacío
  - `starting_lineups`: vacío

Si `missing_players` contiene jugadores ausentes, reportarlos según los niveles de ausencia definidos más abajo.

**Niveles de ausencia (en orden de profundidad):**

1. **Ausencia observada [API]:** Nombre + motivo tal como los devuelve la API (Injury, Inactive, Leg Injury, etc.). Solo reportar lo que la API indica.

2. **Ausencia contextualizada [IND]:** Si además ese jugador aparece en `Get_Tournament_Top_Scorers` o como goleador/generador relevante en `Get_Team_Results` o `Get_Match_Player_Stats` de partidos previos → indicar: "[jugador] ausente — registrado como goleador/top del torneo [IND]." Solo reportar como hecho. No interpretar impacto.

3. **Influencia incierta [N/A/IND]:** Si un jugador está ausente pero no hay evidencia suficiente para estimar su peso → marcar como "influencia no cuantificable con precisión [N/A]". Nunca inventar impacto.

**Regla sobre Carril B solo:**

- Ausencias sin contexto adicional (no aparecen como goleadores relevantes, no hay ranking que los respalde) → reportar como simples hechos observados [API].
- No calcular cuánto baja el equipo por cada ausente.
- No estimar goles perdidos ni probabilidad de gol afectada.
- La acumulación de ausencias en un mismo equipo puede mencionarse como observación contextual (reduce certidumbre sobre el techo de rendimiento del equipo), pero sin cifras inventadas.

**Output obligatorio:**

```
## 3. Protagonistas

[Carril A — Si hay player-stats:]
[Jugador] ([pos]):
  Producción:
  - Goles: X
  - Asistencias: X
  Volumen ofensivo:
  - Tiros: X (X a puerta)
  Creación:
  - Pases clave: X
  Disciplina:
  - Amarillas: X | Rojas: X

[Top del partido]

Dependencia ofensiva:
- [Equipo]: [jugador] → [X]% de los goles del equipo [IND]

[Carril B — Si hay missingPlayers sin player-stats:]
Ausencias observadas [API]:
- [Equipo]: [Jugador] — [motivo de la API]
- [Equipo]: [Jugador] — [motivo de la API]

[Si hay ausencia contextualizada:]
- [Equipo]: [Jugador] — ausente [IND] — [goleador/top scorer del torneo / pieza habitual]

Lectura contextual [IND]:
- [Equipo] llega con [X] bajas registradas en la API.
- La influencia de las ausencias se considera [alta/moderada/baja] solo si coincide con
  otras señales disponibles (producción en排行榜, dependencia ofensiva, ranking histórico, etc.).
- Influencia no cuantificable con precisión [N/A]: [jugador(es)].

[Si commentary disponible Y coincide con indicadores:]
Patrón de estilo observado: [descripción]

[Si commentary disponible pero NO coincide con indicadores:]
Patrón de estilo: [N/A] — dato observacional no respaldado por stats.
```

**Degradación:**

- Si no hay player-stats NI missingPlayers → "Sin datos disponibles de protagonistas [N/A] — capa degradada." No inventar jugadores ni ausencias.
- Si solo hay missingPlayers (Carril B) → capa Carril A = N/A; Carril B según niveles de ausencia definidos arriba.
- Si hay ambos → usar Carril A y añadir Carril B como enriquecimiento.
- Si `analysis_mode = "postmatch"`: `player_stats` como fuente principal, `summary.events` como fuente secundaria, `commentary` como apoyo terciario — solo para describir secuencias, nunca para inventar superioridad estructural. Si no hay `player_stats` pero sí `summary.events` → basarse en eventos para describir el desarrollo.

---

### Capa 4 — Indicadores Compuestos

**Regla (nueva):** Capa 4 puede nombrar indicadores, pero no explicar por qué importan.

| Capa | Qué hace |
|------|----------|
| 4    | **Mide** |
| 5    | **Explica** |

**Pregunta única:** ¿cuánto? (NO: ¿por qué importa?)

```
Capa 4 NO puede contener:
- conclusiones
- inferencias
- lenguaje causal ("porque", "esto implica", "esto sugiere")
- "esto favorece a X"
- "esto indica partido abierto"

Solo descripción estructurada de datos comparables entre equipos.
```

**Inputs:** historial de equipos (`home_team_results`, `away_team_results`, `h2h`), odds.

**Cálculos:**

- Ventaja ofensiva: diferencia de goles avg entre equipos
- Fragilidad defensiva: goles recibidos / partidos jugados del equipo visitante
- Gap forma: puntos últimos N de cada equipo
- Gap casa/fuera: PPG home vs PPG away
- Riesgo Over 2.5: promedio de freq Over de ambos
- Riesgo BTTS: promedio de freq BTTS de ambos
- Disciplina: promedio de tarjetas de ambos equipos (de `Get_Match_Stats`)
- Volatilidad: desv. estándar de goles en últimos 5 de cada equipo
- Estabilidad muestra: N partidos disponibles vs mínimo 5

**Coherencia mercado-datos [IND]:**
- **Alta:** mercado y datos históricos favorecen el mismo lado Y con magnitudes similares.
- **Moderada:** coinciden en el lado, difieren en intensidad.
- **Baja:** favorecen lados distintos, o uno ve equilibrio y el otro no.

*(Medición de alineación — no interpretación de por qué.)*

**Output obligatorio:**

```
## 4. Indicadores Compuestos

Ventaja ofensiva: [Home] por [+/-X.XX] goles [IND]
Fragilidad: [Away] recibe [X.XX] goles/partido [IND]
Gap forma (últimos [N]): [Home] [+/-X pts] sobre [Away] [IND]
Gap casa/fuera: [Home] [+/-X.X] ppg [IND]
Riesgo Over 2.5: [X%] [IND]
Riesgo BTTS: [X%] [IND]
Volatilidad: [baja/media/alta] [IND]
Índice disciplina: [bajo (<1.0 yc/pp) / medio (1.0-1.5) / alto (>1.5)] [IND]
Mercado vs datos: [alta/moderada/baja]
Estabilidad muestra: [N] partidos / mínimo 5 — [suficiente/limitado]
```

**Degradación:**

- Si no hay forma (N<3) → gap forma y volatilidad = N/A.

---

## 4.5 Regla Global de No-Redundancia

> Cada capa debe aportar información **NUEVA**.
> Si una idea ya fue expresada en una capa anterior, no debe repetirse
> salvo que se transforme (ej: de dato → interpretación).

**Impide:**
- Capa 5 re-explicar forma, odds o rachas de capa 2
- Capa 6 re-diagnosticar de capa 5
- Capa 8 resumir señales de capa 6

**Permite:**
- Capa 5 toma datos de capa 2 y los interpreta causalmente
- Capa 6 toma señales de capa 5 y las pondera por peso
- Capa 8 toma la priorización de capa 6 y la traduce a lectura final

**Flujo correcto:**
```
datos (capa 2) → medición (capa 4) → interpretación (capa 5) → priorización (capa 6) → predicción (capa 7) → síntesis (capa 8)
```

---

### Capa 5 — Diagnóstica

**Pregunta única:** ¿Por qué esas señales importan?

**Scope:** Causas + contradicciones + sostenibilidad

**Inputs:** output de capas 1, 2 y 4.

**Regla de causalidad (nueva):** Las causas NO pueden ser una reformulación directa de un dato numérico. Deben explicar el mecanismo, no repetir la métrica.

❌ Ejemplo malo:
"Madrid domina en casa porque tiene 2.25 ppg"

✅ Ejemplo bueno:
"Madrid domina en casa por la intensidad que impone en transiciones y la presión alta — el Bernabéu amplifica esa dinámica, no solo el promedio de puntos"

**Output obligatorio:**

```
## 5. [Por Qué Pasa / Qué Está Pasando]

[Adaptar según estado:]
- notstarted: "Por Qué Pasa" — análisis de tendencias pre-partido
- inprogress: "Qué Está Pasando" — evaluación de lo que ocurre vs lo esperado + comparación con pre-match

Causas [IND]:
- [Causa real derivada de datos — explicar el MECANISMO, no reformular la métrica]
- [Causa 2]

Contradicciones:
- [contradicción 1 — mercado vs stats, forma vs contexto]
- [contradicción 2]

¿Sostenible?
- sí/no — [razón basada en evidencia]

[Para inprogress: usando `live_analysis` y `summary.events`]
Análisis en vivo: El marcador [X-X] [refleja/no refleja] lo que muestran las stats (xG: [xg_home]-[xg_away], posesión: [pos_home]%-[pos_away]%).
[¿El equipo [X] domina aunque no esté ganando?]
[¿Los últimos eventos cambiaron la dinámica?]
[`live_analysis` proporciona probabilidades actualizadas para cada mercado.]
```

**Degradación:**

- Si no hay stats → no se pueden generar causas ni análisis de sostenibilidad.
- Si no hay forma → "Datos insuficientes para diagnóstico de tendencia [N/A]."
- Si `analysis_mode = "postmatch"`: el foco cambia de "qué podría pasar" a "qué pasó y por qué". Incluir contradicciones entre expectativa previa y desarrollo real.

---

### Capa 6 — Ponderación de Señales

**Reglas de peso:**

| Peso         | Qué cuenta                                                                                                                           | Qué NO cuenta                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Fuerte**   | Tiros, consistencia (N≥5), coincidencia mercado-indicadores, producción jugadores clave                                              | Rachas cortas sin respaldo, marcadores aislados |
| **Moderada** | Forma con N=3-4, H2H sin contexto de local/visita, diff mercado-historial moderada, múltiples ausencias corroboradas por otras capas |                                                 |
| **Débil**    | N<3, diff mercado-historial alta, mercado sin respaldo en indicadores, ausencias sin corroboración de otras capas                    |                                                 |

**Regla de identidad (nueva):** Capa 6 es la ÚNICA capa de priorización. No se repite en Capa 8.

Capa 6 NO debe:
- Nueva interpretación causal (eso es capa 5)
- Recomendación de mercados (eso es capa 8)
- Repetir señales ya dichas

Solo: priorizar por peso (fuerte/moderada/débil/no utilizable) con fuentes.

**Ausencias múltiples registradas en `Get_Match_Lineups.missingPlayers`:**

- Pueden contar como señal **moderada** solo si coinciden con otras capas (producción del equipo, ranking, dependencia ofensiva, forma).
- Nunca como señal **fuerte** por sí solas — una lista de ausentes, sola, no domina el análisis.
- Si las ausencias no tienen corroboración en stats o rankings → señal **débil**.

**Output obligatorio:**

```
## 6. Qué Señales Pesan Más

Fuertes [fuente]:
- [señal + razón]

Moderadas [fuente]:
- [señal + razón]

Débiles [razón]:
- [señal]

No utilizables [razón]:
- [señal]

Outliers:
- [partido + razón]
```

**Degradación:**

- Si Capa 4 no está disponible → señales no utilizables.
- Si `analysis_mode = "postmatch"`: el foco cambia de "qué podría pasar" a "qué pasó y por qué". Incluir contradicciones entre expectativa previa y desarrollo real.

---

### Capa 7 — Predictiva (odds-driven)

**Reglas de combinación:**

| Condición                            | Acción                                                        |
| ------------------------------------ | ------------------------------------------------------------- |
| Odds disponibles                     | Usar odds como fuente base de probabilidades                  |
| Indicadores disponibles              | Solo para subir/bajar confianza, no para inventar porcentajes |
| Ni odds ni indicadores               | No emitir predictiva. Confianza muy baja.                     |
| Mercado y datos históricos coinciden | Reforzar señal                                                |
| Contradicción mercado vs historial   | Atenuar. Marcar "inseguro".                                   |

**Las probabilidades numéricas SOLO pueden salir de odds. Los indicadores NO crean porcentajes.**

**Output obligatorio:**

```
## 7. [Qué Podría Pasar / Qué Se Espera]

[Adaptar según estado:]
- notstarted: "Qué Podría Pasar" — predicción pre-partido
- inprogress: "Qué Se Espera" — predicción actualizada con marcador actual y stats en vivo

[Para notstarted:]
Resultado: [Home] [X]% | Empate [Y]% | [Away] [Z]%
Goles esperados: [Home] [X.XX] | [Away] [Y.XX] (basado en avg histórico)
Over 1.5: [X]% | Over 2.5: [Y]% | BTTS: [Z]%
Tipo: [cerrado/abierto/defensivo/competido]
Confianza: [muy baja/baja/media/media-alta/alta] — [motivo de la calificación]

[Para inprogress: usando `live_analysis`]
Marcador actual: [Home] [X] - [Y] [Away] — [minuto]'
xG acumulado: [Home] [X.XX] | [Away] [Y.XX]

Señales en vivo [live_analysis]:
- Over 2.5: [probability]% | BTTS: [probability]%
- Próximo gol — Home: [probability]% | Away: [probability]% | No más goles: [probability]%
- Esquinas próximo: [lean] | Señal: [signal]
- 1X2 final — Home: [probability]% | Empate: [probability]% | Away: [probability]%

Resultado esperado al final: [Home] [X] - [Y] [Away] (basado en xG y tiempo restante)
Tipo de partido: [cerrado/abierto/defensivo/competido]
Confianza: [muy baja/baja/media/media-alta/alta] — [motivo de la calificación]
[¿El equipo que está perdiendo merece estar abajo?]

Nota: "Predictiva basada en `live_analysis` + odds históricas."
```

**Degradación:**

- Si ni odds ni indicadores → "Predictiva no disponible [N/A] — datos insuficientes."
- Si contradicción mercado vs historial → añadir: "⚠ Mercado y datos históricos no coinciden.
  Incertidumbre elevada."

---

### Capa 8 — Lectura Final

**Pregunta única:** ¿Con qué lectura final me quedo?

**Scope:** Interpretación humana + 1-2 mercados bien justificados (conceptual, no numérico)

**Regla (nueva):** Capa 8 opera a nivel conceptual — escenarios, riesgos, lectura. NO repite probabilidades ni métricas numéricas de Capa 7, NO re-justifica con datos, NO resume señales de Capa 6.

Capa 8 NO debe:
- Lista de señales más fuertes (ya dichas en Capa 6)
- Lista de alertas (ya dichas en Capa 5)
- Lista de mercados con sustento (ya dichos en Capa 7)
- Probabilidades ni métricas numéricas

Solo traduce a: qué escenario tiene más sentido, qué riesgo oculto existe, qué NO comprar.

**Output obligatorio:**

```
## 8. Lectura Final

- Qué escenario tiene más sentido
- Qué escenario tiene riesgo oculto
- Qué NO comprar del partido

Opcional:
- 1-2 mercados bien justificados (no lista — solo decisión final bien fundamentada)

Nota: "Las lecturas anteriores son las mejor soportadas por la evidencia disponible."
```

**Degradación:**

- Si Capa 7 es muy baja confianza → Capa 8 se reduce a "lectura de escenarios sin recomendación de mercados".
- Si `analysis_mode = "postmatch"`: el foco cambia de "qué podría pasar" a "qué pasó y por qué". Incluir contradicciones entre expectativa previa y desarrollo real.

---

## 9. Política de Confianza

### Confianza global

| Estado de los datos                              | Confianza máxima                 |
| ------------------------------------------------ | -------------------------------- |
| Evento + odds + stats + player-stats + historial | **Alta**                         |
| Evento + odds + stats (sin player-stats)         | **Media-alta**                   |
| Evento + odds (sin stats)                        | **Media**                        |
| Evento solo                                      | **Baja**                         |
| Sin evento                                       | **Muy baja / análisis inviable** |

### Ajuste por capa

| Dato faltante                  | Capas afectadas | Reducción                       |
| ------------------------------ | --------------- | ------------------------------- |
| Sin odds                       | Capa 1, Capa 7  | Máx. media                      |
| Sin stats (tiros, corners, xG) | Capa 4, Capa 5  | Señales de gol debilitadas      |
| Sin player-stats               | Capa 3          | Solo texto N/A                  |
| Sin historial (N<3)            | Capa 2, Capa 4  | Datos históricos no disponibles |
| Sin H2H                        | Capa 2          | H2H = N/A                       |

### Por capa

Cada capa puede marcarse como:

- **Completa** — todos los inputs disponibles.
- **Parcial** — algunos inputs faltantes, se usa texto [N/A] correspondiente.
- **No disponible** — inputs requeridos faltantes, no se puede calcular.

---

## 11. Anti-Racionalizaciones

Esta es la sección de guardrails. Es de cumplimiento **obligatorio**.
Todo lo que sigue **no se puede hacer**, sin excepción:

### No inventar datos

- `[N/A]` → **no inventar.** Si no hay player-stats → capa 3 = "Sin datos suficientes."
- No inventar alineaciones, lesionados, sancionados, técnicos.
- No inventar H2H si `Get_Match_H2H` viene vacío o null.

### No usar fuentes externas

- No consultar Bzzoiro, SofaScore, Transfermarkt, Wikipedia, ni ninguna otra
  fuente durante el análisis.
- La única fuente válida es FlashScore MCP (a través de los endpoints listados
  en sección 3).

### No improvisar modelos

- No construir un modelo heurístico para reemplazar la predicción basada en modelos de aprendizaje.
- Esta versión es odds-driven por diseño. No improvisar modelo propio.
- Las probabilidades numéricas en Capa 7 SOLO viennent de odds. No de cuentas propias.
- No usar pesos (0.3, 0.5, etc.) ni métricas compuestas en Capa 3.

### No vender certeza

- No decir "va a ganar", "es fijo", "el over entra seguro".
- Siempre decir "podría", "señal", "sugiere", "la evidencia apunta a".
- Siempre indicar confianza.

### No omitir contradicciones

- Si mercado e indicadores favorecen lados distintos → decirlo explícitamente.
- Si una señal es ruido y no tendencia → decirlo.

### No rellenar con frases vacías

- Cada sección tiene output definido con campos obligatorios.
- Si no hay dato para un campo → "[N/A]" + razón breve.
- No dejar una sección "blanca" ni con frases genéricas que no dicen nada.

### No interpretar mal FlashScore MCP

- `Get_Team_Fixtures` / `Get_Team_Results` es la vía de match discovery.
  No existe `/api/events/?team=X`.
- Para partidos `inprogress`: análisis en vivo disponible — usar datos actuales del partido.
- Para partidos `finished`: `analysis_mode = "postmatch"` → proceed con análisis post-partido.

**Reglas para `postmatch`:**

- No inventar causas. Commentary sirve para describir secuencias y momentos, no para inventar superioridad estructural.
- Si no hay `match_stats` → limitarse a resultado + eventos + forma + odds previas.
- Si no hay `summary.events` → no hablar de "punto de quiebre" (la output format ya filtra: "solo si existe evidencia en summary.events o commentary").
- Si los datos son insuficientes para una lectura completa → usar la etiqueta "Lectura parcial del desarrollo" y listar qué datos no estuvieron disponibles.
- Commentary es dato observacional, no señal principal. Solo válido si coincide con indicadores de otras capas.

---

## 12. Formato de Salida del Análisis

**Estructura obligatoria (en este orden exacto):**

```
# [Home] vs [Away] — [Competición] ([Fecha])

[8 capas completas]

---
Confianza global: [muy baja/baja/media/media-alta/alta]
```

**Longitud orientativa por sección:**

- Capas 1-2: 8-15 líneas cada una.
- Capas 3-6: 5-12 líneas cada una.
- Capas 7-8: 8-15 líneas cada una.

**Datos no disponibles:**

- Siempre usar `[N/A]` para datos faltantes.
- Siempre explicar brevemente por qué.

**Señales fuertes / moderadas / débiles:**

- Presentar como lista con viñeta, no en prosa.

**Cierre del análisis:**

- Siempre incluir la confianza global.
- Siempre distinguir entre señal fuerte y correlación débil.
- Nunca cerrar con una frase determinista.

### Guardado de datos

1. Guardar este análisis en un txt en ./claude/skills/football-betting-analysis/football-analysis.
2. Crear una carpeta cuyo nombre corresponda con el nombre de la competición, por ejemplo, Champions League 25-26.
3. Guardar el archivo como [DD_MM_AAAA] [EQUIPO LOCAL] vs [EQUIPO VISITANTE] [JORNADA_X].txt donde X en [JORNADA_X] es el # de la jornada que se juega o si es 1/4 de final u 1/8, lo que corresponda.

---

## 13. Quick Reference

```
CONSULTA NL → parsing → { home, away, date_from, date_to, league? }

Fase 1 (MCP directo):
  Match discovery:   livesport search API → /data/main_teams.csv (fallback) → Get_Team_Fixtures → Get_Team_Results
  → analysis_mode = prematch | live | postmatch
  → Extraer: event_id, home_team_id, away_team_id

Fase 2 (build_match_context.py):
  python scripts/build_match_context.py <event_id> <home_team_id> <away_team_id>
  → Devuelve final_context JSON con todos los datos normalizados

NO LLAMAR ENDPOINTS MCP DIRECTAMENTE PARA DATOS DEL PARTIDO.
Solo Get_Team_Fixtures / Get_Team_Results para match discovery.
```

**Umbrales de confianza:**

| Datos                                            | Confianza máx. |
| ------------------------------------------------ | -------------- |
| Evento + odds + stats + player-stats + historial | Alta           |
| Evento + odds + stats (sin player-stats)         | Media-alta     |
| Evento + odds (sin stats)                        | Media          |
| Evento solo                                      | Baja           |
| Sin evento                                       | Inviable       |

**Etiquetas de fuente obligatorias en todo el análisis:**
`[API]` `[ODDS]` `[IND]` `[N/A]`

---

## Reglas de No-Redundancia (Quick Ref)

| Capa | Pregunta única | Qué NO hacer |
|------|---------------|--------------|
| 3    | ¿qué hay?     | No interpretar, no concluir |
| 4    | ¿cuánto?      | No explicar por qué importa |
| 5    | ¿por qué?     | No reformular datos numéricos — explicar mecanismo |
| 6    | ¿cuáles pesan?| No repetir diagnóstico de capa 5 |
| 8    | ¿con qué quedo?| No resumir señales de capa 6, no repetir números de capa 7 |

---

## 14. Agujeros Cerrados

| Racionalización                                                                                | Contramedida                                                                                                                                               |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Usé Bzzoiro/SofaScore/otra fuente porque FlashScore no tenía"                                 | **Prohibido.** Solo FlashScore MCP. Sin excepciones.                                                                                                       |
| "No había player-stats así que inventé alineación"                                             | **Prohibido.** Capa 3 Carril B: usar `missingPlayers` de `Get_Match_Lineups` si existe. Si no hay nada → [N/A].                                            |
| "Construí un modelo heurístico para reemplazar la predicción basada en modelos de aprendizaje" | **Prohibido.** Capa 7 = odds-driven. No inventar probabilidades.                                                                                           |
| "Usé xG inventado como input"                                                                  | **Prohibido.** Si FlashScore no trae xG en `Get_Match_Stats` → no inventarlo. Usar los datos que la API provee.                                            |
| "El partido ya empezó pero igual quiero hacer el análisis"                                     | **No aplica.** Esta skill es solo para partidos `notstarted`. Para partidos `inprogress` o `finished`, no proceder.                                                   |
| "No había injuries data así que inventé lesionados"                                            | **Prohibido.** Si `missingPlayers` no está disponible → no inventar ausencia ni motivo.                                                                    |
| "Calculé cuánto baja el equipo por cada ausente"                                               | **Prohibido.** No estimar impacto numérico de ausencias. Usar solo lo que la API provee + niveles de ausencia definidos.                                   |
| "Usé missingPlayers como señal fuerte por sí sola"                                             | **Prohibido.** Ausencias sin corroboración en otras capas = señal débil. Nunca señal fuerte.                                                               |
| "El H2H no venía así que puse lo que sabía de memoria"                                         | **Prohibido.** Si Get_Match_H2H = null → "H2H no disponible [N/A]."                                                                                        |
| "Le puse 'Alta' aunque solo tenía el evento"                                                   | **Prohibido.** Evento solo = confianza Baja. Tabla de umbrales es obligatoria.                                                                             |
| "El over entra seguro"                                                                         | **Prohibido.** Lenguaje probabilístico siempre.                                                                                                            |
| "Rellené la capa 3 con nombres de memoria"                                                     | **Prohibido.** Cada capa tiene output definido. Si no hay datos → [N/A].                                                                                   |
| "La muestra de 2 partidos es representativa"                                                   | **Prohibido.** N<5 = "muestra limitada." Indicadores pesan menos.                                                                                          |
| "Calculé un impact score con pesos 0.3/0.5"                                                    | **Prohibido.** Capa 3 usa datos directos y rankings, no fórmulas heurísticas.                                                                              |
| "Llamé a Get_Match_Details/H2H/Stats directamente desde el modelo"                             | **Prohibido.** Toda la recolección de datos del partido pasa por `build_match_context.py`. Solo `Get_Team_Fixtures/Get_Team_Results` para match discovery. |
| "El script emitió un warning pero el dato me parecía correcto"                                 | **Prohibido.** Los warnings del script son instrucciones. Si el script marca un dato como sospechoso → respetarlo y no contradecirlo.                      |
| "El JSON tenía [N/A] pero yo sabía el dato de memoria"                                         | **Prohibido.** El JSON ya normalizó y marcó los datos disponibles. No re-inventar datos marcados como [N/A].                                               |
| "Ejecuté endpoints MCP adicionales después de recibir el JSON"                                 | **Prohibido.** Una vez recibido `final_context`, todos los datos del análisis vienen del JSON. No consultar endpoints adicionales.                         |
