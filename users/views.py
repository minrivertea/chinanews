# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse 

import random
import string
import uuid 

from datetime import datetime

from news.views import render
from users.models import Person
from users.forms import InviteUserForm, EditBioForm
from registration.models import RegistrationProfile
from registration.backends import get_backend
from registration.forms import RegistrationForm



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))



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


@login_required
def edit_bio(request):
    person = request.user.get_profile()
    if request.method == 'POST':
        form = EditBioForm(request.POST)
        if form.is_valid():
            person.bio = form.cleaned_data['bio']
            person.save()
            
            url = reverse('user_profile')
            return HttpResponseRedirect(url)

    else:
        form = EditBioForm(initial={'bio':person.bio})
    
    
    return render(request, 'users/forms/edit_bio.html', locals())

@login_required
def invite_user(request):
    if request.method == 'POST':
        form = InviteUserForm(request.POST)
        if form.is_valid():
            # create a registration profile with the email address
            
            # create a user/person with a dummy account
            username = id_generator()
            password = uuid.uuid1().hex
            email = form.cleaned_data['email']
            
            new_user = User.objects.create_user(username, email, password)
            
            # give them a registration profile too, just so that we can track their signup
            reg_profile = RegistrationProfile.objects.create_profile(new_user) 
            
            # send an invitation email
            message = render_to_string('registration/invitation_email.txt', {
                'activation_key': reg_profile.activation_key, 
                'inviter': request.user.get_profile(),  	
            })
            
            subject_line = "%s has invited you to %s" % (request.user.get_profile(), settings.SITE_NAME)
            receiver = email
            sender = settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject_line,
                message,
                sender,
                [receiver],
                fail_silently=False,
            )
                        
            
            return render(request, 'users/forms/invite_user.html', locals())
    else:
        form = InviteUserForm()
    
    return render(request, 'users/forms/invite_user.html', locals())


def activate_invited_user(request, key):
    account = get_object_or_404(RegistrationProfile, activation_key=key)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # first, update the user with real data, not the dummy data
            account.user.username = form.cleaned_data['username']
            account.user.password = form.cleaned_data['password1']
            account.user.is_active = True
            account.user.save()
            
            
            
            # finally, create a user profile based on the user
            person = Person.objects.create(
                user=account.user,
                email=account.user.email,
                date_joined=datetime.now(),
                karma=0,
            )
            
            # now we'll log the user in
            from django.contrib.auth import load_backend, login
            for backend in settings.AUTHENTICATION_BACKENDS:
                if person.user == load_backend(backend).get_user(person.user.pk):
                    person.user.backend = backend
            if hasattr(person.user, 'backend'):
                login(request, person.user)
            
            # and finally, we'll activate the registration profile
            activate = RegistrationProfile.objects.activate_user(key)
            
            url = reverse('profile', args=[account.user.username])
            return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    return render(request, 'users/activate_invited_user.html', locals())     
       