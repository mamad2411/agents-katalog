#!/usr/bin/env python3
"""
Skill Graph API — Bridge Obsidian Skill Graph ke LLM
=====================================================
HTTP server di localhost:27125 yang ngasih LLM akses ke:
- /search?q=keyword       → cari skill by name/tag
- /related?skill=X       → skill terkait via graph links
- /category?name=AI      → semua skill di kategori
- /load?skill=X          → load full skill content (gzip decompress)
- /quality?skill=X       → quality score + usage stats
- /combinations?skill=X  → rekomendasi skill stacking
- /stats                 → statistik total skill, kategori, usage
- /moc                   → list semua MOC (Map of Content)
- /health                → health check

Zero idle cost: server cuma jalan saat dipanggil.
Token efficient: response di-cap 2000 chars, JSON compact.

Extended with repo reference endpoints:
- /repos                 → list all repo references
- /repos/search?q=keyword → search repos by name/tech
- /repos/tree?name=X      → get file tree of a repo
- /repos/readme?name=X    → get README of a repo
- /repos/structure?name=X → get structure overview for AI learning
"""

import json
import os
import sys
import gzip
import re
import glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import repo reference module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import repo_ref_api
    REPO_ROUTES = repo_ref_api.REPO_ROUTES
except ImportError:
    REPO_ROUTES = {}

VAULT = os.path.expanduser("~/mamatXobsidian")
SKILLS_DIR = os.path.join(VAULT, "05 - Resources", "Skills")
CATALOG = os.path.expanduser("~/.agents/skills-catalog")
MASTER_INDEX = os.path.join(CATALOG, "skill_master_index.json")
EFFICACY_LOG = os.path.expanduser("~/.agents/skill-efficacy-log.json")
QUALITY_SCORES = os.path.expanduser("~/.agents/skill-quality-scores.json")
COMBINATIONS = os.path.expanduser("~/.agents/skill-combinations.json")
PORT = 27125
MAX_RESPONSE_CHARS = 2000

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def truncate(s, maxlen=MAX_RESPONSE_CHARS):
    if len(s) > maxlen:
        return s[:maxlen] + "\n... [truncated]"
    return s

def parse_stub(filepath):
    """Parse skill stub note: frontmatter + category link."""
    try:
        with open(filepath, "r") as f:
            content = f.read(2000)
        fm = {}
        if content.startswith("---"):
            fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
            if fm_match:
                for line in fm_match.group(1).split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        fm[k.strip()] = v.strip().strip('"').strip("'")
        # Extract category from [[X MOC]] link
        cat_match = re.search(r"\[\[(.+?)\s+MOC\]\]", content)
        category = cat_match.group(1) if cat_match else fm.get("category", "Unknown")
        return {"frontmatter": fm, "category": category}
    except Exception:
        return None

def get_all_skills():
    """Get all skill names from master index."""
    idx = load_json(MASTER_INDEX, {"skills": []})
    return idx.get("skills", [])

def get_skill_stub(skill_name):
    """Read skill stub from Obsidian."""
    path = os.path.join(SKILLS_DIR, f"{skill_name}.md")
    return parse_stub(path) if os.path.exists(path) else None

def load_full_skill(skill_name):
    """Load full skill content from gzip catalog."""
    gz_path = os.path.join(CATALOG, f"{skill_name}.md.gz")
    md_path = os.path.join(CATALOG, f"{skill_name}.md")
    if os.path.exists(gz_path):
        try:
            with gzip.open(gz_path, "rt") as f:
                return f.read(5000)
        except Exception:
            return None
    elif os.path.exists(md_path):
        try:
            with open(md_path, "r") as f:
                return f.read(5000)
        except Exception:
            return None
    return None

def get_related_skills(skill_name, limit=10):
    """Find related skills via category + shared tags."""
    stub = get_skill_stub(skill_name)
    if not stub:
        return []
    category = stub.get("category", "General")
    # Find all skills in same category
    related = []
    for s in get_all_skills():
        if s == skill_name:
            continue
        s_stub = get_skill_stub(s)
        if s_stub and s_stub.get("category") == category:
            related.append(s)
            if len(related) >= limit:
                break
    # Also check combinations log
    combos = load_json(COMBINATIONS, {"pairs": {}})
    for pair_key, data in combos.get("pairs", {}).items():
        if skill_name in pair_key:
            other = pair_key.replace(skill_name, "").replace("|", "").strip()
            if other and other not in related:
                related.insert(0, other)
    return related[:limit]

def get_category_skills(category):
    """Get all skills in a category."""
    results = []
    for s in get_all_skills():
        stub = get_skill_stub(s)
        if stub and stub.get("category", "").lower() == category.lower():
            results.append(s)
    return results

def get_all_mocs():
    """List all MOC notes."""
    mocs = []
    for f in glob.glob(os.path.join(SKILLS_DIR, "*MOC.md")):
        mocs.append(os.path.basename(f).replace(".md", ""))
    return mocs

def get_quality_scores():
    return load_json(QUALITY_SCORES, {"scores": {}})

def get_skill_quality(skill_name):
    scores = get_quality_scores()
    return scores.get("scores", {}).get(skill_name, {
        "rating": 3, "uses": 0, "last_used": None, "success_rate": 0.5
    })

def get_combinations(skill_name):
    combos = load_json(COMBINATIONS, {"pairs": {}})
    results = []
    for pair_key, data in combos.get("pairs", {}).items():
        if skill_name in pair_key:
            results.append({"pair": pair_key, **data})
    return results

def get_stats():
    skills = get_all_skills()
    scores = get_quality_scores()
    combos = load_json(COMBINATIONS, {"pairs": {}})
    efficacy = load_json(EFFICACY_LOG, {"runs": []})
    return {
        "total_skills": len(skills),
        "categories": len(get_all_mocs()),
        "quality_scored": len(scores.get("scores", {})),
        "combinations_tracked": len(combos.get("pairs", {})),
        "efficacy_runs": len(efficacy.get("runs", [])),
        "vault_path": VAULT,
        "catalog_path": CATALOG,
    }

class SkillAPIHandler(BaseHTTPRequestHandler):
    
    def _send_json(self, data, code=200):
        body = truncate(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
    
    def _send_text(self, text, code=200):
        text = truncate(text)
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))
    
    def log_message(self, format, *args):
        pass  # Silent — zero console overhead
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        path = parsed.path.rstrip("/")
        
        if path == "/health":
            self._send_json({"status": "ok", "port": PORT, "skills": len(get_all_skills())})
        
        elif path == "/search":
            q = params.get("q", [""])[0].lower()
            if not q:
                return self._send_json({"error": "missing q param"})
            matches = [s for s in get_all_skills() if q in s.lower()][:20]
            self._send_json({"query": q, "count": len(matches), "skills": matches})
        
        elif path == "/related":
            skill = params.get("skill", [""])[0]
            if not skill:
                return self._send_json({"error": "missing skill param"})
            related = get_related_skills(skill)
            self._send_json({"skill": skill, "related": related, "count": len(related)})
        
        elif path == "/category":
            cat = params.get("name", [""])[0]
            if not cat:
                mocs = get_all_mocs()
                return self._send_json({"categories": mocs})
            skills = get_category_skills(cat)
            self._send_json({"category": cat, "count": len(skills), "skills": skills[:50]})
        
        elif path == "/load":
            skill = params.get("skill", [""])[0]
            if not skill:
                return self._send_json({"error": "missing skill param"})
            content = load_full_skill(skill)
            if content:
                self._send_text(content)
            else:
                self._send_json({"error": f"skill not found: {skill}"}, 404)
        
        elif path == "/quality":
            skill = params.get("skill", [""])[0]
            if not skill:
                scores = get_quality_scores()
                return self._send_json({"scores": dict(list(scores.get("scores", {}).items())[:20])})
            q = get_skill_quality(skill)
            self._send_json({"skill": skill, **q})
        
        elif path == "/combinations":
            skill = params.get("skill", [""])[0]
            if not skill:
                combos = load_json(COMBINATIONS, {"pairs": {}})
                pairs = dict(list(combos.get("pairs", {}).items())[:20])
                return self._send_json({"combinations": pairs})
            results = get_combinations(skill)
            self._send_json({"skill": skill, "combinations": results})
        
        elif path == "/stats":
            self._send_json(get_stats())
        
        elif path == "/moc":
            self._send_json({"mocs": get_all_mocs()})
        
        elif REPO_ROUTES:
            # Repo reference routes
            for route_path, handler in REPO_ROUTES.items():
                if path == route_path:
                    result = handler(params)
                    return self._send_json(result)
            self._send_json({
                "endpoints": {
                    "/search?q=keyword": "Search skills by name",
                    "/related?skill=X": "Get related skills via graph",
                    "/category?name=X": "Get all skills in category",
                    "/load?skill=X": "Load full skill content (gzipped)",
                    "/quality?skill=X": "Get quality score + usage stats",
                    "/combinations?skill=X": "Get recommended skill combinations",
                    "/stats": "Get ecosystem statistics",
                    "/moc": "List all MOC categories",
                    "/health": "Health check",
                    "/repos": "List all repo references",
                    "/repos/search?q=keyword": "Search repos by name/tech",
                    "/repos/tree?name=X": "Get file tree of a repo",
                    "/repos/readme?name=X": "Get README of a repo",
                    "/repos/structure?name=X": "Get structure overview for AI learning",
                }
            })
        else:
            self._send_json({
                "endpoints": {
                    "/search?q=keyword": "Search skills by name",
                    "/related?skill=X": "Get related skills via graph",
                    "/category?name=X": "Get all skills in category",
                    "/load?skill=X": "Load full skill content (gzipped)",
                    "/quality?skill=X": "Get quality score + usage stats",
                    "/combinations?skill=X": "Get recommended skill combinations",
                    "/stats": "Get ecosystem statistics",
                    "/moc": "List all MOC categories",
                    "/health": "Health check",
                }
            })
    
    def do_POST(self):
        """Write endpoints: record efficacy, update quality, log combination."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}
        except (json.JSONDecodeError, ValueError):
            body = {}
        
        if path == "/quality/update":
            skill = body.get("skill")
            rating = body.get("rating", 3)
            success = body.get("success", True)
            if not skill:
                return self._send_json({"error": "missing skill"}, 400)
            scores = load_json(QUALITY_SCORES, {"scores": {}})
            current = scores["scores"].get(skill, {"rating": 3, "uses": 0, "last_used": None, "success_rate": 0.5})
            current["uses"] += 1
            current["last_used"] = body.get("timestamp", "")
            current["rating"] = max(1, min(5, rating))
            old_rate = current["success_rate"]
            new_success = 1.0 if success else 0.0
            current["success_rate"] = (old_rate * (current["uses"] - 1) + new_success) / current["uses"]
            scores["scores"][skill] = current
            save_json(QUALITY_SCORES, scores)
            self._send_json({"status": "updated", "skill": skill, **current})
        
        elif path == "/efficacy/log":
            skill = body.get("skill")
            score = body.get("score", 50)
            if not skill:
                return self._send_json({"error": "missing skill"}, 400)
            log = load_json(EFFICACY_LOG, {"runs": []})
            log["runs"].append({"skill": skill, "score": score, "timestamp": body.get("timestamp", "")})
            log["runs"] = log["runs"][-200:]  # Keep last 200
            save_json(EFFICACY_LOG, log)
            self._send_json({"status": "logged", "skill": skill, "score": score})
        
        elif path == "/combination/log":
            skills = body.get("skills", [])
            success = body.get("success", True)
            if len(skills) < 2:
                return self._send_json({"error": "need 2+ skills"}, 400)
            pair_key = "|".join(sorted(skills[:2]))
            combos = load_json(COMBINATIONS, {"pairs": {}})
            current = combos["pairs"].get(pair_key, {"count": 0, "success_rate": 0.5})
            current["count"] += 1
            new_success = 1.0 if success else 0.0
            current["success_rate"] = (current["success_rate"] * (current["count"] - 1) + new_success) / current["count"]
            combos["pairs"][pair_key] = current
            save_json(COMBINATIONS, combos)
            self._send_json({"status": "logged", "pair": pair_key, **current})
        
        else:
            self._send_json({"error": "unknown endpoint", "post_endpoints": ["/quality/update", "/efficacy/log", "/combination/log"]}, 404)

def main():
    os.makedirs(os.path.expanduser("~/.agents"), exist_ok=True)
    # Initialize empty files if not exist
    for path, default in [
        (EFFICACY_LOG, {"runs": []}),
        (QUALITY_SCORES, {"scores": {}}),
        (COMBINATIONS, {"pairs": {}}),
    ]:
        if not os.path.exists(path):
            save_json(path, default)
    
    server = HTTPServer(("127.0.0.1", PORT), SkillAPIHandler)
    print(f"Skill Graph API running on http://127.0.0.1:{PORT}")
    print(f"Endpoints: /search /related /category /load /quality /combinations /stats /moc /health")
    print(f"Skills available: {len(get_all_skills())}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()

if __name__ == "__main__":
    main()
