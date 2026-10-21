# Oxfordshire house prices dashboard - Day 1 log - Questions and faceting

## Questions
- For a property investor
    - How does £ per sqm floor_area vary between districts? Where is space cheapest?
    - Do homes with poor energy efficiency sell at a discount (per m2)?
        - Landlords have to meet a minimum energy rating to let, which may be raised
    - Do prices or sales volume vary throughout the year? When are they lowest/highest?
        - Compare months within a year to avoid long term price rise trend
    - Do new builds cost more per m2?
    - What has been the overall price/volume trend since 2015?
        - Did sales volumes or prices change when tax changes took place?
            - Extra stamp duty changes (first in April 2016 for additional properties then increased)

## Notes
- In transaction_category there are A or B sales. Type A are standard sales whereas type B include repossessions, sales to companies, some buy-to-lets and other transactions not at typical market price.
    - The proportion of type B sales rises from 5% in 2015 to 10% in 2019 then fluctuates between 8% and 10%.
    - Category B will be excluded from price, £/m² and volume charts. They will be labelled as depicting standard market sales only.
- Sales volume in 2025 does not drop in later months (ca. 800 sales in a typical month), but does spike in March (ca. 1600) and drop sharply in April (ca. 400)
    - Likely linked to the stamp duty change in April 2025, confirm year and annotate on volume chart.

## Faceting exercise
How does £ per sqm floor_area vary between districts? Where is space cheapest?
- One panel per property_type, districts compared within each panel

- Data preparation
    - Category A only
    - Using property_subtype, the property type from the Land Registry dataset.
        - As it is recorded with the sale it describes the property most accurately on sale day
        - It's complete for every sale and is standard in house statistics, rather than the split used in the EPCs (e.g. maisonette, bungalow etc)
    - Time period
        - Prices over 2015-2025 have changed significantly
        - Using 2023-2025 to give most relevant period for a property investor
        - 339 to 2419 sales per district/property_subtype category
    - £/m2 outliers
        - Looking at > £25,000 /m2 there are many 1 room properties and also massive sale prices with small floor areas (perhaps matched with an annex due to the known address subset issue)
        - Looking into setting thresholds on reasonable m2 per habitable room
            - Total floor area includes all rooms but number_habitable_rooms does not include kitchen, bathroom etc. So this value will be well above the houses smallest room
            - Difficult to decide non-arbitrary thresholds. Filtering on m2/habitable_room >=10 and < 200 removed about 100 sales. Not a large set, better dealt with in the pipeline during matching.
            - Excluding sales with > £20,000/m2 makes a negligible change to median values.
        - Decision: No filter applied. Outlier markers hidden, boxes and whiskers use all data. Log possible annex matching as pipeline issue.
- Plotting
    - Panels share a similar range on y-axis, so no reason to use independent axes. Shared axis helps make accurate comparisons between panels
    - Replaced property_subtype codes with full names
    - Ordered districts by median £/m2