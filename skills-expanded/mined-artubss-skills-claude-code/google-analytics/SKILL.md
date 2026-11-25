---
name: google-analytics
description: Analise dados do Google Analytics, revise métricas de desempenho do site, identifique padrões de tráfego e sugira melhorias orientadas por dados. Use quando o usuário pergunta sobre análise de dados, métricas de site, análise de tráfego, taxas de conversão, comportamento do usuário ou otimização de desempenho.
---

# Análise do Google Analytics

Analise o desempenho do site usando dados do Google Analytics para fornecer insights acionáveis e recomendações de melhoria.

## Início Rápido

### 1. Configurar Autenticação

Esta Skill requer credenciais da API do Google Analytics. Configure as variáveis de ambiente:

```bash
export GOOGLE_ANALYTICS_PROPERTY_ID="your-property-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

Ou crie um arquivo `.env` na raiz do seu projeto:

```env
GOOGLE_ANALYTICS_PROPERTY_ID=123456789
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

**Nunca faça commit de credenciais no controle de versão.** O arquivo JSON da conta de serviço deve ser armazenado com segurança fora do seu repositório.

### 2. Instalar Pacotes Necessários

```bash
# Opção 1: Instalar do arquivo requirements (recomendado)
pip install -r cli-tool/components/skills/analytics/google-analytics/requirements.txt

# Opção 2: Instalar individualmente
pip install google-analytics-data python-dotenv pandas
```

### 3. Analise seu Projeto

Uma vez configurado, posso:
- Revisar métricas atuais de tráfego e comportamento do usuário
- Identificar páginas com melhor e pior desempenho
- Analisar fontes de tráfego e funis de conversão
- Comparar desempenho entre períodos
- Sugerir melhorias orientadas por dados

## Como Usar

Faça-me perguntas como:
- "Revise nosso desempenho no Google Analytics dos últimos 30 dias"
- "Quais são nossas principais fontes de tráfego?"
- "Quais páginas têm as maiores taxas de rejeição?"
- "Analise o engajamento do usuário e sugira melhorias"
- "Compare o desempenho deste mês com o mês passado"

## Fluxo de Análise

Quando você me pedir para analisar dados do Google Analytics, farei:

1. **Conectar à API** usando o script auxiliar
2. **Buscar métricas relevantes** com base em sua pergunta
3. **Analisar os dados** procurando por:
   - Tendências e padrões de tráfego
   - Insights de comportamento do usuário
   - Gargalos de desempenho
   - Oportunidades de conversão
4. **Fornecer recomendações** com:
   - Sugestões de melhoria específicas
   - Nível de prioridade (alto/médio/baixo)
   - Impacto esperado
   - Orientações de implementação

## Métricas Comuns

Para definições detalhadas de métricas e dimensões, consulte [REFERENCE.md](REFERENCE.md).

### Métricas de Tráfego
- Sessões, Usuários, Novos Usuários
- Visualizações de página, Telas por Sessão
- Duração média da sessão

### Métricas de Engajamento
- Taxa de rejeição, Taxa de engajamento
- Contagem de eventos, Conversões
- Profundidade de scroll, Taxa de clique

### Métricas de Aquisição
- Fonte/Meio de tráfego
- Desempenho de campanha
- Agrupamento por canal

### Métricas de Conversão
- Conclusões de objetivo
- Transações de e-commerce
- Taxa de conversão por fonte

## Exemplos de Análise

Para padrões completos de análise e casos de uso, consulte [EXAMPLES.md](EXAMPLES.md).

## Scripts

A Skill inclui scripts utilitários para interação com a API:

### Buscar Desempenho Atual
```bash
python scripts/ga_client.py --days 30 --metrics sessions,users,bounceRate
```

### Analisar e Gerar Relatório
```bash
python scripts/analyze.py --period last-30-days --compare previous-period
```

Os scripts lidam com autenticação da API, busca de dados e análise básica. Interpretarei os resultados e fornecerei recomendações acionáveis.

## Solução de Problemas

**Erro de Autenticação**: Verifique se:
- `GOOGLE_APPLICATION_CREDENTIALS` aponta para um arquivo JSON de conta de serviço válido
- A conta de serviço tem acesso "Visualizador" à sua propriedade GA4
- `GOOGLE_ANALYTICS_PROPERTY_ID` corresponde ao seu ID de propriedade GA4 (não o ID de medição)

**Nenhum Dado Retornado**: Verifique se:
- O ID da propriedade está correto (encontre em GA4 Admin > Configurações da Propriedade)
- O intervalo de datas contém dados
- A conta de serviço recebeu acesso no GA4

**Erros de Importação**: Instale os pacotes necessários:
```bash
pip install google-analytics-data python-dotenv pandas
```

## Notas de Segurança

- **Nunca codifique** credenciais de API ou IDs de propriedade no código
- Armazene arquivos JSON de conta de serviço **fora** do controle de versão
- Use variáveis de ambiente ou arquivos `.env` para configuração
- Adicione `.env` e arquivos de credenciais ao `.gitignore`
- Rotacione chaves de conta de serviço periodicamente
- Use acesso com menor privilégio (somente função Visualizador)

## Privacidade de Dados

Esta Skill acessa apenas dados de análise agregados. Ela não:
- Acessa informações de identificação pessoal (PII)
- Armazena dados de análise persistentemente
- Compartilha dados com serviços externos
- Modifica sua configuração do Google Analytics

Todos os dados são processados localmente e usados apenas para gerar recomendações durante a conversa.