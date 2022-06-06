from typing import Any

from sqlalchemy.orm import Session


# parent src crud
class AppCRUD:
    db: Session
    logger: Any

    def __init__(self, db: Session = None, logger: Any = None):
        self.db = db
        self.logger = logger

    def commit(self) -> None:
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            if self.logger:
                self.logger.error(f"Exception :: {e}")
            else:
                print(f"Exception :: {e}")
            raise e
