from pynhentai.nhentai import *
from sys import platform
import asyncio


if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
