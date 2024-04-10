"""
This Module Handles all DB operations
"""
import json
import datetime
from json_struct import *
import pandas as pd
from sqlalchemy.sql import func
from common_modules import get_password_hash
from sqlalchemy import DateTime, create_engine, update, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


def initialize_engine():
    return create_engine("sqlite:///database/smart_mark.db")


def initialize_tables(engine):
    Base.metadata.create_all(engine)


# this will create table in database


class DeptMaster(Base):
    __tablename__ = "DepartmentMaster"
    deptID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deptName: Mapped[str] = mapped_column(nullable=False)
    courseName: Mapped[str] = mapped_column(unique=True, nullable=False)
    courseSubject: Mapped[str] = mapped_column(nullable=False)


class FacultyMaster(Base):
    __tablename__ = "StaffMaster"
    staffID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    deptID: Mapped[int] = mapped_column(nullable=False)
    FullName: Mapped[str] = mapped_column(nullable=False)
    EmailID: Mapped[str] = mapped_column(nullable=False)


class AnnouncementMaster(Base):
    __tablename__ = "Announcements"
    msgID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    staffID: Mapped[int] = mapped_column(nullable=False)
    courseName: Mapped[str] = mapped_column(nullable=False)
    Live: Mapped[int] = mapped_column(nullable=False, onupdate=1)
    Msg: Mapped[str] = mapped_column(nullable=False)
    InsertDate: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          onupdate=datetime.datetime.now(), nullable=False)


class StudMaster(Base):
    __tablename__ = "StudentMaster"
    studID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    deptID:  Mapped[int] = mapped_column(nullable=False)
    DivName:  Mapped[str] = mapped_column(nullable=True)
    FullName:  Mapped[str] = mapped_column(nullable=False)
    EmailID:  Mapped[str] = mapped_column(nullable=False, unique=True)
    MobileNumber:  Mapped[int] = mapped_column(nullable=False, unique=True)
    DOB:  Mapped[str] = mapped_column(nullable=False)
    ClgLocation:  Mapped[str] = mapped_column(nullable=False)
    Address:  Mapped[str] = mapped_column(nullable=False)
    Reg_Year:  Mapped[str] = mapped_column(nullable=False)
    Reg_Device:  Mapped[str] = mapped_column(nullable=True)


class Attendance(Base):
    __tablename__ = "AttendanceMaster"
    attendID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    studID:  Mapped[int] = mapped_column(nullable=False)
    StudLocation:  Mapped[str] = mapped_column(nullable=True)
    Subject:  Mapped[str] = mapped_column(nullable=False)
    Device:  Mapped[str] = mapped_column(nullable=True)
    InsertTime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          onupdate=datetime.datetime.now(), nullable=False)


initialize_tables(initialize_engine())


def insert_dept(data: DepartmentMaster):
    """
    Insert into DepartmentMaster table
    :param data: dict with DepartmentMaster details
    :return: status of insertion
    """
    engine = initialize_engine()
    dept_data = DeptMaster(
        deptName=data.deptName,
        courseName=data.courseName,
        courseSubject=json.dumps(data.courseSubject)
    )
    with Session(engine) as session:
        try:
            session.add(dept_data)
            session.commit()
            return True, "Dept Added"
        except Exception as e:
            return False, str(e)


def insert_staff(data: StaffMaster):
    """
    Insert into StaffMaster table
    :param data: dict with StaffMaster details
    :return: status of insertion
    """
    engine = initialize_engine()
    staff_data = FacultyMaster(
        username=data.username,
        password=get_password_hash(data.password.get_secret_value()),
        deptID=data.deptID,
        FullName=data.FullName,
        EmailID=data.EmailID,
    )
    with Session(engine) as session:
        try:
            session.add(staff_data)
            session.commit()
            return True, "Staff Added"
        except Exception as e:
            return False, str(e)


def insert_announcement(data: Announcement):
    """
    Insert into Announcements table
    :param data: dict with Announcements details
    :return: status of insertion
    """
    engine = initialize_engine()
    announce_data = AnnouncementMaster(
        staffID=data.staffID,
        courseName=data.courseName,
        Live=data.Live,
        Msg=data.Msg
    )
    with Session(engine) as session:
        try:
            session.add(announce_data)
            session.commit()
            return True, "Announcement Added"
        except Exception as e:
            return False, str(e)


def insert_student(data: StudentMaster):
    """
    Insert into StudentMaster table
    :param data: dict with Announcements details
    :return: status of insertion
    """
    engine = initialize_engine()
    stud_data = StudMaster(
        username=data.username,
        password=get_password_hash(data.password.get_secret_value()),
        deptID=data.deptID,
        DivName=data.DivName,
        FullName=data.FullName,
        EmailID=data.EmailID,
        MobileNumber=data.MobileNumber,
        DOB=data.DOB,
        ClgLocation=data.ClgLocation,
        Address=data.Address,
        Reg_Year=data.Reg_Year,
        Reg_Device=data.Reg_Device
    )
    with Session(engine) as session:
        try:
            session.add(stud_data)
            session.commit()
            return True, "Student Added"
        except Exception as e:
            return False, str(e)


def insert_attendance(data: AttendanceMaster):
    """
    Insert into Announcements table
    :param data: dict with Announcements details
    :return: status of insertion
    """
    engine = initialize_engine()
    attendance_data = Attendance(
        studID=data.studID,
        StudLocation=data.StudLocation,
        Subject=data.Subject,
        Device=data.Device
    )
    with Session(engine) as session:
        try:
            session.add(attendance_data)
            session.commit()
            return True, "Attendance Added"
        except Exception as e:
            return False, str(e)


def update_creds(data: UpdateCreds):
    """
    Updates User credentials
    :param data: dict with username, pwd and role
    :return: status of update
    """
    engine = initialize_engine()
    with Session(engine) as session:
        try:
            if data.role == "Staff":
                stmt = update(FacultyMaster).where(FacultyMaster.staffID == data.userid).values(
                    password=data.password.get_secret_value())
            elif data.role == "Student":
                stmt = update(StudMaster).where(StudMaster.studID == data.userid).values(
                    password=data.password.get_secret_value())

            session.execute(stmt)
            session.commit()
            return True, "Password Updated"
        except Exception as e:
            return False, str(e)


def select_user(username, role):
    """
    check if user is present in db
    :param username: username/PNR-Number of user
    :param role: Role of user ["Admin", "Staff", "Student"]
    :return: Userdata
    """
    engine = initialize_engine()
    with Session(engine) as session:
        try:
            if role == "Staff":
                stmt = select(FacultyMaster).where(FacultyMaster.username == username)
            elif role == "Student":
                stmt = select(StudMaster).where(StudMaster.username == username)
            rows = pd.read_sql(stmt, session.bind).to_dict('records')[0]
            rows.update(disabled=False)
            return True, StaffMaster(**rows) if role == "Staff" else StudentMaster(**rows)
        except Exception as e:
            return False, str(e)


def select_dept():
    """
    This will return all departments form the table
    :return: department data
    """
    engine = initialize_engine()
    with Session(engine) as session:
        try:
            stmt = select(DeptMaster)
            rows = pd.read_sql(stmt, session.bind).to_dict('records')
            data = []
            for row in rows:
                row['courseSubject'] = json.loads(row['courseSubject'])
                data.append(row)
            return True, data
        except Exception as e:
            return False, str(e)
