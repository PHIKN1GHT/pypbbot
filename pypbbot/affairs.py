from __future__ import annotations
import typing

from pypbbot.logging import logger

if typing.TYPE_CHECKING:
    from typing import Optional, Union, Any

    from pypbbot.typing import Event, ProtobufBotMessageEvent

import asyncio

from pypbbot.utils import Clips, sendBackClipsTo


class BaseAffair:
    def __init__(self, event: Optional[Event]) -> None:
        logger.debug(
            'An affair for [{}] has been created.'.format(type(event)))


class ChatAffair(BaseAffair):
    def __init__(self, event: ProtobufBotMessageEvent) -> None:
        super().__init__(event)
        self.event: ProtobufBotMessageEvent = event
        self.receiver_id: int = event.self_id
        self.sender_id: int = event.sender.user_id
        self.text: str = event.raw_message

    async def send(self, clips: Union[Clips, str, int, float]) -> Any:
        return await sendBackClipsTo(self.event, clips)

    def sendAndWait(self, clips: Union[Clips, str, int, float]) -> Any:
        return asyncio.run(self.send(clips))
