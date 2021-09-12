#default values
from student.libraries import *
from student.models import *

time = datetime.datetime.now()

def Year_Admission():
	return str(time.year)


def uuid_student():
	return uuid.uuid4()

def Attendance_Submit():
	return time

def dzero():
	return 0.00