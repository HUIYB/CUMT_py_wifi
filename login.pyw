import base64
from win11toast import toast
import requests
import sys
import socket
##获取本地ip地址
def get_ip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip = s.getsockname()[0]
    s.close()
    return ip

if __name__ == "__main__":
    ARG = {"title":"校园网"}
    IP = get_ip()
    Success = "注销页"
    Fail = "上网登录页"
    user_account = '输入学号'
    user_password = '填入用户密码'
    Login_IP = 'http://10.2.5.251/'
    sign_parameter = f'http://10.2.5.251:801/eportal/?c=Portal&a=login&callback=dr1740318353616&login_method=1&user_account={user_account}%40telecom&user_password={user_password}&wlan_user_ip={IP}&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=NAS&jsVersion=3.0&_=1740318341152'
    try:
        de_out = requests.get(sign_parameter,timeout=2).text
        get_out = requests.get(Login_IP,timeout=2).text
    except requests.exceptions.ReadTimeout:
        toast(body="连接登陆网页时因超时而失败",**ARG)
        sys.exit()
    if Success in get_out:
        toast(body='已登录',**ARG)
    elif Fail in get_out:
        base64_end = de_out.find(f'=="')+2
        if base64_end == -1:
            toast(body=f"登陆失败:未知错误",**ARG)
            sys.exit()
        else:
            msg_begin = de_out.find(f'"msg":"')+7
            b64 = de_out[msg_begin:base64_end]
            de_coded_bytes = base64.b64decode(b64)
            de_coded_str = de_coded_bytes.decode("utf-8")
            toast(body=f"登陆失败:{de_coded_str}",**ARG)
    sys.exit()