# Code Manager Skill

> GitHub 코드 분석 에이전트

---

## 역할

GitHub 레포지토리를 클론하고 Python 코드를 분석하여 질문 생성에 필요한 정보를 추출합니다.

## 책임

1. **레포지토리 클론**: Git으로 소스 코드 다운로드
2. **파일 필터링**: Python 파일만 선별
3. **AST 분석**: 추상 구문 트리로 코드 구조 파악
4. **패턴 탐지**: 디자인 패턴, 코딩 관습 식별
5. **주목할 구현 추출**: 질문 생성에 적합한 코드 발견
6. **벡터 저장**: 분석 결과를 벡터 스토어에 저장

---

## Activity 정의

### analyze_code

```python
@activity.defn
async def analyze_code(job_id: str, github_urls: list[str]) -> dict:
    """
    GitHub 코드 분석

    Input:
        job_id: 작업 ID
        github_urls: GitHub 레포지토리 URL 목록

    Output:
        CodeAnalysis: {
            repositories: list[RepositoryAnalysis],
            combined_tech_stack: list[str],
            total_patterns: int,
            total_notable_implementations: int,
            top_question_candidates: list[NotableImplementation],
        }
    """
```

---

## Git 클론 전략

```python
import subprocess
import tempfile
from pathlib import Path

async def clone_repository(url: str, job_id: str) -> Path:
    """
    레포지토리 클론

    전략:
    1. Shallow clone (depth=1) - 최신 커밋만
    2. Python 관련 파일만 sparse checkout
    3. 임시 디렉토리에 저장
    """
    # 임시 디렉토리 생성
    work_dir = Path(tempfile.mkdtemp(prefix=f"vantict_{job_id}_"))

    # Sparse checkout 설정
    subprocess.run([
        "git", "clone",
        "--depth", "1",
        "--filter=blob:none",
        "--sparse",
        url,
        str(work_dir / "repo")
    ], check=True)

    # Python 파일만 checkout
    subprocess.run([
        "git", "-C", str(work_dir / "repo"),
        "sparse-checkout", "set",
        "*.py", "requirements.txt", "pyproject.toml", "setup.py"
    ], check=True)

    return work_dir / "repo"


async def cleanup_repository(repo_path: Path) -> None:
    """클론된 레포지토리 정리"""
    import shutil
    shutil.rmtree(repo_path.parent, ignore_errors=True)
```

---

## AST 분석

### Python 코드 파서

```python
import ast
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class FunctionInfo:
    """함수 정보"""
    name: str
    file_path: str
    line_start: int
    line_end: int
    args: List[str]
    decorators: List[str]
    docstring: str | None
    complexity: int
    code: str

@dataclass
class ClassInfo:
    """클래스 정보"""
    name: str
    file_path: str
    line_start: int
    line_end: int
    bases: List[str]
    methods: List[FunctionInfo]
    decorators: List[str]
    docstring: str | None


class PythonAnalyzer(ast.NodeVisitor):
    """Python AST 분석기"""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.lines = source_code.split("\n")

        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.imports: List[str] = []

    def analyze(self) -> Dict[str, Any]:
        """파일 분석 실행"""
        try:
            tree = ast.parse(self.source_code)
            self.visit(tree)
        except SyntaxError:
            pass

        return {
            "file_path": self.file_path,
            "functions": self.functions,
            "classes": self.classes,
            "imports": self.imports,
            "total_lines": len(self.lines),
        }

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """함수 정의 방문"""
        func_info = FunctionInfo(
            name=node.name,
            file_path=self.file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            args=[arg.arg for arg in node.args.args],
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            docstring=ast.get_docstring(node),
            complexity=self._calculate_complexity(node),
            code=self._extract_code(node.lineno, node.end_lineno),
        )
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """클래스 정의 방문"""
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(FunctionInfo(
                    name=item.name,
                    file_path=self.file_path,
                    line_start=item.lineno,
                    line_end=item.end_lineno or item.lineno,
                    args=[arg.arg for arg in item.args.args],
                    decorators=[self._get_decorator_name(d) for d in item.decorator_list],
                    docstring=ast.get_docstring(item),
                    complexity=self._calculate_complexity(item),
                    code=self._extract_code(item.lineno, item.end_lineno),
                ))

        class_info = ClassInfo(
            name=node.name,
            file_path=self.file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            bases=[self._get_base_name(b) for b in node.bases],
            methods=methods,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            docstring=ast.get_docstring(node),
        )
        self.classes.append(class_info)
        self.generic_visit(node)

    def _calculate_complexity(self, node: ast.AST) -> int:
        """순환 복잡도 계산"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _extract_code(self, start: int, end: int) -> str:
        """코드 추출"""
        return "\n".join(self.lines[start-1:end])
```

---

## 패턴 탐지

### 디자인 패턴 탐지기

```python
PATTERN_SIGNATURES = {
    "singleton": {
        "indicators": [
            "private class variable named _instance",
            "classmethod or staticmethod for instance creation",
            "__new__ method with instance check",
        ],
        "code_patterns": [
            r"_instance\s*=\s*None",
            r"def\s+(get_instance|instance)\s*\(",
            r"if\s+(cls|self)\._instance\s+is\s+None",
        ],
    },
    "factory": {
        "indicators": [
            "method that returns different types based on input",
            "abstract base class with concrete implementations",
        ],
        "code_patterns": [
            r"def\s+create_\w+\s*\(",
            r"if\s+\w+\s*==\s*['\"].*['\"]\s*:\s*return\s+\w+\(",
        ],
    },
    "decorator_pattern": {
        "indicators": [
            "wrapper function inside another function",
            "functools.wraps usage",
        ],
        "code_patterns": [
            r"def\s+\w+\([^)]*func[^)]*\):",
            r"@functools\.wraps",
            r"def\s+wrapper\s*\(",
        ],
    },
    "repository": {
        "indicators": [
            "class with CRUD methods",
            "database session injection",
        ],
        "code_patterns": [
            r"def\s+(get|find|create|update|delete)_\w+\s*\(",
            r"session:\s*Session",
        ],
    },
    "service_layer": {
        "indicators": [
            "business logic encapsulation",
            "transaction management",
        ],
        "code_patterns": [
            r"class\s+\w+Service\s*[:\(]",
            r"@transactional",
        ],
    },
}


async def detect_patterns(analysis: Dict[str, Any]) -> List[Dict]:
    """
    코드에서 패턴 탐지

    Returns:
        [
            {
                "pattern_type": "design_pattern",
                "name": "Singleton",
                "file_path": "...",
                "evidence": "...",
                "confidence": 0.9,
            }
        ]
    """
    detected = []

    for class_info in analysis.get("classes", []):
        for pattern_name, signature in PATTERN_SIGNATURES.items():
            confidence = check_pattern_match(class_info, signature)
            if confidence > 0.7:
                detected.append({
                    "pattern_type": "design_pattern",
                    "name": pattern_name.replace("_", " ").title(),
                    "file_path": class_info.file_path,
                    "line_start": class_info.line_start,
                    "line_end": class_info.line_end,
                    "evidence": class_info.code[:500],
                    "confidence": confidence,
                })

    return detected
```

---

## 주목할 구현 추출

```python
async def find_notable_implementations(
    analysis: Dict[str, Any],
    llm_client
) -> List[Dict]:
    """
    질문 생성에 적합한 주목할 만한 구현 찾기

    기준:
    1. 복잡도가 적절한 함수 (5-15)
    2. 명확한 비즈니스 로직
    3. 외부 라이브러리 활용
    4. 에러 처리 로직
    5. 캐싱/최적화 로직
    """
    candidates = []

    # 복잡도 기준 필터링
    for func in analysis.get("functions", []):
        if 5 <= func.complexity <= 15:
            candidates.append({
                "type": "function",
                "name": func.name,
                "file_path": func.file_path,
                "line_start": func.line_start,
                "line_end": func.line_end,
                "code": func.code,
                "complexity": func.complexity,
                "has_docstring": bool(func.docstring),
            })

    # LLM으로 질문 가능성 평가
    notable = []
    for candidate in candidates[:20]:  # 상위 20개만 평가
        evaluation = await llm_client.evaluate_question_potential(
            code=candidate["code"],
            context={
                "file_path": candidate["file_path"],
                "complexity": candidate["complexity"],
            }
        )

        if evaluation["score"] > 0.6:
            notable.append({
                **candidate,
                "title": evaluation["title"],
                "why_notable": evaluation["reason"],
                "question_potential": evaluation["score"],
                "suggested_questions": evaluation.get("suggested_questions", []),
            })

    # 점수 순 정렬
    notable.sort(key=lambda x: x["question_potential"], reverse=True)

    return notable[:10]  # 상위 10개
```

---

## 벡터 저장

```python
async def store_code_vectors(job_id: str, analysis: Dict) -> None:
    """
    코드 분석 결과를 벡터 스토어에 저장
    """
    vector_store = get_vector_store(job_id)

    # 주목할 구현 저장
    for impl in analysis.get("notable_implementations", []):
        await vector_store.upsert(
            id=f"code_{impl['file_path']}_{impl['line_start']}",
            content=f"{impl['title']}: {impl['code'][:1000]}",
            metadata={
                "type": "notable_implementation",
                "file_path": impl["file_path"],
                "line_start": impl["line_start"],
                "line_end": impl["line_end"],
                "question_potential": impl["question_potential"],
            }
        )

    # 패턴 저장
    for pattern in analysis.get("patterns", []):
        await vector_store.upsert(
            id=f"pattern_{pattern['file_path']}_{pattern['line_start']}",
            content=f"{pattern['name']} pattern: {pattern['evidence']}",
            metadata={
                "type": "pattern",
                "pattern_name": pattern["name"],
                "file_path": pattern["file_path"],
            }
        )
```

---

## 출력 예시

```json
{
  "repositories": [
    {
      "repo_url": "https://github.com/user/backend-api",
      "repo_name": "backend-api",
      "language": "Python",
      "total_files": 45,
      "analyzed_files": 38,
      "tech_stack": ["FastAPI", "SQLAlchemy", "Redis", "Celery"],
      "patterns": [
        {
          "pattern_type": "design_pattern",
          "name": "Repository",
          "file_path": "app/repositories/user_repository.py",
          "line_start": 10,
          "line_end": 45,
          "confidence": 0.92
        }
      ],
      "complexity": {
        "total_lines": 3200,
        "code_lines": 2100,
        "comment_lines": 450,
        "avg_function_length": 18.5,
        "max_function_length": 67,
        "cyclomatic_complexity_avg": 4.2
      },
      "notable_implementations": [
        {
          "title": "Redis 캐싱이 적용된 사용자 조회",
          "file_path": "app/services/user_service.py",
          "line_start": 25,
          "line_end": 48,
          "code": "async def get_user_with_cache(self, user_id: int):\n    cache_key = f'user:{user_id}'\n    cached = await self.redis.get(cache_key)\n    ...",
          "why_notable": "캐시 전략, TTL 설정, 캐시 무효화 로직이 포함되어 있어 심층적인 질문이 가능",
          "question_potential": 0.89
        }
      ]
    }
  ],
  "combined_tech_stack": ["FastAPI", "SQLAlchemy", "Redis", "Celery"],
  "total_patterns": 5,
  "total_notable_implementations": 12,
  "top_question_candidates": [...]
}
```

---

## 관련 파일

- `backend/app/workflows/activities/code_analysis.py`
- `backend/app/services/code_analyzer.py`
- `backend/app/services/github_service.py`

---

## 의존성

- **외부 서비스**: GitHub (클론), LLM (평가)
- **내부 서비스**: Vector Store (저장)
- **라이브러리**: git, ast (Python 내장)
