import asyncio
import json

import aio_pika
import uuid
import random


async def main(my_loop):
    connection = await aio_pika.connect_robust(
        f"amqp://guest:guest@localhost:5672/", loop=my_loop
    )

    messages = []
    for i in range(10):

        messages.append(

        {
            "body": {
                "name": f"test{i}",

            },
            "routing_key": "test_RMQ"
        })


    async with connection:
        channel = await connection.channel()

        for message in messages:
            message_str = json.dumps(message.get("body"))
            routing_key = message["routing_key"]
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_str.encode(), correlation_id=random.choice([str(uuid.uuid4()), None]),
                                 headers=message.get('headers')),
                routing_key=routing_key,
            )
            print(f'sent {message_str}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
