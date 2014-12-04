from django.conf.urls import url, include, patterns
from apps.web.views import AboutView, JobsView, Agreement


urlpatterns = patterns(
    'apps.web.views',

    url(r'^$', 'main.index', name='web_index'),

    url(r'^selection/$', 'main.selection', name='web_selection'),
    url(r'^popular/$', 'main.popular', name='web_popular'),
    url(r'^search/$', 'main.search', name='web_search'),
)


from apps.web.views.account import RegisterWizard
from apps.web.forms.account import UserSignUpForm

RegisterForms = [
    ('register', UserSignUpForm),
    ('register-bio', UserSignUpForm),
]

#account
urlpatterns += patterns(
    'apps.web.views.account',
    url(r'^login/$', 'login', name='web_login'),
    # url(r'^register/$', 'register', name='web_register'),
    url(r'^logout', 'logout', name='web_logout'),
    url(r'register/$', RegisterWizard.as_view(RegisterForms), name='web_register'),
)

# static page
urlpatterns += patterns(
    'apps.web.views.main',

    url(r'^about/$', AboutView.as_view(), name='web_about'),
    url(r'^jobs/$', JobsView.as_view(), name='web_jobs'),
    url(r'^agreement$', Agreement.as_view(), name='web_agreement'),
)


# entity
urlpatterns += patterns(
    'apps.web.views',
    url(r'^entity/', include('apps.web.urls.entity')),
    url(r'^category/', include('apps.web.urls.category')),
    url(r'^account/', include('apps.web.urls.account')),
    url(r'^user/', include('apps.web.urls.user')),
)

__author__ = 'edison7500'
