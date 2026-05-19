
# Wind Power Generation Link to German Electricity Prices

This project studies the **relationship** between wind power feed-in and German electricity prices using AR-X and GARCH-X time-series models. The goal is to estimate whether higher wind generation is associated with lower spot prices, and whether wind feed-in is also related to price volatility.

## Setup

Let:

- $P_t$: electricity spot price
- $W_t$: wind power feed-in
- $D_t$: solar power feed-in
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

## AR-X

Electricity prices are highly autocorrelated. A high price today often implies a high price in the next period. The AR terms capture this price persistence:

```math
\sum_{i=1}^{p}\phi_i P_{t-i}
```

Typical useful lags include:

```math
P_{t-1}, \quad P_{t-2}, \quad P_{t-7}
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
+
\gamma D_t
```

Here:

- $\alpha \varepsilon_{t-1}^2$ captures short-term shock effects
- $\delta \sigma_{t-1}^2$ captures volatility persistence
- $\eta W_t$ captures the association between wind feed-in and conditional volatility
