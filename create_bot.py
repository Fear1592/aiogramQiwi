from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger


logger.add("debug.json",format="{time}, {level}, {message}",
          level="DEBUG", rotation="20 MB",
          compression="zip")

logger.add("warning.json",format="{time}, {level}, {message}",
          level="WARNING", rotation="20 MB",
          compression="zip")

storage=MemoryStorage()

import config as cfg
from db import DataBase
from pyqiwip2p import QiwiP2P

bot = Bot(cfg.TOKEN_API)
dp = Dispatcher(bot, storage=storage)
db = DataBase('qiwitestappsss.db')
p2p = QiwiP2P(auth_key=cfg.QIWI_TOKEN)