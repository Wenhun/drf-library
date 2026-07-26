from rest_framework import routers

from library.views import *

app_name = "library"

default_router = routers.DefaultRouter()
default_router.register(r"books", BookViewSet, basename="books")
default_router.register(r"authors", AuthorViewSet, basename="authors")


urlpatterns = default_router.urls
