import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataFrame = pd.read_csv("ubisoft.csv")
samples_arr = dataFrame["Zamkniecie"]
samples = samples_arr.to_numpy()


def calculate_eman(prices, period):
    alpha = 2 / (period + 1)
    ema = np.zeros_like(prices)
    ema[0] = prices[0]
    for i in range(1, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
    return ema

def macd_calc (samples):
    ema12 = calculate_eman(samples,12)
    ema26 = calculate_eman(samples,26)
    return ema12-ema26


macd = macd_calc(samples)
signal = calculate_eman(macd,9)
buy_signals = []
sell_signals = []

for i in range(1, len(macd)):

    if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
        buy_signals.append(i)
    elif macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
        sell_signals.append(i)




plt.figure(figsize=(12, 6))
plt.plot(samples, label="Cena zamknięcia", color="blue")
plt.legend()
plt.title("Notowania Ubisoft - Cena Zamknięcia w Czasie")
plt.xlabel("Dzień")
plt.ylabel("Cena zamknięcia (EUR)")
plt.show()


plt.figure(figsize=(12, 6))
plt.plot(macd, label="MACD", color="blue", linestyle="-")
plt.plot(signal, label="SIGNAL", color="red", linestyle="-")


plt.scatter(buy_signals, macd[buy_signals], color="green", marker="^", label="Sygnał Kupna", s=50)
plt.scatter(sell_signals, macd[sell_signals], color="red", marker="v", label="Sygnał Sprzedaży", s=50)


plt.legend()
plt.title("Wskaźnik MACD Ubisoft - Analiza Trendów")
plt.xlabel("Dzień")
plt.ylabel("Wartość MACD")
plt.show()




