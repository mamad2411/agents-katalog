# GitHub Copilot Instructions — Agentic Healthcare Triage Assistant

> **Purpose:** This file serves as the authoritative context and instruction set for GitHub Copilot across the entire repository. Every suggestion, scaffold, and generation should conform to the architecture, conventions, and constraints described below.

---

## 1. Project Overview

This is a **backend-only, AI-powered healthcare triage system** built for a hackathon. The system autonomously ingests multimodal patient data (text symptoms, PDF medical reports, image URIs), routes it through a deterministic multi-agent pipeline, generates a clinical SBAR report with a severity score, and assigns the patient to an appropriate doctor.

**There is no frontend.** All interaction is via REST API. The AI orchestration is handled entirely by LangGraph agents calling the Groq LLM backend.

---

## 2. Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| LLM Provider | `groq` (Python SDK) | Use `llama3-70b-8192` or `mixtral-8x7b-32768` model |
| Agent Orchestration | `langgraph` | Deterministic state graph, sequential nodes |
| API Framework | `fastapi` + `uvicorn` | Async endpoints, Pydantic request/response models |
| Data Validation | `pydantic` v2 | Strict typing on all LLM outputs and API payloads |
| Database ORM | `sqlalchemy` | SQLite for local dev, PostgreSQL-compatible for prod |
| File Uploads | `python-multipart` | For receiving PDF/image payloads |
| Environment | `python-dotenv` | `.env` file for `GROQ_API_KEY` — never hardcode keys |

### `requirements.txt` (Canonical)
```
fastapi
uvicorn[standard]
groq
langgraph
langchain-core
pydantic>=2.0
sqlalchemy
python-multipart
python-dotenv
aiofiles
```

---

## 3. Repository Structure

```
healthcare-triage/
├── .env                        # GROQ_API_KEY — never commit this
├── .gitignore                  # Must include .env, __pycache__, venv/
├── requirements.txt
├── main.py                     # FastAPI app entrypoint
├── workflow.py                 # LangGraph state graph definition
├── database.py                 # SQLAlchemy engine, session, Base
├── models/
│   ├── __init__.py
│   ├── schemas.py              # Pydantic input/output schemas
│   └── db_models.py            # SQLAlchemy ORM table definitions
├── agents/
│   ├── __init__.py
│   ├── extraction_agent.py     # node_extract_symptoms()
│   ├── reasoning_agent.py      # node_generate_sbar()
│   └── routing_agent.py        # node_route_patient()
├── routers/
│   ├── __init__.py
│   ├── triage.py               # /api/triage/* routes
│   └── doctors.py              # /api/doctors/* routes
└── utils/
    ├── __init__.py
    └── groq_client.py          # Shared Groq client singleton
```

> **Copilot Rule:** Always respect this directory structure. When generating a new function or class, place it in the correct module. Never put agent logic inside `main.py`.

---

## 4. Data Contracts — Pydantic Schemas (`models/schemas.py`)

All LLM inputs and outputs **must** be validated through Pydantic models. Copilot should always generate typed models, never raw dicts.

### 4.1 Input Schemas

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class PatientIntake(BaseModel):
    """Payload received at POST /api/triage/submit"""
    patient_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=130)
    raw_symptoms: str = Field(..., description="Free-text symptom description from patient")
    uploaded_file_uris: Optional[List[str]] = Field(
        default=[], description="S3/local URIs to uploaded PDF reports or images"
    )
```

### 4.2 LangGraph State Schema

```python
from typing import TypedDict, Optional

class TriageState(TypedDict):
    """Shared state object passed between all LangGraph nodes."""
    patient_id: str
    raw_input: str                        # Concatenated raw text from all inputs
    structured_symptoms: Optional[dict]   # Output of Extraction Agent
    sbar_report: Optional[dict]           # Output of Clinical Reasoning Agent
    severity_score: Optional[int]         # 1 (low) to 5 (critical)
    assigned_doctor_id: Optional[int]     # FK to Doctor table
    error: Optional[str]                  # Populated on any agent failure
```

### 4.3 Output / Report Schemas

```python
class SBARReport(BaseModel):
    """Standard clinical SBAR format output from the reasoning agent."""
    situation: str = Field(..., description="Concise summary of the patient's current condition")
    background: str = Field(..., description="Relevant medical history and context")
    assessment: str = Field(..., description="Clinical judgment and differential diagnosis")
    recommendation: str = Field(..., description="Immediate next steps and care pathway")

class DoctorSchema(BaseModel):
    """Doctor record as returned by API responses."""
    id: int
    name: str
    department: str
    current_load: int = Field(..., description="Number of currently assigned active patients")
    is_available: bool
```

### 4.4 API Response Schemas

```python
class TriageSubmitResponse(BaseModel):
    patient_id: str
    status: str = "processing"
    message: str

class TriageStatusResponse(BaseModel):
    patient_id: str
    status: str                           # "processing" | "completed" | "error"
    severity_score: Optional[int]
    sbar_report: Optional[SBARReport]
    assigned_doctor: Optional[DoctorSchema]
```

---

## 5. Database Layer (`database.py` + `models/db_models.py`)

### 5.1 Engine Setup (`database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./triage.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency injector for DB sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 5.2 ORM Models (`models/db_models.py`)

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)   # e.g., "Cardiology", "Emergency"
    current_load = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    patients = relationship("PatientRecord", back_populates="doctor")

class PatientRecord(Base):
    __tablename__ = "patient_records"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)  # UUID string
    patient_name = Column(String)
    age = Column(Integer)
    raw_symptoms = Column(Text)
    structured_symptoms_json = Column(Text)  # JSON string
    sbar_situation = Column(Text)
    sbar_background = Column(Text)
    sbar_assessment = Column(Text)
    sbar_recommendation = Column(Text)
    severity_score = Column(Integer)          # 1-5
    status = Column(String, default="processing")  # processing | completed | error
    assigned_doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    doctor = relationship("Doctor", back_populates="patients")
    prerequisites = Column(Text, default="[]")  # JSON array of doctor-added prerequisites
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

> **Copilot Rule:** Never use raw SQL strings. Always use SQLAlchemy ORM. Always use `get_db()` as a FastAPI `Depends()` injection.

---

## 6. API Layer (`main.py` + `routers/`)

### 6.1 App Entrypoint (`main.py`)

```python
from fastapi import FastAPI
from database import engine, Base
from routers import triage, doctors

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Triage Assistant API",
    description="Agentic multi-modal patient triage system",
    version="1.0.0"
)

app.include_router(triage.router, prefix="/api/triage", tags=["Triage"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### 6.2 Triage Routes (`routers/triage.py`)

```python
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.schemas import PatientIntake, TriageSubmitResponse, TriageStatusResponse
import uuid

router = APIRouter()

@router.post("/submit", response_model=TriageSubmitResponse)
async def submit_triage(
    payload: PatientIntake,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Accepts a patient intake payload. Creates a DB record with status='processing',
    fires the LangGraph workflow as a background task, returns a tracking ID immediately.
    """
    patient_id = str(uuid.uuid4())
    # TODO: Create PatientRecord in DB
    # TODO: background_tasks.add_task(run_triage_workflow, patient_id, payload, db)
    return TriageSubmitResponse(
        patient_id=patient_id,
        status="processing",
        message="Triage pipeline initiated."
    )

@router.get("/status/{patient_id}", response_model=TriageStatusResponse)
def get_triage_status(patient_id: str, db: Session = Depends(get_db)):
    """
    Polls the DB for the completed triage result for a given patient_id.
    Returns 404 if the patient_id is not found.
    """
    # TODO: Query PatientRecord by patient_id
    # TODO: Return structured TriageStatusResponse
    pass
```

### 6.3 Doctor Routes (`routers/doctors.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from typing import List
import json

router = APIRouter()

class DoctorActionPayload(BaseModel):
    patient_id: str
    doctor_id: int
    prerequisite: str  # e.g., "Chest X-Ray", "ECG", "Blood Panel CBC"

@router.get("/dashboard")
def get_doctor_dashboard(doctor_id: int, db: Session = Depends(get_db)):
    """
    Returns all completed patient records assigned to the given doctor_id,
    ordered by severity_score descending (most critical first).
    """
    # TODO: Query PatientRecord filtered by assigned_doctor_id = doctor_id
    pass

@router.post("/action")
def add_prerequisite(payload: DoctorActionPayload, db: Session = Depends(get_db)):
    """
    Allows a doctor to append a diagnostic prerequisite to a patient's record.
    Appends to the JSON array stored in PatientRecord.prerequisites.
    """
    # TODO: Load record, parse prerequisites JSON, append, save
    pass
```

> **Copilot Rule:** All routes must use `Depends(get_db)` for database access. All responses must use typed Pydantic `response_model`. Never return raw dicts from route handlers.

---

## 7. LangGraph Workflow (`workflow.py`)

The pipeline is a **strictly sequential** state machine: `extraction → reasoning → routing`. There is no branching unless an `error` is detected in state.

### 7.1 Graph Structure

```
[START]
   │
   ▼
node_extract_symptoms(state)       ← Extraction Agent (Groq call #1)
   │
   ▼
node_generate_sbar(state)          ← Clinical Reasoning Agent (Groq call #2)
   │
   ▼
node_route_patient(state)          ← Routing Manager (DB query, no Groq call)
   │
   ▼
[END]
```

### 7.2 Scaffold (`workflow.py`)

```python
from langgraph.graph import StateGraph, END
from models.schemas import TriageState

def node_extract_symptoms(state: TriageState) -> TriageState:
    """
    EXTRACTION AGENT
    Input:  state['raw_input'] — combined raw text from all patient sources
    Output: state['structured_symptoms'] — validated dict with keys:
            chief_complaint, symptom_list, duration, severity_indicators, history_flags
    
    Groq Prompt Hint: Instruct the model to return ONLY valid JSON. Parse and validate
    the response against the expected schema before writing to state.
    """
    # TODO: Build Groq prompt with state['raw_input']
    # TODO: Call Groq API via utils/groq_client.py
    # TODO: Parse JSON response into structured_symptoms dict
    # TODO: Handle malformed JSON with a retry or error state
    return state

def node_generate_sbar(state: TriageState) -> TriageState:
    """
    CLINICAL REASONING AGENT
    Input:  state['structured_symptoms'] — output of extraction node
    Output: state['sbar_report'] — SBARReport-compatible dict
            state['severity_score'] — integer 1-5
    
    Groq Prompt Hint: Provide mock clinical triage guidelines in the system prompt.
    The model should reason step-by-step, then output ONLY JSON with keys:
    situation, background, assessment, recommendation, severity_score.
    Severity scale: 1=Non-Urgent, 2=Low, 3=Moderate, 4=High, 5=Critical/Immediate
    """
    # TODO: Build Groq prompt with state['structured_symptoms']
    # TODO: Include clinical guidelines as system context
    # TODO: Parse severity_score (must be int 1-5, validate range)
    # TODO: Populate state['sbar_report'] and state['severity_score']
    return state

def node_route_patient(state: TriageState) -> TriageState:
    """
    ROUTING MANAGER
    Input:  state['severity_score'], state['sbar_report']['recommendation']
    Output: state['assigned_doctor_id']
    
    Logic: 
    - severity 4-5 → Emergency department, pick doctor with lowest current_load
    - severity 3   → Match department from SBAR recommendation
    - severity 1-2 → General Practice, first available
    No Groq call needed here — pure DB lookup.
    """
    # TODO: Parse recommended department from state['sbar_report']
    # TODO: Query DB for available doctors in that department
    # TODO: Select by lowest current_load, set state['assigned_doctor_id']
    return state

# --- Graph Compilation ---

def build_triage_graph():
    graph = StateGraph(TriageState)
    
    graph.add_node("extract", node_extract_symptoms)
    graph.add_node("sbar", node_generate_sbar)
    graph.add_node("route", node_route_patient)
    
    graph.set_entry_point("extract")
    graph.add_edge("extract", "sbar")
    graph.add_edge("sbar", "route")
    graph.add_edge("route", END)
    
    return graph.compile()

triage_graph = build_triage_graph()
```

---

## 8. Groq Client Utility (`utils/groq_client.py`)

```python
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_groq_client() -> Groq:
    """Returns a singleton Groq client. Call this inside agent nodes."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY is not set in environment.")
        _client = Groq(api_key=api_key)
    return _client

def call_groq(system_prompt: str, user_prompt: str, model: str = "llama3-70b-8192") -> str:
    """
    Wrapper for a standard Groq chat completion call.
    Returns the raw text content of the first message choice.
    Always set temperature=0 for deterministic clinical outputs.
    """
    client = get_groq_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=2048
    )
    return response.choices[0].message.content
```

> **Copilot Rule:** All Groq calls must go through `call_groq()`. Never instantiate `Groq()` directly in agent files. Always use `temperature=0` for clinical reasoning tasks.

---

## 9. Mock Database Seed Data

When initializing the app for the first time, seed the `doctors` table with this mock data:

| id | name | department | current_load | is_available |
|----|------|-----------|-------------|-------------|
| 1 | Dr. Priya Sharma | Cardiology | 2 | True |
| 2 | Dr. Arjun Mehta | Emergency | 5 | True |
| 3 | Dr. Leila Hassan | Neurology | 1 | True |
| 4 | Dr. James Okonkwo | General Practice | 3 | True |
| 5 | Dr. Sofia Reyes | Pulmonology | 0 | True |
| 6 | Dr. Wei Zhang | Emergency | 4 | True |
| 7 | Dr. Ananya Iyer | Orthopedics | 2 | True |
| 8 | Dr. Marcus Williams | General Practice | 1 | True |

Seed script should be placed in `utils/seed_db.py` and run once via `python utils/seed_db.py`.

---

## 10. Severity Score Reference

The Clinical Reasoning Agent must score all patients on this scale. Include this in the system prompt verbatim.

| Score | Label | Criteria | Target Department |
|-------|-------|----------|------------------|
| 5 | **Critical** | Chest pain, loss of consciousness, respiratory failure, stroke symptoms | Emergency |
| 4 | **High** | Severe abdominal pain, high fever (>39.5°C), acute allergic reaction | Emergency |
| 3 | **Moderate** | Persistent fever, moderate pain, controlled bleeding, suspected fracture | Specialty (matched) |
| 2 | **Low** | Mild infection, chronic condition flare, minor injury | General Practice |
| 1 | **Non-Urgent** | Routine checkup, prescription renewal, mild cold | General Practice |

---

## 11. Copilot Generation Rules — Critical Conventions

These rules apply to **every file** Copilot generates in this project:

### General
- **Never hardcode secrets.** All API keys and DB URLs come from `os.getenv()` with `python-dotenv`.
- **All agent node functions must accept `TriageState` and return `TriageState`.** Do not change the function signature.
- **Never import `main.py` from other modules.** It is the entrypoint only.

### LLM / Groq
- Always use `temperature=0` for triage-related LLM calls.
- When prompting for structured output, always end system prompts with: *"Respond ONLY with valid JSON. Do not include any preamble, explanation, or markdown code blocks."*
- Always wrap `json.loads()` calls in a `try/except` and set `state['error']` if parsing fails.

### FastAPI
- Use `BackgroundTasks` for kicking off the LangGraph workflow from the submit endpoint. The endpoint should return immediately with a `patient_id` tracking token.
- Use `HTTPException(status_code=404)` when a `patient_id` or `doctor_id` is not found in the DB.
- All routes must have type-annotated parameters.

### SQLAlchemy
- Always call `db.commit()` followed by `db.refresh(instance)` after every write operation.
- Use `db.query(Model).filter(Model.field == value).first()` for single record lookups.
- Never use `db.execute()` with raw SQL strings.

### Pydantic
- Use `model_validate()` (Pydantic v2) instead of `parse_obj()`.
- Add `Field(description="...")` to all model fields to serve as inline API documentation.

---

## 12. Environment Setup Checklist

```bash
# 1. Clone and enter repo
git clone <repo-url> && cd healthcare-triage

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "DATABASE_URL=sqlite:///./triage.db" >> .env

# 5. Seed the database
python utils/seed_db.py

# 6. Start the development server
uvicorn main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

---

## 13. Team Branch Strategy

| Branch | Owner | Scope |
|--------|-------|-------|
| `main` | All | Skeleton only — protected, PR required |
| `feat/extraction-agent` | Dev A | `agents/extraction_agent.py` — Groq prompts + JSON parsing |
| `feat/reasoning-agent` | Dev B | `agents/reasoning_agent.py` — SBAR + severity scoring |
| `feat/routing-manager` | Dev C | `agents/routing_agent.py` + DB queries |
| `feat/api-routes` | Dev D | `routers/triage.py` + `routers/doctors.py` completion |

> Each branch should only touch files within its scope. Cross-cutting changes require a PR review from at least one other team member.

---

*Last updated: Hackathon kickoff — generated for GitHub Copilot context injection.*
