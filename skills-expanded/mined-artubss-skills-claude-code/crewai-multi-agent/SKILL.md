---
name: crewai-multi-agent
description: Framework de orquestração multi-agent para colaboração autônoma de IA. Use ao construir equipes de agentes especializados trabalhando juntos em tarefas complexas, quando você precisa de colaboração de agentes baseada em papéis com memória, ou para workflows em produção exigindo execução sequencial/hierárquica. Construído sem dependências de LangChain para execução enxuta e rápida.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Agents, CrewAI, Multi-Agent, Orchestration, Collaboration, Role-Based, Autonomous, Workflows, Memory, Production]
dependencies: [crewai>=1.2.0, crewai-tools>=1.2.0]
---

# CrewAI - Framework de Orquestração Multi-Agent

Construa equipes de agentes de IA autônomos que colaboram para resolver tarefas complexas.

## Quando usar CrewAI

**Use CrewAI quando:**
- Construir sistemas multi-agent com papéis especializados
- Precisar de colaboração autônoma entre agentes
- Quiser delegação de tarefas baseada em papéis (pesquisador, escritor, analista)
- Exigir execução de processo sequencial ou hierárquico
- Construir workflows em produção com memória e observabilidade
- Precisar de configuração mais simples que LangChain/LangGraph

**Principais características:**
- **Independente**: Sem dependências de LangChain, footprint enxuto
- **Baseado em papéis**: Agentes têm papéis, objetivos e históricos
- **Duplo paradigma**: Crews (autônomas) + Flows (event-driven)
- **50+ ferramentas**: Web scraping, busca, bancos de dados, serviços de IA
- **Memória**: Memória de curto prazo, longo prazo e de entidades
- **Pronto para produção**: Tracing, recursos corporativos

**Use alternativas em vez disso:**
- **LangChain**: Apps LLM de propósito geral, pipelines RAG
- **LangGraph**: Workflows complexos com estado e ciclos
- **AutoGen**: Ecossistema Microsoft, conversas multi-agent
- **LlamaIndex**: Q&A de documentos, recuperação de conhecimento

## Início rápido

### Instalação

```bash
# Framework principal
pip install crewai

# Com 50+ ferramentas built-in
pip install 'crewai[tools]'
```

### Criar projeto com CLI

```bash
# Criar novo projeto crew
crewai create crew my_project
cd my_project

# Instalar dependências
crewai install

# Executar o crew
crewai run
```

### Crew simples (somente código)

```python
from crewai import Agent, Task, Crew, Process

# 1. Definir agentes
researcher = Agent(
    role="Senior Research Analyst",
    goal="Discover cutting-edge developments in AI",
    backstory="You are an expert analyst with a keen eye for emerging trends.",
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, engaging content about technical topics",
    backstory="You excel at explaining complex concepts to general audiences.",
    verbose=True
)

# 2. Definir tarefas
research_task = Task(
    description="Research the latest developments in {topic}. Find 5 key trends.",
    expected_output="A detailed report with 5 bullet points on key trends.",
    agent=researcher
)

write_task = Task(
    description="Write a blog post based on the research findings.",
    expected_output="A 500-word blog post in markdown format.",
    agent=writer,
    context=[research_task]  # Uses research output
)

# 3. Criar e executar crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Tasks run in order
    verbose=True
)

# 4. Executar
result = crew.kickoff(inputs={"topic": "AI Agents"})
print(result.raw)
```

## Conceitos principais

### Agentes - Trabalhadores autônomos

```python
from crewai import Agent

agent = Agent(
    role="Data Scientist",                    # Job title/role
    goal="Analyze data to find insights",     # What they aim to achieve
    backstory="PhD in statistics...",         # Background context
    llm="gpt-4o",                             # LLM to use
    tools=[],                                 # Tools available
    memory=True,                              # Enable memory
    verbose=True,                             # Show reasoning
    allow_delegation=True,                    # Can delegate to others
    max_iter=15,                              # Max reasoning iterations
    max_rpm=10                                # Rate limit
)
```

### Tarefas - Unidades de trabalho

```python
from crewai import Task

task = Task(
    description="Analyze the sales data for Q4 2024. {context}",
    expected_output="A summary report with key metrics and trends.",
    agent=analyst,                            # Assigned agent
    context=[previous_task],                  # Input from other tasks
    output_file="report.md",                  # Save to file
    async_execution=False,                    # Run synchronously
    human_input=False                         # No human approval needed
)
```

### Crews - Equipes de agentes

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],      # Team members
    tasks=[research, write, edit],            # Tasks to complete
    process=Process.sequential,               # Or Process.hierarchical
    verbose=True,
    memory=True,                              # Enable crew memory
    cache=True,                               # Cache tool results
    max_rpm=10,                               # Rate limit
    share_crew=False                          # Opt-in telemetry
)

# Executar com inputs
result = crew.kickoff(inputs={"topic": "AI trends"})

# Acessar resultados
print(result.raw)                             # Final output
print(result.tasks_output)                    # All task outputs
print(result.token_usage)                     # Token consumption
```

## Tipos de processo

### Sequencial (padrão)

As tarefas são executadas em ordem, cada agente completando sua tarefa antes da próxima:

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Task 1 → Task 2 → Task 3
)
```

### Hierárquico

Auto-cria um agente gerenciador que delega e coordena:

```python
crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analyze_task],
    process=Process.hierarchical,  # Manager delegates tasks
    manager_llm="gpt-4o"           # LLM for manager
)
```

## Usando ferramentas

### Ferramentas built-in (50+)

```bash
pip install 'crewai[tools]'
```

```python
from crewai_tools import (
    SerperDevTool,           # Web search
    ScrapeWebsiteTool,       # Web scraping
    FileReadTool,            # Read files
    PDFSearchTool,           # Search PDFs
    WebsiteSearchTool,       # Search websites
    CodeDocsSearchTool,      # Search code docs
    YoutubeVideoSearchTool,  # Search YouTube
)

# Atribuir ferramentas ao agente
researcher = Agent(
    role="Researcher",
    goal="Find accurate information",
    backstory="Expert at finding data online.",
    tools=[SerperDevTool(), ScrapeWebsiteTool()]
)
```

### Ferramentas customizadas

```python
from crewai.tools import BaseTool
from pydantic import Field

class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "Performs mathematical calculations. Input: expression"

    def _run(self, expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

# Usar ferramenta customizada
agent = Agent(
    role="Analyst",
    goal="Perform calculations",
    tools=[CalculatorTool()]
)
```

## Configuração em YAML (recomendado)

### Estrutura do projeto

```
my_project/
├── src/my_project/
│   ├── config/
│   │   ├── agents.yaml    # Agent definitions
│   │   └── tasks.yaml     # Task definitions
│   ├── crew.py            # Crew assembly
│   └── main.py            # Entry point
└── pyproject.toml
```

### agents.yaml

```yaml
researcher:
  role: "{topic} Senior Data Researcher"
  goal: "Uncover cutting-edge developments in {topic}"
  backstory: >
    You're a seasoned researcher with a knack for uncovering
    the latest developments in {topic}. Known for your ability
    to find relevant information and present it clearly.

reporting_analyst:
  role: "Reporting Analyst"
  goal: "Create detailed reports based on research data"
  backstory: >
    You're a meticulous analyst who transforms raw data into
    actionable insights through well-structured reports.
```

### tasks.yaml

```yaml
research_task:
  description: >
    Conduct thorough research about {topic}.
    Find the most relevant information for {year}.
  expected_output: >
    A list with 10 bullet points of the most relevant
    information about {topic}.
  agent: researcher

reporting_task:
  description: >
    Review the research and create a comprehensive report.
    Focus on key findings and recommendations.
  expected_output: >
    A detailed report in markdown format with executive
    summary, findings, and recommendations.
  agent: reporting_analyst
  output_file: report.md
```

### crew.py

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class MyProjectCrew:
    """My Project crew"""

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

### main.py

```python
from my_project.crew import MyProjectCrew

def run():
    inputs = {
        'topic': 'AI Agents',
        'year': 2025
    }
    MyProjectCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
```

## Flows - Orquestração event-driven

Para workflows complexos com lógica condicional, use Flows:

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class MyState(BaseModel):
    confidence: float = 0.0

class MyFlow(Flow[MyState]):
    @start()
    def gather_data(self):
        return {"data": "collected"}

    @listen(gather_data)
    def analyze(self, data):
        self.state.confidence = 0.85
        return analysis_crew.kickoff(inputs=data)

    @router(analyze)
    def decide(self):
        return "high" if self.state.confidence > 0.8 else "low"

    @listen("high")
    def generate_report(self):
        return report_crew.kickoff()

# Executar flow
flow = MyFlow()
result = flow.kickoff()
```

Consulte [Flows Guide](references/flows.md) para documentação completa.

## Sistema de memória

```python
# Habilitar todos os tipos de memória
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    memory=True,           # Enable memory
    embedder={             # Custom embeddings
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

**Tipos de memória:** Curto prazo (ChromaDB), Longo prazo (SQLite), Entidades (ChromaDB)

## Provedores de LLM

```python
from crewai import LLM

llm = LLM(model="gpt-4o")                              # OpenAI (default)
llm = LLM(model="claude-sonnet-4-5-20250929")                       # Anthropic
llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")  # Local
llm = LLM(model="azure/gpt-4o", base_url="https://...")              # Azure

agent = Agent(role="Analyst", goal="Analyze data", llm=llm)
```

## CrewAI vs alternativas

| Característica | CrewAI | LangChain | LangGraph |
|---------|--------|-----------|-----------|
| **Melhor para** | Equipes multi-agent | Apps LLM gerais | Workflows com estado |
| **Curva de aprendizado** | Baixa | Média | Alta |
| **Paradigma de agent** | Baseado em papéis | Baseado em ferramentas | Baseado em grafo |
| **Memória** | Built-in | Plugin-based | Customizada |

## Boas práticas

1. **Papéis claros** - Cada agente deve ter uma especialidade distinta
2. **Configuração em YAML** - Melhor organização para projetos maiores
3. **Habilitar memória** - Melhora o contexto entre tarefas
4. **Definir max_iter** - Prevenir loops infinitos (padrão 15)
5. **Limitar ferramentas** - Máximo 3-5 ferramentas por agente
6. **Rate limiting** - Definir max_rpm para evitar limites de API

## Problemas comuns

**Agente preso em loop:**
```python
agent = Agent(
    role="...",
    max_iter=10,           # Limit iterations
    max_rpm=5              # Rate limit
)
```

**Tarefa não usando contexto:**
```python
task2 = Task(
    description="...",
    context=[task1],       # Explicitly pass context
    agent=writer
)
```

**Erros de memória:**
```python
# Use variável de ambiente para storage
import os
os.environ["CREWAI_STORAGE_DIR"] = "./my_storage"
```

## Referências

- **[Flows Guide](references/flows.md)** - Workflows event-driven, gerenciamento de estado
- **[Tools Guide](references/tools.md)** - Ferramentas built-in, ferramentas customizadas, MCP
- **[Troubleshooting](references/troubleshooting.md)** - Problemas comuns, debugging

## Recursos

- **GitHub**: https://github.com/crewAIInc/crewAI (25k+ stars)
- **Docs**: https://docs.crewai.com
- **Tools**: https://github.com/crewAIInc/crewAI-tools
- **Examples**: https://github.com/crewAIInc/crewAI-examples
- **Version**: 1.2.0+
- **License**: MIT