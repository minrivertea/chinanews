# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from news.views import render
from users.models import Person


def profile(request, slug):
    person = get_object_or_404(Person, user__username=slug)
    return render(request, "users/profile.html", locals())

@login_required
def user_profile(request):
    person = request.user.get_profile()
    return render(request, "users/profile.html", locals())
    
    
def all_posts(request, slug):
    person = get_object_or_404(Person, user__username=slug)
    from news.models import NewsItem
    posts = NewsItem.objects.filter(owner=person).order_by('-date')
    return render(request, "users/all_posts.html", locals())