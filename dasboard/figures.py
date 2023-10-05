import pandas as pd
import plotly.express as px

from utils import RESULTS_DIR

best_found = pd.read_csv(RESULTS_DIR / 'best_found.csv', na_values='')
generation = pd.read_csv(RESULTS_DIR / 'generation.csv', na_values='')


def get_best_fitness_histogram():
    return px.histogram(
        best_found,
        title="Гистограмма распределения (Лучший потомок)",
        color_discrete_sequence=["orange"],
        nbins=15,
        labels={
            'count': 'Количество',
            'value': 'Best Fitness',
        },
    )


def get_generation_histogram():
    return px.histogram(
        generation,
        title="Гистограмма распределения (Поколения)",
        color_discrete_sequence=["orange"],
        nbins=15,
        labels={
            'count': 'Количество',
            'value': 'Количество поколений',
        },
    )


def get_fitness_box_plot(name: str = None):
    if name:
        return px.box(
            data_frame=best_found[name],
            title='График с усами (Лучший потомок)',
            labels={
                'value': 'Best fitness',
                'variable': 'Параметры',
            },
        )
    return px.box(
        data_frame=best_found,
        title='График с усами (Лучший потомок)',
        labels={
            'value': 'Best fitness',
            'variable': 'Параметры',
        },
    )


def get_generation_box_plot(name: str = None):
    if name:
        return px.box(
            data_frame=generation[name],
            title='График с усами (Поколения)',
            labels={
                'value': 'Поколения',
                'variable': 'Параметры',
            },
        )
    return px.box(
        data_frame=generation,
        title='График с усами (Поколения)',
        labels={
            'value': 'Поколения',
            'variable': 'Параметры',
        },
    )
