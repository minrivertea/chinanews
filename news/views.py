from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.contrib.comments.models import Comment

from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse

import uuid
from datetime import datetime, timedelta

from users.models import *
from news.forms import *
from custom_comments.models import CommentWithVote

#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )


def _get_news(request):

#   1. filter all the news stories from the last week
#   2. sort them by combined score
#   3. return the news
#   The algorithm has to take account of the value of points, comments and then also 'freshness'

    news_list = []
    for n in NewsItem.objects.all():
        time_difference = (datetime.now() - n.date)
        time_score = (int(time_difference.days) + 1)
        n.combined_count = ((n.votes + n.get_comment_count()) / time_score)
        news_list.append(n)

    news = sorted(news_list, reverse=True, key=lambda n: n.combined_count)
    return news[:20]

def index(request):
    news = _get_news(request)
    return render(request, "news/index.html", locals())
 
def news_home(request):
    news = _get_news(request)
    #news = NewsItem.objects.all().order_by('-date')
    # need an algorithm here for choosing the news
    return render(request, "news/news_home.html", locals())   


def news_item(request, hashkey):
    news_item = get_object_or_404(NewsItem, hashkey=hashkey)
    return render(request, "news/news_item.html", locals())

@login_required
def news_ding(request, hashkey):
    item = get_object_or_404(NewsItem, hashkey=hashkey)
    item.votes += 1
    item.voters.add(request.user.get_profile())
    item.save()
    
    if item.owner.karma == "0":
        item.owner.karma = 1
    else:
        item.owner.karma += 1
    
    item.owner.save()
    
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)

def news_ding_ajax(request):
    if request.GET.get('xhr'):
        news_item = get_object_or_404(NewsItem, pk=request.GET.get('id'))
        news_item.votes +=1
        news_item.voters.add(request.user.get_profile())
        news_item.save()
        
        if news_item.owner.karma is None:
            news_item.owner.karma = 1
        else:
            news_item.owner.karma +=1
        
        news_item.owner.save()
        
        return HttpResponse(news_item.votes)
    return

@login_required
def news_blocked(request, hashkey):
    item = get_object_or_404(NewsItem, hashkey=hashkey)
    if item.blocked is None:
        item.blocked = 1
    else:
        item.blocked +=1
    
    item.save()
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url) 

@login_required
def comment_ding(request, id):
    comment = get_object_or_404(CommentWithVote, pk=id)
    person = request.user.get_profile()
    
    # increase the number of points the comment has
    if comment.votes is None:
        comment.votes = 1
    else:
        comment.votes += 1   
    
    # add the person to the list of voters (they can't vote again)
    comment.voters.add(person)
    comment.save()
    
    # finally, increase the karma of the comment writer
    comment_owner = get_object_or_404(Person, user__username=comment.user_name)
    if comment_owner.karma is None:
        comment_owner.karma = 1
    else:
        comment_owner.karma += 1
    comment_owner.save()
    
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)

@login_required
def add_news(request):
    if request.method == 'POST':
        form = AddNewsForm(request.POST)
        if form.is_valid():
            
            # check if there's a news item been posted already with the same URL
            url = form.cleaned_data['url']
            if url in [x.url for x in NewsItem.objects.all()]:
                news_items = NewsItem.objects.filter(url=form.cleaned_data['url'])
                return render(request, "news/already_added.html", locals())
            
            if form.cleaned_data['as_user']:
                owner = form.cleaned_data['as_user']
            else:
                owner = request.user.get_profile()
                
            creation_args = {
                'date': datetime.now(),	
                'owner': owner,
                'title': form.cleaned_data['title'],
                'url': form.cleaned_data['url'],
                'text': form.cleaned_data['text'],
                'hashkey': uuid.uuid1().hex,
            }
            
            new_object = NewsItem.objects.create(**creation_args)
            url = reverse('news_home')
            return HttpResponseRedirect(url)
    
    else:
        form = AddNewsForm()
    
    
    return render(request, "news/forms/add_news_form.html", locals())
    