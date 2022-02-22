import math

class SortTool:
    # Detect factors
    camouflage_detect_factor = 0.97
    commander_detect_factor = 0.9
    commander_health_factor = 350
    upgrade_detect_factor = 0.9

    # Fire system refered
    # https://wiki.wargaming.net/en/Ship:Fire#Fire_Reisistance
    # Fire Resistance Coefficient (at top hull)
    # FRC = [1.000, 0.9667, 0.9001, 0.8335, 0.7669, 0.7003, 0.6337, 0.5671, 0.5005]
    FRC = 1.000
    # the effect of the Damage Control System Modification 1 upgrade 5% (0.05) with the upgrade, zero without
    DCM1 = 0
    # the effect of the Fire Prevention skill: 10% (0.10) with the skill, zero without.
    FP = 0
    # the Projectile Base Fire Chance (see above).
    # FCB = burn_probability
    # the effect of the IFHE commander skill: 50% (0.5) or one without the skill.
    IFHE = 1
    # the effect of the Pyrotechnician commander skill: 0.01 with the skill, zero without.
    PY = 0
    # the sum of the effects of the mounted Signals Victor
    S = 0

    def __init__(self, origin_data) :
        self.data = origin_data
        self.add_data()

    def __my_round(self, value, digit = 0) :
        p = 10 ** digit
        return (value * p * 2 + 1) // 2 / p

    def add_data(self) :
        ships = self.data['data']
        for ship_id in ships:
            ship_dic = ships[ship_id]

                # calculate best ditect distance by ship
            # get default distance
            detect_distance_by_ship = ship_dic['default_profile']['concealment']['detect_distance_by_ship']
            # camouflage and commander
            best_detect_distance_by_ship = detect_distance_by_ship * self.camouflage_detect_factor * self.commander_detect_factor

            tier = ship_dic['tier']
            if (8 <= tier) : # upgrade
                best_detect_distance_by_ship = self.__my_round(best_detect_distance_by_ship * self.upgrade_detect_factor, 3)

            best_detect_distance_by_ship = self.__my_round(best_detect_distance_by_ship, 2)
            # store to dictionary
            ship_dic['default_profile']['concealment']['best_detect_distance_by_ship'] = best_detect_distance_by_ship

                # calculate best health
            # get default health
            default_health = ship_dic['default_profile']['hull']['health']
            best_health = default_health + self.commander_health_factor * tier
            # store to dictionary
            ship_dic['default_profile']['hull']['best_health'] = best_health

                # damage and burn
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
                one_hit_fire_chance = self.FRC * (1 - self.DCM1) * (1 - self.FP) * ((burn_probability / 100 * self.IFHE) + self.PY + self.S)
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
            ship_dic['default_profile']['artillery']['shoot_per_s'] = self.__my_round(shoot_per_s, 3)

            damage_per_s = fusillade_damage * shoot_per_s
            ship_dic['default_profile']['artillery']['damage_per_s'] = self.__my_round(damage_per_s, 2)

            ship_dic['default_profile']['artillery']['shell_burn_probability'] = burn_probability

            fusillade_no_fire_chance = (1 - one_hit_fire_chance) ** sum_guns
            ship_dic['default_profile']['artillery']['fusillade_burn_probability'] = self.__my_round((1 - fusillade_no_fire_chance) * 100, 2)

            no_fire_chance_per_s = (1 - one_hit_fire_chance) ** (shoot_per_s * sum_guns)
            ship_dic['default_profile']['artillery']['burn_probability_per_s'] = self.__my_round((1 - no_fire_chance_per_s) * 100, 2)

    def get_target_tier_ships(self, bottom_T, upper_T) :
        ships = self.data['data']
        # mask from T
        target_ship_dic = dict()
        for ship_id in ships:
            ship_dic = ships[ship_id]
            tier = ship_dic['tier']
            if (tier < bottom_T) or (upper_T < tier) :
                pass
            elif ("[" in ship_dic['name']) :
                pass
            else :
                target_ship_dic[ship_id] = ship_dic
        return target_ship_dic

    def get_detect_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['concealment']['best_detect_distance_by_ship'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(str(ship['default_profile']['concealment']['best_detect_distance_by_ship']) + "km  " + str(ship['default_profile']['concealment']['detect_distance_by_ship']) + "km  " + ship['name'] + " - " + str(ship['tier']))
        return sort

    def get_HP_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['hull']['best_health'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(str(ship['default_profile']['hull']['best_health']) + "  " + str(ship['default_profile']['hull']['health']) + "  " + ship['name'] + " - " + str(ship['tier']))
        return sort

    def get_fusillade_damage_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['fusillade_damage'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(str(ship['default_profile']['artillery']['fusillade_damage']) + "  " + str(ship['default_profile']['artillery']['shell_damage']) + "  " + str(ship['default_profile']['artillery']['sum_guns']) + "  " + ship['name'] + " - " + str(ship['tier']))
        return sort

    def get_DPS_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['damage_per_s'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(str(ship['default_profile']['artillery']['damage_per_s']) + "  " + str(ship['default_profile']['artillery']['shoot_per_s']) + "  " + str(ship['default_profile']['artillery']['fusillade_damage']) + "  " + ship['name'] + " - " + str(ship['tier']))
        return sort

    def get_fusillade_burn_probability_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['fusillade_burn_probability'])
        for sorted_data in sort:
            ship = sorted_data[1]
            fusillade_burn_probability = ship['default_profile']['artillery']['fusillade_burn_probability']
            print(ship['name'] + "  " + str(ship['default_profile']['artillery']['sum_guns']) + "  " + str(ship['default_profile']['artillery']['shell_burn_probability']) + "  " + str(ship['default_profile']['artillery']['fusillade_burn_probability']))
        return sort

    def get_burn_probability_per_s_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['burn_probability_per_s'])
        for sorted_data in sort:
            ship = sorted_data[1]
            burn_probability_per_s = ship['default_profile']['artillery']['burn_probability_per_s']
            print(ship['name'] + "  " + str(ship['default_profile']['artillery']['shoot_per_s']) + "  " + str(ship['default_profile']['artillery']['sum_guns']) + "  " + str(ship['default_profile']['artillery']['shell_burn_probability']) + "  " + str(ship['default_profile']['artillery']['burn_probability_per_s']))
        return sort

    def get_bullet_speed_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['shell_bullet_speed'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(ship['name'] + "  " + str(ship['default_profile']['artillery']['shell_bullet_speed']))
        return sort

    def get_max_speed_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['mobility']['max_speed'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(ship['name'] + "  " + str(ship['default_profile']['mobility']['max_speed']))
        return sort

    def get_rudder_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['mobility']['rudder_time'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(ship['name'] + "  " + str(ship['default_profile']['mobility']['rudder_time']))
        return sort

    def get_artillery_rotation_sort(self, bottom_T, upper_T) :
        target_ship_dic = self.get_target_tier_ships(bottom_T, upper_T)

        # get sorted data
        sort = sorted(target_ship_dic.items(), key=lambda x : x[1]['default_profile']['artillery']['rotation_time'])
        for sorted_data in sort:
            ship = sorted_data[1]
            print(ship['name'] + "  " + str(ship['default_profile']['artillery']['rotation_time']))
        return sort