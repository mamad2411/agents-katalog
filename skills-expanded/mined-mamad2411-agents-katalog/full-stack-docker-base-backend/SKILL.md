Folder Structure

.
├── .vscode
├── .yarn
└── apps
    ├── api
    │   ├── src
    │   ├── Dockerfile
    │   └── tsconfig.app.json
    ├── customer
    │   ├── src
    │   ├── test
    │   ├── Dockerfile
    │   └── tsconfig.app.json
    ├── delivery
    │   ├── src
    │   ├── test
    │   ├── Dockerfile
    │   └── tsconfig.app.json
    └── web
        ├── .next
        ├── app
        ├── components
        ├── lib
        ├── node_modules
        ├── .eslintrc.json
        ├── .gitignore
        ├── components.json
        ├── next-env.d.ts
        ├── next.config.mjs
        ├── package.json
        ├── pnpm-lock.yaml
        ├── postcss.config.mjs
        ├── README.md
        ├── tailwind.config.ts
        └── tsconfig.json


use pnpm as the main package manager

# End Goal

A base ms strcuture whic uses kafka for messaging and rabbitmq for rpc
has proper event sourcing
has proper auth
has proper gateway
has proper swagger
has proper graphql
has proper typeorm
has proper redis
has proper rabbitmq
has proper kafka
have correct logging with winston
have elasticsearch
have kibana
have filebeat
have metricbeat
have auditbeat
have heartbeat
have apm
have redis
have rabbitmq
have kafka
have visualise ui for services


Rule :
version: tag is obsolete in docker compose
 