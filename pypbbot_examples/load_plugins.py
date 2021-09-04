# python -m pypbbot_examples.load_plugins
import asyncio

from pypbbot.plugin import _loadedPlugins, load_plugins

asyncio.run(load_plugins("pypbbot_examples\\plugins"))
print(_loadedPlugins)
