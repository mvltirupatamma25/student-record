from django.urls import path
from student.views import *
from student.libraries import *

app_name= 'student'

urlpatterns = [
    path('',Selection, name = 'Selection'),
    path('FACULTY/LOGIN/',Login_Faculty,name = 'Login_Faculty'),
    path('TEACHING/FACULTY/LOGIN/',Login_Teacher,name = 'Login_Teacher'),
    path('STUDENT/LOGIN/',Login_Student,name = 'Login_Student'),
    path('Faculty/Homepage/Welcome/',faculty_first,name = 'faculty_first'),
    path('Student/Homepage/Welcome/',Student_first,name = 'Student_first'),
    path('Teacher/Homepage/Welcome/',Teacher_first,name = 'Teacher_first'),
    path('Faculty/<Year>/<Group_Given>/',faculty_second, name ='faculty_second'),
    path('Student/Attendance/<Roll_Number>/<Group>/',Student_second, name = 'Student_second'),
    path('Teacher/<Id>/<Group>/<Year>/<Semester>/<Course>/',Teacher_second,name = 'Teacher_second'),
    path('Faculty/<Year>/<First_Name>/<Roll_Number>/',faculty_third, name = 'faculty_third'),
    path('Student/<Roll_Number>/Attendance/Semester/1/<Group>/',Student_second, name = 'Student_second'),
    path('Faculty/AddStudent/Details/Register/NewStudent/',Add_Student, name = 'Add_Student'),
    path('Student/Attendance/<Roll_Number>/<Group>/<Id>/<Course>/<Semester>/',Student_eighth, name = 'Student_eighth'),
    path('Teacher/Attendance/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_third, name = 'Teacher_third'),
    path('Teacher/Marks/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_eight, name = 'Teacher_eight'),
    path('Student/<Roll_Number>/Attendance/Semester/2/<Group>/',Student_third, name = 'Student_third'),
    path('Student/ExaminationMarks/<Roll_Number>/<Group>/',Student_ninth, name = 'Student_ninth'),
    path('Teacher/MarkAttendance/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_fourth, name = 'Teacher_fourth'),
    path('Teacher/IInternal/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_ninth, name = 'Teacher_ninth'),
    path('Faculty/Edit/<Year>/<Group>/<Roll_Number>/',Edit_Student, name = 'Edit_Student'),
    path("Student/Marks/Examination/<Roll_Number>/<Group>/<Semester>/<Exam>/",Student_tenth,name = 'Student_tenth'),
    path('Student/<Roll_Number>/Attendance/Semester/3/<Group>/',Student_fourth, name = 'Student_fourth'),
    path('Teacher/IIInternal/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_tenth, name = 'Teacher_tenth'),
    path('Teacher/UpdateAttendance/<Id>/<Year>/<Group>/<Semester>/<Course>/<Date>/',Teacher_fifth, name = 'Teacher_fifth'),
    path('Teacher/Assignment/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_eleven, name = 'Teacher_eleven'),
    path('Student/<Roll_Number>/Attendance/Semester/4/<Group>/',Student_fifth, name = 'Student_fifth'),
    path('Faculty/Delete/<Year>/<Group>/<Roll_Number>/',Delete_Student, name = 'Delete_Student'),
    path('Teacher/Semester/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_twelve, name = 'Teacher_twelve'),
    path('Faculty/Certificates/<Year>/<Group>/<Roll_Number>/',Certificate_Student, name = 'Certificate_Student'),
    path('Teacher/AddAttendance/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_sixth, name = 'Teacher_sixth'),
    path('Student/<Roll_Number>/Attendance/Semester/5/<Group>/',Student_sixth, name = 'Student_sixth'),
    path('Teacher/IInternalSubmit/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_thirteen, name = 'Teacher_thirteen'),
    path('Teacher/ChangeAttendance/<Id>/<Year>/<Group>/<Semester>/<Course>/<Date>/',Teacher_seventh, name = 'Teacher_seventh'),
    path('Teacher/IIInternalSubmit/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_fourteen, name = 'Teacher_fourteen'),
    path('Teacher/AssignmentSubmit/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_fifteen, name = 'Teacher_fifteen'),
    path('Student/<Roll_Number>/Attendance/Semester/6/<Group>/',Student_seventh, name = 'Student_seventh'),
    path('Teacher/SemesterSubmit/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_sixteen, name = 'Teacher_sixteen'),
    path('Teacher/SubmitAttendance/<Id>/<Year>/<Group>/<Semester>/<Course>/',Teacher_seventeen, name = 'Teacher_seventeen'),

]