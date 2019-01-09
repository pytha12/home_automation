from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from hauto.models import House, Room
from django.contrib.auth.models import User
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

#===============================================================================
# These tests are basically meant to test the business and design logic 
# requirements of the home automation API (ie. Custom methods - Using the TDD paradigm).
# In built python or django functions/library are not tested
#===============================================================================

# Instance Factories...
def create_user(username, password, email):
    return User.objects.create_user(
        username=username, 
        password=password, 
        email=email)
    
def create_house(street_address, city, country, furnace_status, furnace_temperature, owner):
    return House.objects.create(
        street_address=street_address, 
        city=city, country=country, 
        furnace_status=furnace_status,
        furnace_temperature=furnace_temperature, 
        owner=owner)
    
def create_room(room_label, room_temperature, house, owner):
    return Room.objects.create(
        room_label=room_label,
        room_temperature=room_temperature,
        house=house,
        owner=owner)
    
class UserHouseRoomModelsCreationTests(APITestCase):
    
    def test_the_creation_of_user_house_room_instances(self):
        '''
        Tests if we can successfully create User, House, and Room Instances successfully,
        given the required fields
        '''
        owner = create_user(
                    username='sam', 
                    password='nimda123', email='sam@gmail.com')
        
        house = create_house(
                    street_address='9 London st', 
                    city='St. Catharines',
                    country='Canada',
                    furnace_status='OFF',
                    furnace_temperature=34.0, 
                    owner=owner)
        
        room = create_room(
                    room_label='room1', 
                    room_temperature=27.0, 
                    house=house, 
                    owner=owner)
    
        # test instances ..True if isinstance 
        self.assertTrue(isinstance(owner, User))
        self.assertTrue(isinstance(house, House))
        self.assertTrue(isinstance(room, Room))
        
        # else False
        self.assertFalse(isinstance(owner, Room))
        self.assertFalse(isinstance(house, User))
        self.assertFalse(isinstance(room, House))
        
        # check against expected fields..Model field label = Instance label
        self.assertEqual(house.__str__(), "%s (%s)" % (house.street_address, house.city))
        self.assertEqual(room.__str__(), room.room_label)
        self.assertEqual(owner.__str__(), owner.username)
        
        
    def test_create_house_without_rooms(self):
        '''
        Should be able to create house with rooms.
        '''
        owner = create_user(
                    username='sam', 
                    password='nimda123', email='sam@gmail.com')
        house = create_house(
                    street_address='9 London st', 
                    city='St. Catharines',
                    country='Canada',
                    furnace_status='OFF',
                    furnace_temperature=34.0, 
                    owner=owner)
        
        self.assertTrue(isinstance(house, House))
        
    def test_create_rooms_without_house(self):
        '''
        It is possible to create a room without a house. House Foreign key accepts 
        NULL(None). This allows flexibility and defers adding room to a house in case a room
        was created first.
        '''
        owner = create_user(
                    username='sam', 
                    password='nimda123', email='sam@gmail.com')
        room = create_room(
                    room_label='room1', 
                    room_temperature=27.0, 
                    house=None,
                    owner=owner)
        self.assertTrue(isinstance(room, Room))
        
    def test_change_furnace_temp_automatically_to_max_or_min_room_temp_on_status_update(self):
        '''
        Furnace temperature might be set above above any needed room temperature. 
        This wastes energy. To cut on waste, whenever the furnace status changes,
        automatically set the furnace status to the max(heat) or min(fan) temp to save energy.
        '''
        owner = create_user(
                    username='sam', 
                    password='nimda123', email='sam@gmail.com')
        
        house = create_house(
                    street_address='9 London st', 
                    city='St. Catharines',
                    country='Canada',
                    furnace_status='OFF',
                    furnace_temperature=34.0, 
                    owner=owner)
        
        room1 = create_room(
                    room_label='room1', 
                    room_temperature=29.0, 
                    house=house, 
                    owner=owner)
        room2 = create_room(
                    room_label='room2', 
                    room_temperature=27.0, 
                    house=house, 
                    owner=owner)
        room3 = create_room(
                    room_label='room3', 
                    room_temperature=25.0, 
                    house=house, 
                    owner=owner)
        # change furnace status to FAN('Running Fan') : furnace_temperature = 25.0
        house.furnace_status = 'FAN'
        house.save()
        self.assertEqual(house.furnace_temperature, 25.0)
        self.assertNotEqual(house.furnace_temperature, 34.0)
        self.assertNotEqual(house.furnace_temperature, 27.0)
        self.assertNotEqual(house.furnace_temperature, 29.0)
        
        # change furnace status to Heat('Running Heat')
        house.furnace_status = 'HEAT'
        house.save()
        self.assertEqual(house.furnace_temperature, 29.0)
        self.assertNotEqual(house.furnace_temperature, 34.0)
        self.assertNotEqual(house.furnace_temperature, 27.0)
        self.assertNotEqual(house.furnace_temperature, 25.0)
        
        
        
        
        
        
        
        
        
        