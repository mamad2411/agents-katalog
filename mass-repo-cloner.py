#!/usr/bin/env python3
"""
Mass Repo Reference Cloner
==========================
Clones README + file tree (depth 2) from 14,000+ curated repos.
NOT full code — just structure for AI reference.

Strategy:
- Batch: 50 repos per batch
- Delay: 2s between batches (thermal guard)
- Max 3 batches per minute
- Each repo: git sparse-checkout (README only) → TREE.txt → remove .git
- Skip if already exists
- Resume capability: if interrupted, re-run picks up where left off

Usage:
  python3 mass-repo-cloner.py              # Start/resume cloning
  python3 mass-repo-cloner.py --status     # Show progress
  python3 mass-repo-cloner.py --index      # Rebuild master index
"""

import os
import sys
import json
import time
import subprocess
import shutil
from datetime import datetime

REPO_LIST = "/tmp/all-repos.json"
REFS_DIR = os.path.expanduser("~/.agents/repo-refs")
INDEX_FILE = os.path.join(REFS_DIR, "repo-master-index.json")
LOG_FILE = os.path.expanduser("~/.agents/repo-clone-progress.json")
BATCH_SIZE = 50
BATCH_DELAY = 2  # seconds between batches
MAX_REPOS = 10000  # Cap at 10K to stay reasonable

def load_repo_list():
    with open(REPO_LIST) as f:
        return json.load(f)

def load_progress():
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"completed": [], "failed": [], "last_batch": 0, "total_started": 0}

def save_progress(progress):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def clone_repo(repo_full, target_dir):
    """Clone only README via sparse checkout, generate TREE.txt, remove .git."""
    url = f"https://github.com/{repo_full}"
    name = repo_full.replace("/", "_")
    repo_path = os.path.join(target_dir, name)
    
    if os.path.exists(repo_path):
        return "skip"
    
    try:
        # Sparse clone — minimal download
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", url, repo_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return "fail"
        
        # Sparse checkout: README files + top-level structure
        os.chdir(repo_path)
        subprocess.run(
            ["git", "sparse-checkout", "set", "README.md", "README", "README.rst", "docs"],
            capture_output=True, text=True, timeout=10
        )
        
        # Generate TREE.txt (depth 2, no .git)
        tree = subprocess.run(
            ["find", ".", "-maxdepth", "2", "-not", "-path", "./.git/*"],
            capture_output=True, text=True, timeout=10
        )
        with open(os.path.join(repo_path, "TREE.txt"), "w") as f:
            f.write(tree.stdout[:3000])
        
        # Generate STUB.md (compact summary for AI)
        readme_content = ""
        for readme_name in ["README.md", "README", "README.rst"]:
            readme_path = os.path.join(repo_path, readme_name)
            if os.path.exists(readme_path):
                with open(readme_path, errors="ignore") as f:
                    readme_content = f.read()[:2000]
                break
        
        stub = f"""# {repo_full}

Source: {url}
Cloned: {datetime.now().isoformat()[:10]}

## Structure
{tree.stdout[:1500]}

## README (first 500 chars)
{readme_content[:500]}
"""
        with open(os.path.join(repo_path, "STUB.md"), "w") as f:
            f.write(stub)
        
        # Remove .git to save space
        shutil.rmtree(os.path.join(repo_path, ".git"), ignore_errors=True)
        
        # Thermal guard
        open(os.path.join(repo_path, ".metadata_never_index"), "w").close()
        
        return "ok"
    
    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        return f"error: {str(e)[:50]}"
    finally:
        # Make sure we're back in a safe dir
        os.chdir(os.path.expanduser("~"))

def run_batch(repos, batch_num, progress):
    """Clone a batch of repos."""
    results = {"ok": 0, "fail": 0, "skip": 0, "timeout": 0}
    
    for repo in repos:
        status = clone_repo(repo, REFS_DIR)
        if status == "ok":
            results["ok"] += 1
            progress["completed"].append(repo)
        elif status == "skip":
            results["skip"] += 1
        elif status == "timeout":
            results["timeout"] += 1
            progress["failed"].append(repo)
        else:
            results["fail"] += 1
            progress["failed"].append(repo)
    
    progress["last_batch"] = batch_num
    save_progress(progress)
    return results

def show_status():
    progress = load_progress()
    try:
        total = len(load_repo_list())
    except:
        total = 0
    completed = len(progress.get("completed", []))
    failed = len(progress.get("failed", []))
    remaining = total - completed - failed
    
    print(f"=== REPO CLONE PROGRESS ===")
    print(f"Total repos in list: {total}")
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Remaining: {remaining}")
    print(f"Last batch: #{progress.get('last_batch', 0)}")
    pct = ((completed+failed)/total*100) if total > 0 else 0
    print(f"Progress: {pct:.1f}%")
    
    # Count actual dirs
    if os.path.exists(REFS_DIR):
        actual = len([d for d in os.listdir(REFS_DIR) if os.path.isdir(os.path.join(REFS_DIR, d)) and not d.startswith(".")])
        print(f"Actual dirs in repo-refs: {actual}")

def rebuild_index():
    """Rebuild master index from cloned repos."""
    repos = []
    if not os.path.exists(REFS_DIR):
        print("No repo-refs directory found.")
        return
    
    for name in sorted(os.listdir(REFS_DIR)):
        path = os.path.join(REFS_DIR, name)
        if not os.path.isdir(path) or name.startswith("."):
            continue
        
        stub_path = os.path.join(path, "STUB.md")
        tree_preview = ""
        if os.path.exists(stub_path):
            with open(stub_path, errors="ignore") as f:
                tree_preview = f.read()[:500]
        
        # Get size
        try:
            size = subprocess.run(["du", "-sh", path], capture_output=True, text=True).stdout.split("\t")[0]
        except:
            size = "?"
        
        repos.append({
            "name": name,
            "path": path,
            "size": size,
            "stub_preview": tree_preview[:300],
        })
    
    index = {"version": "1.0", "count": len(repos), "repos": repos, "updated": datetime.now().isoformat()}
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)
    print(f"Index rebuilt: {len(repos)} repos at {INDEX_FILE}")

def main():
    os.makedirs(REFS_DIR, exist_ok=True)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        show_status()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--index":
        rebuild_index()
        return
    
    # Start/resume cloning
    all_repos = load_repo_list()
    progress = load_progress()
    
    # Filter out already completed/failed
    done = set(progress.get("completed", []) + progress.get("failed", []))
    remaining = [r for r in all_repos if r not in done][:MAX_REPOS]
    
    print(f"=== MASS REPO CLONER ===")
    print(f"Total repos: {len(all_repos)}")
    print(f"Already done: {len(done)}")
    print(f"To clone: {len(remaining)}")
    print(f"Batch size: {BATCH_SIZE}, delay: {BATCH_DELAY}s")
    print()
    
    batch_num = progress.get("last_batch", 0)
    
    for i in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[i:i + BATCH_SIZE]
        batch_num += 1
        
        print(f"Batch #{batch_num}: {len(batch)} repos ({i+1}-{i+len(batch)}/{len(remaining)})")
        results = run_batch(batch, batch_num, progress)
        print(f"  ok={results['ok']} fail={results['fail']} skip={results['skip']} timeout={results['timeout']}")
        
        # Thermal guard: delay between batches
        if i + BATCH_SIZE < len(remaining):
            time.sleep(BATCH_DELAY)
    
    print(f"\n=== DONE ===")
    print(f"Total completed: {len(progress.get('completed', []))}")
    print(f"Total failed: {len(progress.get('failed', []))}")
    
    # Rebuild index
    rebuild_index()
    show_status()

if __name__ == "__main__":
    main()
