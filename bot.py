from aiogram.utils import executor

import handlers.client
from create_bot import dp
from handlers import client, manage, common
from loging import printl
from order_DB import Orders, Orders2


async def on_startup(_):
    print('Бот успешно вышел в Телеграм')
    printl('Бот успешно вышел в Телеграм')

Orders()
Orders2()
client.handlers_register(dp)
manage.handlers_register_manage(dp)
common.register_common_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
