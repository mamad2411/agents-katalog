---
name: crafting-effective-readmes
description: Use when writing or improving README files. Not all READMEs are the same — provides templates and guidance matched to your audience and project type.
---

# Elaborando READMEs Efetivos

## Visão Geral

READMEs respondem perguntas que seu público terá. Diferentes públicos precisam de informações diferentes - um contribuidor de um projeto OSS precisa de contexto diferente do seu eu futuro abrindo uma pasta de configuração.

**Sempre pergunte:** Quem vai ler isso, e o que precisa saber?

## Processo

### Passo 1: Identifique a Tarefa

**Pergunte:** "Qual tarefa de README você está trabalhando?"

| Tarefa | Quando |
|--------|--------|
| **Criar** | Novo projeto, sem README ainda |
| **Adicionar** | Precisa documentar algo novo |
| **Atualizar** | Capacidades mudaram, conteúdo está desatualizado |
| **Revisar** | Verificar se o README ainda está preciso |

### Passo 2: Perguntas Específicas da Tarefa

**Criando README inicial:**
1. Que tipo de projeto? (veja Tipos de Projeto abaixo)
2. Que problema resolve em uma frase?
3. Qual é o caminho mais rápido para "funciona"?
4. Algo notável para destacar?

**Adicionando uma seção:**
1. O que precisa ser documentado?
2. Onde deveria ficar na estrutura existente?
3. Quem mais precisa dessa informação?

**Atualizando conteúdo existente:**
1. O que mudou?
2. Leia o README atual, identifique seções desatualizadas
3. Proponha edições específicas

**Revisando/atualizando:**
1. Leia o README atual
2. Verifique contra o estado real do projeto (package.json, arquivos principais, etc.)
3. Sinalize seções desatualizadas
4. Atualize a data de "Última revisão" se presente

### Passo 3: Sempre Pergunte

Após rascunhar, pergunte: **"Há algo mais para destacar ou incluir que eu possa ter deixado passar?"**

## Tipos de Projeto

| Tipo | Público | Seções-Chave | Template |
|------|---------|--------------|----------|
| **Open Source** | Contribuidores, usuários do mundo todo | Instalação, Uso, Contribuindo, Licença | `templates/oss.md` |
| **Pessoal** | Seu eu futuro, visualizadores de portfólio | O que faz, Stack de tecnologias, Aprendizados | `templates/personal.md` |
| **Interno** | Colegas de time, novos contratados | Setup, Arquitetura, Runbooks | `templates/internal.md` |
| **Config** | Seu eu futuro (confuso) | O que está aqui, Por quê, Como estender, Armadilhas | `templates/xdg-config.md` |

**Pergunte ao usuário** se não estiver claro. Não presuma padrões OSS para tudo.

## Seções Essenciais (Todos os Tipos)

Todo README precisa no mínimo de:

1. **Nome** - Título auto-explicativo
2. **Descrição** - O que + por quê em 1-2 frases
3. **Uso** - Como usá-lo (exemplos ajudam)

## Referências

- `section-checklist.md` - Quais seções incluir por tipo de projeto
- `style-guide.md` - Erros comuns em README e orientação de prosa
- `using-references.md` - Guia para materiais de referência mais profundos