# Self-Healing Web Scraper Pipeline

It is an autonomous web scraping infrastructure built to eliminate pipeline downtime caused by DOM mutations, schema drift, and network volatility. When extraction fails, the pipeline autonomously captures failure context, engages an LLM-powered diagnostics engine to refactor broken code, and redeploys the healed scraper via CI/CD.

---

## Problem Statement
Traditional web scrapers are fragile. Minor changes in website DOM structures, CSS selectors, or upstream API schemas cause abrupt pipeline failures, requiring manual engineering intervention to debug, patch, and deploy fixes.

---

## Key Features

* **Autonomous Self-Healing Loop:** Automatically catches runtime validation faults and triggers real-time LLM-driven code repair.
* **Resilient Scraping Architecture:** Powered by Bright Data Collector infrastructure with exponential backoff and network glitch mitigation.
* **Zero-Touch CI/CD Automation:** Integrated with GitHub Actions to orchestrate scraping, anomaly detection, code healing, and Git persistence.

---

## 🏗️ Architecture & Workflow
<img width="757" height="608" alt="working_flow" src="https://github.com/user-attachments/assets/ced36977-440d-42e7-9b5c-27cd5f5af61e" />


