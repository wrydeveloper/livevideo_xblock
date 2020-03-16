# -*- coding:utf-8 -*-
import time
import pkg_resources
import requests
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from django.template import Context, Template
from wh_live import WH_live


@XBlock.wants('user')
class LivevideostreamingXBlock(XBlock):

    icon_class = 'video'
    live_image_cover = String(
        display_name='LIVE_IMAGE_COVER',
        default='/static/images/default_live_cover.jpeg',
        scope=Scope.content,
        help='Course Live Cover, Show to student'
    )
    house_number = Integer(
        display_name='HOUSE_NUMBER',
        default=100,
        scope=Scope.content,
        help='house number from weihou'
    )
    is_interact = Integer(default=0, scope=Scope.content, help="0 is video and 1 is interact")
    player = Integer(default=1 ,scope=Scope.content, help="player type include h5 and flash player")
    subject = String(
        display_name='SUBJECT',
        default='default subject name',
        scope=Scope.content,
        help='subject name, Must be less than 30 characters'
    )
    introduction = String(
        display_name='SUBJECT',
        default='default introducation',
        scope=Scope.content,
        help='subject name, Must be less than 1024 character'
    )
    layout = Integer(
        display_name='LAYOUT',
        default=3,
        scope=Scope.content,
        help='1 single video, 2 single doc, 3 doc and video'
    )
    is_new_version = Integer(
        display_name='IS_NEW_VERSION',
        default=0,
        scope=Scope.content,
        help='0 is old layout,1 is new layout'
    )
    topics = String(
        display_name='TOPICS',
        default='',
        scope=Scope.content,
        help='Live Topic Tag Field, Must be divided by `,`(Comma), For example: A,B,C'
    )
    is_chat = Integer(
        display_name='IS_CHAT',
        default=0,
        scope=Scope.content,
        help='Start chat in live or close it'
    )
    auto_record = Integer(
        display_name='AUTO_RECORD',
        default=1,
        scope=Scope.content,
        help='Open auto record or close it'
    )
    start_time = String(
        display_name='START_TIME',
        default='1970-01-01 00:00:00',
        scope=Scope.content,
        help='Live start time, type: YYYY:MM:DD HH:mm:SS'
    )
    
    student_live_url = String(
        display_name='STUDENT_LIVE_URL',
        default='student_live_url',
        scope=Scope.content,
        help='hidden msg'
    )
    teacher_live_url = String(
        display_name='TEACHER_LIVE_URL',
        default='teacher_live_url',
        scope=Scope.content,
        help='hidden msg'
    )

    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        username = xb_user.opt_attrs.get('edx-platform.username')
        email = xb_user.emails
        student_live_url = self.student_live_url
        student_live_url = student_live_url.replace('@email@', '{email}').replace('@username@', '{username}')
        context = {
            'teacher_live_url': self.teacher_live_url,
            'student_live_url': student_live_url.format(email=email[0], username=username),
        }
        
        html = self.render_template("static/html/livevideo_view.html", context)
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/livevideo.css"))
        frag.add_javascript(self.load_resource("static/js/src/livevideo_view.js"))
        frag.initialize_js('LivevideostreamingXBlock')
        return frag
    
    def studio_view(self, context=None):
        
        context = {
            'house_number': self.house_number,
            'player': self.player,
            'is_interact': self.is_interact,
            'start_time': self.start_time,
            'subject': self.subject,
            'introduction': self.introduction,
            'layout': self.layout,
            'topics': self.topics,
            'is_chat': self.is_chat,
            'auto_record': self.auto_record,
            'is_new_version': self.is_new_version
        }
        
        html = self.render_template('static/html/livevideo_edit.html', context)
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/calendar.min.css"))
        frag.add_javascript(self.load_resource("static/js/src/livevideo_edit.js"))
        frag.add_javascript(self.load_resource("static/js/src/calendar.min.js"))
        frag.initialize_js('LivevideoEditXBlock')
        return frag

    @XBlock.json_handler
    def save_live_config(self, data, suffix=''):
        for name in ['subject', 'player', 'start_time', 'introduction', 'layout', 'topics', 'is_chat', 'auto_record', 'is_new_version', 'is_interact']:
            if name in data:
                exec("self.{} = data['{}']".format(name, name))
        
        username = 's45311060'
        password = 'wry19950107'
        wh = WH_live(username, password)
        data['start_time'] = int(time.mktime(time.strptime(str(data['start_time']), "%Y-%m-%d %H:%M:%S")))
        if 'house_number' not in data or data['house_number'] == 100:
            res = wh.create_live_house(data)
            if res is not None:
                self.house_number = res
            else:
                return {'msg': 'Failed create live', 'status': 10001, 'data': ''}
        else:
            data['webinar_id'] = self.house_number
            wh.update_live_house(data)
    
        param = {}
        param['webinar_id'] = self.house_number
        param['is_interact'] = self.is_interact
        teacher_url = wh.get_live_url(param)
        if teacher_url:
            if teacher_url.startswith('http'):
                teacher_url = teacher_url.replace('http', 'https')
            self.teacher_live_url = teacher_url
        else:
            return {'msg': 'failed to get live url', 'status': 10002, 'data': ''}
    
        self.student_live_url = 'https://live.vhall.com/room/embedclient/{house_number}?email=@email@&name=@username@&k=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2&state=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2'. \
            format(house_number=self.house_number)
    
        return {'msg': 'success', 'status': 10000, 'data': ''}

    @XBlock.json_handler
    def get_upload_cover_url(self, data, suffix=''):
        url = 'assets/' + self.course_id
        data = {
            'url': url
        }
        return {'msg': 'success', 'status': 10000, 'data': data}
    
    def _getweihou_userinfo(self):
        url = 'localhost:8000/api/v1/weihouaccount/'
        res = requests.get(url)
        content = res.content
        if content['res'] == 'success':
            return content['data']['username'], content['data']['password']

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("livevideo",
             """<vertical_demo>
                <livevideo/>
                </vertical_demo>
             """),
        ]
