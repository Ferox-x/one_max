import dash

from utils import BASE_DIR

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder=BASE_DIR / 'assets',
)
