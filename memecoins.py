import requests

MEMECOINS = ["SHIB", "PEPE", "FLOKI"]
EXCHANGES = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT",
    "OKX": "https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT",
    "Bybit": "https://api.bybit.com/v2/public/tickers"
}

def get_price_binance(symbol):
    try:
        r = requests.get(EXCHANGES["Binance"].format(symbol=symbol))
        return float(r.json()["price"])
    except: return None

def get_price_okx(symbol):
    try:
        r = requests.get(EXCHANGES["OKX"].format(symbol=symbol))
        return float(r.json()["data"][0]["last"])
    except: return None

def get_price_bybit(symbol):
    try:
        r = requests.get(EXCHANGES["Bybit"])
        data = r.json()["result"]
        for item in data:
            if item["symbol"] == f"{symbol}USDT":
                return float(item["last_price"])
    except: return None

def compare_memecoins():
    results = []
    for token in MEMECOINS:
        b = get_price_binance(token)
        o = get_price_okx(token)
        y = get_price_bybit(token)

        prices = {"Binance": b, "OKX": o, "Bybit": y}
        combos = [("Binance", "OKX"), ("Binance", "Bybit"), ("OKX", "Bybit"),
                  ("OKX", "Binance"), ("Bybit", "Binance"), ("Bybit", "OKX")]

        for src, tgt in combos:
            if prices[src] and prices[tgt]:
                spread = prices[tgt] - prices[src]
                percent = (spread / prices[src]) * 100
                if percent >= 0.8:
                    results.append(f"🐸 {token}: {src} → {tgt}\n"
                                   f"Buy at {prices[src]:.8f}, Sell at {prices[tgt]:.8f}\n"
                                   f"💰 Spread: {percent:.2f}%\n")

    return results if results else ["😕 No meme token arbitrage (≥ 0.8%)"]
