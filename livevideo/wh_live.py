# -*- coding=utf8 -*-
import requests
import json
import time
import logging

log = logging.getLogger(__name__)

CREATE_LIVE_URL = 'http://e.vhall.com/api/vhallapi/v2/webinar/create'


common_param = {
        'auth_type': 1,
        'account': '',
        'password': ''
    }
create_live_param = {
    'player': 1, # 创建直播时的播放器类型。1代表flash播放器，2代表H5播放器，默认为1
    'subject': '', #<30个字符,活动主题
    'start_time': 0,  #时间戳
    #'user_id': '', #通过第三方创建用户接口获取的微吼用户ID，子账号创建活动时此参数必填，管理员账号创建直播时忽略此参数
    'use_global_k': 0, # 默认为0不开启，1为开启,是否针对此活动开启全局K值配置
    'exist_3rd_auth': 0, # 默认为0不开启，1为开启,是否开启第三方K值验证查看说明
    'auth_url': '', # http://domain,<256个字符,第三方K值验证接口URL(exist_3rd_auth为1必填)
    'failure_url': '', #http://domain,<256个字符,第三方K值验证失败跳转URL(可选)
    'introduction': '', # <1024个字符,活动描述
    'topics': '', # 直播话题标签字段,以","(半角符号) 分割可以多个,标签最多为6个,单个标签不超过8个字 格式例: "商务,教育,视频教育"
    'layout': 3, # 1为单视频,2为单文档,3为文档+视频,观看布局.如果is_new_version为1且活动为互动，该参数只能为3， 如果is_new_version为1且活动不为互动，该参数可以选2或3
    'is_new_version': 0, #0为旧版布局,1为新版布局，默认旧版布局。当player参数为2时，is_new_version参数必传且为1。
    'type': 0, #0为公开,1为非公开,个人公开/非公开活动
    'auto_record': 0, #0为否,1为是(默认为否),是否自动回放
    'is_chat': 0, #0为是,1为否(默认为是),是否开启聊天
    'host': '', #<50个字符,可为空,主持人姓名
    'buffer': 3, #>0的数字,可为空,直播延时，单位为秒，默认为3
    #'is_allow_extension': 1 # 默认为1表示开启并发扩展包，传其他参数表示不开启，流量套餐或没有并发扩展包时忽略此参数
}

create_live_error_code = {
    10001: u'账户不存在',
    10002: u'Vhall正在审核API接入权限，接口暂不可用',
    10014: u'直播标题不能为空',
    10059:	u'直播标题不能超过30个字符',
    10013:	u'直播开始时间不能为空,或直播结束时间小于开始时间',
    # '10013':	u'直播结束时间小于开始时间',
    10016:	u'k值验证的验证地址不能为空',
    10026:	u'布局设置参数错误',
    10053:	u'回放设置参数错误',
    10054:	u'聊天设置参数错误',
    10056:	u'buffer设置不能小于0',
    10003:	u'没有可用的扩展包',
    10103:	u'第三方用户对象不存在',
    10104:	u'子账号信息不存在',
    12100:	u'单个话题标签不能超过8个字',
    12101:	u'最多只可添加6个话题标签',
    13202:	u'版本参数错误',
    13203:	u'新版布局不能为单视频',
}


class WH_live(object):
    
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.init_common_param()
        
    def init_common_param(self):
        common_param['account'] = self._username
        common_param['password'] = self._password
        
    def create_live_house(self, param={}):
        for key in param:
            if key in create_live_param.keys():
                create_live_param[key] = param[key]
        
        param = dict(create_live_param.items() + common_param.items())
        res = self.request_data_by_post(CREATE_LIVE_URL, param)
        if 'code' in res and res['code'] == 200:
            return res['data']
        else:
            print(create_live_error_code[res['code']])
            return None
            
    def request_data_by_post(self, url, data):
        res = requests.post(url, data=data)
        log.info(res.content)
        try:
            res = json.loads(res.content)
        except Exception as e:
            log.info(e)
            res = {}
            
        return res
            
# if __name__ == '__main__':
#     username = 'v18250150'
#     password = '8014311'
#     wh = WH_live(username, password)
#     param = {
#         'subject': '测试直播创建直播接口',
#         'start_time': int(time.time())
#     }
#     wh.create_live_house(param)
