from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter(prefix="/cats", tags=["cats"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.CatOut)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_cat(db, cat)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid breed")


@router.get("/", response_model=list[schemas.CatOut])
def list_cats(db: Session = Depends(get_db)):
    return crud.get_cats(db)


@router.get("/{cat_id}", response_model=schemas.CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.put("/{cat_id}", response_model=schemas.CatOut)
def update_cat_salary(cat_id: int, update: schemas.CatUpdate, db: Session = Depends(get_db)):
    cat = crud.update_cat_salary(db, cat_id, update.salary)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.delete_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return {"detail": "Cat deleted"}
