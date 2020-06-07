import csv
import matplotlib
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 8]


def readIsothermFromCSVFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return readIsothermFromString(lines)


def readIsothermFromString(s):
    reader = csv.reader(s)
    data = []
    for x, y in reader:
        try:
            x = float(x)
            y = float(y)
            data.append([x, y])
        except ValueError as e:
            pass
    data.sort()
    return data


def isothermProperties(data):
    pmin = min(x for x, y in data)
    pmax = max(x for x, y in data)
    nmin = min(y for x, y in data)
    nmax = max(y for x, y in data)
    print(f'Number of data points: {len(data)}')
    print(f'Minimal value of P/P°: {pmin:.4f}')
    print(f'Maximal value of P/P°: {pmax:.4f}')
    print(f'Minimal value of uptake: {nmin:.1f}')
    print(f'Maximal value of uptake: {nmax:.1f}')


def plotIsotherm(data):
    nmax = max(y for x, y in data)
    plt.title('Adsorption isotherm')
    plt.xlabel('P / P°')
    plt.ylabel('Nads')
    plt.axis([0, 1, 0, 1.1*nmax])
    plt.plot(*zip(*data), 'c-')
    plt.plot(*zip(*data), 'b+')
    plt.show()


def plotBET(data, xplotmax, xregmin, xregmax):
    fig, (plot1, plot2) = plt.subplots(2, sharex=True)
    fig.suptitle('BET plots')

    # All data for BET plot
    bet = [[x, x/(1-x)/y] for x, y in data if x <= xplotmax]
    betmax = max(y for x, y in bet)

    # All data for Rouquerol plot
    bet2 = [[x, y*(1-x)] for x, y in data if x <= xplotmax]
    bet2max = max(y for x, y in bet2)

    # Rouquerol plot within the regression window
    bet2reg = [y*(1-x) for x, y in data if xregmin <= x <= xregmax]
    Rouquerol_increasing = True
    for i in range(1, len(bet2reg)):
        if bet2reg[i] < bet2reg[i-1]:
            Rouquerol_increasing = False
            break

    # Perform the linear regression
    betreg = [[x, x/(1-x)/y] for x, y in data if xregmin <= x <= xregmax]
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(*zip(*betreg))

    BET_C = slope/intercept + 1
    BET_nmono = 1/(intercept*BET_C)
    BET_surf = BET_nmono / 0.02241396954e6 * 0.162e-18 * 6.02214076e23

    plot1.set(ylabel='')
    plot1.axis([0, xplotmax, 0, 1.1*betmax])
    plot1.plot(*zip(*bet), 'c-')
    plot1.plot([0, 1], [intercept, intercept+slope], 'r--')
    plot1.plot([xregmin, xregmin], [0, 2*betmax], 'g--')
    plot1.plot([xregmax, xregmax], [0, 2*betmax], 'g--')
    plot1.plot(*zip(*bet), 'b+')

    plot2.set(xlabel='P / P°', ylabel='')
    plot2.axis([0, xplotmax, 0, 1.1*bet2max])
    plot2.plot(*zip(*bet2), 'c-')
    plot2.plot([xregmin, xregmin], [0, 2*bet2max], 'g--')
    plot2.plot([xregmax, xregmax], [0, 2*bet2max], 'g--')
    plot2.plot(*zip(*bet2), 'b+')

    if BET_C > 0:
        print(f'✅ C = {BET_C:.2f} is positive')
    else:
        print(f'🔴 C = {BET_C:.2f} should be positive')

    nmaxfit = max(y for x, y in data if xregmin <= x <= xregmax)
    if BET_nmono <= nmaxfit:
        print(f'✅ nmono = {BET_nmono:.2f} is within BET range (up to {nmaxfit:.2f})')
    else:
        print(f'🔴 nmono = {BET_nmono:.2f} is outside BET range (up to {nmaxfit:.2f})')

    if Rouquerol_increasing:
        print(f'✅ Rouquerol plot increasing in fit range')
    else:
        print(f'🔴 Rouquerol plot should be increasing in fit range')

    print(f'R^2 = {r_value**2:.4f}')
    print(f'\nSurface area = {BET_surf:.3f} m^2/g')
