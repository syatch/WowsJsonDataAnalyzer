import json
from get_sort import *
from save_output import *
from base_data import *

def read_json(path) :
    with open(path) as jsdata:
        data = json.load(jsdata)
    return data

def check_data(data) :
    for ship_id in data['data']:
        ship_dic = data['data'][ship_id]
        # get name
        print("Name : " + ship_dic['name'])
        # get tier
        print("Tier : " + str(ship_dic['tier']))

        default_profile = ship_dic['default_profile']
        # get HP
        print("HP : " + str(default_profile['hull']['health']))
        # get barrels
        print("Artillery_Barrels : " + str(default_profile['hull']['artillery_barrels']))

        mobility = default_profile["mobility"]
        # get rudder
        print("Rudder Time : " + str(mobility['rudder_time']))
        # get turning radius
        print("Turning Radius : " + str(mobility['turning_radius']))
        # get max speed
        print("Max Speed : " + str(mobility['max_speed']))

        concealment = default_profile['concealment']
        print("Detect Distance By Plane : " + str(concealment['detect_distance_by_plane']))
        print("Detect Distance By Ship : " + str(concealment['detect_distance_by_ship']))

        artillery = default_profile['artillery']
        print("Rotation Time : " + str(artillery['rotation_time']))
        print("Shot Delay : " + str(artillery['shot_delay']))
        print("Distance : " + str(artillery['distance']))

        try :
            AP = shells['AP']
            print("Bullet Speed : " + str(HE['bullet_speed']))
            print("Damage : " + str(HE['damage']))
        except:
            pass
        try :
            SAP = shells['SAP']
            print("Bullet Speed : " + str(HE['bullet_speed']))
            print("Damage : " + str(HE['damage']))
        except:
            pass
        try :
            HE = shells['HE']
            print("Bullet Speed : " + str(HE['bullet_speed']))
            print("Damage : " + str(HE['damage']))
            print("Burn Probability : " + str(HE['burn_probability']))
        except:
            pass

def write_json(write_data) :
    with open('output/DD_data.json', 'w') as write_file:
        json.dump(write_data, write_file, indent = 4)


if __name__ == "__main__" :
    import time
    start_time = time.process_time()

    data_path = 'data/Destroyer.json'
    target_path = 'data/target.json'

    data = read_json(data_path)
    sort_tool = SortTool(data)
    save_tool = SaveTool()
    # check_data(data)
    search = read_json(target_path)
    for target in search['target'] :
        print("Tier : " + str(target[0]) + "  Ship : " + target[1])
        id = ["bottom_range", "all_range", "top_range"]
        T = target[0]
        T_range = 2

        for data_type in DataType :
            print(" - " + str(data_type.name))
            data = sort_tool.get_sort_data[data_type](T, T_range)
            save_tool.save_table(data, T, id, data_type, target[1])
            save_tool.save_hist(data, T, id, data_type, target[1])

    write_json(sort_tool.get_dic())

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("Elapsed Time :" + str(elapsed_time))
