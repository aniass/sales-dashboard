import pandas as pd
import pandas_bokeh
from bokeh.io import output_file


PATH = r'C:\Python Scripts\Datasets\supermarket_sales.csv'
OUTPUT_PATH = r'C:\Python Scripts\Projects_done\bokeh_project\sales4.html'


def read_data(path):
    return pd.read_csv(path)


def calculate_metrics(df):
    # Rolling 7-day average of daily sales
    days = (df["Total"].groupby(df['Date']).sum().rolling(7, min_periods=7).mean())
    # Income by city
    income_city = df.pivot_table(index='City',
                                values='gross income',
                                aggfunc='sum').round(0)
    # Sales by gender and product line
    total_gender = df.pivot_table(index='Gender',
                                columns='Product line',
                                values='Total',
                                aggfunc='sum').round(0)
    # # Revenue by City and Customer type
    total_customer = df.pivot_table(index='City',
                                columns='Customer type',
                                values='gross income',
                                aggfunc='sum').round(0)

    # Total revenue by product line
    product = df.groupby('Product line')['gross income'].sum().sort_values(ascending=True).to_frame()
    
    return days, income_city, total_gender, total_customer, product


def create_dashboard(PATH, OUTPUT_PATH):
    pandas_bokeh.output_notebook()
    output_file(OUTPUT_PATH)
    
    df = read_data(PATH)
    metrics = calculate_metrics(df)
    
    colors=['#FDE724', '#D01C8B', '#4DAC26', '#d7191c']
    # 1 line plot
    p_line = metrics[0].plot_bokeh(kind="line",y="Total",color='#d01c8b', title='7-day moving average of daily sales.', plot_data_points=True,show_figure=True)

    # 2 bar plot
    p_bar = metrics[1].plot_bokeh(kind="bar", color='#d01c8b', legend=False, title='Revenue by the city.', show_figure=True)

    # 3 bar plot
    p_bar2 = metrics[2].plot_bokeh(kind="bar", legend=False, title='Sales by Product line and Gender.', show_figure=True)

    # 4 stacked bar chart
    p_stack =  metrics[3].plot_bokeh(kind='barh', stacked=True, title='Revenue by City and Customer type.', colormap=colors, show_figure=True)

    # 5 pie chart
    p_pie = df.groupby(["Product line"])["Total"].sum().plot_bokeh(kind='pie', y='Total', title='Total sales by products line.',show_figure=True) 

    # 6 stacked bar chart
    p_stack2 = metrics[4].plot_bokeh(kind='barh', stacked=True, color='#4DAC26',legend=False, title='The products which generate the most revenue.', show_figure=True)
    
    # making dashboard with Grid Layout
    plots = pandas_bokeh.plot_grid([[p_bar2, p_pie, p_line],[p_stack2, p_bar, p_stack]], plot_width=400)
    return plots


if __name__ == '__main__':
    create_dashboard(PATH, OUTPUT_PATH)
