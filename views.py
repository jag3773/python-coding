from django.shortcuts import render
from coding.models import *


def root(request):
  message = False
  tests = CodingTest.objects.all().order_by('name')
  return render(request, 'home.html', {'message': message, 'tests': tests})

