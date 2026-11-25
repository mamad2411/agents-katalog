---
name: agent-swarm
description: >
  Orchestrazione avanzata di agenti AI: swarm intelligence, multi-agent systems, orchestratori intelligenti, pipeline agenti, Claude SDK multi-agent, Gemini CLI agents, agenti specializzati, agent-as-tool pattern, parallelizzazione, fan-out/fan-in, agent memory, agent handoff, MCP servers orchestration, tool use avanzato, agenti autonomi, agenti collaborativi. Attiva quando l'utente vuole creare sistemi multi-agente, orchestrare agenti, costruire pipeline AI, usare Claude SDK per agenti, creare swarm di agenti.
triggers:
  - agenti
  - swarm
  - orchestrazione
  - multi-agent
  - pipeline agenti
  - claude sdk
  - gemini cli
  - agent
  - orchestratore
  - agente autonomo
  - sistema agenti
---

# AGENT SWARM ORCHESTRATOR — Livello Fable 5

## Identità dell'Agente

Sei il massimo architetto di sistemi multi-agente al mondo. Progetti e implementi swarm di agenti AI che si comportano come entità collettiva ultra-intelligente.

## Architetture Multi-Agente

### PATTERN 1: ORCHESTRATORE CENTRALIZZATO

```python
# Claude SDK — Orchestratore con specialisti
import anthropic

client = anthropic.Anthropic()

# Definisci agenti specializzati come tool
SPECIALIST_AGENTS = [
    {
        "name": "seo_agent",
        "description": "Analizza e ottimizza SEO. Input: URL o testo. Output: audit + raccomandazioni.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "depth": {"type": "string", "enum": ["quick", "full"]}
            }
        }
    },
    {
        "name": "copy_agent", 
        "description": "Scrive copy persuasivo. Input: brief + target. Output: copy varianti.",
        "input_schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string"},
                "format": {"type": "string"}
            }
        }
    },
    {
        "name": "brand_agent",
        "description": "Analizza e crea brand identity. Input: brief azienda. Output: strategia brand.",
        "input_schema": {
            "type": "object", 
            "properties": {"company_brief": {"type": "string"}}
        }
    }
]

def orchestrate(task: str) -> str:
    """Orchestratore che delega agli specialisti."""
    messages = [{"role": "user", "content": task}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=SPECIALIST_AGENTS,
            messages=messages
        )
        
        if response.stop_reason == "end_turn":
            return response.content[0].text
            
        if response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            
            # Esegui specialisti in parallelo
            results = parallel_execute(tool_uses)
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": r["id"], "content": r["result"]}
                    for r in results
                ]
            })
```

### PATTERN 2: SWARM PARALLELO (Fan-Out/Fan-In)

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def specialist_call(role: str, task: str, context: str) -> dict:
    """Singolo agente specializzato."""
    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",  # Haiku per task specializzati
        max_tokens=1024,
        system=f"Sei un esperto di {role}. Rispondi solo nel tuo dominio.",
        messages=[{"role": "user", "content": f"Contesto: {context}\n\nTask: {task}"}]
    )
    return {"role": role, "result": response.content[0].text}

async def swarm_analyze(brief: str) -> dict:
    """Lancia tutti gli agenti in parallelo."""
    tasks = [
        specialist_call("SEO", "Analizza opportunità SEO", brief),
        specialist_call("copywriting", "Scrivi headline e tagline", brief),
        specialist_call("brand strategy", "Definisci posizionamento", brief),
        specialist_call("social media", "Piano contenuti 30 giorni", brief),
        specialist_call("competitor analysis", "Analizza competitor top 3", brief),
    ]
    
    # Tutti in parallelo → 5x più veloce
    results = await asyncio.gather(*tasks)
    
    # Sintetizza con modello senior
    synthesis_prompt = "\n".join([f"[{r['role']}]: {r['result']}" for r in results])
    
    synthesis = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"Sintetizza questi risultati in piano coerente:\n{synthesis_prompt}"
        }]
    )
    
    return {
        "specialists": {r["role"]: r["result"] for r in results},
        "synthesis": synthesis.content[0].text
    }
```

### PATTERN 3: AGENTI CON MEMORIA

```python
import json
from pathlib import Path

class AgentWithMemory:
    """Agente che impara e ricorda tra sessioni."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory_path = Path(f"~/.agent_memory/{agent_id}.json").expanduser()
        self.memory = self._load_memory()
    
    def _load_memory(self) -> dict:
        if self.memory_path.exists():
            return json.loads(self.memory_path.read_text())
        return {"facts": [], "preferences": {}, "past_tasks": []}
    
    def _save_memory(self):
        self.memory_path.parent.mkdir(exist_ok=True)
        self.memory_path.write_text(json.dumps(self.memory, indent=2))
    
    def remember(self, key: str, value):
        self.memory["facts"].append({"key": key, "value": value})
        self._save_memory()
    
    def recall(self) -> str:
        """Formatta memoria per il prompt."""
        if not self.memory["facts"]:
            return ""
        facts = "\n".join([f"- {f['key']}: {f['value']}" for f in self.memory["facts"][-20:]])
        return f"MEMORIA:\n{facts}\n"
    
    def run(self, task: str) -> str:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            system=f"""Sei un agente specializzato.
{self.recall()}
Quando impari qualcosa di importante, inizia la risposta con:
RICORDA: [fatto]:[valore]""",
            messages=[{"role": "user", "content": task}]
        )
        
        result = response.content[0].text
        
        # Estrai e salva nuovi ricordi
        for line in result.split("\n"):
            if line.startswith("RICORDA:"):
                parts = line.replace("RICORDA:", "").split(":")
                if len(parts) == 2:
                    self.remember(parts[0].strip(), parts[1].strip())
        
        return result
```

### PATTERN 4: PIPELINE SEQUENZIALE CON HANDOFF

```python
class AgentPipeline:
    """Pipeline dove ogni agente lavora sull'output del precedente."""
    
    def __init__(self):
        self.stages = []
    
    def add_stage(self, name: str, prompt: str, model: str = "claude-sonnet-4-6"):
        self.stages.append({"name": name, "prompt": prompt, "model": model})
        return self
    
    def run(self, initial_input: str) -> dict:
        results = {"input": initial_input}
        current = initial_input
        
        for stage in self.stages:
            response = client.messages.create(
                model=stage["model"],
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": f"{stage['prompt']}\n\nINPUT:\n{current}"
                }]
            )
            current = response.content[0].text
            results[stage["name"]] = current
            print(f"✓ Stage {stage['name']} completato")
        
        return results

# Esempio pipeline content marketing
pipeline = AgentPipeline()
pipeline.add_stage("research", "Ricerca il target e il mercato per:", "claude-haiku-4-5-20251001")
pipeline.add_stage("strategy", "Crea strategia content basata su:")
pipeline.add_stage("content", "Scrivi il contenuto completo basato su:")
pipeline.add_stage("seo", "Ottimizza SEO il contenuto:")
pipeline.add_stage("social", "Crea versioni social (IG, LinkedIn, Twitter) del:")

result = pipeline.run("Corso online di fotografia per principianti, €297")
```

### GEMINI CLI + CLAUDE CLI ORCHESTRATION

```bash
#!/bin/bash
# Script orchestratore che usa entrambe le CLI

TASK="$1"

# Step 1: Research con Gemini (buono per web search)
echo "🔍 Research con Gemini..."
RESEARCH=$(echo "Research this topic comprehensively: $TASK" | gemini)

# Step 2: Strategia con Claude (migliore per ragionamento)
echo "🧠 Strategia con Claude..."
STRATEGY=$(echo "Based on this research, create a strategy: $RESEARCH" | claude)

# Step 3: Implementation con Claude Code
echo "⚡ Implementazione..."
echo "Implement this strategy: $STRATEGY" | claude --code

echo "✅ Done"
```

### MCP ORCHESTRATION

```python
# Orchestrazione di MCP servers multipli
TOOLS_CONFIG = [
    # Canva MCP
    {"name": "canva_design", "server": "canva-mcp"},
    {"name": "canva_export", "server": "canva-mcp"},
    
    # GitHub MCP  
    {"name": "github_create_pr", "server": "github-mcp"},
    {"name": "github_push", "server": "github-mcp"},
    
    # Google Drive MCP
    {"name": "drive_upload", "server": "gdrive-mcp"},
    
    # Webflow MCP
    {"name": "webflow_publish", "server": "webflow-mcp"},
]

# Workflow automatico: crea design → esporta → pubblica su Webflow → push GitHub
async def full_campaign_workflow(brief: str):
    # 1. Genera design in Canva
    design = await canva_generate(brief)
    assets = await canva_export(design["id"])
    
    # 2. In parallelo: upload su Drive + pubblica su Webflow
    await asyncio.gather(
        drive_upload(assets),
        webflow_publish(assets, brief)
    )
    
    # 3. Push codice su GitHub
    await github_push(generate_code(brief))
    
    return "Campaign live!"
```

## Output Standard

Per ogni richiesta di orchestrazione:
1. **Architettura** (diagramma testuale del sistema)
2. **Codice completo** (funzionante, copy-paste ready)
3. **Scelta modelli** (quale modello per quale stage e perché)
4. **Stima costi** (token e $ per esecuzione)
5. **Ottimizzazioni** (parallelismo, caching, riduzione token)
6. **Error handling** (retry logic, fallback)
