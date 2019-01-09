'''
@author : Norbert Kofi Amafu <pytha12@gmail.com>
@date : 2019/01/05
'''
# Authentication 
# Home Automation

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Max, Min


class House(models.Model):
    '''
    @Note : Houses can be identified by address(Street address, Unit, City, State/Province, 
                                    Zip/Post Code, Country)
            No need to have a separate model for furnace since every house has a single furnace. 
            It can as well be in the House model
            
            Rooms have one temperature each.
            Preamble: Each room has a thermostat including the furnace room.
            The furnace heats up to temperature set by the thermostat.
            The key solution to the problem of energy lost is to make this temperature
            dynamic; based on the Max or Min temperature of each room in a house.
            
            Assumption: Rooms have their IDEAL temperature(RT) each.
            As long as each room's temperature remains constant, there would be 
            no need to ever change, no matter the season or weather condition.
            **Thermostat can regulate the temperature to keep it stable.
            >> PROS : if all rooms are at their ideal temperature, turn furnace off to SAVE ENERGY.
            
            Example room temperatures: RT1 = 29deg, RT2 = 28deg, RT3 = 27deg, RT4 = 26deg, RT5 = 25deg
            
            FURNACE STATUS: 
                OFF  : RT(s) = Normal or within range.
                HEAT : Turn on Furnace to Max(RT). Thermostats bring down temperatures in rooms with lower RT requirements.
                       >> PROS : SAVE ENERGY. Furnace will not be heated more than necessary. eg. Max(RT) = RT1 = 29deg
                FAN  : Run fan till Min(RT) is attained. Thermostats regulates temperature by regulating amount of air allowed in rooms with higher RT.
                       In some cases, vents could be shut to prevent temperature cooling below RT in rooms with higher RT requirements.
                       >> PROS : SAVE ENERGY. Furnace will not blow too much air than necessary. eg. Min(RT) = RT5 = 25deg
    @reference : https://www.comfortflow.com/blog/heating-service/how-does-a-furnace-work/ (How furnace works)
    
    '''
    
    # Furnace choices
    OFF = 'OFF'
    FAN = 'FAN'
    HEAT = 'HEAT'
    FURNACE_STATE_CHOICES = (
        (OFF, 'OFF'), 
        (FAN, 'Running Fan'), 
        (HEAT, 'Running Heat'),
    )
    
    street_address = models.CharField("Street address", max_length=50, null=True) # street number and street name. eg. 23 Pelham St.
    unit = models.CharField("Unit #", max_length=5, null=True)
    city = models.CharField("City", max_length=60)
    state_province = models.CharField("State / Province", max_length=50, null=True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12, null=True)
    country = models.CharField("Country", max_length=50, null=True)
    furnace_temperature = models.DecimalField("Furnace Temperature", max_digits=5, decimal_places=2) # A furnace is in a room so it has a temperature too.
    furnace_status = models.CharField("Furnace Status",
        max_length=15, 
        choices=FURNACE_STATE_CHOICES, 
        default=OFF, 
        null=True, 
        blank=True,
    )
    owner = models.ForeignKey(User, related_name='houses', on_delete=models.CASCADE)    
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(editable=False, default=timezone.now)
    

    def save(self, *args, **kwargs):
        ''' 
        On save, update timestamps. 
        We do not want make date created editable
        This approach is more reliable than auto_now or auto_now_add 
        '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        
        # Energy saver mode :: on update of furnace status.
        if self.id:
            # Get the Max(room temp) for all rooms in this house instance.
            RqsetMax = Room.objects.filter(house_id=self.id).aggregate(Max('room_temperature'))
            self._max_temp = RqsetMax.get('room_temperature__max')
            # Get the Min(room temp) for all rooms in this house instance.
            RqsetMin = Room.objects.filter(house_id=self.id).aggregate(Min('room_temperature'))
            self._min_temp = RqsetMin.get('room_temperature__min')
            
            if self.furnace_status == 'HEAT' and self._max_temp:
                self.furnace_temperature = self._max_temp
            elif self.furnace_status == 'FAN' and self._min_temp:
                self.furnace_temperature = self._min_temp
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return "%s (%s)" % (self.street_address, self.city)
    

    class Meta:
        ordering = ('created',)
              
    
        
    
class Room(models.Model):
    """ 
    Assumption: Temperature scale is in degree celcius
    """
    # Light choices
    ON = 'ON'
    OFF = 'OFF'
    NoLIGHTS = 'NL'
    LIGHT_STATE_CHOICES = (
        (ON, ON), 
        (OFF, OFF),
        (NoLIGHTS, 'No Lights'),
    )
    
    room_label = models.CharField("Room Label", max_length=50, null=True) # alphanumeric
    room_temperature = models.DecimalField("Room Temperature", max_digits=5, decimal_places=2) 
    house = models.ForeignKey(House, null=True, related_name='rooms', on_delete=models.CASCADE)
    light_status = models.CharField("Light Status",
        max_length=4, 
        choices=LIGHT_STATE_CHOICES, 
        default=OFF, 
        null=True, 
        blank=True,
    )
    owner = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE) 
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(editable=False, default=timezone.now)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps. '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        
        return super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('room_label', 'house',)
        ordering = ('id',)
        
    def __str__(self):
        return "%s" % self.room_label
        
    