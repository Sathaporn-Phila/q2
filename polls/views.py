from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Question
# Create your views here.
def display(request):
    return render(request,"polls/index.html")