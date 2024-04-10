import datetime
import logging
from json_struct import *
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from DB_Ops import (
    insert_dept,
    insert_staff,
    insert_attendance,
    insert_student,
    insert_announcement,
    update_creds,
    select_user,
    select_dept
)
from common_modules import (
    HASH_ALGO,
    SECRET_KEY,
    invite_user_mail,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logging.getLogger('passlib').setLevel(logging.ERROR)
app = FastAPI()


async def get_current_user(token: str = Depends(oauth_2_scheme)):
    """
    Verify user for authentication.
    :param token: user details= username and creds
    :return: exception or full user data
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not verify credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGO])
        username: str = playload.get("sub")
        role: str = playload.get("role")
        if username is None:
            print("us is none")
            raise credentials_exception

        token_data = TokenData(username=username, role=role)
    except JWTError as e:
        print("us is jwt" + str(e))
        raise credentials_exception

    user = select_user(username=token_data.username, role=token_data.role)
    if user[0] is False:
        print("us is False")
        raise credentials_exception
    return user[1]


async def get_current_active_user(current_user: UserInDb = Depends(get_current_user)):
    """
    Checks if user token is active or not
    :param current_user: user details with latest token
    :return: exception or current user data
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@app.get('/', description="Get Server Heartbeat")
def home():
    current_dt = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    return {"Status": "Hello From SmartMark Backend!!", 'ServerTime': current_dt}


@app.post("/token", response_model=Token, description="validate user and get token")
async def login_for_access_token(user_role: str, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, user_role)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.username), "role": user_role}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/add_dept', description="Insert Department details")
async def add_dept(dept_data: DepartmentMaster):
    resp = insert_dept(dept_data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Insert Data " + resp[1])
    return {"Status": resp[1]}


@app.post('/add_staff', description="Insert Staff details")
async def add_staff(staff_data: StaffMaster):
    resp = insert_staff(staff_data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Insert Data " + resp[1])
    # send invitation to user
    invite_user_mail(staff_data.FullName, staff_data.username, staff_data.EmailID,
                     staff_data.password.get_secret_value())
    return {"Status": resp[1]}


@app.post('/add_student', description="Insert Student details")
async def add_student(stud_data: StudentMaster):
    resp = insert_student(stud_data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Insert Data " + resp[1])
    # send invitation to user
    invite_user_mail(stud_data.FullName, str(stud_data.username), stud_data.EmailID,
                     stud_data.password.get_secret_value())
    return {"Status": resp[1]}


@app.post('/add_attendance', description="Insert Student Attendance details")
async def add_attendance(attend_data: AttendanceMaster, current_user: User = Depends(get_current_active_user)):
    resp = insert_attendance(attend_data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Insert Data " + resp[1])
    return {"Status": resp[1]}


@app.post('/add_announcement', description="Insert Announcement from Staff details")
async def add_announcement(announce_data: Announcement, current_user: User = Depends(get_current_active_user)):
    resp = insert_announcement(announce_data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Insert Data " + resp[1])
    return {"Status": resp[1]}


@app.put('/update_user_cred', description="Update Credential of user")
async def update_user_cred(data: UpdateCreds, current_user: User = Depends(get_current_active_user)):
    resp = update_creds(data)
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Failed To Update Password Try Again Later " + resp[1])
    return {"Status": resp[1]}


@app.get('/get_dept', description="Get all Departments")
async def get_dept():
    resp = select_dept()
    if not resp[0]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unable to Fetch Data, Try Again Later " + resp[1])
    return {"Status": resp[1]}


@app.get('/test')
async def hello(current_user: User = Depends(get_current_active_user)):
    return current_user

