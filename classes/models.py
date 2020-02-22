from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	teacher = models.ForeignKey(User,on_delete = models.CASCADE)
	subject = models.CharField(max_length=120)
	grade = models.IntegerField()
	year = models.IntegerField()

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})

	def __str__(self):
		return self.subject


class Student(models.Model):
	GENDER_CHOICES = (
	('M','Male'),
	('F','Female'),
	)

	name  = models.CharField(max_length = 120)
	dob  = models.DateField()
	gender = models.CharField(max_length = 50, choices = GENDER_CHOICES)
	exam_grade = models.DecimalField(max_digits = 5 ,decimal_places = 2)
	classroom = models.ForeignKey(Classroom ,on_delete = models.CASCADE)


	def __str__(self):
		return self.name
