from app.user.models import User, UserUpdate
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

class UserService:
    async def get_all_users(self, db_session: AsyncSession, offset: int = 0, limit: int = 100):
        result =  await db_session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_user_by_id(self, db_session: AsyncSession, user_id: int) -> User | None:
        return await db_session.get(User, user_id)

    async def add_user(self, db_session: AsyncSession, user: User) ->User:
        db_session.add(user)
        await db_session.commit()
        return user

    async def update_user(self, db_session: AsyncSession, user: User, user_update: UserUpdate) ->User:
        user_data = user_update.model_dump(exclude_unset=True) # default values are not touched
        user.updated_at = datetime.now(timezone.utc)
        user.sqlmodel_update(user_data)
        user = await self.add_user(db_session, user)
        return user

    async def remove_user(self, db_session: AsyncSession, user:User) ->None:
        await db_session.delete(user)
        await db_session.commit()