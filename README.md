# Web Scraper & Data Collection Engine
### Computing Aptitude Mini Project &bull; C++ Core &amp; Modern CSS Design

A mini project for **Computing Aptitude**, integrating high-performance **C++17 systems programming** with a modern **CSS Glassmorphic data intelligence dashboard**.

---

## 🌟 Key Highlights & Computing Aptitude Concepts

1. **Networking & Sockets (C++ Core)**:
   - Built on native Windows **WinSock2** & **WinINet** API stacks (RFC-compliant HTTP/HTTPS GET requests).
   - Embedded lightweight HTTP Web Server written in C++ that serves the web dashboard and REST API (`/api/scrape`, `/api/data`, `/api/stats`, `/api/export`).
   - Zero third-party library dependencies (no external libcurl or Boost required).

2. **DFA Pattern Extraction & Tokenization**:
   - Parses unstructured HTML into structured records (Quotes, Authors, Tags, Books, Prices, Availability).
   - Regex-based and state-machine tag stripping and entity decoding (`&quot;`, `&amp;`, `&#39;`).

3. **Computing Aptitude Statistical Metrics**:
   - Computes keyword frequencies using hash maps ($O(1)$ lookup time complexity).
   - Tracks network fetch latency, throughput, and C++ extraction speed in milliseconds.

4. **Modern CSS Design System**:
   - Sleek **Glassmorphic dark UI** (`backdrop-filter: blur()`).
   - CSS Grid and Flexbox responsive layouts.
   - Pure CSS animated frequency bar chart.
   - Interactive data table with real-time search filtering, status badges, and CSV/JSON export.

5. **100% Offline & Online Resilient**:
   - Works seamlessly with live web endpoints (`quotes.toscrape.com`, `books.toscrape.com`).
   - Automatically falls back to built-in computing sandbox datasets if offline or running in an isolated exam/lab environment.

---

## 📁 Project Structure

```
computing project/
├── src/
│   ├── scraper.cpp          # Main C++ Web Scraper & Embedded Web Server
│   ├── http_client.hpp      # C++ HTTP/HTTPS Client (WinINet & WinSock2)
│   ├── parser.hpp           # DFA Tag Stripping & HTML Pattern Extractor
│   └── data_store.hpp       # Data serializer & CSV / JSON export engine
├── web/
│   ├── index.html           # Interactive Web Dashboard
│   ├── style.css            # Modern CSS3 Glassmorphic Styling
│   └── app.js               # Dynamic Dashboard Controller & Live Visualizer
├── data/
│   ├── sample_data.json     # Sample structured scraped dataset
│   └── sample_data.csv      # Sample CSV export
├── build_and_run.bat        # 1-Click Windows Compiler & Launcher
├── run_project.py           # Python 3 Runner (Twin engine, zero pip dependencies)
├── PROJECT_REPORT.md        # Academic Mini Project Report
└── README.md                # Project documentation
```

---

## 🚀 How to Run the Project

### Option 1: 1-Click Launch (Recommended)
Double-click `build_and_run.bat` in the project folder.
- If **MinGW (g++)** or **Visual Studio (cl)** is detected, it automatically compiles `scraper.exe` and launches the dashboard.
- If no C++ compiler is installed, it runs via `run_project.py` or opens the dashboard directly in your default browser.

### Option 2: Python Runner
Open a terminal in this directory and execute:
```bash
python run_project.py
```
This starts the local web server at `http://127.0.0.1:8080` and automatically opens your browser.

### Option 3: Manual C++ Compilation
Using MinGW (g++):
```bash
g++ -O2 -std=c++17 src/scraper.cpp -o scraper.exe -lws2_32 -lwininet
scraper.exe --serve 8080
```
Then open `http://127.0.0.1:8080` in your web browser.

### Option 4: Direct Browser Preview
Double-click `web/index.html` to open the styled dashboard directly in Google Chrome, Edge, or Firefox. The interface includes a client-side simulation engine that runs immediately even without a backend!

---

## 📊 Available API Endpoints (C++ Server)

| Endpoint | Method | Description |
|---|---|---|
| `/` or `/index.html` | GET | Serves the interactive Web Dashboard |
| `/style.css` | GET | Serves the CSS glassmorphic stylesheet |
| `/app.js` | GET | Serves the dynamic frontend JavaScript |
| `/api/scrape?target=quotes` | GET | Triggers live/sandbox scraping and returns structured JSON |
| `/api/data` | GET | Returns currently stored scraped dataset |
| `/api/export/csv` | GET | Downloads dataset formatted as CSV |
| `/api/export/json` | GET | Downloads dataset formatted as JSON |
