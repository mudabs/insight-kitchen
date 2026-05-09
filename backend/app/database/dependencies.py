#Import database session factory
from app.database.database import sessionLocal

def get_db():
    """
    Creates a new database session for each request.

    WHY?
    Database sessions should not stay open forever.
    Each API request gets its own session.

    This prevents issues like:
    - Memory leaks from sessions that never close.
    -Locked connections that never release resources.
    -Concurrency issues from multiple requests sharing the same session.
    """

    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()