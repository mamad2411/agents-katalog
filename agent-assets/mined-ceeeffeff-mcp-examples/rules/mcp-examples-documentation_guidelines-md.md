# Documentation Guidelines for Multi-Service Projects

**Rule:** When documenting setup for multi-service projects with varied dependency managers, leverage existing READMEs and dependency files, verify critical version-specific notes, and cross-check with configuration files to ensure accuracy.

**Key Actions:**
1. **Use Existing Documentation:** Base your setup instructions on READMEs and dependency files (e.g., `pyproject.toml`, `package.json`, `requirements.txt`).
2. **Verify Version-Specific Notes:** Flag critical version dependencies (e.g., `huggingface-hub==0.34.2`) to avoid compatibility issues.
3. **Cross-Reference Configs:** Ensure configuration files (e.g., `agent/agent.json`, `main.py`) are explicitly mentioned in setup steps.
4. **Clarify Prerequisites:** Add "Prerequisites" sections for inter-service dependencies (e.g., requiring Gradio servers to be running before starting hosts).

**General Use Case:**  
This approach applies to projects with multiple services using different package managers (UV, npm, pip) or configuration formats. It ensures consistency, reduces ambiguity, and prevents version-related issues.
