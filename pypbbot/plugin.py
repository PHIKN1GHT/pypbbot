from __future__ import annotations

import os
import pkgutil
import typing
from queue import PriorityQueue
from typing import Dict

if typing.TYPE_CHECKING:
    from typing import Dict, Coroutine

from enum import Enum
from importlib.abc import MetaPathFinder, PathEntryFinder
from types import ModuleType
from typing import Any, Callable

from pypbbot.affairs import BaseAffair
from pypbbot.logging import logger

if typing.TYPE_CHECKING:
    from pypbbot.affairs import BaseAffair
    from typing import Dict

import typing

from pypbbot.logging import logger


class HandlerPriority(Enum):
    SYSTEM = 0  # SHOULD NOT USED BY PLUGINS
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, HandlerPriority):
            return NotImplemented
        return self.value < other.value


Filter = Callable[[BaseAffair], bool]
Handler = Callable[[BaseAffair], Coroutine[Any, Any, None]]


class CallableHandler():
    def __init__(self, ftr: Filter, func: Handler, priority: HandlerPriority) -> None:
        self._func = func
        self._ftr = ftr
        self._priority = priority

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CallableHandler):
            return NotImplemented
        return self._priority == other._priority

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CallableHandler):
            return NotImplemented
        return self._priority < other._priority


_loadedPlugins: Dict[str, ModuleType] = {}


async def load_plugins(*plugin_dir: str) -> Dict[str, ModuleType]:
    for _dir in plugin_dir:
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    for module_finder, name, _ in pkgutil.iter_modules(plugin_dir):
        logger.info('Loading module [{}] ...'.format(name))
        if isinstance(module_finder, PathEntryFinder):  # Hack for Type Check
            module = module_finder.find_module(name)
        elif isinstance(module_finder, MetaPathFinder):
            module = module_finder.find_module(name, None)  # SourceFileLoader
        if module is not None:
            _loadedPlugins[name] = module.load_module(name)
    return _loadedPlugins

_handlers: PriorityQueue[CallableHandler] = PriorityQueue()


def _register(name: str, affair_filter: Filter, func: Handler, priority: HandlerPriority) -> None:
    logger.debug('Registering handler [{}] for filter [{}] ...'.format(
        func.__name__, affair_filter.__name__))
    _handlers.put(CallableHandler(affair_filter, func, priority))
