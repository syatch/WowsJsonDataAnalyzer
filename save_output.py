import matplotlib
import matplotlib.pyplot as plt
import colorsys
from statistics import mean
from base_data import *

class SaveTool:
    def __init__(self) :
        self.__h_start = 0.3
        self.__h_length = 0.4
        self.__s = 0.9
        self.__v = 1.0
        self.__class_num = 10
        self.__highlight__fill_h = 0.155
        self.__highlight__border_h = 0.1
        self.__highlight_color = colorsys.hsv_to_rgb(self.__highlight__fill_h, self.__s, self.__v)
        self.__highlight_border = colorsys.hsv_to_rgb(self.__highlight__border_h, self.__s, self.__v)

    def __remove_sub_data(self, data) :
        delete_num  = data.find(")") - data.find("(") + 1
        return data[0:-delete_num].rstrip()

    def __get_min_max_data(self, data) :
        min_row_data = data[0][1]
        min_row_data = float(self.__remove_sub_data(min_row_data))
        max_row_data = data[len(data) - 1][1]
        max_row_data = float(self.__remove_sub_data(max_row_data))
        return (min_row_data, max_row_data)

    def __get_color_map(self, data) :
        # create color
        colors = list()
        (min_row_data, max_row_data) = self.__get_min_max_data(data)
        for row_data in data :
            order_data = float(self.__remove_sub_data(row_data[1]))
            h = self.__h_start + self.__h_length * (order_data - min_row_data) / (max_row_data - min_row_data)
            color = colorsys.hsv_to_rgb(h, self.__s, self.__v)
            colors.append(color)
        return colors

    def __save_table(self, labels, data, save_path, ship_name = "") :
        matplotlib.rc('font', family='Noto Sans CJK JP')

        colors = self.__get_color_map(data)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Draw table
        the_table = plt.table(cellText = data,
                            colColours = (["gainsboro"]) * len(labels),
                            rowColours = colors,
                            colWidths = [0.1] * len(labels),
                            colLabels = labels,
                            loc = 'center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(24)
        the_table.scale(10, 5)

        # if ship_name is not null, highlight ship row
        if ship_name :
            count = 0
            found = False
            for cell in the_table.get_children() :
                cell_text = self.__remove_sub_data(cell.get_text().get_text())
                if (cell_text == ship_name) :
                    found = True
                if found :
                    if count < len(labels) :
                        cell.set_facecolor(self.__highlight_color)
                        cell.set_edgecolor(self.__highlight_border)
                        count += 1
                    else :
                        break

        # Removing ticks and spines enables you to get the figure only with table
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
        for pos in ['right','top','bottom','left']:
            plt.gca().spines[pos].set_visible(False)

        plt.savefig('output/' + save_path, bbox_inches='tight', pad_inches=0.05)
        plt.close()

    def __get_hist_class(self, data) :
        (min_row_data, max_row_data) = self.__get_min_max_data(data)
        class_freq = list()
        class_freq.append(min_row_data)
        width = (max_row_data - min_row_data) / 10
        for i in range(1, self.__class_num + 1) :
            class_freq.append(my_round(min_row_data + width * i, 2))

        return class_freq

    def __save_hist(self, labels, data, save_path, ship_name = "") :
        matplotlib.rc('font', family = 'Noto Sans CJK JP')

        data_value = list()
        for row_data in data :
            order_data = float(self.__remove_sub_data(row_data[1]))
            data_value.append(order_data)

        class_freq = self.__get_hist_class(data)

        n, bins, patches = plt.hist(data_value, bins = class_freq, color = 'deepskyblue', edgecolor = 'k', fill = True)

        plt.axvline(mean(data_value), color = 'red', linestyle = 'dashed', linewidth = 2)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])

        data_width = list()
        for i in range(self.__class_num) :
            data_width.append([str(class_freq[i]) + " - " + str(class_freq[i + 1]), int(n[i])])

        the_table = plt.table(cellText = data_width,
                    colColours = (["gainsboro"]) * len(labels),
                    colLabels = labels,
                    colWidths = [0.15, 0.1],
                    loc = 'right'
                    )
        the_table.scale(1.5, 2.3)


        if ship_name :
            for row_data in data :
                row_ship_name = self.__remove_sub_data(row_data[0])
                if ship_name == row_ship_name :
                    for i in range(len(bins) - 1) :
                        value = float(self.__remove_sub_data(row_data[1]))
                        if (bins[i] <= value) and (value < bins[i+1]) :
                            patches[i].set_facecolor(self.__highlight_color)
                            break
                    break

        plt.savefig('output/' + save_path, facecolor="azure", edgecolor="k", bbox_inches = 'tight', pad_inches = 0.05)
        plt.close()

    def save_table(self, data, T, id_list, data_type, ship_name = "") :
        index = 0
        for id in id_list :
            labels = TableLabel.labels[data_type]
            if ship_name :
                ship_type = "/" + ship_name
            else :
                ship_type = "/none"
            save_path = str(T) + ship_type + SaveDirectory.directory[data_type] + 'table_' + str(id)
            self.__save_table(labels, data[index], save_path, ship_name)
            index += 1

    def save_hist(self, data, T, id_list, data_type, ship_name = "") :
        index = 0
        for id in id_list :
            labels = HistLabel.labels[data_type]
            if ship_name :
                ship_type = "/" + ship_name
            else :
                ship_type = "/none"
            save_path = str(T) + ship_type + SaveDirectory.directory[data_type] + 'hist_' + str(id)
            self.__save_hist(labels, data[index], save_path, ship_name)
            index += 1