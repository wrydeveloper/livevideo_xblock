"""TO-DO: Write a description of what this XBlock is."""
import pkg_resources
import requests
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String


@XBlock.wants('user')
class LivevideostreamingXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    icon_class = 'video'
    house_number = String(
        display_name='HOUSE_NUMBER',
        default='house_number',
        scope=Scope.content,
        help="house number from weihou"
    )
    live_type = String(
        display_name='LIVE_TYPE',
        default='live_type',
        scope=Scope.content,
        help="0 video live and 1 is interactive live"
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

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the LivevideostreamingXBlock, shown to students
        when viewing courses.
        """
        # user_service = self.runtime.service(self, 'user')
        # xb_user = user_service.get_current_user()
        # username = xb_user.opt_attrs.get('edx-platform.username')
        # email=xb_user.emails
        # print('===========================================user_id:')
        # print(xb_user.opt_attrs.get('edx-platform.user_id'))
        # print('===========================================is_staff')
        # print(xb_user.opt_attrs.get('edx-platform.user_is_staff'))
        # print('===========================================email')
        # print(xb_user.opt_attrs.get('edx-platform.email'))
        # email = 'hdxuiabcxn@qq.com'
        # username = 'wry'
        # self.student_live_url = 'https://live.vhall.com/room/embedclient/521181387?email=test%40vhall.com&name=visitor&k=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2&state=%E9%9A%8F%E6%9C%BA%E5%AD%97%E7%AC%A6%E4%B8%B2'
        # self.teacher_live_url = 'https://e.vhall.com/webinar/new-host/521181387'
        html = self.resource_string("static/html/livevideo_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/livevideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/livevideo_view.js"))
        frag.initialize_js('LivevideostreamingXBlock')
        return frag
    
    def studio_view(self, context=None):
        html = self.resource_string("static/html/livevideo_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/livevideo_edit.js"))
        frag.initialize_js('LivevideoEditXBlock')
        return frag

    @XBlock.json_handler
    def save_live_config(self, data, suffix=''):
        self.house_number = data['house_number']
        self.live_type = int(data['live_data'])
        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
        username = xb_user.opt_attrs.get('edx-platform.username')
        email=xb_user.emails
        
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
        if self.live_type == 0:
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
