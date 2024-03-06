from typing import TYPE_CHECKING, Union

from nonebot.adapters import Bot, Event, Message

from ..segment import Text, Emoji
from ..export import Target, SupportAdapter, MessageExporter, export

if TYPE_CHECKING:
    from nonebot.adapters.console.message import MessageSegment


class ConsoleMessageExporter(MessageExporter["MessageSegment"]):
    def get_message_type(self):
        from nonebot.adapters.console.message import Message

        return Message

    @classmethod
    def get_adapter(cls) -> SupportAdapter:
        return SupportAdapter.console

    def get_message_id(self, event: Event) -> str:
        from nonebot.adapters.console.event import MessageEvent

        assert isinstance(event, MessageEvent)
        return str(event.self_id)

    @export
    async def text(self, seg: Text, bot: Bot) -> "MessageSegment":
        ms = self.segment_class
        style = seg.extract_most_style()
        if style and style.startswith("markup"):
            _style = style.split(":", 1)[-1]
            return ms.markup(seg.text, _style)
        if style and style.startswith("markdown"):
            code_theme = style.split(":", 1)[-1]
            return ms.markdown(seg.text, code_theme)
        return ms.text(seg.text)

    @export
    async def emoji(self, seg: Emoji, bot: Bot) -> "MessageSegment":
        ms = self.segment_class

        return ms.emoji(seg.name or seg.id)

    async def send_to(self, target: Union[Target, Event], bot: Bot, message: Message):
        from nonebot.adapters.console import Bot as ConsoleBot

        assert isinstance(bot, ConsoleBot)
        if TYPE_CHECKING:
            assert isinstance(message, self.get_message_type())
        if isinstance(target, Event):
            target = self.get_target(target, bot)
        return await bot.send_msg(user_id=target.id, message=message)
