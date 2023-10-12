from dash import dcc, Output, Input
from dash import html

from dasboard.app import app
from dasboard.data import params
from dasboard.figures import (
    get_generation_box_plot,
    get_fitness_box_plot,
)


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-example-graph', 'value'),
)
def render_content(tab):
    if tab == 'tab_fitness':
        return html.Div(
            [
                html.H2('Поиск по набору параметров', className="font title-graph"),
                dcc.Input(
                    id='search-input-individual',
                    className="input-purple",
                    type='text',
                    placeholder='Поиск лучшего по параметрам',
                ),
                dcc.Loading(
                    children=[
                        dcc.Graph(
                            id='individual-graph',
                            figure=get_fitness_box_plot(),
                            className="graph-size font",
                        ),
                    ],
                    type="circle",
                ),
            ],
            className="graph-block",
        )
    elif tab == 'tab_generation':
        return html.Div(
            [
                html.Div(
                    [
                        html.H2('Поиск по набору параметров', className="font title-graph"),
                        dcc.Input(
                            id='search-input-generation',
                            type='text',
                            placeholder='Поиск поколений по параметрам',
                            className="input-purple",
                        ),
                        dcc.Loading(
                            id="loading-2",
                            children=[
                                dcc.Graph(
                                    id='generation-graph',
                                    figure=get_generation_box_plot(),
                                    className="graph-size font",
                                ),
                            ],
                            type="circle",
                        ),
                    ],
                    className="graph-block",
                )
            ],
            className="graph-block",
        )


@app.callback(
    Output('generation-graph', 'figure'),
    Input('search-input-generation', 'value'),
)
def perform_search_generation(search_value: str):
    if search_value is None:
        return get_generation_box_plot()
    search_value = search_value.upper()
    try:
        return get_generation_box_plot(search_value)
    except KeyError:
        return get_generation_box_plot()


@app.callback(
    Output('individual-graph', 'figure'),
    Input('search-input-individual', 'value'),
)
def perform_search_individual(search_value: str):
    if search_value:
        search_value = search_value.upper()
        try:
            return get_fitness_box_plot(search_value)
        except KeyError:
            return get_fitness_box_plot()
    else:
        return get_fitness_box_plot()


@app.callback(
    Output('search-result', 'children'),
    Input('search-input', 'value'),
)
def perform_search(search_value):
    if search_value is None:
        return ""

    search_value = str(search_value).upper()
    result = params[params['Номер параметров'] == search_value]

    if result.empty:
        return f"Номер параметров {search_value} не найден"

    params_find = result['Параметры'].iloc[0]
    filename_find = result['Название файла'].iloc[0]
    result_string = f"{params_find}\nНазвание файла: {filename_find}"
    result_html = html.Div(
        children=[
            html.P(
                children=f'Параметры {search_value}:',
            ),
            html.Div(
                className='grid-container',
                children=[
                    html.P(
                        children=children,
                        className='p-default',
                    )
                    for children in result_string.split('\n')
                    if children
                ],
            ),
        ],
        className='font',
    )
    return result_html
