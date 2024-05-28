import asyncio
from bot import start_bot, check_lots
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv


async def main():
    load_dotenv()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_lots, "interval", seconds=5)
    scheduler.start()

    while True:
        asyncio.run(start_bot())
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

