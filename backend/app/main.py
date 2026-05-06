from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

from app.auth.routes import router as auth_router
from app.config import get_settings
from app.courses.routes import router as courses_router
from app.questionnaires.routes import router as questionnaires_router
from app.registrations.routes import router as registrations_router

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {"message": settings.app_name, "env": settings.app_env}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/health/deps")
def health_deps() -> dict:
    deps = {
        "google": {
            "configured": bool(settings.google_client_id),
            "client_id_preview": (settings.google_client_id[:16] + "...") if settings.google_client_id else None,
        },
        "supabase": {
            "configured": bool(settings.supabase_url and settings.supabase_key),
            "connected": False,
            "error": None,
        },
    }

    if deps["supabase"]["configured"]:
        try:
            client = create_client(settings.supabase_url, settings.supabase_key)
            client.table("questionnaire_questions").select("id").limit(1).execute()
            deps["supabase"]["connected"] = True
        except Exception as exc:  # pragma: no cover - depende de entorno externo
            deps["supabase"]["error"] = str(exc)

    return deps


app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(courses_router, prefix="/api/courses", tags=["courses"])
app.include_router(registrations_router, prefix="/api/registrations", tags=["registrations"])
app.include_router(questionnaires_router, prefix="/api/questionnaires", tags=["questionnaires"])

