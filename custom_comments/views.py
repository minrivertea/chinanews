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

from custom_comments.models import CommentWithVote
from news.views import render

@login_required
def comment_reply(request, hashkey, id):
    comment = get_object_or_404(CommentWithVote, pk=id)
    next = reverse('news_item', args=[hashkey])
    return render(request, "custom_comments/reply.html", locals())