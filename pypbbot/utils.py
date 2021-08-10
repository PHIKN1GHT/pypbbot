from __future__ import annotations

import asyncio
import typing
from functools import partial, wraps

from google.protobuf.internal.containers import BaseContainer  # For type anno

if typing.TYPE_CHECKING:
    from typing import Tuple, Dict, Union, Type, List, Optional, Iterator, Dict, Callable, Any
    from pypbbot.typing import ProtobufBotAPI
    from collections import _OrderedDictKeysView

import copy
import threading
from asyncio import get_event_loop
from collections import OrderedDict
from typing import Coroutine, Mapping, TypeVar

import pypbbot.server
from pypbbot.protocol import (GroupMessageEvent, PrivateMessageEvent,
                              SendGroupMsgReq, SendPrivateMsgReq)
from pypbbot.typing import ProtobufBotMessage as Message


def in_lower_case(text: str) -> str:
    lst: List[str] = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)
    return "".join(lst).lower()


T = TypeVar('T', bound='Clips')


class Clips():
    def __init__(self) -> None:
        self._data: List[Tuple[str, Dict[str, str]]] = []

    def append(self: T, data: Tuple[str, Dict[str, str]]) -> T:
        self._data.append(data)
        return self

    def __add__(self: T, other: Union[T, str, int, float]) -> T:
        clips = copy.deepcopy(self)
        if isinstance(other, Clips):
            clips._data += copy.deepcopy(other._data)
        elif isinstance(other, str) or isinstance(other, int) or isinstance(other, float):
            clips._data += Clips.from_str(str(other))._data
        return clips

    def __radd__(self: T, other: Union[T, str, int, float]) -> T:
        clips = copy.deepcopy(self)
        if isinstance(other, Clips):
            clips._data = copy.deepcopy(other._data) + clips._data
        else:
            clips._data = Clips.from_str(str(other))._data + clips._data
        return clips

    def __str__(self: T) -> str:
        reprstr = ''
        for datum in self._data:
            reprstr += datum[1]['text'] if datum[0] == 'text' else str(
                datum[1])
        return reprstr

    def toMessageList(self: T) -> List[Message]:
        lst: List[Message] = []
        for datum in self._data:
            textmsg = Message()
            textmsg.type = datum[0]
            for item in datum[1].keys():
                textmsg.data[item] = datum[1][item]
            lst.append(textmsg)
        return lst

    @classmethod
    def from_str(cls: Type[T], text: str) -> T:
        return cls().append(("text", {"text": text}))

    @classmethod
    def fromMessageList(cls: Type[T], msgList: BaseContainer[Message]) -> T:
        clips = cls()
        for msg in msgList:
            datum = {}
            for item in msg.data:
                datum[item] = msg.data[item]
            clips._data.append((msg.type, datum))
        return clips

    @classmethod
    def from_image_url(cls: Type[T], url: str) -> T:
        return cls().append(("image", {"url": url}))


KT = TypeVar('KT')
VT = TypeVar('VT')


class LRULimitedDict(Mapping[KT, VT]):
    def __init__(self, capacity: int = 65536):
        self.cache: OrderedDict[KT, VT] = OrderedDict()
        self.capacity = capacity

    def pop(self, key: KT) -> VT:
        return self.cache.pop(key)

    def remove(self, key: KT) -> None:
        self.cache.pop(key)

    def __iter__(self) -> Iterator[KT]:
        return self.cache.__iter__()

    def __len__(self) -> int:
        return self.cache.__len__()

    def __getitem__(self, key: KT) -> VT:
        self.cache.move_to_end(key)
        return self.cache[key]

    def __setitem__(self, key: KT, value: VT) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def __delitem__(self, key: KT) -> None:
        del self.cache[key]

    def keys(self) -> _OrderedDictKeysView[KT]:
        return self.cache.keys()


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(
                        SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


async def sendBackClipsTo(event: Union[GroupMessageEvent, PrivateMessageEvent], clips: Union[Clips, str, int, float]) -> Optional[ProtobufBotAPI]:
    clips = Clips() + clips
    api_content: Optional[Union[SendPrivateMsgReq, SendGroupMsgReq]] = None
    if isinstance(event, PrivateMessageEvent):
        api_content = SendPrivateMsgReq()
        api_content.user_id, api_content.auto_escape = event.user_id, True
    elif isinstance(event, GroupMessageEvent):
        api_content = SendGroupMsgReq()
        api_content.group_id, api_content.auto_escape = event.group_id, True
    api_content.message.extend(clips.toMessageList())
    return await pypbbot.server.send_frame(event.self_id, api_content)

RT = TypeVar('RT')


def wait(async_func: Coroutine[Any, Any, RT]) -> Optional[RT]:
    loop = asyncio.get_event_loop()
    if loop is None:
        return asyncio.run(async_func)
    else:
        try:
            result = loop.create_task(async_func).result()
            return result
        except:
            return None


def asyncify(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @wraps(func)
    async def run(*args: Any, loop: Optional[asyncio.AbstractEventLoop] = None, executor: Any = None, **kwargs: Any) -> Any:
        if loop is None:
            loop = get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


def find_free_port() -> int:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)
