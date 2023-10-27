from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_name_duplicate,
                                check_project_was_closed,
                                check_project_was_invested,
                                check_charity_project_invested_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import investment_process
router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_reservation(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_name_duplicate(
        charity_project.name, session
    )
    new_project = await charity_project_crud.create(charity_project,
                                                    session,
                                                    commit=False)
    donations_to_add = investment_process(new_project,
                                          await donation_crud.get_uninvested_objects(session))
    session.add_all(donations_to_add)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_project_was_invested(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_project_was_closed(project_id, session)
    if object_in.full_amount is not None:
        await check_charity_project_invested_amount(project_id,
                                                    session,
                                                    object_in.full_amount)
    if object_in.name is not None:
        await check_charity_project_name_duplicate(object_in.name,
                                                   session)
    charity_project = await charity_project_crud.update(charity_project,
                                                        object_in,
                                                        session)
    return charity_project
