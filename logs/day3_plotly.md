# Oxfordshire house prices dashboard - Day 3 log - Plotly

Replotting graphs using Plotly express

## Chart 1
- Generated table of medians and counts for district x property_subtype. As Plotly Express doesn't calculate medians like Seaborn.
- Used plotly express to plot a scatter of median vs district, coloured by property type
- Increased marker size
- Added £ and commas to price labels on x axis
- Changed axis labels, no Y label as districts are clear and Median price per m2 for X
- Used plotly_white template to remove grey background and gridlines
- Updated labels inc legend title
- Adjusted order of districts to match sorted medians as before, adjusted order to property types to reflect size
- Adjusted font sizes
- Added subtitle
- Changed marker colours to 'safe' palette to be more generally readable, red vs green is a hazard for colour-blind readers
- Removed horizontal gridlines
- Changed tooltip to be more easily scanned than raw labels. Added £ and comma to median in tooltip. Shows sample size which isnt in main chart
- Hid display mode bar, as pan/zoom not needed
- Things that happened:
    - A typo in category_order silently stopped it working. Plotly doesnt warn about mis-matched keys
    - Changed hover_data to custom_data to solidify the indexes used in the tooltip
    - The overlapping dots in South Oxfordshire can't be separated with dodge, as in Seaborn, but they are distinguished by the tooltip
