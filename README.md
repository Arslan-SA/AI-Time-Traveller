<div align="center">

# ⏳ AI Time Traveler

### Your future is not predicted. It is simulated from your behavior.

**AI Time Traveler transforms historical personal activity into data-driven future scenarios.**

[![Status](https://img.shields.io/badge/status-early%20development-orange?style=for-the-badge)](#-project-status)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](#-license)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](#-contributing)

[Overview](#-overview) · [How It Works](#-how-it-works) · [What-If Simulation](#-what-if-scenario-simulation) · [Architecture](#-system-architecture) · [Installation](#-installation) · [Roadmap](#-future-roadmap)

</div>

---

> ⚠️ **Note on numbers:** every projection, metric, and JSON value shown in this README is an **illustrative example**. AI Time Traveler produces *estimates with uncertainty*, not guarantees.

## 📌 Project Status

This README describes both the current scope and the intended design. Each feature is tagged with a status so nothing is overstated.

| Tag | Meaning |
|---|---|
| ✅ **Implemented** | Working in the repository today |
| 🚧 **Planned (MVP)** | Scoped for the first usable version |
| 🔭 **Roadmap** | Longer-term idea, not yet scheduled |

> 🛠️ *Maintainer: update the status tags in the tables below as features land.*

---

## 🧭 Overview

**AI Time Traveler** is a personal productivity **forecasting and scenario-simulation** application.

It takes your historical activity (coding hours, GitHub commits, LeetCode problems, study time, and other customizable metrics), analyzes your trends, and projects where you *could* be in 30, 60, or 90 days if your current habits continue. Then it lets you change the variables and see how a different path might look.

It helps answer questions like:

- *"Where will I be in 30 days if I continue like this?"*
- *"How many coding hours might I accumulate next month?"*
- *"How many LeetCode problems could I solve?"*
- *"What happens if I increase coding from 2 hrs/day to 4 hrs/day?"*
- *"What happens if I stop studying for 10 days?"*
- *"How different could my trajectory look after 90 days?"*

**What it is not:** a crystal ball. It does not know the future. It extrapolates from your own data, states its uncertainty, and lets you explore alternatives.

---

## 🤔 Why AI Time Traveler?

Most productivity tools are **rear-view mirrors**: they show what you did. Very few help you reason about **what your current habits imply**.

| Typical tracker | AI Time Traveler |
|---|---|
| Shows past activity | Projects a *range* of future outcomes |
| Static dashboards | Interactive "What If?" scenarios |
| Raw numbers | Plain-English explanations of trends |
| Single number goals | Uncertainty-aware forecasts |
| Motivation by guilt | Motivation by seeing the compounding effect of small changes |

Small daily differences compound. Seeing *"+60 projected coding hours per month"* is often more tangible than being told to "code more".

---

## 💡 Core Concept

```text
Historical behavior  +  Current habits  ─▶  Statistical forecast  ─▶  Scenario simulation  ─▶  Explained insight
```

1. **Observe** – collect activity history from connected sources or manual entry.
2. **Model** – detect trends and seasonality with simple, transparent models.
3. **Project** – forecast each metric over a chosen horizon, with uncertainty.
4. **Simulate** – change inputs and recompute an alternate trajectory.
5. **Explain** – use an LLM to translate the numbers into plain-English insight.

> **Central message:** Your future is not predicted. It is *simulated from your behavior*.

---

## ⚙️ How It Works

```mermaid
flowchart LR
    A[Connect data source<br/>or enter data] --> B[Collect history]
    B --> C[Clean and transform]
    C --> D[Extract features]
    D --> E[Forecast trends]
    E --> F[Choose horizon<br/>30 / 60 / 90 days]
    F --> G[Projected metrics]
    G --> H[Adjust variables<br/>What-If simulator]
    H --> I[Recalculate trajectory]
    I --> J[AI explains changes<br/>in plain English]
```

### Example user journey

| Step | What happens |
|---|---|
| 1 | User connects GitHub |
| 2 | Application collects historical activity |
| 3 | Data is cleaned and transformed |
| 4 | Features are extracted |
| 5 | Forecasting model analyzes the historical trend |
| 6 | User selects a 30 / 60 / 90-day horizon |
| 7 | System generates projected metrics |
| 8 | User modifies variables in the scenario simulator |
| 9 | System recalculates the future trajectory |
| 10 | AI explains the projected changes in plain English |

---

## ✨ Key Features

| Feature | Description | Status |
|---|---|---|
| Activity tracking | Manual entry of coding hours, study hours, LeetCode problems, projects | 🚧 Planned (MVP) |
| Custom metrics | Define your own productivity metrics | 🚧 Planned (MVP) |
| Historical analysis | Rolling averages, trend detection, consistency scores | 🚧 Planned (MVP) |
| Baseline forecasting | 30 / 60 / 90-day projections from simple models | 🚧 Planned (MVP) |
| What-If simulator | Modify habits and compare against the current path | 🚧 Planned (MVP) |
| Dashboard | Current metrics, history, projections, scenario controls | 🚧 Planned (MVP) |
| AI insights | LLM-generated plain-English explanations of forecasts | 🚧 Planned (MVP) |
| GitHub integration | Import commit history automatically | 🚧 Planned (MVP) |
| LeetCode data | Import solved-problem history via a suitable source/API, if available | 🔭 Roadmap |
| Confidence intervals | Uncertainty bands on every projection | 🚧 Planned (MVP) |
| Calendar integration | Derive study/coding time from calendar events | 🔭 Roadmap |
| Goal-based simulation | "What must change to hit X by date Y?" | 🔭 Roadmap |

---

## 🔮 Example Prediction

**Current behavior (illustrative input):**

| Metric | Current rate |
|---|---|
| Coding | 2 hours/day |
| LeetCode | 4 problems/week |
| GitHub | 18 commits/week |
| Study | 5 days/week |

**Estimated 30-day trajectory (illustrative output):**

| Metric | Projected (30 days) | Range (example) |
|---|---|---|
| Coding hours | ~60 hrs | 50–68 |
| LeetCode problems | ~16–18 | 12–20 |
| GitHub commits | ~70 | 58–82 |

Example API-style output:

```json
{
  "horizon_days": 30,
  "model": "exponential_smoothing",
  "disclaimer": "Illustrative estimate based on historical behavior. Not a guarantee.",
  "projections": {
    "coding_hours":  { "expected": 60, "lower": 50, "upper": 68 },
    "leetcode":      { "expected": 17, "lower": 12, "upper": 20 },
    "github_commits":{ "expected": 70, "lower": 58, "upper": 82 }
  }
}
```

---

## 🧪 "What If?" Scenario Simulation

Modify one or more variables and the system recalculates the trajectory, then visualizes **Current Path vs What-If Path**.

```text
CURRENT PATH
Coding: 2 hrs/day
Projected monthly coding: ~60 hrs

WHAT IF
Coding: 4 hrs/day
Projected monthly coding: ~120 hrs

Difference:
+60 projected coding hours
```

> These numbers are **illustrative examples**, not guaranteed predictions. Real outcomes depend on consistency, burnout, schedule changes, and many things the model cannot see.

### Example scenarios

| Scenario | Change |
|---|---|
| Level up | Coding 2 → 4 hrs/day |
| Break | No studying for 10 days, then resume |
| Consistency push | Study days 5 → 7 per week |
| Sprint | LeetCode 4 → 10 problems/week for 30 days |

Example simulation request:

```json
{
  "horizon_days": 90,
  "baseline": "auto",
  "overrides": {
    "coding_hours_per_day": 4,
    "study_pause": { "start_day": 10, "duration_days": 10 }
  }
}
```

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    U([👤 User]) --> DS

    subgraph DS[Data Sources]
        GH[GitHub API]
        LC[LeetCode data source]
        MAN[Manual entry]
        CAL[Calendar - roadmap]
    end

    DS --> COL[Data Collection and Processing]
    COL --> FE[Feature Engineering]
    FE --> FC[Forecasting Engine]
    FC --> SIM[Scenario Simulation]
    SIM --> AI[AI Insight Layer<br/>LLM API]
    AI --> DASH[Dashboard<br/>React + Charts]

    COL <--> DB[(Database<br/>PostgreSQL / SQLite)]
    FC <--> DB
    DASH <--> API{{REST API<br/>FastAPI / Flask}}
    API <--> SIM
```

### Layer summary

| Layer | Responsibility |
|---|---|
| Data Sources | Where activity originates |
| Collection / Processing | Fetch, validate, clean, store |
| Feature Engineering | Turn raw logs into model-ready signals |
| Forecasting Engine | Project each metric forward with uncertainty |
| Scenario Simulation | Apply user overrides to produce alternate paths |
| AI Insight Layer | Explain results in natural language |
| Dashboard | Visualize and interact |

---

## 🔄 Data Pipeline

```mermaid
flowchart LR
    RAW[Raw events<br/>commits, sessions, solves] --> CLEAN[Cleaning<br/>dedupe, timezones, gaps]
    CLEAN --> AGG[Aggregation<br/>daily and weekly totals]
    AGG --> FEAT[Feature engineering]
    FEAT --> STORE[(Feature store / DB)]
```

**Cleaning & aggregation**

- Deduplicate events and normalize timezones
- Fill missing days explicitly (a missing day is `0`, not "unknown", unless the source says otherwise)
- Aggregate to daily and weekly series per metric

**Example engineered features**

| Feature | Description |
|---|---|
| `rolling_mean_7d` / `rolling_mean_30d` | Smoothed recent activity level |
| `trend_slope` | Direction and rate of change |
| `consistency_score` | Share of active days in a window |
| `weekday_profile` | Typical activity by day of week |
| `streak_length` | Current and longest activity streak |
| `volatility` | Variation around the trend |

---

## 📈 ML / Forecasting Approach

The goal is **useful, explainable estimates**, not model complexity.

```mermaid
flowchart LR
    H[Historical Data] --> C[Cleaning]
    C --> A[Aggregation]
    A --> F[Feature Engineering]
    F --> T[Trend Detection]
    T --> P[Forecasting]
    P --> S[Scenario Simulation]
    S --> V[Visualization]
```

### First-version models

| Model | Why it's useful |
|---|---|
| **Moving averages** | Simple, robust baseline; easy to explain |
| **Linear regression** | Captures steady upward/downward trends |
| **Exponential smoothing** | Weights recent behavior more heavily |
| **Classical time-series models** (e.g. ARIMA-style) | Handles autocorrelation and seasonality when enough data exists |

### Why simple models first?

- Personal activity data is **small and noisy**, usually weeks or months, not millions of rows.
- Simple models are **interpretable**, so users can see *why* a projection changed.
- They are **fast** and cheap to run interactively during scenario simulation.
- They set a **baseline** any future model must beat.
- Deep learning is **not required** for the MVP and would likely overfit sparse personal data.

### How scenarios work

Scenarios are applied to the **forecast inputs**, not by retraining a "magic" model. For example, a coding-hours override replaces the baseline daily rate over the chosen days, and dependent metrics are recomputed using observed relationships (such as historical commits per coding hour). The result is a **counterfactual projection**: *"if the rate were X, the accumulated total would be Y."*

### Uncertainty

Projections should ship with ranges (for example prediction intervals or residual-based bands) so the UI communicates that the estimate is a spread of plausible outcomes, not a single truth.

---

## 🤖 AI Layer

The LLM does **not** produce the numbers. The forecasting engine does. The LLM **explains** them.

| Responsibility | Handled by |
|---|---|
| Computing projections | Forecasting engine (statistical models) |
| Computing scenario deltas | Simulation module |
| Summarizing trends in plain English | LLM |
| Explaining what changed between paths | LLM |
| Suggesting (never mandating) next steps | LLM, grounded in computed numbers |

**Design principles**

- The LLM receives **structured forecast output** and is instructed not to invent numbers.
- Insights must reference the provided data and its uncertainty.
- Prompts explicitly discourage certainty language ("will", "guaranteed").

Example insight:

> *"Over the last 30 days you averaged about 2 hours of coding on 5 days per week. If that pattern continues, the model estimates roughly 50–68 coding hours next month. In the What-If path at 4 hrs/day, the estimate roughly doubles, but it assumes you sustain that pace every day. Your historical consistency suggests the upper end may be hard to hold."*

---

## 🧰 Tech Stack

> Stack below reflects the **intended** design. Update status as components ship.

| Area | Technology | Status |
|---|---|---|
| Frontend | React, Tailwind CSS, Recharts | 🚧 Planned (MVP) |
| Backend | Python, FastAPI (or Flask) | 🚧 Planned (MVP) |
| Data / ML | Pandas, NumPy, scikit-learn, statsmodels (time series) | 🚧 Planned (MVP) |
| Database | SQLite (dev) → PostgreSQL (prod) | 🚧 Planned (MVP) |
| Integrations | GitHub API | 🚧 Planned (MVP) |
| Integrations | LeetCode data (via suitable source/API, if available) | 🔭 Roadmap |
| AI | LLM API for explanations and insights | 🚧 Planned (MVP) |

---

## 🗂️ Project Structure

Proposed layout:

```text
ai-time-traveler/
├── backend/
│   ├── app/
│   │   ├── main.py              # API entrypoint
│   │   ├── api/                 # Route handlers
│   │   ├── core/                # Config, settings
│   │   ├── db/                  # Models, migrations, session
│   │   ├── ingestion/           # GitHub / LeetCode / manual collectors
│   │   ├── processing/          # Cleaning and aggregation
│   │   ├── features/            # Feature engineering
│   │   ├── forecasting/         # Models, evaluation, intervals
│   │   ├── simulation/          # What-If engine
│   │   └── insights/            # LLM prompts and formatting
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # Charts, controls, cards
│   │   ├── pages/               # Dashboard, Scenarios, Settings
│   │   ├── hooks/
│   │   └── api/                 # API client
│   ├── package.json
│   └── tailwind.config.js
├── docs/
│   └── images/                  # Screenshots
├── .env.example
├── docker-compose.yml           # optional
└── README.md
```

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- (Optional) PostgreSQL 14+ — SQLite works for local development

```bash
# 1. Clone
git clone https://github.com/<your-username>/ai-time-traveler.git
cd ai-time-traveler

# 2. Backend
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend
cd ../frontend
npm install
```

---

## 🔐 Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

```env
# --- App ---
APP_ENV=development
SECRET_KEY=change-me

# --- Database ---
# SQLite (default for local dev)
DATABASE_URL=sqlite:///./time_traveler.db
# PostgreSQL (production)
# DATABASE_URL=postgresql://user:password@localhost:5432/time_traveler

# --- GitHub integration ---
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret

# --- LLM provider ---
LLM_API_KEY=your_api_key
LLM_MODEL=your_model_name

# --- Frontend ---
VITE_API_BASE_URL=http://localhost:8000
```

> 🔒 Never commit `.env`. Keep secrets out of version control.

---

## ▶️ Running Locally

```bash
# Terminal 1 — backend
cd backend
alembic upgrade head          # create tables and seed built-in metrics
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm run dev
```

The default `DATABASE_URL` is SQLite (`sqlite:///./time_traveler.db`). Set it to
a PostgreSQL URL (for example `postgresql://user:password@localhost:5432/time_traveler`)
in production; the `psycopg` driver is already included.

### Database migrations

```bash
cd backend
alembic revision --autogenerate -m "describe the change"   # after editing models
alembic upgrade head                                        # apply migrations
alembic downgrade -1                                        # roll back one step
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| API docs (FastAPI) | http://localhost:8000/docs |

---

## 🔌 API Overview

> Proposed endpoints. Final routes may change during development.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/activities` | Add manual activity entries |
| `GET` | `/api/activities` | Retrieve historical activity |
| `POST` | `/api/integrations/github/connect` | Connect a GitHub account |
| `POST` | `/api/integrations/github/sync` | Import GitHub activity |
| `GET` | `/api/metrics/summary` | Current metrics and features |
| `POST` | `/api/forecast` | Generate baseline projection |
| `POST` | `/api/simulate` | Run a What-If scenario |
| `POST` | `/api/insights` | Generate AI explanation for a forecast |

### `POST /api/forecast`

```json
{
  "metrics": ["coding_hours", "github_commits", "leetcode"],
  "horizon_days": 30
}
```

### `POST /api/simulate` (response, illustrative)

```json
{
  "horizon_days": 30,
  "current_path": {
    "coding_hours": { "expected": 60, "lower": 50, "upper": 68 }
  },
  "what_if_path": {
    "coding_hours": { "expected": 120, "lower": 95, "upper": 130 }
  },
  "difference": {
    "coding_hours": 60
  },
  "assumptions": [
    "Coding rate of 4 hrs/day is sustained across the horizon",
    "Historical relationships between metrics remain similar"
  ],
  "disclaimer": "Illustrative scenario estimate. Not a guarantee."
}
```

### `POST /api/insights` (response, illustrative)

```json
{
  "summary": "If your current pace continues, you may accumulate roughly 50–68 coding hours next month.",
  "key_changes": [
    "Doubling daily coding time roughly doubles projected hours, assuming it is sustained."
  ],
  "caveats": [
    "Your historical consistency is about 71%, so full-pace weeks may be hard to maintain."
  ]
}
```

---

## 🧵 Example Workflow

```text
1. Sign in and connect GitHub
2. Import the last 90 days of activity
3. Add LeetCode / study hours manually (or via integration when available)
4. Open the dashboard → review current metrics and history
5. Choose a 30 / 60 / 90-day horizon
6. Inspect the baseline projection and its uncertainty band
7. Open the Scenario Simulator → set coding from 2 to 4 hrs/day
8. Compare "Current Path vs What-If Path"
9. Read the AI-generated explanation and its caveats
10. Save the scenario and revisit as your habits change
```

### Example dashboard

| Panel | Content |
|---|---|
| **Current metrics** | Coding hours, commits, LeetCode solved, study consistency |
| **Historical activity** | Time-series graph of past behavior |
| **Future projection** | Forecast line with confidence/uncertainty band |
| **Scenario controls** | Sliders and inputs for hypothetical changes |
| **Current Path vs What-If Path** | Overlaid comparison chart and delta table |
| **AI insights** | Plain-English explanation, assumptions, and caveats |

---

## 🖼️ Screenshots

> Replace these placeholders with real screenshots as the UI is built.

| Dashboard | Forecast |
|---|---|
| ![Dashboard](docs/images/dashboard.png) | ![Forecast](docs/images/forecast.png) |

| What-If Simulator | AI Insights |
|---|---|
| ![What-If](docs/images/what-if.png) | ![Insights](docs/images/insights.png) |

---

## 🗺️ Future Roadmap

```mermaid
timeline
    title AI Time Traveler Roadmap
    MVP : Manual and GitHub data : Baseline forecasting : What-If simulator : Dashboard : AI insights
    Next : Confidence intervals : Multiple forecasting models : Calendar integration : Automated collection
    Later : Personalized forecasting : Habit detection : Anomaly detection : Goal-based simulation
    Vision : AI recommendations : Personal knowledge graph : Mobile app : Digital-twin modeling
```

- [ ] GitHub integration
- [ ] Calendar integration
- [ ] Automated activity collection
- [ ] Personalized forecasting
- [ ] Multiple forecasting models with backtesting and comparison
- [ ] Confidence intervals
- [ ] Habit detection
- [ ] Productivity anomaly detection
- [ ] Goal-based simulation ("what do I need to change to reach X?")
- [ ] AI-generated recommendations
- [ ] Personal knowledge graph
- [ ] Mobile application
- [ ] Long-term, digital-twin-style modeling of personal behavior

---

## ⚠️ Limitations

Being honest about what this system can and cannot do:

- **It is not a predictor of the future.** It extrapolates from past behavior.
- **Small data.** A few weeks of history yields wide uncertainty.
- **Behavior changes.** Exams, illness, burnout, new jobs, and motivation shifts are invisible to the model.
- **Activity ≠ progress.** Hours and commit counts are proxies; they do not measure learning quality or impact.
- **Scenarios assume sustainability.** Doubling effort on paper does not mean you can sustain it.
- **Data source constraints.** Third-party APIs may be rate-limited, incomplete, or unavailable (LeetCode access in particular depends on a suitable source).
- **LLM explanations can be imperfect.** They are grounded in computed numbers but should be read critically.
- **Privacy.** Personal activity data is sensitive; self-hosting and minimal data retention are recommended.

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

**Good first areas:** forecasting model evaluation, uncertainty visualization, new data-source connectors, test coverage, and documentation.

Please open an issue first for major changes so we can discuss direction.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

**AI Time Traveler** — a forecasting and scenario simulation system.

*Your future is not predicted. It is simulated from your behavior.*

</div>
