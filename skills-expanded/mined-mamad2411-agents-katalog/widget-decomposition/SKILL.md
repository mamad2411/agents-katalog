---
name: widget_decomposition
description: >
  Use this skill when working on Flutter UI files containing widgets.
  Triggers automatically when part-of directives following this pattern are
  detected (*.events.dart, *.parts.dart). Triggers manually when the user asks
  to decompose, organise, or refactor a complex widget, or when a widget meets
  complexity criteria (build > 40 lines, non-trivial event handlers, mixed
  plumbing and functional logic).
---

# Widget Decomposition

Pattern de décomposition des widgets Flutter complexes en fichiers `part of`
pour séparer la plomberie Flutter, les handlers d'événements et les
sous-widgets.

## Pattern de décomposition

### Organisation en dossier

Lors de la décomposition, **proposer** de regrouper les fichiers du widget
dans un dossier dédié portant le nom du widget :

```
my_widget/
├── my_widget.dart          ← fichier principal (plomberie Flutter)
├── my_widget.events.dart   ← mixin privé (handlers d'événements)
└── my_widget.parts.dart    ← mixin privé (sous-widgets)
```

Cela évite de polluer le dossier parent avec plusieurs fichiers liés au même
widget. Les imports externes vers ce widget ne changent pas si le barrel export
est conservé, ou pointent vers `my_widget/my_widget.dart`.

### Placement des sous-widgets dédiés

Quand un widget (ou son dossier) **n'est consommé que par un seul widget
parent**, il doit être placé **dans le dossier du consommateur**, pas dans
un dossier partagé comme `lib/widgets/`.

**Règle** : si le widget consommateur n'a pas encore de dossier dédié, le
créer au préalable (appliquer d'abord la décomposition du consommateur).

Exemple : `AudioControlPanel` n'est utilisé que par `FilteringTab` →

```
lib/screens/page_filter/
├── page_filter.dart
├── page_filter.events.dart
├── page_filter.dialog.dart
└── audio_control_panel/
    ├── audio_control_panel.dart
    ├── audio_control_panel.parts.dart
    └── panel_painter.dart
```

En revanche, un widget réutilisé par plusieurs consommateurs reste dans
`lib/widgets/` (éventuellement dans son propre sous-dossier).

### Structure cible (StatefulWidget)

Pour un widget `MyWidget` avec sa classe State `_MyWidgetState` :

### Fichier principal — `my_widget.dart`

Contient uniquement :
- Imports et directives `part`
- Classe du widget : constructeur, propriétés
- Classe State avec `with _MyWidgetParts` :
  - Variables d'état
  - Plomberie Flutter : `initState()`, `dispose()`, `build()`,
    `didUpdateWidget()`, `didChangeDependencies()`
  - `build()` garde la structure squelettique (Scaffold, Column, Row,
    StreamBuilder…) et utilise les fonctions/champs du mixin pour les
    feuilles et les méthodes de l'extension pour les handlers

#### Ordre des membres dans la classe State

Dans la classe State (décomposée ou non), respecter cet ordre :

1. **Getters sur les propriétés du widget** — raccourcis pour éviter `widget.prop` dans le corps de la classe
2. **Champs `final`** — dépendances injectées, constantes d'instance
3. **Champs `late`** — initialisés dans `initState()`
4. **`initState()`** — si nécessaire
5. **`dispose()`** — si nécessaire
6. **`build()`** — toujours présent
7. **`didUpdateWidget()`** — si nécessaire
8. **Handlers d'événements** — dans le cas dégénéré (widget simple, pas de `*.events.dart`), les callbacks restent ici ; sinon délégués au mixin `_MyWidgetEvents`
9. **Méthodes utilitaires** — dans le cas dégénéré (pas de `*.parts.dart`) ; sinon déléguées au mixin `_MyWidgetParts`

```dart
class _MyWidgetState extends State<MyWidget> with _MyWidgetParts {
  // 1. Getters widget
  String get title => widget.title;
  bool get isReadOnly => widget.isReadOnly;

  // 2. Champs final
  final _formKey = GlobalKey<FormState>();

  // 3. Champs late
  late final TextEditingController _controller;

  // 4. initState
  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: title);
  }

  // 5. dispose
  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // 6. build
  @override
  Widget build(BuildContext context) { ... }

  // 7. didUpdateWidget (si nécessaire)
  @override
  void didUpdateWidget(MyWidget old) { ... }

  // 8. Handlers (cas dégénéré seulement)
  void _onSubmit() { ... }

  // 9. Méthodes utilitaires (cas dégénéré seulement)
  String _formatValue(double v) => v.toStringAsFixed(2);
}
```

```dart
import "package:flutter/material.dart";

part "my_widget.events.dart";
part "my_widget.parts.dart";

class MyWidget extends StatefulWidget {
  const MyWidget({super.key, required this.title});
  final String title;

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> with _MyWidgetParts {
  var isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          header(),       // ← mixin _MyWidgetParts
          vSpace16,
          statusBadge(),  // ← mixin _MyWidgetParts
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: onSaveTap,  // ← extension _MyWidgetEvents
        child: const Icon(Icons.save),
      ),
    );
  }
}
```

### Fichier événements — `my_widget.events.dart`

- `part of "my_widget.dart";`
- Mixin privé sur la classe State
- Contient les handlers d'événements non triviaux
- Accès direct à `widget`, `context`, `setState`, `mounted` (même bibliothèque)

```dart
part of "my_widget.dart";

mixin _MyWidgetEvents on State<MyWidget> {
  Future<void> onSaveTap() async {
    final confirmed = await showConfirm(
      context,
      title: "Sauvegarder",
      message: "Confirmer la sauvegarde ?",
      confirmLabel: "Sauvegarder",
    );
    if (!confirmed || !mounted) return;
    await repository.save(widget.title);
  }

  void onExpandToggle() {
    setState(() => isExpanded = !isExpanded);
  }
}
```

### Fichier sous-widgets — `my_widget.parts.dart`

- `part of "my_widget.dart";`
- Mixin privé avec contrainte `on State<MyWidget>`
- Sous-widgets **sans** dépendance à l'état/contexte → champ `final`
- Sous-widgets **avec** dépendance à l'état/contexte → fonction
- Contient les "feuilles" et sous-arbres intermédiaires, **pas** les structures
  de mise en page (Column, Row, Stack…) qui restent dans `build()`

```dart
part of "my_widget.dart";

mixin _MyWidgetParts on State<MyWidget> {
  // Indépendant du state/context → champ final
  final sectionTitle = Text("Paramètres",
    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
  );

  // Dépend du state → fonction
  Widget statusBadge() => Badge(
    label: Text(isExpanded ? "Ouvert" : "Fermé"),
  );

  // Dépend du context → fonction
  Widget header() => Text(
    widget.title,
    style: Theme.of(context).textTheme.headlineMedium,
  );
}
```

### Variante StatelessWidget

Pour un StatelessWidget sans classe State :
- Extension : `extension _MyWidgetEvents on MyWidget { ... }`
- Mixin : `mixin _MyWidgetParts on StatelessWidget { ... }`
  - Tous les sous-widgets dépendant de propriétés du widget → fonctions
    (pas de champs `final` accédant à `this` dans un mixin)
- La classe widget déclare `with _MyWidgetParts`

### Cas dégénéré

Si le widget n'a que des handlers à extraire (pas de sous-widgets complexes)
ou inversement, ne créer que le fichier pertinent (events OU parts, pas
les deux).

## Critères de complexité

Proposer la décomposition quand **au moins un** critère est vrai :

1. **`build()` dépasse 40 lignes** (~écran visible)
2. **Handlers d'événements non triviaux** : plus qu'un simple `context.pop()`
   ou appel de setter en une ligne
3. **Mélange plomberie/logique** : les méthodes relevant de la plomberie
   Flutter (`initState`, `dispose`, `build`…) cohabitent avec des méthodes
   répondant aux besoins fonctionnels de l'écran

## Déclenchement

- **Automatique** : si des directives `part of` liées à ce pattern sont
  détectées (fichiers `*.events.dart` ou `*.parts.dart`) → appliquer les
  conventions du pattern lors de toute modification
- **Manuel** : si le widget atteint les critères de complexité mais n'est
  pas encore décomposé → **proposer** la décomposition à l'utilisateur,
  **attendre sa validation** avant d'agir

## styled_widget : notations postfix

Si le projet dépend du package `styled_widget`, **TOUJOURS** utiliser les
notations postfix à la place des widgets conteneurs équivalents
(`Padding`, `Expanded`, `SizedBox`, `Center`, `ClipRRect`, `Transform`…).

```dart
// ❌ À éviter
Padding(
  padding: const EdgeInsets.all(16),
  child: Expanded(child: Text("hello").bold()),
)

// ✅ styled_widget
Text("hello").bold().padding(all: 16).expanded()
```

Référence complète des 78 méthodes disponibles (Widget, Text, TextSpan, Icon,
List<Widget>) : voir [styled_widget.md](./styled_widget.md).

## Utilitaires partagés

Tout projet Flutter devrait définir des utilitaires réutilisables :

| Fichier | Contenu |
|---------|---------|
| `lib/widgets/common.dart` | Constantes d'espacement (`vSpace8`, `hSpace16`…), paddings, widgets réutilisables simples |
| `lib/widgets/extensions.dart` | Extensions sur `BuildContext` (navigation) et `Widget` (composition) |
| `lib/utils/dialogs.dart` | Fonctions de dialogue réutilisables (`showMessage`, `showConfirm`…) |

Si ces fichiers sont absents du projet, **proposer** de les créer à partir
des templates fournis dans `templates/` de ce skill.

## Sous-compétence : refactoring

Pour le processus détaillé de transformation d'un widget existant
(analyse, proposition, création des fichiers, post-traitement), voir
[refactoring.md](./refactoring.md).
