from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from questions import views


urlpatterns = patterns('',
    url(r'^$', views.questions, name="questions_home"),
    url(r'^add/$', views.add_question, name="add_question"),
    url(r'^answer/([\w+])/$', views.answer_vote, name="answer_vote"),
    url(r'^(?P<questionslug>[\w-]+)/add-answer/$', views.add_answer, name="add_answer"),
    url(r'^(?P<questionslug>[\w-]+)/$', views.question, name="question"),
    

)

