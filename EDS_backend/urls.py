from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Expert Database Api",
        default_version= 'v1',
        description= "This is AfriDATAi expert database api used to register experts who have specialization in different fields. The purpose of the api is to allow the AfriDATAi staff to be able to register experts and also build their cv, search and filter experts using different tags and filtering mechanisms."
        ,
        terms_of_service= "https://www.example.com/terms",
        contact= openapi.Contact(email="ziontaa9@gmail.com"),
        license= openapi.License(name='MIT License')
        ),
    public = True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path("", include("fileparser.urls")),
     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
