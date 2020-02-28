import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import sqlite3

import plotly.graph_objs as go
#conn = sqlite3.connect(r"C:\Users\MTGro\Desktop\coding\wineApp\db\wine_data.sqlite")
#c = conn.cursor()
df = pd.read_csv("Extract43871.csv")
df = df[['country', 'description', 'rating', 'price','province','title','variety','winery','color']]
df.head(1)

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

#set the app.layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

#callback to control the tab content
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.H1('Tab 1')
    elif tab == 'tab-2':
        return html.H1('Tab 2')

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(dash_table.DataTable(
                            id='table-sorting-filtering',
                            columns=[
                                {'name': i, 'id': i, 'deletable': True} for i in df.columns
                            ],
                            style_table={'overflowX': 'scroll'},
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px',
                                'whiteSpace': 'normal'
                            },
                            page_current= 0,
                            page_size= 50,
                            page_action='custom',
filter_action='custom',
                            filter_query='',
sort_action='custom',
                            sort_mode='multi',
                            sort_by=[]
                        )
                        )

    elif tab == 'tab-2':
        return html.Div([
    dcc.Graph(
        id='rating-price',
        figure={
            'data': [
                dict(
                    y = df['price'],
                    x = df['rating'],
                    mode ='markers',
                    opacity = 0.7,
                    marker = {
                        'size': 8,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name = 'Price v Rating'
                )
            ],
            'layout': dict(
                xaxis = {'type': 'log', 'title': 'Rating'},
                yaxis = {'title': 'Price'},
                margin = {'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend = {'x': 0, 'y': 1},
                hovermode = 'closest'
            )
        }
    )
])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
# word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
            return [None] * 3
@app.callback(Output('table-sorting-filtering', 'data'),
[Input('table-sorting-filtering', "page_current"),
Input('table-sorting-filtering', "page_size"),
Input('table-sorting-filtering', 'sort_by'),
Input('table-sorting-filtering', 'filter_query')])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
        # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by], ascending=[col['direction'] == 'asc'
            for col in sort_by
            ],
            inplace=False)
#page = page_current
 #   size = page_size
  #  return dff.iloc[page * size: (page + 1) * size].to_dict('records')

if __name__ == "__main__":
    app.run_server()