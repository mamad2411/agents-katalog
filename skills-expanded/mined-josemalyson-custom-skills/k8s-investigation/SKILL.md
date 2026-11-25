# K8s + VPS Ultimate Investigation Skill (SRE Pro-Max)

Skill de investigação profunda 360º focada em Root Cause Analysis (RCA), Performance de Kernel, Segurança em Runtime e Pentesting. O Agente deve orquestrar 12 ferramentas de elite (Trivy, K9s, Netdata, Kubeshark, bpftrace, Kubescape, Lynis, Falco, kube-bench, Popeye, kube-hunter, Glances) para compilar um dossiê executivo e técnico irrefutável no formato `html-first`.

Você atuará como um "Agentic Harness", podendo usar a tool `task` para orquestrar Subagents especialistas (SRE, SecOps, PerfOps) em paralelo para auditar todo o ambiente simultaneamente, ou executar você mesmo se o ambiente for menor.

## FASES DE EXECUÇÃO DO WORKFLOW

### FASE 1: Observability & Health (Camada Ops/Node) - SRE Subagent
1. **Glances / Netdata:** Extrair métricas em tempo real do VPS (I/O de disco, CPU steal time, interrupts, network drops).
   - `glances --export json -q --stop-after 5`
2. **Popeye / kubectl:** Escanear "sujeira" e má alocação no cluster (ConfigMaps órfãos, pods sem limits, overcommit, namespaces inativos).
   - `popeye -A -o json --save`
3. **K9s (Contexto):** Como agente, valide eventos problemáticos (CrashLoop, OOMKilled) e instrua o usuário sobre como rastreá-los visualmente.

### FASE 2: Network & Tracing (Camada Perf/Rede) - PerfOps Subagent
1. **Kubeshark:** Analisar o tráfego de rede L7. Identificar latência de API, erros HTTP 5xx ocultos e comunicação entre microserviços.
   - `kubeshark tap -n <namespace> --dump` (se disponível).
2. **bpftrace:** Rastrear gargalos a nível de Kernel (Syscalls lentas, latência de VFS/disco, OOM killers assíncronos no VPS).

### FASE 3: Vulnerability, Compliance & Hardening (Camada Sec Estática) - SecOps Subagent
1. **Trivy:** Scan completo de imagens buscando CVEs Críticos/High rodando nos containers atuais.
2. **Kubescape & kube-bench:** Rodar frameworks NSA, MITRE e CIS Benchmarks. Obter o Score de Compliance do K8s.
3. **Lynis:** Auditoria de Hardening do Sistema Operacional base do VPS.
   - `lynis audit system --quick`

### FASE 4: Active Defense & Runtime Security (Camada Sec Dinâmica) - SecOps Subagent
1. **Falco:** Inspecionar logs de segurança em tempo real se o daemon estiver rodando.
2. **kube-hunter:** Executar um pentest ativo interno no cluster para encontrar portas abertas, serviços expostos e falhas de RBAC (se disponível e autorizado).

---

## ESTRUTURA DO NOVO RELATÓRIO HTML (Obrigatório)

O agente deve gerar um arquivo `/tmp/investigation/ultimate_report.html`. O design **deve utilizar Tabs (Navegação Interna em CSS/JS vanilla)** para acomodar o alto volume de dados sem poluir a tela. O output deve ter aspecto profissional, estilo Datadog / Grafana estático.

**TAB 1: 🚨 EXECUTIVE RCA & HEALTH**
- **Scorecards:** Cluster Health (Popeye), Sec Posture (Kubescape), Node Perf (Glances/Host CPU).
- **Active RCA:** A tabela de correlação cruzando logs do Kubernetes com gargalos de I/O (Glances) ou rede (Kubeshark) para explicar falhas.
- **Overcommit Dashboard:** Barras de progresso com CSS (`width: X%`) mostrando Limits vs Capacity da CPU e Memória.

**TAB 2: 🛡️ THREAT INTELLIGENCE & COMPLIANCE**
- **CVEs & Imagens (Trivy):** Top imagens vulneráveis listadas com `<details>` e `<summary>`.
- **CIS Benchmark (kube-bench) & OS Hardening (Lynis):** Pontos críticos no Linux e no K8s.
- **Pentest Results / Sec Posture:** Vetores de ataque descobertos internamente.

**TAB 3: ⚡ DEEP PERFORMANCE & TRACING**
- **API Latency & Tracing:** Lista de gargalos rastreados por Kubeshark ou bpftrace (ou análise heurística em caso de ausência).
- **Host OS Metrics:** Memória do Host (swap), Zombie processes, Steal Time.

**TAB 4: 🛡️ RUNTIME SECURITY (Opcional)**
- Alertas de processos anômalos detectados rodando dentro dos pods pelo Falco.
- Plano de Ação Estrutural (SRE + SecOps).

### UI/UX Guidelines para o HTML
- Incluir script simples em JS vanilla para alternar as `<div class="tab-content">`.
- Paleta de cores Cyber/Dark (`#0f172a` base).
- Gráficos de barra horizontais puramente em CSS para os scores de compliance.
- Caixas expansíveis (`<details><summary>`) para listas longas de CVEs ou logs de auditoria.
