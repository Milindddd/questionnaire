from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="mForm Parser API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "mForm Parser API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/forms/parse")
async def parse_form(file: UploadFile = File(...)):
    """
    Endpoint to parse uploaded Excel file into JSON format.
    Will be implemented in Phase 3.
    """
    return JSONResponse(
        status_code=501,
        content={"message": "Form parsing not implemented yet"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 