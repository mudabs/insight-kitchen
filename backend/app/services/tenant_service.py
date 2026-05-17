from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.restaurant import Restaurant


def get_current_organization(
    db: Session,
    current_user: dict
):
    """
    Resolve organization using Clerk org_id.
    """

    clerk_org_id = current_user.get("org_id")

    if not clerk_org_id:

        raise HTTPException(
            status_code=400,
            detail="Organization ID not found in token"
        )

    organization = (
        db.query(Organization)
        .filter(
            Organization.clerk_org_id == clerk_org_id
        )
        .first()
    )

    if not organization:

        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    return organization


def get_restaurant_ids_for_organization(
    db: Session,
    organization_id: int
):
    """
    Return restaurant IDs
    belonging to organization.
    """

    restaurants = (
        db.query(Restaurant.id)
        .filter(
            Restaurant.organization_id == organization_id
        )
        .all()
    )

    return [r.id for r in restaurants]