"""BlueJam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from JamAPI import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^article/(?P<identifier>.+)/file/(?P<file_id>\d+)/$', views.serve_article_file,
        name='article_file_download'),
    url(r'^clone/journals/$', views.clone_journals, name='clone_journals'),
    url(r'^clone/licences/$', views.clone_licences, name='clone_licences'),
    url(r'^clone/jams/$', views.clone_jams, name='clone_jams'),
    url(r'^clone/files/$', views.clone_files, name='clone_files'),
]
