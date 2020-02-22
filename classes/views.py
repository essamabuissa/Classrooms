from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignInForm , SignUpForm , ClassroomForm , StudentForm
from django.contrib.auth import login , authenticate , logout
from .models import Classroom,Student


def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom).order_by('name' , 'exam_grade')
	context = {
		"classroom": classroom,
		"students" : students
	}
	return render(request, 'classroom_detail.html', context)

def student_create(request ,classroom_id):
	classroom = Classroom.objects.get(id =classroom_id )
	if request.user.is_anonymous or classroom.teacher != request.user:
		return redirect('signin')

	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student = form.save(commit = False)
			student.classroom = classroom
			student.save()
			messages.success(request, f"Successfully Added {student.name}!")
			return redirect('classroom-detail' , classroom_id)

	context = {
	"form": form,
	"classroom":classroom
	}
	return render(request, 'create_student.html', context)

def student_update(request , classroom_id , student_id):
	classroom = Classroom.objects.get(id =classroom_id )
	if request.user.is_anonymous or classroom.teacher != request.user:
		return redirect('signin')



	student = Student.objects.get(id = student_id)
	form = StudentForm(instance = student)

	if request.method == "POST":
		form = StudentForm(request.POST,instance = student)
		if form.is_valid():
			student = form.save(commit = False)
			student.classroom = classroom
			student.save()
			messages.success(request, f"Successfully Added {student.name}!")
			return redirect('classroom-detail' , classroom_id)

	context = {
	"form": form,
	"classroom":classroom,
	"student" : student
	}
	return render(request, 'update_student.html', context)



def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')

	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom = form.save(commit = False)
			classroom.teacher = request.user
			classroom.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id =classroom_id )
	if request.user.is_anonymous or classroom.teacher != request.user:
		return redirect('signin')
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)

def student_delete(request ,classroom_id ,student_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if classroom.teacher == request.user:
		Student.objects.get(id=student_id).delete()
		messages.success(request, "Successfully Deleted!")
		return redirect('classroom-detail' , classroom_id)
	else:
		messages.warning(request ,"You dont have the access!")
		return redirect('classroom-detail',classroom_id)

def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id =classroom_id )
	if request.user.is_anonymous or classroom.teacher != request.user:
		return redirect('signin')
	classroom.delete()	
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')

#Sign Up Function:

def signUp(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.set_password(user.password)
			user.save()
			login(request,user)
			messages.success(request, "Successfully Registered!")
			return redirect('classroom-list')

	context = {
	"form" : form,

	}
	return render(request , "signup.html" , context)
#Sign In Function:

def signIn(request):
	form = SignInForm()
	if request.method == "POST":
		form = SignInForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")

			auth_user = authenticate(username = username , password = password)
			if auth_user is not None:
				login(request,auth_user)

				messages.success(request, "Successfully Logged In!")
				return redirect('classroom-list')
			else:
				messages.warning(request , "Wrong Password , Try Again!!")
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'signin.html', context)


def signOut(request):
	logout(request)

	messages.warning(request , "You have logged out!")
	return redirect('signin')
	return render(request , "signout.html" , context)
