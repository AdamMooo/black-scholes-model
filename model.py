import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ── Black-Scholes closed-form ──────────────────────────────────────────
def black_scholes_price(S0, K, T, r, sigma, option="call"):
    if T <= 0:
        return max(0.0, (S0 - K) if option == "call" else (K - S0))

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option == "call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("option must be 'call' or 'put'")

# ── GBM simulator (physical measure, μ may differ from r) ─────────────
def gbm_paths(S0=100, mu=0.08, sigma=0.2, T=1.0, n_steps=252,
              n_paths=10, seed=None):
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    dW = rng.standard_normal((n_paths, n_steps)) * np.sqrt(dt)
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * dW
    log_paths = np.cumsum(log_returns, axis=1)
    paths = S0 * np.exp(log_paths)
    return np.column_stack([np.full(n_paths, S0), paths])

# ── Example usage & visualisations ────────────────────────────────────
if __name__ == "__main__":
    S0, K, T, r, sigma = 100, 105, 1, 0.05, 0.05
    print("Black–Scholes call:", black_scholes_price(S0, K, T, r, sigma))

    # 1) GBM sample paths
    paths = gbm_paths(S0, mu=0.08, sigma=sigma, T=T, n_paths=10, seed=42)
    t = np.linspace(0, T, paths.shape[1])

    plt.figure()
    for path in paths:
        plt.plot(t, path)
    plt.xlabel("Time (years)")
    plt.ylabel("Price")
    plt.title("Sample GBM Paths")
    plt.grid(True)

    # 2) Call price vs strike
    Ks = np.linspace(50, 150, 100)
    prices = [black_scholes_price(S0, k, T, r, sigma) for k in Ks]

    plt.figure()
    plt.plot(Ks, prices)
    plt.xlabel("Strike")
    plt.ylabel("Call Price")
    plt.title("European Call Price vs. Strike (T = 1y)")
    plt.grid(True)

    plt.show()
