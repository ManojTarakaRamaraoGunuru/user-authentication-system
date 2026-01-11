from app.database.db_setup import DbSession
from app.models.user import User, UserUpdate
from sqlmodel import select


def get_all_users(db_session: DbSession, offset: int = 0, limit: int = 100):
    return db_session.exec(select(User).offset(offset).limit(limit)).all()

def get_user_by_id(db_session: DbSession, user_id: int) -> User | None:
    return db_session.get(User, user_id)

def add_user(db_session: DbSession, user: User) ->User:
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def update_user(db_session: DbSession, user: User, user_update: UserUpdate) ->User:
    user_data = user_update.model_dump(exclude_unset=True) # default values are not touched
    user.sqlmodel_update(user_data)
    user = add_user(db_session, user)
    return user

def remove_user(db_session:DbSession, user:User) ->None:
    db_session.delete(user)
    db_session.commit()