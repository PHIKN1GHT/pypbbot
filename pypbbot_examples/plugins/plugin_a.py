from pypbbot.plugin import useFilter


def uselessFilter_a():
    return True


@useFilter(uselessFilter_a)
async def plugin_a_hander():
    return
