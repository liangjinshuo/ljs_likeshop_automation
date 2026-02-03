import requests

from project_likeshop.config.application_config import *


#likeshop平台登录
def login_api():
    #请求载体设置
    data = {
        "account": number,
        "password": password,
        "client": 5
    }
    #发送请求
    response = requests.post(
        url=LOGIN_URL,
        json=data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    try:
        return response.json()
    except ValueError:
        # 解析失败时返回原始文本，方便排查问题
        return {"code": -1, "msg": "响应不是JSON格式", "response_text": response.text}


#likeshop平台首页搜索（模糊搜索）
def query_api(token,page_size=20, name=""):
    params = {
        "page_size": page_size,
        "name": name
    }

    headers = {
        "Cookie": f"token={token}",
        "Token": token
    }
    # 3. 发送 GET 请求（params 自动拼接参数到 URL）
    try:
        res = requests.get(
            url=GOODS_URL,  # 基础 URL，无参数
            params=params,        # 动态参数，自动拼接
            headers=headers,
            timeout=3
        )
        print(f"📌 实际请求 URL：{res.url}")  # 调试：打印最终拼接的 URL
        return res.json()
    except Exception as e:
        return {"code": -1, "msg": f"搜索异常：{str(e)}"}

#likeshop平台搜索后下单
#点击立即购买
def buy_api_01(token):
    data = {
    "action": "info",
    "goods": [
        {
            "item_id": 1,
            "num": 1
        }
    ],
    "delivery_type": 1
}
    headers = {
        "Cookie": f"token={token}",
        "Token": token
    }
    try:
        res = requests.post(
            url=BUYS_URL,
            json=data,
            headers=headers,
            timeout=5
        )
        print(f"📌 实际请求 URL：{res.url}")
        return res.json()
    except Exception as e:
        return {"code": -1, "msg": f"搜索异常：{str(e)}"}
#提交订单
def buy_api_02(token):
    data1 = {
        "action": "submit",
        "delivery_type": 1,
        "goods": [{"item_id": 1, "num": 1}],
        "use_integral": 0,
        "address_id": "",
        "remark": ""
    }
    headers = {
        "Cookie": f"token={token}",
        "Token": token
    }
    try:
        res = requests.post(
            url=BUYS_URL,
            json=data1,
            headers=headers,
            timeout=5
        )
        print(f"📌 实际请求 URL：{res.url}")
        res_json = res.json()

        #提取订单id，供后面其他接口可以方便传参
        order_id = res_json.get("data", {}).get("order_id")
        res_json["order_id"] = order_id
        return res_json
    except Exception as e:
        return {"code": -1, "msg": f"提交订单异常：{str(e)}", "order_id": None}

#使用账户余额支付
def buy_api_03(token, order_id):
    data = {
        "order_id": order_id,
        "pay_way": 3,
        "order_source": 5
    }
    headers = {
        "Cookie": f"token={token}",
        "Token": token
    }
    try:
        res = requests.post(
            url=pcPrepay,
            json=data,
            headers=headers,
            timeout=5
        )
        print(f"📌 实际请求 URL：{res.url}")
        return res.json()
    except Exception as e:
        return {"code": 1, "msg": f"支付异常：{str(e)}"}

#查看订单列表（全部订单、待支付、已下单）
def get_order_list_api(token, order_type="all", page_size=10, page_no=1):
    # 映射订单类型到config中的URL常量
    order_url_map = {
        "all": ALL_LIST,
        "pay": PAY_LIST,
        "delivery": DELIVERY_LIST,
        "finish": FINISH_LIST,
        "close": CLOSE_LIST
    }
    # 校验订单类型合法性
    if order_type not in order_url_map:
        return {"code": -1, "msg": f"不支持的订单类型：{order_type}，仅支持{list(order_url_map.keys())}"}

    # 获取对应类型的基础URL
    base_url = order_url_map[order_type]
    # 构造请求参数（覆盖/补充基础URL的参数）
    params = {
        "page_size": page_size,
        "page_no": page_no,
        "type": order_type
    }
    headers = {
        "Cookie": f"token={token}",
        "Token": token
    }

    try:
        res = requests.get(
            url=base_url,
            params=params,  # 覆盖基础URL的page_size/page_no/type参数
            headers=headers,
            timeout=5
        )
        print(f"📌 【{order_type}订单】实际请求URL：{res.url}")
        return res.json()
    except Exception as e:
        return {"code": -1, "msg": f"{order_type}订单列表请求异常：{str(e)}"}