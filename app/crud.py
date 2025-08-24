from sqlalchemy.orm import Session
from . import models, schemas
from .utils import validate_breed


def create_cat(db: Session, cat: schemas.CatCreate):
    if not validate_breed(cat.breed):
        raise ValueError("Invalid breed")

    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def get_cats(db: Session):
    return db.query(models.Cat).all()


def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()


def update_cat_salary(db: Session, cat_id: int, salary: float):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db_cat.salary = salary
        db.commit()
        db.refresh(db_cat)
    return db_cat


def delete_cat(db: Session, cat_id: int):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
    return db_cat
