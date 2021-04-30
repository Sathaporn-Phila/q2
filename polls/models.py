import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):

    question_text = models.CharField(max_length=200) #เก็บคำถาม
    pub_date = models.DateTimeField('date published') #เก็บวันที่ทำการสร้างคำถาม
    allVote = models.IntegerField(default=0)
    lastVoteTime = models.DateTimeField('LastVoteTime',auto_now_add=True)

    def __str__(self):
        return self.question_text #แสดงคำถาม

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now #ข้อความถูกสร้างตอนปัจจุบันหรือเปล่า

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE) #บอกว่าเป็นตัวเลือกของคำถามข้อไหน
    choice_text = models.CharField(max_length=200) #เก็บชื่อตัวเลือก
    votes = models.IntegerField(default=0) #จำนวนการโหวต
    lastVoteTime = models.DateTimeField('lastVoteTime',auto_now_add=True)

    def __str__(self):
        return self.choice_text #แสดงชื่อตัวเลือก

class Vote(models.Model):
    
    time = models.DateTimeField('pub date',auto_now_add=True)  # attribute  สำหรับเก็บค่าเวลา
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE) # attribute ใช้เเสดงความสัมพันธ์บอกว่า Vote นี้อยู่ใน choice ไหน

    def __str__(self):
        return str(self.time.date())+" "+str(self.time.strftime("%H:%M:%S")) #แสดงผลลัพธ์ในรูปของ ชม.:นาที:วินาที

