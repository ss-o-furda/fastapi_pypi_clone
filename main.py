from pathlib import Path

import fastapi
import fastapi_chameleon
import uvicorn
from starlette.staticfiles import StaticFiles

from views import account, home, packages
from data import db_session

api = fastapi.FastAPI()


def main():
    configure(dev_mode=True)
    uvicorn.run(api, host='127.0.0.1', port=8000)


def configure(dev_mode: bool):
    configure_templates(dev_mode)
    configure_routes()
    configure_db(dev_mode)


def configure_templates(dev_mode: bool):
    fastapi_chameleon.global_init('templates')


def configure_db(dev_mode: bool):
    file = (Path(__file__).parent / 'db' / 'pypi.sqlite').absolute()
    db_session.global_init(file.as_posix())


def configure_routes():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(account.router)
    api.include_router(packages.router)


if __name__ == "__main__":
    main()
else:
    configure(dev_mode=False)
