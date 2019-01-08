from rest_framework import serializers
from hauto.models import House, Room
from django.contrib.auth.models import User


class HouseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    rooms = serializers.HyperlinkedRelatedField(
        many=True, view_name='room-detail', queryset=Room.objects.all().order_by('-id'))
    
    class Meta:
        model = House
        fields = ('url', 'id', 'owner', 'street_address', 'unit', 'city', 'state_province', 
                  'zip_code', 'country', 'furnace_temperature', 'furnace_status', 'rooms')
        

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    house = serializers.HyperlinkedRelatedField(view_name='house-detail', read_only=True)
    
    class Meta:
        model = Room
        fields = ('url', 'id', 'owner', 'house', 'room_label', 'room_temperature', 'light_status')
        
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    houses = serializers.HyperlinkedRelatedField(
        many=True, view_name='house-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'houses')