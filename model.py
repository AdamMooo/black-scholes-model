from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


DEMO_PARAMS = {
    "S0": 100,
    "K": 105,
    "T": 1.0,
    "r": 0.05,
    "sigma": 0.05,
}

# ── Black-Scholes closed-form ──────────────────────────────────────────
def black_scholes_price(S0, K, T, r, sigma, option="call"):
    """Return the Black-Scholes price for a European call or put."""
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
    """Simulate geometric Brownian motion paths."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    dW = rng.standard_normal((n_paths, n_steps)) * np.sqrt(dt)
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * dW
    log_paths = np.cumsum(log_returns, axis=1)
    paths = S0 * np.exp(log_paths)
    return np.column_stack([np.full(n_paths, S0), paths])


def write_demo_outputs(output_dir="outputs"):
    """Generate reproducible demo artifacts for the README."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    S0 = DEMO_PARAMS["S0"]
    K = DEMO_PARAMS["K"]
    T = DEMO_PARAMS["T"]
    r = DEMO_PARAMS["r"]
    sigma = DEMO_PARAMS["sigma"]
    call_price = black_scholes_price(S0, K, T, r, sigma)

    # Save a few reference prices so readers can inspect concrete results.
    sample_strikes = np.array([90, 100, 105, 110, 120])
    sample_prices = np.array([
        black_scholes_price(S0, strike, T, r, sigma) for strike in sample_strikes
    ])
    price_table = np.column_stack([sample_strikes, sample_prices])
    np.savetxt(
        output_path / "sample_call_prices.csv",
        price_table,
        delimiter=",",
        header="strike,call_price",
        comments="",
        fmt=["%.0f", "%.6f"],
    )

    summary_lines = [
        "Black-Scholes demo output",
        f"spot={S0}",
        f"strike={K}",
        f"maturity_years={T}",
        f"rate={r}",
        f"volatility={sigma}",
        f"call_price={call_price:.6f}",
    ]
    (output_path / "example_output.txt").write_text("\n".join(summary_lines) + "\n")

    paths = gbm_paths(S0, mu=0.08, sigma=sigma, T=T, n_paths=10, seed=42)
    t = np.linspace(0, T, paths.shape[1])

    fig, ax = plt.subplots()
    for path in paths:
        ax.plot(t, path)
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Price")
    ax.set_title("Sample GBM Paths")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path / "gbm_sample_paths.png", dpi=150)
    plt.close(fig)

    strikes = np.linspace(50, 150, 100)
    prices = [black_scholes_price(S0, strike, T, r, sigma) for strike in strikes]

    fig, ax = plt.subplots()
    ax.plot(strikes, prices)
    ax.set_xlabel("Strike")
    ax.set_ylabel("Call Price")
    ax.set_title("European Call Price vs. Strike (T = 1y)")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path / "call_price_vs_strike.png", dpi=150)
    plt.close(fig)

    return {
        "call_price": call_price,
        "output_dir": output_path,
    }


def main():
    outputs = write_demo_outputs()
    print(f"Black-Scholes call: {outputs['call_price']:.6f}")
    print(f"Saved demo outputs to: {outputs['output_dir']}")

# ── Example usage & visualisations ────────────────────────────────────
if __name__ == "__main__":
    main()
