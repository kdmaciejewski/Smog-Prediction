import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
from meteostat import Hourly, Stations, Point


#funkcja mapująca
def map_func(df, a, b, c, d, e, f, g):
    return a*df['Month'] + b*df['Day'] + c*df['Time'] + d*df['temp'] + e*df['rhum'] + f*df['Yest'] + g

#liczenie parametrów funkcji
def parameters(func):
    df = pd.read_csv('airday.csv', sep=';', encoding='cp1250')
    df = df.fillna(df.mean())  # uzupełnienie braków średnimi wartościami
    df2 = pd.read_csv('airpollution1.csv', sep=';', encoding='cp1250')
    df['Date'] = df2['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'],format='%d.%m.%Y %H')

    #pobieranie danych pogodowych wrocławia
    start = datetime(2017, 1, 1)
    end = datetime(2017, 12, 31, 23, 59)
    wroc = Point(51.0636, 17.0120, 70)
    datamet = Hourly(wroc, start, end)
    datamet = datamet.fetch()

    df.index = datamet.index
    df[['temp', 'rhum']] = datamet[['temp', 'rhum']].astype(float)

    params, _ = curve_fit(func, xdata=df[['Month','Day','Time','Yest','temp','rhum']], ydata=df['Air'])
    mse = mean_squared_error(df['Air'], map_func(df[['Month','Day','Time','Yest','temp','rhum']],
                                                 params[0], params[1], params[2], params[3],
                                                 params[4], params[5], params[6]))
    #print(params)
    print(f'Błąd średniokwadratowy: {mse}')

    plt.plot(df['Date'], df['Air'])
    plt.plot(df['Date'], map_func(df[['Month','Day','Time','Yest','temp','rhum']],
                                  params[0], params[1], params[2], params[3],
                                  params[4], params[5], params[6]), label="curve fit")

    plt.plot(grid=True, figsize=(25, 15))
    plt.title("Jakość Powietrza")
    plt.xlabel("Data")
    plt.ylabel("Stężenie pyłów PM2.5 [Âµg/m3]")
    plt.legend()
    plt.show()
    return params

# def predict(params, day, month, time):
#     res = params[0] * month + params[1] * day + params[2] * time + params[3]
#     print(f'Przewidywana jakość powietrza w dniu {day}.{month}: {res}')
#     if res > 50:
#         print('Uwaga! Jakość powietrza jest zła, zostań w domu!')
#     elif res > 70:
#         print('Uwaga! Jakość powietrza jest zła, na dwór wychodź tylko w masce ochronnej')


if __name__ == '__main__':
    parameters(map_func)

