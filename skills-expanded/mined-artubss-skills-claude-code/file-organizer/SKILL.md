---
name: file-organizer
description: Organiza arquivos e pastas de forma inteligente, compreendendo contexto, encontrando duplicatas e sugerindo estruturas organizacionais melhores. Use quando o usuário quiser limpar diretórios, organizar downloads, remover duplicatas ou reestruturar projetos.
---

# Organizador de Arquivos

## Quando Usar Esta Habilidade

- Sua pasta Downloads é um caos total
- Você não consegue encontrar arquivos porque estão espalhados por todos os lugares
- Você tem arquivos duplicados ocupando espaço
- Sua estrutura de pastas não faz mais sentido
- Você quer estabelecer melhores hábitos de organização
- Você está iniciando um novo projeto e precisa de uma boa estrutura
- Você está limpando antes de arquivar projetos antigos

## O Que Esta Habilidade Faz

1. **Analisa Estrutura Atual**: Revisa suas pastas e arquivos para entender o que você tem
2. **Encontra Duplicatas**: Identifica arquivos duplicados em seu sistema
3. **Sugere Organização**: Propõe estruturas de pastas lógicas com base no seu conteúdo
4. **Automatiza Limpeza**: Move, renomeia e organiza arquivos com sua aprovação
5. **Mantém Contexto**: Toma decisões inteligentes com base em tipos de arquivo, datas e conteúdo
6. **Reduz Desordem**: Identifica arquivos antigos que você provavelmente não precisa mais

## Instruções

Quando um usuário solicita ajuda na organização de arquivos:

1. **Entenda o Escopo**

   Faça perguntas de esclarecimento:

   - Qual diretório precisa de organização? (Downloads, Documentos, pasta pessoal inteira?)
   - Qual é o principal problema? (Não consegue encontrar coisas, duplicatas, muito bagunçado, sem estrutura?)
   - Há arquivos ou pastas a evitar? (Projetos atuais, dados sensíveis?)
   - Qual intensidade de organização? (Conservadora vs. limpeza abrangente)

2. **Analise o Estado Atual**

   Revise o diretório de destino:

   ```bash
   # Obter visão geral da estrutura atual
   ls -la [target_directory]

   # Verificar tipos e tamanhos de arquivo
   find [target_directory] -type f -exec file {} \; | head -20

   # Identificar os maiores arquivos
   du -sh [target_directory]/* | sort -rh | head -20

   # Contar tipos de arquivo
   find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
   ```

   Resuma os achados:

   - Total de arquivos e pastas
   - Decomposição por tipo de arquivo
   - Distribuição de tamanho
   - Intervalos de data
   - Problemas óbvios de organização

3. **Identifique Padrões de Organização**

   Com base nos arquivos, determine agrupamentos lógicos:

   **Por Tipo**:

   - Documentos (PDFs, DOCX, TXT)
   - Imagens (JPG, PNG, SVG)
   - Vídeos (MP4, MOV)
   - Arquivos compactados (ZIP, TAR, DMG)
   - Código/Projetos (diretórios com código)
   - Planilhas (XLSX, CSV)
   - Apresentações (PPTX, KEY)

   **Por Propósito**:

   - Trabalho vs. Pessoal
   - Ativo vs. Arquivo
   - Específico do projeto
   - Materiais de referência
   - Arquivos temporários/rascunho

   **Por Data**:

   - Ano/mês atual
   - Anos anteriores
   - Muito antigo (candidatos a arquivo)

4. **Encontre Duplicatas**

   Quando solicitado, procure por duplicatas:

   ```bash
   # Encontrar duplicatas exatas por hash
   find [directory] -type f -exec md5 {} \; | sort | uniq -d

   # Encontrar arquivos com nomes semelhantes
   find [directory] -type f -printf '%f\n' | sort | uniq -d

   # Encontrar arquivos com tamanho similar
   find [directory] -type f -printf '%s %p\n' | sort -n
   ```

   Para cada conjunto de duplicatas:

   - Mostre todos os caminhos de arquivo
   - Exiba tamanhos e datas de modificação
   - Recomende qual manter (geralmente o mais novo ou melhor nomeado)
   - **Importante**: Sempre peça confirmação antes de deletar

5. **Proponha Plano de Organização**

   Apresente um plano claro antes de fazer alterações:

   ```markdown
   # Plano de Organização para [Diretório]

   ## Estado Atual

   - X arquivos em Y pastas
   - [Tamanho] total
   - Tipos de arquivo: [decomposição]
   - Problemas: [listar problemas]

   ## Estrutura Proposta

   [Diretório]/
   ├── Trabalho/
   │ ├── Projetos/
   │ ├── Documentos/
   │ └── Arquivo/
   ├── Pessoal/
   │ ├── Fotos/
   │ ├── Documentos/
   │ └── Mídia/
   └── Downloads/
   ├── Para-Organizar/
   └── Arquivo/

   ## Mudanças que Farei

   1. **Criar novas pastas**: [listar]
   2. **Mover arquivos**:
      - X PDFs → Trabalho/Documentos/
      - Y imagens → Pessoal/Fotos/
      - Z arquivos antigos → Arquivo/
   3. **Renomear arquivos**: [quaisquer padrões de renomeação]
   4. **Deletar**: [duplicatas ou arquivos de lixo]

   ## Arquivos Que Precisam Sua Decisão

   - [Listar qualquer arquivo que você não tem certeza]

   Pronto para prosseguir? (sim/não/modificar)
   ```

6. **Execute a Organização**

   Após aprovação, organize sistematicamente:

   ```bash
   # Criar estrutura de pastas
   mkdir -p "path/to/new/folders"

   # Mover arquivos com logging claro
   mv "old/path/file.pdf" "new/path/file.pdf"

   # Renomear arquivos com padrões consistentes
   # Exemplo: "AAAA-MM-DD - Descrição.ext"
   ```

   **Regras Importantes**:

   - Sempre confirme antes de deletar qualquer coisa
   - Registre todos os movimentos para possível desfazer
   - Preserve datas originais de modificação
   - Lide com conflitos de nome de arquivo graciosamente
   - Pare e pergunte se encontrar situações inesperadas

7. **Forneça Resumo e Dicas de Manutenção**

   Após organizar:

   ```markdown
   # Organização Completa! ✨

   ## O Que Mudou

   - Criadas [X] novas pastas
   - Organizados [Y] arquivos
   - Liberados [Z] GB removendo duplicatas
   - Arquivados [W] arquivos antigos

   ## Nova Estrutura

   [Mostrar a nova árvore de pastas]

   ## Dicas de Manutenção

   Para manter isto organizado:

   1. **Semanalmente**: Organizar novos downloads
   2. **Mensalmente**: Revisar e arquivar projetos concluídos
   3. **Trimestralmente**: Verificar novas duplicatas
   4. **Anualmente**: Arquivar arquivos antigos

   ## Comandos Rápidos para Você

   # Encontrar arquivos modificados esta semana

   find . -type f -mtime -7

   # Organizar downloads por tipo

   [comando personalizado para sua configuração]

   # Encontrar duplicatas

   [comando personalizado]
   ```

   Quer organizar outra pasta?

## Melhores Práticas

### Nomenclatura de Pastas

- Use nomes claros e descritivos
- Evite espaços (use hífens ou underscores)
- Seja específico: "propostas-cliente" em vez de "docs"
- Use prefixos para ordenação: "01-atual", "02-arquivo"

### Nomenclatura de Arquivos

- Inclua datas: "2024-10-17-notas-reuniao.md"
- Seja descritivo: "relatorio-financeiro-q3.xlsx"
- Evite números de versão em nomes (use controle de versão em vez disso)
- Remova artefatos de download: "documento-final-v2 (1).pdf" → "documento.pdf"

### Quando Arquivar

- Projetos não tocados há 6+ meses
- Trabalho concluído que pode ser consultado depois
- Versões antigas após migração para novos sistemas
- Arquivos dos quais você está hesitante em deletar (arquive primeiro)