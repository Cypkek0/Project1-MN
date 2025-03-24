import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#wybor danych ubisoft - ubisfot - 9697_jp_d -capcom
#dataFrame = pd.read_csv("ubisoft.csv")
dataFrame = pd.read_csv("9697_jp_d.csv")
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



#akcje ubi
plt.figure(figsize=(12, 6))
plt.plot(samples, label="Cena zamknięcia", color="blue")
plt.legend()
plt.title("Notowania Capcom - Cena Zamknięcia w Czasie")
plt.xlabel("Dzień")
plt.ylabel("Cena zamknięcia (JPY)")
plt.show()

#macd, signal i punkty na calym wykresie
plt.figure(figsize=(12, 6))
plt.plot(macd, label="MACD", color="blue", linestyle="-")
plt.plot(signal, label="SIGNAL", color="red", linestyle="-")
plt.scatter(buy_signals, macd[buy_signals], color="green", marker="^", label="Sygnał Kupna", s=50)
plt.scatter(sell_signals, macd[sell_signals], color="red", marker="v", label="Sygnał Sprzedaży", s=50)
plt.legend()
plt.title("Wskaźnik MACD Capcom - Analiza Trendów")
plt.xlabel("Dzień")
plt.ylabel("Wartość MACD")
plt.show()

#akcje ubi + punkty kupna sprzedazy
plt.figure(figsize=(12, 6))
plt.plot(samples, label="Cena zamknięcia", color="blue")
plt.scatter(buy_signals, samples[buy_signals], color="green", marker="^", label="Sygnał Kupna", s=50)
plt.scatter(sell_signals, samples[sell_signals], color="red", marker="v", label="Sygnał Sprzedaży", s=50)
plt.legend()
plt.title("Notowania Capcom ze wskaźnikami zakupu i sprzedaży MACD")
plt.xlabel("Dzień")
plt.ylabel("Cena zamknięcia (JPY)")
plt.show()

#odcinek od 600 do 800
mid_index = 700
start_index = max(0, mid_index - 100)
end_index = min(len(samples), mid_index + 100)
samples_cut = samples[start_index:end_index]
macd_cut = macd[start_index:end_index]
signal_cut = signal[start_index:end_index]
buy_signals_cut = [i for i in buy_signals if start_index <= i < end_index]
sell_signals_cut = [i for i in sell_signals if start_index <= i < end_index]

transactions = []
total_profit = 0
holding = False

for i in range(len(buy_signals_cut)):
    buy_day = buy_signals_cut[i]
    buy_price = samples[buy_day]

    sell_day = next((s for s in sell_signals_cut if s > buy_day), None)

    if sell_day is not None:
        sell_price = samples[sell_day]
        profit = ((sell_price - buy_price) / buy_price) * 100

        transactions.append((buy_day, sell_day, buy_price, sell_price, profit))
        total_profit += profit

for t in transactions:
    print(f"Transakcja: Kupno {t[0]} po {t[2]:.2f}, sprzedaż {t[1]} po {t[3]:.2f}, zysk: {t[4]:.2f}%")

print(f"Łączny zysk/strata: {total_profit:.2f}%")

#plot macd i signal dla 600-800 + buy/sell pointy
plt.figure(figsize=(12, 6))
plt.plot(macd_cut, label="MACD", color="blue")
plt.plot(signal_cut, label="SIGNAL", color="red")
plt.scatter([i - start_index for i in buy_signals_cut], macd[buy_signals_cut],
            color="green", marker="^", label="Kupno", s=50)
plt.scatter([i - start_index for i in sell_signals_cut], macd[sell_signals_cut],
            color="red", marker="v", label="Sprzedaż", s=50)
plt.legend()
plt.title("Analiza MACD na wybranym fragmencie 1")
plt.xlabel("Dzień")
plt.ylabel("Wartość MACD")
plt.show()

#plot macd i signal dla 600-800 + buy/sell pointy
plt.figure(figsize=(12, 6))
plt.plot(samples_cut, label="Samples", color="blue")
plt.scatter([i - start_index for i in buy_signals_cut], samples[buy_signals_cut],
            color="green", marker="^", label="Kupno", s=50)
plt.scatter([i - start_index for i in sell_signals_cut], samples[sell_signals_cut],
            color="red", marker="v", label="Sprzedaż", s=50)
plt.legend()
plt.title("Analiza akcji na wybranym fragmencie 1")
plt.xlabel("Dzień")
plt.ylabel("Wartość akcji (JPY)")
plt.show()


#odcinek od 200 do 400
mid_index = 300
start_index = max(0, mid_index - 100)
end_index = min(len(samples), mid_index + 100)
samples_cut = samples[start_index:end_index]
macd_cut = macd[start_index:end_index]
signal_cut = signal[start_index:end_index]
buy_signals_cut = [i for i in buy_signals if start_index <= i < end_index]
sell_signals_cut = [i for i in sell_signals if start_index <= i < end_index]

transactions = []
total_profit = 0
holding = False

for i in range(len(buy_signals_cut)):
    buy_day = buy_signals_cut[i]
    buy_price = samples[buy_day]

    sell_day = next((s for s in sell_signals_cut if s > buy_day), None)

    if sell_day is not None:
        sell_price = samples[sell_day]
        profit = ((sell_price - buy_price) / buy_price) * 100

        transactions.append((buy_day, sell_day, buy_price, sell_price, profit))
        total_profit += profit

for t in transactions:
    print(f"Transakcja: Kupno {t[0]} po {t[2]:.2f}, sprzedaż {t[1]} po {t[3]:.2f}, zysk: {t[4]:.2f}%")

print(f"Łączny zysk/strata: {total_profit:.2f}%")


plt.figure(figsize=(12, 6))
plt.plot(macd_cut, label="MACD", color="blue")
plt.plot(signal_cut, label="SIGNAL", color="red")
plt.scatter([i - start_index for i in buy_signals_cut], macd[buy_signals_cut],
            color="green", marker="^", label="Kupno", s=50)
plt.scatter([i - start_index for i in sell_signals_cut], macd[sell_signals_cut],
            color="red", marker="v", label="Sprzedaż", s=50)
plt.legend()
plt.title("Analiza MACD na wybranym fragmencie 2")
plt.xlabel("Dzień")
plt.ylabel("Wartość MACD")
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(samples_cut, label="Samples", color="blue")
plt.scatter([i - start_index for i in buy_signals_cut], samples[buy_signals_cut],
            color="green", marker="^", label="Kupno", s=50)
plt.scatter([i - start_index for i in sell_signals_cut], samples[sell_signals_cut],
            color="red", marker="v", label="Sprzedaż", s=50)
plt.legend()
plt.title("Analiza akcji na wybranym fragmencie 1")
plt.xlabel("Dzień")
plt.ylabel("Wartość akcji (JPY)")
plt.show()


