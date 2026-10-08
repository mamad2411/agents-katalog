# MIA IA TRADING SYSTEM - Instructions Projet
# ============================================
# Ce fichier définit le contexte et les règles pour Claude/Cursor AI

## 🎯 DESCRIPTION DU PROJET

MIA_IA_system est un bot de trading algorithmique professionnel pour les futures US (ES, NQ, RTY).
Il utilise un système ML 3-Layer basé sur MenthorQ (données options/gamma) pour générer des signaux de trading.

**Technologies:**
- Python 3.11+
- Sierra Chart (broker via DTC Protocol)
- Discord (notifications temps réel)
- LightGBM (ML models)

**Marchés tradés:**
- ES (E-mini S&P 500)
- NQ (E-mini Nasdaq 100)
- RTY (E-mini Russell 2000)

---

## 📁 STRUCTURE DU PROJET

```
MIA_IA_system/
├── LAUNCH/
│   ├── launch_production_CLEAN_v2.py   # ⭐ BOT PRINCIPAL (lancé par watchdog)
│   └── mia_watchdog.py                 # ⭐ WATCHDOG ANTI-CRASH
│
├── COMMANDE_MIA/                       # Scripts d'installation
│   ├── INSTALL_WATCHDOG_WINDOWS.bat    # Installe tâche planifiée
│   └── CONFIGURE_AUTO_REBOOT_BSOD.bat  # Config anti-BSOD
│
├── core/                               # Modules core (33 fichiers)
│   ├── session_quality_monitor.py      # Filtre sessions London/US
│   ├── safety_kill_switch.py           # Arrêt d'urgence
│   ├── trailing_stop_manager.py        # Trailing stops
│   └── ...
│
├── ml/                                 # Machine Learning
│   ├── ml_3layer_filter.py             # ⭐ CŒUR DU SYSTÈME ML
│   └── ml_3layer_integrated_system.py
│
├── strategies/                         # Stratégies
│   ├── menthorq_3layer_strategy.py     # ⭐ STRATÉGIE PRINCIPALE
│   └── strategy_manager_optimized_v3.py
│
├── execution/                          # Exécution ordres
│   ├── sierra_dtc_connector.py         # Connexion broker
│   ├── trade_snapshotter_ml_ready.py   # Capture trades pour ML
│   └── risk_manager.py
│
├── monitoring/                         # Notifications
│   ├── discord_notifier.py             # Discord webhooks
│   └── discord_styles.py
│
├── features/                           # Features ML
│   ├── ml_ready_reader.py              # Lecture snapshots
│   └── dom_health_analyzer.py
│
├── config/                             # Configuration
│   └── unified_thresholds.py           # ⭐ SEUILS ML (NE PAS MODIFIER)
│
├── utils/                              # Utilitaires
│   ├── advanced_logging.py             # Logs avancés
│   ├── economic_calendar.py            # Protection annonces
│   └── data_quality_checker.py         # ⭐ PROTECTION DONNÉES PÉRIMÉES
│
├── extracteur/                         # Dumper C++ Sierra Chart
│   └── MIA_Dumper_G3_Unifier.cpp
│
├── snapshots/                          # Données ML (1.17M fichiers)
├── snapshots_trades/                   # Captures trades (226K fichiers)
├── logs_advanced/                      # Logs thématiques
├── DATA_SIERRA_CHART/                  # Données marché
├── docs/                               # Documentation
└── ARCHIVE/                            # Anciens fichiers (backup)
```

---

## 🧠 ARCHITECTURE ML 3-LAYER

Le système utilise 3 couches de validation pour chaque signal:

### LAYER 1: MenthorQ (50% du score)
- Gamma Walls (10%)
- GEX Levels (10%)
- Blind Spots (8%)
- Next Wall (8%)
- Distances (8%)
- Confluence (6%)

### LAYER 2: OrderFlow (30% du score)
- Delta instantané (12%)
- Volume bid/ask (6%)
- DOM Imbalance (6%)
- Institutional Pressure (4%)
- Battle Navale (2%)

### LAYER 3: Context (20% du score)
- VWAP Position (6%)
- Value Area (5%)
- Market Structure (5%)
- Volatility (4%)

**Seuil minimum pour trader:** 35% confidence (ES/NQ), 40% (RTY)

---

## ⚠️ FICHIERS CRITIQUES - NE PAS MODIFIER SANS RAISON

1. **config/unified_thresholds.py** - Tous les seuils ML calibrés
2. **ml/ml_3layer_filter.py** - Logique de filtrage ML
3. **LAUNCH/launch_production_CLEAN_v2.py** - Lanceur principal

---

## 🕐 SESSIONS DE TRADING (Heure Paris)

- **London:** 08:00 - 11:00
- **US Morning:** 15:50 - 17:00
- **US Power Hour:** 20:00 - 21:30
- **Hard Stop:** 21:30 (pas de trades après)
- **Lunch Block:** 17:00 - 19:30 (pas de trades)

---

## 🛡️ PROTECTIONS ACTIVES

1. **VIX Regime Filtering:**
   - VIX < 15: Trading normal
   - VIX 15-20: Normal
   - VIX 20-25: Prudence
   - VIX 25-35: Skip trades
   - VIX ≥ 35: STOP TOTAL

2. **Economic Calendar:**
   - Bloque trading 15min avant / 30min après annonces ⭐⭐⭐ (3 étoiles)
   - Source: Investing.com via investpy

3. **Data Quality Checker:** ⭐ NOUVEAU
   - Bloque trading si données > 5 secondes
   - Vérifie champs critiques présents
   - Détecte spreads anormaux
   - Score qualité 0-100
   - Protection contre données périmées/corrompues

4. **Risk Management:**
   - Max 1 position par symbole
   - Daily loss limit
   - Drawdown monitor
   - Safety kill switch

---

## 📊 DONNÉES ET LOGS

### Snapshots ML (dumper C++)
- Chemin: `snapshots/[YYYYMMDD]/[SYMBOL]_[TIMESTAMP].json`
- Contient: mid, delta, DOM, VWAP, GEX, gamma levels, etc.

### Logs Avancés (AdvancedLogManager)
- Chemin: `logs_advanced/`
- Sous-dossiers:
  - `trades/` - Tous les trades exécutés (JSON + texte)
  - `signals/` - Tous les signaux générés (acceptés + rejetés)
  - `discord/` - Historique des messages Discord
  - `dtc/` - Logs connexion broker DTC
  - `performance/` - Métriques de performance
  - `summaries/` - Résumés journaliers

**Utilisation dans le code:**
```python
from utils.advanced_logging import AdvancedLogManager
self.advanced_log = AdvancedLogManager()

# Logger un trade
self.advanced_log.log_trade(symbol, "OPEN", {"entry": 5000, "direction": "LONG"})

# Logger un signal
self.advanced_log.log_signal(symbol, "LONG", accepted=True, reason="ML score 45%")

# Générer résumé journalier
self.advanced_log.generate_daily_summary()
```

### Captures Trades ML (TradeSnapshotterMLReady)
- Chemin: `snapshots_trades/`
- Sous-dossiers:
  - `daily/` - Snapshots par jour
  - `ml_ready/` - Données prêtes pour entraînement
  - `rejected_signals/` - Signaux rejetés (pour analyse)
  - `archive/` - Anciennes captures

**Utilisation dans le code:**
```python
from execution.trade_snapshotter_ml_ready import TradeSnapshotterMLReady
self.trade_snapshotter = TradeSnapshotterMLReady()

# Capturer un trade exécuté
self.trade_snapshotter.capture_trade_snapshot(symbol, signal, ml_data, entry_price)

# Capturer un signal rejeté (IMPORTANT pour ML)
self.trade_snapshotter.capture_rejected_signal_snapshot(
    symbol=symbol,
    signal=signal.to_dict(),
    ml_data=snapshot,
    rejection_reason="VIX trop haut",
    rejection_category="VIX_FILTER"
)
```

---

## 🛡️ SYSTÈME ANTI-CRASH & LANCEMENT BOT (14 Déc 2025)

### ⚠️ RÈGLE CRITIQUE - COMMENT LANCER LE BOT

**NE JAMAIS lancer directement le bot principal !**

```powershell
# ❌ NE PAS FAIRE:
python LAUNCH/launch_production_CLEAN_v2.py

# ✅ TOUJOURS UTILISER LE WATCHDOG:
schtasks /run /tn "MIA_Watchdog"
# OU
python LAUNCH/mia_watchdog.py
```

### Architecture Anti-Crash

```
┌─────────────────────────────────────────┐
│         DÉMARRAGE WINDOWS               │
│                 ↓                        │
│     Tâche planifiée "MIA_Watchdog"      │
│     (délai 1 min après boot)            │
│                 ↓                        │
│         🐕 WATCHDOG                      │
│         LAUNCH/mia_watchdog.py          │
│                 ↓                        │
│         🤖 BOT MIA                       │
│         launch_production_CLEAN_v2.py   │
│                 ↓                        │
│     Si crash → Watchdog relance auto    │
│     + Alerte Discord                    │
└─────────────────────────────────────────┘
```

### Fichiers du Système Anti-Crash

| Fichier | Rôle |
|---------|------|
| `LAUNCH/mia_watchdog.py` | ⭐ Surveille et relance le bot si crash |
| `LAUNCH/launch_production_CLEAN_v2.py` | Bot principal (lancé par watchdog) |
| `COMMANDE_MIA/INSTALL_WATCHDOG_WINDOWS.bat` | Installe la tâche planifiée |
| `COMMANDE_MIA/CONFIGURE_AUTO_REBOOT_BSOD.bat` | Config Windows anti-BSOD |

### Commandes de Gestion

```powershell
# Démarrer le bot (via watchdog)
schtasks /run /tn "MIA_Watchdog"

# Vérifier si watchdog/bot tournent
Get-Process python

# Voir status tâche planifiée
schtasks /query /tn "MIA_Watchdog"

# Arrêter tout (watchdog + bot)
Get-Process python | Stop-Process -Force

# Voir logs watchdog
Get-Content D:\MIA_IA_system\logs\watchdog.log -Tail 20

# Voir logs bot du jour
Get-Content D:\MIA_IA_system\logs\__main___$(Get-Date -Format 'yyyyMMdd').log -Tail 50
```

### Comportement Automatique

1. **Au démarrage Windows:** La tâche planifiée lance le watchdog après 1 minute
2. **Crash du bot:** Le watchdog détecte et relance automatiquement + alerte Discord
3. **BSOD/Crash Windows:** Windows redémarre auto → watchdog relance le bot
4. **Arrêt manuel:** Utiliser `Get-Process python | Stop-Process -Force`

### ⚠️ NE JAMAIS MODIFIER

- `LAUNCH/mia_watchdog.py` - Watchdog validé et testé
- La tâche planifiée "MIA_Watchdog" dans Windows

---

## 🚀 COMMANDES UTILES (LEGACY - Voir section Anti-Crash ci-dessus)

```powershell
# ⚠️ PRÉFÉRER: schtasks /run /tn "MIA_Watchdog"

# Vérifier processus
Get-Process python

# Arrêter le bot
Get-Process python | Stop-Process -Force

# Voir derniers logs
Get-Content logs\*.log -Tail 50
```

---

## 📋 CONVENTIONS DE CODE

1. **Logging standard:** `from core.logger import get_logger`
2. **Logging avancé:** `from utils.advanced_logging import AdvancedLogManager`
3. **Types:** Utiliser dataclasses pour TradingSignal, Position
4. **Async:** Le lanceur principal est async (asyncio)
5. **Timezone:** Europe/Paris pour sessions, UTC pour timestamps

### Exemple de logging complet:
```python
# Logger standard (console + fichier)
logger = get_logger(__name__)
logger.info("Message info")
logger.warning("Message warning")

# Logger avancé (JSON structuré + fichiers thématiques)
self.advanced_log.log_trade(symbol, action, details_dict)
self.advanced_log.log_signal(symbol, direction, accepted, reason)
```

---

## 🔧 QUAND MODIFIER LE CODE

### ✅ OK de modifier:
- Ajouter des logs pour debug
- Corriger des bugs évidents
- Améliorer les messages Discord
- Ajouter des protections

### ❌ NE PAS modifier sans discussion:
- Les seuils dans unified_thresholds.py
- La logique ML 3-Layer
- Les poids des layers
- La structure des snapshots

---

## 📝 NOTES IMPORTANTES

1. Le backup complet a été fait le 29/11/2025
2. Tous les anciens fichiers sont dans ARCHIVE/
3. Le projet a été nettoyé: 0 fichiers à la racine
4. Les modules Python ont des dépendances croisées via __init__.py
5. Ne pas supprimer de fichiers .py dans les dossiers modules

---

## 🎯 OBJECTIFS DU BOT

- Win Rate cible: > 50%
- Ratio R/R: 1:1.5 minimum
- Max trades/jour: ~10-15
- Sessions actives: ~5h40/jour
- Protection capitale: PRIORITÉ #1

---

## ⚡ OPTIMISATIONS PERFORMANCE (30 Nov 2025)

### Gains de Latence Totaux: -35ms
Le système a été optimisé pour réduire la latence de la boucle principale de 124ms à 89ms.

**1. Snapshots Parallèles (-20ms)**
- AVANT: Lecture séquentielle = 30ms (10ms × 3 symbols)
- APRÈS: Lecture parallèle avec `asyncio.gather()` = 10ms
- GAIN: -20ms par cycle
- Implémentation: `_read_all_snapshots_parallel()` dans `launch_production_CLEAN_v2.py`

**2. Cache Données Statiques (-10ms)**
- AVANT: Accès répétés à `config.tick_size.get(symbol)` = 10ms cumulés
- APRÈS: Cache LRU avec `@lru_cache(maxsize=10)` = ~0ms
- GAIN: -10ms par cycle
- Méthodes cachées: `_get_tick_size`, `_get_tick_value`, `_get_point_value`, `_get_sl_ticks`, `_get_tp_ticks`

**3. Variables Locales (-5ms)**
- AVANT: Accès répétés `self.config.xxx` dans boucles = 5ms
- APRÈS: Variables locales au début de chaque boucle = ~0ms
- GAIN: -5ms par cycle
- Variables: `symbols`, `daily_pnl`, `daily_loss_limit`, `snapshot_max_age_ms`, etc.

### Tests Unitaires & Intégration
- ✅ **39 tests pytest** créés et validés (30 Nov 2025)
- `tests/unit/test_risk_manager.py` - 205 lignes
- `tests/unit/test_session_quality.py` - 172 lignes
- `tests/unit/test_ml_filter.py` - 184 lignes
- `tests/integration/test_pipeline.py` - 163 lignes
- Couverture: RiskManager, SessionQualityMonitor, ML3LayerFilter, Pipeline complète

### Validation Production (30 Nov 2025)
- ✅ DTC Protocol connecté (ES + NQ)
- ✅ Mode LIVE actif
- ✅ 27 modules chargés avec succès
- ✅ VIX Regime Filtering actif
- ✅ Session Quality Monitor opérationnel
- ✅ Optimisations latence appliquées et validées
- ✅ Pipeline complète testée et fonctionnelle

### Ordre des Types Utilisés
- **Market Orders** pour entries (exécution immédiate)
- Bracket Orders (Entry + TP + SL) via DTC
- Justification: Stratégie momentum nécessite fills rapides
- Win Rate élevé (>80%) compense le slippage (~0.5 tick)

### Data Quality Validation
- `EnhancedDataValidator.validate()` implémenté (30 Nov 2025)
- Vérifie: champs requis, cohérence prix, spread anormal, VIX valide, session_id
- Bloque trading si données > 5 secondes (protection péremption)
- Score qualité 0-100 pour chaque snapshot

---

## 🔴 HISTORIQUE: PROBLÈME OVER-ENGINEERING (RÉSOLU)

### Le Problème
Le système original avait **23 validateurs en cascade** qui bloquaient presque tous les trades:
- En backtest: ~15 trades/jour
- En live: ~2-3 trades/jour seulement!

### La Solution (CLEAN V2)
Réduction à **8 validateurs essentiels**:
1. ML 3-Layer Score (≥35%)
2. VIX Regime (<35)
3. Session Hours
4. Economic Calendar (⭐⭐⭐ only)
5. Risk Manager
6. Drawdown Monitor
7. Max Positions
8. Safety Kill Switch

### Leçon Apprise
> "Un système simple qui trade est meilleur qu'un système parfait qui ne trade pas."

**NE PAS AJOUTER de nouveaux validateurs** sans preuve backtest qu'ils améliorent les résultats.
Le ML 3-Layer intègre DÉJÀ toute la logique (MenthorQ + OrderFlow + Context).

Voir `docs/BACKTESTS_HISTORIQUE.md` pour les détails complets.

---

## 🚨 BRACKET ORDERS & OCO - SOLUTION VALIDÉE (1er Déc 2025)

### ⚠️ RÈGLES CRITIQUES - NE PAS OUBLIER!

**Ce problème a été résolu plusieurs fois. Ne pas cramer de tokens à le refaire!**

### ❌ CE QUI NE FONCTIONNE PAS (Sierra Chart DTC Simulation):

```python
# NE JAMAIS UTILISER:
"ParentTriggerClientOrderID": parent_cid  # ← CASSE TOUT!
"IsParentOrder": 1                         # ← Ignoré
"AttachedOrderType": ...                   # ← Non supporté
```

### ✅ CE QUI FONCTIONNE:

1. **3 ordres SÉPARÉS** (entry + TP + SL)
2. **OCOGroup1** identique pour TP et SL (seul lien!)
3. **OCO géré MANUELLEMENT** côté bot (Sierra ne le fait pas auto)
4. **Prix ABSOLUS** calculés depuis le fill réel

### 🔥 Calcul des Offsets selon la Direction:

```python
if parent_side == "BUY":  # LONG
    tp_price = fill_price + (tp_offset * tick_size)  # TP AU-DESSUS
    sl_price = fill_price - (sl_offset * tick_size)  # SL EN-DESSOUS
else:  # SHORT (SELL)
    tp_price = fill_price - (tp_offset * tick_size)  # TP EN-DESSOUS
    sl_price = fill_price + (sl_offset * tick_size)  # SL AU-DESSUS
```

### 📁 Documentation Complète:
- `docs/SOLUTION_BRACKET_OCO_FINAL.md` - Solution détaillée
- `ARCHIVE/old_folders/EXECUTION BAKUP/` - Code backup fonctionnel

### 🧪 Test Validé:
```
Entry SHORT @ 6842.75
TP @ 6837.75 (20t en-dessous) ✅
SL @ 6847.75 (20t au-dessus) ✅
TP FILLED → SL automatiquement annulé ✅
```
