#!/usr/bin/env python3
"""
Dynamic MCP Proxy Manager
=========================
Manages tool promotion/demotion based on usage.
- Fixed tools: always available (search, load, related)
- Dynamic tools: promoted after 3 calls, demoted after 7 days unused
- Max 5 dynamic tools at any time
- Output capped at 600 chars per tool response

Usage:
  python3 mcp-proxy-manager.py record <tool_name>   # Record a tool call
  python3 mcp-proxy-manager.py status               # Show current tool status
  python3 mcp-proxy-manager.py tools                # List active tools (for LLM)
  python3 mcp-proxy-manager.py cleanup              # Demote stale tools
"""

import json
import os
import sys
from datetime import datetime, timedelta

PROXY_CONFIG = os.path.expanduser("~/.agents/mcp-dynamic-proxy.json")
CALL_LOG = os.path.expanduser("~/.agents/mcp-call-history.json")

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

def record_call(tool_name):
    config = load_json(PROXY_CONFIG, {"call_history": {}, "dynamic_tools": {}, "promotion_rules": {}})
    history = config.get("call_history", {})
    
    entry = history.get(tool_name, {"count": 0, "last_called": None, "promoted": False})
    entry["count"] += 1
    entry["last_called"] = datetime.now().isoformat()
    
    # Check promotion
    rules = config.get("promotion_rules", {})
    promote_threshold = rules.get("promote_after_calls", 3)
    max_dynamic = rules.get("max_dynamic_tools", 5)
    
    if entry["count"] >= promote_threshold and not entry.get("promoted", False):
        dynamic = config.get("dynamic_tools", {})
        if len(dynamic) < max_dynamic:
            dynamic[tool_name] = {
                "promoted_at": datetime.now().isoformat(),
                "call_count": entry["count"],
                "last_called": entry["last_called"],
            }
            entry["promoted"] = True
            config["dynamic_tools"] = dynamic
            print(f"PROMOTED: {tool_name} (after {entry['count']} calls)")
        else:
            # Evict least recently used dynamic tool
            lru_tool = min(dynamic, key=lambda k: dynamic[k].get("last_called", ""))
            del dynamic[lru_tool]
            dynamic[tool_name] = {
                "promoted_at": datetime.now().isoformat(),
                "call_count": entry["count"],
                "last_called": entry["last_called"],
            }
            entry["promoted"] = True
            # Demote evicted tool
            if lru_tool in history:
                history[lru_tool]["promoted"] = False
            config["dynamic_tools"] = dynamic
            print(f"PROMOTED: {tool_name} (evicted {lru_tool})")
    
    history[tool_name] = entry
    config["call_history"] = history
    config["status"] = "active"
    save_json(PROXY_CONFIG, config)

def show_status():
    config = load_json(PROXY_CONFIG, {})
    fixed = config.get("fixed_tools", [])
    dynamic = config.get("dynamic_tools", {})
    history = config.get("call_history", {})
    
    print(f"Fixed tools: {len(fixed)}")
    for t in fixed:
        print(f"  - {t['name']}: {t['description']} (always on, {t['token_cost']}t)")
    
    print(f"\nDynamic tools: {len(dynamic)}/{config.get('promotion_rules', {}).get('max_dynamic_tools', 5)}")
    for name, data in dynamic.items():
        print(f"  - {name}: {data['call_count']} calls, promoted {data['promoted_at'][:10]}")
    
    total_calls = sum(h.get("count", 0) for h in history.values())
    print(f"\nTotal tool calls: {total_calls}")
    print(f"Tracked tools: {len(history)}")

def list_active_tools():
    """Output JSON for LLM to consume — minimal tokens."""
    config = load_json(PROXY_CONFIG, {})
    fixed = config.get("fixed_tools", [])
    dynamic = config.get("dynamic_tools", {})
    
    tools = []
    for t in fixed:
        tools.append({"name": t["name"], "desc": t["description"], "url": t["endpoint"]})
    for name, data in dynamic.items():
        tools.append({"name": name, "desc": "dynamic", "url": f"http://127.0.0.1:2725/{name}"})
    
    # Compact JSON — minimal tokens
    print(json.dumps({"tools": tools}, separators=(",", ":")))

def cleanup_stale():
    """Demote tools unused for >7 days."""
    config = load_json(PROXY_CONFIG, {})
    dynamic = config.get("dynamic_tools", {})
    history = config.get("call_history", {})
    threshold_days = config.get("promotion_rules", {}).get("demote_after_days_unused", 7)
    now = datetime.now()
    demoted = []
    
    for name in list(dynamic.keys()):
        last = dynamic[name].get("last_called")
        if last:
            try:
                last_dt = datetime.fromisoformat(last)
                if (now - last_dt).days >= threshold_days:
                    del dynamic[name]
                    if name in history:
                        history[name]["promoted"] = False
                    demoted.append(name)
            except ValueError:
                pass
    
    config["dynamic_tools"] = dynamic
    config["call_history"] = history
    save_json(PROXY_CONFIG, config)
    
    if demoted:
        print(f"DEMOTED: {', '.join(demoted)} (unused >{threshold_days} days)")
    else:
        print("No stale tools to demote.")

def main():
    if len(sys.argv) < 2:
        print("Usage: mcp-proxy-manager.py [record|status|tools|cleanup] [tool_name]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "record" and len(sys.argv) >= 3:
        record_call(sys.argv[2])
    elif cmd == "status":
        show_status()
    elif cmd == "tools":
        list_active_tools()
    elif cmd == "cleanup":
        cleanup_stale()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
