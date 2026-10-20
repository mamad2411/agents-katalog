---
description: >
  Gera variações ortográficas e estruturais de um nome brasileiro para uso
  em buscas em bases americanas. Expande: ordem invertida, sem acentos,
  iniciais, sobrenome isolado, variações de parentes.
argument-hint: "Nome Completo"
---

Você vai expandir o nome em $ARGUMENTS em variações para busca em bases americanas.

Aja como a sub-skill definida em `skills/expand-brazilian-identity/SKILL.md`.

Use o script `skills/expand-brazilian-identity/scripts/expand_identity.py` se disponível.

## Saída esperada

Liste as variações geradas no formato:
1. Nome completo original
2. Nome completo sem acentos
3. Primeiro nome + último sobrenome
4. Último sobrenome + primeiro nome (ordem americana)
5. Iniciais + sobrenome (ex: C. Ferreira, C.E. Ferreira)
6. Sobrenome isolado

E pergunte ao usuário:
- Se há parentes a incluir (nome + grau de parentesco)
- Se há apelidos conhecidos
- Se deseja aprovar ou ajustar as variações antes de prosseguir
