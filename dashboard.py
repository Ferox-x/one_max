import dash
import pandas as pd
import plotly.express as px

from dash import dcc, Output, Input
from dash import html

from utils import RESULTS_DIR


best_found = pd.read_csv(RESULTS_DIR / 'best_found.csv', na_values='')
generation = pd.read_csv(RESULTS_DIR / 'generation.csv', na_values='')
params = pd.read_csv(RESULTS_DIR / 'params.csv')

fig_best_found = px.box(
    data_frame=best_found,
    title='График с усами (Лучший потомок)',
    labels={
        'value': 'Best fitness',
        'variable': 'Параметры',
    },
)

fig_best_found.update_layout(
    height=800,
    width=1900,
)

fig_generation = px.box(
    data_frame=generation,
    title='График с усами (Поколения)',
    labels={
        'value': 'Поколения',
        'variable': 'Параметры',
    },
)

fig_generation.update_layout(
    height=800,
    width=1900,
)

histogram_best_found = px.histogram(
    best_found,
    title="Гистограмма распределения (Лучший потомок)",
    color_discrete_sequence=["orange"],
    nbins=15,
    labels={
        'count': 'Количество',
        'value': 'Best Fitness',
    },
)

histogram_best_found.update_layout(
    height=800,
    width=1900,
)

histogram_generation = px.histogram(
    generation,
    title="Гистограмма распределения (Поколения)",
    color_discrete_sequence=["orange"],
    nbins=15,
    labels={
        'count': 'Количество',
        'value': 'Количество поколений',
    },
)

histogram_generation.update_layout(
    height=800,
    width=1900,
)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1('One Max'),
        html.H2('Поиск параметров по коду'),
        dcc.Input(id='search-input', type='text', placeholder='Введите код'),
        html.Div(id='search-result'),
        html.H2('Индивида по параметрам'),
        dcc.Input(id='search-input-individual', type='text', placeholder='Поиск лучшего по параметрам'),
        dcc.Graph(id='individual-graph', figure=fig_best_found),
        dcc.Input(id='search-input-generation', type='text', placeholder='Поиск поколений по параметрам'),
        dcc.Graph(id='generation-graph', figure=fig_generation),
        dcc.Graph(figure=histogram_best_found),
        dcc.Graph(figure=histogram_generation),
    ]
)


@app.callback(
    Output('generation-graph', 'figure'),
    Input('search-input-generation', 'value'),
)
def perform_search_generation(search_value: str):
    if search_value is None:
        return fig_generation
    search_value = search_value.upper()
    try:
        return px.box(
            data_frame=generation[search_value],
            title='График с усами (Поколения)',
            labels={
                'value': 'Поколения',
                'variable': 'Параметры',
            },
        )
    except KeyError:
        return fig_generation


@app.callback(
    Output('individual-graph', 'figure'),
    Input('search-input-individual', 'value'),
)
def perform_search_individual(search_value: str):
    if search_value is None:
        return fig_best_found
    search_value = search_value.upper()
    try:
        return px.box(
            data_frame=best_found[search_value],
            title='График с усами (Лучший потомок)',
            labels={
                'value': 'Best fitness',
                'variable': 'Параметры',
            },
        )
    except KeyError:
        return fig_best_found


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
    return f"Параметры {search_value}:\n{params_find}, Название файла: {filename_find}"


if __name__ == '__main__':
    app.run_server(debug=True)
