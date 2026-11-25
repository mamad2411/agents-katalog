---
name: cli-forge-perf
metadata:
  author: clement
description: >-
  Catalogue + méthode pour optimiser la performance de n'importe quoi : code,
  requêtes, algorithmes, pages web, systèmes. Couvre complexité algorithmique,
  structures de données, requêtes DB (index, N+1), cache et RAM-vs-disque,
  astuces math/physique (distance² vs sqrt, éviter cos/sin, SIMD),
  async/concurrence, frontend/web (Lighthouse), bas niveau et hardware. Utilise
  ce skill DÈS QUE l'utilisateur veut accélérer quelque chose, réduire latence
  ou mémoire, "rendre plus rapide", "ça rame", "ça consomme trop", optimiser une
  boucle/requête/page — même sans dire "performance". Couvre aussi comment
  mesurer et benchmarker rigoureusement (harnais A/B, distribution vs moyenne,
  pièges de mesure), générer des idées hors catalogue et expérimenter : déclenche
  pour "benchmark ça", "ce gain est-il réel ?", "pourquoi X est plus lent que Y",
  "perf budget", "p95/p99", "hot path", "profiling", "flamegraph".
argument-hint: "[scope-or-symptom]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** Ce skill utilise du chargement à la demande. Les contenus lourds vivent dans `references/` et sont lus à la demande.

> **Language rule:** Les instructions du skill sont en français (le catalogue lui-même). Pour les artefacts générés (rapports, benches, scripts), détecte la langue du projet (README, commentaires, docs, commits) et produis dans cette langue. Si le projet est bilingue, demande à l'utilisateur.

> **Gotchas:** Lis `../gotchas.md` AVANT de produire un livrable.

# Perf Optimization

Catalogue ordonné des techniques d'optimisation, du plus rentable au moins
rentable. L'objectif : donner le bon réflexe au bon niveau, et **empêcher de
micro-optimiser avant d'avoir réglé l'algo et l'I/O**.

## Règle d'or : MESURE avant d'optimiser

> "Premature optimization is the root of all evil." — Knuth

On n'optimise jamais à l'intuition. 90 % du temps est passé dans 10 % du code
(le *hot path*). Optimiser le reste = effort gaspillé + complexité ajoutée pour
rien. Méthode en boucle :

1. **Mesure** — profile/trace pour trouver le vrai bottleneck (pas celui qu'on
   imagine). Établis une baseline chiffrée. Ne suppose jamais quel langage/lib
   est plus rapide : instrumente. *Méthodo détaillée : `references/profiling.md`.*
2. **Localise & classe** — identifie LE point chaud ET sa nature : CPU-bound,
   memory-bound, bandwidth-bound, I/O-bound, lock-bound ou syscall-bound ? Cette
   classification (roofline) dicte quel niveau de la hiérarchie attaquer. Loi
   d'Amdahl : accélérer ×10 un bloc qui pèse 5 % du temps total ne gagne que
   ~4,5 %. Inutile.
3. **Optimise** — applique la technique du bon niveau (voir hiérarchie ci-dessous).
4. **Re-mesure** — confirme le gain réel. Si nul ou négatif, **reviens en arrière**.
   Garde le code lisible si le gain n'est pas significatif.

> **Reproductibilité** — un bench n'a de valeur que s'il est rejouable à l'identique : seed, horloge, environnement, ordre, locale. Le toolkit canonique est partagé : `../shared/determinism.md`. Sans ces pins, deux exécutions consécutives produisent des chiffres différents et l'A/B devient impossible à départager.

### Le GATE — definition-of-done (ne pas sauter)

Trois portes obligatoires. Tant qu'une case n'est pas cochée, on ne passe pas. La structure 3-phases (pré → pendant → post) est canonique dans `../shared/done-gate.md` — ce GATE en est la spécialisation perf (distribution + permutation + anti-DCE en post). Les autres forge-* skills (resilience, pipeline, oci-rootless, demo, chef) instancient le même squelette pour leur domaine.

**Avant de toucher au code :**
- [ ] baseline chiffrée et **reproductible** (même entrée, même environnement).
- [ ] bottleneck **localisé ET classé** (CPU/mem/bande passante/I/O/lock/syscall) —
      sinon `references/profiling.md`.
- [ ] **borne max du gain** estimée (Amdahl/roofline). Si le plafond est faible
      → **stop**, change de cible.

**Pendant :**
- [ ] **une seule variable à la fois** (sinon tu ne sauras pas qui a causé quoi).

**Avant de CLAIMER un gain :**
- [ ] **distribution** rapportée (médiane + p95/p99), jamais une moyenne seule.
- [ ] Δ **supérieur au bruit** de mesure (test de permutation, cf. le harnais)
      — sinon il n'y a **pas** de gain.
- [ ] **aucun piège de mesure** : le compilo n'a pas supprimé le bench, warmup
      fait, runs A/B interleavés. Détail : `references/benchmarking-traps.md`.
- [ ] gain réel **non significatif** → revert et garde la lisibilité.

> **Position sur le gate-ladder partagé** (`../shared/gate-ladder.md`) — le GATE de perf est un **T1-T4 spécialisé** : le bench in-process est T1 (composant), la baseline reproductible est T2 (environnement maîtrisé), l'A/B sous charge est T4 (stress). Une régression de perf observée en prod sans test T4 = "false green" — exactement le défaut que le ladder existe pour rattraper.

### Harnais natif (langue-agnostique)

Le **protocole** (warmup, N échantillons, distribution + p95/p99 + σ, A/B interleavé, test de permutation, anti-DCE) s'implémente dans n'importe quel langage. **L'actif réutilisable n'est pas un script** — c'est la méthode de mesure et la règle de verdict. `references/bench-protocol.md` formalise ce protocole et **route vers l'outil natif mûr** selon le langage :

| Cas | Outil natif recommandé | Significativité statistique |
|---|---|---|
| Rust, micro in-process | **Criterion** (`criterion-rs`) ou `divan` | baseline intégré + détection de régression |
| Go | `testing.B` + **benchstat** | test U de Mann-Whitney |
| C/C++ | **Google Benchmark** ou `clock_gettime` manuel | scripts maison |
| JVM (Java/Kotlin/Scala) | **JMH** | intervalles de confiance |
| JS/TS | **mitata** ou tinybench | intégré |
| CLI / boîte noire | **hyperfine** | ratio + σ, A/B intégré |
| Python | **pytest-benchmark** ou `timeit` | intégré |

**Préfère TOUJOURS** un framework natif mûr à une boucle maison : ils gèrent warmup, outliers et stats bien mieux qu'un harnais ad-hoc. Pour le sub-ms et l'in-process, c'est obligatoire — l'overhead d'un sous-process domine la mesure.

Squelettes prêts à copier (Rust/Criterion, Rust std seul pour l'air-gap, Go/benchstat, C, hyperfine) + règle de routage détaillée : `references/bench-protocol.md` §Squelettes.

Modes opératoires courants (à implémenter dans le langage cible — patterns, pas scripts) :
- **A/B avec significativité** : interleaver A,B,A,B…, comparer médianes, test de permutation (ou Mann-Whitney). Δ dans le bruit ⇒ pas de gain prouvé.
- **Ablation / autotune** : bencher N variantes, classer par médiane, tester chacune vs la meilleure. « ≈ dans le bruit » des suivantes = égalité, pas victoire.
- **Sweep paramétrique** : balayer (threads, batch size, cache size…), sortir la courbe + l'optimum. L'optimum est rarement à un extrême — élargir si c'en est un.
- **Chiffrage €/kWh/CO₂ d'une optim** : modèle + garde-fous (latence ≠ énergie, carbone embarqué, effet rebond) dans `references/cost-accounting.md`.

Traces complètes (symptôme → fix → chiffres) : `references/worked-examples.md`.

**Pourquoi pas de script générique fourni ?** Le langage d'un runner est accessoire (il dort en attendant le sous-process), mais aucun langage n'est portable partout : Python n'existe pas dans un conteneur FROM scratch ni en embarqué ; un binaire Rust ne tourne pas sur la JVM. La portabilité réelle vient du **protocole** et de son implémentation **native** dans la cible — pas d'un script à packager.

### Mode recherche : quand la réponse n'est pas dans le catalogue

Le catalogue ci-dessous couvre le connu. Pour le reste — un goulot inédit, un
résultat contre-intuitif, un domaine non couvert — on bascule en mode recherche :
**générer** des idées (divergent), puis les **valider** par l'expérience
(convergent). Ne mélange pas les deux phases.

- **Générer des idées** d'optimisation qu'on ne connaît pas encore (premiers
  principes, inversion, analogie/biomimétisme, suppression, relâchement de
  contrainte, "et si 10× ?"). *Réf : `references/idea-generation.md`*
- **Valider par l'expérience** : hypothèse falsifiable, table de mixage
  (ablation, une variable à la fois), contrôle de l'aléa, mesure
  multidimensionnelle, pièges statistiques (mêmes stats ≠ mêmes données).
  *Réf : `references/experiment-method.md`* — et les pièges de **mesure**
  (coordinated omission, DCE, warmup, A/B confondu) : `references/benchmarking-traps.md`.
- **Dissoudre les contraintes** quand on est coincé : réécrire à n'importe quel
  niveau (Rust/C/asm/hexa/FPGA/DSL), détourner d'autres domaines ou équipements
  (le WiFi détecte une présence…), inversion radicale du problème lui-même.
  *Réf : `references/lateral-thinking.md`*

### Outils de mesure par domaine
| Domaine | Outils |
|---|---|
| CPU / code | `perf`, flamegraph, `cargo flamegraph`, `py-spy`, Chrome DevTools Profiler, `hyperfine` (bench CLI) |
| Mémoire | `valgrind --tool=massif`, `heaptrack`, `dhat` (Rust), allocation profiler |
| DB | `EXPLAIN ANALYZE`, slow query log, `pg_stat_statements` |
| Web | Lighthouse, WebPageTest, DevTools Performance/Network, Core Web Vitals |
| Réseau / I/O | `iostat`, `iotop`, `strace -c`, latency tracing |
| Systèmes distribués | tracing **OpenTelemetry** (spans, p95/p99), Jaeger/Tempo, exemplars |
| Bas niveau / kernel | **eBPF** (`bpftrace`, `bcc`), `perf stat` (IPC, cache miss), `strace -c` (syscalls) |
| Hardware / limites | roofline model, `likwid`, compteurs PMU, `numactl --hardware` |

## Hiérarchie des gains (ordre de priorité STRICT)

Attaque toujours dans cet ordre. Les gains du haut se comptent en **ordres de
grandeur** ; ceux du bas en **pourcents**. Le **niveau 0 (diagnostic)** décide
*où* dans cette liste se trouve réellement ton bottleneck.

0. **Diagnostic du bottleneck** → profiling + tracing + roofline. Détermine la
   nature du goulot (CPU/mémoire/bande passante/I/O/lock/syscall) AVANT de
   choisir une optim. *Réf : `references/profiling.md`*
1. **Algorithme & complexité** → O(n²) → O(n log n) → O(n) → O(1). Le levier
   le plus puissant de tous. *Réf : `references/algorithmic.md`*
2. **Accès aux données (I/O, DB, réseau)** → ne pas faire l'aller-retour est
   toujours plus rapide que le faire vite. *Réf : `references/database.md`*
3. **Mémoire & cache** → RAM > disque, cache locality, mémoïsation, éviter de
   recalculer. *Réf : `references/memory-cache.md`*
4. **Async & parallélisme** → recouvrir l'attente I/O, paralléliser le CPU,
   ne pas bloquer. *Réf : `references/async-concurrency.md`*
5. **Micro-optimisations CPU (math/physique, branchless, SIMD)** → en DERNIER,
   uniquement sur le hot path confirmé. *Réf : `references/math-physics.md`*
6. **Frontend / web** → axe transverse, piloté par Lighthouse / Core Web
   Vitals. *Réf : `references/frontend-web.md`*

**Au-delà de la hiérarchie** (axes transverses & domaines — voir l'index pour router) :

- **Systèmes & limites physiques** → hardware : roofline, trade-offs
  proc/RAM/disque (recompute vs transfert, compression), syscalls, instructions
  hardware (AES-NI, SIMD, GPU), NUMA, footprint, conso. *`references/systems-hardware.md`*
- **Dépendances & footprint** → empilement de libs : justifier chaque dep,
  mutualiser les redondantes, libs « à leur maximum », aplatir les couches.
  *`references/dependencies.md`*
- **Inférence LLM (tok/s)** → quantization, KV cache, continuous batching,
  speculative decoding ; le decode est *memory-bandwidth-bound*. *`references/llm-inference.md`*
- **Crypto (ops/s)** → choix d'algo (Ed25519, ChaCha20, BLAKE3), accélération
  hardware, batch verification — **sans casser le constant-time**. *`references/crypto-throughput.md`*
- **Biomimétisme (à cadrer)** → utile pour l'optim combinatoire dure et la
  coordination décentralisée ; folklore pour le reste. *`references/bio-inspired.md`*

## Latency numbers — le modèle mental qui explique tout

Pourquoi "RAM plutôt que disque" et "ne fais pas de requête dans une boucle" :
les ordres de grandeur. Mémorise-les, ils dictent 80 % des décisions.

| Opération | Latence approx. | Échelle humaine (×1 mds) |
|---|---|---|
| Accès registre / L1 cache | ~1 ns | 1 s |
| L2 cache | ~4 ns | 4 s |
| RAM (accès principal) | ~100 ns | 1,5 min |
| SSD NVMe (lecture) | ~16 µs | 4,5 h |
| SSD lecture 1 MB | ~50 µs | — |
| Réseau même datacenter (RTT) | ~0,5 ms | 6 jours |
| Disque HDD seek | ~5 ms | 2 mois |
| Réseau intercontinental (RTT) | ~150 ms | 5 ans |

**Conséquences directes :** un appel réseau coûte ~10 000× un accès RAM. Donc :
batch les requêtes, cache en mémoire, et **ne mets jamais une I/O dans une
boucle serrée**. C'est la base de la priorité #2 et #3.

## Index rapide : "j'ai ce problème" → "va lire ça"

| Symptôme / situation | Fichier de référence |
|---|---|
| Boucle lente, trop de `if`, recherche linéaire, mauvaise complexité | `references/algorithmic.md` |
| Requête SQL lente, full table scan, N+1, ORM qui rame | `references/database.md` |
| Trop de mémoire, recalcul permanent, lecture disque répétée, cache | `references/memory-cache.md` |
| Calcul lourd (distance, trigo, math, géo, graphismes, simulation) | `references/math-physics.md` |
| Bloque sur de l'I/O, threads, UI qui freeze, débit faible | `references/async-concurrency.md` |
| Page web lente, mauvais score Lighthouse, LCP/CLS/INP | `references/frontend-web.md` |
| Je ne sais pas où est le goulot, "X est plus lent que Y", besoin de tracing/profiling | `references/profiling.md` |
| « C'est combien environ ? » ordre de grandeur d'un coût (RAM vs disque, RTT, syscall) | Table « Latency numbers » plus haut dans ce SKILL.md |
| Limites hardware, calcul intensif, crypto/compression lente, embarqué, conso, saturer CPU/RAM/IO, trade-off proc/RAM/bus, syscalls | `references/systems-hardware.md` |
| Trop de dépendances, libs redondantes/empilées, binaire trop gros, build/lib mal configurés | `references/dependencies.md` |
| Inférence LLM lente, augmenter les tok/s, débit GPU, quantization, KV cache, serving | `references/llm-inference.md` |
| Débit crypto faible, chiffrement/signature/hash lents, ops/s, choix d'algo crypto | `references/crypto-throughput.md` |
| Optimisation combinatoire dure, coordination d'agents/distribuée, métaheuristiques, biomimétisme | `references/bio-inspired.md` |
| Je sèche / pas d'idée, besoin de générer des pistes, penser hors catalogue, premiers principes, simplifier | `references/idea-generation.md` |
| Tester une optim, expérimenter, mesurer proprement, isoler une variable, hypothèse, chiffres trompeurs | `references/experiment-method.md` |
| Benchmark suspect, chiffre trop beau, le compilo a mangé mon bench, p99 ment, A/B douteux, warmup | `references/benchmarking-traps.md` |
| Coincé / réécrire à un autre niveau (C/asm/hexa/FPGA/DSL), détourner un autre domaine ou équipement, inverser le problème | `references/lateral-thinking.md` |
| Exemple concret de bout en bout, trace symptôme→fix→chiffres, "montre-moi" | `references/worked-examples.md` |
| Pourquoi tel langage de bench, mesurer en Rust/Go/C, in-process, cible sans python, générer un harnais natif, protocole portable | `references/bench-protocol.md` |
| Chiffrer un gain en €/watts/CO₂/coût-utilisateur, justifier ou prioriser une optim, sobriété | `references/cost-accounting.md` |
| Contexte récurrent (Rust, air-gapped, souverain, footprint conteneur, inférence locale M5, crypto) | `references/_project-profiles.md` |

## Anti-patterns universels (vrais quel que soit le langage)

- **Optimiser sans profiler** → tu optimises le mauvais endroit.
- **I/O dans une boucle** (requête DB, appel HTTP, lecture fichier par item) →
  batch ou pré-charge. *Le plus fréquent et le plus coûteux.*
- **Recalculer la même chose** dans une boucle (invariant de boucle, `len()`
  recalculé, propriété recalculée) → sors-le de la boucle, mémoïse.
- **Recherche linéaire** dans une grande collection alors qu'un Set/Map/index
  donne du O(1) ou O(log n).
- **Tout charger en mémoire** quand un stream / une pagination suffit (et
  l'inverse : relire le disque à chaque fois au lieu de cacher).
- **Sérialiser ce qui peut être parallèle**, ou paralléliser ce qui est borné
  par autre chose (réseau saturé, contention de lock).
- **Allouer dans le hot path** (alloc/free répétés, copies, conversions de
  type) → réutilise des buffers, pré-alloue.
- **Abstractions à coût caché** : ORM lazy qui déclenche du N+1, `.map().filter()
  .reduce()` qui crée 3 collections intermédiaires sur des données massives.

## Règle finale

La lisibilité est une feature. N'échange jamais de la clarté contre un gain de
perf non mesuré et non significatif. Le code le plus rapide est souvent celui
qui fait **moins de travail**, pas celui qui fait le même travail "plus vite".

## Sortie machine-lisible (cli-cycle)

Quand ce skill tourne sous `cli-cycle`, émet une enveloppe `.claude/cli-forge-perf.json` au format `../shared/result-schema.md` :

- `score` : « perf budget compliance » (% de cas hot-path qui passent le GATE) si la cible a un budget ; sinon `null`.
- `findings[]` : un par hotspot non traité ou par claim de gain non significatif (`tier`: 3 si bottleneck en prod, 2 si dégradation détectée, 1 si micro-optim spéculative).
- `strengths[]` : sections du catalogue déjà appliquées correctement (mesure avant optim, distribution rapportée, etc.).
- `handoffs[]` : voir Dynamic Handoffs ci-dessous.

Sans `cli-cycle`, le rapport prose reste primaire ; l'enveloppe est optionnelle.

## Upstream inputs — ce qu'on tire d'AUTRES skills avant de mesurer

Avant de profiler/bencher, vérifie si ces skills ont déjà produit du matériel à réutiliser.

| Source skill | Quoi récupérer | Où ça atterrit |
|---|---|---|
| `cli-audit-tangle` | `.claude/tangle-partition.json` : god functions, cluster Fiedler, boundary functions | les **god functions sont les premiers candidats au profiling** — fan-in × LoC × call count = priorité du diagnostic |
| `cli-audit-xray` | Optimization Cards (`../shared/optimization-card.md`) : hypothèses, invariants, validation attendue | transforme une intuition sémantique en bench ciblé ; le GATE perf prouve ou rejette la carte |
| `cli-forge-resilience` | Le **stress-strain** (rung T4) et les **resource cliffs / phase transitions** | les cliffs de ressource (CPU 80 %, mémoire OOM, disque plein) sont des **bornes Amdahl** déjà documentées |
| `cli-audit-test` | La nominale du plan de test et D6 (NFR perf) | les benchs deviennent des **tests de non-régression** ; le test plan documente le SLO cible |
| `cli-audit-drift` | `CONTRACTS.md` : invariants comportementaux. Si un invariant *de perf* y a été ajouté (« p95 < 100 ms »), le GATE doit le rejouer ; sinon, le budget perf vient du plan de test (`cli-audit-test` D6/NFR) ou d'un SLO externe | un gain qui viole un invariant existant n'est pas un gain, c'est une régression à chasser |
| `cli-forge-pipeline` | Les jobs CI existants + la stratégie de cache | un bench A/B se branche dans le pipeline ; cache content-hashé = baseline reproductible (cf. `../shared/determinism.md`) |
| `cli-forge-infra` | Le profil hardware réel (NUMA, CPU model, RAM) | calibre le roofline ; un bench sur laptop ne prédit pas la prod si la membrane diffère |

## Integration with other cli-* skills

| Skill | Relation |
|-------|----------|
| `cli-audit-xray` | Produit les hypothèses d'optimisation et les invariants manquants ; ce skill mesure les candidats `benchmarkable` avec le protocole natif |
| `cli-audit-tangle` | Topologie du code → la god function est presque toujours le hot path ; ce skill fournit le diagnostic structurel, `cli-forge-perf` fournit la mesure dynamique |
| `cli-forge-resilience` | T4 stress-strain est le terrain commun ; ce skill cartographie *où ça casse*, `cli-forge-perf` mesure *combien ça coûte avant de casser* |
| `cli-audit-test` | D6 (NFR) et D7 (risque) couvrent la perf en *intention* ; ce skill fournit le harnais d'**exécution** de cette intention |
| `cli-forge-pipeline` | CI = lieu de re-mesure systématique ; ce skill alimente le pipeline en benches + gates + cache content-hashé |
| `cli-audit-code` | Détecte les anti-patterns statiques (alloc dans le hot path, complexité quadratique évidente) ; ce skill valide qu'ils sont *effectivement* coûteux |
| `cli-forge-infra` | Le profil hardware réel (NUMA, CPU baseline) calibre le roofline et le routage natif (`bench-protocol.md`) |
| `cli-cycle` | Tourne ce skill en mode handoff quand D6 (NFR) est faible ou que `cli-audit-tangle` détecte ≥ 1 god function critique |
| `cli-git-conventional` | Toute optim mergée passe par un commit conventional ; les benches sont des artefacts versionnés |
| `cli-forge-chef` (Tier XL) | Le rôle `sous-chef-perf` du cluster OPS exécute ce skill comme quality gate avant merge |

## Dynamic Handoffs

| Condition détectée | Recommande | Pourquoi |
|---|---|---|
| Profil plat ou coût réparti entre transformations sans rewrite évident | `/cli-audit-xray` | Extraire dataflow/resource-flow et générer des Optimization Cards avant de micro-optimiser |
| Hot path = god function (fan-in × LoC élevé) | `/cli-audit-tangle` | Diagnostic topologique avant de mesurer ; le refactor structurel précède l'optim |
| Gain significatif mais aucun test de non-régression | `/cli-audit-test` | D6/D7 : le gain doit être verrouillé en CI |
| Bench A/B non rejouable (médiane bouge entre runs) | `/cli-audit-wizard` (idempotence du setup) + lire `../shared/determinism.md` | Le harnais ou l'environnement n'est pas pinné — pas un problème de perf |
| Cliff de ressource observé (OOM, CPU 100 %, file pleine) | `/cli-forge-resilience` (T4) | Phase transition à documenter dans le runbook, pas seulement à benchmarker |
| Bench in-house alors qu'un outil natif existe (Criterion, JMH, benchstat, hyperfine) | (interne) Implémente le squelette natif de `references/bench-protocol.md` §Squelettes | Les stats des outils natifs sont rigoureuses, le maison ment |
| Aucun cache CI / baseline reproductible | `/cli-forge-pipeline` | Sans cache content-hashé, l'A/B mesure aussi le bruit du CI |
| Claim de gain en mémoire/€/CO₂ sans modèle explicite | (interne) Applique le modèle de `references/cost-accounting.md` | Chiffrer avec garde-fous (latence ≠ énergie, effet rebond), pas à la louche |

**Règle :** recommande, n'exécute pas sans demande explicite.

## Reference files

| Fichier | Contenu |
|---|---|
| `references/profiling.md` | Diagnostic du bottleneck (CPU/mem/I/O/lock/syscall) et classification roofline |
| `references/algorithmic.md` | Hiérarchie de complexité, structures de données, choix d'algo |
| `references/database.md` | Index, N+1, batch, EXPLAIN ANALYZE, ORM |
| `references/memory-cache.md` | RAM/disque, cache locality, mémoïsation |
| `references/async-concurrency.md` | I/O overlap, parallélisme, locks, backpressure |
| `references/math-physics.md` | Math/physique tricks, branchless, SIMD |
| `references/frontend-web.md` | Lighthouse, Core Web Vitals, LCP/CLS/INP |
| `references/systems-hardware.md` | Roofline, NUMA, hardware accelerators, footprint |
| `references/dependencies.md` | Empilement de libs, footprint binaire |
| `references/llm-inference.md` | Quantization, KV cache, batching, decode = mem-BW-bound |
| `references/crypto-throughput.md` | Choix d'algo, HW accel, batch verification, constant-time |
| `references/bio-inspired.md` | Optim combinatoire, coordination décentralisée |
| `references/idea-generation.md` | Premiers principes, inversion, analogie, "et si 10× ?" |
| `references/experiment-method.md` | Hypothèse falsifiable, ablation, contrôle de l'aléa |
| `references/benchmarking-traps.md` | DCE, warmup, p99 ment, coordinated omission, A/B confondu |
| `references/lateral-thinking.md` | Réécrire à un autre niveau, détournement, inversion |
| `references/worked-examples.md` | Traces complètes symptôme→fix→chiffres |
| `references/bench-protocol.md` | Protocole portable + routage vers Criterion/benchstat/JMH/hyperfine |
| `references/cost-accounting.md` | Modèle €/kWh/CO₂ + garde-fous (latence ≠ énergie, rebond) |
| `references/_project-profiles.md` | Contextes récurrents (Rust, air-gapped, footprint conteneur, M5, crypto) |
