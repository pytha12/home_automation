from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from hauto.models import House, Room
from django.contrib.auth.models import User
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.test import RequestsClient



#===============================================================================
# These tests are basically meant to test the business and design logic 
# requirements of the home automation API (ie. Custom methods - Using the TDD paradigm).
# In built python or django functions/library are not tested
#===============================================================================

def create_user(username, password, email):
    return User.objects.create_user(
        username=username, 
        password=password, 
        email=email)
    
def create_house(street_address, city, country, furnace_temperature, owner):
    return House.objects.create(
        street_address=street_address, 
        city=city, country=country, 
        furnace_temperature=furnace_temperature, owner=owner)
    
def create_room(room_label, room_temperature, house, owner):
    return Room.objects.create(
        room_label=room_label,
        room_temperature=room_temperature,
        house=house,
        owner=owner)
    
    

class ListURLRequestTests(APITestCase):
    '''
    test_basic_requests makes sure all the list urls for users, houses, rooms
    can be reached.
    '''
    def test_basic_requests(self):
        users_response = self.client.get('http://testserver/users/')
        houses_response = self.client.get('http://testserver/houses/')
        rooms_response = self.client.get('http://testserver/rooms/')
        assert users_response.status_code == houses_response.status_code == rooms_response.status_code == status.HTTP_200_OK
        
        
            
class DetailURLRequestTests(APITestCase):
    
    def test_api_client_requests_to_detail_pages(self):
        '''
        Test if calls can be made to details pages of newly created instances.
        '''
        owner = create_user(
                    username='sam', 
                    password='nimda123', email='sam@gmail.com')
        
        house = create_house(
                    street_address='9 London st', 
                    city='St. Catharines',
                    country='Canada',
                    furnace_temperature=34.0, 
                    owner=owner)
        
        room = create_room(
                    room_label='room1', 
                    room_temperature=27.0, 
                    house=house, 
                    owner=owner)
        
        user_url = reverse('user-detail', args=(owner.id,))
        house_url = reverse('house-detail', args=(house.id,))
        room_url = reverse('room-detail', args=(room.id,))
        
        user_response = self.client.get(user_url, format='json')
        house_response = self.client.get(room_url, format='json')
        room_response = self.client.get(room_url, format='json')
        
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(house_response.status_code, status.HTTP_200_OK)
        self.assertEqual(room_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_response.data), 4)
        self.assertEqual(len(house_response.data), 7)
        self.assertEqual(len(room_response.data), 7)
        
        
        
        
        
        
        
        