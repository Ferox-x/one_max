import dash
import pandas as pd
import plotly.express as px

from dash import dcc
from dash import html

from utils import RESULTS_DIR


best_found = pd.read_csv(RESULTS_DIR / 'best_found.csv', na_values='')
generation = pd.read_csv(RESULTS_DIR / 'generation.csv', na_values='')

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
        dcc.Graph(figure=fig_best_found),
        dcc.Graph(figure=fig_generation),
        dcc.Graph(figure=histogram_best_found),
        dcc.Graph(figure=histogram_generation),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
