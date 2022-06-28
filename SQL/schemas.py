from typing import Union

from pydantic import BaseModel


class ApartmentBase(BaseModel):
	name: str
	address: str
	city: str
	state: str
	floor_num: int
	unit_num: int
	manager_id: Union[int, None] = None


class ApartmentCreate(ApartmentBase):
	pass


class Apartment(ApartmentBase):
	id: int

	class Config:
		orm_mode = True


class UserBase(BaseModel):
	phone_num: int
	email: str
	name: str
	home_num: str
	role: int


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int
	apartment_id: Union[int, None] = None

	class Config:
		orm_mode = True


class UserUpdate(BaseModel):
	apartment_id: int

	class Config:
		orm_mode = True


class RepairmanBase(BaseModel):
	name: str
	email: str
	phone_num: int
	email: str
	job: str
	state: str
	city: str


class RepairmanCreate(RepairmanBase):
	password: str


class Repairman(RepairmanBase):
	id: int

	class Config:
		orm_mode = True


class RequestForRepairmanBase(BaseModel):
	repairman_id: int
	manager_id: int
	apartment_id: int
	job: str


class RequestForRepairmanCreate(RequestForRepairmanBase):
	pass


class RequestForRepairman(RequestForRepairmanBase):
	id: int
	address: str
	manager_name: str

	class Config:
		orm_mode = True


class ApartmentAndRepairmenBase(BaseModel):
	repairman_id: int
	apartment_id: int
	manager_id: int
	job: str


class ApartmentAndRepairmenCreate(ApartmentAndRepairmenBase):
	pass


class ApartmentAndRepairmen(ApartmentAndRepairmenBase):
	id: int
	repairman_name: str
	apartment_name: str

	class Config:
		orm_mode = True


class RequestForRepairBase(BaseModel):
	user_id: int
	repairman_id: int
	apartment_id: int
	job: str
	description: str
	user_name: str
	repairman_name: str


class RequestForRepairCreate(RequestForRepairBase):
	pass


class RequestForRepair(RequestForRepairBase):
	id: int

	class Config:
		orm_mode = True


class RequestForRepairElvBase(BaseModel):
	user_id: int
	repairman_id: int
	apartment_id: int
	description: str
	user_name: str
	repairman_name: str


class RequestForRepairElvCreate(RequestForRepairElvBase):
	pass


class RequestForRepairElv(RequestForRepairElvCreate):
	id: int
	manager_id: int
	manager_name: str
	checked_by_manager: int

	class Config:
		orm_mode = True
