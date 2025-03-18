from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from JWT_router import router as jwt_router
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
#boiler plate for making the jwt token available in the swagger UI
original_openapi = app.openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = original_openapi()
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    openapi_schema["components"]["securitySchemes"] = security_scheme
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
#changing the openapi schema to include the jwt token changes
app.openapi = custom_openapi
#generic cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
#router because why not
app.include_router(jwt_router)
app.include_router(task_router)
#checking if up and running
@app.get("/")
async def readRoot():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Task_manager:app", host="0.0.0.0", port=8000, reload=True)

