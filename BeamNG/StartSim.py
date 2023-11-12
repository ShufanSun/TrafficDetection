from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera, State
import time
import cv2
import numpy as np

# Instantiate BeamNGpy instance running the simulator from the given path,
# communicating over localhost:64256
bng = BeamNGpy('localhost', 64256, home="C:\Games\BeamNG.tech.v0.30.6.0", quit_on_close=False)
# Launch BeamNG.tech
try:
    bng.open(launch=False)
except Exception as e:
    bng.open(launch=True)


# Create a scenario in west_coast_usa called 'example'
# scenario = Scenario('west_coast_usa', 'example')
# Create an ETK800 with the licence plate 'PYTHON'
# vehicle = Vehicle('ego_vehicle', model='etk800', license='PYTHON')
# Add it to our scenario at this position and rotation
# scenario.add_vehicle(vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))
# Place files defining our scenario for the simulator to read
# scenario.make(bng)

# Load and start our scenario
# bng.scenario.load(scenario)
# bng.scenario.start()
# Make the vehicle's AI span the map

# input("Press Enter to continue...")
pos_sensor = State()
player_vehicle_id = bng.vehicles.get_player_vehicle_id()["vid"]
# bng.vehicles.replace(vehicle)
# vehicle.ai.set_mode('span')

player_vehicle = bng.get_current_vehicles()[str(player_vehicle_id)]
player_vehicle.sensors.attach
player_vehicle.attach_sensor('pos', pos_sensor)

time.sleep(1)
player_vehicle.poll_sensors()

while len(pos_sensor.data) == 0:
    time.sleep(0.1)
print(pos_sensor.data)

if bng.tech_enabled():
    player_pos: tuple = pos_sensor.data['pos']
    dashcam = Camera(
        'dashcam', bng, player_vehicle, (player_pos[0], player_pos[1] + 1, player_pos[2] + 1.5), dir=(0, 0, -0.75),
        field_of_view_y=60, resolution=(1024, 1024), requested_update_time=0, is_render_depth=False)
    rq_id = dashcam.send_ad_hoc_poll_request()
    while not dashcam.is_ad_hoc_poll_request_ready(rq_id):
        time.sleep(0.1)
    data = dashcam.collect_ad_hoc_poll_request(rq_id)
    image = data['colour']
    
    cv2.imshow('image', np.asarray(image.convert('RGB')))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
