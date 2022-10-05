import asyncio
import random


class OddCounter:

    def __init__(self, end_range):
        self.end = end_range
        self.start = -1

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.start < self.end-1:
            self.start += 2
            return self.start
        else:
            raise StopAsyncIteration


async def main(loop):
    async for c in OddCounter(100):
        print(c)
        await asyncio.sleep(random.randint(1,3))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
