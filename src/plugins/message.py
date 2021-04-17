import json
import re

from aiocqhttp import Event, Message, MessageSegment
from nonebot import CommandSession, CQHttpError, get_bot, on_command

bot = get_bot()
@bot.on_message
async def handle_message(event: Event):
    '''
        解析收到的信息并给出自动回复.
        目前的功能有:
            将收到的包含有json(比如说QQ小程序分享)的消息转为纯文本消息并发送回去.
    '''
    params = event.copy()
    message: Message = params['message']
    del params['message']
    new_message = await parse_message(message)
    if new_message:
        try:
            print('[qq_bot.plugin.miniprogram] INFO: 准备发送信息.')
            await bot.send_msg(**params, message=new_message)
        except CQHttpError:
            print('[qq_bot.plugin.miniprogram] ERROR: 发送信息"{}"失败.'.format(new_message))

async def parse_message(message: Message) -> Message:
    has_json = False
    new_message = Message()
    for segement in message:
        new_segement, flag = await parse_segement(segement)
        has_json = has_json or flag
        if (not new_segement is None):
            new_message.append(await parse_segement(segement))
    return new_message if has_json else None

async def parse_segement(segement: MessageSegment) -> MessageSegment, bool:
    '''
        解析并处理json消息段.
    '''
    if segement.type == 'json':
        data: str = segement.data['data']

        # 需要先对收到的字符串进行转义, 才能进行json解析
        PATTERNS = ['&#44;', '&#91;', '&#93;']
        REPLACES = [',', '[', ']']
        for index, pattern in enumerate(PATTERNS):
            data = re.sub(pattern, REPLACES[index], data)

        segement_json = json.loads(data)
        prompt = segement_json['prompt']
        descrption = segement_json['meta']['detail_1']['desc']
        link = segement_json['meta']['detail_1']['qqdocurl']
        text = '{}\n{}\n{}'.format(prompt, descrption, link)
        new_segement = MessageSegment.text(text)
        has_json = True
    else:
        new_segement = segement
        has_json = False
    return new_segement, has_json

# # on_command 装饰器将函数声明为一个命令处理器
# # 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
# @on_command('weather', aliases=('天气', '天气预报', '查天气'))
# async def weather(session: CommandSession):
#     # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
#     city = session.get('city', prompt='你想查询哪个城市的天气呢？')
#     # 获取城市的天气预报
#     weather_report = await get_weather_of_city(city)
#     # 向用户发送天气预报
#     await session.send(weather_report)


# # weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# # 命令解析器用于将用户输入的参数解析成命令真正需要的数据
# @weather.args_parser
# async def _(session: CommandSession):
#     # 去掉消息首尾的空白符
#     stripped_arg = session.current_arg_text.strip()

#     if session.is_first_run:
#         # 该命令第一次运行（第一次进入命令会话）
#         if stripped_arg:
#             # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
#             # 例如用户可能发送了：天气 南京
#             session.state['city'] = stripped_arg
#         return

#     if not stripped_arg:
#         # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
#         # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
#         session.pause('要查询的城市名称不能为空呢，请重新输入')

#     # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
#     session.state[session.current_key] = stripped_arg


# async def get_weather_of_city(city: str) -> str:
#     # 这里简单返回一个字符串
#     # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
#     return f'{city}的天气是……'