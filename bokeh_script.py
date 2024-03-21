import pandas as pd
import pandas_bokeh
from bokeh.io import output_file


PATH = '\Datasets\supermarket_sales.csv'
OUTPUT_PATH = '\bokeh_dashboard\\sales_dashboard.html'


def create_dashboard(path):
    '''Function to create automated dashboard with bokeh'''
       
    pandas_bokeh.output_notebook()
    output_file(OUTPUT_PATH )
    
    df = pd.read_csv(path)
    
    # build sales functions
    days = (df["Total"].groupby(df['Date']).sum().rolling(7, min_periods=7).mean())
    
    income_city = df.pivot_table(index='City',
                                values='gross income',
                                aggfunc='sum').round(0)
    
    total_gender = df.pivot_table(index='Gender',
                                columns='Product line',
                                values='Total',
                                aggfunc='sum').round(0)
    
    total_customer = df.pivot_table(index='City',
                                columns='Customer type',
                                values='gross income',
                                aggfunc='sum').round(0)
    
    product = df.groupby('Product line')['gross income'].sum().sort_values(ascending=True).to_frame()

    # plotting charts
    colors=['#FDE724', '#D01C8B', '#4DAC26', '#d7191c']
    # 1 line plot
    p_line = days.plot_bokeh(kind="line",y="Total",color='#d01c8b', title='7-day moving average of daily sales.', plot_data_points=True,show_figure=True)

    # 2 bar plot
    p_bar = income_city.plot_bokeh(kind="bar", color='#d01c8b', legend=False, title='Revenue by the city.', show_figure=True)

    # 3 bar plot
    p_bar2 = total_gender.plot_bokeh(kind="bar", legend=False, title='Sales by Product line and Gender.', show_figure=True)

    # 4 stacked bar chart
    p_stack = total_customer.plot_bokeh(kind='barh', stacked=True, title='Revenue by City and Customer type.', colormap=colors, show_figure=True)

    # 5 pie chart
    p_pie = df.groupby(["Product line"])["Total"].sum().plot_bokeh(kind='pie', y='Total', title='Total sales by products line.',show_figure=True) 

    # 6 stacked bar chart
    p_stack2 = product.plot_bokeh(kind='barh', stacked=True, color='#4DAC26',legend=False, title='The products which generate the most revenue.', show_figure=True)

    # making dashboard with Grid Layout
    plot = pandas_bokeh.plot_grid([[p_bar2, p_pie, p_line],[p_stack2, p_bar, p_stack]], plot_width=400)
    
    return plot


if __name__ == '__main__':
    create_dashboard(PATH)
