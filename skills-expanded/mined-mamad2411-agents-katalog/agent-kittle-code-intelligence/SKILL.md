---
name: agent-kittle-code-intelligence
description: "Kittle Agent — AI-Powered Code Intelligence Hub. Analyse de repos, debug, architecture diagrams (Mermaid.js), multi-model intelligence (Gemini 2.0, GPT-4o, Claude 3.5, DeepSeek R1). Design mode + live demo."
tags: [kittle, code-intelligence, mermaid, architecture, debug, multi-model]
---

# 🧩 Kittle — AI-Powered Code Intelligence Hub

## Rôle
Agent de code intelligence qui analyse les repositories, debug la logique complexe, et génère des diagrams d'architecture en temps réel via multi-modèles IA.

## Ce que fait Kittle (d'après l'image)

### 🎯 Core Features
- **Multi-Model Intelligence** : Connecte à Gemini 2.0/Thinking, GPT-4o, Claude 3.5, DeepSeek R1 via API directe
- **Design Mode** : Interface visuelle pour designer et explorer le code
- **Instant Mermaid.js Architecture Diagrams** : Chats avec le code → génère des diagrams d'architecture en temps réel
- **Live Demo** : Démo en direct des capacités
- **Next.js + TypeScript + Tailwind CSS** : Stack technique du site

### 🔧 Ce que l'agent Kittle fait concrètement
1. **Analyser** un repository GitHub/local → comprendre la structure, les dépendances, les patterns
2. **Générer** des diagrams Mermaid.js d'architecture en discutant avec le code
3. **Debugger** la logique complexe en croisant plusieurs modèles (un pour analyser, un pour proposer des fixes)
4. **Documenter** automatiquement le code analysé
5. **Explorer** le code en mode design (vue visuelle + code)

## Stack Technique (de l'image)
- **Frontend** : Next.js + TypeScript + Tailwind CSS
- **Logo** : K stylisé (4 formes qui s'overlapent : rouge, rose, jaune, bleu)
- **Tags** : LIVE, DEMO, NEXT.JS, TYPESCRIPT, TAILWIND CSS
- **Couleurs** : Background sombre (gray-900/950), texte blanc, accents vert/bleu/jaune
- **Modèles connectés** : Gemini 2.0/Thinking, GPT-4o, Claude 3.5, DeepSeek R1

## Architecture Kittle
```
Utilisateur (chat)
    ↓
Kittle Agent (routing multi-modèle)
    ├── Gemini 2.0 → Analyse structurelle, thinking profond
    ├── GPT-4o → Génération de code, fixes rapides
    ├── Claude 3.5 → Refactoring, architecture clean
    └── DeepSeek R1 → Raisonnement complexe, debug profond
    ↓
Mermaid.js Diagrams (output visuel)
    ↓
Codebase (analyse + documentation auto)
```

## Workflow typique
1. **Pointer** vers un repo ou un dossier de code
2. **Scanner** la structure (fichiers, dépendances, patterns)
3. **Générer** un diagramme Mermaid.js de l'architecture
4. **Discuter** avec le code (poser des questions, demander des refactorings)
5. **Debugger** en croisant les modèles pour validation croisée
6. **Documenter** les insights dans le Knowledge Graph

## Comment construire Kittle
- **Site web** : Next.js 14 + TypeScript + Tailwind CSS (même stack que Heziri)
- **Design** : Dark theme, logo K coloré, tags LIVE/DEMO
- **API** : Routes Next.js qui proxym vers les modèles IA
- **Mermaid.js** : Génération de diagrams en temps réel via chat
- **Design Mode** : Vue split (code + diagramme côte à côte)

## Connexions Knowledge Graph
- [[project-botflow-dz]] — Même stack (Next.js + Tailwind)
- [[project-heziri]] — Déployé sur le même VPS
- [[tool-model-routing]] — Routing multi-modèle (même concept)
- [[agent-fullstack-developer]] — Pour construire le frontend
- [[agent-builder-architecte]] — Pour l'architecture multi-agents