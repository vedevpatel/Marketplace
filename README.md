# AI Marketplace Simulation

A full-stack, agent-based economic simulation built to train and evaluate autonomous AI agents in a dynamic, real-time marketplace. The system models complex market behaviors such as dynamic pricing, inventory management, and consumption, leading to realistic emergent phenomena like price wars and market bubbles.

---

## Features
- Dynamic Multi-Agent Simulation — Hundreds of autonomous buyer and seller agents interact each "tick."
- Real-Time Visualization — A React frontend connects via WebSockets, providing a rich dashboard with live charts and tables.
- Complex Agent Behaviors — Agents use sophisticated, rule-based logic for pricing, restocking, and consumption, creating unpredictable market dynamics.
- AI Training Pipeline — Built-in Multi-Agent Reinforcement Learning (MARL) pipeline using shared policies for profit-maximizing strategies.
- Containerized Environment — One-command setup with Docker & Docker Compose for reproducible experiments.

---

## Tech Stack

| Category   | Technologies |
|------------|--------------|
| Backend    | Python, FastAPI, WebSockets |
| Frontend   | React, Vite, Chart.js, Tailwind CSS |
| AI/ML      | Stable-Baselines3, PettingZoo, Gymnasium, SuperSuit, PyTorch |
| DevOps     | Docker, Docker Compose |

---

## Getting Started

### Prerequisites
- Docker and Docker Compose
- (Optional for AI Training) NVIDIA Container Toolkit for GPU acceleration.

### Installation & Running
Clone the repository:
git clone https://github.com/vedevpatel/Marketplace.git
cd marketplace

Choose the simulation mode by editing `backend/Dockerfile` and uncomment one of the final CMD lines:

- Run with trained AI agents:  
  `CMD ["uvicorn", "run_trained:app", "--host", "0.0.0.0", "--port", "8000"]`
- Run with rule-based agents:  
  `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

Build and start the application:  
`docker-compose up --build`

Access the dashboard at: [http://localhost:3000](http://localhost:3000)

---

## AI Agent Training

To train your own AI models:

1. Ensure containers are running in the background. If already running, stop with Ctrl+C and restart in detached mode:  
   `docker-compose up --build -d`
2. Execute the training script inside the backend container:  
   `docker-compose exec backend python train.py`

---

## Project Structure

Marketplace/
├── backend/ # FastAPI backend & agent simulation
│ ├── main.py # Rule-based simulation entrypoint
│ ├── run_trained.py # AI-trained simulation entrypoint
│ ├── train.py # Training pipeline for MARL agents
│ └── Dockerfile
├── frontend/ # React + Vite dashboard
│ └── src/ # Charts, tables, WebSocket hooks
├── docker-compose.yml # Containerized setup
└── README.md
