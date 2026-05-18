
# Wind-Driven Merit-Order Effect in German Electricity Prices

This project studies the relationship between wind power feed-in and German day-ahead electricity prices using AR-X and GARCH-X time-series models. The goal is to estimate whether higher wind generation is associated with lower spot prices, and whether wind feed-in is also related to conditional price volatility.

## Setup

Let:

- $P_t$: electricity spot price
- $W_t$: wind power feed-in
- $S_t$: seasonal controls
- $\varepsilon_t$: residual shock

The baseline AR-X mean equation is:

```math
P_t
=
\alpha
+
\sum_{i=1}^{p}\phi_i P_{t-i}
+
\beta W_t
+
\gamma D_t
+
S_t
+
\varepsilon_t
```

## Seasonality Treatment

Electricity prices and wind generation both have strong seasonal patterns. Ignoring these patterns may confound the wind-price relationship.

The model controls for seasonality using calendar fixed effects:

```math
S_t
=
\lambda_{\text{hour}}
+
\mu_{\text{weekday}}


This means the wind coefficient is interpreted as the association between wind feed-in and prices after controlling for normal intraday, weekly or monthly price patterns.

An alternative robustness check is to use seasonally adjusted variables:

```math
\tilde{P}_t = P_t - \hat{s}_P(t)
```

```math
\tilde{W}_t = W_t - \hat{s}_W(t)
```

and estimate:

```math
\tilde{P}_t
=
\alpha
+
\sum_{i=1}^{p}\phi_i \tilde{P}_{t-i}
+
\beta \tilde{W}_t
+
\varepsilon_t
```

This tests whether wind generation above its normal seasonal level is associated with prices below their normal seasonal level.


## Why AR-X?

Electricity prices are highly autocorrelated. A high price today often implies a high price in the next period. The AR terms capture this price persistence:

```math
\sum_{i=1}^{p}\phi_i P_{t-i}
```

Typical useful lags include:

```math
P_{t-1}, \quad P_{t-24}, \quad P_{t-168}
```

for hourly data, representing previous hour, previous day and previous week effects.


## GARCH-X Volatility Model

Electricity prices often show volatility clustering. After estimating the mean equation, residuals may still have time-varying variance.

The GARCH-X variance equation is:

```math
\sigma_t^2
=
\omega
+
\alpha \varepsilon_{t-1}^2
+
\delta \sigma_{t-1}^2
+
\eta W_t
```

Here:

- $\alpha \varepsilon_{t-1}^2$ captures short-term shock effects
- $\delta \sigma_{t-1}^2$ captures volatility persistence
- $\eta W_t$ captures the association between wind feed-in and conditional volatility
