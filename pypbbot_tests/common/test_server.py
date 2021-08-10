from pypbbot import app
from pypbbot.logging import logger
from pypbbot.testing import TestServer


def test_start_test_server():
    with TestServer(app) as tserver:
        logger.info(
            "Test Server has been started with port [{}] !".format(tserver.port))
