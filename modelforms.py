from django import forms
from student.models import *


class Student_ModelForm(forms.ModelForm):
	class Meta:
		model  = Student
		fields = '__all__'


