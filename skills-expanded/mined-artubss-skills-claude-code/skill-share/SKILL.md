---
name: skill-share
description: Uma skill que cria novas skills Claude e as compartilha automaticamente no Slack usando Rube para colaboração em equipe e descoberta de skills perfeita.
license: Complete terms in LICENSE.txt
---

## Quando usar esta skill

Use esta skill quando precisar:
- **Criar novas skills Claude** com estrutura e metadados apropriados
- **Gerar pacotes de skill** prontos para distribuição
- **Compartilhar automaticamente skills criadas** em canais do Slack para visibilidade da equipe
- **Validar a estrutura da skill** antes de compartilhar
- **Empacotar e distribuir** skills para sua equipe

Também use esta skill quando:
- **Usuário quer criar/compartilhar sua skill**

Esta skill é ideal para:
- Criar skills como parte de workflows em equipe
- Construir ferramentas internas que precisam de criação de skill + notificação da equipe
- Automatizar o pipeline de desenvolvimento de skills
- Criação colaborativa de skills com notificações em equipe

## Recursos Principais

### 1. Criação de Skill
- Cria diretórios de skill estruturados adequadamente com SKILL.md
- Gera diretórios padronizados scripts/, references/ e assets/
- Auto-gera frontmatter YAML com metadados obrigatórios
- Aplica convenções de nomenclatura (hyphen-case)

### 2. Validação de Skill
- Valida formato SKILL.md e campos obrigatórios
- Verifica convenções de nomenclatura
- Garante completude de metadados antes do empacotamento

### 3. Empacotamento de Skill
- Cria arquivos zip para distribuição
- Inclui todos os assets e documentação da skill
- Executa validação automaticamente antes do empacotamento

### 4. Integração com Slack via Rube
- Envia automaticamente informações da skill criada para canais designados no Slack
- Compartilha metadados da skill (nome, descrição, link)
- Publica resumo da skill para descoberta em equipe
- Fornece links diretos aos arquivos da skill

## Como Funciona

1. **Inicialização**: Forneça nome e descrição da skill
2. **Criação**: Diretório da skill é criado com estrutura apropriada
3. **Validação**: Metadados da skill são validados quanto à correção
4. **Empacotamento**: Skill é empacotada em formato distribuível
5. **Notificação no Slack**: Detalhes da skill são postados no canal Slack da sua equipe

## Exemplo de Uso

```
Quando você pede ao Claude para criar uma skill chamada "pdf-analyzer":
1. Cria /skill-pdf-analyzer/ com template SKILL.md
2. Gera diretórios estruturados (scripts/, references/, assets/)
3. Valida a estrutura da skill
4. Empacota a skill como arquivo zip
5. Posta no Slack: "Nova Skill Criada: pdf-analyzer - Recursos avançados de análise e extração de PDF"
```

## Integração com Rube

Esta skill aproveita Rube para:
- **SLACK_SEND_MESSAGE**: Posta informações da skill em canais da equipe
- **SLACK_POST_MESSAGE_WITH_BLOCKS**: Compartilha metadados da skill em formato rico
- **SLACK_FIND_CHANNELS**: Descobre canais alvo para anúncios de skills

## Requisitos

- Conexão de workspace Slack via Rube
- Acesso de escrita ao diretório de criação de skills
- Python 3.7+ para scripts de criação de skill
- Canal Slack alvo para notificações de skills