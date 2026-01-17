# Intelligent Traffic Control System (RL + Microservices)

A hybrid AI-driven traffic control system that uses **Reinforcement Learning (Q-Learning)** to optimize traffic flow in real-time. The system is built on a decoupled microservices architecture.

## Architecture
* **Simulation Engine (Java Spring Boot):** * Manages the intersection state, traffic rules, and threading. 
    * Exposes a RESTful API (`GET /state`, `POST /action`) for external control.
* **AI Agent (Python + Pygame):**
    * Acts as the "Brain" of the system.
    * Uses **Tabular Q-Learning** to learn optimal signal timing strategies.
    * Provides a "Digital Twin" visualization of the traffic flow.
      
```mermaid
flowchart LR
    %% --- STYLING ---
    classDef java fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef python fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef storage fill:#fff3e0,stroke:#e65100,stroke-width:2px;

    %% --- JAVA BACKEND (LEFT) ---
    subgraph Java_Spring_Boot ["Java Spring Boot (Simulation Engine)"]
        direction TB
        StateDB[("Intersection State<br/>(North: 5, East: 10)")]:::storage
        Controller["REST Controller"]:::java
        Logic["Traffic Rules Engine"]:::java
        
        Logic -->|Updates Car Counts| StateDB
        StateDB -->|Reads State| Controller
    end

    %% --- PYTHON FRONTEND (RIGHT) ---
    subgraph Python_AI ["Python AI (Control Agent)"]
        direction TB
        Visualizer["Pygame Renderer"]:::python
        Agent["DQN Neural Network"]:::python
        Memory[("Replay Buffer")]:::storage
        
        Agent -->|Draws| Visualizer
        Agent <-->|Learns from| Memory
    end

    %% --- COMMUNICATION (THE BRIDGE) ---
    Controller -- "GET /state<br/>(JSON)" --> Agent
    Agent -- "POST /action<br/>(Switch Light)" --> Controller
```

## Key Features
* **Polyglot Microservices:** Seamless communication between Java (Backend) and Python (AI) via HTTP REST.
* **Reinforcement Learning:** The agent learns to minimize total wait time by penalized rewards (negative queue length).
* **Real-time Visualization:** Pygame rendering acts as a visual monitor for the backend state.

## Tech Stack
* **Backend:** Java 17, Spring Boot 3.x
* **AI/ML:** Python 3.10, NumPy, Q-Learning
* **Visualization:** Pygame
* **Communication:** REST API (JSON)

## How to Run
1.  **Start the Java Simulation:**
    ```bash
    cd backend-simulation
    ./mvnw spring-boot:run
    ```
2.  **Start the AI Agent:**
    ```bash
    cd ai-control-agent
    pip install -r requirements.txt
    python traffic_viz.py
    ```
