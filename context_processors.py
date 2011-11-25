from django.conf import settings


def common(request):
    from chinanews import settings
    context = {}
    context['sitename'] = settings.SITE_NAME
    context['siteurl'] = settings.SITE_URL
    context['ga_is_on'] = settings.GA_IS_ON
    
    return context