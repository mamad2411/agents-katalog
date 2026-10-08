---
name: threat-model
description: Loop disciplinado de modelagem de ameaças para arquiteturas de software e APIs. Mapear ativos → aplicar STRIDE → classificar impacto → mitigar. Todas as respostas devem ser em português. Invocar quando o usuário disser "modelagem de ameaças", "modele isso", "modele esta arquitetura", "analise a segurança", "análise de risco", "superfície de ataque" ou ao descrever uma nova funcionalidade, endpoint, fluxo de dados ou arquitetura.
---

# Modelagem de Ameaças

Disciplina de arquitetura segura por design (Secure-by-Design). Execute todas as fases em ordem. Pule fases apenas quando explicitamente justificado.

Todas as respostas devem ser **em português**.

**Modo somente leitura (CRÍTICO):** Esta skill é exclusivamente de diagnóstico. É estritamente proibido criar, editar ou deletar qualquer arquivo do projeto durante a execução. Não implemente nenhuma mitigação, não altere configurações e não corrija código — mesmo que a solução seja óbvia. Seu único papel é mapear, analisar e recomendar. Qualquer implementação requer solicitação explícita do usuário após a entrega do diagnóstico.

Ao explorar o sistema, use o contexto fornecido para construir um modelo mental dos limites de confiança, fluxos de dados e defesas ativas (configurações do Spring Security, matrizes de RBAC, topologia de rede Docker).

---

## Fase 1 — Contexto e Mapeamento de Ativos

**Gate: não avance para a Fase 2 até que os três itens abaixo estejam mapeados.**

- **Atores** — Quem ou o que interage com o sistema? (USER, ADMIN, DIRETOR, serviço externo)
- **Ativos** — Quais são os dados mais valiosos? (PII, tokens JWT, registros críticos no banco de dados)
- **Limites de Confiança** — Onde os dados cruzam de uma zona não confiável para uma confiável? (internet → API Spring Boot → cache Redis)

---

## Fase 2 — Identificação de Ameaças (STRIDE)

Gere ≥1 cenário de ameaça concreto por categoria aplicável:

| Letra | Categoria | Pergunta-chave |
|-------|-----------|----------------|
| S | Spoofing | Um ator pode contornar a autenticação ou forjar um token? |
| T | Tampering | Dados em trânsito ou em repouso podem ser modificados sem autorização? |
| R | Repudiation | Uma ação crítica pode ocorrer sem uma trilha de auditoria imutável? |
| I | Info Disclosure | Um invasor pode extrair dados sensíveis (ex: stacktraces verbosos em um `@ExceptionHandler` mal configurado)? |
| D | Denial of Service | Existe rate limiting configurado no gateway ou na camada de aplicação? |
| E | Elevation of Privilege | Um USER pode manipular o input para acessar endpoints de DIRETOR/ADMIN ou escalar controle? |

---

## Fase 3 — Classificação

Formato por ameaça:
> `[STRIDE] – [Nome]: Se <ator> fizer <ação>, então <consequência>. (Impacto: Alto/Médio/Baixo | Probabilidade: Alto/Médio/Baixo)`

Apresente a lista classificada **antes** de gerar as mitigações — o usuário pode ter conhecimento de domínio sobre controles compensatórios já existentes. Não bloqueie nessa etapa; prossiga após uma breve pausa se não houver resposta.

---

## Fase 4 — Mitigação

Cada ameaça de risco **Alto/Médio** exige uma mitigação específica e acionável:

- Referencie padrões de mercado (RoleHierarchy, prepared statements, isolamento de rede Docker)
- Especifique *onde* aplicar a correção: cadeia de filtros de segurança, orquestração de containers ou propriedades da aplicação
- Nunca diga "escreva um código melhor" — prescreva padrões arquiteturais concretos, bibliotecas estabelecidas ou mudanças de configuração

---

## Fase 5 — Revisão Final

Obrigatório antes de declarar a análise como concluída:

- [ ] Toda ameaça de alto risco possui uma estratégia de mitigação correspondente
- [ ] Todas as mitigações respeitam as restrições da stack tecnológica atual
- [ ] Output entregue em uma tabela Markdown:

| Ameaça | STRIDE | Risco | Mitigação Arquitetural |
|--------|--------|-------|------------------------|
| ...    | ...    | ...   | ...                    |