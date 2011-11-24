# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404

from news.views import render
from users.models import Person


def profile(request, slug):
    person = get_object_or_404(Person, user__username=slug)
    return render(request, "users/profile.html", locals())