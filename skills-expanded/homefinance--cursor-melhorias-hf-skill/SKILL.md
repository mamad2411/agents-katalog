# Home Finance Project Skill

Você está trabalhando no projeto Home Finance.

## Objetivo

Corrigir a integração entre front, back e banco de dados

## Processo obrigatório

### 1. Analisar incompatibilidades

- Identificar:
  - Divergencia entre tipos de dados entre front e back
  - Migrations ou configurações do EF na tipagem

Corrigir os pontos de divergencia.

### 2. Dockerização

Atualizar se necessário:

- Dockerfile Backend
- Dockerfile Frontend
- docker-compose.yml

O ambiente deve subir com um único comando:

docker compose up

Garantir persistência através de volumes.


### 3. Documentação

Atualizar README.md contendo:

## Como executar

docker compose up --build

## URLs

Frontend:
http://localhost:3000

Backend:
http://localhost:5000

## Estrutura

Descrição resumida dos módulos.

## Restrições

- Não remover funcionalidades existentes.
- Não alterar regras de negócio sem necessidade.
- Não criar código duplicado.
- Reutilizar componentes existentes.
- Seguir princípios SOLID.
- Seguir Clean Architecture quando aplicável.
- Preferir soluções simples.

## Resultado esperado

Ao final:

- Frontend integrado ao backend.
- Projeto compilando.
- Containers funcionando.
- README atualizado.
- Nenhum erro de build.