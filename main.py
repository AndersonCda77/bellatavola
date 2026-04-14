from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Configurações
from config import settings

# Routers existentes
from routers.pratos import router as pratos_router
from routers.bebidas import router as bebidas_router
from routers.pedidos import router as pedidos_router
from routers.reservas import router as reservas_router

# Novo router de ML
from routers.predict import router as predict_router

app = FastAPI(
    title=settings.app_name,
    description="API do restaurante Bella Tavola com predição de sobremesa",
    version=settings.version,
    debug=settings.debug
)

# Incluindo todos os routers
app.include_router(pratos_router,   prefix="/pratos",   tags=["Pratos"])
app.include_router(bebidas_router,  prefix="/bebidas",  tags=["Bebidas"])
app.include_router(pedidos_router,  prefix="/pedidos",  tags=["Pedidos"])
app.include_router(reservas_router, prefix="/reservas", tags=["Reservas"])

# Novo router de Machine Learning
app.include_router(predict_router,  prefix="/ml",       tags=["ML"])

@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chef": "Marco Rossi",
        "cidade": "São Paulo",
        "versao": settings.version
    }


# ==================== HANDLERS DE ERRO ====================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados de entrada inválidos",
            "status": 422,
            "path": str(request.url),
            "detalhes": exc.errors()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail,
            "status": exc.status_code,
            "path": str(request.url)
        }
    )