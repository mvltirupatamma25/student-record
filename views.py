from django.shortcuts import render,get_object_or_404,HttpResponse
from student.models import *
from student.logic import *
from student.libraries import *
from student.modelforms import *
# Create your views here.

def Selection(request):
	return render(request,'temp/selection.html')

def Login_Faculty(request):
	return render(request,'temp/Facultylogin.html')

def Login_Teacher(request):
	return render(request,'temp/Teacherlogin.html')

def Login_Student(request):
	return render(request,'temp/Studentlogin.html')

def faculty_first(request):
	if request.method == 'POST':
		if request.POST.get('Username') == 'Faculty' and request.POST.get('Password') == 'Siddhartha':
			Groups_list = sorted_set(Student,'Group')
			Class_list = sorted_set(Student,'Class')
			Year_Of_Admission_list = sorted_set(Student,'Year_Of_Admission')
			Student_list = Student.objects.all()
			content = {
					'Class_list':Class_list,
					'Groups_list':Groups_list,
					'Year_Of_Admission_list': Year_Of_Admission_list,
					'Student_list':Student_list
				}
			return render(request, 'temp/course.html',content)
		else:
			return HttpResponse('INVALID')

def faculty_second(request,Year,Group_Given):
	Student_Filter_Year_Of_Admission = Student.objects.filter(Year_Of_Admission = Year, Group = Group_Given).order_by('-Group','Year_Of_Admission')
	content = {
				'Student_Filter' : Student_Filter_Year_Of_Admission
	}
	return render(request, 'temp/class.html',content)

def faculty_third(request,Year,First_Name,Roll_Number):
	Student_Details = Student.objects.filter(Roll_Number = Roll_Number)
	content = {
				'Student_Details':Student_Details
	}
	return render(request,'temp/student.html',content)

def Add_Student(request):
	if request.method == 'POST':
		if Student.objects.filter(Roll_Number = request.POST.get('Roll_Number')).exists():
			try:
				for key, value in request.POST.items():
					#print(key,value)
					if key == "Roll_Number":
						student = get_object_or_404(Student,Roll_Number = value)
						Id_Number = value

				Student_Details = Student.objects.get(Roll_Number = Id_Number)
				form = Student_ModelForm(request.POST or None, request.FILES or None,  instance=Student_Details)
				if form.is_valid():
					edit = form.save(commit = False)
					edit.save()
				Student_Details = Student.objects.filter(Roll_Number = Id_Number)
				content = {
							'Student_Details':Student_Details
				}
				return render(request,'temp/student.html',content)
			except:
				return HttpResponse("Details Incorrect")

		else:
			content = {}
			form = Student_ModelForm(request.POST, request.FILES)
			print(form)
			if form.is_valid():
				form.save()
				content = {
						'form':form
				}
			return render(request,"temp/addstudent.html",content)
	else:
		form = Student_ModelForm()
		content = {
				'form':form
		}
		return render(request,"temp/addstudent.html",content)

def Edit_Student(request,Year,Group,Roll_Number):
	if request.method == 'POST':
		student = get_object_or_404(Roll_Number = Roll_Number)
		content = {}
		form = Student_ModelForm(request.POST, request.FILES, instance=	student)
		if form.is_valid():
			form.save()
		content = {
				'form':form
			}
		return render("temp/editstudent.html",content)
	else:
		student = get_object_or_404(Student, Roll_Number = Roll_Number)
		form = Student_ModelForm(instance  = student)
		details = Student.objects.filter(Roll_Number = Roll_Number)
		content = {
				'form':form,
				'details':details
		}
		return render(request,"temp/editstudent.html",content)

def Delete_Student(request,Year,Group,Roll_Number):
	Student_Details = Student.objects.get(Roll_Number = Roll_Number)
	Student_Details.delete()
	Student_Filter_Year_Of_Admission = Student.objects.filter(Year_Of_Admission = Year, Group = Group).order_by('-Group','Year_Of_Admission')
	content = {
				'Student_Filter' : Student_Filter_Year_Of_Admission
	}
	return render(request, 'temp/class.html',content)

def Certificate_Student(request,Year,Group,Roll_Number):
	Student_Details = Student.objects.filter(Roll_Number = Roll_Number)
	content = {
			'Details': Student_Details
	}
	return render(request,'temp/certificates.html',content)

def Teacher_first(request):
	if request.method == 'POST':
		teacher = Teacher.objects.filter(Teacher_Id = request.POST.get('Username'))
		if teacher.exists() and teacher[0].valid_User_Password_Teacher == request.POST.get('Password'):
			visit = Teacher_Course.objects.filter(Teacher_Id = request.POST.get('Username'))
			content = {
					'visit' : visit
			}
			return render(request,'temp/Teacherfirst.html',content)
		else:
			return HttpResponse('INVALID DETAILS OR NOT A STUDENT')

def Teacher_second(request,Id,Group,Year,Semester,Course):
	Class_Students = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
	content = {
			'Id' : Id,
			'class_student' : Class_Students,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course
	}
	return render(request, 'temp/Teachersecond.html',content)

def Teacher_third(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous = Student_Attendance.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Roll_Number_Attendance__in = Rolls).order_by('Date_Time_Original')
	Previous_Date = Previous.values_list('Date_Time_Original')
	Total_strength = len(Rolls)
	Dates = {}
	for p in Previous:
		Date = p.Date_Time_Original.date()
		Dates[Date] = len(Previous.filter(Date_Time_Original = p.Date_Time_Original).filter(Attendance_Date = 'PRESENT'))
	content = {
			'Id' : Id,
			'T' : Total_strength,
			'Dates' : Dates,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course
	}
	return render(request, 'temp/Teacherthird.html',content)

def Teacher_fourth(request,Id,Year,Group,Semester,Course):
	if request.POST['SUBMIT'] == 'Mark':
		Attendance = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		Roll =Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number').values_list('Roll_Number')
		Rolls = json.dumps(list(Roll))
		content = {
				'Id' : Id,
				'Attendance':Attendance,
				'Roll':Rolls,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
				}
		return render(request,'temp/Teacherfourth.html',content)
	elif request.POST['SUBMIT'] == 'Delete':
		values = list(request.POST.keys())
		for i in range(2,len(values)):
			if request.POST[values[i]] == 'on':
				Date = values[i]
				Month = Find_Month(Date[0:3])
				Values = Student_Attendance.objects.filter(Teacher_Id_Attendance = Id).filter(Course_Code = Course).filter(Semester = Semester).filter(Date_Time_Original__date = datetime.date(int(Date[9:13]),Month,int(Date[5:7])))
		for i in Values:
			i.delete()
		Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
		Previous = Student_Attendance.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Roll_Number_Attendance__in = Rolls)
		Previous_Date = Previous.values_list('Date_Time_Original')
		Total_strength = len(Rolls)
		Dates = {}
		for p in Previous:
			Date = p.Date_Time_Original.date()
			Dates[Date] = len(Previous.filter(Date_Time_Original = p.Date_Time_Original).filter(Attendance_Date = 'PRESENT'))
		content = {
					'Id' : Id,
					'T' : Total_strength,
					'Dates' : Dates,
					'Year' : Year,
					'Group' : Group,
					'Semester' : Semester,
					'Course' : Course
			}
		return render(request, 'temp/Teacherthird.html',content)
	elif request.POST['SUBMIT'] == 'Report':
		studentgraph = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		dataframe = Bargraph(Id,Year,Group,Semester,Course)[0]
		average_present = round(Bargraph(Id,Year,Group,Semester,Course)[1],2)
		average_absent = float(100)-average_present
		cos = Courses.objects.filter(Course_Code = Course)
		dataframe2 = Bargraph(Id,Year,Group,Semester,Course)[3]
		datas = list()
		for i in range(len(studentgraph)):
			if len(dataframe2) != 0:
				datas.append(list(dataframe2.loc[i]))
			else:
				pass
		if len(dataframe2) != 0:
			content = {
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course,
				'student' : studentgraph,
				'dataframe' : datas,
				'labels' : ['Average Present','Average Absent'],
				'data' : [average_present,average_absent],
				'barlabels' : list(dataframe['percent']),
				'bardata' : list(dataframe['index']),
				'class' : Group,
				'Sem' : Semester,
				'course' : Course,
				'Cos' : cos[0],
				'T_W' : Bargraph(Id,Year,Group,Semester,Course)[2],
				'len' : len(studentgraph),
				'p' : round(Bargraph(Id,Year,Group,Semester,Course)[1],2),
				'below' : list(dataframe['index'])[0]
			}
			return render(request, 'temp/TeacherReport.html',content)
		else:
			return HttpResponse("No Attendance to Generate The Report")

def Teacher_fifth(request,Id,Year,Group,Semester,Course,Date):
	Month = Find_Month(Date[0:3])
	Values = Student_Attendance.objects.filter(Teacher_Id_Attendance = Id).filter(Course_Code = Course).filter(Semester = Semester).filter(Date_Time_Original__date = datetime.date(int(Date[9:13]),Month,int(Date[5:7])))
	content = {
			'Date' : Date[5:7],
			'Month' : Date[0:3],
			'Year' : Date[9:13],
			'Date_Total' : Date,
			'Attendance' : Values,
			'Id' : Id,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course
	}
	return render(request, 'temp/Teacherfifth.html',content)

def Teacher_sixth(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous = Student_Attendance.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Roll_Number_Attendance__in = Rolls)
	Previous_Date = set()
	Course_original = Course
	Id_original = Id
	for i in Previous.values_list('Date_Time_Original'):
		Previous_Date.add(str(i[0].date()))
	value = list(request.POST)
	li = value[3:len(value)]
	Attendance = {}
	for i in range(0,len(li)):
		Attendance[li[i]] = request.POST.get(li[i])
	Course = Courses.objects.get(Course_Code = Course)
	Id = Teacher.objects.get(Teacher_Id = Id)
	for key in Attendance:
		Key = Student.objects.get(Roll_Number = key)
		if request.POST.get('Date') not in Previous_Date:
			Instance = Student_Attendance(Date_Time_Original = request.POST.get('Date'),Semester = Semester,
			Course_Code = Course,Roll_Number_Attendance = Key, Teacher_Id_Attendance = Id,
			Attendance_Date = Attendance[key])
			Instance.save()
		else:
			return HttpResponse("The Attendance of the Date exists?Are You Trying To Update The Attendance?")
	Total_strength = len(Rolls)
	Dates = {}
	for p in Previous:
		Date = p.Date_Time_Original.date()
		Dates[Date] = len(Previous.filter(Date_Time_Original = p.Date_Time_Original).filter(Attendance_Date = 'PRESENT'))
	content = {
			'Id' : Id_original,
			'T' : Total_strength,
			'Dates' : Dates,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course_original
	}
	return render(request, 'temp/Teacherthird.html', content)

def Teacher_seventh(request,Id,Year,Group,Semester,Course,Date):
	Month = Find_Month(Date[0:3])
	Values = Student_Attendance.objects.filter(Teacher_Id_Attendance = Id).filter(Course_Code = Course).filter(Semester = Semester).filter(Date_Time_Original__date = datetime.date(int(Date[9:13]),Month,int(Date[5:7])))
	value = list(request.POST)
	li = value[3:len(value)]
	Attendance = {}
	for i in range(0,len(li)):
		Attendance[li[i]] = request.POST.get(li[i])
	for i in range(len(Values)):
		if list(Attendance.keys())[i] == Values[i].Roll_Number_Attendance.Roll_Number and Attendance[list(Attendance.keys())[i]] != Values[i].Attendance_Date:
			instance = Values[i]
			instance.Attendance_Date = Attendance[list(Attendance.keys())[i]]
			instance.save()
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous = Student_Attendance.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Roll_Number_Attendance__in = Rolls)
	Previous_Date = Previous.values_list('Date_Time_Original')
	Total_strength = len(Rolls)
	Dates = {}
	for p in Previous:
		Date = p.Date_Time_Original.date()
		Dates[Date] = len(Previous.filter(Date_Time_Original = p.Date_Time_Original).filter(Attendance_Date = 'PRESENT'))
	content = {
			'Id' : Id,
			'T' : Total_strength,
			'Dates' : Dates,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course
	}
	return render(request, 'temp/Teacherthird.html',content)

def Teacher_eight(request,Id,Year,Group,Semester,Course):
	Student_List = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
	Types = {'I INTERNAL','II INTERNAL','ASSIGNMENT','SEMESTER'}
	content = {
			'Attendance' : Student_List,
			'Types' : Types,
			'Id' : Id,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Course
	}
	return render(request,'temp/Teachereight.html',content)

def Teacher_ninth(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Internal_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'I Internal').filter(Roll_Number_Marks__in = Rolls)
	Total_Strength = len(Internal_1)
	Absent = Internal_1.filter(Marks_Alloted = None)
	Total_Absent = len(Absent)
	Total_Present = Total_Strength - Total_Absent
	Total_Fail = 0
	Total_Pass = 0
	for i in Internal_1:
		if i.Marks_Alloted == None or i.Marks_Alloted < 12:
			Total_Fail += 1
		else:
			Total_Pass += 1
	if len(Internal_1) != 0:
		content = {
				'T_S' : len(Rolls),
				'average': marks_details('I Internal',Internal_1),
				'labels' :['Total Students Passed','Total Students Failed'],
				'data' : [Total_Pass,Total_Fail],
				'Attendance' : Internal_1,
				'Absent' : Total_Absent,
				'Present' : Total_Present,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course,
			}
		return render(request, 'temp/Teacherninehalf.html',content)
	else:
		Internal_2 = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
				'Attendance' : Internal_2,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
		}
		return render(request, 'temp/Teacherninth.html',content)

def Teacher_tenth(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Internal_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'II Internal').filter(Roll_Number_Marks__in = Rolls)
	Total_Strength = len(Internal_2)
	Absent = Internal_2.filter(Marks_Alloted = None)
	Total_Absent = len(Absent)
	Total_Present = Total_Strength - Total_Absent
	Total_Fail = 0
	Total_Pass = 0
	for i in Internal_2:
		if i.Marks_Alloted == None or i.Marks_Alloted < 12:
			Total_Fail += 1
		else:
			Total_Pass += 1
	if len(Internal_2) != 0:
		content = {
				'T_S' : len(Rolls),
				'average': marks_details('II Internal',Internal_2),
				'labels' :['Total Students Passed','Total Students Failed'],
				'data' : [Total_Pass,Total_Fail],
				'Attendance' : Internal_2,
				'Id' : Id,
				'Absent' : Total_Absent,
				'Present' : Total_Present,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
			}
		return render(request, 'temp/Teachertenhalf.html',content)
	else:
		Internal_2 = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
				'Attendance' : Internal_2,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
		}
		return render(request, 'temp/Teachertenth.html',content)

def Teacher_eleven(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Assignment = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'Assignment').filter(Roll_Number_Marks__in = Rolls)
	if len(Assignment) != 0:
		content = {
				'Attendance' : Assignment,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
			}
		return render(request, 'temp/Teacherelevenhalf.html',content)
	else:
		Assignment = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
				'Attendance' : Assignment,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
		}
		return render(request, 'temp/Teachereleven.html',content)

def Teacher_twelve(request,Id,Year,Group,Semester,Course):
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Semesters = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'Semester').filter(Roll_Number_Marks__in = Rolls)
	Total_Strength = len(Semesters)
	Absent = Semesters.filter(Marks_Alloted = None)
	Total_Absent = len(Absent)
	Total_Present = Total_Strength - Total_Absent
	Total_Fail = 0
	Total_Pass = 0
	for i in Semesters:
		if i.Marks_Alloted == None or i.Marks_Alloted < 35:
			Total_Fail += 1
		else:
			Total_Pass += 1
	if len(Semesters) != 0:
		content = {
				'T_S' : len(Rolls),
				'average': marks_details('Semester',Semesters),
				'labels' :['Total Students Passed','Total Students Failed'],
				'data' : [Total_Pass,Total_Fail],
				'Attendance' : Semesters,
				'Absent' : Total_Absent,
				'Present' : Total_Present,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
			}
		return render(request, 'temp/Teachertwelvehalf.html',content)
	else:
		Semesters = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
				'Attendance' : Semesters,
				'Id' : Id,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Course
		}
		return render(request, 'temp/Teachertwelve.html',content)

def Teacher_thirteen(request,Id,Year,Group,Semester,Course):
	Cours = Course
	Ids = Id
	A = request.POST
	B = list(A.keys())[3:len(A)]
	Course = Courses.objects.get(Course_Code = Course)
	Id = Teacher.objects.get(Teacher_Id = Id)
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous_Internal_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls)
	previous_marks_type = set()
	for i in Previous_Internal_1.values_list('Marks_Type'):
		previous_marks_type.add(i[0])
	if request.POST['SUBMIT'] == 'submit' and "I Internal" not in  previous_marks_type:
		for i in B:
			if len(A[i]) != 0:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'I Internal',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'],Marks_Alloted = float(A[i]))
				Instance.save()
			else:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'I Internal',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'])
				Instance.save()
		Previous_Internal_1 = Previous_Internal_1.filter(Marks_Type = 'I Internal')
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'I Internal')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 12:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'T_S' : len(Rolls),
			'average': marks_details('I Internal',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_Internal_1,
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teacherninehalf.html',content)
	elif request.POST['SUBMIT'] == 'updatepage':
		Internal_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'I Internal').filter(Roll_Number_Marks__in = Rolls)
		content = {
				'Attendance' : Internal_1,
				'Id' : Ids,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Cours
			}
		return render(request, 'temp/Teacherninehalfupdate.html',content)
	elif request.POST['SUBMIT'] == 'updatemarks':
		Previous_Internal_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'I Internal')
		for student in Previous_Internal_1:
			for s in B:
				if student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) != 0:
					student.Marks_Alloted = float(A[s])
					student.save()
				elif student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) == 0:
					student.Marks_Alloted = None
					student.save()
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'I Internal')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 12:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'T_S' : len(Rolls),
			'average': marks_details('I Internal',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_1,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teacherninehalf.html',content)
	elif request.POST['SUBMIT'] == 'delete':
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'I Internal')
		for i in Previous_1:
			i.delete()
		previous_marks = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
			'Attendance' : previous_marks,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teacherninth.html',content)

def Teacher_fourteen(request,Id,Year,Group,Semester,Course):
	Cours = Course
	Ids = Id
	A = request.POST
	B = list(A.keys())[3:len(A)]
	Course = Courses.objects.get(Course_Code = Course)
	Id = Teacher.objects.get(Teacher_Id = Id)
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous_Internal_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls)
	previous_marks_type = set()
	for i in Previous_Internal_2.values_list('Marks_Type'):
		previous_marks_type.add(i[0])
	if request.POST['SUBMIT'] == 'submit' and "II Internal" not in  previous_marks_type:
		for i in B:
			if len(A[i]) != 0:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'II Internal',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'],Marks_Alloted = float(A[i]))
				Instance.save()
			else:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'II Internal',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'])
				Instance.save()
		Previous_Internal_1 = Previous_Internal_2.filter(Marks_Type = 'II Internal')
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'II Internal')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 12:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'T_S' : len(Rolls),
			'average': marks_details('II Internal',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_Internal_1,
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertenhalf.html',content)
	elif request.POST['SUBMIT'] == 'updatepage':
		Internal_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'II Internal').filter(Roll_Number_Marks__in = Rolls)
		content = {
				'Attendance' : Internal_2,
				'Id' : Ids,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Cours
			}
		return render(request, 'temp/Teachertenhalfupdate.html',content)
	elif request.POST['SUBMIT'] == 'updatemarks':
		Previous_Internal_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'II Internal')
		for student in Previous_Internal_2:
			for s in B:
				if student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) != 0:
					student.Marks_Alloted = float(A[s])
					student.save()
				elif student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) == 0:
					student.Marks_Alloted = None
					student.save()
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'II Internal')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 12:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'T_S' : len(Rolls),
			'average': marks_details('II Internal',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_1,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertenhalf.html',content)
	elif request.POST['SUBMIT'] == 'delete':
		Previous_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = "II Internal")
		for i in Previous_2:
			i.delete()
		previous_marks = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
			'Attendance' : previous_marks,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertenth.html',content)

def Teacher_fifteen(request,Id,Year,Group,Semester,Course):
	Cours = Course
	Ids = Id
	A = request.POST
	B = list(A.keys())[3:len(A)]
	Course = Courses.objects.get(Course_Code = Course)
	Id = Teacher.objects.get(Teacher_Id = Id)
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous_Assignment = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls)
	previous_marks_type = set()
	for i in Previous_Assignment.values_list('Marks_Type'):
		previous_marks_type.add(i[0])
	if request.POST['SUBMIT'] == 'submit' and "Assignment" not in  previous_marks_type:
		for i in B:
			Instance = Student_Marks(Semester = Semester,Marks_Type = 'Assignment',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'],Marks_Alloted = float(A[i]))
			Instance.save()
		Previous_Assignment = Previous_Assignment.filter(Marks_Type = 'Assignment')
		content = {
			'Attendance' : Previous_Assignment,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teacherelevenhalf.html',content)
	elif request.POST['SUBMIT'] == 'updatepage':
		Assignment = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'Assignment').filter(Roll_Number_Marks__in = Rolls)
		content = {
				'Attendance' : Assignment,
				'Id' : Ids,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Cours
			}
		return render(request, 'temp/Teacherelevenhalfupdate.html',content)
	elif request.POST['SUBMIT'] == 'updatemarks':
		Previous_Assignment = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Assignment')
		for student in Previous_Assignment:
			for s in B:
				if student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s]:
					student.Marks_Alloted = float(A[s])
					student.save()
		Previous_Assignment_2 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Assignment')
		content = {
			'Attendance' : Previous_Assignment_2,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teacherelevenhalf.html',content)
	elif request.POST['SUBMIT'] == 'delete':
		Previous_Assignment = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Assignment')
		for i in Previous_Assignment:
			i.delete()
		previous_marks = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
			'Attendance' : previous_marks,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachereleven.html',content)

def Teacher_sixteen(request,Id,Year,Group,Semester,Course):
	Cours = Course
	Ids = Id
	A = request.POST
	B = list(A.keys())[3:len(A)]
	Course = Courses.objects.get(Course_Code = Course)
	Id = Teacher.objects.get(Teacher_Id = Id)
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous_Semester = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls)
	previous_marks_type = set()
	for i in Previous_Semester.values_list('Marks_Type'):
		previous_marks_type.add(i[0])
	print(previous_marks_type)
	if request.POST['SUBMIT'] == 'submit' and "Semester" not in  previous_marks_type:
		print('hello')
		for i in B:
			if len(A[i]) != 0:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'Semester',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'],Marks_Alloted = float(A[i]))
				Instance.save()
			else:
				Instance = Student_Marks(Semester = Semester,Marks_Type = 'Semester',Course_Code = Course,Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Id,Marks_Total = A['Total Marks'])
				Instance.save()
		Previous_Internal_1 = Previous_Semester.filter(Marks_Type = 'Semester')
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Semester')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 35:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'T_S' : len(Rolls),
			'average': marks_details('Semester',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_Internal_1,
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertwelvehalf.html',content)
	elif request.POST['SUBMIT'] == 'updatepage':
		Semesters = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Marks_Type = 'Semester').filter(Roll_Number_Marks__in = Rolls)
		content = {
				'Attendance' : Semesters,
				'Id' : Ids,
				'Year' : Year,
				'Group' : Group,
				'Semester' : Semester,
				'Course' : Cours
			}
		return render(request, 'temp/Teachertwelvehalfupdate.html',content)
	elif request.POST['SUBMIT'] == 'updatemarks':
		Previous_Semester = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Semester')
		for student in Previous_Semester:
			for s in B:
				if student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) != 0:
					student.Marks_Alloted = float(A[s])
					student.save()
				elif student.Roll_Number_Marks.Roll_Number == s and str(student.Marks_Alloted) != A[s] and len(A[s]) == 0:
					student.Marks_Alloted = None
					student.save()
		Previous_1 = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Semester')
		Total_Strength = len(Previous_1)
		Absent = Previous_1.filter(Marks_Alloted = None)
		Total_Absent = len(Absent)
		Total_Present = Total_Strength - Total_Absent
		Total_Fail = 0
		Total_Pass = 0
		for i in Previous_1:
			if i.Marks_Alloted == None or i.Marks_Alloted < 35:
				Total_Fail += 1
			else:
				Total_Pass += 1
		content = {
			'Absent' : Total_Absent,
			'Present': Total_Present,
			'T_S' : len(Rolls),
			'average': marks_details('Semester',Previous_1),
			'labels' :['Total Students Passed','Total Students Failed'],
			'data' : [Total_Pass,Total_Fail],
			'Attendance' : Previous_1,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertwelvehalf.html',content)
	elif request.POST['SUBMIT'] == 'delete':
		Previous_Semester = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Semester')
		for i in Previous_Semester:
			i.delete()
		previous_marks = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
		content = {
			'Attendance' : previous_marks,
			'Id' : Ids,
			'Year' : Year,
			'Group' : Group,
			'Semester' : Semester,
			'Course' : Cours
		}
		return render(request,'temp/Teachertwelve.html',content)
	elif request.POST['SUBMIT'] == 'Report':
		Previous_Marks = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls)
		Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).order_by('Roll_Number')
		result = Total_Marks(Previous_Marks,Rolls)
		content = {
			'result' : result,
			'Attendance' : Previous_Marks,
			'rolls' : Rolls
		}
		return render(request,'temp/TeacherReport2.html',content)

def Teacher_seventeen(request,Id,Year,Semester,Course,Group):
	A = request.POST
	B = list(A.keys())[2:len(A)]
	Rolls = Student.objects.filter(Year_Of_Admission = Year).filter(Group = Group).values_list('Roll_Number')
	Previous_Attendance = Student_Marks.objects.filter(Semester = Semester).filter(Course_Code = Course).filter(Teacher_Id_Marks = Id).filter(Roll_Number_Marks__in = Rolls).filter(Marks_Type = 'Attendance')
	if len(Previous_Attendance) == 0:
		for i in B:
			instance = Student_Marks(Semester = Semester,Marks_Type = 'Attendance',Course_Code = Courses.objects.get(Course_Code = Course),Roll_Number_Marks = Student.objects.get(Roll_Number= i),Teacher_Id_Marks = Teacher.objects.get(Teacher_Id = Id),Marks_Total = 5,Marks_Alloted = float(A[i]))
			instance.save()
	else:
		for student in Previous_Attendance:
			for j in B:
				if student.Roll_Number_Marks.Roll_Number == j and student.Marks_Alloted != float(A[j]):
					student.Marks_Alloted = float(A[j])
					student.save()
	studentgraph = Student.objects.filter(Group = Group).filter(Year_Of_Admission = Year).order_by('Roll_Number')
	dataframe = Bargraph(Id,Year,Group,Semester,Course)[0]
	average_present = round(Bargraph(Id,Year,Group,Semester,Course)[1],2)
	average_absent = float(100)-average_present
	cos = Courses.objects.filter(Course_Code = Course)
	dataframe2 = Bargraph(Id,Year,Group,Semester,Course)[3]
	datas = list()
	for i in range(len(studentgraph)):
		datas.append(list(dataframe2.loc[i]))
	content = {
		'Id' : Id,
		'Year' : Year,
		'Group' : Group,
		'Semester' : Semester,
		'Course' : Course,
		'student' : studentgraph,
		'dataframe' : datas,
		'labels' : ['Average Present','Average Absent'],
		'data' : [average_present,average_absent],
		'barlabels' : list(dataframe['percent']),
		'bardata' : list(dataframe['index']),
		'class' : Group,
		'Sem' : Semester,
		'course' : Course,
		'Cos' : cos[0],
		'T_W' : Bargraph(Id,Year,Group,Semester,Course)[2],
		'len' : len(studentgraph),
		'p' : round(Bargraph(Id,Year,Group,Semester,Course)[1],2),
		'below' : list(dataframe['index'])[0]
	}
	return render(request, 'temp/TeacherReport.html',content)

def Student_first(request):
	if request.method == 'POST':
		student = Student.objects.filter(Roll_Number = request.POST.get('Username'))
		if student.exists() and student[0].valid_User_Password == request.POST.get('Password'):
			content = {
					'student' : student
			}
			return render(request,'temp/Studentdetails.html',content)
		else:
			return HttpResponse('INVALID DETAILS OR NOT A STUDENT')
#STUDENT ATTENDANCE
def Student_second(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "1")
	if len(Courses_Involved) != 0:
		content = {
		#'Attendance' : courses_attendance,
		'Semester' : 'Semester 1',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		'sem' : "1"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 1',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)
#STUDENT MARKS
def Student_third(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "2")
	if len(Courses_Involved) != 0:
		content = {
		'Semester' : 'Semester 2',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		'sem' : "2"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 2',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)
def Student_fourth(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "3")
	if len(Courses_Involved) != 0:
		content = {
		'Semester' : 'Semester 3',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		"sem" : "3"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 3',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)
def Student_fifth(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "4")
	if len(Courses_Involved) != 0:
		content = {
		'Semester' : 'Semester 4',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		"sem" : "4"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 4',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)
def Student_sixth(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "5")
	if len(Courses_Involved) != 0:
		content = {
		'Semester' : 'Semester 5',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		"sem" : "5"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 5',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)
def Student_seventh(request,Roll_Number,Group):
	Courses_Involved = Teacher_Course.objects.filter(Group = Group).filter(Semester_Teacher = "6")
	if len(Courses_Involved) != 0:
		content = {
		'Semester' : 'Semester 6',
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group,
		"sem" : "6"
		}
		return render(request,'temp/Studentsecond.html',content)
	else:
		content = {
		'Semester' : 'Semester 6',
		"no": "NO ATTENDANCE POSTED YET",
		'Roll_Number': Roll_Number,
		'Attendance' : Courses_Involved,
		'Group' : Group
		}
		return render(request,'temp/Studentthird.html',content)

def Student_eighth(request,Roll_Number,Group,Id,Course,Semester):
	Student_attendance = Student_Attendance.objects.filter(Roll_Number_Attendance = Roll_Number,
		Teacher_Id_Attendance = Id).filter(Course_Code = Course).filter(Semester = Semester).order_by('Date_Time_Original')
	Total_working = len(Student_attendance)
	Total_Present = len(Student_Attendance.objects.filter(Roll_Number_Attendance = Roll_Number,
		Teacher_Id_Attendance = Id).filter(Course_Code = Course).filter(Semester = Semester).filter(Attendance_Date = 'PRESENT'))
	Total_Absent = Total_working - Total_Present
	if Total_working != 0:
		content = {
				'Attendance' : Student_attendance,
				'T_W' : Total_working,
				'T_P' : Total_Present,
				'T_A' : Total_Absent
		}
		return render(request,'temp/Studentfourth.html',content)
	else:
		return HttpResponse('No Attendane posted yet')

def Student_ninth(request,Roll_Number,Group):
	Semesters = ('SEMESTER  I','SEMESTER II','SEMESTER III','SEMESTER IV','SEMESTER V','SEMESTER VI')
	Marks = ('I INTERNAL','II INTERNAL','SEMESTER','ASSIGNMENT','ATTENDANCE')
	Internal_1_marks = Student_Marks.objects.filter(Roll_Number_Marks = Roll_Number).filter(Marks_Type = 'I Internal').filter(Semester = "1")
	content ={
			'Student' : Internal_1_marks,
			'Roll_Number' : Roll_Number,
			'Group' : Group,
			'Attendance' : Semesters,
			'Marks' : Marks
	}
	return render(request,'temp/Studentfifth.html',content)

def Student_tenth(request,Roll_Number,Group,Semester,Exam):
	Semesters = ('SEMESTER  I','SEMESTER II','SEMESTER III','SEMESTER IV','SEMESTER V','SEMESTER VI')
	Semester_Rank = {'SEMESTER  I' : '1','SEMESTER II' : '2','SEMESTER III' : '3',
	'SEMESTER IV' : '4','SEMESTER V' : '5','SEMESTER VI' : '6'}
	Marks = ('I INTERNAL','II INTERNAL','SEMESTER','ASSIGNMENT','ATTENDANCE')
	Marks_Rank = {'I INTERNAL' : 'I Internal','II INTERNAL':'II Internal','SEMESTER':'Semester','ASSIGNMENT':'Assignment','ATTENDANCE':'Attendance'}
	Internal_1_marks = Student_Marks.objects.filter(Roll_Number_Marks = Roll_Number).filter(Marks_Type = Marks_Rank[Exam]).filter(Semester = Semester_Rank[Semester])
	if len(Internal_1_marks) != 0:
		content ={
			'Student' : Internal_1_marks,
			'Roll_Number' : Roll_Number,
			'Group' : Group,
			'Attendance' : Semesters,
			'Marks' : Marks,
			'sem' : Semester
		}
		return render(request,'temp/Studentfifth.html',content)
	else:
		Text = 'No Marks Posted Yet'
		content ={
			'Student' : Internal_1_marks,
			'Roll_Number' : Roll_Number,
			'Group' : Group,
			'Attendance' : Semesters,
			'Marks' : Marks,
			'sem' : Semester,
			'text' : Text
		}
		return render(request,'temp/Studentsixth.html',content)