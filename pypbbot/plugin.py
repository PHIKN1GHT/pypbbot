from __future__ import annotations
import importlib
import zipfile
import zipimport
import sys

import inspect
import os
import pkgutil
import typing
from queue import PriorityQueue
from typing import Dict

if typing.TYPE_CHECKING:
    from typing import Dict

from enum import Enum
from importlib.abc import MetaPathFinder, PathEntryFinder
from types import ModuleType
from typing import Any, Callable, Coroutine, Union

from pypbbot.affairs import BaseAffair
from pypbbot.logging import logger
from pypbbot.utils import asyncify

if typing.TYPE_CHECKING:
    from pypbbot.affairs import BaseAffair
    from typing import Dict

import functools
import typing


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

        for name in os.listdir(_dir):
            if name.endswith(".zip"):
                zippath = os.path.join(_dir, name)
                sys.path.append(zippath)
                module_names: set[str] = set()
                try:
                    with zipfile.ZipFile(zippath) as zipmodule:
                        for filename in zipmodule.namelist():
                            module_name = filename
                            _pathsep = filename.find("/")
                            if _pathsep != -1:
                                module_name = filename[:_pathsep]
                            module_names.add(module_name)
                except:
                    logger.warning("Illegal zip file [{}]. Skipping ...", name)
                for module_name in module_names:
                    logger.info('Loading module [{}] from [{}] ...'.format(
                        module_name, name))
                    try:
                        _loadedPlugins[name] = importlib.import_module(
                            module_name)
                    except:
                        logger.warning('Failed to load [{}]. Possibly illegal module type.'.format(
                            module_name))

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


def _register(affair_filter: Filter, func: Handler, priority: HandlerPriority) -> None:
    logger.debug('Registering handler [{}] for filter [{}] ...'.format(
        func.__name__, affair_filter.__name__))
    _handlers.put(CallableHandler(affair_filter, func, priority))


HandlerCandidate = Union[Callable[[Any],
                                  Coroutine[Any, Any, Any]],  Callable[[Any], Any]]
HandlerDecorator = Callable[[HandlerCandidate], HandlerCandidate]


def useFilter(ftr: Filter, priority: HandlerPriority = HandlerPriority.NORMAL) -> HandlerDecorator:
    '''An decorator to register an affair handler for a specific affait filter.
    Args:
        ftr: the filter function.
        priority: the priority of the handler
    '''
    try:
        getattr(ftr, '__name__')
    except AttributeError:
        logger.error(
            'Unnamed filter funcion detected. You SHOULD NOT use lambda expression.')
        setattr(ftr, '__name__', '[UNKNOWN]')

    def decorator(func: Callable[[BaseAffair], Coroutine[Any, Any, None]]) -> Callable[[BaseAffair], Coroutine[Any, Any, None]]:
        # DO NOT USE LAMBDA EXPRESSION
        if not inspect.iscoroutinefunction(func):
            func = asyncify(func)
            logger.warning(
                "Function {} has been asyncified for being registered.".format(func.__name__))

        _register(ftr, func, priority)

        @functools.wraps(func)
        def wrapper(affair: BaseAffair) -> Coroutine[Any, Any, None]:
            return func(affair)
        return wrapper
    return decorator
