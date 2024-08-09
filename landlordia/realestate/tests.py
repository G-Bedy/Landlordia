from rest_framework.test import APITestCase
from django.urls import resolve


class PropertySmokeTest(APITestCase):
    """ CRUD """
    def setUp(self):
        pass

    def test_create_property(self):
        self.client.post(
            url=resolve('realestate:property_list'),
            data={
                ...
            }
        )


class LeaseContractSmokeTest(APITestCase):
    """ CRUD """
    pass
