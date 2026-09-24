#!/usr/bin/env python3
"""browse.py URL — buka web, cetak isi. Simple, tanpa batas."""
import sys
from playwright.sync_api import sync_playwright
url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page()
    pg.goto(url, timeout=30000)
    print("TITLE:", pg.title())
    print("URL:", pg.url)
    print(pg.inner_text("body"))
    b.close()
