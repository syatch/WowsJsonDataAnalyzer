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
        for T_range in [[0, 2, "bottom_range"], [2, 2, "all_range"], [2, 0, "top_range"]] :
            print("range : " + T_range[2])

            bottom_T = max(T - T_range[0], 1)
            top_T = min(T + T_range[1], 10)

            print(" - detect")
            data = sort_tool.get_detect_sort(bottom_T, top_T)
            save_tool.save_detect(data, T, T_range[2])

            print(" - HP")
            data = sort_tool.get_HP_sort(bottom_T, top_T)
            save_tool.save_health(data, T, T_range[2])

            print(" - fusillade_damage")
            data = sort_tool.get_fusillade_damage_sort(bottom_T, top_T)
            save_tool.save_fusillade_damage(data, T, T_range[2])

            print(" - DPS")
            data = sort_tool.get_DPS_sort(bottom_T, top_T)
            save_tool.save_DPS(data, T, T_range[2])

            print(" - fusillade_burn_probability")
            data = sort_tool.get_fusillade_burn_probability_sort(bottom_T, top_T)
            save_tool.save_fusillade_burn(data, T, T_range[2])

            print(" - burn_probability_per_s")
            data = sort_tool.get_burn_probability_per_s_sort(bottom_T, top_T)
            save_tool.save_burn_probability(data, T, T_range[2])

            print(" - bullet_speed")
            data = sort_tool.get_bullet_speed_sort(bottom_T, top_T)
            save_tool.save_bullet_speed(data, T, T_range[2])

            print(" - artillery_rotation")
            data = sort_tool.get_artillery_rotation_sort(bottom_T, top_T)
            save_tool.save_rotation(data, T, T_range[2])

            print(" - max_speed")
            data = sort_tool.get_max_speed_sort(bottom_T, top_T)
            save_tool.save_max_speed(data, T, T_range[2])

            print(" - rudder")
            data = sort_tool.get_rudder_sort(bottom_T, top_T)
            save_tool.save_rudder(data, T, T_range[2])
            print(" - end")

    write_json(sort_tool.get_dic())
