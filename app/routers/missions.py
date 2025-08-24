from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import SessionLocal

router = APIRouter(prefix="/missions", tags=["missions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.MissionOut)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    if len(mission.targets) < 1 or len(mission.targets) > 3:
        raise HTTPException(status_code=400, detail="Mission must have 1 to 3 targets")

    db_mission = models.Mission(is_complete=mission.is_complete)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target in mission.targets:
        db_target = models.Target(
            mission_id=db_mission.id,
            name=target.name,
            country=target.country,
            notes=target.notes,
            is_complete=target.is_complete
        )
        db.add(db_target)
    db.commit()
    db.refresh(db_mission)

    return db_mission


@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned to a cat, cannot delete")

    db.delete(mission)
    db.commit()
    return {"detail": "Mission deleted"}


@router.put("/{mission_id}/assign/{cat_id}", response_model=schemas.MissionOut)
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already has a cat assigned")

    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    active_mission = db.query(models.Mission).filter(models.Mission.cat_id == cat_id, models.Mission.is_complete == False).first()
    if active_mission:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


@router.put("/targets/{target_id}/notes", response_model=schemas.TargetOut)
def update_notes(target_id: int, notes: str, db: Session = Depends(get_db)):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = db.query(models.Mission).filter(models.Mission.id == target.mission_id).first()
    if mission.is_complete or target.is_complete:
        raise HTTPException(status_code=400, detail="Notes cannot be updated for completed target or mission")

    target.notes = notes
    db.commit()
    db.refresh(target)
    return target


@router.put("/targets/{target_id}/complete", response_model=schemas.TargetOut)
def complete_target(target_id: int, db: Session = Depends(get_db)):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    target.is_complete = True
    db.commit()
    db.refresh(target)

    mission = db.query(models.Mission).filter(models.Mission.id == target.mission_id).first()
    all_done = all(t.is_complete for t in mission.targets)
    if all_done:
        mission.is_complete = True
        db.commit()

    return target


@router.get("/", response_model=List[schemas.MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()


@router.get("/{mission_id}", response_model=schemas.MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
