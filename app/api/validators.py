from http import HTTPStatus
from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.crud.charity_project import charity_project_crud


async def check_charity_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name,
        session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_was_closed(
    project_id: int,
    session: AsyncSession
):
    project_close_date = await (
        charity_project_crud.get_close_date(
            project_id, session
        )
    )
    if project_close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession
):
    invested_project = await charity_project_crud.get_invested_amount(project_id,
                                                                      session)
    if invested_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_invested_amount(
    project_id: int,
    session: AsyncSession,
    amount_to_update: PositiveInt
):
    project_invested_amount = await charity_project_crud.get_invested_amount(
        project_id,
        session
    )
    if project_invested_amount > amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нужно больше донатить',
        )
