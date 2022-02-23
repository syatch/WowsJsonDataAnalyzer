import matplotlib
import matplotlib.pyplot as plt

class SaveTool:

    def save_table(self, labels, data, save_path) :
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
        plt.close()

    def save_detect(self, data, T, id) :
        labels = ['艦名(Tier)', '最良海面発見距離(標準)\n[km]']
        save_path = str(T) + '/detect_distance/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_health(self, data, T, id) :
        labels = ['艦名(Tier)', '最大体力(標準)\n[points]']
        save_path = str(T) + '/HP/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_fusillade_damage(self, data, T, id) :
        labels = ['艦名(Tier)', '斉射火力\n[damage/shot]', '単発火力\n[damage/shell]', '門数\n[guns]']
        save_path = str(T) + '/fusillade_damage/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_DPS(self, data, T, id) :
        labels = ['艦名(Tier)', '1秒あたりの貫通ダメージ\n[damage/s]', '斉射火力\n[damage/shot]', '1秒あたり射撃回数\n[times/s]']
        save_path = str(T) + '/DPS/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_fusillade_burn(self, data, T, id) :
        labels = ['艦名(Tier)', '斉射あたり火災発生率\n[%/shot]', '単発火災発生率\n[%/shell]', '門数\n[guns]']
        save_path = str(T) + '/fusillade_burn_probability/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_burn_probability(self, data, T, id) :
        labels = ['艦名(Tier)', '1秒あたり火災発生率 [%/s]', '単発火災発生率\n[%/shell]', '門数\n[guns]', '1秒あたり射撃回数\n[times/s]']
        save_path = str(T) + '/burn_probability_per_s/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_bullet_speed(self, data, T, id) :
        labels = ['艦名(Tier)', '砲弾初速 [m/s]']
        save_path = str(T) + '/bullet_speed/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_rotation(self, data, T, id) :
        labels = ['艦名(Tier)', '主砲旋回時間 []']
        save_path = str(T) + '/artillery_rotation/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_max_speed(self, data, T, id) :
        labels = ['艦名(Tier)', '最大速力 [kt]']
        save_path = str(T) + '/max_speed/data_' + str(id)
        self.save_table(labels, data, save_path)

    def save_rudder(self, data, T, id) :
        labels = ['艦名(Tier)', '転舵所要時間 [s]']
        save_path = str(T) + '/rudder/data_' + str(id)
        self.save_table(labels, data, save_path)