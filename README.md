# 🚀 StreamIQ AI
### Intelligent Video Streaming Optimizer

**An AI-powered adaptive video streaming optimization and network simulation platform.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-149ECA?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-97CA00?style=for-the-badge)

---

**Machine Learning · Adaptive Bitrate Streaming · Network Simulation · Quality of Experience · Full-Stack Engineering**

StreamIQ AI is a full-stack, machine-learning-powered video streaming optimization platform designed to explore how intelligent bandwidth prediction and adaptive bitrate selection can improve streaming performance under changing network conditions.

The system combines a Python-based simulation engine, machine learning models, a FastAPI backend, and a modern React dashboard to analyze network behavior, simulate video playback, and evaluate streaming quality through measurable performance indicators.

Rather than relying on static bitrate selection, StreamIQ AI investigates a prediction-driven approach to adaptive streaming and compares it with established baseline strategies.

---

## Project Overview

Modern video streaming systems must continuously balance video quality, playback smoothness, and changing network bandwidth. Selecting a bitrate that is too high can cause buffering and playback interruptions, while selecting a bitrate that is too low can unnecessarily reduce visual quality.

**StreamIQ AI addresses this optimization challenge through simulation, predictive modeling, and performance analysis.**

The platform is designed to:

- Simulate realistic fluctuations in network bandwidth.
- Generate and analyze synthetic network measurements.
- Train a machine learning model for bandwidth prediction.
- Make adaptive bitrate decisions using predicted network conditions.
- Compare machine-learning-assisted adaptation against conventional bitrate strategies.
- Evaluate streaming performance using Quality of Experience (QoE) metrics.
- Present network, playback, and model performance through an interactive dashboard.

The project provides an experimental environment for studying the relationship between network conditions, prediction accuracy, bitrate adaptation, and end-user streaming experience.

## Core Features

### 1. Intelligent Bandwidth Prediction

StreamIQ AI incorporates a machine learning workflow for estimating future network bandwidth from simulated network measurements.

The ML component supports dataset generation, model training, evaluation, and model artifact persistence.

Its purpose is to investigate whether predictive information can help an adaptive bitrate controller respond more effectively to network changes.

### 2. Adaptive Bitrate Optimization

The streaming simulation evaluates bitrate selection under variable bandwidth conditions.

Supported experimental strategies include:

| Strategy | Description |
|---|---|
| Fixed Bitrate | Maintains a constant video bitrate regardless of network changes |
| Buffer-Based ABR | Uses playback buffer conditions to guide bitrate selection |
| Throughput-Based ABR | Uses measured network throughput to estimate an appropriate bitrate |
| ML-Assisted ABR | Uses predicted bandwidth to inform bitrate selection |

These strategies provide a foundation for comparing streaming behavior across the same simulated network conditions.

### 3. Network Simulation

The project uses software-based network simulation to reproduce different bandwidth conditions without requiring physical networking equipment.

Network scenarios can represent relatively stable connectivity, bandwidth degradation, fluctuations, and other changing conditions.

This makes the platform suitable for controlled, repeatable experiments.

### 4. Streaming Quality Evaluation

StreamIQ AI evaluates streaming performance using metrics such as:

- Average selected video bitrate.
- Rebuffering events and rebuffering duration.
- Playback buffer behavior.
- Bitrate switching frequency.
- Network bandwidth utilization.
- Quality of Experience (QoE).
- Bandwidth prediction error.

These indicators help illustrate the trade-offs between video quality, playback stability, and adaptation responsiveness.

### 5. Interactive Analytics Dashboard

The React-based frontend provides a user-facing interface for exploring simulation results.

The dashboard is designed to visualize bandwidth changes, adaptive bitrate decisions, playback behavior, and comparisons between streaming strategies.

### 6. API-Driven Backend

The FastAPI backend connects the frontend, simulation logic, machine learning components, and data persistence.

The architecture separates presentation, API services, simulation logic, and model training to improve maintainability and extensibility.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| Machine Learning | scikit-learn, Python |
| Database | SQLite, SQLAlchemy |
| Real-Time Communication | WebSockets |
| Simulation | Python-based network and playback simulation |
| Testing | pytest |
| Deployment Tooling | Docker, Docker Compose |
| Version Control | Git, GitHub |

## System Architecture

```text
                  STREAMIQ AI
       Intelligent Video Streaming Optimizer
                         |
             React + TypeScript
               Frontend Dashboard
                         |
                  REST API / WS
                         |
                 FastAPI Backend
                         |
           +-------------+-------------+
           |             |             |
     Network & ABR   ML Prediction   Persistence
      Simulation       Pipeline       Layer
           |             |             |
     Bandwidth &      Trained ML     SQLAlchemy
     Playback Data     Artifacts       SQLite
           |             |             |
           +-------------+-------------+
                         |
                  QoE Evaluation
                         |
                Analytics & Results
                         |
                  React Dashboard
```

### Processing Workflow

1. Generate or select a simulated network scenario.
2. Produce bandwidth measurements over time.
3. Estimate available bandwidth using the trained ML model.
4. Apply adaptive bitrate selection strategies.
5. Simulate segment downloads and playback buffer behavior.
6. Calculate playback and QoE metrics.
7. Compare the performance of different strategies.
8. Visualize the results in the frontend dashboard.

---

## Project Structure

```text
streamiq-ai/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── engine.py
│   │   └── main.py
│   ├── __init__.py
│   ├── main.py
│   └── simulator.py
│
├── frontend/
│   └── ...
│
├── ml/
│   ├── models/
│   │   ├── bandwidth.joblib
│   │   └── metrics.json
│   ├── __init__.py
│   └── train.py
│
├── tests/
│   ├── test_fullstack.py
│   └── test_simulator.py
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── ML_MODEL.md
│   ├── ROADMAP.md
│   ├── SIMULATION.md
│   └── TESTING.md
│
├── .env.example
├── .gitignore
├── Dockerfile.backend
├── docker-compose.yml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

Before running the application, install:

- Python 3.12
- Node.js and npm
- Git
- A code editor such as Visual Studio Code

### 1. Clone the Repository

```bash
git clone https://github.com/ShahCoding1/streamiq-ai.git
cd streamiq-ai
```

### 2. Create a Python Virtual Environment

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
```

### 3. Install Backend Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Train the Machine Learning Model

```powershell
.\.venv\Scripts\python.exe -m ml.train
```

The training pipeline produces model artifacts used by the prediction component.

### 5. Start the FastAPI Backend

From the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --reload-dir backend
```

Backend address:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the React Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite typically serves the frontend at:

```text
http://localhost:5173
```

Open the address displayed in your terminal to access the application.

---

## Machine Learning Pipeline

The machine learning subsystem is organized around bandwidth prediction.

Its experimental workflow includes:

**Data generation:** Create simulated network observations representing changing bandwidth conditions.

**Feature processing:** Prepare relevant network measurements for model training.

**Model training:** Fit a regression model to learn relationships between network observations and target bandwidth values.

**Evaluation:** Measure prediction performance using regression metrics.

**Artifact generation:** Save the trained model and evaluation results for subsequent use.

**Simulation integration:** Use bandwidth estimates as an input to ML-assisted adaptive bitrate decisions.

The saved model and metrics are located in:

```text
ml/models/bandwidth.joblib
ml/models/metrics.json
```

For additional implementation details, see `docs/ML_MODEL.md`.

## Adaptive Bitrate Streaming

Adaptive bitrate streaming selects the video representation for each upcoming segment based on available information about network and playback conditions.

StreamIQ AI uses this principle to study different adaptation approaches.

### Traditional Approaches

Fixed bitrate streaming provides a simple baseline but does not adapt to network changes.

Throughput-based adaptation uses previously observed network throughput to estimate a suitable bitrate.

Buffer-based adaptation prioritizes playback buffer conditions when deciding whether to increase or decrease quality.

### Prediction-Assisted Adaptation

The ML-assisted approach introduces a bandwidth prediction component into the decision-making process.

The objective is to evaluate whether predicted bandwidth can support more responsive bitrate decisions while maintaining playback stability.

The relative effectiveness of each approach depends on the simulated network conditions, prediction accuracy, and controller behavior. ML-assisted adaptation is therefore evaluated experimentally rather than assumed to outperform every baseline.

---

## Quality of Experience (QoE)

Video streaming performance is not determined by video resolution alone.

A high-quality stream that repeatedly pauses may deliver a worse experience than a slightly lower-quality stream with uninterrupted playback.

StreamIQ AI examines this trade-off using QoE-related indicators.

| Metric | Purpose |
|---|---|
| Average Bitrate | Measures the overall selected video quality |
| Rebuffering Duration | Measures time spent waiting for playback data |
| Rebuffering Events | Counts playback interruptions |
| Bitrate Switches | Measures adaptation frequency |
| Buffer Level | Indicates playback data available ahead of consumption |
| Bandwidth Prediction Error | Evaluates ML prediction accuracy |
| QoE Score | Provides a combined measure of streaming performance |

QoE calculations and their interpretation should be understood within the assumptions of the simulation model.

## Testing

The project includes automated tests for backend and simulation functionality.

Run tests from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

For testing guidance, see:

```text
docs/TESTING.md
```

## Docker Support

The repository includes a backend Dockerfile and Docker Compose configuration.

To build and start the configured services:

```bash
docker compose up --build
```

Refer to `docker-compose.yml` and `docs/DEPLOYMENT.md` for the available services and configuration requirements.

---

## Documentation

Additional technical documentation is organized in the `docs/` directory.

| Document | Description |
|---|---|
| `API.md` | Backend API reference |
| `ARCHITECTURE.md` | System architecture and component organization |
| `DEPLOYMENT.md` | Deployment guidance |
| `ML_MODEL.md` | Machine learning pipeline and model details |
| `ROADMAP.md` | Planned improvements |
| `SIMULATION.md` | Simulation concepts and behavior |
| `TESTING.md` | Testing instructions |

## Engineering Objectives

StreamIQ AI was developed as a practical exploration of the intersection between software engineering, machine learning, computer networks, and multimedia systems.

The project emphasizes:

- Modular full-stack application architecture.
- Integration of ML models into backend services.
- Simulation-based experimentation.
- Reproducible performance comparisons.
- Data-driven optimization.
- Separation of training, inference, and application logic.
- Clear technical documentation and automated testing.

## Limitations

StreamIQ AI is a research-oriented software simulation and engineering project.

Its experimental results should not be interpreted as direct evidence of performance in commercial streaming platforms or real-world production networks.

Synthetic network measurements simplify many factors that affect actual streaming, including transport protocols, device behavior, network contention, encoding characteristics, and content-dependent quality.

The current architecture provides a foundation for extending the platform toward more realistic streaming experiments.

## Future Improvements

Potential extensions include:

- Evaluation using real-world network trace datasets.
- More advanced time-series forecasting models.
- Reinforcement-learning-based adaptive bitrate control.
- Additional ABR baseline algorithms.
- Video segment encoding and playback integration.
- More comprehensive QoE models.
- Multi-user network simulation.
- Reproducible experiment configurations.
- Extended model explainability and benchmarking.
- Deployment and continuous integration improvements.

---

## Author

**Muhammad Shah Khalid**

Software Engineering Graduate | Python Developer | AI & Machine Learning Enthusiast

Interested in intelligent software systems, applied machine learning, computer networks, and data-driven engineering.

**GitHub:** [ShahCoding1](https://github.com/ShahCoding1)

**Project Repository:** [StreamIQ AI](https://github.com/ShahCoding1/streamiq-ai)

## License

This project is distributed under the terms provided in the repository's `LICENSE` file.

---

**StreamIQ AI — Exploring smarter streaming through machine learning, network simulation, and adaptive decision-making.**
