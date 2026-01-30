import time

from conftest import get_login_token
from project_likeshop.api.likeshop_api_url import login_api, query_api, buy_api


class TestLikeShop:
    #登录场景case
    def test_likeshop_login(self):
        res = login_api()
        assert res["code"] == 1 ,f"HTTP状态码错误，实际：{res['code']}"

    time.sleep(3)

    #搜索场景
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

    #下单场景（待支付）
    def test_likeshop_buy(self, get_login_token):
        res = buy_api(get_login_token)
        assert res["code"] == 1,f"接口调用失败：{res['msg']}"