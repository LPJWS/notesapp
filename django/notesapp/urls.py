from django.conf.urls import url
from django.urls import path
from rest_framework.routers import SimpleRouter

from notesapp.views import *

router = SimpleRouter()
router.register(r'auth', AuthView, basename='auth')
router.register(r'user', UserView, basename='user')
router.register(r'note', NoteView, basename='note')

urlpatterns = router.urls
