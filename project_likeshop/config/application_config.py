import json
import os


#登录地址
LOGIN_URL = "http://192.168.10.7:6688/api/account/login"
GOODS_URL = "http://192.168.10.7:6688/api/pc/goodsList"
BUYS_URL = "http://192.168.10.7:6688/api/order/buy"
pcPrepay = "http://192.168.10.7:6688/api/payment/pcPrepay"
ALL_LIST = "http://192.168.10.7:6688/api/order/lists?page_size=10&page_no=1&type=all" #全部订单列表
PAY_LIST = "http://192.168.10.7:6688/api/order/lists?page_size=10&page_no=1&type=pay" #待支付订单列表
DELIVERY_LIST = "http://192.168.10.7:6688/api/order/lists?page_size=10&page_no=1&type=delivery" #待收货订单列表
FINISH_LIST = "http://192.168.10.7:6688/api/order/lists?page_size=10&page_no=1&type=finish" #已完成订单列表
CLOSE_LIST = "http://192.168.10.7:6688/api/order/lists?page_size=10&page_no=1&type=close" #已关闭订单列表


#梁今硕账号和密码，目前为固定，项目为likeshop
number = "15237992506"
password = "Ljs0306777"