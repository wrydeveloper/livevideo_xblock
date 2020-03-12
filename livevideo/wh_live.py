# -*- coding=utf8 -*-
import requests
import json
import time
import logging

log = logging.getLogger(__name__)

CREATE_LIVE_URL = 'http://e.vhall.com/api/vhallapi/v2/webinar/create'
UPDATE_LIVE_URL = 'http://e.vhall.com/api/vhallapi/v2/webinar/update'
DELETE_LIVE_URL = 'http://e.vhall.com/api/vhallapi/v2/webinar/delete'
UPLOAD_FILE_URL= 'http://e.vhall.com/api/vhallapi/v2/webinar/doc'
GET_LIVE_START_URL = 'http://e.vhall.com/api/vhallapi/v2/webinar/start'

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

update_live_param = {
    'webinar_id': 0,
    'subject': '', #<30个字符,活动主题
    'start_time': 0,  #时间戳
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
    'buffer': 3 #>0的数字,可为空,直播延时，单位为秒，默认为3
}

get_live_start_param = {
    'webinar_id': 0,
    'is_sec_auth': 0,
    'is_interact': 0
}

delete_live_param = {
    'webinar_id': 0
}

upload_file_param = {
    'webinar_id': 0
}


try:
    with open('wh_error_code.json', 'r+') as f:
        error_code = json.load(f)
except Exception as e:
    error_code = {}

class WH_live(object):
    
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.init_common_param()
        
    def init_common_param(self):
        common_param['account'] = self._username
        common_param['password'] = self._password
        
    def create_live_house(self, param={}):
        '''
        :param param:
        :return: house number or None
        '''
        for key in param:
            if key in create_live_param.keys():
                create_live_param[key] = param[key]
        
        param = dict(create_live_param.items() + common_param.items())
        res_data = self.request_data_by_post(CREATE_LIVE_URL, param)
        return res_data
    
    def update_live_house(self, param={}):
        '''
        :param param:
        :return: house number or None
        '''
        for key in param:
            if key in update_live_param.keys():
                update_live_param[key] = param[key]
        param = dict(update_live_param.items() + common_param.items())
        res_data = self.request_data_by_post(UPDATE_LIVE_URL, param)
        return res_data
    
    def get_live_url(self, param={}):
        '''
        :param param:
        :return: url or None
        '''
        for key in param:
            if key in get_live_start_param.keys():
                get_live_start_param[key] = param[key]
        param = dict(get_live_start_param.items() + common_param.items())
        res_data = self.request_data_by_post(GET_LIVE_START_URL, param)
        return res_data
    
    def delete_live_house(self, house_number):
        '''
        :param house_number:
        :return: house number or None
        '''
        delete_live_param['webinar_id'] = house_number
        param = dict(delete_live_param.items() + common_param.items())
        res_data = self.request_data_by_post(DELETE_LIVE_URL, param)
        return res_data
    
    def post_file_to_video(self, house_number, file_path):
        '''
        :param house_number:
        :param file_path:
        :return: [] or None
        '''
        files = {'resfile': open(file_path, 'rb')}
        upload_file_param['webinar_id'] = house_number
        upload_file_param['resfile'] = open(file_path, 'rb')
        param = dict(upload_file_param.items() + common_param.items())
        res_data = self.request_data_by_post(UPLOAD_FILE_URL, param, files=files)
        return res_data

    def request_data_by_post(self, url, data, files={}):
        if files:
            res = requests.post(url, files=files, data=data)
        else:
            res = requests.post(url, data=data)
        try:
            res = json.loads(res.content)
            log.info('weihou_content:' + str(res))
        except Exception as e:
            log.error(e)
            res = {}
        
        if 'code' in res and res['code'] == '200':
            return res['data']
        else:
            if str(res['code']) in error_code.keys():
                log(error_code[str(res['code'])].encode('utf-8'))
            else:
                log(res['msg'])
            return None
            
# if __name__ == '__main__':
#     username = 's45311060'
#     password = 'wry19950107'
#     # username = 's45011331'
#     # password = '19880419'
#     wh = WH_live(username, password)
#     param = {
#         'subject': '测试直播创建直播接口',
#         'start_time': int(time.time())
#     }
    # wh.delete_live_house(521181387)
    
    # wh.create_live_house(param)
    # wh.post_file_to_video(602352767, './python.pdf')