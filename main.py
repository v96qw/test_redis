import asyncio
import hashlib
import json

import aio_pika
import uuid
import random


async def sleep():
    # await asyncio.sleep(random.randint(1,3))
    await asyncio.sleep(1)


async def test(queue):
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            try:
                async with message.process():
                    print(message.body)
                    task = asyncio.create_task(sleep())
                    await task
            except Exception as e:
               print(e)


async def main(my_loop):
    connection = await aio_pika.connect_robust(
        f"amqp://guest:guest@localhost:5672/", loop=my_loop
    )

    sub_channel = await connection.channel()
    await sub_channel.set_qos(prefetch_count=1)
    queue = await sub_channel.declare_queue("test_RMQ", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            try:
                async with message.process():
                    print(message.body)
                    task = asyncio.create_task(sleep())
                    await task
            except Exception as e:
                print(e)
    # tasks = []
    # tasks.append(test(queue))
    # tasks.append(test(queue))
    # await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
