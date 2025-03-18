from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.openapi.models import SecuritySchemeType, SecurityScheme
from Task_model import Task
from JWT_router import router as jwt_router, verify_token
from Task_router import router as task_router

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with JWT authentication",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "JWT authentication operations"},
        {"name": "Tasks", "description": "Operations with tasks"},
    ],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.openapi_schema = None  

security_scheme = {
    "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
}

# Save the original openapi method before replacing it
original_openapi = app.openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Call the original method instead of the overridden one
    openapi_schema = original_openapi()
    
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    
    openapi_schema["components"]["securitySchemes"] = security_scheme
    
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jwt_router)
app.include_router(task_router)

@app.get("/")
async def readRoot():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Task_manager:app", host="localhost", port=8000, reload=True)

