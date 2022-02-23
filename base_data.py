from enum import IntEnum

class DataType(IntEnum) :
    DETECT = 0,
    HP = 1,
    FUSILLADE_DAMAGE = 2,
    DPS = 3,
    FUSILLADE_BURN_PROBABILITY = 4,
    BURN_PROBABILITY_PER_S = 5,
    BULLET_SPEED = 6,
    ARTILLERY_ROTATION = 7,
    MAX_SPEED = 8,
    RUDDER = 9,

class TableLabel :
    labels = [
        ['艦名\n[Tier]', '最良海面発見距離(標準)\n[km]'],
        ['艦名\n[Tier]', '最大体力(標準)\n[points]'],
        ['艦名\n[Tier]', '斉射火力\n[damage/shot]', '単発火力\n[damage/shell]', '門数\n[guns]'],
        ['艦名\n[Tier]', '1秒あたりの貫通ダメージ\n[damage/s]', '斉射火力\n[damage/shot]', '1秒あたり射撃回数\n[times/s]'],
        ['艦名\n[Tier]', '斉射あたり火災発生率\n[%/shot]', '単発火災発生率\n[%/shell]', '門数\n[guns]'],
        ['艦名\n[Tier]', '1秒あたり火災発生率\n[%/s]', '単発火災発生率\n[%/shell]', '門数\n[guns]', '1秒あたり射撃回数\n[times/s]'],
        ['艦名\n[Tier]', '砲弾初速\n[m/s]'],
        ['艦名\n[Tier]', '主砲旋回時間\n[]'],
        ['艦名\n[Tier]', '最大速力\n[kt]'],
        ['艦名\n[Tier]', '転舵所要時間\n[s]'],
    ]

class HistLabel :
    labels = [
        ['隠蔽', '頻度'],
        ['HP', '頻度'],
        ['斉射火力', '頻度'],
        ['1秒あたりの貫通ダメージ', '頻度'],
        ['斉射あたり火災発生率\n[%/shot]', '頻度'],
        ['1秒あたり火災発生率\n[%/s]', '頻度'],
        ['砲弾初速\n[m/s]', '頻度'],
        ['主砲旋回時間\n[]', '頻度'],
        ['最大速力\n[kt]', '頻度'],
        ['転舵所要時間\n[s]', '頻度'],
    ]

class SaveDirectory :
    directory = [
        '/detect_distance/',
        '/HP/',
        '/fusillade_damage/',
        '/DPS/',
        '/fusillade_burn_probability/',
        '/burn_probability_per_s/',
        '/bullet_speed/',
        '/artillery_rotation/',
        '/max_speed/',
        '/rudder/',
    ]

def my_round(value, digit = 0) :
    p = 10 ** digit
    return (value * p * 2 + 1) // 2 / p