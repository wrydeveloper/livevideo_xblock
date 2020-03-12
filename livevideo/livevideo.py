# -*- coding:utf-8 -*-
"""TO-DO: Write a description of what this XBlock is."""
import pkg_resources
import requests
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from django.template import Context, Template


@XBlock.wants('user')
class LivevideostreamingXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    icon_class = 'video'
    house_number = Integer(
        display_name='HOUSE_NUMBER',
        default=100,
        scope=Scope.content,
        help="house number from weihou"
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
        default=1,
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

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

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
        """
        The primary view of the LivevideostreamingXBlock, shown to students
        when viewing courses.
        """
        # self.student_live_url = 'https://live.vhall.com/room/embedclient/435712157?email=test%40vhall.com&name=visitor&k=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2&state=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2'
        # self.teacher_live_url = 'https://e.vhall.com/webinar/new-host/435712157'
        html = self.resource_string("static/html/livevideo_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/livevideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/livevideo_view.js"))
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
            'auto_record': self.auto_record
        }
        
        html = self.render_template('static/html/livevideo_edit.html', context)
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/jquery.cxcalendar.css"))
        frag.add_javascript(self.resource_string("static/js/src/jquery.cxcalendar.js"))
        frag.add_javascript(self.resource_string("static/js/src/livevideo_edit.js"))
        frag.initialize_js('LivevideoEditXBlock')
        return frag

    @XBlock.json_handler
    def save_live_config(self, data, suffix=''):
        if 'house_number' in data or data['house_number'] != 100:
            self.house_number = data['house_number']
        
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        username = xb_user.opt_attrs.get('edx-platform.username')
        email = xb_user.emails
        
        # username, password = self._getweihou_userinfo()
        # wh = WH_live(username, password)
        # param = {
        #     'subject': '测试直播创建直播接口',
        #     'start_time': int(time.time())
        # }
        # house_number = wh.create_live_house(param)
        # if house_number is None:
        #     house_number = self.house_number
        
        self.student_live_url = 'https://live.vhall.com/room/embedclient/{house_number}?email={email}&name={username}&k=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2&state=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2'.\
                                format(house_number=self.house_number, email=email[0], username=username)
        if data['live_type'] == '0':
            self.teacher_live_url = 'https://e.vhall.com/webinar/new-host/{house_number}'.format(house_number=self.house_number)
        else:
            self.teacher_live_url = 'https://e.vhall.com/webinar/new-interact/{house_number}'.format(house_number=self.house_number)
        
        return {'msg': 'success'}
    
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
