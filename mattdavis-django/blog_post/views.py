from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import datetime
# imports for gmapi functions
from django import forms

#

from blog_post.models import Post, Photo, Category, Music, Concert, Disc, MusicEmbed
from blog_post.models import get_categories, get_music_categories


###########################
# simple flat pages
###########################

def contact(request):
    """       """
    return render_to_response("contact.html", dict(user=request.user), context_instance=RequestContext(request))

def about(request):
    """       """
    return render_to_response("about.html", dict(user=request.user), context_instance=RequestContext(request))

def aerialphoto(request):
    """       """
    return render_to_response("aerialphoto.html", dict(user=request.user), context_instance=RequestContext(request))


###########################
# discography page
###########################
def disc_page(request):
    """main listing of all discs in the discograpy"""
    posts = Disc.objects.all().order_by("-year")

    filters = []
    paginator = Paginator(posts, 4)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage): posts = paginator.page(paginator.num_pages)
	
    return render_to_response("disc2.html", dict(posts=posts, user=request.user), context_instance=RequestContext(request))

###########################
# concert pages
###########################

def concert_page(request):
    today = datetime.datetime.now()
    TODAY = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
    posts = Concert.objects.all().filter(date__gte=TODAY).order_by("-date")
    filters = []
    paginator = Paginator(posts, 4)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage): posts = paginator.page(paginator.num_pages)

    return render_to_response("concerts.html", dict(posts=posts, user=request.user), context_instance=RequestContext(request))

def past_concert_page(request):
    today = datetime.datetime.now()
    TODAY = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
    posts = Concert.objects.all().filter(date__lte=TODAY).order_by("-date")
    filters = []
    paginator = Paginator(posts, 4)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage): posts = paginator.page(paginator.num_pages)

    return render_to_response("past_concerts.html", dict(posts=posts, user=request.user), context_instance=RequestContext(request))

###########################
# blog pages
###########################

def blog_page(request):
    """main listing of all blog posts"""
    cats = get_categories('post')
    posts = Post.objects.all().order_by("-created")
    filters = []
    for post in posts:
        post.photos = Photo.objects.filter(post=post.pk)

    paginator = Paginator(posts, 4)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage): posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, cats=cats, user=request.user), context_instance=RequestContext(request))

def blog_page_cat(request, category):
    """listing of blog posts that fit the given category"""
    posts = Post.objects.filter(category__name__exact=category).order_by("-created")
    for post in posts:
        cat = str(Category.objects.filter(name=category))
        post.cat = cat.split(":")[1].strip(">]").strip(' ')
        post.photos = Photo.objects.filter(post=post.pk)

    paginator = Paginator(posts, 5)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage): posts = paginator.page(paginator.num_pages)

    return render_to_response("list_cat.html", dict(posts=posts, cat=category, user=request.user), context_instance=RequestContext(request))

def single_blog_post(request, slug):
    """ page that contains a single blog post, with its permanent URL, the slug
    i.e. ...com/posts/post_slug_text    """
    post = Post.objects.get(slug=slug)
    post.photos = Photo.objects.filter(post=post.pk)

    return render_to_response("single_post.html", dict(post=post, slug=slug), context_instance=RequestContext(request))

###########################
# photo pages
###########################

def photo_page(request):
    """listing that shows all photos"""
    cats = get_categories('photo')
    photos = Photo.objects.all().order_by("-date")

    paginator = Paginator(photos,9)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try: photos = paginator.page(page)
    except (InvalidPage, EmptyPage): photos = paginator.page(paginator.num_pages)

    return render_to_response("photo_list.html", dict(photos=photos, cats=cats, user=request.user), context_instance=RequestContext(request))

def photo_page_cat(request, category):
    """listing that shows all photos that fit a given category"""
    photos = Photo.objects.filter(category__name__exact=category).order_by("-date")
    for photo in photos:
        cat = str(Category.objects.filter(name=category))
        photo.cat = cat.split(":")[1].strip(">]").strip(' ')

    paginator = Paginator(photos, 4)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1
    try:
        photos = paginator.page(page)
    except (InvalidPage, EmptyPage):
        photos = paginator.page(paginator.num_pages)

    return render_to_response("photo_cat.html", dict(photos=photos, cat=category, user=request.user), context_instance=RequestContext(request))

###########################
# music page
###########################

def music_page_cat(request, category):
    """listing of blog posts that fit the given category"""
    bands = MusicEmbed.objects.filter(category__name__exact=category)
    return render_to_response("music_cat.html", dict(bands=bands, cat=category), context_instance=RequestContext(request))


def music_page(request):
    """listing of all music embeds"""
    cats = get_music_categories()
    bands = MusicEmbed.objects.all().order_by("-date")
    return render_to_response("music.html", dict(bands=bands, cats=cats), context_instance=RequestContext(request))