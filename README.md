# Self-Healing Web Scraper Pipeline

Autonomous web scraping infrastructure built to eliminate pipeline downtime caused by DOM mutations, schema drift, and network volatility. When extraction fails, the pipeline autonomously captures failure context, engages an LLM-powered diagnostics engine to refactor broken code, and redeploys the healed scraper via CI/CD.

---

## Problem Statement

Traditional web scrapers are fragile. Minor changes in website DOM structures, CSS selectors, or upstream API schemas cause abrupt pipeline failures, requiring manual engineering intervention to debug, patch, and deploy fixes.

---

## Key Features

- **Autonomous Self-Healing Loop** — Automatically catches runtime validation faults and triggers real-time LLM-driven code repair.
- **Resilient Scraping Architecture** — Powered by Bright Data Collector infrastructure with exponential backoff and network glitch mitigation.
- **Zero-Touch CI/CD Automation** — Integrated with GitHub Actions to orchestrate scraping, anomaly detection, code healing, and Git persistence.

---

## Architecture & Workflow

<img width="757" height="608" alt="working_flow" src="https://github.com/user-attachments/assets/ced36977-440d-42e7-9b5c-27cd5f5af61e" />

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.11+ |
| **Data Extraction** | Bright Data Collector APIs, Requests, Urllib3 |
| **AI Diagnostics Engine** | Groq API (`llama-3.3-70b-versatile`) / Google GenAI SDK (`gemini-3.6-flash`) |
| **CI/CD Orchestration** | GitHub Actions Workflow Pipelines |
| **Version Control** | Git |

---

## Repository Structure

```text
├── .github/
│   └── workflows/
│       └── scrape.yml        # CI/CD orchestration pipeline
├── src/
│   ├── scraper.py            # Primary scraper with schema validation
│   ├── healer.py             # LLM-based autonomous repair engine
│   ├── scraped_output.json   # Extracted data store
│   └── failure_dump.txt      # Temporary execution error buffer
├── .gitignore        
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Local Setup & Execution

### 1. Clone the repository

```bash
git clone https://github.com/Yoges19/Self-Healing-WebScraper.git
cd Self-Healing-WebScraper
```

### 2. Environment setup

Create a `.env` file in the root folder:

```env
BRIGHTDATA_COLLECTOR_ID=your_collector_id
BRIGHTDATA_API_TOKEN=your_brightdata_token
GROQ_API_KEY=your_groq_api_key
```
[Visit BRIGHTDATA](https://brightdata.com/cp/start)
[Visit GROQ](https://console.groq.com/keys)


### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python src/scraper.py
```

---

## 🧪 Simulating Failure & Auto-Repair

1. **Trigger an anomaly** — Alter expected fields inside `src/scraper.py` (e.g., set `required_keys = ["company_name", "broken_key"]`).
2. **Execute the scraper** — Run `python src/scraper.py`. The error will be logged into `src/failure_dump.txt`.
3. **Execute the healer** — Run `python src/healer.py`. The repair engine analyzes the dump, refactors `src/scraper.py`, and restores pipeline integrity.

---

## Publishing Changes

Once created, stage and commit the documentation:

```bash
git add README.md
git commit -m "docs: add architecture and setup documentation"
git push origin master
```
