from fastapi import APIRouter, Depends, HTTPException
from supabase import create_client
from app.auth.deps import get_current_user_id
from app.registrations.schemas import PreRegistrationOut, PreRegistrationIn
from app.storage.repository import get_repository
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/pre-register", response_model=PreRegistrationOut)
def pre_register(user_id: str = Depends(get_current_user_id)) -> PreRegistrationOut:
    repo = get_repository()
    pre = repo.create_pre_registration(user_id)
    return PreRegistrationOut(id=pre.id, user_id=pre.user_id, status=pre.status, created_at=pre.created_at)


@router.get("/status", response_model=PreRegistrationOut)
def status(user_id: str = Depends(get_current_user_id)) -> PreRegistrationOut:
    repo = get_repository()
    pre = repo.get_pre_registration_by_user(user_id)
    if not pre:
        pre = repo.create_pre_registration(user_id)
    return PreRegistrationOut(id=pre.id, user_id=pre.user_id, status=pre.status, created_at=pre.created_at)


@router.post("/pre-registro", response_model=PreRegistrationOut, status_code=201)
def create_pre_registro(data: PreRegistrationIn) -> PreRegistrationOut:
    """
    Endpoint público para el pre-registro del curso de Python.
    No requiere autenticación.
    Guarda los datos en Supabase.
    """
    settings = get_settings()
    
    if not settings.supabase_url or not settings.supabase_key:
        logger.error("Supabase no está configurado")
        raise HTTPException(
            status_code=500,
            detail="El servidor no está configurado para guardar registros en este momento"
        )
    
    try:
        supabase = create_client(settings.supabase_url, settings.supabase_key)
        
        # Preparar datos para Supabase
        registration_data = {
            "full_name": data.full_name,
            "student_code": data.student_code,
            "institutional_email": data.institutional_email,
            "personal_email": data.personal_email,
            "phone_whatsapp": data.phone_whatsapp,
            "career": data.career,
            "semester": data.semester,
            "programming_level": data.programming_level,
            "python_experience": data.python_experience,
            "operating_system": data.operating_system,
            "has_laptop": data.has_laptop,
            "preferred_days": data.preferred_days,
            "preferred_schedule": data.preferred_schedule,
            "motivation": data.motivation,
            "shirt_size": data.shirt_size,
            "attendance_commitment": data.attendance_commitment,
            "payment_option": data.payment_option,
            "scholarship_reason": data.scholarship_reason if data.payment_option == "scholarship" else None
        }
        
        # Insertar en Supabase
        response = supabase.table("pre_registrations").insert(registration_data).execute()
        
        if not response.data:
            logger.error(f"Error inserting into Supabase: {response}")
            raise HTTPException(
                status_code=500,
                detail="Error al guardar el registro"
            )
        
        inserted_data = response.data[0]
        logger.info(f"Pre-registration created: {inserted_data.get('id')}")
        
        return PreRegistrationOut(
            id=inserted_data.get("id"),
            user_id=None,
            status=None,
            created_at=None,
            full_name=inserted_data.get("full_name"),
            student_code=inserted_data.get("student_code"),
            institutional_email=inserted_data.get("institutional_email")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en pre-registro: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el pre-registro: {str(e)}"
        )

