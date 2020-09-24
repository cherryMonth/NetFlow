from sanic import Sanic
from sanic.response import json
from time import ctime
import asyncio

app = Sanic()


async def task_sleep():
    print("sleep before", ctime())
    await asyncio.sleep(5)
    print("sleep after", ctime())


@app.route("/")
async def test(request):
    my_loop = request.app.loop
    my_loop.create_task(task_sleep())
    return json({"hello": "world"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
