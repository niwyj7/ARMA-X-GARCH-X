
# Wind Power Generation Link to German Electricity Prices

This project studies the **relationship** between wind power feed-in and German electricity prices (daily) using AR-X and GARCH-X time-series models. The goal is to estimate whether higher wind generation is associated with lower spot prices, and whether wind feed-in is also related to price volatility. 

Price ACF and PACF plot before seasonal adjustment:

<img width="1234" height="449" alt="image" src="https://github.com/user-attachments/assets/7059cb25-cb2c-44ab-a61d-8794d79b948b" />


Wind ACF and PACF plot before seasonal adjustment:

<img width="1234" height="449" alt="image" src="https://github.com/user-attachments/assets/c8e5d8d6-5214-4583-bfb8-7a44c9bc1fda" />


Seasonal decomposition (period=7):

<img width="1489" height="820" alt="image" src="https://github.com/user-attachments/assets/2a5e1eea-2cf1-464e-a22d-0ea0a268f676" />

<img width="1489" height="820" alt="image" src="https://github.com/user-attachments/assets/18cd4bc3-c16b-430d-a021-0c1cc27d8936" />

Adjusted price and wind:

<img width="1194" height="547" alt="image" src="https://github.com/user-attachments/assets/cd2544be-e18b-4ff9-841a-088428da2dff" />

<img width="1163" height="547" alt="image" src="https://github.com/user-attachments/assets/a73c1721-3fde-4447-89e7-8879303f2875" />

<img width="842" height="545" alt="image" src="https://github.com/user-attachments/assets/17260e4d-86b1-406a-99a4-259eb763c19d" />


Adjusted ACF and PACF plot:

<img width="1234" height="449" alt="image" src="https://github.com/user-attachments/assets/1476178f-a8c7-4422-abf5-1050908792ba" />
<img width="1234" height="449" alt="image" src="https://github.com/user-attachments/assets/8d052286-2bfd-4fe0-a022-275d75284b7d" />


## Setup

Let:

- $P_t$: daily price
- $W_t$: wind power feed-in
- $W_{t-1}$: wind power feed-in lag term
- $\varepsilon_t$: residual shock
- $\varepsilon_{t-1}$: residual shock

The baseline AR-X mean equation is:

```math
P_t
=
\alpha
+
\phi P_{t-i}
+
\lambda W_{t-1}
+
\beta W_t
+
\varepsilon_t
+
\theta \varepsilon_{t-1}
```

## ARMA-X

Standardise data first.

<img width="848" height="644" alt="7e5ba899-aaa5-4798-b99b-26904d191c41" src="https://github.com/user-attachments/assets/e76d0c11-2740-472c-8b70-27feab1c0838" />

Autocorrelation Test (Ljung-Box) of Residuals

lb_stat  lb_pvalue

3.078383   0.079339


Autocorrelation Test (Ljung-Box) of Squared Residuals

lb_stat  lb_pvalue

10.750803   0.001042

Squared Residuals:

<img width="1234" height="449" alt="image" src="https://github.com/user-attachments/assets/632aa103-681a-4df6-9415-19e4c87ab6f3" />

Residual:

<img width="838" height="372" alt="image" src="https://github.com/user-attachments/assets/b46b1cf6-2ab1-4a26-8442-47d3ff077b91" />

mean=-0.005027

## GARCH-X

```math
\sigma_t^2 = 
\omega +
\beta_1 W_t +
\beta_2 crash\_dummy_t +
\alpha_1 \varepsilon_{t-1}^2 + 
\beta_3 \sigma_{t-1}^2 

```
<br>
<img width="706" height="604" alt="9ecd8142-89fa-4cf1-b1ab-0d2f9e894be5" src="https://github.com/user-attachments/assets/20d3b7ca-5f19-469d-84b8-821f78c28ee4" />


