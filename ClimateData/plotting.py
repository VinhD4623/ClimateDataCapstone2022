import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import pandas as pd

'''
TODO
functions to implement
- Plot per county data
- Plot per state data
- Plot per country data (Eventually)

'''
csv_path = './data/raw/climdiv-avgtmp.csv'
headers = ['Codes', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def get_test_data():
    df = pd.read_csv(csv_path, delimiter=',', nrows=127, header=None)
    df.columns = headers

    print(df.head())

    x_dates_format = []
    x_data = []
    for i in df['Codes']:
        for j in range(1,13):
            x_dates_format.append(str(i)[-4:] + '-' + str(j))
            x_data.append(int(str(i)[-4:]) + (j-1) / 12)

    y_data = []
    for i, row in df.head(127).iterrows():
        for j in row[1:]:
            y_data.append(j)

    return [x_data, y_data, x_dates_format]
 

def plot(ptype, df, plot_vars_map):

    x_data, y_data = process_data(df, plot_vars_map['process_type'], plot_vars_map['range'])
    if ptype == 'scatter':
        pass
    elif ptype == 'poly':
        pass
    elif ptype == 'scatter_poly':
        scatter_poly(x_data, y_data, plot_vars_map['degree'])
    elif ptype == 'us_heatmap':
        pass
    else:
        return 'Invalid plot type!'


def process_data(df, process_type, data_range):
    x_data = []
    y_data = []

    if process_type == 'months':
        for i in df.iloc[:,0]:
            for j in data_range:
                x_data.append(int(str(i)[-4:]) + j / 12)

        for i, row in df.iterrows():
            for j in row[1:]:
                y_data.append(j)
    return x_data, y_data
 
def scatter_poly(x, y, deg):
    #ordered_coefs = [-i for i in coefs][::-1]
    #d, c, b, a = poly.polyfit(x, y, deg)
    #fiteq = lambda x: a * x ** 3 + b * x ** 2 + c * x + d

    coeffs = poly.polyfit(x, y, deg)
    def fiteq(x, idx=0):
        if idx == deg:
            return coeffs[idx] * x ** (idx)
        else:
            return coeffs[idx] * x ** (idx) + fiteq(x, idx+1)

    x_fit = np.linspace(min(x), max(x), 1000)
    y_fit = fiteq(x_fit)

    # TODO: If you look closely at the graph, 
    # it appears there's an issue with the position of the scatter plot points
    fig, ax1 = plt.subplots()
    ax1.plot(x_fit, y_fit, color='r', alpha=0.5, label='Polynomial fit')
    ax1.scatter(x, y, s=4, color='b', label='Data points')
    ax1.set_title(f'Polynomial fit example deg={deg}')
    ax1.legend()
    plt.show()
    plt.scatter()

def scatter_plot(x, y):
    x_data = np.array(x)
    y_data = np.array(y)

    y_axis = np.arange(0, 120, 10)
    x_axis = np.arange(x_data[0], x_data[-1], 2)

    plt.figure(figsize=(20,5))
    plt.xticks(x_axis)
    plt.yticks(y_axis)
    plt.scatter(x_data, y_data)
    plt.show()


if __name__ == '__main__':
    x, y, x_dates = get_test_data()
    degree = 30
    scatter_poly(x, y, degree)


'''
Sample data 
01001021895,44,38.2,55.5,64.1,70.6,78.3,80.4,80.4,79,61.4,54.4,45.3
01001021896,44.3,49,54,69.3,76.8,78,81.7,83.1,77.9,64.7,58,47.3
01001021897,43.7,52.3,61.3,63,70,82.4,82.4,79.6,76.6,67.4,54.9,48.2
01001021898,50.1,46.8,60.1,59.6,75,81.5,80.8,79.2,76.2,62.1,50.2,44.2
01001021899,44.6,41.5,56.6,62.3,76.7,81,81,81.5,74.3,66.6,55.7,45.3
01001021900,43.9,45.1,53.8,65.3,71.7,76.4,80.6,81.5,78.1,69.3,56.1,48.3
01001021901,48.2,44.3,54.3,59.3,71.1,79.2,82.9,79.6,73.2,63.1,49.6,42.7
01001021902,44.6,41.9,56.1,62.9,76,82.5,84.2,83.6,74.9,63.5,58.4,45.6
01001021903,44.8,49.3,60.7,61.6,70,74.4,81.1,81.7,73.5,63.9,52.9,40.8
01001021904,43,51.2,60,61.5,71.1,79.1,79.6,79.1,77.3,65.7,54.6,46.7
01001021905,40.9,40.6,60,64.3,75.2,80.5,81.1,80,77.1,64.5,57,43.2
01001021906,47,46,51.8,64.7,69.8,79.6,80.2,81.3,79.1,61,55.9,50.1
01001021907,54.6,50.4,65.1,59.7,69,76.6,81.7,80.9,75.8,64,51.5,45.9
01001021908,44.8,44.4,63.7,68.4,72.2,79,81.2,80.4,74.8,60.5,57.5,51.5
01001021909,50.8,50.6,56.9,63.8,69.5,79,81.3,81.7,76.3,63.5,59.5,41.9
01001021910,46.5,47.1,61.2,62.6,70,76.4,79.2,80.2,77.3,67.3,51.7,42.4
01001021911,50.6,55.6,58.7,64.3,72.8,81.2,78.8,79.8,80.5,69.4,51.2,50.2
01001021912,41,45.7,53.6,65.3,72.5,76.1,80.5,80,77.6,66.4,50.8,47.6
01001021913,51.5,47.4,56.4,62.2,71.6,78.7,81.9,80.9,73,60.6,56,48
01001021914,46.7,45.4,50.4,64.2,71.9,83.3,81.8,79.8,73.3,63.8,52.8,44.2
01001021915,43.6,48.7,47.4,64.5,74.9,78.9,81.4,80.4,76.8,66.7,57,46.1
01001021916,52.2,47.1,54.6,62.4,73.6,78.6,79.6,80.3,74.1,65,54.7,47.5
01001021917,50.8,49.6,57.9,64.4,66.2,79.1,80.5,79.1,74,58.8,51.5,40.8
01001021918,39.7,55,63.3,61.9,73.2,80.3,78.7,80.9,71,69.6,54.1,50
01001021919,45.4,48.9,57.9,63.2,69.6,79,80.4,79.5,75.5,75.5,58,47.7
01001021920,48.5,46.7,52.5,63.3,70.7,77.4,80.3,78.6,77.6,64.3,51.4,44.9
01001021921,50.6,50.7,64.3,62.6,70.7,81.2,81.9,81.3,81.3,63.5,58.6,51.2
01001021922,47.7,55.2,56.3,67.8,72.5,79.2,80.7,79.9,78.2,65.7,58.4,54.5
01001021923,51.9,48.7,55.5,64.3,69.9,77.5,78.8,79.4,76.6,63.7,51.8,54.8
01001021924,42.4,48.4,52,63.4,67.7,79.9,80.1,81.9,73,64.4,56.3,49.6
01001021925,48.2,53,58.5,68,70.3,81,82,80.5,83.4,65.6,52.8,45
01001021926,45.2,51.4,50.1,61.7,70.4,77.8,79.3,81.1,79.3,66.2,51,51.7
01001021927,49.8,59.5,57,68.4,73,79,81.4,79.1,78,67.2,60.3,47.4
01001021928,45.1,48.9,56.6,60.4,69.8,76.5,81.1,81.5,74.6,68.7,53.9,46.9
01001021929,50.5,47.2,60.6,67.7,72.2,77.7,80.4,80.8,75.5,63.2,55.5,43.8
01001021930,46.6,54.5,53,65.3,73.1,77.1,84.4,79.4,76.7,62,54.4,44
01001021931,45.2,50,50.6,61.8,68.3,79.4,81.7,78.2,79.3,67.9,60.5,55
01001021932,52.9,58.2,52.2,65,70,79,83,81,75.6,63.1,50.3,50.9
01001021933,52.8,50.2,56.5,62.9,76.6,78.5,79,80.3,79.1,66.3,54.6,56.1
01001021934,49.9,44.4,54.3,64.3,71.8,80.2,81.9,80.2,74.4,66.5,56.5,45.2
01001021935,47.9,49.4,61.2,65,72.8,77.4,81.6,81.5,74.4,66.9,56.4,39.6
01001021936,44.8,46.4,59.5,62.4,73,81,82,80.8,78,67,53.3,49.7
01001021937,58.7,48.4,53.4,63.4,72.4,80.4,80.2,81.1,73.4,62.6,51,46.6
01001021938,47.1,54.7,63.1,63.1,72.3,77.5,80.9,81.5,74.8,65.2,55.6,46.5
01001021939,50.1,53.3,59.2,62.7,71.2,79.4,81,78.2,76.8,65.9,52.5,48.6
01001021940,34.2,45.4,54.7,62,68.7,76.9,78.7,80.2,73.1,65,54.7,50.6
01001021941,47.4,43.8,50.7,65.5,73.2,78.6,80.7,80.6,78.3,71.3,54,49.2
01001021942,44,44.9,54.9,64.4,71.2,78,80.8,78.2,73.2,65,56.8,49.1
01001021943,49.3,50.2,55,64.2,73.7,81.1,81.7,81.4,72.3,62,51.7,46.6
01001021944,46.8,55.6,57.4,62.3,72.3,80.7,79.7,78.8,76.1,63.5,54.7,46
01001021945,46.4,53.1,63.9,66.4,69.6,79.9,81,80.9,77.9,63.1,56.6,41.3
01001021946,48.1,50.8,60.8,66.7,71,76.3,79.6,78,72.9,64.4,60.7,51.2
01001021947,50,42.7,50.7,65.3,70.6,77.6,78.1,81.2,77.2,70,52.9,47.8
01001021948,39.7,52,58.9,67.5,72.1,79.5,81.2,79,73.2,61.4,56.3,50.2
01001021949,53.4,53.6,53.8,62.4,73,77.8,81.4,79.8,73.5,70,52.4,48.5
01001021950,60.3,54.7,53,60.3,74.6,78.7,79,78.4,73,66.8,49.3,41.5
01001021951,47.8,50.3,57.1,62.2,70.8,79.6,82.2,83,76.8,66.7,49.1,50.2
01001021952,53.6,51.8,54.2,61.8,72.2,82.4,83.4,80.6,73.4,58.4,52.4,45.6
01001021953,49.3,49.5,58.5,61.3,74.6,80.7,80.5,79.9,74,65.7,53.1,45.4
01001021954,48,52.6,55.2,68.1,66.9,80.2,83.1,84.1,78.4,65.7,51.4,44.9
01001021955,44.8,50.2,59.8,66.8,73.9,73.9,80.7,80.8,77.3,62.3,53,46.8
01001021956,43.1,54.9,55.5,61.8,73.8,77,80.6,81.1,72.8,64.9,50.8,54.2
01001021957,49.9,58.1,53.4,65.5,72.3,79.2,80.2,80,74.1,59.6,55.9,47.4
01001021958,40.2,39,51.9,63.6,71.4,79.3,79.5,80.4,76.2,63.3,56.8,43.7
01001021959,44.4,50.8,53.1,63.3,73.8,77.9,81.3,81.5,75.2,67,52.2,47.3
01001021960,45.2,46.4,46.7,65.1,68.4,78.1,82.3,80.1,75.8,66.2,54.1,42.9
01001021961,40,52.8,58,59.6,68.2,74.7,78.9,78.1,74.9,62.4,56.1,47.4
01001021962,43.4,56.8,52.2,60.8,75.7,77.9,81.8,81,75.2,66,51.5,44.2
01001021963,40.9,43.1,59.4,67.2,72.9,78.1,78.8,80.5,73.6,65.5,53.5,38.5
01001021964,42.7,43.1,54.8,65.6,71.6,79.4,78.3,78.7,74.7,60.3,56.7,48.6
01001021965,46.9,46.7,52.2,65.9,73.3,76.5,79.7,78.9,75.2,63,57.6,46.8
01001021966,41.3,47.4,53.7,64.7,70,74.3,81.5,78.2,73.6,62.5,54.9,46.6
01001021967,45.7,45.7,59.5,68.4,69.8,76.4,76.4,76,69,61,51.6,51
01001021968,42.8,41.2,52.6,64.2,69.6,78.4,79.2,79.9,73.3,64.3,51,43.1
01001021969,44.5,47.1,48.8,64.5,70.7,78.3,81.7,77.1,72.3,64.8,51,43.9
01001021970,38.5,45.1,53.6,66.2,71.2,75.6,80.1,79.4,77.7,65,49.8,49.8
01001021971,46.5,46.7,50.6,61.7,66.7,78.4,78.2,78,75.7,68.1,52.1,56.2
01001021972,50.1,48.1,55.8,64,69.4,76,78.4,79.6,77.6,64.1,51,50.4
01001021973,44,45.3,60.6,60.7,68.5,77,80.3,78.3,77.2,67,57.4,46.7
01001021974,56.3,48.2,60.7,62.6,73,74.3,79.3,78.2,71.7,60.9,53.1,47.4
01001021975,50,51.6,55,61.1,73,76.3,78,79.3,71.3,65.2,55.3,46.2
01001021976,41.5,54.2,59.1,63.5,66,75.4,79.1,77.5,73,58.4,46.4,42.4
01001021977,34.3,46.2,58.2,65.8,73.3,81,81.9,80.1,76.9,61.8,57.4,46.4
01001021978,37.2,40.6,52.2,64.5,71.4,78.7,81.3,79.6,77.7,62.8,59.6,47.7
01001021979,39.1,44.7,56.8,64.5,70.4,75.6,79.3,79.1,73.6,63,53.7,46.8
01001021980,47.8,44.6,53.7,61.2,70.9,78.4,82.5,81.7,78.9,60.7,52.2,45.8
01001021981,40.4,48.1,52.7,67.4,68.4,81.2,81.5,78.4,72.1,62.2,55.3,43.6
01001021982,43.8,49.4,59.4,61,72.6,77.1,80.3,79.6,73.4,65.2,56,53.8
01001021983,42.9,47.4,52.7,58.5,69.4,75.2,81.1,81.5,72.7,64.8,54,43
01001021984,41.3,49.1,54.8,61.8,69.5,77.8,79,77.8,73.6,70.8,52.8,56.3
01001021985,38.2,47,60,64.7,71.8,78.5,79.4,79.3,73.7,68.3,61.5,42.2
01001021986,44,52.2,56,63.2,72.5,79.9,83,79.3,77.5,65.1,59.8,46.3
01001021987,43.9,49.6,56.5,61.7,74,77.5,81,82.1,74.6,59,56.1,51.9
01001021988,41.6,46.3,55.4,63.4,69.3,77.7,79.1,80.6,75.2,60.3,57.3,47.4
01001021989,50.8,49.2,57.9,61.8,69.9,77,79.5,79.8,73.8,63,54,39.5
01001021990,50.2,55.5,58.8,62,70.2,78.8,80.4,82.2,77.7,65.6,57,52.2
01001021991,46.7,52.1,57.6,66.8,74.2,77.3,81.1,79.4,75.2,65.3,51,50.2
01001021992,44.6,52.5,56,61.8,68.6,75.5,80.6,76.7,74.4,62.7,52.6,47.6
01001021993,49.7,46.9,52.7,59.6,69.8,78.7,82.9,80.6,75.2,63.6,51.5,46
01001021994,41.7,51.6,56.9,65.2,70,78.4,78.2,78,73.1,64.5,58.9,50.9
01001021995,46.4,49.2,59.8,64.2,73.7,76.1,82.5,82.7,75.2,64.4,50.2,45.3
01001021996,44,48.4,52,61,73.7,77.4,80,78.7,73.1,63.5,53.7,49.6
01001021997,47,51.7,62.4,59.7,68,74.9,80.9,78.6,75.6,63.9,50.7,45.3
01001021998,48.5,50,53.9,62.4,74.6,81.3,82.5,80.6,78.2,67.5,58.6,52.5
01001021999,50.5,52.7,53.9,67.6,70.2,77.3,81.2,82.6,73.5,64.3,56.4,47.9
01001022000,47.9,53,59.8,60.7,75.1,78.3,83,81.2,74.4,65.4,53.4,39.8
01001022001,42.2,53.5,52.4,64.9,71.6,76.6,80.1,79.1,72.6,61.2,59.5,51.4
01001022002,47.6,46.6,55.7,67.4,71.4,77.8,80.9,80.5,78.2,68.7,51.6,45.8
01001022003,41,49.4,58.4,64.1,72.8,76.5,79.1,80,73.7,64,58.3,44.5
01001022004,45,46.1,60.1,62.3,74,77.9,80.4,77.2,74.8,69.4,58.2,46.2
01001022005,49.9,52.2,54,61.5,69,77.4,80.8,80.7,78,64.3,56.3,44.2
01001022006,52,47.2,57,68,71.2,78.8,82.7,82.8,73.9,62.8,53.2,50
01001022007,47.3,46.2,61,61.2,72,80.2,80.1,85.4,76.7,67.4,54.1,51.5
01001022008,43.4,49.8,56.1,63.9,71.6,79.7,80.6,79.1,75.5,62.9,51.8,51.1
01001022009,46.5,49.4,58.3,62.3,72.6,80.1,78.9,78.8,76,63.6,53.3,45.5
01001022010,41.5,41.6,51.9,64.7,74.7,81.9,83.4,83.7,78.4,65.1,55.5,40.7
01001022011,41.5,50.3,58.6,66.5,70.3,82.1,82.5,83.3,73.6,61.6,55.8,49.8
01001022012,50.5,53.4,65.2,66.3,74.3,77.3,82.1,78.9,73.8,63.2,51.7,51.2
01001022013,51.1,48.6,50.3,63.4,69.4,79.1,78.3,78.6,75.6,65.7,52.7,49.1
01001022014,37.6,48.7,53.5,63.4,70.5,78.8,79.5,80.6,77.3,66.1,48.2,51.2
01001022015,44.7,42.8,59.1,67.4,72.9,79.7,82.4,80.4,75.4,66,60.2,57.5
01001022016,44.1,50.7,60.3,64.4,71.7,79.7,82.4,82.8,79.5,68.9,57.9,51
01001022017,53.1,56.3,59.3,68.2,70.4,76.4,81.3,79.5,75.2,66.7,55.5,47.3
01001022018,40.6,58.7,56.2,60.6,75,80.4,81.6,80,80.5,68.1,50.8,49.4
01001022019,47,58.7,56.4,64.6,75.5,79.4,81.7,82.2,82,69.5,51.8,52.1
01001022020,50.7,52.5,65.2,63.4,70.2,78.2,82.2,81.6,76,68.4,59.6,46.8
01001022021,48.2,49.2,61.2,62.8,71,78.2,80.3,81.4,75.1,68.4,53.6,57.4
'''