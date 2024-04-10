"""
This module handle all json/dictionary structure using in APIs
"""
from typing import Literal
from pydantic import BaseModel, EmailStr, SecretStr

# authentication


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None
    role: str


class User(BaseModel):
    ID: int
    username: str
    disabled: bool or None = None
    role: Literal["Admin", "Staff", "Student"]


class UserInDb(User):
    hashed_password: str


class DepartmentMaster(BaseModel):
    deptID: int
    deptName: str = ""
    courseName: str = ""
    courseSubject: list = []


class StaffMaster(DepartmentMaster):
    staffID: int
    username: str
    FullName: str
    EmailID: EmailStr
    password: SecretStr
    disabled: bool or None = None
    role: str = "Staff"


class Announcement(StaffMaster):
    msgID: int
    staffID: int
    courseName: str
    Live: int
    InsertDate: str
    Msg: str


class StudentMaster(DepartmentMaster):
    studID: int
    username: str
    password: SecretStr
    deptID: int or None = None
    DivName: str
    FullName: str
    EmailID: EmailStr
    MobileNumber: int
    DOB: str
    ClgLocation: str
    Address:  str
    Reg_Year: str
    Reg_Device: str
    disabled: bool or None = None
    role: str = "Student"


class AttendanceMaster(BaseModel):
    attendID: int
    studID: int
    StudLocation: str
    Subject: str
    Device: str
    InsertTime: str


class UpdateCreds(BaseModel):
    userid: int
    username: str
    password: SecretStr
    role: Literal["Admin", "Staff", "Student"]
