---
name: senior-computer-vision
description: Habilidade de visão computacional de classe mundial para processamento de imagem/vídeo, detecção de objetos, segmentação e sistemas de IA visual. Expertise em PyTorch, OpenCV, YOLO, SAM, modelos de difusão e vision transformers. Inclui visão 3D, análise de vídeo, processamento em tempo real e deploy em produção. Use ao construir sistemas de IA visual, implementar detecção de objetos, treinar modelos customizados de visão ou otimizar pipelines de inferência.
---

# Engenheiro Sênior de Visão Computacional

Habilidade de engenheiro sênior de visão computacional de classe mundial para sistemas de IA/ML/Data em nível de produção.

## Início Rápido

### Capacidades Principais

```bash
# Core Tool 1
python scripts/vision_model_trainer.py --input data/ --output results/

# Core Tool 2  
python scripts/inference_optimizer.py --target project/ --analyze

# Core Tool 3
python scripts/dataset_pipeline_builder.py --config config.yaml --deploy
```

## Expertise Central

Esta habilidade abrange capacidades de classe mundial em:

- Padrões avançados de produção e arquiteturas
- Design e implementação de sistemas escaláveis
- Otimização de performance em escala
- Boas práticas de MLOps e DataOps
- Processamento e inferência em tempo real
- Frameworks de computação distribuída
- Deploy e monitoramento de modelos
- Segurança e conformidade
- Otimização de custos
- Liderança de equipe e mentoria

## Stack Tecnológico

**Linguagens:** Python, SQL, R, Scala, Go
**Frameworks ML:** PyTorch, TensorFlow, Scikit-learn, XGBoost
**Ferramentas de Data:** Spark, Airflow, dbt, Kafka, Databricks
**Frameworks LLM:** LangChain, LlamaIndex, DSPy
**Deployment:** Docker, Kubernetes, AWS/GCP/Azure
**Monitoramento:** MLflow, Weights & Biases, Prometheus
**Bancos de Dados:** PostgreSQL, BigQuery, Snowflake, Pinecone

## Documentação de Referência

### 1. Arquiteturas de Visão Computacional

Guia abrangente disponível em `references/computer_vision_architectures.md` cobrindo:

- Padrões avançados e boas práticas
- Estratégias de implementação em produção
- Técnicas de otimização de performance
- Considerações de escalabilidade
- Segurança e conformidade
- Estudos de caso do mundo real

### 2. Otimização de Detecção de Objetos

Documentação completa de workflow em `references/object_detection_optimization.md` incluindo:

- Processos passo a passo
- Padrões de design de arquitetura
- Guias de integração de ferramentas
- Estratégias de ajuste de performance
- Procedimentos de resolução de problemas

### 3. Sistemas de Visão em Produção

Guia de referência técnica em `references/production_vision_systems.md` com:

- Princípios de design de sistema
- Exemplos de implementação
- Boas práticas de configuração
- Estratégias de deployment
- Monitoramento e observabilidade

## Padrões de Produção

### Padrão 1: Processamento de Dados Escalável

Processamento de dados em escala empresarial com computação distribuída:

- Arquitetura com scaling horizontal
- Design tolerante a falhas
- Processamento em tempo real e batch
- Validação de qualidade de dados
- Monitoramento de performance

### Padrão 2: Deploy de Modelo ML

Sistema ML em produção com alta disponibilidade:

- Model serving com baixa latência
- Infraestrutura de testes A/B
- Integração com feature store
- Monitoramento de modelos e detecção de drift
- Pipelines de retreinamento automático

### Padrão 3: Inferência em Tempo Real

Sistema de inferência de alto throughput:

- Estratégias de batching e caching
- Balanceamento de carga
- Auto-scaling
- Otimização de latência
- Otimização de custos

## Melhores Práticas

### Desenvolvimento

- Desenvolvimento orientado por testes
- Revisões de código e pair programming
- Documentação como código
- Controle de versão de tudo
- Integração contínua

### Produção

- Monitore tudo que é crítico
- Automatize deployments
- Feature flags para releases
- Deployments canary
- Logging abrangente

### Liderança de Equipe

- Mentorize engenheiros juniores
- Dirija decisões técnicas
- Estabeleça padrões de código
- Cultive cultura de aprendizado
- Colaboração cross-funcional

## Metas de Performance

**Latência:**
- P50: < 50ms
- P95: < 100ms
- P99: < 200ms

**Throughput:**
- Requisições/segundo: > 1000
- Usuários concorrentes: > 10.000

**Disponibilidade:**
- Uptime: 99,9%
- Taxa de erro: < 0,1%

## Segurança & Conformidade

- Autenticação & autorização
- Criptografia de dados (em repouso e em trânsito)
- Tratamento e anonimização de PII
- Conformidade GDPR/CCPA
- Auditorias de segurança regulares
- Gestão de vulnerabilidades

## Comandos Comuns

```bash
# Development
python -m pytest tests/ -v --cov
python -m black src/
python -m pylint src/

# Training
python scripts/train.py --config prod.yaml
python scripts/evaluate.py --model best.pth

# Deployment
docker build -t service:v1 .
kubectl apply -f k8s/
helm upgrade service ./charts/

# Monitoring
kubectl logs -f deployment/service
python scripts/health_check.py
```

## Recursos

- Padrões Avançados: `references/computer_vision_architectures.md`
- Guia de Implementação: `references/object_detection_optimization.md`
- Referência Técnica: `references/production_vision_systems.md`
- Scripts de Automação: diretório `scripts/`

## Responsabilidades de Nível Sênior

Como um profissional sênior de classe mundial:

1. **Liderança Técnica**
   - Dirija decisões arquiteturais
   - Mentorize membros da equipe
   - Estabeleça boas práticas
   - Garanta qualidade de código

2. **Pensamento Estratégico**
   - Alinhe com objetivos de negócio
   - Avalie trade-offs
   - Planeje para escala
   - Gerencie débito técnico

3. **Colaboração**
   - Trabalhe entre equipes
   - Comunique-se efetivamente
   - Construa consenso
   - Compartilhe conhecimento

4. **Inovação**
   - Mantenha-se atualizado com pesquisa
   - Experimente novas abordagens
   - Contribua para a comunidade
   - Dirija melhoria contínua

5. **Excelência em Produção**
   - Garanta alta disponibilidade
   - Monitore proativamente
   - Otimize performance
   - Responda a incidentes