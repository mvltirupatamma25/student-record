from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from student.validations import *
from student.choices import *
from student.defaults import *

# Create your models here.

class Groups(models.Model):
	#Group
	Group = models.CharField(default = '',max_length = 10, primary_key = True)
	Class = models.CharField(default  = '',max_length = 10)
	Groups_Type = models.CharField(default = '',max_length=10, choices = Groups_Type_Choices)

class Student(models.Model):
	#TIMESTAMP
	Date_Time = models.DateTimeField(auto_now = True)
	Year_Of_Admission = models.IntegerField(default = Year_Admission)
	#STUDENT DETAILS
	First_Name = models.CharField(max_length = 50)
	Middle_Name = models.CharField(max_length = 50, blank = True)
	Last_Name = models.CharField(max_length = 50)
	Class = models.CharField(max_length = 50)
	Group = models.ForeignKey(Groups,on_delete = models.PROTECT)
	Admission_Number = models.CharField(max_length = 50)
	Roll_Number = models.CharField(max_length = 50, primary_key = True)
	Date_of_Birth = models.CharField(max_length = 10,help_text = 'YYYY-MM-DD')
	Gender = models.CharField(max_length= 20, choices = Gender_Choices)
	Father_Name = models.CharField(max_length = 50, blank = True, null = True)
	Mother_Name = models.CharField(max_length = 50, blank = True, null = True)
	Guardian_Name = models.CharField(max_length = 50, blank = True, null = True, default = '')
	Religion = models.CharField(max_length = 50)
	Nationality = models.CharField(max_length = 50)
	Aadhaar_Number = models.CharField(max_length = 50, default = '')
	#CONTACT DETAILS
	Mobile_Number = models.CharField(max_length = 10, validators = [Phone_Number])
	Email_Id = models.EmailField(max_length = 250)
	Alternate_Mobile_Number = models.CharField(max_length = 10, validators = [Phone_Number], null = True)
	#ADDRESS DETAILS
	Door_Number = models.CharField(max_length = 20, help_text = 'Flat/Door/Block Number')
	Premises = models.CharField(max_length = 100, help_text = 'Name of the Premises/Building/Village')
	Street = models.CharField(max_length = 100, help_text = 'Street/Road/Post Office', blank = True)
	Area = models.CharField(max_length = 50, help_text = 'Area/Locality Details',default = "", blank = True)
	City = models.CharField(max_length = 50, default = "", blank = True)
	State = models.CharField(max_length = 50, default = "")
	Country = models.CharField(max_length = 50, default = '')
	Pin_Code = models.CharField(max_length = 20, default = "")
	Student_Image = models.ImageField(default = "",upload_to = 'Images/')
	Study_Of_Conduct = models.ImageField(default = "",upload_to = 'Images/',validators = [Image_Size],help_text='Size should be less than 300 KB')
	Transfer_Certificate = models.ImageField(default = "",upload_to = 'Images/',validators = [Image_Size],help_text='Size should be less than 300 KB')
	Tenth_Marks_Long_Memo = models.ImageField(default = "",upload_to = 'Images/',validators = [Image_Size],help_text='Size should be less than 300 KB')
	Intermediate_Marks_Short_Memo = models.ImageField(default = "",upload_to = 'Images/',validators = [Image_Size],help_text='Size should be less than 300 KB')
	Student_Signature = models.ImageField(default = "",upload_to = 'Images/',validators = [Image_Size],help_text='Size should be less than 300 KB')
	valid_User_Password = models.CharField(max_length = 20,editable = False,default='')


@receiver(pre_save, sender=Student)
def default_Student(sender, instance, **kwargs):
	if not instance.valid_User_Password:
		instance.valid_User_Password = instance.Roll_Number

class Courses(models.Model):
	#Course Details
	Course_Code = models.CharField(max_length = 10, primary_key = True)
	Course_Subject = models.CharField(max_length = 20, default = '')
	Course_Title = models.CharField(max_length = 100,default = '')

class Department(models.Model):
	#Department Details
	Department_Name = models.CharField(max_length = 30)
	Department_Id = models.CharField(max_length = 10, primary_key = True)

class Teacher(models.Model):
	#Teacher Details
	Teacher_Name = models.CharField(max_length = 50)
	Teacher_Id = models.CharField(max_length = 10, primary_key = True)
	Teacher_Mobile_Number = models.CharField(max_length = 10, validators = [Phone_Number])
	Tecaher_Email_Id = models.EmailField(max_length = 250)
	Teacher_Department_Id = models.ForeignKey(Department, on_delete = models.CASCADE)
	valid_User_Password_Teacher = models.CharField(default = '',max_length = 20,editable = False)

@receiver(pre_save, sender=Teacher)
def default_Teacher(sender, instance, **kwargs):
	if not instance.valid_User_Password_Teacher:
		instance.valid_User_Password_Teacher = instance.Teacher_Id

class Student_Marks(models.Model):
	#Marks Alloted
	Date_Time_Marks = models.DateTimeField(auto_now = True)
	Semester = models.CharField(max_length= 20, choices = Semester_Choices, null = True)
	Marks_Type = models.CharField(max_length = 30, choices = Exam_Type_Choices)
	Course_Code = models.ForeignKey(Courses,on_delete = models.PROTECT, default = '')
	Roll_Number_Marks = models.ForeignKey(Student,on_delete = models.PROTECT, default = '')
	Teacher_Id_Marks = models.ForeignKey(Teacher,on_delete = models.PROTECT, default = '')
	Marks_Total = models.CharField(max_length = 3,default = '')
	Marks_Alloted = models.DecimalField(max_digits = 6, decimal_places = 2,null = True,blank=True)

class Student_Attendance(models.Model):
	#Attendance Given
	Date_Time_Marks = models.DateTimeField(auto_now = True)
	Date_Time_Original = models.DateTimeField(default = '',null=True)
	Semester = models.CharField(max_length= 20, choices = Semester_Choices, null = True)
	Course_Code = models.ForeignKey(Courses,on_delete = models.PROTECT, default = '')
	Roll_Number_Attendance =  models.ForeignKey(Student,on_delete = models.PROTECT ,default = '')
	Teacher_Id_Attendance = models.ForeignKey(Teacher,on_delete = models.PROTECT, default = '')
	Attendance_Date = models.CharField(max_length = 15, choices = Attendance_Choices)

class Teacher_Course(models.Model):
	#Courses and Teacher
	Group = models.ForeignKey(Groups, on_delete = models.PROTECT)
	Teacher_Id = models.ForeignKey(Teacher,on_delete = models.PROTECT)
	Course_Code = models.ForeignKey(Courses,on_delete = models.PROTECT)
	Semester_Teacher = models.CharField(max_length= 20, choices = Semester_Choices)
	Year_Of_Admission = models.IntegerField(default = Year_Admission)