from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from PIL import Image as PImage
import os

from myproject.settings import MEDIA_ROOT

from PIL.ExifTags import TAGS, GPSTAGS


###################################
# category model
###################################
class Category(models.Model):
    name = models.CharField(max_length=60)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "categories"


###################################
# blog post model
###################################
class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField(Category)

    def photos(self):
        photos_in_post = []
        photos = Photo.objects.all()
        for photo in photos:
            if photo.post == self.title:
                photos_in_post.append(photo)
        return photos_in_post

    def formatted_body(self):
        """formats text to include tab at beginning of paragraphs"""
        formatted_text = []
        tab = ("<br/>" * 2) + ("&nbsp;" * 5)
        text = self.body
        text_list = text.split("<br/>")
        first_par = ("&nbsp;" * 5) + text_list[0]
        formatted_text.append(first_par)
        for par in text_list[1:]:
            formatted_par = tab + par
            formatted_text.append(formatted_par)
        new_text = "".join(formatted_text)
        return new_text

    def summary(self):
        """formats first two paragraphs to include tabs"""
        formatted_text = []
        tab = ("<br/>" * 2) + ("&nbsp;" * 5)
        text = self.body
        text_list = text.split("<br/>")
        first_par = ("&nbsp;" * 5) + text_list[0]
        formatted_text.append(first_par)
        if len(text_list) > 1:
            second_par = tab + text_list[1]
            formatted_text.append(second_par)
        new_text = "".join(formatted_text)
        return new_text

    def long_or_short(self):
        """0 = short, 1 = long"""
        if len(self.summary()) >= len(self.body):
            # if there is no text overflow
            # but there is more than one photo
            if len(Photo.objects.filter(post=self.pk)) > 1:
                value = 1
            # 1 photo, short body
            else:
                value = 0
        elif len(self.summary()) < len(self.body):
            # if the body is longer than the summary
            value = 1
        return value

    def __unicode__(self):
        return self.title

###################################
# PHOTO model
###################################
ORIENTATION_CHOICES = (
    (0, "Landscape"),
    (1, "Portrait"),
)
COVER_CHOICES = (
    (1, 'cover photo'),
    (2, 'post body')
)
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%y/%m')
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=100)
    date = models.DateField()
    orientation = models.IntegerField(default=0, choices=ORIENTATION_CHOICES)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    cover = models.IntegerField(default=2, choices=COVER_CHOICES)

    def __unicode__(self):
        return self.name

    def lat(self):
        image = PImage.open(self.image)
        self.lat, self.lon = get_lat_lon(get_exif(image))
        return self.lat

    def lon(self):
        image = PImage.open(self.image)
        self.lat, self.lon = get_lat_lon(get_exif(image))
        return self.lon

    def tbnl(self):
        image = PImage.open(self.image)
        bounding_box = (10, 10, 60, 60)
        self.cropped = image.crop(bounding_box)
        return self.cropped


###################################
# music page model
###################################
class Music(models.Model):
    band = models.CharField(max_length=200)
    description = models.TextField()
    iframe = models.TextField()
    website = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    def __unicode__(self):
        return self.band
    class Meta:
        verbose_name_plural = "music"
###################################
# filtering functions
###################################
def get_categories(cat_type):
    """creates list of all categories for a given input type;
    valid options: 'music', 'post', or 'photo' """
    cat_list = []
    for cat in Category.objects.all():
        if cat_type == 'music':
            if cat.music_set.all():
                cat_list.append(str(cat.name))
        elif cat_type == 'post':
            if cat.post_set.all():
                cat_list.append(str(cat.name))
        elif cat_type == 'photo':
            if cat.photo_set.all():
                cat_list.append(str(cat.name))
    return cat_list
###################################
# latitude and longitude functions
###################################
def get_exif(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon
###########################
# Admin business
###########################
class PhotosInLine(admin.TabularInline):
    model = Photo
    extra = 3
    fieldsets = [
        (None, {'fields': ['name', 'date', 'cover', 'orientation', 'category', 'image']})
    ]

class PostAdmin(admin.ModelAdmin):
    search_fields = ['category', 'title', 'created']
    fields = ["title", "category", "slug", "body"]
    inlines = [PhotosInLine]

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ['category', 'post', 'date']

class MusicAdmin(admin.ModelAdmin):
    fields = ["band", "description", "iframe", "website", "category"]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Music, MusicAdmin)