
from django.urls import path, re_path
from app.viewsets import *
from app.views import healthcheck, login
from rest_framework.routers import DefaultRouter

# swagger (documentation)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
# end swagger
router = DefaultRouter()
router.register('post', PostViewSet, basename="post")
router.register('user', UserViewSet, basename="user")

urlpatterns = router.urls
urlpatterns += [
    # custom views
    path("healthcheck/", healthcheck, name="healthcheck"),
    path("login/", login, name="login"),
    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path("documentation/", schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui")
]
