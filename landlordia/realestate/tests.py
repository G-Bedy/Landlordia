from datetime import datetime, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from realestate.models import LeaseContract, Payment, Property, Tenant
from users.models import CustomUser


class UserMixin:
    def create_and_login_user(self,
                              email='testuser@mail.ru',
                              password='12345',
                              is_staff=False):
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_staff=is_staff
        )
        self.client.login(email=email, password=password)
        return user

    def create_and_login_admin(self,
                               email='testuser@mail.ru',
                               password='12345',
                               is_staff=True):
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_staff=is_staff
        )
        self.client.login(email=email, password=password)
        return user


class PropertyMixin:
    def create_property(self, owner):
        return Property.objects.create(
            owner=owner,
            address='Красная площадь дом 1',
            property_type='Apartment',
            description='Тестовая квартира',
            rental_type='Hourly',
            price=100500.00,
            price_period='Hour',
            minimum_rental_value=2,
            minimum_rental_unit='Hour'
        )


class TenantMixin:
    def create_tenant(self):
        return Tenant.objects.create(
            first_name='Иван',
            last_name='Иванов',
            email='ivan@mail.ru',
            phone_number='1234567890',
            address='улица Тестовая'
        )


class LeaseContractMixin:
    def create_lease_contract(self, property, tenant):
        return LeaseContract.objects.create(
            property=property,
            tenant=tenant,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            rent_amount=Decimal('40000.00'),
            rent_period='Month',
            deposit_amount=Decimal('70000.00')
        )


class PaymentMixin:
    def create_payment(self, lease):
        return Payment.objects.create(
            lease=lease,
            amount=45000.00
        )


class PropertyAPITestCase(UserMixin, PropertyMixin, APITestCase):

    def setUp(self):
        self.owner = self.create_and_login_user()
        self.property = self.create_property(owner=self.owner)
        self.url_list = reverse('realestate:property-list')
        self.url_detail = reverse(
            'realestate:property-detail',
            kwargs={'pk': self.property.pk}
        )

    def test_get_property_list(self):
        """Тест на получение списка объектов Property"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['address'], self.property.address)

    def test_create_property(self):
        """Тест на создание объекта Property"""
        data = {
            "address": "123",
            "property_type": "Apartment",
            "description": "квартира создана от имени админа 123",
            "rental_type": "Hourly",
            "price": Decimal(10000.00),
            "price_period": "Hour",
            "minimum_rental_value": 1,
            "minimum_rental_unit": "Hour"
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)
        self.assertEqual(
            Property.objects.get(address='123').description,
            'квартира создана от имени админа 123'
        )

    def test_get_property_detail(self):
        """Тест на получение объекта Property"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], self.property.address)

    def test_update_property(self):
        """Тест на обновление объекта Property"""
        data = {
            "address": "Новый тестовый адрес",
            "property_type": "Apartment",
            "description": "квартира создана от имени админа 123",
            "rental_type": "Hourly",
            "price": Decimal(77777.77),
            "price_period": "Hour",
            "minimum_rental_value": 1,
            "minimum_rental_unit": "Hour"
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_property = Property.objects.get(pk=self.property.pk)
        self.assertEqual(updated_property.address, 'Новый тестовый адрес')
        self.assertEqual(updated_property.price, Decimal('77777.77'))

    def test_delete_property(self):
        """Тест на удаление объекта Property"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)


class TenantAPITestCase(UserMixin, PropertyMixin, TenantMixin,
                        LeaseContractMixin, APITestCase):

    def setUp(self):
        self.owner = self.create_and_login_admin()
        self.property = self.create_property(owner=self.owner)
        self.tenant = self.create_tenant()
        self.lease_contract = self.create_lease_contract(
            property=self.property,
            tenant=self.tenant
        )
        self.url_list = reverse('realestate:tenant-list')
        self.url_detail = reverse(
            'realestate:tenant-detail',
            kwargs={'pk': self.tenant.pk}
        )

    def test_get_tenant_list(self):
        """Тест на получение списка объектов Tenant"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], self.tenant.email)

    def test_create_tenant(self):
        """Тест на создание объекта Tenant"""
        data = {
            'first_name': 'Пётр',
            'last_name': 'Петров',
            'email': 'piter@mail.ru',
            'phone_number': '89261234567',
            'address': 'улица Петрова'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tenant.objects.count(), 2)
        self.assertEqual(
            Tenant.objects.get(email='piter@mail.ru').first_name, 'Пётр'
        )

    def test_get_tenant_detail(self):
        """Тест на получение объекта Tenant"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.tenant.email)

    def test_update_tenant(self):
        """Тест на обновление объекта Tenant"""
        data = {
            'first_name': 'Сидр',
            'last_name': 'Сидоров',
            'email': 'sidr@mail.ru',
            'phone_number': '1234567890',
            'address': 'улица Сидорова'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tenant = Tenant.objects.get(pk=self.tenant.pk)
        self.assertEqual(updated_tenant.first_name, 'Сидр')
        self.assertEqual(updated_tenant.email, 'sidr@mail.ru')

    def test_delete_tenant(self):
        """Тест на удаление объекта Tenant"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tenant.objects.count(), 0)


class LeaseContractAPITestCase(UserMixin, PropertyMixin, TenantMixin,
                               LeaseContractMixin, APITestCase):

    def setUp(self):
        self.owner = self.create_and_login_user()
        self.property = self.create_property(owner=self.owner)
        self.tenant = self.create_tenant()
        self.lease_contract = self.create_lease_contract(
            property=self.property,
            tenant=self.tenant
        )
        self.url_list = reverse('realestate:leasecontract-list')
        self.url_detail = reverse(
            'realestate:leasecontract-detail',
            kwargs={'pk': self.lease_contract.pk}
        )

    def test_get_leasecontract_list(self):
        """Тест на получение списка объектов LeaseContract"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rent_amount'], '40000.00')

    def test_create_leasecontract(self):
        """Тест на создание объекта LeaseContract"""
        data = {
            'property': self.property.id,
            'tenant': self.tenant.id,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=180)).isoformat(),
            'rent_amount': '45000.00',
            'rent_period': 'Month',
            'deposit_amount': '90000.00'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LeaseContract.objects.count(), 2)

    def test_get_leasecontract_detail(self):
        """Тест на получение объекта LeaseContract"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rent_amount'], '40000.00')

    def test_update_leasecontract(self):
        """Тест на обновление объекта LeaseContract"""
        data = {
            'property': self.property.id,
            'tenant': self.tenant.id,
            'start_date': self.lease_contract.start_date.isoformat(),
            'end_date': (datetime.now() + timedelta(days=540)).isoformat(),
            'rent_amount': 55000.00,
            'rent_period': 'Month',
            'deposit_amount': 110000.00
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lease_contract.refresh_from_db()
        self.assertEqual(self.lease_contract.rent_amount, Decimal('55000.00'))

    def test_delete_leasecontract(self):
        """Тест на удаление объекта LeaseContract"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LeaseContract.objects.count(), 0)

    def test_invalid_date_validation(self):
        """Тест на валидацию некорректных дат в LeaseContract"""
        data = {
            'property': self.property.id,
            'tenant': self.tenant.id,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() - timedelta(days=1080)).isoformat(),
            'rent_amount': 45000.00,
            'rent_period': 'Month',
            'deposit_amount': 90000.00
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Дата окончания аренды не может быть раньше даты начала аренды",
            response.data['non_field_errors']
        )


class PaymentAPITestCase(UserMixin, PropertyMixin, TenantMixin,
                         LeaseContractMixin, PaymentMixin, APITestCase):
    def setUp(self):
        self.owner = self.create_and_login_user()
        self.property = self.create_property(owner=self.owner)
        self.tenant = self.create_tenant()
        self.lease_contract = self.create_lease_contract(
            property=self.property,
            tenant=self.tenant
        )
        self.payment = self.create_payment(lease=self.lease_contract)
        self.url_list = reverse('realestate:payment-list')
        self.url_detail = reverse(
            'realestate:payment-detail',
            args=[self.payment.id]
        )

    def test_get_payment_list(self):
        """Тест на получение списка платежей. Модель Payment."""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], '45000.00')

    def test_create_payment(self):
        """Тест на создание нового платежа"""
        data = {
            'lease': self.lease_contract.id,
            'amount': '50000.00'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)
        self.assertEqual(
            Payment.objects.latest('id').amount,
            Decimal('50000.00')
        )

    def test_get_payment_detail(self):
        """Тест на получение платежа"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '45000.00')

    def test_update_payment(self):
        """Тест на обновление платежа"""
        data = {
            'lease': self.lease_contract.id,
            'amount': '55000.00',
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.amount, Decimal('55000.00'))

    def test_delete_payment(self):
        """Тест на удаление платежа"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Payment.objects.count(), 0)
