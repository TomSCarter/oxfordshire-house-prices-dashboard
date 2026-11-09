import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# SHARED STYLE SETTINGS

TEMPLATE = 'plotly_white'
TITLE_FONT_SIZE = 22
FONT_SIZE = 18
# proprety type color mapping
PRICE_LINE_COLOR ='orange'
VOLUME_LINE_COLOR = 'blue'
HIDE_BAR = {'displayModeBar': False}

# ANNOTATIONS

ANNOTATIONS = [['2016-03-01', 
1250, "Additional property<br>surcharge introduced", -50],
['2020-04-01', 600, "COVID-19 lockdown", -100],
['2021-06-01', 1900, "Stamp duty holiday deadlines", -75],
['2025-03-01', 1500, "Thresholds reduced", 0]]

# CHART 1
def chart_1(df):
    fig = px.scatter(df, 
            x= '£_per_m²', 
            y='district', 
            color='property_type', 
                
            category_orders={'district':['Cherwell', 'Vale of White Horse', 'West Oxfordshire', 'South Oxfordshire', 'Oxford'], 
                                'property_type':['Detached', 'Semi-detached', 'Terraced', 'Flat']},
            template= TEMPLATE,
            labels={'count':'Number of sales', 'property_type':'Property type', 'district':'District', '£_per_m²': '£ per m²'},
            custom_data=['property_type', 'count'],
            color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_xaxes(title_text='Median price per m² floor area', tickprefix='£', tickformat=',')
    fig.update_yaxes(title_text=None, showgrid=False)
    fig.update_layout(title_text='Oxford city is the most expensive district per m² for every property type',
                    title_subtitle_text='Median price per m², standard market sales (cat. A), Oxfordshire, 2023–2025',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE)
    fig.update_traces(marker_size=12,
                    hovertemplate='<b>%{customdata[0]}, %{y}</b><br>Median £%{x:,.0f} per m²<br>%{customdata[1]} sales<extra></extra>')
    return fig



# CHART 2
def chart_2(df):
    fig = px.line(df, 
            template=TEMPLATE,
            x = df.index,
            y = 'monthly_sales_count',
            labels={'monthly_sales_count':'Monthly number of sales'})
    fig.update_xaxes(title_text=None, 
                    nticks=20, 
                    ticklabelstep=2, 
                    range=['2015-01-01','2026-01-01'], 
                    rangeslider_visible=True)
    fig.update_yaxes(title_text="Monthly number of sales", 
                    range=[0, 2500])

    for x_val, y_val, text_val, ay_val in ANNOTATIONS:
        fig.add_annotation(x=x_val, 
                        y=y_val,
                        text=text_val,
                        showarrow=True,
                        arrowhead=1,
                        ay=ay_val)

    fig.update_layout(title_text='Tax changes shift sales earlier',
                    title_subtitle_text='Standard market sales (cat. A) per month, Oxfordshire, 2015–2025',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    showlegend=False,
                    margin_t=100)
    fig.update_traces(hovertemplate='%{x|<b>%b %Y</b>}<br>Number of sales: %{y}<extra></extra>', line_color = VOLUME_LINE_COLOR)
    fig.add_trace(go.Scatter(x=df.index, 
                            y=df['median_£_per_m2'], 
                            name='median £ per m2', 
                            mode='lines', 
                            line_color= PRICE_LINE_COLOR, 
                            hovertemplate='%{x|<b>%b %Y</b>}<br>Median £ per m²: %{y:,.0f}<extra></extra>',
                            visible=False))
    fig.update_layout(updatemenus=[dict(
        buttons=[
            dict(label='Monthly number of sales',
                method='update',
                args=[{'visible':[True, False]},
                    {'title.text':'Tax changes shift sales earlier',
                        'title.subtitle.text':'Standard market sales (cat. A) per month, Oxfordshire, 2015–2025',
                        'yaxis.title.text':'Monthly number of sales',
                        'yaxis.range':[0, 2500],
                        'annotations':fig.layout.annotations,
                        'yaxis.tickprefix': ''}]),
            dict(label='Median £ per m²',
                        method='update',
                        args=[{'visible':[False, True]},
                            {'title.text':"Median price per m² rose about 15% 2020–22, then levelled off",
                                'title.subtitle.text':'Standard market sales (cat. A) median £ per m² each month, Oxfordshire, 2015–2025 (not adjusted for inflation)',
                                'yaxis.title.text':'Median £ per m²',
                                'yaxis.range':[3000, 5000],
                                'yaxis.tickprefix':'£',
                                'yaxis.tickformat':',',
                                'annotations':[]}])
        ],
        direction='down',
        x=1, xanchor='right', y=1.15, yanchor='top'
    )])

    return fig