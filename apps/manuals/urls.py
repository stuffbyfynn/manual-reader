from django.urls import path
from . import views

app_name = 'manuals'

urlpatterns = [
    path('', views.BrandListView.as_view(), name='brand_list'),
    path('<slug:brand_slug>/', views.ModelListView.as_view(), name='model_list'),
    path('<slug:brand_slug>/<slug:model_slug>/<int:year>/', views.ManualListView.as_view(), name='manual_list'),
    path('viewer/<int:manual_id>/', views.viewer_page, name='viewer'),
]
