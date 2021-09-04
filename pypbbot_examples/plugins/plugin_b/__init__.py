from pypbbot.plugin import useFilter


def uselessFilter_b():
    return True


@useFilter(uselessFilter_b)
async def plugin_b_hander():
    return
