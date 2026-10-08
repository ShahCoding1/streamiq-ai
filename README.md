# StreamIQ AI — Intelligent Video Streaming Optimizer

A research-oriented **adaptive bitrate (ABR) streaming simulator** powered by a **trained gradient-boosted bandwidth forecasting model**. Includes React/TypeScript analytics, live WebSocket simulation, four-strategy benchmarking, SQLite experiment history, and CSV/JSON export. No paid APIs or hardware required.

> **Research disclaimer:** Network traces and video segment downloads are **simulated**. The system does **not** transmit real video, measure real Internet connections, or claim a standardized subjective QoE/MOS score. ML predictions are real inferences from a trained model, but the training data is synthetic.

## Requirements

- Python 3.10+ (recommended 3.11)
- Node.js 20+
- VS Code / Windows PowerShell

## Run on Windows

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ml.train
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --reload-dir backend
```

In a **second terminal**:

```powershell
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5173**. Backend docs: **http://127.0.0.1:8000/docs**.

## Features

- Seven reproducible network scenarios: stable, mobile, congested, variable, sudden drop, recovery, extreme fluctuation
- Seven quality levels: 144p through 1440p, 300–8000 kbps
- Buffer consumption, download time, stalls, startup delay, switches and QoE proxy
- Actual HistGradientBoostingRegressor inference, trained separately and loaded via joblib
- ML vs buffer-based vs fixed vs throughput-based comparisons using **identical traces**
- React charts for bandwidth, bitrate, buffer and QoE; live WebSocket updates
- Simulation configuration for bandwidth, latency, packet loss, buffer, segment duration and run length
- SQLite session persistence; CSV and JSON exports
- REST API with OpenAPI docs; Docker Compose deployment

## Training and evaluation

`python -m ml.train` generates synthetic traces with **disjoint random seeds** across train/validation/test. Features: last throughput, mean of last 3/5 measurements, 5-sample standard deviation, recent trend, buffer seconds and previous bitrate. Target: next-segment bandwidth (kbps). The model is a regression model; it does **not** output a calibrated classification confidence. Predicted bandwidth is converted into a safe bitrate by a transparent buffer-dependent safety factor.

Training outputs: `ml/models/bandwidth.joblib` and `ml/models/metrics.json`.

## QoE definition

For each segment: `qoe_step = selected_bitrate_kbps / 1000 - 4.3 × stall_seconds - 0.12 × abs(selected_bitrate - previous_bitrate) / 1000`. Run score = average segment score − `0.1 × startup_seconds`. This is an **illustrative QoE proxy**, not MOS, VMAF, or a validated perceptual metric.

## API

- `GET /api/health`
- `GET /api/scenarios`
- `GET /api/model/info`
- `POST /api/ml/predict`
- `POST /api/simulation/run`
- `POST /api/comparison/run`
- `GET /api/sessions`
- `GET /api/sessions/{id}`
- `GET /api/sessions/{id}/export?format=csv|json`
- `WS /ws/simulation` (send JSON configuration to stream segment ticks)

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
cd frontend
npm run build
```

## Docker

```powershell
docker compose up --build
```

Open **http://localhost:8080**. Docker is optional.

## Known limitations

Synthetic network traces; simplified segment-download model; no real MPEG-DASH/HLS player, video encoding, congestion control, calibrated uncertainty, or reinforcement learning. These are future research extensions, not implemented features.

## Project structure

- `backend/app/engine.py`: deterministic streaming simulator and ABR strategies
- `backend/app/main.py`: FastAPI, inference, WebSocket and session APIs
- `backend/app/database.py`: SQLAlchemy persistence
- `ml/train.py`: reproducible offline ML training
- `frontend/src/main.tsx`: React dashboard
- `tests/`: simulator, API and ML integration checks
- `docs/`: architecture, model, simulation, testing and deployment notes

MIT License — educational and portfolio use.
