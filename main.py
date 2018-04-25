import argparse
import logging
import math
import pickle

import matplotlib.pyplot as plt
import numpy as np

import settings
from base_station import BaseStation
from user_device import UserDevice

LOG = logging.getLogger("main")
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

if args.verbose:
    LOG.debug("Verbosity turned on")
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def create_base_station_grid(number_of_stations, width, spectrum_sharing=True):
    """Create a set of base stations and place them into a square grid.
    The result is more even if the square root of the station count is
    an integer. (Should be)
    """
    # Determine the number of rows/columns
    rows = math.ceil(np.sqrt(number_of_stations))
    increment = width / (rows - 1)
    # Fill the grid with stations
    assigned_stations = []
    oper_index = 1
    cnt = 0
    for i in range(0, rows):
        for j in range(0, rows):
            if len(assigned_stations) < number_of_stations:
                cnt += 1
                if spectrum_sharing == True:
                    station = BaseStation(
                        x=i * increment, y=j * increment, id=cnt)
                else:
                    station = BaseStation(
                        x=i * increment,
                        y=j * increment,
                        operator=oper_index,
                        id=cnt)
                    oper_index = ((oper_index + 1) % 3) + 1
                assigned_stations.append(station)
    return assigned_stations


def create_users(number_of_users, width, spectrum_sharing=True):
    """Create a set of users and place them randomly into our designated
    area.
    """
    user_list = []
    oper_index = 1
    for i in range(0, number_of_users):
        x = np.random.randint(0, width)
        y = np.random.randint(0, width)
        if spectrum_sharing == True:
            user = UserDevice(x=x, y=y)
        else:
            user = UserDevice(x=x, y=y, operator=oper_index)
            oper_index = ((oper_index + 1) % 3) + 1
        user_list.append(user)
    return user_list


######################
#  START SIMULATING  #
######################
"""Create and place 9 stations in 1 square kilometer.
Also assigns a minimal starting frequency range to each base station at random.
This will be grown dynamically later on."""
base_stations = create_base_station_grid(9, settings.area_width, False)
"""Obligatory LOG.debuging to confirm it works"""
LOG.debug("Base Stations")
for x in base_stations:
    LOG.debug(x)
"""Place 50 users at random locations"""
# Load them from file
# users = create_users(50, settings.area_width, False)
#
f = open('store.pckl', 'rb')
users = pickle.load(f)
f.close()
"""Let users connect to their nearest/best station first.
Strive for maximal signal strength without considering other users and interference (GADIA)."""
for user in users:
    user.set_initial_user_station(base_stations)
#set_initial_user_stations(users, base_stations)
"""Obligatory LOG.debuging to confirm it works"""
LOG.debug("\nUsers")
for x in users:
    LOG.debug(x)
"""Make base stations listen to each other on initial frequency slices."""
for station in base_stations:
    station.update_base_stations_in_range(base_stations)
"""Obligatory LOG.debuging to confirm it works."""
LOG.debug("\nWhich station needs hearing aids?")
for station_1 in base_stations:
    for station_2 in station.base_stations_in_range:
        station_2_id = station_2[0].id
        LOG.debug(str(station_1.id) + "\t" + str(station_2_id))
"""Let base stations grow their frequency ranges up to the limit.
At this stage we do not listen to users, only nearby stations."""
"""LOOP START"""
"""Users can now switch to another less populated base station.
This is done with the following knowledge:
- Number of users that each nearby base station is serving
- Frequency ranges currently used by nearby stations."""
"""Let base stations adjust their frequency range dynamically according to the user count."""
"""LOOP END WHEN NOTHING CHANGES"""
"""Summarise and plot results"""
#Lines from users to their base stations
for user in users:
    plt.plot(
        [user.x, user.current_base_station.x],
        [user.y, user.current_base_station.y],
        color="green")
#Users as dots
for user in users:
    plt.plot(user.x, user.y, "o", color="blue")
#Stations as dots
for station in base_stations:
    plt.plot(station.x, station.y, "o", color="black")
    plt.text(station.x, station.y, str(station.id), color="red", fontsize=12)
plt.show()