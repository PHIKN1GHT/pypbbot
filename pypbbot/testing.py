from __future__ import annotations

import asyncio
import threading
import time
from typing import Any, Optional

import websockets

from pypbbot.protocol import Frame, PrivateMessageEvent
from pypbbot.server import PyPbBotApp, run_server
from pypbbot.utils import Clips, find_free_port


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


class TestClient:
    __test__ = False

    def __init__(self, server: TestServer, botId: int = -1) -> None:
        self.server = server
        self.botId = botId

    async def connect(self) -> TestClient:
        self.session = await websockets.connect(  # type: ignore[attr-defined]
            "ws://localhost:{}/pbbot".format(self.server.port), extra_headers={"x-self-id": str(self.botId)})
        return self

    async def recvPrivateMessage(self, msg: Clips, sender_id: int = 0) -> None:
        frame = Frame()
        frame.botId, frame.echo, frame.ok = self.botId, "", True
        frame.frame_type = Frame.TPrivateMessageEvent
        event = PrivateMessageEvent()
        event.message.extend(msg.toMessageList())
        event.raw_message = str(msg)
        event.user_id = sender_id
        event.self_id = self.botId
        frame.private_message_event.CopyFrom(event)
        await self.session.send(
            frame.SerializeToString())

    async def expectPrivateReply(self, sender_id: int = 0) -> Clips:
        rawdata = await self.session.recv()
        frame = Frame()
        frame.ParseFromString(rawdata)
        resp = frame.send_private_msg_req
        assert resp != None
        assert resp.user_id == sender_id
        return Clips.fromMessageList(resp.message)
