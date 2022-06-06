from typing import Any, List, Optional

from src.crud.base import AppCRUD


def create(obj_in: Any) -> Any:
    # db_obj = UserLevel(**obj_in.dict())
    # self.db.add(db_obj)
    # self.commit()
    # self.db.refresh(db_obj)
    # return db_obj
    return None


class ArticleCRUD(AppCRUD):
    def get(self, obj_id: int) -> Optional[Any]:
        # return self.db.query(UserLevel).get(obj_id)
        return None

    def get_all(self) -> List[Any]:
        # users = self.db.query(UserLevel).all()
        # users = [schemas.UserLevelResponse.from_orm(user) for user in users]
        # return users
        return []

    def get_by_level_name(self) -> None:
        # return (
        #     self.db.query(UserLevel).filter(UserLevel.level_name == level_name).first()
        # )
        return None
