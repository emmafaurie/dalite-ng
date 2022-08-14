from cookie_consent.models import ACTION_ACCEPTED, LogItem
from cookie_consent.util import (
    dict_to_cookie_str,
    get_cookie_dict_from_request,
    get_cookie_groups,
)
from cookie_consent.views import CookieGroupAcceptView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def admin_index_wrapper(request):
    """
    Redirect to login page outside of an iframe, show help on enabling cookies
    inside an iframe.  We consider the request to come from within an iframe if
    the HTTP Referer header is set.  This isn't entirely accurate, but should
    be good enough.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("admin:index"))
    else:
        # We probably got here from within the Studio, and the user has
        # third-party cookies disabled, so we show help on enabling cookies for
        # this site.
        return render(
            request, "peerinst/cookie_help.html", {"host": request.get_host()}
        )


def set_cookie_dict_to_response(response, dic):
    # https://github.com/jazzband/django-cookie-consent/pull/27
    COOKIE_SECURE = settings.SESSION_COOKIE_SECURE
    try:
        COOKIE_SAMESITE = settings.SESSION_COOKIE_SAMESITE
    except AttributeError:
        COOKIE_SAMESITE = "Lax"

    response.set_cookie(
        settings.COOKIE_CONSENT_NAME,
        dict_to_cookie_str(dic),
        settings.COOKIE_CONSENT_MAX_AGE,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
    )


def accept_cookies(request, response, varname=None):
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in get_cookie_groups(varname):
        cookie_dic[cookie_group.varname] = cookie_group.get_version()
        if settings.COOKIE_CONSENT_LOG_ENABLED:
            LogItem.objects.create(
                action=ACTION_ACCEPTED,
                cookiegroup=cookie_group,
                version=cookie_group.get_version(),
            )
    set_cookie_dict_to_response(response, cookie_dic)


class CookieGroupAcceptViewPatch(CookieGroupAcceptView):
    def process(self, request, response, varname):
        accept_cookies(request, response, varname)
