from fastapi.testclient import TestClient
from pypbbot import app, logger
from pypbbot.protocol import PrivateMessageEvent, Frame
import time

client = TestClient(app)


def test_websocket() -> None:
    total_times = 50000
    logger.disable('pypbbot')
    with client.websocket_connect("/pbbot", headers={"x-self-id": str(0)}) as ws:
        i = total_times
        time_start = time.time()
        while i > 0:
            event = PrivateMessageEvent()
            frame = Frame()
            frame.botId, frame.echo, frame.ok = 0, "", True
            frame.frame_type = Frame.TPrivateMessageEvent
            frame.private_message_event.CopyFrom(event)
            data = frame.SerializeToString()
            ws.send_bytes(data)
            i -= 1
        time_cost = time.time() - time_start
        logger.debug('\n{} frames has been passed. \nTotal cost: {:.2f} seconds. \nProcessing speed: {:.2f} frames pre second.'.format(
            total_times, time_cost, total_times / time_cost))
