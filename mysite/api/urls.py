from django.urls import path,include

from .views import ProductListApiView,PostListDetail

urlpatterns = [
    path('dj-rest-auth/registration/',include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('<int:pk>/',PostListDetail.as_view()),
    path('', ProductListApiView.as_view())
]
