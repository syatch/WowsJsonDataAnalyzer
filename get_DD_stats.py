import json
from get_sort import *
from save_output import *

def read_json() :
    with open(data_path) as jsdata:
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
    data_path = 'data/Destroyer.json'
    data = read_json()
    sort_tool = SortTool(data)
    save_tool = SaveTool()
    # check_data(data)
    Tier = [8, 9]
    for T in Tier :
        print("Tier : " + str(T))
        id = ["bottom_range", "all_range", "top_range"]
        T_range = 2

        print(" - detect")
        data = sort_tool.get_detect_sort(T, T_range)
        save_tool.save_detect(data, T, id)

        print(" - HP")
        data = sort_tool.get_HP_sort(T, T_range)
        save_tool.save_health(data, T, id)

        print(" - fusillade_damage")
        data = sort_tool.get_fusillade_damage_sort(T, T_range)
        save_tool.save_fusillade_damage(data, T, id)

        print(" - DPS")
        data = sort_tool.get_DPS_sort(T, T_range)
        save_tool.save_DPS(data, T, id)

        print(" - fusillade_burn_probability")
        data = sort_tool.get_fusillade_burn_probability_sort(T, T_range)
        save_tool.save_fusillade_burn(data, T, id)

        print(" - burn_probability_per_s")
        data = sort_tool.get_burn_probability_per_s_sort(T, T_range)
        save_tool.save_burn_probability(data, T, id)

        print(" - bullet_speed")
        data = sort_tool.get_bullet_speed_sort(T, T_range)
        save_tool.save_bullet_speed(data, T, id)

        print(" - artillery_rotation")
        data = sort_tool.get_artillery_rotation_sort(T, T_range)
        save_tool.save_rotation(data, T, id)

        print(" - max_speed")
        data = sort_tool.get_max_speed_sort(T, T_range)
        save_tool.save_max_speed(data, T, id)

        print(" - rudder")
        data = sort_tool.get_rudder_sort(T, T_range)
        save_tool.save_rudder(data, T, id)
        print(" - end")

    write_json(sort_tool.get_dic())
