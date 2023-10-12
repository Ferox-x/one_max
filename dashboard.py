import dasboard.callbacks  # noqa

from dash import dcc
from dash import html

from dasboard.app import app
from dasboard.figures import (
    get_best_fitness_histogram,
    get_generation_histogram,
)

app.layout = html.Div(
    [
        html.H1('One Max', className="font title"),
        html.Hr(),
        html.H2('Поиск параметров по коду', className="title-graph font"),
        dcc.Input(
            id='search-input',
            type='text',
            className="input-purple",
            placeholder='Введите код',
        ),
        html.Div(
            id='search-result',
            children=[],
        ),
        dcc.Tabs(
            id="tabs-example-graph",
            value='tab_fitness',
            children=[
                dcc.Tab(
                    label='Ящик с усами (Лучший потомок)',
                    value='tab_fitness',
                    className='font',
                ),
                dcc.Tab(
                    label='Ящик с усами (Поколения)',
                    value='tab_generation',
                    className='font',
                ),
            ],
        ),
        html.Div(id='tabs-content'),
        dcc.Graph(figure=get_best_fitness_histogram()),
        dcc.Graph(figure=get_generation_histogram()),
    ],
    className="container",
)


if __name__ == '__main__':
    app.run_server(
        debug=True,
    )
