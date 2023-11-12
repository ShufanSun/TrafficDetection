from beamngpy import BeamNGpy
from beamngpy.sensors import Camera, State
import time
import cv2
import numpy as np

try: 
    # Instantiate BeamNGpy instance running the simulator from the given path,
    # communicating over localhost:64256
    bng = BeamNGpy('localhost', 64256, home="C:\Games\BeamNG.tech.v0.30.6.0", quit_on_close=False)
    # Launch BeamNG.tech
    try:
        bng.open(launch=False)
    except Exception as e:
        bng.open(launch=True)


    input("Press Enter to continue...")
    player_vehicle_id = bng.vehicles.get_player_vehicle_id()["vid"]
    # bng.vehicles.replace(vehicle)
    # vehicle.ai.set_mode('span')

    player_vehicle = bng.get_current_vehicles()[str(player_vehicle_id)]
    player_vehicle.connect(bng)

    player_vehicle.sensors.poll()
    player_pos: tuple = player_vehicle.state['pos']
    print(player_pos)
    dashcam = Camera(
        'dashcam', bng, player_vehicle, 0.2, 0, (player_vehicle.state['pos'][0] + -0.3, player_vehicle.state['pos'][1], player_vehicle.state['pos'][2] + 3), dir=player_vehicle.state['dir'],
        field_of_view_y=65, resolution=(640, 640), is_render_depth=False, is_render_annotations=False)

    time.sleep(1)

    while True:
        time.sleep(0.1)
        data = dashcam.poll()
        image = np.array(data['colour'])
        
        cv2.imshow('Dashcam', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        cv2.waitKey(1)


except:
    dashcam.remove()
    player_vehicle.disconnect()
    
