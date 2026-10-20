---
description: "Repo Bootstrapper — minimal, demo-ready scaffolds"
globs: []
alwaysApply: false
---

<rule>
name: repo_bootstrapper
description: "Maghanda ng skeleton manifests para sa piniling demo (RAG | REST API | Web UI)."
triggers:
  - command: "/bootstrap"
outputs:
  - "memory-bank/bootstrap/manifest.yaml"
  - "memory-bank/bootstrap/README.md"
  - "memory-bank/bootstrap/tree.md"
actions:
  - type: generate_file
    path: "memory-bank/bootstrap/manifest.yaml"
    template: |
      demo_type: "<rag|rest_api|web_ui>"
      name: "sample-<demo_type>"
      structure:
        - path: demos/<demo_type>/
        - path: demos/<demo_type>/README.md
        - path: demos/<demo_type>/.env.example
        - path: demos/<demo_type>/scripts/run_demo.sh
      notes:
        - "No code yet; outline only. Populate later."
  - type: generate_file
    path: "memory-bank/bootstrap/README.md"
    template: |
      # Repo Bootstrapper (Goal-Level)
      Choose a demo_type: rag | rest_api | web_ui
      Outputs:
      - manifest.yaml (structure)
      - tree.md (file tree)
      - README.md (how to extend)

      Next:
      1) Fill in sample inputs
      2) Define acceptance criteria
      3) Keep demo ≤10 minutes
  - type: generate_file
    path: "memory-bank/bootstrap/tree.md"
    template: |
      # Target File Tree (Draft)
      demos/
      └── <demo_type>/
          ├── README.md
          ├── .env.example
          └── scripts/
              └── run_demo.sh
  - type: suggest
    message: "Bootstrap manifests created. Set demo_type in manifest.yaml, then populate."
</rule>
