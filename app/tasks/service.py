from app.tasks.models import Task, UpdateTask
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, text
from typing import List
from datetime import datetime, timezone

class TasksService():

    async def get_tasks(self, db_session:AsyncSession, limit:int = 20, offset:int = 0) -> List[Task] | None:
        result = await db_session.execute(select(Task).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_tasks_by_id(self, db_session:AsyncSession, id: int) -> Task | None:
        return await db_session.get(Task, id)
    
    async def get_tasks_by_user_id(self, db_session:AsyncSession, user_id: int, limit:int = 20, offset:int = 0) -> List[Task] | None:
        filter = text(f"user_id={user_id}")
        result = await db_session.execute(select(Task).filter(filter))
        return result.scalars().all()

    async def get_task_by_user_id(self, db_session:AsyncSession, user_id: int, task_id: int) -> Task | None:
        filter = text(f"user_id={user_id} and id={task_id}")
        result = await db_session.execute(select(Task).filter(filter))
        return result.scalars().first()

    async def create_task(self, db_session:AsyncSession, task: Task) -> Task:
        db_session.add(task)
        await db_session.commit()
        return task

    async def update_task(self, db_session: AsyncSession, task: Task, task_update: UpdateTask) -> Task:
        task_data = task_update.model_dump(exclude_unset=True) # default values are not touched
        task.updated_at = datetime.now(timezone.utc)
        task.sqlmodel_update(task_data)
        db_session.add(task)
        await db_session.commit()
        return task
    
    async def delete_task(self, db_session:AsyncSession, task: Task):
        await db_session.delete(task)
        await db_session.commit()