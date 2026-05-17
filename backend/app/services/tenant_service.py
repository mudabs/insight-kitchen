from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.restaurant import Restaurant

def get_current_organization(db: Session, current_user: dict):
    """Fetches the current organization from the database.
    """
    clerk_org_id = current_user.get("organization_id")

    if not clerk_org_id:
        raise HTTPException(
            status_code=400,
            detail="Organization ID not found in user payload"
        )

    organization = db.query(Organization).filter(Organization.id == clerk_org_id).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    
    return organization

def get_restaurants_for_organization(db: Session, organization_id: int):
    """Fetches all restaurants associated with the given organization.
    """
    restaurants = db.query(Restaurant).filter(Restaurant.organization_id == organization_id).all()
    return restaurants