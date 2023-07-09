import time
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import binascii  # 二进制和ASCII转换模块
import requests


def encrypt_data(msg, secret):
    # 创建AES密码器，使用ECB模式
    cipher = AES.new(secret.encode(), AES.MODE_ECB)
    # 对数据进行加密，并填充
    encrypted_data = cipher.encrypt(pad(msg.encode('utf-8'), AES.block_size))
    # 将加密后的数据转换为十六进制并返回字符串形式
    return binascii.hexlify(encrypted_data).decode()


def whiteList():
    # 获取本机公网ip
    ip = requests.get("https://speed.neu.edu.cn/getIP.php").text
    timestamp = int(time.time())
    # 账号密码:提取密码:时间戳
    data = f'账号密码:提取密码:{timestamp}'
    key = 'XXXXXXXXX'
    sign = encrypt_data(data, key)
    params = {
        "no": "XXXXXX",
        "ip": ip,
        "sign": sign,
        "replace": "1"
    }
    res = requests.get("https://service.ipzan.com/whiteList-add", params=params)
    print(res.text)


def extract(num=1, area=None):
    params = {
        "no": "套餐编号",
        "secret": "密钥",
        "num": num,
        "mode": "whitelist",  # 默认
        "minute": "3",  # 1 3 5 10 15 30
        "format": "txt",
        "area": area,
        "pool": "ordinary",
        "protocol": "1"  # 默认
    }
    res = requests.get("https://service.ipzan.com/core-extract", params=params)
    ip_text = res.text
    ip_list = ip_text.split("\r\n")
    return ip_list
