---
name: methodologies-apprentissage
description: Concevez ou examinez des applications éducatives en reliant objectifs d'apprentissage, besoins des apprenants, activités, rétroaction et preuves d'apprentissage. Utilisez ce skill pour les nouveaux outils pédagogiques ou les modifications substantielles de leur ingénierie didactique.
metadata:
  version: "1.6.0"
  language: "fr"
  based_on: "learning-methodologies@1.6.0"
  license: "MIT"
  repo: "https://github.com/siberius/learning-methodologies"
  author: "Luděk Sušický"
  format: "paquet natif avec Markdown autonome généré"
---

# Méthodologies d'apprentissage

Aidez à concevoir, mettre en œuvre ou examiner des applications éducatives dont les activités d'apprentissage, l'étayage et l'évaluation répondent aux besoins des apprenants ciblés. Adaptez l'ampleur du travail à la demande, aux enjeux et aux incertitudes. Une brève activité de classe ne nécessite ni une étude d'évaluation complète ni un nouveau document de cadrage.

## Méthodes didactiques pour les applications créées avec l'IA

Utilisez ces méthodes pour traduire les objectifs pédagogiques en actions de l'apprenant, en règles de rétroaction et en preuves d'apprentissage au sein de l'application générée. Par exemple, la récupération en mémoire exige une tentative active avant de révéler la réponse, tandis que l'étayage nécessite une aide modulable et une distinction claire entre performance assistée et autonome. L'IA peut aider à concrétiser ces choix ; son résultat exige toujours une révision didactique et disciplinaire. Cela s'applique aux applications hors ligne comme à l'IA en cours d'exécution lorsque l'objectif d'apprentissage le justifie.

Consultez la [justification didactique](references/didactic-rationale.md) pour expliquer l'adéquation d'une méthode ou guider son implémentation. Elle relie les méthodes aux décisions produit et aux preuves nécessaires pour les évaluer.

## Guider le concepteur dans ses choix

À chaque décision didactique substantielle, réexaminez l'objectif, l'action de l'apprenant, les preuves, le soutien et les contraintes. Réutilisez les choix déjà établis. Pour un arbitrage important non résolu, proposez une sélection restreinte et pertinente, généralement deux ou trois options, assorties d'une description simple et d'une application concrète au projet. Recommandez-en une, expliquez le compromis principal et demandez quelle approche le concepteur préfère. Consultez le [dialogue de conception](references/design-dialogue.md) pour amorcer ou réexaminer un tel choix. Ce processus régit l'échange avec le concepteur, distinct de l'interaction tuteur-apprenant.

Ne rouvrez pas les choix tranchés ou refusés sans élément nouveau pertinent. Respectez la délégation explicite des décisions courantes et poursuivez avec une justification concise. Le silence ne vaut pas approbation d'un élargissement du périmètre. En attente d'une réponse, avancez sur les parties indépendantes. Une modification cosmétique ne déclenche pas ce processus.

Chargez les détails selon le besoin : [méthodes](references/methods.md) pour les activités d'apprentissage et l'étayage ; [jeux](references/learning-games.md) pour la motivation et les mécaniques ludiques ; [évaluation](references/assessment.md) pour les preuves et le barème ; [interface cognitive](references/cognitive-ux.md) pour les représentations, le multimédia et la charge attentionnelle ; [pratique adaptative](references/adaptive-practice.md) pour les séances répétées ou l'ajustement de la difficulté. Suivez les parcours conditionnels ci-dessous pour les simulations, l'état du tuteur et l'IA en temps d'exécution. Étudiez la méthode pertinente avant de la proposer ; ne chargez pas toutes les références d'emblée.

Traduisez la méthode retenue en comportement observable du produit et en vérification probante. Distinguez les décisions proposées, retenues, implémentées et vérifiées. La validation technique n'établit pas l'efficacité didactique.

## Parcours de travail

Suivez ce parcours avec la granularité requise par la tâche : définir l'objectif et les contraintes → choisir une méthode adaptée à l'obstacle d'apprentissage → relier l'activité de l'apprenant aux preuves → implémenter dans le périmètre défini → vérifier le résultat. Pour une revue ou un audit, examinez la conception existante au lieu de créer. Réutilisez le contexte connu ; n'exigez pas un document de cadrage à chaque étape.

Consultez les [exemples de décisions](references/decision-examples.md) lorsqu'une clarification est nécessaire sur l'étayage, les réponses alternatives ou l'alignement curriculaire. Ils illustrent des décisions concrètes, non des scripts rigides à reproduire partout.

## Établir le contexte d'apprentissage

Exploitez les informations déjà présentes dans la demande, le projet et les documents fournis. En cas de lacunes, n'interrogez que sur les éléments qui modifient sensiblement la conception. Pour les incertitudes mineures, formulez une hypothèse raisonnable et poursuivez. Évitez les questionnaires systématiques ou les demandes répétées de validation pour des choix ordinaires déjà couverts par la consigne.

Identifiez le contexte qui influe sur la conception : profil et prérequis des apprenants, discipline, acquis visés, usage autonome ou en classe, temps disponible et équipements, langue, besoins d'accessibilité et référentiels fournis. Adossez-vous à un programme ou un socle d'apprentissage lorsqu'il est pertinent pour le contexte ; ne supposez pas un cadre national unique par défaut. Ajustez le ton au contexte et aux attentes de l'auteur. N'inférez pas l'attention, la motivation, les capacités ou une pédagogie préférée à partir d'étiquettes générationnelles.

Intégrez l'activité pédagogique environnante lorsque c'est utile : préparation, travail individuel ou de groupe, étayage de l'enseignant, mise en commun et prolongements. Une démonstration guidée par l'enseignant peut nécessiter une bonne question de relance ; les comptes utilisateurs et les scores individuels ne sont pas requis.

Distinguez l'âge, le statut scolaire et l'expérience du sujet : enfant, élève, étudiant et apprenant adulte ne sont ni des catégories interchangeables ni des niveaux d'aptitude figés. Pour définir ou ajuster le public cible, consultez le profil d'apprenant dans le [dialogue de conception](references/design-dialogue.md). Adaptez la terminologie et le soutien au cadre d'usage ; conservez des termes neutres dans les directives générales. Le concepteur, l'apprenant et l'enseignant ou parent accompagnateur peuvent être des personnes distinctes.

## Relier les objectifs à une activité observable

Pour chaque objectif clé, reliez l'action de l'apprenant, les preuves, les critères de réussite, les conditions d'aide et la décision didactique suivante. Restez concis pour les tâches simples. Pour une démarche d'investigation ouverte, les preuves peuvent porter sur la pertinence d'une question, l'exploitation d'indices ou la révision d'une explication ; une réponse préétablie unique n'est pas le seul format possible.

Exemple : l'élève prédit l'effet d'une variation de résistance sur l'intensité du courant, teste son hypothèse sur un modèle, explicite les écarts éventuels et résout en autonomie un nouveau problème. Manipuler un curseur ou faire défiler un écran ne suffit pas à attester la compréhension.

Appuyez-vous sur l'obstacle d'apprentissage identifié pour choisir une intervention adaptée. Traitez l'explication d'une erreur comme une hypothèse de travail, non comme un diagnostic définitif. Sélectionnez un ensemble restreint et cohérent de démarches ; n'accumulez pas les fonctionnalités sous prétexte qu'elles figurent dans le catalogue. Consultez les [méthodes](references/methods.md) lors du choix ou de la mise en œuvre d'une démarche, d'une séquence d'étayage ou d'une règle de progression.

Pour les mécaniques ludiques, les leviers motivationnels ou la revue de jeux éducatifs, consultez [jeux d'apprentissage et ludification raisonnée](references/learning-games.md). Il détaille les boucles d'apprentissage jouables, la sélection des mécaniques, les limites des preuves et l'implémentation depuis les micro-outils jusqu'aux dispositifs longitudinaux. Adaptez l'approche au primaire, au secondaire, au supérieur et à la formation d'adultes selon les acquis préalables et le contexte local.

La référence des méthodes aborde explicitement le questionnement socratique, la technique de Feynman, la zone proximale de développement et l'étayage, les exemples résolus et commentés, la pratique de récupération et l'espacement critique, l'apprentissage par l'erreur, la métacognition, l'investigation, le jeu de rôle, l'apprentissage par les pairs et coopératif, la pédagogie de projet, la classe inversée et la ludification ciblée. Ce sont des approches à la carte, non des exigences systématiques pour chaque outil.

La taxonomie de Bloom structure les objectifs cognitifs et les types de connaissances. Distinguez la complexité intrinsèque des prérequis ; n'imposez pas six niveaux obligatoirement verrouillés. Pour des compétences pratiques, relationnelles ou transversales, choisissez des preuves cohérentes avec l'acquis visé et reconnaissez ce qu'une tâche sur écran ne peut évaluer.

## Choisir une réalisation proportionnée

Distinguez l'IA mobilisée pour développer l'application de l'IA exploitée par les apprenants dans le produit final. Choisissez entre contenus statiques validés, interactions ou simulations déterministes, et IA en temps d'exécution selon l'objectif visé et les contraintes opérationnelles. Indices, rétroaction guidée et réactivation espacée peuvent fonctionner sans aucun service d'IA externe.

Avant d'ajouter une fonctionnalité lourde, évaluez son apport pédagogique, la charge cognitive induite, la charge pour l'enseignant, la maintenance, la gestion des données et le coût d'exploitation. Explicitez les compromis essentiels. N'ajoutez pas de comptes, d'analytique complexe, de tableaux de bord, de backend, de services payants ou de flux de données externes dans le seul but de donner une illusion d'exhaustivité. Faites valider les décisions modifiant le périmètre si elles ne sont pas déjà autorisées.

Consultez les [simulations](references/simulations.md) pour la modélisation de systèmes, la réalisation d'expériences ou la scénarisation de jeux de rôle. Distinguez nettement les observations réelles, les calculs modélisés et les reconstitutions fictives. Ne présentez jamais une génération d'IA fictive comme une mesure expérimentale ni ne prétendez qu'une expérience physique a eu lieu.

Consultez l'[IA en cours d'exécution](references/runtime-ai.md) uniquement lorsque le produit final interroge directement un modèle d'IA. Précisez le rôle tutoriel, les frontières documentaires, la supervision humaine, la circulation des données, les plafonds budgétaires et la gestion des pannes. Un prompt ne remplace pas la sécurité applicative.

Consultez les [modes du tuteur et la continuité](references/tutor-state.md) pour concevoir un tutorat guidé multi-étapes, des transitions entre entraînement et évaluation ou la reprise d'une session. Conservez l'état et les traces d'apprentissage au sein de l'application ; ces mécanismes ne requièrent aucune IA en temps réel.

## Rendre la rétroaction et les décisions fiables

Proposez une étape constructive après une erreur. En situation d'entraînement, prévoyez un accès à des indices progressifs et à une explication directe ou un exemple résolu si nécessaire ; évitez l'interrogation socratique sans fin. Réduisez l'étayage à mesure que l'autonomie se confirme, tout en maintenant l'aide disponible sur demande. Une situation d'évaluation peut encadrer ou restreindre l'assistance selon des règles explicites.

Distinguez la réussite autonome, la réussite guidée, la simple lecture de la solution et le doute. Une bonne réponse fortuite, une déclaration d'assurance ou deux succès avec étayage ne suffisent pas à certifier la maîtrise. N'inférez pas d'aptitude stable, de manque de motivation ou de trouble d'apprentissage à partir d'une brève interaction isolée.

Consultez l'[évaluation](references/assessment.md) pour concevoir des exercices notés, des grilles critériées, des parcours adaptatifs ou mesurer les acquis. Contrôlez l'exactitude disciplinaire, la plausibilité des distracteurs, les unités de mesure et tolérances chiffrées, ainsi que l'alignement réel de la tâche avec la compétence visée. Préservez la validité des méthodes ou formulations alternatives rigoureuses. Dissociez les gratifications ludiques ou la rapidité du niveau de maîtrise effectif, sauf si la vitesse constitue un critère pédagogique explicite.

## Préserver l'accessibilité et le pouvoir d'agir enseignant

Concevez l'application selon les critères WCAG 2.2 niveau AA pertinents pour l'activité et les besoins effectifs des apprenants. Vérifiez la navigabilité au clavier, la visibilité de la focalisation, la clarté des intitulés et messages, les alternatives au tout-couleur ou tout-audio, et la présence de durées ajustables ou justifiées. Proposez des modalités adaptées pour appréhender l'information et exprimer sa compréhension ; n'attribuez pas de prétendus « styles d'apprentissage » rigides. Faites appel à une expertise spécialisée en accessibilité lorsque la mise en œuvre le justifie.

Ne collectez que les données strictement indispensables à l'activité pédagogique et explicitez qui y a accès, où elles transitent et combien de temps elles sont conservées. Vérifiez les obligations applicables (fournisseur, établissement, cadre local et RGPD) pour le déploiement effectif ; n'inventez pas de règles juridiques imaginaires. Une activité locale et anonyme ne requiert ni comptes nominatifs ni traçage persistant.

Permettez à l'enseignant ou au responsable pédagogique de relire les contenus, corriger les arbitrages et intervenir en cas d'adaptation automatisée inappropriée. Un simple fichier de configuration éditable peut suffire ; une plateforme de gestion complexe n'est pas requise. Toute décision lourde d'évaluation sommative ou d'orientation exige un arbitrage humain responsable.

## Coordonner les expertises sans alourdir le flux de travail

Mobilisez ces différentes perspectives selon les besoins du projet ; un seul agent peut les synthétiser pour une tâche modeste :

- Ingénieur pédagogique : acquis visés, scénarisation didactique et choix des démarches.
- Didacticien de la discipline : exactitude des notions, prérequis, exemples et conceptions erronées fréquentes.
- Concepteur de l'évaluation : preuves, critères de réussite, alternatives recevables et limites de validité.
- Designer d'interaction : flux de l'apprenant, ergonomie de l'étayage, accessibilité et intégration en classe.
- Développeur : modèles de données, calculs, gestion d'état, persistance et résilience aux pannes.
- Réviseur : conformité entre l'intention didactique, la conception et le comportement constaté.

Concrétisez ces arbitrages dans l'implémentation. Ne qualifiez pas un choix technique commode de pédagogiquement vertueux sans justification. Tranchez les désaccords substantiels par une vérification documentaire, un test ciblé ou une question formulée clairement au responsable. Recourez à une revue indépendante quand la complexité ou les enjeux le justifient ; ne montez pas une équipe entière pour chaque intervention. N'invoquez d'autres compétences que si elles sont disponibles et adaptées au travail à accomplir.

## Vérifier et rendre compte avec discernement

Pour l'implémentation, testez le parcours réel de l'apprenant, les erreurs typiques observées, l'accès à l'étayage et les états de défaillance critiques. Pour une demande d'analyse pure, consignez constats et recommandations sans altérer le produit. Adaptez la validation au type d'application : une simulation réclame la vérification du modèle physique ou mathématique ; une IA en temps d'exécution nécessite de tester les ruptures de service et le filtrage des réponses ; une activité statique classique n'a besoin d'aucun de ces tests par défaut.

Distinguez trois niveaux de conclusions : le bon fonctionnement technique, la pertinence didactique et les acquis réels d'apprentissage observés. La seule conformité informatique ne prouve pas l'efficacité pédagogique. Un test pilote restreint peut révéler des difficultés d'ergonomie sans prouver de gain d'apprentissage direct. Rendez compte des tests réellement effectués et des hypothèses restant à valider ; n'inventez pas d'observations d'élèves ni de résultats d'efficacité fictifs.

Lors de la restitution, synthétisez l'objectif d'apprentissage, la démarche adoptée, les hypothèses opérationnelles notables, les tests réalisés et les limites résiduelles. N'incluez un tableau objectifs-preuves que s'il facilite l'appropriation du livrable. Adaptez la forme à la demande de l'utilisateur.

## Rédiger les textes pour les apprenants sans bavardage d'IA

Le texte de l'application est le vecteur de l'enseignement. Appliquez la même exigence aux consignes, amorces, rétroactions et explications :

- Bannissez les qualificatifs creux (« moderne », « stimulant », « interactif ») à moins que la phrase suivante n'en démontre la réalité concrète.
- Formulez directement le propos ; évitez les tournures rhétoriques comme « ce n'est pas seulement X, mais Y ».
- Supprimez les annonces métatextuelles (« dans cette activité, vous allez apprendre… ») ; indiquez directement ce que fait l'apprenant.
- La rétroaction précise ce qui est correct, ce qui manque et l'étape d'action suivante.
- Soyez précis sur les chiffres, unités et conditions ; proscrivez « améliore sensiblement » sans données mesurées.
- Pas d'emojis dans les boutons, titres ou libellés. Privilégiez du texte clair et des icônes cohérentes.
- Adaptez le registre de langue aux apprenants et utilisez une terminologie constante pour chaque notion.

Relisez le texte du point de vue de l'apprenant. Si une formulation pouvait figurer à l'identique dans n'importe quel autre produit générique, supprimez-la ou rendez-la spécifique.

## Intégration

Pour choisir un modèle, un niveau de raisonnement ou de vitesse, ou pour adapter le chargement, consultez les [profils de modèles et environnements](references/model-profiles.md). Ce document fournit des repères documentés pour OpenAI, Claude et Gemini. Maintenez un cadre pédagogique commun et distinguez les tests effectivement réalisés de la compatibilité théorique. Ne chargez pas ce profil pour une tâche pédagogique ordinaire qui ne le requiert pas.

Adapté aux jeux éducatifs, quiz, tutoriels, simulations et revues d'ingénierie didactique. Le cœur ne requiert aucun paquet externe, API, modèle d'IA particulier ni données d'élèves. Les références sont conditionnelles. Le paquet natif utilise ce fichier et ses références ; `methodologies-apprentissage.md` est l'édition autonome générée. L'installation, le déploiement et les modifications externes nécessitent l'accord préalable de l'utilisateur. Ce skill ne se substitue pas aux consignes du projet et n'autorise pas d'extension non convenue du périmètre.

Références de conception : [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Lignes directrices CUA de CAST](https://udlguidelines.cast.org/). Elles éclairent la conception et la revue ; les mentionner ne vaut pas certification de conformité ni d'efficacité didactique.
