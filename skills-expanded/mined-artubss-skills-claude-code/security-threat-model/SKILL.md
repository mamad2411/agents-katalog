---
name: "security-threat-model"
description: "Modelagem de ameaças fundamentada em repositório que enumera limites de confiança, ativos, capacidades do atacante, caminhos de abuso e mitigações, e escreve um modelo de ameaças conciso em Markdown. Ative apenas quando o usuário solicitar explicitamente modelagem de ameaças de uma base de código ou caminho, enumerar ameaças/caminhos de abuso ou realizar modelagem de ameaças AppSec. Não ative para resumos de arquitetura geral, revisão de código ou trabalho de design não relacionado à segurança."
author: openai
---

# Modelo de Ameaças para Repositório de Código-Fonte

Entregue um modelo de ameaças de nível AppSec acionável e específico para o repositório ou caminho de projeto, não uma lista de verificação genérica. Ancore toda alegação arquitetônica em evidências no repositório e mantenha as suposições explícitas. Priorizando objetivos realistas do atacante e impactos concretos sobre listas de verificação genéricas.

## Início rápido

1) Colete (ou infira) entradas:
- Caminho raiz do repositório e quaisquer caminhos no escopo.
- Uso pretendido, modelo de deployment, exposição à internet e expectativas de autenticação (se conhecidas).
- Qualquer resumo de repositório existente ou especificação de arquitetura.
- Use prompts em `references/prompt-template.md` para gerar um resumo do repositório.
- Siga o contrato de saída obrigatório em `references/prompt-template.md`. Use-o literalmente quando possível.

## Fluxo de Trabalho

### 1) Escopo e extraia o modelo do sistema
- Identifique componentes primários, armazenamentos de dados e integrações externas do resumo do repositório.
- Identifique como o sistema é executado (servidor, CLI, biblioteca, worker) e seus pontos de entrada.
- Separe o comportamento em tempo de execução de ferramentas de CI/build/dev e de testes/exemplos.
- Mapeie os locais no escopo para esses componentes e exclua itens fora do escopo explicitamente.
- Não alegue componentes, fluxos ou controles sem evidência.

### 2) Derive limites, ativos e pontos de entrada
- Enumere limites de confiança como bordas concretas entre componentes, anotando protocolo, autenticação, criptografia, validação e limite de taxa.
- Liste ativos que impulsionam o risco (dados, credenciais, modelos, configuração, recursos de computação, logs de auditoria).
- Identifique pontos de entrada (endpoints, superfícies de upload, analisadores/decodificadores, acionadores de job, ferramentas de administração, sinks de logging/erro).

### 3) Calibre ativos e capacidades do atacante
- Liste os ativos que impulsionam o risco (credenciais, PII, estado crítico para integridade, componentes críticos para disponibilidade, artefatos de build).
- Descreva capacidades realistas do atacante baseado em exposição e uso pretendido.
- Anote explicitamente não-capacidades para evitar severidade inflacionada.

### 4) Enumere ameaças como caminhos de abuso
- Prefira objetivos do atacante que mapeiem para ativos e limites (exfiltração, escalação de privilégio, comprometimento de integridade, negação de serviço).
- Classifique cada ameaça e a vincule aos ativos impactados.
- Mantenha o número de ameaças pequeno, mas de alta qualidade.

### 5) Priorize com raciocínio explícito de probabilidade e impacto
- Use probabilidade e impacto qualitativos (baixo/médio/alto) com justificativas breves.
- Defina prioridade geral (crítico/alto/médio/baixo) usando probabilidade × impacto, ajustado para controles existentes.
- Declare quais suposições mais influenciam o ranking.

### 6) Valide contexto do serviço e suposições com o usuário
- Resuma suposições-chave que afetam materialmente ranking de ameaça ou escopo, e solicite ao usuário que as confirme ou corrija.
- Faça 1–3 perguntas direcionadas para resolver contexto ausente (proprietário do serviço e ambiente, escala/usuários, modelo de deployment, autenticação/autorização, exposição à internet, sensibilidade de dados, multi-tenancy).
- Pause e aguarde feedback do usuário antes de produzir o relatório final.
- Se o usuário declinar ou não puder responder, declare quais suposições permanecem e como influenciam a prioridade.

### 7) Recomende mitigações e caminhos de foco
- Distinga mitigações existentes (com evidência) de mitigações recomendadas.
- Vincule mitigações a locais concretos (componente, limite ou ponto de entrada) e tipos de controle (verificações authZ, validação de entrada, aplicação de schema, sandboxing, limites de taxa, isolamento de segredos, logging de auditoria).
- Prefira dicas de implementação específicas a conselhos genéricos (ex: "enforce schema at gateway for upload payloads" vs "validate inputs").
- Base recomendações em contexto de usuário validado; se suposições permanecerem não resolvidas, marque recomendações como condicionais.

### 8) Execute uma verificação de qualidade antes de finalizar
- Confirme que todos os pontos de entrada descobertos são cobertos.
- Confirme que cada limite de confiança é representado em ameaças.
- Confirme separação runtime vs CI/dev.
- Confirme que clarificações de usuário (ou respostas não explícitas) são refletidas.
- Confirme que suposições e perguntas abertas são explícitas.
- Confirme que o formato do relatório corresponde próximo ao formato de saída obrigatório definido em template de prompt: `references/prompt-template.md`
- Escreva o Markdown final para um arquivo nomeado `<repo-ou-dir-name>-threat-model.md` (use o basename da raiz do repositório, ou o diretório no escopo se você foi solicitado a modelar um subcaminho).

## Orientação de priorização de risco (ilustrativa, não exaustiva)
- Alto: RCE pré-autenticação, bypass de autenticação, acesso entre tenants, exfiltração de dados sensíveis, roubo de chave ou token, comprometimento de integridade de modelo ou configuração, fuga de sandbox.
- Médio: DoS direcionado de componentes críticos, exposição parcial de dados, bypass de limite de taxa com impacto mensurável, envenenamento de log/métricas que afeta detecção.
- Baixo: vazamentos de info com baixa sensibilidade, DoS ruidoso com mitigação fácil, problemas exigindo precondições improváveis.

## Referências

- Contrato de saída e template de prompt completo: `references/prompt-template.md`
- Lista opcional de controles/ativos: `references/security-controls-and-assets.md`

Carregue apenas os arquivos de referência que você precisa. Mantenha o resultado final conciso, fundamentado e revisável.