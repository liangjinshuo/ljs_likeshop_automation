import requests

from project_likeshop.config.application_config import LOGIN_URL, GOODS_URL, number, password, BUYS_URL


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
        "Authorization": f"Bearer {token}"  # 常见格式1：Bearer Token
        # 如果你们接口是直接传 token，就写："token": token
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

#likeshop平台搜索后下单（此为进入待支付场景）
def buy_api(token):
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
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.post(
            url=BUYS_URL,
            json=data,
            headers=headers,
            timeout=5
        )
        print(f"📌 实际请求 URL：{res.url}")  # 调试：打印最终拼接的 URL
        return res.json()
    except Exception as e:
        return {"code": -1, "msg": f"搜索异常：{str(e)}"}