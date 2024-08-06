from django.urls import path, include
from .views import *


urlpatterns = [
    path('tests/', Tests.as_view(), name='tests'),
    path('tests/detail/<int:pk>/', DetailTest.as_view(), name='detail-test'),
    path('test/detail/before/', BeforeTesting.as_view(), name='before'),
    path('tests/runtest/<int:pk_test>/', RunTest.as_view(), name='test-run'),
]