from fastapi import FastAPI
from docai.views import file_route
from settings import connect_to_mongo

# Create the FastAPI app
app = FastAPI(title="Document AI")

# Connect to MongoDB
connect_to_mongo()

# Include the file upload router with a prefix and tags for documentation
app.include_router(file_route, prefix="/documents", tags=["Uploader"])

if __name__ == "__main__":
    # Run the FastAPI app with debug mode on, accessible at localhost:5000
    app.run(debug=True, port=5000, host="localhost")
