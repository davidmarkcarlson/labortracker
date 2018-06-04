"""LaborTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import (
    portal_home,
    portal_account,
    partograph,
    patient_list,
    add_patient,
    add_reading,
    add_practitioner,
    current_labors,
    patient_view,
    add_partograph,
    practitioner_list,
    complete_delivery
)

urlpatterns = [
    url(r'^$', portal_home, name="portal"),
    url(r'^account/$', portal_account, name='account'),
    url(r'^partograph/(?P<partograph_id>\d+)/$', partograph, name='partograph'),
    url(r'^patient-list/$', patient_list, name='patient_list'),
    url(r'^add-patient/$', add_patient, name='add_patient'),
    url(r'^add-practitioner/$', add_practitioner, name='add_practitioner'),
    url(r'^add-reading/$', add_reading, name='add_reading'),
    url(r'^current-labors/$', current_labors, name='current_labors'),
    url(r'^patient/(?P<id>\d+)/$', patient_view, name='patient_view'),
    url(r'^add-partograph/$', add_partograph, name='add_partograph'),
    url(r'^practitioner-list/$', practitioner_list, name='practitioner_list'),
    url(r'^complete-delivery/$', complete_delivery, name='complete_delivery')
]
