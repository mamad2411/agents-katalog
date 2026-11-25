---
name: github-workflow-automation
description: "Automatize workflows do GitHub com assistência de IA. Inclui reviews de PR, triagem de issues, integração CI/CD e operações Git. Use ao automatizar workflows do GitHub, configurar automação de review de PR, criar GitHub Actions ou fazer triagem de issues."
---

# 🔧 Automação de Workflows do GitHub

> Padrões para automatizar workflows do GitHub com assistência de IA, inspirados em [Gemini CLI](https://github.com/google-gemini/gemini-cli) e práticas modernas de DevOps.

## Quando Usar Esta Habilidade

Use esta habilidade quando:

- Automatizar reviews de PR com IA
- Configurar automação de triagem de issues
- Criar workflows do GitHub Actions
- Integrar IA em pipelines CI/CD
- Automatizar operações Git (rebases, cherry-picks)

---

## 1. PR Review Automatizado

### 1.1 Ação de Review de PR

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          echo "files<<EOF" >> $GITHUB_OUTPUT
          echo "$files" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Get diff
        id: diff
        run: |
          diff=$(git diff origin/${{ github.base_ref }}...HEAD)
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          echo "$diff" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Review
        uses: actions/github-script@v7
        with:
          script: |
            const { Anthropic } = require('@anthropic-ai/sdk');
            const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

            const response = await client.messages.create({
              model: "claude-3-sonnet-20240229",
              max_tokens: 4096,
              messages: [{
                role: "user",
                content: `Review this PR diff and provide feedback:
                
                Changed files: ${{ steps.changed.outputs.files }}
                
                Diff:
                ${{ steps.diff.outputs.diff }}
                
                Provide:
                1. Summary of changes
                2. Potential issues or bugs
                3. Suggestions for improvement
                4. Security concerns if any
                
                Format as GitHub markdown.`
              }]
            });

            await github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: response.content[0].text,
              event: 'COMMENT'
            });
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 1.2 Padrões de Comentário de Review

````markdown
# Estrutura de Review de IA

## 📋 Resumo

Breve descrição do que este PR faz.

## ✅ O que está bom

- Código bem estruturado
- Boa cobertura de testes
- Convenções de nomenclatura claras

## ⚠️ Possíveis Problemas

1. **Linha 42**: Possível exceção de null pointer
   ```javascript
   // Atual
   user.profile.name;
   // Sugerido
   user?.profile?.name ?? "Unknown";
   ```
````

2. **Linha 78**: Considere tratamento de erros
   ```javascript
   // Adicione try-catch ou .catch()
   ```

## 💡 Sugestões

- Considere extrair a lógica de validação para uma função separada
- Adicione comentários JSDoc para métodos públicos

## 🔒 Notas de Segurança

- Nenhuma exposição de dados sensíveis detectada
- Tratamento de chave de API parece correto

````

### 1.3 Reviews Focados

```yaml
# Review apenas tipos de arquivo específicos
- name: Filter code files
  run: |
    files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | \
            grep -E '\.(ts|tsx|js|jsx|py|go)$' || true)
    echo "code_files=$files" >> $GITHUB_OUTPUT

# Review com contexto
- name: AI Review with context
  run: |
    # Inclua arquivos de contexto relevantes
    context=""
    for file in ${{ steps.changed.outputs.files }}; do
      if [[ -f "$file" ]]; then
        context+="=== $file ===\n$(cat $file)\n\n"
      fi
    done

    # Envie para IA com contexto de arquivo completo
````

---

## 2. Automação de Triagem de Issues

### 2.1 Auto-etiquetagem de Issues

```yaml
# .github/workflows/issue-triage.yml
name: Issue Triage

on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - name: Analyze issue
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;

            // Chame IA para analisar
            const analysis = await analyzeIssue(issue.title, issue.body);

            // Aplique etiquetas
            const labels = [];

            if (analysis.type === 'bug') {
              labels.push('bug');
              if (analysis.severity === 'high') labels.push('priority: high');
            } else if (analysis.type === 'feature') {
              labels.push('enhancement');
            } else if (analysis.type === 'question') {
              labels.push('question');
            }

            if (analysis.area) {
              labels.push(`area: ${analysis.area}`);
            }

            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              labels: labels
            });

            // Adicione resposta inicial
            if (analysis.type === 'bug' && !analysis.hasReproSteps) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: `Obrigado por reportar este issue!

Para nos ajudar na investigação, você poderia fornecer:
- Passos para reproduzir o problema
- Comportamento esperado
- Comportamento atual
- Ambiente (SO, versão, etc.)

Isso nos ajudará a resolver seu issue mais rapidamente. 🙏`
              });
            }
```

### 2.2 Prompt de Análise de Issue

```typescript
const TRIAGE_PROMPT = `
Analise este issue do GitHub e classifique:

Título: {title}
Corpo: {body}

Retorne JSON com:
{
  "type": "bug" | "feature" | "question" | "docs" | "other",
  "severity": "low" | "medium" | "high" | "critical",
  "area": "frontend" | "backend" | "api" | "docs" | "ci" | "other",
  "summary": "resumo de uma linha",
  "hasReproSteps": boolean,
  "isFirstContribution": boolean,
  "suggestedLabels": ["label1", "label2"],
  "suggestedAssignees": ["username"] // baseado em expertise da área
}
`;
```

### 2.3 Gestão de Issues Obsoletos

```yaml
# .github/workflows/stale.yml
name: Manage Stale Issues

on:
  schedule:
    - cron: "0 0 * * *" # Diariamente

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: |
            Este issue foi marcado automaticamente como obsoleto por não ter 
            tido atividade recente. Será fechado em 14 dias se não houver 
            mais atividade.

            Se este issue ainda é relevante:
            - Adicione um comentário com uma atualização
            - Remova a etiqueta `stale`

            Obrigado pelas suas contribuições! 🙏

          stale-pr-message: |
            Este PR foi marcado automaticamente como obsoleto. Atualize-o 
            ou será fechado em 14 dias.

          days-before-stale: 60
          days-before-close: 14
          stale-issue-label: "stale"
          stale-pr-label: "stale"
          exempt-issue-labels: "pinned,security,in-progress"
          exempt-pr-labels: "pinned,security"
```

---

## 3. Integração CI/CD

### 3.1 Seleção Inteligente de Testes

```yaml
# .github/workflows/smart-tests.yml
name: Smart Test Selection

on:
  pull_request:

jobs:
  analyze:
    runs-on: ubuntu-latest
    outputs:
      test_suites: ${{ steps.analyze.outputs.suites }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze changes
        id: analyze
        run: |
          # Obtenha arquivos alterados
          changed=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)

          # Determine quais suites de testes executar
          suites="[]"

          if echo "$changed" | grep -q "^src/api/"; then
            suites=$(echo $suites | jq '. + ["api"]')
          fi

          if echo "$changed" | grep -q "^src/frontend/"; then
            suites=$(echo $suites | jq '. + ["frontend"]')
          fi

          if echo "$changed" | grep -q "^src/database/"; then
            suites=$(echo $suites | jq '. + ["database", "api"]')
          fi

          # Se nada específico, execute tudo
          if [ "$suites" = "[]" ]; then
            suites='["all"]'
          fi

          echo "suites=$suites" >> $GITHUB_OUTPUT

  test:
    needs: analyze
    runs-on: ubuntu-latest
    strategy:
      matrix:
        suite: ${{ fromJson(needs.analyze.outputs.test_suites) }}

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: |
          if [ "${{ matrix.suite }}" = "all" ]; then
            npm test
          else
            npm test -- --suite ${{ matrix.suite }}
          fi
```

### 3.2 Deploy com Validação de IA

```yaml
# .github/workflows/deploy.yml
name: Deploy with AI Validation

on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get deployment changes
        id: changes
        run: |
          # Obtenha commits desde o último deploy
          last_deploy=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
          if [ -n "$last_deploy" ]; then
            changes=$(git log --oneline $last_deploy..HEAD)
          else
            changes=$(git log --oneline -10)
          fi
          echo "changes<<EOF" >> $GITHUB_OUTPUT
          echo "$changes" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Risk Assessment
        id: assess
        uses: actions/github-script@v7
        with:
          script: |
            // Analise mudanças para risco de deploy
            const prompt = `
            Analise estas mudanças para risco de deploy:

            ${process.env.CHANGES}

            Retorne JSON:
            {
              "riskLevel": "low" | "medium" | "high",
              "concerns": ["concern1", "concern2"],
              "recommendations": ["rec1", "rec2"],
              "requiresManualApproval": boolean
            }
            `;

            // Chame IA e analise resposta
            const analysis = await callAI(prompt);

            if (analysis.riskLevel === 'high') {
              core.setFailed('Deploy de alto risco detectado. Revisão manual necessária.');
            }

            return analysis;
        env:
          CHANGES: ${{ steps.changes.outputs.changes }}

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        run: |
          echo "Implantando em produção..."
          # Comandos de deploy aqui
```

### 3.3 Automação de Rollback

```yaml
# .github/workflows/rollback.yml
name: Automated Rollback

on:
  workflow_dispatch:
    inputs:
      reason:
        description: "Motivo do rollback"
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find last stable version
        id: stable
        run: |
          # Encontre o último deploy bem-sucedido
          stable=$(git tag -l 'v*' --sort=-version:refname | head -1)
          echo "version=$stable" >> $GITHUB_OUTPUT

      - name: Rollback
        run: |
          git checkout ${{ steps.stable.outputs.version }}
          # Implante versão estável
          npm run deploy

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🔄 Production rolled back to ${{ steps.stable.outputs.version }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Rollback executado*\n• Versão: `${{ steps.stable.outputs.version }}`\n• Motivo: ${{ inputs.reason }}\n• Acionado por: ${{ github.actor }}"
                  }
                }
              ]
            }
```

---

## 4. Operações Git

### 4.1 Rebase Automatizado

```yaml
# .github/workflows/auto-rebase.yml
name: Auto Rebase

on:
  issue_comment:
    types: [created]

jobs:
  rebase:
    if: github.event.issue.pull_request && contains(github.event.comment.body, '/rebase')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Rebase PR
        run: |
          # Busque branch do PR
          gh pr checkout ${{ github.event.issue.number }}

          # Faça rebase em main
          git fetch origin main
          git rebase origin/main

          # Force push
          git push --force-with-lease
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Comment result
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '✅ Rebase em main realizado com sucesso!'
            })
```

### 4.2 Smart Cherry-Pick

```typescript
// Cherry-pick assistido por IA que lida com conflitos
async function smartCherryPick(commitHash: string, targetBranch: string) {
  // Obtenha informações do commit
  const commitInfo = await exec(`git show ${commitHash} --stat`);

  // Verifique possíveis conflitos
  const targetDiff = await exec(
    `git diff ${targetBranch}...HEAD -- ${affectedFiles}`
  );

  // Análise de IA
  const analysis = await ai.analyze(`
    Preciso fazer cherry-pick deste commit para ${targetBranch}:
    
    ${commitInfo}
    
    Estado atual dos arquivos afetados em ${targetBranch}:
    ${targetDiff}
    
    Haverá conflitos? Se sim, sugira estratégia de resolução.
  `);

  if (analysis.willConflict) {
    // Crie branch para resolução manual
    await exec(
      `git checkout -b cherry-pick-${commitHash.slice(0, 7)} ${targetBranch}`
    );
    const result = await exec(`git cherry-pick ${commitHash}`, {
      allowFail: true,
    });

    if (result.failed) {
      // Resolução de conflito assistida por IA
      const conflicts = await getConflicts();
      for (const conflict of conflicts) {
        const resolution = await ai.resolveConflict(conflict);
        await applyResolution(conflict.file, resolution);
      }
    }
  } else {
    await exec(`git checkout ${targetBranch}`);
    await exec(`git cherry-pick ${commitHash}`);
  }
}
```

### 4.3 Limpeza de Branch

```yaml
# .github/workflows/branch-cleanup.yml
name: Branch Cleanup

on:
  schedule:
    - cron: '0 0 * * 0'  # Semanal
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find stale branches
        id: stale
        run: |
          # Branches não atualizados em 30 dias
          stale=$(git for-each-ref --sort=-committerdate refs/remotes/origin \
            --format='%(refname:short) %(committerdate:relative)' | \
            grep -E '[3-9][0-9]+ days|[0-9]+ months|[0-9]+ years' | \
            grep -v 'origin/main\|origin/develop' | \
            cut -d' ' -f1 | sed 's|origin/||')

          echo "branches<<EOF" >> $GITHUB_OUTPUT
          echo "$stale" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create cleanup PR
        if: steps.stale.outputs.branches != ''
        uses: actions/github-script@v7
        with:
          script: |
            const branches = `${{ steps.stale.outputs.branches }}`.split('\n').filter(Boolean);

            const body = `## 🧹 Limpeza de Branches Obsoletos

Os seguintes branches não foram atualizados há mais de 30 dias:

${branches.map(b => `- \`${b}\``).join('\n')}

### Ações:
- [ ] Revise cada branch
- [ ] Delete branches que não são mais necessários
- Comente \`/keep branch-name\` para preservar branches específicos
`;

            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Limpeza de Branches Obsoletos',
              body: body,
              labels: ['housekeeping']
            });
```

---

## 5. Assistência sob Demanda

### 5.1 Bot @mention

```yaml
# .github/workflows/mention-bot.yml
name: AI Mention Bot

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  respond:
    if: contains(github.event.comment.body, '@ai-helper')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Extract question
        id: question
        run: |
          # Extraia texto após @ai-helper
          question=$(echo "${{ github.event.comment.body }}" | sed 's/.*@ai-helper//')
          echo "question=$question" >> $GITHUB_OUTPUT

      - name: Get context
        id: context
        run: |
          if [ "${{ github.event.issue.pull_request }}" != "" ]; then
            # É um PR - obtenha diff
            gh pr diff ${{ github.event.issue.number }} > context.txt
          else
            # É um issue - obtenha descrição
            gh issue view ${{ github.event.issue.number }} --json body -q .body > context.txt
          fi
          echo "context=$(cat context.txt)" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: AI Response
        uses: actions/github-script@v7
        with:
          script: |
            const response = await ai.chat(`
              Contexto: ${process.env.CONTEXT}
              
              Pergunta: ${process.env.QUESTION}
              
              Forneça uma resposta útil e específica. Inclua exemplos de código se relevante.
            `);

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: response
            });
        env:
          CONTEXT: ${{ steps.context.outputs.context }}
          QUESTION: ${{ steps.question.outputs.question }}
```

### 5.2 Padrões de Comando

```markdown
## Comandos Disponíveis

| Comando              | Descrição                          |
| :------------------- | :--------------------------------- |
| `@ai-helper explain` | Explique o código neste PR         |
| `@ai-helper review`  | Solicite review de código de IA    |
| `@ai-helper fix`     | Sugira correções para problemas    |
| `@ai-helper test`    | Gere casos de teste                |
| `@ai-helper docs`    | Gere documentação                  |
| `/rebase`            | Faça rebase de PR em main          |
| `/update`            | Atualize branch de PR desde main   |
| `/approve`           | Marque como aprovado por bot       |
| `/label bug`         | Adicione etiqueta 'bug'            |
| `/assign @user`      | Atribua a usuário                  |
```

---

## 6. Configuração de Repositório

### 6.1 CODEOWNERS

```
# .github/CODEOWNERS

# Proprietários globais
* @org/core-team

# Frontend
/src/frontend/ @org/frontend-team
*.tsx @org/frontend-team
*.css @org/frontend-team

# Backend
/src/api/ @org/backend-team
/src/database/ @org/backend-team

# Infraestrutura
/.github/ @org/devops-team
/terraform/ @org/devops-team
Dockerfile @org/devops-team

# Docs
/docs/ @org/docs-team
*.md @org/docs-team

# Sensível a segurança
/src/auth/ @org/security-team
/src/crypto/ @org/security-team
```

### 6.2 Proteção de Branch

```yaml
# Configure via GitHub API
- name: Configure branch protection
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.repos.updateBranchProtection({
        owner: context.repo.owner,
        repo: context.repo.repo,
        branch: 'main',
        required_status_checks: {
          strict: true,
          contexts: ['test', 'lint', 'ai-review']
        },
        enforce_admins: true,
        required_pull_request_reviews: {
          required_approving_review_count: 1,
          require_code_owner_reviews: true,
          dismiss_stale_reviews: true
        },
        restrictions: null,
        required_linear_history: true,
        allow_force_pushes: false,
        allow_deletions: false
      });
```

---

## Melhores Práticas

### Segurança

- [ ] Armazene chaves de API em GitHub Secrets
- [ ] Use permissões mínimas em workflows
- [ ] Valide todos os inputs
- [ ] Não exponha dados sensíveis em logs

### Desempenho

- [ ] Cache dependências
- [ ] Use builds em matriz para testes paralelos
- [ ] Pule jobs desnecessários com path filters
- [ ] Use runners self-hosted para workloads pesados

### Confiabilidade

- [ ] Adicione timeouts para jobs
- [ ] Trate rate limits graciosamente
- [ ] Implemente lógica de retry
- [ ] Tenha procedimentos de rollback

---

## Recursos

- [Gemini CLI GitHub Action](https://github.com/google-github-actions/run-gemini-cli)
- [Documentação do GitHub Actions](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)
- [Sintaxe CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)