from __future__ import annotations

import asyncio
import threading
import time
from typing import Any, Optional

import websockets

from pypbbot.server import PyPbBotApp, run_server
from pypbbot.utils import find_free_port


class TestServer:
    __test__ = False

    def __init__(self, app: PyPbBotApp, port: Optional[int] = None) -> None:
        self.app = app
        if port is None:
            port = find_free_port()
        self.port = port
        self.thread = threading.Thread(target=run_server, kwargs={
                                       "app": app, "port": port})

    def start(self) -> None:
        self.thread.start()

    def exit(self) -> None:
        def shutdown() -> None:
            async def handshake() -> None:
                await websockets.connect(  # type: ignore[attr-defined]
                    "ws://localhost:{}/shutdown".format(self.port))
            asyncio.run(handshake())
            time.sleep(1)
        threading.Thread(target=shutdown).start()

    def __enter__(self) -> TestServer:
        self.start()
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self.exit()
