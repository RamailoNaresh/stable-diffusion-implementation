from django.urls import path
from app import views

urlpatterns = [
    path('generate_image/', views.generate_image, name='generate-image'),
    path('upscale_image/', views.upscale_image, name='upscale-image'),
    path('remove_bg/', views.edit_image_remove_bg, name='remove-background'),
    path('sketch/', views.sketch_image, name='sketch image')
]
