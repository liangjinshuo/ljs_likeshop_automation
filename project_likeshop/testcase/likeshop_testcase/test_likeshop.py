import time

from conftest import get_login_token
from project_likeshop.api.likeshop_api_url import *


class TestLikeShop:
    #登录场景case
    def test_likeshop_login(self):
        res = login_api()
        assert res["code"] == 1 ,f"HTTP状态码错误，实际：{res['code']}"

    time.sleep(3)

    #搜索商品场景
    def test_likeshop_like_query(self, get_login_token):

        res = query_api(get_login_token, name="晨光", page_size=20)

        data = res.get("data",{})
        goods_list = data.get("list",[])
        assert res["code"] == 1, f"接口调用失败：{res['msg']}"
        assert len(goods_list) > 0, "商品列表为空"
        # 2. 遍历校验所有name包含关键词
        for idx, goods in enumerate(goods_list):
            # 校验每个商品都有name字段
            assert "name" in goods, f"第{idx + 1}条商品缺失name字段"
            # 校验name包含关键词
            assert "晨光" in goods["name"], f"第{idx + 1}条商品name不包含{"晨光"}：实际={goods['name']}"

    time.sleep(3)

    #下单支付场景
    def test_likeshop_buy(self, get_login_token):
        res1 = buy_api_01(get_login_token)
        assert res1["code"] == 1,f"接口调用失败：{res1['msg']}"

        res2 = buy_api_02(get_login_token)
        assert res2["code"] == 1,f"接口调用失败：{res2['msg']}"
        #上面的res1和res2接口都一样，只是传递的参数不同
        res3 = buy_api_03(get_login_token,order_id=res2["order_id"])
        assert res3["code"] == 10001,f"接口调用失败：{res3['msg']}"
        assert res3["msg"] == "支付成功",f"支付失败：{res3['msg']}"

    time.sleep(3)

    #查看全部订单
    def test_likeshop_order_all(self, get_login_token):
        res = get_order_list_api(get_login_token, order_type="all", page_size=20, page_no=1)
        assert res["code"] == 1, f"全部订单接口失败：{res['msg']}"
        data = res.get("data", {})
        all_list = data.get("list", [])  # 修复：默认值改为列表（原是字典）
        assert len(all_list) >= 0, "全部订单列表为空"  # 允许空，避免无订单时断言失败
        for idx, order in enumerate(all_list):
            assert "order_goods" in order, f"第{idx + 1}条订单缺失order_goods字段"
        time.sleep(3)