from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as auth_token_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('product/<int:pk>/order/', views.place_order, name='place_order'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
]

# API

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Store API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )
#
# urlpatterns = [
#     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('api/v1/profile/', views.ProfileView.as_view(), name='profile'),
#     path('api/v1/register/', views.RegisterView.as_view(), name='register'),
#     path('api/v1/login/', auth_token_views.obtain_auth_token, name='login_view'),
#     path('api/v1/logout/', views.logout_view, name='logout'),
#     path('api/v1/product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
#     path('api/v1/category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
#     path('api/v1/product/<int:pk>/order/', views.PlaceOrderView.as_view(), name='place_order'),
#     path('api/v1/cart/', views.CartView.as_view(), name='cart'),
#     path('api/v1/add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),
#     path('api/v1/remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
