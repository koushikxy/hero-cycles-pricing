# Hero Cycles Pricing Engine

A time-sensitive pricing engine built for the Hero Cycles sales team. 

This project fulfills the Full-Stack Engineer assignment by providing a robust, time-aware calculation engine alongside a strict command-line interface and a modern, responsive web dashboard.

---

## 🚀 Features
* **Time-Sensitive Logic:** Dynamically calculates component prices based on historical date ranges (inclusive/exclusive boundary logic).
* **Command-Line Interface (Core Requirement):** Parses JSON quote requests and outputs a formatted price breakdown grouped by high-level components.
* **Web Configurator (Extra Credit):** A single-page application (SPA) with a modern dashboard, real-time recalculation, and active validation.
* **Robust Validation:** Prevents invalid physical configurations (e.g., selecting both Tubeless Tyres and standard Tubes).

---

## 🛠 Tech Stack
* **Backend Engine & CLI:** Python
* **Web API:** FastAPI, Uvicorn
* **Frontend UI:** HTML5, CSS3, JavaScript

---

## 📦 Quick Start & Setup (Under 2 Minutes)

### Prerequisites
Ensure you have Python 3.8 or higher installed on your machine.

### 1. Installation
The core CLI engine requires zero external packages. However, to run the Web UI, install the lightweight API framework:
`bash
pip install fastapi uvicorn
`

### 2. How to Run the Command-Line Engine (CLI)
The CLI reads the cycle configuration from `quote_request.json` and outputs a formatted, grouped receipt to the terminal.
1. Open your terminal in the project root.
2. Run the following command:
`bash
python cli.py
`

### 3. How to Run the Web Dashboard (UI)
To view the interactive configurator in your browser:
1. Start the local API server by running:
`bash
python -m uvicorn main:app --reload
`
2. Open your web browser and navigate to: **http://127.0.0.1:8000**

### 4. How to Run the Unit Tests
To verify the core pricing logic, time boundaries, and error handling edge cases, run the built-in test suite:
`bash
python -m unittest test_engine.py
`

---

## 📂 Project Structure

* `/src` - Core backend logic (`models.py`, `database.py`, `engine.py`)
* `/ui` - Frontend web assets (`index.html`, `style.css`, `script.js`)
* `main.py` - The FastAPI server connecting the engine to the Web UI
* `cli.py` - The Command-Line Interface application
* `test_engine.py` - Unit test suite for pricing logic boundaries
* `quote_request.json` - Sample input configuration for the CLI tool
* `THINKING.md` - Problem breakdown and data model strategy
* `UI_NOTES.md` - Design sensibility and UX decisions