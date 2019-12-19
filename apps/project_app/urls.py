from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.welcome),
    # GET
    url(r'^registrationprocess$', views.registrationprocess),
    # POST
    url(r'^loginprocess$', views.loginprocess),
    # POST
    url(r'^logout$', views.logout),
    # POST
    url(r'^dashboard$', views.dashboard), 
    # GET
    url(r'^party/new$', views.newparty), 
    # GET
    url(r'^makepartyprocess$', views.makeparty_process), 
    # POST
    url(r'^party/(?P<id>\d+)$', views.partyinfo), 
    # GET
    url(r'^party/(?P<id>\d+)/editinfo$', views.editinfo),
    # GET
    url(r'^party/(?P<id>\d+)/editprocess$', views.partyedit_process),
    # POST
    url(r'^party/(?P<id>\d+)/removeprocess$', views.removeparty_process),
    # POST
    url(r'^party/(?P<id>\d+)/joinprocess$', views.joinparty_process), 
    # POST
    url(r'^party/(?P<id>\d+)/cancelprocess$', views.cancelparty_process),
    # POST
    url(r'^party/(?P<id>\d+)/writemessage$', views.writemessage),
    # GET
    url(r'^party/(?P<id>\d+)/addmessageprocess$', views.addmessage_process),
    # # POST
    url(r'^party/(?P<id>\d+)/addcommentprocess$', views.addcomment_process),
    # POST
    url(r'^party/(?P<id>\d+)/getdirections$', views.getdirections),
    # GET
    url(r'^party/(?P<id>\d+)/directionsprocess$', views.directions_process),
    # POST
    url(r'^party/(?P<id>\d+)/directions$', views.directions),
    # GET
]