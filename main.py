from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from iptables.utils import add_target_rule, get_rule_line_num_by_args, get_endpoint_info, update_rule_by_line_num

app = Sanic()


class NetFlowView(HTTPMethodView):
    async def get(self, request):
        get_loop = request.app.loop
        result = get_loop.create_task(get_endpoint_info(**request.json))
        await result
        return json({"received": True, "message": result.result()})

    async def post(self, request):
        """
        添加规则
        :param request:
        :return:
        """
        get_loop = request.app.loop
        result = get_loop.create_task(add_target_rule(**request.json))
        await result
        return json({"received": True, "message": result.result()})

    async def put(self, request):
        """
        更新规则
        :param request:
        :return:
        """
        get_loop = request.app.loop
        result = get_loop.create_task(update_rule_by_line_num(**request.json))
        await result
        return json({"received": True, "message": result.result()})

    async def patch(self, request):
        """
        获取规则行号
        :param request:
        :return:
        """
        get_loop = request.app.loop
        result = get_loop.create_task(get_rule_line_num_by_args(**request.json))
        await result
        return json({"received": True, "message": result.result()})


app.add_route(NetFlowView.as_view(), '/rule', version=1)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
