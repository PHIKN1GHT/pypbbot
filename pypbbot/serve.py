# python -m pypbbot.serve
import click

from pypbbot import app, run_server
from pypbbot.driver import AffairDriver

app.driver_builder = AffairDriver


@click.command()
@click.option("--host", default='localhost', show_default=True, help='Host address.')
@click.option("--port", default=8080, show_default=True, help='Port number.')
@click.option("--plugin_path", default='plugins', show_default=True, help='Plugin path.')
@click.option("--reload/--no-reload", default=False, show_default=True, help='Whether to enable hot-reload.')
def serve(host: str, port: int, plugin_path: str, reload: bool) -> None:
    app.plugin_path = plugin_path
    run_server(app='pypbbot.serve:app', host=host,
               port=port, reload=reload)  # type: ignore


if __name__ == '__main__':
    serve()
