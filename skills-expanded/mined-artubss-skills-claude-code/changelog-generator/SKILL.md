---
name: changelog-generator
description: Cria automaticamente changelogs voltados para usuários a partir de commits do git, analisando o histórico de commits, categorizando mudanças e transformando commits técnicos em notas de lançamento claras e amigáveis para clientes. Transforma horas de escrita manual de changelog em minutos de geração automatizada.
---

# Changelog Generator

Esta habilidade transforma commits técnicos do git em changelogs polidos e amigáveis para usuários que seus clientes e usuários realmente compreenderão e apreciarão.

## Quando Usar Esta Habilidade

- Preparar notas de lançamento para uma nova versão
- Criar resumos de atualizações de produtos semanais ou mensais
- Documentar mudanças para clientes
- Escrever entradas de changelog para submissões em app stores
- Gerar notificações de atualização
- Criar documentação de lançamento interna
- Manter uma página pública de changelog/atualizações de produto

## O Que Esta Habilidade Faz

1. **Verifica Histórico do Git**: Analisa commits de um período específico ou entre versões
2. **Categoriza Mudanças**: Agrupa commits em categorias lógicas (recursos, melhorias, correções de bugs, mudanças quebradoras, segurança)
3. **Traduz Técnico → Amigável para Usuários**: Converte commits de desenvolvedores em linguagem de cliente
4. **Formata Profissionalmente**: Cria entradas de changelog limpas e estruturadas
5. **Filtra Ruído**: Exclui commits internos (refatoração, testes, etc.)
6. **Segue Boas Práticas**: Aplica diretrizes de changelog e sua voz de marca

## Como Usar

### Uso Básico

Do seu repositório do projeto:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### Com Intervalo de Data Específico

```
Create a changelog for all commits between March 1 and March 15
```

### Com Diretrizes Personalizadas

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## Exemplo

**Usuário**: "Crie um changelog para commits dos últimos 7 dias"

**Output**:
```markdown
# Atualizações - Semana de 10 de março de 2024

## ✨ Novos Recursos

- **Espaços de Trabalho em Equipe**: Crie espaços de trabalho separados 
  para diferentes projetos. Convide membros da equipe e mantenha tudo 
  organizado.

- **Atalhos do Teclado**: Pressione ? para ver todos os atalhos disponíveis. 
  Navegue mais rápido sem tocar no mouse.

## 🔧 Melhorias

- **Sincronização Mais Rápida**: Arquivos agora sincronizam 2x mais rápido 
  entre dispositivos
- **Busca Melhorada**: A busca agora inclui o conteúdo dos arquivos, não 
  apenas títulos

## 🐛 Correções

- Corrigido problema em que imagens grandes não carregavam
- Resolvida confusão de fuso horário em posts agendados
- Corrigida contagem de emblema de notificação
```

**Inspirado por:** Caso de uso de Manik Aggarwal do Lenny's Newsletter

## Dicas

- Execute a partir da raiz do seu repositório git
- Especifique intervalos de datas para changelogs focados
- Use seu CHANGELOG_STYLE.md para manter a formatação consistente
- Revise e ajuste o changelog gerado antes de publicar
- Salve o output diretamente em CHANGELOG.md

## Casos de Uso Relacionados

- Criando notas de lançamento do GitHub
- Escrevendo descrições de atualização de app store
- Gerando atualizações por email para usuários
- Criando posts de anúncio em redes sociais