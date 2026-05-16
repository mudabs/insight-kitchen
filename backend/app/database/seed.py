from app.database.database import sessionLocal

from app.models.organization import Organization
from app.models.restaurant import Restaurant


db = sessionLocal()

# Create organization
org = Organization(
    name="Demo Organization"
)

db.add(org)

db.flush()

# Create restaurant
restaurant = Restaurant(
    organization_id=org.id,
    name="Main Campus Dining Hall",
    location="Saint Louis University"
)

db.add(restaurant)

db.commit()

print("Seed data inserted successfully.")