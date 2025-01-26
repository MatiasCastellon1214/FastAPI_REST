# Documentación: https://fastapi.tiangolo.com/es/

# Instalación de FastAPI: pip install "fastapi[all]


from fastapi import FastAPI
#from Backend.FastAPI.routers import image_product_db
from routers import users, products, basic_auth_users, jwt_auth_users, users_db, products_db, image_product_db, image_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(products.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.include_router(products_db.router)
app.include_router(image_product_db.router)
app.include_router(image_db.router)

# Url local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hello World!"

# Url local: http://127.0.0.1:8000/message

@app.get("/message")
async def message():
    return {"message": "Hello World"}

# Iniciar el server: uvicorn main:app --reload
# Detener el server: Ctrl + C

# Documentacioón con Swagger: http://127.0.0.1:8000/docs
# Documentacioón con Redocly: http://127.0.0.1:8000/redoc