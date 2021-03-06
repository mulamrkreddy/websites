from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import blog_post.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/index.html'}),
    (r'about/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/about.html'}),
    (r'video/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/about_video.html'}),
    (r'^blog/$', 'blog_post.views.blog_page'),
    url(r'^blog/(?P<category>\w+)/$', 'blog_post.views.blog_page_cat', name='category'),
    url(r'^post/(?P<slug>\w+)/$', 'blog_post.views.single_blog_post'),
    (r'^photos/$', 'blog_post.views.photo_page'),
    url(r'^photos/(?P<category>\w+)/$', 'blog_post.views.photo_page_cat'),
   (r'^music/$', 'blog_post.views.music_page'),
    url(r'^music/(?P<category_short>\w+)/$', 'blog_post.views.music_page_cat'),
   (r'maps/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/maps.html'}),
   (r'walkshed/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/walkshed.html'}),
   (r'walkshed_mobile/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/walkshed_mobile.html'}),
    #(r'map/', 'django.views.generic.simple.direct_to_template', {'template': '/home/afraint/webapps/blog/myproject/templates/map.html'}),

)
##from django.core.urlresolvers import reverse
##reverse('category')
