# ATOMIA - Agente de IA Educativo Agéntico
# Reglas principales para desarrollo con Cursor

## 🎯 DESCRIPCIÓN DEL PROYECTO
Atomia es un **sistema agéntico educativo** que implementa aprendizaje personalizado basado en principios pedagógicos científicos. El sistema combina capacidades de razonamiento avanzado con herramientas educativas especializadas para atomizar contenido, generar preguntas adaptativas, evaluar respuestas, y personalizar rutas de aprendizaje usando agentes de IA con memoria y razonamiento.

## 🤖 ARQUITECTURA AGÉNTICA

### Capacidades Agénticas Implementadas ✅
- **Agente Educativo Principal**: ReAct con LangChain para razonamiento educativo
- **Sistema de Memoria Multi-Nivel**: Corto plazo, largo plazo (Redis), semántica (ChromaDB)
- **Herramientas Educativas Especializadas**: Búsqueda de átomos, seguimiento de progreso, generación de preguntas, evaluación
- **Workflow Plan-Execute-Observe-Reflect**: Implementado con LangGraph
- **Orquestador Agéntico**: Gestiona el ciclo completo de razonamiento educativo

### Stack Tecnológico Agéntico
- **Agentes**: LangChain + LangGraph para workflow de razonamiento
- **LLM Principal**: DeepSeek R1 vía Azure AI
- **Memoria Semántica**: ChromaDB para búsqueda vectorial
- **Memoria Persistente**: Redis para contexto de usuario
- **Herramientas**: Custom Tools para tareas educativas específicas
- **Frontend**: Flutter (multiplataforma: iOS, Android, Web)
- **Backend**: Microservicios Python/FastAPI
- **Bases de Datos**: 
  - PostgreSQL (datos estructurados) - instalación local
  - MongoDB (contenido de átomos) - instalación local
  - Neo4j (grafo de conocimiento) - instalación local
- **Queue**: RabbitMQ para procesamiento asíncrono - instalación local

### Configuración Agéntica
```python
# backend/services/llm_orchestrator/src/config.py
class Config:
    # Azure AI Configuration
AZURE_AI_ENDPOINT = "https://ai-bryanjavierjaramilloc0912ai799661901077.services.ai.azure.com/models"
    AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")
    MODEL_NAME = "deepseek-r1"
    
    # Redis Configuration for Memory
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    # ChromaDB Configuration for Semantic Memory
    CHROMA_PERSIST_DIR = "./chroma_db"
    CHROMA_COLLECTION = "atomia_memory"
    
    # Agent Configuration
    MAX_ITERATIONS = 10
    MEMORY_WINDOW = 10
    SEMANTIC_SEARCH_LIMIT = 5
```

## Core Pedagogical Principles (Implementation Required)

### 1. Skinner's Teaching Machine
- **Microlearning**: Break content into small, manageable pieces
- **Immediate Feedback**: Provide instant response to every user action
- **Active Participation**: Require user engagement, not passive consumption
- **Progressive Difficulty**: Gradual increase in complexity
- **Individualized Pacing**: Each user advances at their own speed

### 2. Spaced Repetition (SM-2 Algorithm)
- **Ease Factor**: 1.3 to 2.5, adjusted based on response quality
- **Interval Calculation**: interval = previous_interval * ease_factor
- **Quality Scoring**: 0-5 scale for response quality assessment
- **Dynamic Scheduling**: Adjust review timing based on forgetting patterns

### 3. Active Learning Implementation
- **Higher-Order Questions**: Focus on analysis, synthesis, evaluation (Bloom's Taxonomy)
- **Scaffolding**: Provide temporary support that's gradually removed
- **Metacognitive Prompts**: Encourage reflection on learning process
- **Connection Building**: Help users relate new information to prior knowledge

### 4. Intermittent Positive Reinforcement
- **Variable Ratio Schedule**: Unpredictable reward timing for maximum engagement
- **Intrinsic + Extrinsic**: Balance internal satisfaction with external rewards
- **Achievement Recognition**: Celebrate effort and progress, not just correct answers
- **Gamification Elements**: Points, badges, streaks, leaderboards (optional)

## 📋 COMPONENTES AGÉNTICOS PRINCIPALES

### 1. Agente Educativo Principal (Implementado ✅)
- **Arquitectura**: ReAct con LangChain para razonamiento educativo
- **Capacidades**: Planifica, ejecuta herramientas, observa resultados, reflexiona
- **Prompt Especializado**: Incluye principios pedagógicos y objetivos educativos
- **Herramientas**: Acceso a 4 herramientas educativas especializadas

### 2. Sistema de Memoria Multi-Nivel (Implementado ✅)
- **Memoria a Corto Plazo**: Buffer de conversación en memoria (últimas 10 interacciones)
- **Memoria a Largo Plazo**: Persistencia en Redis con TTL de 30 días
- **Memoria Semántica**: ChromaDB para búsqueda vectorial de interacciones previas
- **Contexto de Usuario**: Perfil, progreso de aprendizaje, historial

### 3. Herramientas Educativas Especializadas (Implementado ✅)
- **search_learning_atoms**: Busca átomos de aprendizaje relacionados con consultas
- **track_learning_progress**: Rastrea y actualiza progreso de aprendizaje
- **generate_adaptive_questions**: Genera preguntas basadas en principios pedagógicos
- **evaluate_user_answer**: Evalúa respuestas y proporciona retroalimentación

### 4. Orquestador Agéntico con LangGraph (Implementado ✅)
- **Workflow Plan-Execute-Observe-Reflect**: Ciclo completo de razonamiento
- **Estados del Agente**: Mensajes, tareas, contexto, herramientas usadas, pasos de razonamiento
- **Lógica Condicional**: Decide cuándo continuar iterando o finalizar
- **Manejo de Errores**: Recuperación automática con límites de reintentos

### 5. Módulo de Atomización de Contenido
- Descompone material educativo en átomos de aprendizaje
- Cada átomo: autocontenido, coherente, evaluable
- Establece relaciones y prerrequisitos entre átomos
- Usa LLM para análisis semántico profundo

### 6. Motor de Evaluación
- Evalúa respuestas cerradas (algoritmos) y abiertas (LLM)
- Detecta conceptos erróneos y brechas de conocimiento
- Genera retroalimentación constructiva personalizada
- Actualiza modelo del estudiante en tiempo real

### 7. Planificador Adaptativo
- Implementa repetición espaciada (FSRS)
- Ajusta dificultad y ritmo dinámicamente
- Balancea contenido nuevo vs repaso
- Detecta necesidades especiales (frustración, aburrimiento)

### 8. Sistema de Adherencia y Gamificación
- Refuerzo positivo intermitente
- Puntos, insignias, niveles, progreso visual
- Notificaciones inteligentes personalizadas
- Análisis de comportamiento para prevenir abandono

## 🔧 REGLAS DE DESARROLLO AGÉNTICO

### Estructura de Proyecto Agéntico
```
atomia/
├── backend/
│   ├── services/
│   │   ├── llm_orchestrator/     # ✅ Sistema agéntico completo
│   │   │   ├── src/
│   │   │   │   ├── agents.py     # Agente educativo ReAct
│   │   │   │   ├── memory.py     # Memoria multi-nivel
│   │   │   │   ├── tools.py      # Herramientas educativas
│   │   │   │   ├── orchestrator.py # Workflow LangGraph
│   │   │   │   ├── config.py     # Configuración agéntica
│   │   │   │   └── main.py       # API FastAPI
│   │   │   └── requirements.txt
│   │   ├── atomization/          # Servicio de atomización
│   │   ├── evaluation/           # Motor de evaluación
│   │   ├── planning/             # Planificador adaptativo
│   │   ├── questions/            # Generador de preguntas
│   │   └── gamification/         # Sistema de adherencia
│   ├── shared/
│   │   ├── models/              # Modelos de datos compartidos
│   │   ├── utils/               # Utilidades comunes
│   │   └── prompts/             # Templates de prompts
│   └── api_gateway/             # Gateway principal
├── frontend/
│   ├── lib/
│   │   ├── core/               # Lógica central
│   │   ├── features/           # Features por módulo
│   │   ├── shared/             # Componentes compartidos
│   │   └── config/             # Configuración
│   └── platforms/              # Código específico por plataforma
├── infrastructure/
│   ├── scripts/               # Scripts de setup y utilidades
│   └── configs/               # Archivos de configuración
└── docs/                      # Documentación existente
```

### Convenciones de Código Agéntico

#### Python (Agentes y Backend)
```python
# Usar type hints siempre con tipos agénticos
from typing import List, Dict, Optional, TypedDict
from langchain.tools import BaseTool
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

# Estado del agente con TypedDict
class AgentState(TypedDict):
    messages: List[Any]
    current_task: str
    user_context: Dict[str, Any]
    tools_used: List[str]
    reasoning_steps: List[str]
    final_answer: str
    error_count: int

# Herramientas educativas con BaseModel
class AtomSearchInput(BaseModel):
    query: str = Field(description="Consulta para buscar átomos relacionados")
    difficulty: str = Field(default="all", description="Nivel de dificultad")

class AtomSearchTool(BaseTool):
    name = "search_learning_atoms"
    description = "Busca átomos de aprendizaje relacionados"
    args_schema: Type[BaseModel] = AtomSearchInput
    
# Async por defecto para endpoints agénticos
@app.post("/agent/process")
async def process_educational_task(request: EducationalTaskRequest) -> AgentResponse:
    result = await orchestrator.process_educational_task(request.dict())
    return AgentResponse(**result)

# Manejo de errores agénticos
class AgenticException(Exception):
    pass
```

#### Flutter (Frontend)
```dart
// Estructura de features agénticas
lib/features/agent_interaction/
├── domain/
│   ├── entities/
│   │   ├── agent_response.dart
│   │   └── reasoning_step.dart
│   ├── repositories/
│   └── usecases/
│       └── process_educational_task.dart
├── data/
│   ├── datasources/
│   │   └── agent_api_datasource.dart
│   ├── models/
│   └── repositories/
└── presentation/
    ├── pages/
    │   └── agent_chat_page.dart
    ├── widgets/
    │   ├── reasoning_steps_widget.dart
    │   └── tools_used_widget.dart
    └── bloc/
        └── agent_interaction_bloc.dart

// Uso de BLoC para estado agéntico
class AgentInteractionBloc extends Bloc<AgentEvent, AgentState> {
  final ProcessEducationalTaskUseCase processTask;
  final SearchMemoryUseCase searchMemory;
}
```

### Integración Agéntica con LLMs

#### Agente Educativo ReAct
```python
class EducationalAgent:
    """
    Agente educativo con capacidades de razonamiento, memoria y herramientas especializadas
    """
    
    def __init__(self, llm, tools, memory_system):
        self.llm = llm
        self.tools = tools
        self.memory = memory_system
        
        # Prompt especializado para educación
        self.prompt = PromptTemplate.from_template("""
        Eres un agente de IA educativo especializado en aprendizaje personalizado.
        
        Tu misión es:
        1. Atomizar contenido educativo en unidades mínimas de aprendizaje
        2. Generar preguntas adaptativas basadas en principios pedagógicos
        3. Evaluar respuestas y proporcionar retroalimentación constructiva
        4. Personalizar rutas de aprendizaje según el progreso del estudiante
        
        Principios pedagógicos que debes seguir:
        - Microaprendizaje (Skinner): Divide en unidades pequeñas con feedback inmediato
        - Repetición espaciada: Programa revisiones basadas en curva de olvido
        - Aprendizaje activo: Genera preguntas que requieren reflexión profunda
        - Refuerzo intermitente: Varía recompensas para mantener motivación
        
        Tienes acceso a las siguientes herramientas:
        {tools}
        
        Usuario: {input}
        Pensamiento: {agent_scratchpad}
        """)
        
        # Crear agente ReAct
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
```

#### Sistema de Memoria Multi-Nivel
```python
class AgenticMemorySystem:
    """
    Sistema de memoria multi-nivel para el agente educativo:
    1. Memoria a corto plazo: Buffer de conversación
    2. Memoria a largo plazo: Persistencia en Redis
    3. Memoria semántica: Búsqueda vectorial con ChromaDB
    """
    
    async def add_interaction(self, user_id: str, query: str, 
                            response: str, tools_used: List = None):
        # Almacenar en los 3 niveles de memoria
        pass
    
    async def search_semantic_memory(self, query: str, limit: int = 5) -> List[Dict]:
        # Búsqueda vectorial en ChromaDB
        pass
    
    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        # Recuperar contexto completo del usuario
    pass
```

#### Workflow Plan-Execute-Observe-Reflect
```python
class AgenticOrchestrator:
    """
    Orquestador agéntico que implementa el ciclo Plan-Execute-Observe-Reflect
    """
    
    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)

        # Nodos del workflow
        workflow.add_node("plan", self._plan_step)
        workflow.add_node("execute", self._execute_step)
        workflow.add_node("observe", self._observe_step)
        workflow.add_node("reflect", self._reflect_step)
        workflow.add_node("finalize", self._finalize_step)
        
        # Lógica condicional para continuar o finalizar
        workflow.add_conditional_edges(
            "reflect",
            self._should_continue,
            {"continue": "plan", "finish": "finalize"}
        )
        
        return workflow.compile()
```

### API Endpoints Agénticos

#### Servidor FastAPI con Capacidades Agénticas
```python
# backend/services/llm_orchestrator/src/main.py
app = FastAPI(title="Atomia - Agente Educativo Agéntico", version="1.0.0")

@app.post("/agent/process", response_model=AgentResponse)
async def process_educational_task(request: EducationalTaskRequest):
    """Procesa una tarea educativa usando el agente con capacidades de razonamiento"""
    result = await orchestrator.process_educational_task(request.dict())
    return AgentResponse(**result)

@app.post("/agent/memory/search")
async def search_memory(query: str, user_id: Optional[str] = None, limit: int = 5):
    """Busca en la memoria semántica del agente"""
    results = await memory_system.search_semantic_memory(query, limit)
    return {"results": results}

@app.get("/agent/context/{user_id}")
async def get_user_context(user_id: str):
    """Obtiene el contexto completo de un usuario"""
    context = await memory_system.get_user_context(user_id)
    return context
```

### Testing Agéntico

#### Tests para Sistema Agéntico
```python
# tests/test_agentic_system.py
class TestAgenticSystem:
    @pytest.mark.asyncio
    async def test_educational_task_processing(self):
        """Test completo del procesamiento de tareas educativas"""
        result = await orchestrator.process_educational_task({
            "query": "Explica el concepto de funciones en matemáticas",
            "user_id": "test_user_123"
        })
        
        assert "answer" in result
        assert "reasoning_steps" in result
        assert "tools_used" in result
        assert isinstance(result["iterations"], int)
    
    @pytest.mark.asyncio
    async def test_memory_system_integration(self):
        """Test del sistema de memoria multi-nivel"""
        await memory_system.add_interaction(
            user_id="test_user",
            query="¿Qué es una función?",
            response="Una función es una relación...",
            tools_used=["search_learning_atoms"]
        )
        
        results = await memory_system.search_semantic_memory("funciones matemáticas")
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Test del workflow completo Plan-Execute-Observe-Reflect"""
        # Test pasos del workflow
        state_after_plan = await orchestrator._plan_step(initial_state)
        assert len(state_after_plan['reasoning_steps']) > 0
        assert "PLAN" in state_after_plan['reasoning_steps'][0]
```

### Optimización y Performance Agéntica

#### Estrategias Clave para Agentes
1. **Cache de razonamiento**: Redis para razonamientos similares
2. **Memoria semántica**: ChromaDB para reutilizar conocimiento
3. **Procesamiento asíncrono**: Workflows agénticos en background
4. **Herramientas optimizadas**: Cache de resultados de herramientas
5. **Límites de iteración**: Evitar bucles infinitos de razonamiento

#### Monitoreo Agéntico
```python
# Métricas específicas para el sistema agéntico
agent_task_duration = prom.Histogram(
    'agent_task_duration_seconds',
    'Duración de procesamiento de tareas educativas',
    ['task_type', 'user_level']
)

agent_reasoning_steps = prom.Histogram(
    'agent_reasoning_steps_count',
    'Número de pasos de razonamiento por tarea',
    ['task_type', 'completion_status']
)

agent_tool_usage = prom.Counter(
    'agent_tool_usage_total',
    'Uso de herramientas educativas por el agente',
    ['tool_name', 'success']
)
```

## 🚀 FLUJOS DE DESARROLLO AGÉNTICO

### 1. Implementar Nueva Herramienta Educativa
1. Definir input/output schema con Pydantic
2. Crear clase heredando de BaseTool
3. Implementar método _run con lógica específica
4. Agregar a get_educational_tools()
5. Actualizar prompt del agente
6. Escribir tests de integración
7. Documentar uso de la herramienta

### 2. Extender Capacidades de Memoria
1. Identificar nuevo tipo de memoria necesaria
2. Extender AgenticMemorySystem
3. Actualizar métodos de almacenamiento/recuperación
4. Modificar get_user_context para incluir nueva información
5. Testear integración con agente
6. Optimizar índices de búsqueda

### 3. Mejorar Workflow de Razonamiento
1. Identificar nuevos pasos en el workflow
2. Crear métodos _new_step en AgenticOrchestrator
3. Actualizar _build_workflow con nuevos nodos
4. Modificar lógica condicional _should_continue
5. Testear nuevo flujo completo
6. Medir impacto en performance

## 📝 MEJORES PRÁCTICAS AGÉNTICAS

### Diseño de Prompts Agénticos
- Incluir principios pedagógicos en system prompt
- Definir claramente misión y objetivos educativos
- Listar herramientas disponibles con descripciones
- Proporcionar formato ReAct consistente
- Incluir contexto de usuario personalizado

### Herramientas Educativas
- Una herramienta = una responsabilidad específica
- Input/output schemas claros con Pydantic
- Documentación descriptiva en description
- Manejo robusto de errores
- Logs para debugging y monitoreo

### Sistema de Memoria
- Separar tipos de memoria por propósito
- TTLs apropiados para cada nivel
- Búsqueda semántica para patrones complejos
- Contexto enriquecido para personalización
- Limpieza automática de datos antiguos

### Workflow de Razonamiento
- Límites claros de iteraciones
- Manejo graceful de errores
- Estados inmutables en StateGraph
- Lógica condicional robusta
- Logging detallado de pasos

## 🔍 DEBUGGING AGÉNTICO

### Logs Estructurados Agénticos
```python
logger.info("Agent task completed", extra={
    "user_id": user_id,
    "task_type": task_type,
    "reasoning_steps": len(reasoning_steps),
    "tools_used": tools_used,
    "iterations": iterations,
    "duration_ms": duration
})
```

### Trazabilidad de Razonamiento
- Loggear cada paso del workflow
- Incluir request_id en toda la cadena agéntica
- Guardar prompts y respuestas del agente
- Monitorear uso de herramientas
- Detectar patrones de razonamiento anómalos

## 📚 RECURSOS AGÉNTICOS

### Documentación Clave Agéntica
- `/development/llm-integration.md` - Guía completa de integración agéntica
- `/backend/services/llm_orchestrator/` - Código fuente del sistema agéntico
- `/docs/prompts/` - Templates de prompts educativos
- `/docs/algoritmos/` - Algoritmos pedagógicos implementados

### Principios Agénticos Educativos
1. **Razonamiento Educativo**: Cada decisión debe basarse en principios pedagógicos
2. **Memoria Contextual**: Mantener contexto rico del estudiante para personalización
3. **Herramientas Especializadas**: Cada herramienta debe servir un propósito educativo específico
4. **Workflow Adaptativo**: El ciclo de razonamiento debe adaptarse al contexto educativo

## ⚠️ CONSIDERACIONES AGÉNTICAS

### Estado Actual del Sistema Agéntico ✅
- **Agente educativo ReAct**: Completamente implementado
- **Memoria multi-nivel**: Redis + ChromaDB funcionando
- **4 herramientas educativas**: Implementadas y probadas
- **Workflow LangGraph**: Plan-Execute-Observe-Reflect operativo
- **API FastAPI**: Endpoints agénticos disponibles

### Próximas Prioridades Agénticas
1. **Agentes especializados**: Atomización, evaluación, planificación
2. **Coordinador multi-agente**: Orquestar múltiples agentes
3. **Aprendizaje por refuerzo**: Mejora continua basada en feedback
4. **Herramientas avanzadas**: Integración con bases de datos específicas
5. **Dashboard agéntico**: Visualización de razonamiento y memoria

### Anti-patterns Agénticos a Evitar
- NO crear herramientas sin propósito educativo claro
- NO permitir bucles infinitos de razonamiento
- NO ignorar el contexto de memoria del usuario
- NO diseñar prompts sin principios pedagógicos
- NO omitir logging de pasos de razonamiento
- NO asumir que el agente siempre tendrá éxito

## 🤝 COLABORACIÓN AGÉNTICA

### Commits Agénticos
```
feat: Add semantic memory search tool
fix: Correct agent reasoning loop termination
docs: Update agentic architecture documentation
test: Add workflow integration tests
refactor: Extract educational tool interface
agent: Improve planning step with pedagogical principles
```

### Pull Requests Agénticas
- Describir capacidades agénticas añadidas/modificadas
- Incluir tests de workflow completo
- Documentar nuevas herramientas o cambios de memoria
- Screenshots de logs de razonamiento
- Métricas de performance agéntica

### Code Review Agéntico
- Verificar principios pedagógicos en prompts
- Validar manejo de errores en workflow
- Confirmar logging adecuado de razonamiento
- Revisar esquemas de herramientas educativas
- Testear integración de memoria

**El sistema agéntico de Atomia representa la próxima generación de educación personalizada, donde agentes inteligentes razonan, recuerdan y adaptan continuamente para optimizar el aprendizaje de cada estudiante.** 

## 🐳 INICIO DEL PROYECTO CON DOCKER (ACTUALIZADO)

### **🚀 Inicio Completo del Sistema**

**Prerrequisitos:**
- Docker y Docker Compose instalados
- Git para clonar el repositorio
- Variable de entorno AZURE_AI_KEY configurada

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd Atomia

# 2. Configurar variable de entorno LLM
export AZURE_AI_KEY="your-azure-ai-key-here"

# 3. Iniciar todo el sistema con un solo comando
docker-compose up -d --build

# 4. Verificar estado de servicios
docker-compose ps

# 5. Ver logs si es necesario
docker-compose logs -f [servicio]
```

### **📊 Arquitectura Dockerizada Completa**

```yaml
# docker-compose.yml - Sistema completo containerizado
services:
  # 🗄️ INFRAESTRUCTURA
  postgres:     # Base de datos principal (Puerto 5432)
  mongodb:      # Almacenamiento de átomos (Puerto 27017)
  redis:        # Cache y memoria (Puerto 6379)
  neo4j:        # Grafo de conocimiento (Puerto 7474, 7687)
  rabbitmq:     # Cola de mensajes (Puerto 5672, 15672)
  
  # 🔧 SERVICIOS BACKEND
  llm_orchestrator:  # Sistema agéntico principal (Puerto 8002)
  atomization:       # Procesamiento de contenido (Puerto 8001)
  evaluation:        # Motor de evaluación (Puerto 8003)
  planning:          # Planificador adaptativo (Puerto 8004)
  questions:         # Generador de preguntas (Puerto 8005)
  gamification:      # Sistema de adherencia (Puerto 8006)
  authentication:    # Autenticación y autorización (Puerto 8007)
  
  # 🌐 FRONTEND
  frontend:         # Aplicación Flutter Web (Puerto 3000)
```

### **🌐 Enlaces de Acceso**

Una vez iniciado el sistema, puedes acceder a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Aplicación Principal** | http://localhost:3000 | Frontend Flutter Web |
| **API Documentation** | http://localhost:8002/docs | Documentación LLM Orchestrator |
| **Neo4j Browser** | http://localhost:7474 | Interfaz gráfica del grafo |
| **RabbitMQ Management** | http://localhost:15672 | Admin de colas (guest/guest) |

### **🔧 Comandos de Gestión**

```bash
# Iniciar todo el sistema
docker-compose up -d

# Parar todo el sistema
docker-compose down

# Reiniciar un servicio específico
docker-compose restart [servicio]

# Ver logs de un servicio
docker-compose logs -f [servicio]

# Rebuild y reiniciar
docker-compose up -d --build

# Ver estado de todos los servicios
docker-compose ps

# Acceder a shell de un contenedor
docker-compose exec [servicio] bash
```

### **🔍 Troubleshooting**

```bash
# Verificar que todos los servicios estén corriendo
docker-compose ps

# Ver logs de servicios que fallaron
docker-compose logs [servicio-que-fallo]

# Reiniciar servicios con problemas
docker-compose restart [servicio]

# Limpiar y rebuild completo
docker-compose down
docker system prune -f
docker-compose up -d --build

# Verificar puertos ocupados
ss -tlnp | grep -E "(3000|8001|8002|8003|8004|8005|8006|8007)"
```

### **📱 Frontend Flutter Dockerizado**

**Dockerfile personalizado para Flutter Web:**
```dockerfile
FROM cirrusci/flutter:stable
RUN flutter config --enable-web
WORKDIR /app
COPY pubspec.yaml pubspec.lock ./
RUN flutter pub get
COPY . .
EXPOSE 3000
CMD ["flutter", "run", "-d", "web-server", "--web-port", "3000", "--web-hostname", "0.0.0.0", "--release"]
```

**Variables de entorno para conectar con backend:**
```yaml
environment:
  LLM_ORCHESTRATOR_URL: http://llm_orchestrator:8002
  ATOMIZATION_URL: http://atomization:8001
  EVALUATION_URL: http://evaluation:8003
  PLANNING_URL: http://planning:8004
  QUESTIONS_URL: http://questions:8005
```

### **⚠️ Notas Importantes**

1. **Primera ejecución**: El primer `docker-compose up` puede tardar varios minutos en descargar y construir todas las imágenes.

2. **Variables de entorno**: Asegúrate de tener `AZURE_AI_KEY` configurada para el LLM.

3. **Recursos del sistema**: El sistema completo requiere al menos 4GB de RAM disponible.

4. **Persistencia de datos**: Los volúmenes Docker mantienen los datos entre reinicios:
   - `postgres_data`: Datos de PostgreSQL
   - `mongo_data`: Datos de MongoDB  
   - `neo4j_data`: Datos de Neo4j
   - `redis_data`: Datos de Redis
   - `rabbitmq_data`: Datos de RabbitMQ

5. **Hot reload**: Flutter en modo release no tiene hot reload. Para desarrollo, ejecutar Flutter localmente.

### **🔄 Flujo de Desarrollo**

```bash
# Desarrollo de backend
docker-compose up -d postgres mongodb redis neo4j rabbitmq  # Solo infra
# Ejecutar servicios backend localmente para desarrollo

# Desarrollo de frontend  
docker-compose up -d  # Todo el sistema
cd frontend
flutter run -d web-server --web-port 3001  # Puerto diferente para dev
```

### **🎯 Estado del Sistema Completo**

- ✅ **Infraestructura**: PostgreSQL, MongoDB, Redis, Neo4j, RabbitMQ
- ✅ **Backend**: 7 microservicios agénticos completamente dockerizados
- ✅ **Frontend**: Flutter Web dockerizado con hot reload opcional
- ✅ **Orquestación**: docker-compose.yml completo y funcional
- ✅ **Configuración**: Variables de entorno y redes automáticas
- ✅ **Persistencia**: Volúmenes para todos los datos importantes

**¡Todo el sistema Atomia ahora se inicia con un solo comando Docker Compose!** 🎉 