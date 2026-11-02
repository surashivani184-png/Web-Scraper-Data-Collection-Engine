#!/usr/bin/env python3
"""
Computing Aptitude Mini Project Runner
Web Scraper for Data Collection (C++ Engine & Modern CSS Design)

This script:
1. Detects available C++ compilers (g++, clang, cl) to build the native C++ scraper.
2. If a compiler is present, compiles and runs the high-performance C++ executable.
3. If no C++ compiler is in PATH, serves the C++ project's web frontend and API
   using the Python standard library (zero external pip packages required).
4. Automatically opens the interactive web dashboard in your default browser.
"""

import os
import sys
import shutil
import subprocess
import webbrowser
import time
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")

def check_cpp_compiler():
    for compiler in ["g++", "clang++", "cl"]:
        path = shutil.which(compiler)
        if path:
            return compiler
    return None

def compile_cpp(compiler):
    print(f"\n[+] Detected C++ Compiler: {compiler}")
    src_file = os.path.join(SRC_DIR, "scraper.cpp")
    exe_file = os.path.join(BASE_DIR, "scraper.exe")

    if compiler in ["g++", "clang++"]:
        cmd = [compiler, "-O2", "-std=c++17", src_file, "-o", exe_file, "-lws2_32", "-lwininet"]
    else: # cl (MSVC)
        cmd = [compiler, "/O2", "/EHsc", "/std:c++17", src_file, f"/Fe:{exe_file}", "ws2_32.lib", "wininet.lib"]

    print(f"[+] Compiling C++ Scraper: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] C++ Compilation Successful! Generated: scraper.exe")
            return exe_file
        else:
            print("[-] C++ Compilation Error:\n", res.stderr)
            return None
    except Exception as e:
        print(f"[-] Compilation exception: {e}")
        return None

# Built-in lightweight server and scraper handler
class ScraperServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/scrape"):
            self.handle_scrape_api()
        elif self.path == "/api/data" or self.path == "/api/stats":
            self.handle_data_api()
        else:
            super().do_GET()

    def handle_scrape_api(self):
        target = "quotes"
        if "target=books" in self.path:
            target = "books"
        
        target_url = "https://quotes.toscrape.com" if target == "quotes" else "https://books.toscrape.com"
        
        print(f"[API] Scraping {target_url}...")
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            start = time.time()
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8', errors='ignore')
            latency = (time.time() - start) * 1000
        except Exception as e:
            print(f"[Warning] Live fetch fallback: {e}")
            sample_path = os.path.join(DATA_DIR, "sample_data.json")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.send_json_response(data)
                return
            html = ""
            latency = 14.5

        # Extract items using regex (mimicking the C++ parser logic)
        items = []
        parse_start = time.time()
        if target == "quotes":
            blocks = re.findall(r'<div class="quote"[^>]*>([\s\S]*?)<\/div>\s*<\/div>', html)
            for idx, b in enumerate(blocks, 1):
                text_m = re.search(r'<span class="text"[^>]*>([\s\S]*?)<\/span>', b)
                author_m = re.search(r'<small class="author"[^>]*>([\s\S]*?)<\/small>', b)
                tags = re.findall(r'<a class="tag"[^>]*>([\s\S]*?)<\/a>', b)
                items.append({
                    "id": idx,
                    "title": re.sub('<[^<]+?>', '', text_m.group(1)).strip() if text_m else "Quote",
                    "authorOrMeta": author_m.group(1) if author_m else "Unknown",
                    "categoryOrTag": ", ".join(tags) if tags else "general",
                    "detailOrPrice": "Verified Quote",
                    "timestamp": "2026-11-02"
                })
        else: # books
            blocks = re.findall(r'<article class="product_pod">([\s\S]*?)<\/article>', html)
            for idx, b in enumerate(blocks[:15], 1):
                title_m = re.search(r'title="([^"]+)"', b)
                price_m = re.search(r'<p class="price_color">([^<]+)<\/p>', b)
                items.append({
                    "id": idx,
                    "title": title_m.group(1) if title_m else "Book Title",
                    "authorOrMeta": "Book Sandbox",
                    "categoryOrTag": "In Stock",
                    "detailOrPrice": price_m.group(1) if price_m else "£0.00",
                    "timestamp": "2026-11-02"
                })

        if not items:
            # Fallback to sample data
            sample_path = os.path.join(DATA_DIR, "sample_data.json")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    self.send_json_response(json.load(f))
                    return

        parse_ms = (time.time() - parse_start) * 1000

        # Compute frequency metrics
        word_counts = {}
        for it in items:
            words = re.findall(r'\b[a-z]{4,}\b', it["title"].lower())
            for w in words:
                if w not in ["that", "this", "with", "from", "they", "have", "were"]:
                    word_counts[w] = word_counts.get(w, 0) + 1

        top_keywords = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:6])

        result = {
            "status": "success",
            "sourceUrl": target_url,
            "metrics": {
                "totalItems": len(items),
                "totalWords": sum(len(it["title"].split()) for it in items),
                "fetchTimeMs": round(latency, 1),
                "parseTimeMs": round(parse_ms, 2),
                "topKeywords": top_keywords
            },
            "items": items
        }

        # Save to data directory
        with open(os.path.join(DATA_DIR, "scraped_data.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        self.send_json_response(result)

    def handle_data_api(self):
        sample_path = os.path.join(DATA_DIR, "scraped_data.json")
        if not os.path.exists(sample_path):
            sample_path = os.path.join(DATA_DIR, "sample_data.json")
        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.send_json_response(data)

    def send_json_response(self, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

def main():
    print("=" * 65)
    print("   Computing Aptitude Mini Project: Web Scraper for Data Collection")
    print("   Engine: C++17 Core Architecture | Design: CSS Glassmorphism")
    print("=" * 65)

    compiler = check_cpp_compiler()
    if compiler:
        exe = compile_cpp(compiler)
        if exe and os.path.exists(exe):
            print(f"\n[+] Launching Native C++ Scraper & Dashboard Server...")
            webbrowser.open(f"http://127.0.0.1:{PORT}")
            subprocess.run([exe, "--serve", str(PORT)], cwd=BASE_DIR)
            return

    # Fallback to built-in Python Server
    print("\n[i] Starting Local Dashboard Server on port", PORT)
    server = HTTPServer(("127.0.0.1", PORT), ScraperServerHandler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"[+] Server is running at: {url}")
    print("[+] Opening web browser automatically...")
    webbrowser.open(url)
    print("\n[+] Press Ctrl+C in terminal to stop the server.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down cleanly.")
        server.server_close()

if __name__ == "__main__":
    main()
