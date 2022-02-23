import math
from base_data import *

class SortTool:
    # Detect factors
    __camouflage_detect_factor = 0.97
    __commander_detect_factor = 0.9
    __commander_health_factor = 350
    __upgrade_detect_factor = 0.9

    # Fire system refered
    # https://wiki.wargaming.net/en/Ship:Fire#Fire_Reisistance
    # Fire Resistance Coefficient (at top hull)
    # FRC = [1.000, 0.9667, 0.9001, 0.8335, 0.7669, 0.7003, 0.6337, 0.5671, 0.5005]
    __FRC = 1.000
    # the effect of the Damage Control System Modification 1 upgrade 5% (0.05) with the upgrade, zero without
    __DCM1 = 0
    # the effect of the Fire Prevention skill: 10% (0.10) with the skill, zero without.
    __FP = 0
    # the Projectile Base Fire Chance (see above).
    # FCB = burn_probability
    # the effect of the IFHE commander skill: 50% (0.5) or one without the skill.
    __IFHE = 1
    # the effect of the Pyrotechnician commander skill: 0.01 with the skill, zero without.
    __PY = 0
    # the sum of the effects of the mounted Signals Victor
    __S = 0

    __pop_list = ['description', 'price_gold', 'ship_id_str', 'has_demo_profile', 'images', 'is_premium', 'price_credit', 'modules', 'modules_tree', 'upgrades', 'next_ships', 'mod_slots', 'is_special']
    __profile_pop_list = ['engine', 'torpedo_bomber', 'anti_aircraft', 'atbas', 'fighters', 'fire_control', 'weaponry', 'flight_control', 'armour', ]

    def __init__(self, origin_data) :
        self.data = origin_data
        self.__add_data()
        self.get_sort_data = [
            self.__get_detect_sort,
            self.__get_HP_sort,
            self.__get_fusillade_damage_sort,
            self.__get_DPS_sort,
            self.__get_fusillade_burn_probability_sort,
            self.__get_burn_probability_per_s_sort,
            self.__get_bullet_speed_sort,
            self.__get_artillery_rotation_sort,
            self.__get_max_speed_sort,
            self.__get_rudder_sort,
        ]

    def get_dic(self) :
        return self.data

    def __add_data(self) :
        ships = self.data['data']
        for ship_id in ships:
            ship_dic = ships[ship_id]

            # delete unused data
            for pop_key in self.__pop_list :
                ship_dic.pop(pop_key)
            for pop_key in self.__profile_pop_list :
                ship_dic['default_profile'].pop(pop_key)

            ### calculate best ditect distance by ship
            # get default distance
            detect_distance_by_ship = ship_dic['default_profile']['concealment']['detect_distance_by_ship']
            # camouflage and commander
            best_detect_distance_by_ship = detect_distance_by_ship * self.__camouflage_detect_factor * self.__commander_detect_factor

            tier = ship_dic['tier']
            if (8 <= tier) : # upgrade
                best_detect_distance_by_ship = my_round(best_detect_distance_by_ship * self.__upgrade_detect_factor, 3)

            best_detect_distance_by_ship = my_round(best_detect_distance_by_ship, 2)
            # store to dictionary
            ship_dic['default_profile']['concealment']['best_detect_distance_by_ship'] = best_detect_distance_by_ship

            ### calculate best health
            # get default health
            default_health = ship_dic['default_profile']['hull']['health']
            best_health = default_health + self.__commander_health_factor * tier
            # store to dictionary
            ship_dic['default_profile']['hull']['best_health'] = best_health

            ### damage and burn
            artillery = ship_dic["default_profile"]['artillery']
            shells = artillery['shells']
            shell_damage = 0
            shell_speed = 0
            burn_probability = 0
            one_hit_fire_chance = 0
            try :
                HE = shells['HE']
                shell_damage = HE['damage']
                shell_speed = HE['bullet_speed']
                burn_probability = HE['burn_probability']
                one_hit_fire_chance = self.__FRC * (1 - self.__DCM1) * (1 - self.__FP) * ((burn_probability / 100 * self.__IFHE) + self.__PY + self.__S)
            except:
                try :
                    AP = shells['AP']
                    shell_damage = AP['damage']
                    shell_speed = AP['bullet_speed']
                except:
                    try :
                        SAP = shells['SAP']
                        shell_damage = SAP['damage']
                        shell_speed = SAP['bullet_speed']
                    except:
                        pass
            ship_dic['default_profile']['artillery']['shell_damage'] = shell_damage
            ship_dic['default_profile']['artillery']['shell_bullet_speed'] = shell_speed

            sum_guns = 0
            slots = artillery["slots"]
            for slot in slots :
                    barrels = slots[slot]["barrels"]
                    guns = slots[slot]["guns"]
                    sum_guns += barrels * guns
            ship_dic['default_profile']['artillery']['sum_guns'] = sum_guns

            fusillade_damage = shell_damage * sum_guns
            ship_dic['default_profile']['artillery']['fusillade_damage'] = fusillade_damage

            shoot_per_s = 1 / artillery['shot_delay']
            if (9 <= tier) : # upgrade
                shoot_per_s *= 1 / 0.88
            ship_dic['default_profile']['artillery']['shoot_per_s'] = my_round(shoot_per_s, 3)

            damage_per_s = fusillade_damage * shoot_per_s
            ship_dic['default_profile']['artillery']['damage_per_s'] = my_round(damage_per_s, 2)

            ship_dic['default_profile']['artillery']['shell_burn_probability'] = burn_probability

            fusillade_no_fire_chance = (1 - one_hit_fire_chance) ** sum_guns
            ship_dic['default_profile']['artillery']['fusillade_burn_probability'] = my_round((1 - fusillade_no_fire_chance) * 100, 2)

            no_fire_chance_per_s = (1 - one_hit_fire_chance) ** (shoot_per_s * sum_guns)
            ship_dic['default_profile']['artillery']['burn_probability_per_s'] = my_round((1 - no_fire_chance_per_s) * 100, 2)

    def __get_target_tier_ships(self, T, T_range) :
        bottom_T = max(T - T_range, 1)
        top_T = min(T + T_range, 10)

        ships = self.data['data']
        # mask from T
        target_ship_dic = list()
        bottom_dic = dict()
        match_dic = dict()
        top_dic = dict()
        for ship_id in ships:
            ship_dic = ships[ship_id]

            tier = ship_dic['tier']
            if (tier < bottom_T) or (top_T < tier) :
                pass
            elif ("[" in ship_dic['name']) :
                pass
            elif (bottom_T <= tier) and (tier <= top_T) :
                match_dic[ship_id] = ship_dic
                if (tier <= T) :
                    top_dic[ship_id] = ship_dic
                if (T <= tier) :
                    bottom_dic[ship_id] = ship_dic

        target_ship_dic.append(bottom_dic)
        target_ship_dic.append(match_dic)
        target_ship_dic.append(top_dic)
        return target_ship_dic

    def __get_detect_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['concealment']['best_detect_distance_by_ship'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "   "
                concealment = ship['default_profile']['concealment']
                best_detect_distance = concealment['best_detect_distance_by_ship']
                detect_distance = concealment['detect_distance_by_ship']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(best_detect_distance) + "(" + str(detect_distance) + ")"])
            return_dic.append(data)
        return return_dic

    def __get_HP_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['hull']['best_health'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = "   "
                else :
                    brank = "    "
                hull = ship['default_profile']['hull']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(hull['best_health']) + "(" + str(hull['health']) + ")"])
            return_dic.append(data)
        return return_dic

    def __get_fusillade_damage_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['fusillade_damage'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                artillery = ship['default_profile']['artillery']
                fusillade_damage = artillery['fusillade_damage']
                shell_damage = artillery['shell_damage']
                sum_guns = artillery['sum_guns']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(fusillade_damage), str(shell_damage), str(sum_guns)])
            return_dic.append(data)
        return return_dic

    def __get_DPS_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['damage_per_s'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                artillery = ship['default_profile']['artillery']
                damage_per_s = artillery['damage_per_s']
                fusillade_damage = artillery['fusillade_damage']
                shoot_per_s = artillery['shoot_per_s']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(damage_per_s), str(fusillade_damage), str(shoot_per_s)])
            return_dic.append(data)
        return return_dic

    def __get_fusillade_burn_probability_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['fusillade_burn_probability'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                artillery = ship['default_profile']['artillery']
                fusillade_burn_probability = artillery['fusillade_burn_probability']
                burn_probability = artillery['shell_burn_probability']
                sum_guns = artillery['sum_guns']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(fusillade_burn_probability), str(burn_probability), str(sum_guns)])
            return_dic.append(data)
        return return_dic

    def __get_burn_probability_per_s_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['burn_probability_per_s'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                artillery = ship['default_profile']['artillery']
                burn_probability_per_s = artillery['burn_probability_per_s']
                burn_probability = artillery['shell_burn_probability']
                sum_guns = artillery['sum_guns']
                shoot_per_s = artillery['shoot_per_s']
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(burn_probability_per_s), str(burn_probability), str(sum_guns), str(shoot_per_s)])
            return_dic.append(data)
        return return_dic

    def __get_bullet_speed_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['shell_bullet_speed'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(ship['default_profile']['artillery']['shell_bullet_speed'])])
            return_dic.append(data)
        return return_dic

    def __get_artillery_rotation_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['artillery']['rotation_time'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(ship['default_profile']['artillery']['rotation_time'])])
            return_dic.append(data)
        return return_dic

    def __get_max_speed_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['mobility']['max_speed'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(ship['default_profile']['mobility']['max_speed'])])
            return_dic.append(data)
        return return_dic

    def __get_rudder_sort(self, T, T_range) :
        target_ship_dic = self.__get_target_tier_ships(T, T_range)

        return_dic = list()
        for dic in target_ship_dic :
            # get sorted data
            sort = sorted(dic.items(), key=lambda x : x[1]['default_profile']['mobility']['rudder_time'])
            data = list()
            for sorted_data in sort:
                ship = sorted_data[1]
                brank = ""
                if ship['tier'] == 10 :
                    brank = " "
                else :
                    brank = "  "
                data.append([ship['name'] + brank + "(" + str(ship['tier']) + ")", str(ship['default_profile']['mobility']['rudder_time'])])
            return_dic.append(data)
        return return_dic