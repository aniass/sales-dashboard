import pandas as pd
import pandas_bokeh
from bokeh.io import output_file

PATH = 'C:\Python Scripts\Datasets\supermarket_sales.csv'

output_path = 'C:\\Python Scripts\\Projects_new\\bokeh_project\\sales_dashboard.html'


def make_dashboard(path):
    pandas_bokeh.output_notebook()
    output_file(output_path)
    
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

    # Plotting charts
    colors=['#FDE724', '#D01C8B', '#4DAC26', '#d7191c']
    # plot 1 - line plot
    p_line = days.plot_bokeh(kind="line",y="Total",color='#d01c8b', title='7-day moving average of daily sales.', plot_data_points=True,show_figure=True)

    # plot 2 - bar plot
    p_bar = income_city.plot_bokeh(kind="bar", color='#d01c8b', legend=False, title='Revenue by the city.', show_figure=True)

    # plot 3 - bar plot
    p_bar2 = total_gender.plot_bokeh(kind="bar", legend=False, title='Sales by Product line and Gender.', show_figure=True)

    # plot 4- stacked bar chart
    p_stack = total_customer.plot_bokeh(kind='barh', stacked=True, title='Revenue by City and Customer type.', colormap=colors, show_figure=True)

    # plot 5- pie chart
    p_pie = df.groupby(["Product line"])["Total"].sum().plot_bokeh(kind='pie', y='Total', title='Total sales by products line.',show_figure=True) 

    # plot 6 - stacked bar chart
    p_stack2 = product.plot_bokeh(kind='barh', stacked=True, color='#4DAC26',legend=False, title='The products which generate the most revenue.', show_figure=True)

    plot = pandas_bokeh.plot_grid([[p_bar2, p_pie, p_line],[p_stack2, p_bar, p_stack]], plot_width=400)
    
    return plot


if __name__ == '__main__':
    make_dashboard(PATH)
