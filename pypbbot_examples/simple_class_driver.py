from pypbbot import app, run_server, BaseDriver
from pypbbot.utils import wait, sendBackClipsTo
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent


class SimpleDriver(BaseDriver):
    def onPrivateMessage(self, event: PrivateMessageEvent) -> None:
        message = event.raw_message
        if message.startswith('#echo '):
            retmsg = 'ECHOING "{}" FROM MSG_ID {}'.format(
                message.replace('#echo ', ""), event.message_id)
            wait(sendBackClipsTo(event, retmsg))

    async def onGroupMessage(self, event: GroupMessageEvent) -> None:
        message = event.raw_message
        if message.startswith('#echo '):
            retmsg = 'ECHOING "{}" FROM MSG_ID {}'.format(
                message.replace('#echo ', ""), event.message_id)
            wait(sendBackClipsTo(event, retmsg))


app.driver_builder = SimpleDriver

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost',
               port=8082, reload=True)  # type: ignore
