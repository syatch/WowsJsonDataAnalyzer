import json
from get_sort import *

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

data_path = 'data/Destroyer.json'

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

def save_table(labels, data, save_path) :
    matplotlib.rc('font', family='Noto Sans CJK JP')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Draw table
    the_table = plt.table(cellText = data,
                        colWidths = [0.1] * len(labels),
                        colLabels = labels,
                        loc = 'center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(24)
    the_table.scale(10, 5)

    # Removing ticks and spines enables you to get the figure only with table
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)

    plt.savefig('output/' + save_path, bbox_inches='tight', pad_inches=0.05)

if __name__ == "__main__" :
    data = read_json()
    sort_tool = SortTool(data)
    # check_data(data)
    Tier = [9]
    for T in Tier :
        bottom_T = max(T - 2, 1)
        top_T = min(T + 2, 10)

        data = sort_tool.get_detect_sort(bottom_T, top_T)
        labels = ['艦名', '最良海面発見距離(標準)\n[km]']
        save_path = str(T) + '/detect_distance/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_HP_sort(bottom_T, top_T)
        labels = ['艦名', '最大体力(標準)\n[points]']
        save_path = str(T) + '/HP/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_fusillade_damage_sort(bottom_T, top_T)
        labels = ['艦名', '斉射火力\n[damage/shot]', '単発火力\n[damage/shell]', '門数\n[guns]']
        save_path = str(T) + '/fusillade_damage/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_DPS_sort(bottom_T, top_T)
        labels = ['艦名', '1秒あたりの貫通ダメージ\n[damage/s]', '斉射火力\n[damage/shot]', '1秒あたり射撃回数\n[times/s]']
        save_path = str(T) + '/DPS/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_fusillade_burn_probability_sort(bottom_T, top_T)
        labels = ['艦名', '斉射あたり火災発生率\n[%/shot]', '単発火災発生率\n[%/shell]', '門数\n[guns]']
        save_path = str(T) + '/fusillade_burn_probability/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_burn_probability_per_s_sort(bottom_T, top_T)
        labels = ['艦名', '1秒あたり火災発生率 [%/s]', '単発火災発生率\n[%/shell]', '門数\n[guns]', '1秒あたり射撃回数\n[times/s]']
        save_path = str(T) + '/burn_probability_per_s/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_bullet_speed_sort(bottom_T, top_T)
        labels = ['艦名', '砲弾初速 [m/s]']
        save_path = str(T) + '/bullet_speed/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_artillery_rotation_sort(bottom_T, top_T)
        labels = ['艦名', '主砲旋回時間 []']
        save_path = str(T) + '/artillery_rotation/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_max_speed_sort(bottom_T, top_T)
        labels = ['艦名', '最大速力 [kt]']
        save_path = str(T) + '/max_speed/data'
        save_table(labels, data, save_path)

        data = sort_tool.get_rudder_sort(bottom_T, top_T)
        labels = ['艦名', '転舵所要時間 [s]']
        save_path = str(T) + '/rudder/data'
        save_table(labels, data, save_path)

    write_json(sort_tool.get_dic())
