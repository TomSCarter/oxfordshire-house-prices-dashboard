import plotly.express as px
import plotly.graph_objects as go

# SHARED STYLE SETTINGS

TEMPLATE = 'plotly_white'
TITLE_FONT_SIZE = 22
FONT_SIZE = 18
COLOR_PALETTE = px.colors.qualitative.Safe
PRICE_LINE_COLOR ='orange'
VOLUME_LINE_COLOR = '#1f77b4'
PALE_GREY = "#d9dcdeff"
HIDE_BAR = {'displayModeBar': False}

# ANNOTATIONS

ANNOTATIONS = [['2016-03-01', 
1250, "Additional property<br>surcharge introduced", 1800],
['2020-04-01', 600, "COVID-19<br>lockdown", 1800],
['2021-06-01', 1900, "Stamp duty holiday deadlines", 2450],
['2025-03-01', 1500, "Thresholds reduced", 1800]]

# CHART 1
def district_price_chart(df):

    df = df.sort_values(['district_median_£_per_m2'])
    district_order = list(df['district'].unique())
    fig = px.scatter(df, 
            x= '£_per_m²', 
            y='district', 
            color='property_type', 
                
            category_orders={'district':district_order, 
                                'property_type':['Detached', 'Semi-detached', 'Terraced', 'Flat']},
            template= TEMPLATE,
            labels={'count':'Number of sales', 'property_type':'Property type', 'district':'District', '£_per_m²': '£ per m²'},
            custom_data=['property_type', 'count'],
            color_discrete_sequence=COLOR_PALETTE)
    fig.update_xaxes(title_text='Median price per m² floor area', tickprefix='£', tickformat=',')
    fig.update_yaxes(title_text=None, showgrid=False)
    fig.update_layout(title_text='Cherwell is the least expensive district per m² for every property type',
                    title_subtitle_text='Median price per m², standard market sales (cat. A), Oxfordshire, 2023–2025',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    margin_t=100,
                    plot_bgcolor='white',
                    title_x=0)
    fig.update_traces(marker_size=12,
                    hovertemplate='<b>%{customdata[0]}, %{y}</b><br>Median £%{x:,.0f} per m²<br>%{customdata[1]} sales<extra></extra>')
    return fig



# CHART 2
def historical_volume_chart(df):
    fig = px.line(df, 
            template=TEMPLATE,
            x = 'deed_date',
            y = 'monthly_sales_count',
            labels={'monthly_sales_count':'Monthly number of sales'})
    fig.update_xaxes(title_text=None, 
                    nticks=20, 
                    ticklabelstep=2, 
                    range=['2015-01-01','2026-01-01'], 
                    rangeslider_visible=True)
    fig.update_yaxes(title_text="Monthly number of sales", 
                    range=[0, 2500],
                    tickformat=',')

    for x_val, y_val, text_val, ay_val in ANNOTATIONS:
        fig.add_annotation(x=x_val, 
                        y=y_val,
                        text=text_val,
                        showarrow=True,
                        arrowhead=1,
                        ayref='y',
                        ay=ay_val)

    fig.update_layout(title_text='Tax changes shift sales earlier',
                    title_subtitle_text='Standard market sales (cat. A) per month, Oxfordshire, 2015–2025',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    showlegend=False,
                    margin_t=100,
                    plot_bgcolor='white',
                    title_x=0,
                    height=500)
    fig.update_traces(hovertemplate='%{x|<b>%b %Y</b>}<br>Number of sales: %{y}<extra></extra>', line_color = VOLUME_LINE_COLOR)
    return fig

# CHART 3
def historical_price_chart(df):
    fig = px.line(df, 
            template=TEMPLATE,
            x = 'deed_date',
            y = 'median_£_per_m2',
            labels={'median_£_per_m2':'Median £ per m²'})
    fig.update_xaxes(title_text=None, 
                    nticks=20, 
                    ticklabelstep=2, 
                    range=['2015-01-01','2026-01-01'], 
                    rangeslider_visible=True,
                    rangeslider_range=['2015-01-01','2026-01-01'])
    fig.update_yaxes(title_text="Median £ per m²", 
                    range=[3000, 5000],
                    tickformat=',',
                    tickprefix='£')

    fig.update_layout(title_text='Median price per m² rose about 15% 2020–22, then levelled off',
                    title_subtitle_text='Standard market sales (cat. A) median £ per m² each month, Oxfordshire, 2015–2025 (not adjusted for inflation)',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    showlegend=False,
                    margin_t=100,
                    plot_bgcolor='white',
                    title_x=0)
    fig.update_traces(hovertemplate='%{x|<b>%b %Y</b>}<br>Median £ per m²: %{y:,.0f}<extra></extra>', line_color = PRICE_LINE_COLOR)


    for x_val, y_val, text_val, ay_val in ANNOTATIONS:
        fig.add_vline(x=x_val, line_width=1, line_dash="dot",
                  line_color="gray", opacity=0.8, annotation_text=text_val,
    annotation_position="top right")

    return fig

# CHART 4

def seasonality_chart(df):
    fig = px.line(df, x='month', y='max', template='plotly_white')
    fig.update_traces(hovertemplate=None, line_color = PALE_GREY)

    fig.add_trace(go.Scatter(x=df['month'], 
                            y=df['min'],
                            name='min', 
                            mode='lines',  
                            hovertemplate=None,
                            fill='tonexty',
                            line_color=PALE_GREY))
    fig.add_trace(go.Scatter(x=df['month'], 
                            y=df['median'],
                            name='median' ,
                            mode='lines',  
                            hovertemplate=None,
                            line_color=VOLUME_LINE_COLOR))
    fig.update_yaxes(title='Sales vs average month<br>(100 = average)')
    fig.update_xaxes(title=None, tickmode="array",
        tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    fig.update_layout(showlegend=False)
    fig.add_hline(y=100, line_width=1, line_dash="dot",
                    line_color="darkgray", opacity=0.8)
    fig.update_layout(title_text='Sales are lowest in winter, peak in June and stay above average through the second half',
                    title_subtitle_text='Median across years, with range shaded. Cat. A sales, Oxfordshire, 2015–2025, excluding tax-affected years (2016, 2020, 2021, 2025).',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    showlegend=False,
                    margin_t=100,
                    plot_bgcolor='white',
                    title_x=0)
    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y:,.0f} (average month =100)<extra></extra>')
    
    return fig

# CHART 5

def energy_efficiency_chart(df):
    fig = px.line(df, 
              x='energy_efficiency_rating_group', 
              y='median', 
              color='property_type',
              category_orders={'property_type':['Detached', 'Semi-detached', 'Terraced', 'Flat']},
              template= TEMPLATE,
              labels={'property_type':'Property type', '£/m2': '£ per m²'},
              custom_data=['property_type', 'count'],
              color_discrete_sequence=COLOR_PALETTE)
    fig.update_yaxes(title_text='Median price<br>per m² floor area', tickprefix='£', tickformat=',')
    fig.update_xaxes(title_text='Energy efficiency rating', showgrid=False)
    fig.update_layout(title_text='Homes with highest energy efficiency linked to lowest price per  m²',
                    title_subtitle_text='Median price per m², standard market sales (cat. A), Oxfordshire, 2023–2025. New builds and records with expired EPC certificates excluded. Includes some records from before rating method changed in 2015. Excluded Flats rated F/G for too few records (18).',
                    title_font_size=TITLE_FONT_SIZE,
                    font_size=FONT_SIZE,
                    margin_t=100,
                    plot_bgcolor='white',
                    title_x=0)
    fig.update_traces(marker_size=12,
                    hovertemplate='<b>%{customdata[0]}, Rating: %{x}</b><br>Median £%{y:,.0f} per m²<br>Count: %{customdata[1]}<extra></extra>')


    return fig