# Marketplace

AI Marketplace Simulation 🚀
This project is a full-stack, agent-based economic simulation built to train and evaluate autonomous AI agents in a dynamic, real-time marketplace. The system models complex market behaviors such as dynamic pricing, inventory management, and consumption, leading to realistic emergent phenomena like price wars and market bubbles.

Features
Dynamic Multi-Agent Simulation: The core of the project is a Python-based simulation where hundreds of autonomous buyer and seller agents interact each "tick."

Real-Time Visualization: A React frontend connects to the simulation via WebSockets, providing a rich dashboard with live-updating charts and tables to visualize market dynamics.

Complex Agent Behaviors: Agents follow sophisticated, rule-based logic for pricing, restocking, and consumption, leading to emergent, unpredictable market behavior.

AI Training Pipeline: Features a complete Multi-Agent Reinforcement Learning (MARL) pipeline to train agents using shared policies to discover optimal, profit-maximizing strategies.

Containerized Environment: The entire full-stack application is containerized with Docker and Docker Compose for easy, one-command setup and reproducible experiments.

Tech Stack
Category	Technologies
Backend	Python, FastAPI, WebSockets
Frontend	React, Vite, Chart.js, Tailwind CSS
AI/ML	Stable-Baselines3, PettingZoo, Gymnasium, SuperSuit, PyTorch
DevOps	Docker, Docker Compose

Export to Sheets
Getting Started
Prerequisites
Docker and Docker Compose

(Optional for AI Training) NVIDIA Container Toolkit to enable GPU acceleration.

Installation & Running
Clone the repository:

Bash

git clone <your-repo-url>
cd Marketplace
Choose the Simulation to Run:
Open the backend/Dockerfile and select which server to run by uncommenting one of the final CMD lines.

For the simulation with the trained AI agent:

Dockerfile

CMD ["uvicorn", "run_trained:app", "--host", "0.0.0.0", "--port", "8000"]
For the simulation with only rule-based agents:

Dockerfile

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Build and Run the Application:

Bash

docker-compose up --build
View the Dashboard:
Open your browser and navigate to http://localhost:3000.

AI Agent Training 🤖
To train your own AI models, follow these steps:

Ensure containers are running in the background. If they are already running, stop them with Ctrl+C. Then, start them in detached mode:

Bash

docker-compose up --build -d
Execute the training script. This will run the train.py file inside the running backend container.

Bash

docker-compose exec backend python train.py
The script will print its progress and save the trained model to a .zip file inside the backend directory.

Generate code to prototype this with Canvas
