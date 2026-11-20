# Oxfordshire House Prices

## How much more do new builds sell for in Oxfordshire (2015–2025), once you account for size, property type, location, time and energy rating?

## What I've Done
- An ordinary least squares (linear) regression of log price on the new_build flag
- Three models: 
    1. Raw model
    2. Accounting for floor_area, district, year (of sale), property_subtype, energy_efficiency_rating_band
    3. Accounting for floor_area, district, year (of sale), property_subtype
- Added section to README and noted link to finding 4 (homes with high efficiency rating sell for less)

## Decisions
- Used cat. A only sales, cat. B sales often aren't market prices
- Used the most common values as reference levels when accounting for the variables
- Chose robust standard errors
- Chose model without efficiency rating, as decided that EPC rating is a bad control (being new causes high efficiency ratings, and rating can stand in for property age)

## Problems/surprises
- Premium went from 8.8% in the raw model to 4.4% with all the factors accounted for, then to 0% when EPC rating was removed (not accounted for)
- Energy rating pointed the opposite way from expected (A/B less expensive, F/G more expensive, vs D)

## Learned
- Using statsmodels API
    - model = smf.ols('log_price ~ new_build', data=df).fit(cov_type='HC1')
    - print(model.summary()) 
    - C(), Treatment(reference=)
    - Converting log coefficients (exp(coeff)-1)
    - Reading a regression summary
    - Robust standard erros
    - Inference vs prediction
    - Bad controls

## Next
- Interaction by year (did help-to-buy change things)
- Add construction age band
- Centre floor area
