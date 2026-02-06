# Deployment Guide for LegalSense AI

This application is containerized using Docker and Docker Compose, employing a microservices architecture with:
1.  **Frontend/Backend**: Streamlit Application (Python)
2.  **LLM Support**: Ollama Container (runs locally within Docker)

## Prerequisites
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   [Git](https://git-scm.com/) (optional, for cloning).

## Quick Start (Run Locally)

1.  **Build and Start**:
    Open your terminal/command prompt in the project directory and run:
    ```bash
    docker-compose up --build
    ```

2.  **Access the App**:
    Open your browser and go to: [http://localhost:8501](http://localhost:8501)

3.  **Pull Models (First Time Only)**:
    Since the Ollama container starts empty, you need to pull the models *inside* the container.
    
    Open a new terminal window:
    ```bash
    # Pull the standard model
    docker exec -it legalsense_ollama ollama pull mistral
    
    # Pull the thinking model
    docker exec -it legalsense_ollama ollama pull deepseek-r1
    ```

## Cloud Deployment (e.g., AWS, Azure, GCP)

1.  **Provision a VM**: Use a virtual machine (EC2, Droplet, Compue Engine) with at least **8GB RAM** (16GB recommended for DeepSeek R1).
2.  **GPU Support**: If available, install `nvidia-container-toolkit` and uncomment the GPU section in `docker-compose.yml` for faster inference.
3.  **Transfer Files**: Copy the project files to the VM.
4.  **Run**: Execute `docker-compose up -d --build`.
