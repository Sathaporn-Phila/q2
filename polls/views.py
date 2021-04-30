from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import datetime
from .models import Choice, Question, Vote

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context = {'latest_question_list': Question.objects.all()}
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future)."""
        return Question.objects.all().order_by("-allVote") #แสดงคำถาม

def display(request):
    context = {'latest_question_list': sortQuestion(request)}
    return render(request,"polls/index.html",context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()) #แสดงคำถามและตัวเลือกของคำถาม


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all().order_by("-votes")
    print(choices)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        question.allVote += 1
        voteTime = Vote(choice=selected_choice) # บันทึกเวลาที่ทำการ Vote ล่าสุด
        voteTime.save()# เก็บข้อมูล vote ลงฐานข้อมูล
        question.lastVoteTime = voteTime.time
        selected_choice.lastVoteTime = voteTime.time
        selected_choice.save() # บันทึกข้อมูล choice ลงฐานข้อมูล
        context = {'question':question,"choices":choices}
        question.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request,"polls/result.html",context)

def sortResult(request , question_id):
    question = get_object_or_404(Question, pk=question_id) # get a question
    sort = request.POST.get('sortResult') # get type sort
    if sort == "maxToMinV": #max vote to min vote
        choices = question.choice_set.all().order_by("-votes")
    elif sort == "minToMaxV": #min vote to max vote
        choices = question.choice_set.all().order_by("votes")
    elif sort == "lastToOldT": #last time vote to oldest vote
        choices = question.choice_set.all().order_by("-lastVoteTime")
    elif sort == "OldTolastT": #oldest vote to last time vote
        choices = question.choice_set.all().order_by("lastVoteTime")
    else: #order by time that publish poll
        choices = question.choice_set.all()
        
    context = {'question':question,"choices":choices}
    return render(request,"polls/result.html",context)

def sortQuestion(request):
    question = Question.objects.all() # get a question
    sort = request.POST.get('sort') # get a type sort
    if sort == "maxToMinV": #max vote to min vote
        return question.order_by("-allVote")
    elif sort == "minToMaxV": #min vote to max vote
        return question.order_by("allVote")
    elif sort == "lastToOldT": #last time vote to oldest vote
        return question.order_by("-lastVoteTime")
    elif sort == "oldToLastT": #oldest vote to last time vote 
        return question.order_by("lastVoteTime")
    else: #order by time that publish poll
        return question
