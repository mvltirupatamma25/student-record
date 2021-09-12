from django.contrib import admin
from student.models import *
# Register your models here.
admin.site.register(Groups)
admin.site.register(Student)
admin.site.register(Courses)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Student_Marks)
admin.site.register(Student_Attendance)
admin.site.register(Teacher_Course)