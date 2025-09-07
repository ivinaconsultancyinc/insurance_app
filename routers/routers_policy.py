from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schenas.policy_schema import PolicyResponse, PolicyCreate, PolicyUpdate
from schemas.document_schema import DocumentOut
from database import get_db
import services
router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)
@router.post("/", response_model=PolicyOut, status_code=status.HTTP_201_CREATED)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    return services.policy_service.create_policy(db, policy)
@router.get("/", response_model=List[PolicyOut])
def get_all_policies(db: Session = Depends(get_db)):
    return services.policy_service.get_all_policies(db)
@router.get("/{policy_id}", response_model=PolicyOut)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    db_policy = services.policy_service.get_policy_by_id(db, policy_id)
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return db_policy
@router.put("/{policy_id}", response_model=PolicyOut)
def update_policy(policy_id: int, policy_update: PolicyUpdate, db: Session = Depends(get_db)):
    return services.policy_service.update_policy(db, policy_id, policy_update)
@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    services.policy_service.delete_policy(db, policy_id)
# 🔗 New endpoint to fetch documents related to a policy
@router.get("/{policy_id}/documents", response_model=List[DocumentOut])
def get_documents_for_policy(policy_id: int, db: Session = Depends(get_db)):
    return services.document_service.get_documents_by_entity(db, "policy", policy_id)





