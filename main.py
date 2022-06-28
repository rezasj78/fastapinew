from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from SQL import crud, models, schemas
from SQL.databases import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#  SCHEMA FOR LOGGING IN
class verify(BaseModel):
	phone: int
	password: str


# SCHEMA FOR RESPONSE FOR DELETE
class DeleteResponse(BaseModel):
	response: str


# dependency

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


###############################################################################################
# ENDPOINT FOR USERS ###############################################################################################
@app.post("/user", response_model=schemas.User)
def creat_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db, phone_num=user.phone_num)
	if db_user:
		raise HTTPException(status_code=404, detail="phone number already exists")
	return crud.create_user(db, user)


@app.post('/user/login', response_model=schemas.User)
def login(user: verify, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db=db, phone_num=user.phone)
	if db_user:
		if db_user.hashed_password == (user.password + "think its hashed"):
			return db_user
		else:
			raise HTTPException(status_code=404, detail="wrong pass or phone")
	else:
		raise HTTPException(status_code=404, detail="wrong pass or phone")


@app.patch('/user/{phone_num}', response_model=schemas.User)
def update_user_apartment(user: schemas.UserUpdate, phone_num: int, db: Session = Depends(get_db)):
	db_user = crud.update_user_apartment(db=db, user=user, phone_num=phone_num)
	if db_user is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


@app.patch("/user/exit_apartment/{phone_num}", response_model=schemas.User)
def remove_user_from_apartment(phone_num: int, db: Session = Depends(get_db)):
	db_user = crud.remove_user_apartment(db, phone_num=phone_num)
	if db_user is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(dependency=get_db)):
	users = crud.get_users(db)
	return users


@app.get('/user/{phone_num}', response_model=schemas.User)
def get_user(phone_num: int, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_phone(db=db, phone_num=phone_num)
	if db_user is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


@app.get('/users/{apartment_id}', response_model=List[schemas.User])
def get_users_by_apartment(apartment_id, db: Session = Depends(get_db)):
	users = crud.get_users_by_apartment(db, apartment_id)
	if users is None:
		raise HTTPException(status_code=404, detail='no user was found for this apartment')
	return users


@app.get('/repairman_for_hire/{job}/{city}', response_model=List[schemas.Repairman])  # TODO
def get_repairmen_for_manager(job: str, city: str, db: Session = Depends(get_db)):
	repairmen = crud.get_repairman_for_manager(db, job, city)
	if repairmen is None:
		raise HTTPException(status_code=404, detail='no repairman found')
	return repairmen


###############################################################################################
# ENDPOINT FOR REPAIRMAN #############################################################################################
@app.post("/repairmen", response_model=schemas.Repairman)
def creat_repairman(repairman: schemas.RepairmanCreate, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db, phone_num=repairman.phone_num)
	if db_repairman:
		raise HTTPException(status_code=404, detail="phone number already exists")
	return crud.create_repairman(db, repairman)


@app.post('/repairman/login', response_model=schemas.Repairman)
def login(repairman: verify, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db=db, phone_num=repairman.phone)
	if db_repairman:
		if db_repairman.hashed_password == (repairman.password + "think its hashed"):
			return db_repairman
		else:
			raise HTTPException(status_code=404, detail="wrong pass or phone")
	else:
		raise HTTPException(status_code=404, detail="wrong pass or phone")


@app.get("/repairmen", response_model=List[schemas.Repairman])
def get_repairmen(db: Session = Depends(dependency=get_db)):
	users = crud.get_repairmen(db)
	return users


@app.get('/repairman/{phone_num}', response_model=schemas.Repairman)
def get_repairman(phone_num: int, db: Session = Depends(get_db)):
	db_repairman = crud.get_repairman_by_phone(db=db, phone_num=phone_num)
	if db_repairman is None:
		raise HTTPException(status_code=404, detail="user not found")
	return db_repairman


###############################################################################################
# ENDPOINT FOR APARTMENT #############################################################################################
@app.post('/apartment', response_model=schemas.Apartment)
def create_apartment(apartment: schemas.ApartmentCreate, db: Session = Depends(get_db)):
	return crud.creat_apartment(db, apartment=apartment)


@app.get('/manager/apartment/{phone_num}', response_model=schemas.Apartment)
def get_apartment_by_manager(phone_num: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment_by_manager(db, phone_num=phone_num)
	if apartment is None:
		raise HTTPException(status_code=404, detail="user not found")
	if apartment == 0:
		raise HTTPException(status_code=404, detail="phone num does not belong to manager")
	if apartment == 1:
		raise HTTPException(status_code=404, detail="manager has no apartment")
	return apartment


@app.get('/user/apartment/{phone_num}', response_model=schemas.Apartment)
def get_apartment_by_user(phone_num: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment_by_user(db, phone_num)
	if apartment is None:
		raise HTTPException(status_code=404, detail="user not found")
	if apartment == 0:
		raise HTTPException(status_code=404, detail="user has no apartment")
	return apartment


@app.get('/apartment/{apartment_id}', response_model=schemas.Apartment)
def get_apartment_by_id(apartment_id: int, db: Session = Depends(get_db)):
	apartment = crud.get_apartment(db, apartment_id)
	if apartment is None:
		raise HTTPException(status_code=404, detail="apartment not found")
	return apartment


###############################################################################################
# ENDPOINT FOR HIRING REQUEST ##########################################################################################


@app.post('/requests/hiring', response_model=schemas.RequestForRepairman)
def create_request_for_hiring(request: schemas.RequestForRepairmanCreate, db: Session = Depends(get_db)):
	return crud.create_request_for_hiring_repairman(db, request)


@app.get('/requests/hiring/manager/{manager_id}', response_model=List[schemas.RequestForRepairman])
def get_hiring_requests_for_manager(manager_id: int, db: Session = Depends(get_db)):
	requests = crud.get_hiring_requests_for_manager(db, manager_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no requests found')
	return requests


@app.get('/requests/hiring/repairman/{repairman_id}', response_model=List[schemas.RequestForRepairman])
def get_hiring_requests_for_repairman(repairman_id: int, db: Session = Depends(get_db)):
	requests = crud.get_hiring_requests_for_repairman(db, repairman_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no requests found')
	return requests


@app.delete('/requests/hiring/remove/{request_id}', response_model=DeleteResponse)
def remove_hiring_request(request_id: int, db: Session = Depends(get_db)):
	request = crud.remove_hiring_request(db=db, request_id=request_id)
	if request is None:
		raise HTTPException(status_code=404, detail="request not found")


###############################################################################################
# ENDPOINT FOR Apartment AND REPAIRMEN ################################################################################

@app.post('/apartment_and_repairmen', response_model=schemas.ApartmentAndRepairmen)
def create_apartment_and_repairmen(relation: schemas.ApartmentAndRepairmenCreate, db: Session = Depends(get_db)):
	db_relation = crud.create_apartment_and_repairmen(db, relation)
	if db_relation == 1:
		raise HTTPException(status_code=404, detail='repairman not found')
	if db_relation == 2:
		raise HTTPException(status_code=404, detail='apartment not found')
	print("first5")

	return db_relation


@app.get('/apartment_and_repairmen/user/{apartment_id}', response_model=List[schemas.ApartmentAndRepairmen])
def get_repairmen_for_user(apartment_id: int, db: Session = Depends(get_db)):
	repairmen = crud.get_apartment_and_repairmen_for_user(db, apartment_id)
	if repairmen is None:
		raise HTTPException(status_code=404, detail='no repairmen was found')
	else:
		return repairmen


@app.get('/apartment_and_repairmen/repairman/{repairman_id}', response_model=List[schemas.ApartmentAndRepairmen])
def get_apartments_for_repairmen(repairman_id: int, db: Session = Depends(get_db)):
	apartments = crud.get_apartment_and_repairmen_for_repairman(db, repairman_id)
	if apartments is None:
		raise HTTPException(status_code=404, detail='no apartment was found')
	else:
		return apartments


###############################################################################################
# ENDPOINT FOR REQUESTS FOR REPAIR ################################################################################


@app.post('/request_for_repair', response_model=schemas.RequestForRepair)
def create_request_for_repair(request: schemas.RequestForRepairCreate, db: Session = Depends(get_db)):
	db_request = crud.create_request_for_repair(db, request)
	return db_request


@app.get('/request_for_repair/repairman/{repairman_id}', response_model=List[schemas.RequestForRepair])
def get_request_repair_for_repairman(repairman_id: int, db: Session = Depends(get_db)):
	requests = crud.get_requests_repair_for_repairman(db, repairman_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no request was found')
	return requests


@app.get('/request_for_repair/user/{user_id}', response_model=List[schemas.RequestForRepair])
def get_request_repair_for_user(user_id: int, db: Session = Depends(get_db)):
	requests = crud.get_requests_repair_for_user(db, user_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no request was found')
	return requests


@app.delete('/request_for_repair/remove/{request_id}', response_model=DeleteResponse)
def remove_request(request_id: int, db: Session = Depends(get_db)):
	response = crud.remove_request_for_repair(db, request_id)
	if response is None:
		raise HTTPException(status_code=404, detail="request not found")
	return {"response": "success"}


###############################################################################################
# ENDPOINT FOR REQUESTS FOR REPAIR ELV ################################################################################


@app.post('/request_for_repair_elv', response_model=schemas.RequestForRepairElv)
def create_request_for_repair(request: schemas.RequestForRepairElvCreate, db: Session = Depends(get_db)):
	db_request = crud.create_request_for_repair_elv(db, request)
	return db_request


@app.get('/request_for_repair_elv/repairman/{repairman_id}', response_model=List[schemas.RequestForRepairElv])
def get_request_repair_elv_for_repairman(repairman_id: int, db: Session = Depends(get_db)):
	requests = crud.get_request_repair_elv_for_repairman(db, repairman_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no request was found')
	return requests


@app.get('/request_for_repair_elv/user/{user_id}', response_model=List[schemas.RequestForRepairElv])
def get_request_repair_elv_for_user(user_id: int, db: Session = Depends(get_db)):
	requests = crud.get_request_repair_elv_for_user(db, user_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no request was found')
	return requests


@app.get('/request_for_repair_elv/manager/{manager_id}', response_model=List[schemas.RequestForRepairElv])
def get_request_repair_elv_for_manager(manager_id: int, db: Session = Depends(get_db)):
	requests = crud.get_request_repair_elv_for_manager(db, manager_id)
	if requests is None:
		raise HTTPException(status_code=404, detail='no request was found')
	return requests


@app.delete('/request_for_repair_elv/remove/{request_id}', response_model=DeleteResponse)
def remove_elv_request(request_id: int, db: Session = Depends(get_db)):
	response = crud.remove_request_for_repair_elv(db, request_id)
	if response is None:
		raise HTTPException(status_code=404, detail="request not found")
	return {"response": "success"}


@app.patch('/request_for_repair_elv/approve/{request_id}', response_model=schemas.RequestForRepairElv)
def approve_request(request_id: int, db: Session = Depends(get_db)):
	response = crud.approve_request_for_repair_elv(db, request_id)
	return response


@app.delete('/request_for_repair_elv/delete/{request_id}', response_model=DeleteResponse)
def remove_request_elv(request_id: int, db: Session = Depends(get_db)):
	response = crud.remove_request_for_repair_elv(db, request_id)
	if response is None:
		raise HTTPException(status_code=404, detail="request not found")
	return {"response": "success"}
