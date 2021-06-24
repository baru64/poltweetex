import os
from datetime import datetime, timezone

from . import models
from .database import SessionLocal

INDEX = int(os.environ['JOB_COMPLETION_INDEX'])


def main():
    with SessionLocal() as db:
        items = db.query(models.Item).all()
        item = items[INDEX]
        item.description = datetime.now(tz=timezone.utc).isoformat()
        db.add(item)
        db.commit()


if __name__ == "__main__":
    main()
