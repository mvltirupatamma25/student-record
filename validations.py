from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from student.libraries import *

def Phone_Number(value):
	if len(value)!= 10:
		raise ValidationError(
			_('The Mobile Number is invalid'),
			)


def Image_Size(Input):
	ImageSize = Input.file.size
	limit_Kb_Min = 20
	limit_Kb_Max = 300
	if ImageSize > limit_Kb_Max * 1024:
		raise ValidationError(
			_('The maximum image size is 300 kb'))