from fastapi import APIRouter, Depends, status, Request
from typing import List
from app.database.db_setup import DbSession
from app.tasks.service import TasksService
from app.user.dependencies import AccessTokenBearer
from app.tasks.models import Task, TaskPublic, CreateTask, UpdateTask
from app.user.dependencies import user_role

router = APIRouter(
    prefix = "/tasks",
    tags = ["tasks"]
)

task_service = TasksService()
access_token_bearer = AccessTokenBearer() 


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskPublic], dependencies=[user_role])
async def get_tasks(
    db_session: DbSession,
    user_creds= Depends(access_token_bearer) # call to __call__ 
):
    user_id = int(user_creds.get('user').get('user_id'))
    tasks = await task_service.get_tasks_by_user_id(db_session, user_id)
    return tasks

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskPublic, dependencies=[user_role])
async def create_task(
    req_body: CreateTask,
    db_session: DbSession,
    user_creds = Depends(access_token_bearer)
):
    data = req_body.model_dump()
    task = Task(**data)
    task.user_id = int(user_creds.get('user').get('user_id'))
    task = await task_service.create_task(db_session, task)
    return task

@router.patch("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskPublic, dependencies=[user_role])
async def update_task(
    db_session: DbSession,
    task_id: int,
    req_body: UpdateTask,
    user_creds = Depends(access_token_bearer)
):
    user_id = int(user_creds.get('user').get('user_id'))
    task = await task_service.get_task_by_user_id(db_session, user_id, task_id)
    task = await task_service.update_task(db_session, task, req_body)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role])
async def delete_task(
    db_session: DbSession,
    task_id:int,
    user_creds = Depends(access_token_bearer)
):
    user_id = int(user_creds.get('user').get('user_id'))
    task = await task_service.get_task_by_user_id(db_session, user_id, task_id)
    await task_service.delete_task(db_session, task)

