from pypbbot import app
from pypbbot.testing import TestServer, TestClient
from pypbbot.utils import Clips, sendBackClipsTo
from pypbbot.typing import PrivateMessageEvent
from pypbbot import BaseDriver
import pytest
import random
import string


class SimpleDriver(BaseDriver):
    async def onPrivateMessage(self, event: PrivateMessageEvent) -> None:
        message = event.raw_message
        if message.startswith('#echo '):
            await sendBackClipsTo(event, message.replace('#echo ', ""))


app.driver_builder = SimpleDriver


@pytest.mark.asyncio
async def test_start_test_server():
    with TestServer(app) as tserver:
        client = await TestClient(tserver).connect()
        somerandomwords = ''.join(random.choices(
            string.ascii_letters + string.digits, k=32))
        await client.recvPrivateMessage(Clips.fromStr("#echo " + somerandomwords))
        assert str(await client.expectPrivateReply()) == somerandomwords
