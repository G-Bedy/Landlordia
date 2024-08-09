from rest_framework.test import APITestCase
from django.urls import resolve

class PropertySmokeTest(APITestCase):

    def setUp(self):
        pass

    def test_create_property(self):
        self.client.post(
            url=resolve('realestate:property_list')
        )



