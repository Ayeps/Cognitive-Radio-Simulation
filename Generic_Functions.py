from Base_Station import BaseStation
from User_Device import UserDevice
import numpy as np
from math import ceil



"""Create a set of base stations and place them into a square grid.
The result is more even if the square root of the station count is an integer."""
def create_base_station_grid(number_of_stations, width, operator):
    #Determine the number of rows/columns
    rows = ceil(np.sqrt(number_of_stations))
    increment = width / rows
    #Fill the grid with stations
    assigned_stations = []
    for i in range(0, rows):
        for j in range(0, rows):
            if len(assigned_stations) < number_of_stations:
                station = BaseStation(x=i*increment, y=j*increment, operator=operator)
                assigned_stations.append(station)
    return assigned_stations
    
    


"""Calculate received signal power received from another transmitter
according to Friis transmission formula (free space).
This can be substituted with a more accurate formula later on."""
def calculate_signal_power(receiver, sender):
    distance = np.sqrt(np.power(receiver.x - sender.x,2) + np.power(receiver.y - sender.y,2))
    avg_wavelength = np.average(sender.frequency)
    received_signal_power = (sender.tx_power * sender.gain * receiver.gain * np.power(avg_wavelength,2))\
                             / np.power(4 * np.pi * distance, 2)
    return received_signal_power


