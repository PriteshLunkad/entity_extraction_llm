# Document AI Service

This project provides a Document AI service built with FastAPI, which allows you to upload and process documents using various AI models. The project includes a MongoDB database for storing document data and MongoExpress for visualizing the database.

## Prerequisites

Before you start, make sure you have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

### Step 1: Set Up Environment Variables
Update the .env file in the project with the below api keys,

- GROQ_API_KEY=your_groq_api_key
- GROQ_BASE_URL=your_groq_base_url
- OPENAI_API_KEY=your_openai_api_key
- LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
- MONGO_HOST=mongodb://mongo:27017

### Step 2: Build and Run the Docker Containers
Run the following command to build and start the Docker containers:

docker-compose up --build

This command will:

Build the Docker images for the FastAPI application and MongoDB.
Start the containers for the FastAPI application, MongoDB, and MongoExpress.

### Step 3: Access the FastAPI Documentation
Once the containers are up and running, you can access the FastAPI interactive API documentation at:

http://localhost:8000/docs

### Step 4: Access MongoExpress
MongoExpress provides a web-based MongoDB admin interface to visualize and manage your database. Access it at:

http://localhost:8081

## Project Structure
- `config/`: contains the prompt and secrets to manage the api keys and mongo db 
- `docai/`: contains the app code setup and run the fastapi application
- `documents/`: Contains the shared pdf documents
- `experiments/`: Contains the code for huggingface experiment using flan T5 model and also document with outputs of google Document AI 
- `output_analysis.ipynb`: Contains the notebook with the results of the 3 shared documents
- `outputs/`: Contains the json and excel file of the outputs from various parsers and models on the documents


## API Endpoints
POST /documents/upload: Endpoint to upload and process a document.

## Troubleshooting
- Ensure Docker and Docker Compose are installed and running correctly.
- Check that the environment variables in the .env file are correctly set.
- Make sure the specified ports (8000 for FastAPI and 8081 for MongoExpress) are not in use by other applications.

