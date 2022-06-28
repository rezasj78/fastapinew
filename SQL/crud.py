from sqlalchemy.orm import Session

from . import models, schemas


# USER STUFF ###################################
def get_user(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
	return db.query(models.User).limit(100).all()


def get_user_by_phone(db: Session, phone_num: int):
	return db.query(models.User).filter(models.User.phone_num == phone_num).first()


def create_user(db: Session, user: schemas.UserCreate):
	supposedly_hashed_password = user.password + "think its hashed"
	db_user = models.User(phone_num=user.phone_num, hashed_password=supposedly_hashed_password, home_num=user.home_num,
						  role=user.role, name=user.name, email=user.email)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def get_users_by_apartment(db: Session, apartment_id: int):
	return db.query(models.User).filter(models.User.apartment_id == apartment_id).all()


def update_user_apartment(db: Session, phone_num, user: schemas.UserUpdate):
	db_user = get_user_by_phone(db, phone_num=phone_num)
	if db_user is None:
		return None
	user_data = user.dict()
	for key, value in user_data.items():
		setattr(db_user, key, value)
	db.add(db_user)
	db.commit()
	return db_user


def remove_user_apartment(db: Session, phone_num):
	db_user = get_user_by_phone(db, phone_num=phone_num)
	if db_user is None:
		return None
	db_user.apartment_id = None
	db.add(db_user)
	db.commit()
	return db_user


# REPAIRMAN STUFF ###########################
def get_repairman_by_phone(db: Session, phone_num: int):
	return db.query(models.Repairman).filter(models.Repairman.phone_num == phone_num).first()


def get_repairman(db: Session, repairman_id):
	return db.query(models.Repairman).filter(models.Repairman.id == repairman_id).first()


def get_repairmen(db: Session):
	return db.query(models.Repairman).limit(50).all()


def get_repairman_for_manager(db: Session, job: str, city: str):
	if db.query(models.Repairman).filter(models.Repairman.job == job and models.Repairman.city == city).first() is None:
		return None
	return db.query(models.Repairman).filter(models.Repairman.job == job and models.Repairman.city == city).all()


def create_repairman(db: Session, repairman: schemas.RepairmanCreate):
	supposedly_hashed_password = repairman.password + "think its hashed"
	db_repairman = models.Repairman(name=repairman.name, phone_num=repairman.phone_num,
									hashed_password=supposedly_hashed_password,
									email=repairman.email, job=repairman.job, state=repairman.state,
									city=repairman.city)
	db.add(db_repairman)
	db.commit()
	db.refresh(db_repairman)
	return db_repairman


# APARTMENT STUFF ######################

def get_apartment_by_manager(db: Session, phone_num: int):
	manager = get_user_by_phone(db=db, phone_num=phone_num)
	if manager is None:
		return None
	if manager.role == 0:
		return 0
	print(manager.id)
	db_apartment = db.query(models.Apartment).filter(models.Apartment.manager_id == manager.id).first()
	if db_apartment is None:
		return 1
	return db_apartment


def get_apartment_by_user(db: Session, user_phone):
	user = get_user_by_phone(db=db, phone_num=user_phone)
	if user is None:
		return None
	ap_id = user.apartment_id
	if ap_id is None:
		return 0
	return db.query(models.Apartment).filter(models.Apartment.id == ap_id).first()


def get_apartment(db: Session, apartment_id: int):
	return db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()


def creat_apartment(db: Session, apartment: schemas.ApartmentCreate):
	db_apartment = models.Apartment(name=apartment.name, address=apartment.address, city=apartment.city,
									state=apartment.state, floor_num=apartment.floor_num, unit_num=apartment.unit_num,
									manager_id=apartment.manager_id)
	db.add(db_apartment)
	db.commit()
	db.refresh(db_apartment)
	return db_apartment


# REQUEST FOR FINDING REPAIRMAN STUFF
def get_hiring_requests_for_manager(db: Session, manager_id):  # TODO
	if db.query(models.RequestsForRepairman).filter(
			models.RequestsForRepairman.manager_id == manager_id).first() is None:
		return None
	requests = db.query(models.RequestsForRepairman).filter(
		models.RequestsForRepairman.manager_id == manager_id).all()
	return requests


def get_hiring_requests_for_repairman(db: Session, repairman_id):  # TODO
	print(repairman_id)
	if db.query(models.RequestsForRepairman).filter(
			models.RequestsForRepairman.repairman_id == repairman_id).first() is None:
		return None
	requests = db.query(models.RequestsForRepairman).filter(
		models.RequestsForRepairman.repairman_id == repairman_id).all()
	return requests


def create_request_for_hiring_repairman(db: Session, request: schemas.RequestForRepairmanCreate):  # TODO
	manager_name = get_user(db, request.manager_id).name
	address = get_apartment(db, request.apartment_id).address
	db_request = models.RequestsForRepairman(repairman_id=request.repairman_id, manager_id=request.manager_id,
											 apartment_id=request.apartment_id, address=address,
											 manager_name=manager_name, job=request.job)
	db.add(db_request)
	db.commit()
	db.refresh(db_request)
	return db_request


def remove_hiring_request(db: Session, request_id: int):
	request = db.query(models.RequestsForRepairman).filter(models.RequestsForRepairman.id == request_id).first()
	if request is None:
		return None
	db.delete(request)
	db.commit()
	return 1


# APARTMENT AND REPAIRMAN STUFF ##################################

def get_apartment_and_repairmen_for_user(db: Session, apartment_id: int):
	if db.query(models.ApartmentAndRepairmen).filter(
			models.ApartmentAndRepairmen.apartment_id == apartment_id).first() is None:
		return None
	relations = db.query(models.ApartmentAndRepairmen).filter(
		models.ApartmentAndRepairmen.apartment_id == apartment_id).all()
	print(relations[0].id)
	print(relations[0].repairman_id)
	print(relations[0].apartment_id)
	print(relations[0].manager_id)
	print(relations[0].job)
	print(relations[0].repairman_name)
	print(relations[0].apartment_name)
	return relations


def get_apartment_and_repairmen_for_repairman(db: Session, repairman_id: int):
	if db.query(models.ApartmentAndRepairmen).filter(
			models.ApartmentAndRepairmen.repairman_id == repairman_id).first() is None:
		return None
	relations = db.query(models.ApartmentAndRepairmen).filter(
		models.ApartmentAndRepairmen.repairman_id == repairman_id).all()
	return relations


def create_apartment_and_repairmen(db: Session, aar: schemas.ApartmentAndRepairmenCreate):
	repairman_name = db.query(models.Repairman).filter(models.Repairman.id == aar.repairman_id).first()
	if repairman_name is None:
		return 1
	apartment_name = db.query(models.Apartment).filter(models.Apartment.id == aar.apartment_id).first()
	if apartment_name is None:
		return 2
	repairman_name = repairman_name.name
	apartment_name = apartment_name.name
	db_request = models.ApartmentAndRepairmen(repairman_id=aar.repairman_id, apartment_id=aar.apartment_id,
											  manager_id=aar.manager_id, job=aar.job, repairman_name=repairman_name,
											  apartment_name=apartment_name)
	db.add(db_request)
	db.commit()
	db.refresh(db_request)
	print("first4")
	return db_request


# REQUEST FOR REPAIR STUFF ##################################

def get_requests_repair_for_user(db: Session, user_id: int):
	if db.query(models.RequestForRepair).filter(models.RequestForRepair.user_id == user_id).first() is None:
		return None
	return db.query(models.RequestForRepair).filter(models.RequestForRepair.user_id == user_id).all()


def get_requests_repair_for_repairman(db: Session, repairman_id: int):
	if db.query(models.RequestForRepair).filter(models.RequestForRepair.repairman_id == repairman_id).first() is None:
		return None
	return db.query(models.RequestForRepair).filter(models.RequestForRepair.repairman_id == repairman_id).all()


def create_request_for_repair(db: Session, request: schemas.RequestForRepairCreate):
	db_request = models.RequestForRepair(user_id=request.user_id, repairman_id=request.repairman_id,
										 apartment_id=request.apartment_id, job=request.job,
										 description=request.description, user_name=request.user_name,
										 repairman_name=request.repairman_name)
	db.add(db_request)
	db.commit()
	db.refresh(db_request)
	return db_request


def remove_request_for_repair(db: Session, request_id: int):
	if db.query(models.RequestForRepair).filter(models.RequestForRepair.id == request_id).first() is None:
		return None
	request_db = db.query(models.RequestForRepair).filter(models.RequestForRepair.id == request_id).first()
	db.delete(request_db)
	db.commit()
	return 1


# REQUEST FOR REPAIR ELEVATOR STUFF ##################################

def get_request_repair_elv_for_repairman(db: Session, repairman_id: int):
	if db.query(models.RequestForRepairElv).filter(
			models.RequestForRepairElv.repairman_id == repairman_id and models.RequestForRepairElv.checked_by_manager == 1).first() is None:
		return None
	requests = db.query(models.RequestForRepairElv).filter(
		models.RequestForRepairElv.repairman_id == repairman_id and models.RequestForRepairElv.checked_by_manager == 1).all()
	return requests


def get_request_repair_elv_for_user(db: Session, user_id: int):
	if db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.user_id == user_id).first() is None:
		return None
	requests = db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.user_id == user_id).all()
	return requests


def get_request_repair_elv_for_manager(db: Session, manager_id: int):
	if db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.manager_id == manager_id).first() is None:
		return None
	requests = db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.manager_id == manager_id).all()
	return requests


def create_request_for_repair_elv(db: Session, request: schemas.RequestForRepairElvCreate):
	db_user = db.query(models.User).filter(models.User.id == request.user_id).first()
	if db_user.role == 0:
		db_apartment = db.query(models.Apartment).filter(models.Apartment.id == request.apartment_id).first()
		manager_id = db_apartment.manager_id
		db_manger = db.query(models.User).filter(models.User.id == manager_id).first()
		manager_name = db_manger.name
		db_request = models.RequestForRepairElv(user_id=request.user_id, repairman_id=request.repairman_id,
												apartment_id=request.apartment_id, manager_id=manager_id,
												description=request.description, user_name=request.user_name,
												repairman_name=request.description, manager_name=manager_name,
												checked_by_manager=0)
		db.add(db_request)
		db.commit()
		db.refresh(db_request)
		return db_request
	if db_user.role == 1:
		db_request = models.RequestForRepairElv(user_id=request.user_id, repairman_id=request.repairman_id,
												apartment_id=request.apartment_id, manager_id=request.user_id,
												description=request.description, user_name=request.user_name,
												repairman_name=request.description, manager_name=request.user_name,
												checked_by_manager=1)
		db.add(db_request)
		db.commit()
		db.refresh(db_request)
		return db_request


def remove_request_for_repair_elv(db: Session, request_id: int):
	if db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.id == request_id).first() is None:
		return None
	request_db = db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.id == request_id).first()
	db.delete(request_db)
	db.commit()
	return 1


def approve_request_for_repair_elv(db: Session, request_id: int):
	db_request = db.query(models.RequestForRepairElv).filter(models.RequestForRepairElv.id == request_id).first()
	db_request.checked_by_manager = 1
	db.add(db_request)
	db.commit()
	return db_request
