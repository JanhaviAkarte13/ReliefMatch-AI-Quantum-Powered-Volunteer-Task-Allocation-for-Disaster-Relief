# ReliefMatch

**AI + quantum-assisted volunteer-to-task allocation for disaster relief.**

ReliefMatch is a web-based decision-support prototype that helps relief coordinators assign volunteers to urgent tasks during disasters such as floods, earthquakes, cyclones, wildfires and landslides. An AI model scores how urgent each task is, then the assignment is solved two independent ways, with QAOA on a quantum simulator and with the classical Hungarian algorithm, and the dashboard compares both side by side.

> This is an academic prototype built on synthetic data at small scale. It supports a human coordinator's decision and does not replace it.

---

## The problem

During a disaster, coordinators must match a limited pool of volunteers to many urgent tasks (medical aid, rescue, food, water, shelter). Today this is mostly done by memory, phone calls, messaging groups and spreadsheets. That is slow and inconsistent, and it does not scale: as tasks and volunteers grow, the number of possible pairings grows combinatorially, so high-priority needs can go unstaffed while lower-priority ones are covered.

## How it works

1. **Input.** A coordinator logs tasks (location, type, severity, people affected, required skills, time reported) and volunteers (name, skills, location, availability).
2. **AI urgency scoring.** A scikit-learn model scores each task's urgency from severity, people affected and time since reported.
3. **Fit scores.** Every volunteer-task pair gets a fit score from skill match, distance and task urgency.
4. **Two solvers on the same problem.**
   - **Quantum:** the assignment is formulated as a QUBO and solved with QAOA (Qiskit, simulator).
   - **Classical:** the Hungarian algorithm (SciPy `linear_sum_assignment`) as a baseline.
5. **Comparison.** The dashboard shows both assignments with total fit score, tasks covered and solve time.
6. **Human review.** The coordinator reviews the suggestion before acting on it.

## Features

- Task and volunteer management (add, edit, delete) with auto-generated IDs
- Task types: Medical, Food, Water & Sanitation, Shelter, Rescue, Other
- Severity scale of 1 to 10 with colour-coded status badges
- Volunteer availability: Available, Assigned, Unavailable
- One-click sample data loader for demos
- Assignment page that runs the AI + quantum + classical pipeline
- Comparison page with quantum vs classical charts
- Login and signup, with a local-only fallback session when the backend is not reachable
- Home page with a multi-disaster visual (flood, earthquake, cyclone, wildfire, landslide)

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, React Router, Recharts, Axios |
| Backend | FastAPI (Python) |
| Database | SQLite (PostgreSQL optional) |
| AI module | scikit-learn |
| Quantum module | Qiskit, qiskit-optimization (QAOA, MinimumEigenOptimizer) |
| Classical baseline | SciPy (Hungarian algorithm) |
| Version control | Git, GitHub |

## Project structure

```
ReliefMatch/
├── frontend/              # React dashboard (Vite)
│   ├── src/
│   │   ├── api/           # apiClient.js: all backend calls
│   │   ├── components/    # forms, lists, results, comparison chart
│   │   └── pages/         # Dashboard.jsx (nav, routes, sections)
│   ├── index.html
│   └── .env
├── backend/               # FastAPI app
│   ├── main.py
│   ├── routers/           # tasks, volunteers, assignment
│   └── requirements.txt
├── ai_module/             # urgency scoring and fit-score logic
├── quantum_module/        # QUBO builder, QAOA solver, classical solver
├── data_generator/        # synthetic task and volunteer data
└── docs/
```

## Getting started

### Prerequisites

- Node.js 18 or higher
- Python 3.10 or higher

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ReliefMatch.git
cd ReliefMatch
```

### 2. Run the frontend

```bash
cd frontend
npm install
```

Create or check `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

Start the dev server:

```bash
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`). If the backend is not running, the app falls back to local-only mode and shows a notice banner, so you can still explore the UI. Use **Load sample data** on the Home page to fill in example tasks and volunteers.

### 3. Run the backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate    macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs are served at `http://localhost:8000/docs`.

## Data shapes

**Task**

```json
{
  "id": "TASK-001",
  "location": "Riverside Colony, Sector 4",
  "type": "Rescue",
  "severity": 9,
  "required_skills": ["Search & Rescue", "Medical"],
  "population_affected": 340,
  "disaster_datetime": "2026-07-18T14:30",
  "description": "Optional free text",
  "status": "Pending"
}
```

**Volunteer**

```json
{
  "id": "VOL-001",
  "name": "Asha Patil",
  "location": "Sector 4, near bus depot",
  "skills": ["Medical", "Search & Rescue"],
  "availability": "Available"
}
```

**Assignment response (`POST /generate-assignment`)**

```json
{
  "quantum":   { "assignments": [], "total_fit_score": 0, "tasks_covered": 0, "solve_time_ms": 0 },
  "classical": { "assignments": [], "total_fit_score": 0, "tasks_covered": 0, "solve_time_ms": 0 }
}
```

## Results and honest limitations

- Runs on **synthetic data** at small scale (roughly 10 tasks and 10 volunteers), which suits a quantum simulator on a normal laptop.
- In our experiments QAOA reached the same assignment quality as the classical Hungarian algorithm. It is used here as a **proof-of-concept comparison**, not as evidence of quantum advantage.
- The classical result guarantees a usable answer every time.
- No real-time GPS or live tracking. The map view, if enabled, uses simulated positions.
- Scaling to district-level use would need live data intake, real geocoding and larger-scale solvers.

## Team

| Role | Member |
|---|---|
| Frontend and dashboard | Janhavi Akarte |
| Backend and integration | Gauri Pradhan |
| AI module | Khushboo Chourasia |
| Quantum module | Ayush Jha |

Guide: Prof. Manisha Raut
