from pypbbot import protocol
from pypbbot.protocol import Frame


def test_api_completeness() -> None:
    for entry in protocol.__dict__:
        if entry.endswith('Req') or entry.endswith('Resp') or entry.endswith('Event'):
            assert getattr(Frame.FrameType, 'T' + entry) != None
