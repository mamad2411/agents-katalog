---
name: private-project-context
description: Use quando precisar decidir se uma mudança do ecossistema Conn2Flow pertence ao repositório privado, ao núcleo conn2flow, ou aos dois.
user-invocable: false
---

# Contexto de projeto privado

Use esta skill sempre que a tarefa tocar código que exista ou possa existir tanto no repositório privado quanto em `conn2flow`.

## Papéis dos repositórios

- `conn2flow`: núcleo aberto e genérico do sistema.
- repositório privado: camada do projeto, com módulos, customizações, temas e overrides específicos.

## Regras de decisão

1. Procure primeiro a solução no repositório privado.
2. Se o arquivo já existir no privado, priorize esse arquivo.
3. Se a funcionalidade for privada e ainda não existir, crie-a no privado.
4. Só edite `conn2flow` quando a mudança for genérica, reaproveitável e útil para todos os projetos.
5. Se a correção envolver os dois lados, separe o que é core do que é específico do projeto.

## Checklist rápido

- A mudança atende apenas este cliente ou projeto?
- Existe override correspondente no repositório privado?
- Criar o arquivo no privado resolve sem tocar o core?
- Mover para o core reduz duplicação real entre projetos?
- Há risco de sobrescrever comportamento privado já existente?