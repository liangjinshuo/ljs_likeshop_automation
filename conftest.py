import pytest
import requests
from project_likeshop.config.application_config import LOGIN_URL, number, password

@pytest.fixture(scope="session")
def get_login_token():

    req_data = {"account": number, "password": password, "client": 5}
    try:
        response = requests.post(
            url=LOGIN_URL,
            json=req_data,
            headers={"Content-Type": "application/json"},
            timeout=3
        )
        login_res = response.json()
        assert login_res["code"] == 1, f"登录失败：{login_res}"
        assert login_res["data"]["token"] is not None, "token 为空"
        yield login_res["data"]["token"]
    except Exception as e:
        pytest.fail(f"夹具执行失败：{str(e)}")