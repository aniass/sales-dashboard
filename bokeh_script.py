import pandas as pd
import pandas_bokeh
from bokeh.io import output_file


PATH = r'datasets\supermarket_sales.csv'
OUTPUT_PATH = r'bokeh_dashboard\sales_dashboard.html'


def read_data(path):
    '''Read data from CSV file'''
    return pd.read_csv(path)


def calculate_metrics(df):
    '''Calculate various metrics for the dashboard'''
    # Rolling 7-day average of daily sales
    days = (df["Total"].groupby(df['Date']).sum().rolling(7, min_periods=7).mean())
    
    # Income by City
    income_city = df.pivot_table(index='City',
                                values='gross income',
                                aggfunc='sum').round(0)
    
    # Sales by Gender and Product line
    total_gender = df.pivot_table(index='Gender',
                                columns='Product line',
                                values='Total',
                                aggfunc='sum').round(0)
    
    # Revenue by City and Customer type
    total_customer = df.pivot_table(index='City',
                                columns='Customer type',
                                values='gross income',
                                aggfunc='sum').round(0)

    # Total revenue by Product Line
    product = df.groupby('Product line')['gross income'].sum().sort_values(ascending=True).to_frame()
    
    return days, income_city, total_gender, total_customer, product


def create_dashboard(path, output_path):
    '''Create automated dashboard with Bokeh'''
    pandas_bokeh.output_notebook()
    output_file(output_path)
    
    df = read_data(path)
    metrics = calculate_metrics(df)
    
    # Plot various charts for the dashboard
    colors=['#FDE724', '#D01C8B', '#4DAC26', '#d7191c']
            
    # Line plot: 7-day moving average of daily sales
    p_line = metrics[0].plot_bokeh(kind="line",y="Total",color='#d01c8b', title='7-day moving average of daily sales.', plot_data_points=True,show_figure=True)

    # Bar plot: Revenue by city
    p_bar = metrics[1].plot_bokeh(kind="bar", color='#d01c8b', legend=False, title='Revenue by the city.', show_figure=True)

    # Bar plot: Sales by Product line and Gender
    p_bar2 = metrics[2].plot_bokeh(kind="bar", legend=False, title='Sales by Product line and Gender.', show_figure=True)

    # Stacked bar chart: Revenue by City and Customer type
    p_stack =  metrics[3].plot_bokeh(kind='barh', stacked=True, title='Revenue by City and Customer type.', colormap=colors, show_figure=True)

    # Pie chart: Total sales by product line
    p_pie = df.groupby(["Product line"])["Total"].sum().plot_bokeh(kind='pie', y='Total', title='Total sales by products line.',show_figure=True) 

    # Stacked bar chart: The products which generate the most revenue
    p_stack2 = metrics[4].plot_bokeh(kind='barh', stacked=True, color='#4DAC26',legend=False, title='The products which generate the most revenue.', show_figure=True)
    
    # Create dashboard with Grid Layout
    plots = pandas_bokeh.plot_grid([[p_bar2, p_pie, p_line],[p_stack2, p_bar, p_stack]], plot_width=400)
    return plots


if __name__ == '__main__':
    create_dashboard(PATH, OUTPUT_PATH)
