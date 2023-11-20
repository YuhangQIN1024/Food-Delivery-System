import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
import json
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT


REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"



ACCESS_KEY_ID = 'LTAI5tK3FdB7dwSBXkrfiQR9'
ACCESS_KEY_SECRET = 'dJX056GXGD26Gv73lLAprhWnJCQwDw'
SING_NAME = "hitqyh"
TEMPLATE_CODE = "SMS_275060723"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(phone_numbers, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码
    smsRequest.set_TemplateCode(TEMPLATE_CODE)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号
    business_id = uuid.uuid1()
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(SING_NAME)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    return smsResponse


if __name__ == '__main__':

    params = {
        'code': 1234
    }
    print(send_sms("18346617639", json.dumps(params)))