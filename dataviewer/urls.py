from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('dataviewer/tracking/', views.tracking, name='tracking'),
    path('dataviewer/tracking/<int:dept_id>/', views.tracking_dept, name='tracking_dept'),
    path('dataviewer/tracking/<int:dept_id>/<str:tab>/', views.tracking_dept_tab, name='tracking_dept_tab'),
    path('daily/', views.daily, name='daily'),
    path('weekly/', views.weekly, name='weekly'),
    # path('test/', views.test, name='test'),
    # path('feedback/', views.feedback, name='feedback'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

