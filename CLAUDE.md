# Claude Context — Black-Scholes-Model

**Status: STABLE / REFERENCE — do not add features or change implementations.**

## Purpose
Black-Scholes option pricing model from first principles. Computes European call/put prices
analytically. Foundation for all options work in the ecosystem. Project #1 in the
9-project learning journey.

## Architecture
```
Code/                   Core implementation (single-file or small set of files)
```

## Current State
- Complete and stable
- Foundation for Option-Greeks, Volatility-Surface-Monitor, and related projects
- GitHub: https://github.com/AdamMooo/Black-Scholes-Model

## Key Reference Points
- Black-Scholes PDE: ∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S - rV = 0
- Closed-form solution for European options
- Inputs: S (spot), K (strike), T (time to expiry), r (risk-free rate), σ (volatility)
- Output: option price + d1, d2 intermediates (used by Option-Greeks)
- Key insight: options do not scale linearly with spot price

## Do Not
- Add new features or extend scope
- Change pricing logic — it is analytically correct
- Add American option pricing (different model, different project)
- Add new dependencies

## When to Read This Project
- When reviewing theoretical foundations of options pricing
- When Volatility-Surface-Monitor needs IV surface context
- Not for active development sessions
