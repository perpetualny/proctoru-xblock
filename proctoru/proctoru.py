# -*- coding: utf-8 -*-
"""
    ProctorU is an online proctoring company that allows a candidate to take their exam from home
"""
import datetime
import pkg_resources
import random
import pytz
import dateutil.parser

from django.contrib.auth.models import User
from django.template import Context, Template
from django.utils.translation import ugettext_lazy, ugettext as _
from student.models import CourseEnrollment

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils2.studio_editable import StudioContainerXBlockMixin

from .api import ProctoruAPI
from .models import ProctoruUser

from .timezonemap import win_tz

# Please start and end the path with a trailing slash
loader = ResourceLoader(__name__)


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ProctorUXBlock(StudioContainerXBlockMixin, XBlock):

    """
    TO-DO: document what your XBlock does.
    """

    has_children = True

    display_name = String(display_name=ugettext_lazy("Exam Name"),
                          default="ProctorU XBlock",
                          scope=Scope.settings,
                          help=ugettext_lazy(
                              "This name appears in the horizontal navigation at the top of the page.")
                          )

    start_date = String(display_name=ugettext_lazy("Exam Start Date"),
                        default="2016-03-15T00:27:12.311587+00:00",
                        scope=Scope.settings,
                        help=ugettext_lazy("This will be the exam start date.")
                        )

    end_date = String(display_name=ugettext_lazy("Exam End Date"),
                      default="2016-03-15T00:27:12.311587+00:00",
                      scope=Scope.settings,
                      help=ugettext_lazy("This will be the exam end date.")
                      )

    duration = Integer(display_name=ugettext_lazy("Duration"),
                       default=30,
                       scope=Scope.settings,
                       help=ugettext_lazy("This will be exam duration.")
                       )

    exam_date = String(
        default=None,
        scope=Scope.user_state,
        help=ugettext_lazy("This will be the exam date.")
    )

    exam_time = String(
        default=None,
        scope=Scope.user_state,
        help=ugettext_lazy("This will be the exam time selected by student.")
    )

    password = String(
        default='password',
        scope=Scope.settings,
        help=ugettext_lazy("This will be the password for lock the exam.")
    )

    description = String(display_name=ugettext_lazy("Exam Description"),
                         default="ProctorU exam",
                         scope=Scope.settings,
                         help=ugettext_lazy("This will be Exam Description")
                         )

    notes = String(display_name=ugettext_lazy("Exam Notes"),
                   default="ProctorU Exam Notes",
                   scope=Scope.settings,
                   help=ugettext_lazy("This will be Exam Notes"))

    is_exam_scheduled = Boolean(help=ugettext_lazy("Is exam scheduled?"), default=False,
                                scope=Scope.user_state)

    exam_start_time = String(display_name=ugettext_lazy("Exam Start Time"),
                             default="2016-03-10T11:24:03.305494",
                             scope=Scope.settings,
                             help=ugettext_lazy("This will be exam start time"))

    exam_end_time = String(display_name=ugettext_lazy("Exam End Time"),
                           default="2016-03-10T11:24:03.305494",
                           scope=Scope.settings,
                           help=ugettext_lazy("This will be exam end time"))

    is_exam_completed = Boolean(help=ugettext_lazy("Is exam completed?"), default=False,
                                scope=Scope.user_state)

    is_started = Boolean(help=ugettext_lazy("Is exam completed?"), default=False,
                         scope=Scope.user_state)

    is_rescheduled = Boolean(help=ugettext_lazy("Is exam rescheduled?"), default=False,
                             scope=Scope.user_state)

    is_exam_start_clicked = Boolean(help=ugettext_lazy("Is exam start clicked?"), default=False,
                                    scope=Scope.user_state)

    is_exam_unlocked = Boolean(help=ugettext_lazy("Is exam unlocked?"), default=False,
                               scope=Scope.user_state)

    is_exam_ended = Boolean(help=ugettext_lazy("Is exam ended?"), default=False,
                            scope=Scope.user_state)

    is_exam_canceled = Boolean(help="Is exam canceled?", default=False,
                               scope=Scope.user_state)

    time_zone = String(display_name=ugettext_lazy("Time Zone"),
                       default="Coordinated Universal Time",
                       scope=Scope.settings,
                       help=ugettext_lazy("Time zone of the instructor")
                       )

    student_time_zone = String(display_name=ugettext_lazy("Time Zone"),
                               default="",
                               scope=Scope.user_state
                               )
    student_old_time_zone = String(display_name=ugettext_lazy("Time Zone"),
                                   default="",
                                   scope=Scope.user_state
                                   )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def _is_studio(self):
        """
        This Function checks if call is from CMS or LMS and returns boolean
        True if call is from studio.
        """
        studio = False
        try:
            studio = self.runtime.is_author_mode
        except AttributeError:
            pass
        return studio

    def _user_is_staff(self):
        """
        This Function checks if user is staff and returns boolean
        True if user is staff.
        """
        return getattr(self.runtime, 'user_is_staff', False)

    def _allowed_verified(self):
        """
        This Function checks if user is staff and returns boolean
        True if user is staff.
        """
        course_enrollment = CourseEnrollment.objects.get(
            course_id=self.location.course_key, user=self.runtime.user_id)
        if course_enrollment.mode == 'verified':
            return True
        else:
            return False

    def get_block_id(self):
        """
        Thsi function returns the block id.
        """
        return self.url_name

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ProctorUXBlock, shown to students
        when viewing courses.
        """
        if self._is_studio():  # studio view
            fragment = Fragment(
                self._render_template('static/html/studio.html'))
            fragment.add_css(
                self.resource_string('public/css/proctoru.css'))
            return fragment
        elif self._user_is_staff():
            return self.staff_view()
        elif self._allowed_verified():
            api_obj = ProctoruAPI()
            fragment = Fragment()
            context = {}
            fragment.add_css(loader.load_unicode('public/css/proctoru.css'))
            fragment.add_css(
                loader.load_unicode('public/css/custom_bootstrap.css'))
            fragment.add_javascript(
                loader.load_unicode('static/js/src/proctoru.js'))
            if self.is_exam_ended:
                context.update({"self": self})
                fragment.add_content(
                    loader.render_template('static/html/exam_ended.html', context))
                fragment.initialize_js('ProctorUXBlockExamEnabled')
                return fragment
            if self.is_exam_unlocked:
                context.update({"self": self})
                fragment.add_content(
                    loader.render_template('static/html/exam_enabled.html', context))
                fragment.initialize_js('ProctorUXBlockExamEnabled')
                child_frags = self.runtime.render_children(
                    block=self, view_name='student_view')
                html = self._render_template(
                    'static/html/sequence.html', children=child_frags)
                fragment.add_content(html)
                fragment.add_frags_resources(child_frags)
                return fragment
            elif self.is_exam_start_clicked:
                exam_data = api_obj.get_student_reservation_list(
                    self.runtime.user_id)
                if len(exam_data) > 0:
                    exam_found = False
                    for exam in exam_data:
                        start_date = exam.get('start_date')
                        exam_obj = api_obj.get_schedule_exam_arrived(
                            self.runtime.user_id, self.get_block_id())
                        # check for reseration
                        if int(exam_obj.reservation_no) == int(exam.get('reservation_no')):
                            exam_found = True

                            context.update({
                                "self": self,
                                "exam": api_obj.get_schedule_exam_arrived(self.runtime.user_id, self.get_block_id())
                            })
                            fragment.add_content(
                                loader.render_template('static/html/exam_password.html', context))
                            fragment.initialize_js(
                                'ProctorUXBlockExamPassword')
                            return fragment
                        else:
                            # if reservatin id not found schedule page
                            exam_found = False

                    if not exam_found:
                        # if reservatin id not found return the
                        self.exam_time = ""
                        self.is_exam_scheduled = False
                        self.is_rescheduled = False
                        self.is_exam_canceled = False
                        self.is_exam_start_clicked = False
                        time_details = {
                            'exam_start_date_time': self.start_date,
                            'exam_end_date_time': self.end_date,
                        }

                        time_details = api_obj.get_time_details_api(
                            time_details, self.exam_date)

                        if time_details.get('status') == "examdatepass":
                            context.update(
                                {'self': self, 'status': "examdatepass"})
                            fragment.add_content(
                                loader.render_template('static/html/error_template.html', context))
                        else:
                            context = api_obj.render_shedule_ui(
                                self.runtime.user_id, time_details, self.duration)
                            context.update({'self': self})

                            status = context.get('status')
                            if status == "error":
                                fragment.add_content(
                                    loader.render_template('static/html/error_template.html', context))
                            elif status == "emptylist":
                                fragment.add_content(
                                    loader.render_template('static/html/shedule_form_proctoru.html', context))
                            else:
                                fragment.add_content(
                                    loader.render_template('static/html/shedule_form_proctoru.html', context))

                        fragment.initialize_js('ProctorUXBlockSchedule')
                        return fragment

                else:
                    # if exam not found
                    self.exam_time = ""
                    self.is_exam_scheduled = False
                    self.is_rescheduled = False
                    self.is_exam_canceled = False
                    self.is_exam_start_clicked = False
                    time_details = {
                        'exam_start_date_time': self.start_date,
                        'exam_end_date_time': self.end_date,
                    }

                    time_details = api_obj.get_time_details_api(
                        time_details, self.exam_date)

                    if time_details.get('status') == "examdatepass":
                        context.update(
                            {'self': self, 'status': "examdatepass"})
                        fragment.add_content(
                            loader.render_template('static/html/error_template.html', context))
                    else:
                        context = api_obj.render_shedule_ui(
                            self.runtime.user_id, time_details, self.duration)
                        context.update({'self': self})

                        status = context.get('status')
                        if status == "error":
                            fragment.add_content(
                                loader.render_template('static/html/error_template.html', context))
                        elif status == "emptylist":
                            fragment.add_content(
                                loader.render_template('static/html/shedule_form_proctoru.html', context))
                        else:
                            fragment.add_content(
                                loader.render_template('static/html/shedule_form_proctoru.html', context))

                    fragment.initialize_js('ProctorUXBlockSchedule')
                    return fragment
            elif api_obj.is_user_created(self.runtime.user_id) and self.is_rescheduled:
                time_details = {
                    'exam_start_date_time': self.start_date,
                    'exam_end_date_time': self.end_date,
                }

                time_details = api_obj.get_time_details_api(
                    time_details, self.exam_date)

                if time_details.get('status') == "examdatepass":
                    context.update({'self': self, 'status': "examdatepass"})
                    fragment.add_content(
                        loader.render_template('static/html/error_template.html', context))
                else:
                    context = api_obj.render_shedule_ui(
                        self.runtime.user_id, time_details, self.duration)
                    context.update({'self': self})

                    exam_time_heading = api_obj.get_formated_exam_start_date(
                        self.exam_time, self.runtime.user_id)

                    old_exam_time = dateutil.parser.parse(self.exam_time)

                    exam_start_date_time = time_details.get(
                        'str_exam_start_date')

                    exam_end_date_time = time_details.get('exam_end_date_time')

                    allowed_keep_old_exam = False

                    if exam_start_date_time <= old_exam_time <= exam_end_date_time:
                        allowed_keep_old_exam = True
                    else:
                        allowed_keep_old_exam = False

                    context.update({
                        'exam_time_heading': exam_time_heading,
                        'allowed_keep_old_exam': allowed_keep_old_exam,
                    })
                    context.update({"proctoru_user": api_obj.get_proctoru_user(
                        self.runtime.user_id)})
                    timezones = api_obj.get_time_zones()
                    context.update(
                        {"time_zone_list": timezones.get("data", None)})
                    status = context.get('status')
                    if status == "error":
                        fragment.add_content(
                            loader.render_template('static/html/error_template.html', context))
                    elif status == "emptylist":
                        fragment.add_content(
                            loader.render_template('static/html/reshedule_form_proctoru.html', context))
                    else:
                        fragment.add_content(
                            loader.render_template('static/html/reshedule_form_proctoru.html', context))

                fragment.initialize_js('ProctorUXBlockSchedule')
                return fragment
            elif self.is_exam_scheduled:
                exam_data = api_obj.get_student_reservation_list(
                    self.runtime.user_id)
                context.update({"proctoru_user": api_obj.get_proctoru_user(
                    self.runtime.user_id)})
                timezones = api_obj.get_time_zones()
                context.update({"time_zone_list": timezones.get("data", None)})
                if len(exam_data) > 0:
                    exam_found = False
                    for exam in exam_data:
                        start_date = exam.get('start_date')
                        exam_obj = api_obj.get_schedule_exam_arrived(
                            self.runtime.user_id, self.get_block_id())
                        # check for reseration
                        if int(exam_obj.reservation_no) == int(exam.get('reservation_no')):
                            exam_found = True
                            exam_obj.start_date = dateutil.parser.parse(
                                start_date)
                            exam_obj.save()

                            pr_user = ProctoruUser.objects.get(
                                student=self.runtime.user_id)

                            start_date = dateutil.parser.parse(
                                start_date)

                            start_date = start_date.replace(tzinfo=pytz.utc)
                            tzobj = pytz.timezone(win_tz[pr_user.time_zone])
                            start_date = start_date.astimezone(tzobj)

                            current_time = pytz.utc.localize(
                                datetime.datetime.utcnow()).astimezone(tzobj)

                            diff = start_date-current_time

                            remaining_time = (
                                diff.days * 24 * 60) + (diff.seconds/60)

                            if remaining_time <= -15:
                                # if examtime pass away
                                self.exam_time = ""
                                self.is_exam_scheduled = False
                                self.is_rescheduled = False
                                self.is_exam_canceled = False
                                time_details = {
                                    'exam_start_date_time': self.start_date,
                                    'exam_end_date_time': self.end_date,
                                }

                                time_details = api_obj.get_time_details_api(
                                    time_details, self.exam_date)

                                if time_details.get('status') == "examdatepass":
                                    context.update(
                                        {'self': self, 'status': "examdatepass"})
                                    fragment.add_content(
                                        loader.render_template('static/html/error_template.html', context))
                                else:
                                    context = api_obj.render_shedule_ui(
                                        self.runtime.user_id, time_details, self.duration)
                                    context.update({'self': self})

                                    status = context.get('status')
                                    if status == "error":
                                        fragment.add_content(
                                            loader.render_template('static/html/error_template.html', context))
                                    elif status == "emptylist":
                                        fragment.add_content(
                                            loader.render_template('static/html/shedule_form_proctoru.html', context))
                                    else:
                                        fragment.add_content(
                                            loader.render_template('static/html/shedule_form_proctoru.html', context))

                                fragment.initialize_js(
                                    'ProctorUXBlockSchedule')
                                return fragment
                            else:
                                self.exam_time = start_date.isoformat()

                                context.update(
                                    {"exam": exam_obj, "self": self})

                                fragment.add_content(
                                    loader.render_template('static/html/exam_arrived_proctoru.html', context))
                                fragment.initialize_js('ProctorUXBlockArrived')
                                return fragment
                        else:
                            # if reservatin id not found schedule page
                            exam_found = False

                    if not exam_found:

                        # if reservatin id not found return the
                        self.exam_time = ""
                        self.is_exam_scheduled = False
                        self.is_rescheduled = False
                        self.is_exam_canceled = False
                        time_details = {
                            'exam_start_date_time': self.start_date,
                            'exam_end_date_time': self.end_date,
                        }

                        time_details = api_obj.get_time_details_api(
                            time_details, self.exam_date)

                        if time_details.get('status') == "examdatepass":
                            context.update(
                                {'self': self, 'status': "examdatepass"})
                            fragment.add_content(
                                loader.render_template('static/html/error_template.html', context))
                        else:
                            context = api_obj.render_shedule_ui(
                                self.runtime.user_id, time_details, self.duration)
                            context.update({'self': self})

                            status = context.get('status')
                            if status == "error":
                                fragment.add_content(
                                    loader.render_template('static/html/error_template.html', context))
                            elif status == "emptylist":
                                fragment.add_content(
                                    loader.render_template('static/html/shedule_form_proctoru.html', context))
                            else:
                                fragment.add_content(
                                    loader.render_template('static/html/shedule_form_proctoru.html', context))

                        fragment.initialize_js('ProctorUXBlockSchedule')

                        return fragment

                else:
                    # if exam not found
                    self.exam_time = ""
                    self.is_exam_scheduled = False
                    self.is_rescheduled = False
                    self.is_exam_canceled = False
                    time_details = {
                        'exam_start_date_time': self.start_date,
                        'exam_end_date_time': self.end_date,
                    }

                    time_details = api_obj.get_time_details_api(
                        time_details, self.exam_date)

                    if time_details.get('status') == "examdatepass":
                        context.update(
                            {'self': self, 'status': "examdatepass"})
                        fragment.add_content(
                            loader.render_template('static/html/error_template.html', context))
                    else:
                        context = api_obj.render_shedule_ui(
                            self.runtime.user_id, time_details, self.duration)
                        context.update({'self': self})

                        status = context.get('status')
                        if status == "error":
                            fragment.add_content(
                                loader.render_template('static/html/error_template.html', context))
                        elif status == "emptylist":
                            fragment.add_content(
                                loader.render_template('static/html/shedule_form_proctoru.html', context))
                        else:
                            fragment.add_content(
                                loader.render_template('static/html/shedule_form_proctoru.html', context))

                    fragment.initialize_js('ProctorUXBlockSchedule')
                    return fragment

            elif api_obj.is_user_created(self.runtime.user_id) and not self.is_exam_scheduled:
                self.exam_time = ""
                self.is_exam_scheduled = False
                self.is_rescheduled = False
                self.is_exam_canceled = False
                time_details = {
                    'exam_start_date_time': self.start_date,
                    'exam_end_date_time': self.end_date,
                }

                time_details = api_obj.get_time_details_api(
                    time_details, self.exam_date)

                if time_details.get('status') == "examdatepass":
                    context.update({'self': self, 'status': "examdatepass"})
                    fragment.add_content(
                        loader.render_template('static/html/error_template.html', context))
                else:
                    context = api_obj.render_shedule_ui(
                        self.runtime.user_id, time_details, self.duration)
                    context.update({'self': self})
                    context.update({"proctoru_user": api_obj.get_proctoru_user(
                        self.runtime.user_id)})
                    timezones = api_obj.get_time_zones()
                    context.update(
                        {"time_zone_list": timezones.get("data", None)})
                    status = context.get('status')
                    if status == "error":
                        fragment.add_content(
                            loader.render_template('static/html/error_template.html', context))
                    elif status == "emptylist":
                        fragment.add_content(
                            loader.render_template('static/html/shedule_form_proctoru.html', context))
                    else:
                        fragment.add_content(
                            loader.render_template('static/html/shedule_form_proctoru.html', context))

                fragment.initialize_js('ProctorUXBlockSchedule')
                return fragment
            else:
                api_obj = ProctoruAPI()
                timezones = api_obj.get_time_zones()
                context.update({"self": self})
                context.update({"timezones": timezones.get("data", None)})
                fragment.add_content(
                    loader.render_template('static/html/proctoru.html', context))
                fragment.initialize_js('ProctorUXBlockCreate')
                return fragment
        else:
            fragment = Fragment()
            context = {}
            context.update({"self": self})
            fragment.add_content(
                loader.render_template('static/html/blank.html', context))
            fragment.initialize_js('ProctorUXBlockBlank')
            return fragment

    def _render_template(self, ressource, **kwargs):
        template = Template(self.resource_string(ressource))
        context = dict({}, **kwargs)
        html = template.render(Context(context))
        return html

    def studio_view(self, context=None):
        """This is the view displaying xblock form in studio."""
        api_obj = ProctoruAPI()
        timezones = api_obj.get_time_zones()
        time_zone_list = timezones.get("data")

        fragment = Fragment()

        fragment.add_content(loader.render_template('static/html/studio_edit.html',
                                                    {'time_zone_list': time_zone_list,
                                                     'self': self}))
        fragment.add_css(
            self.resource_string('public/css/custom_bootstrap.css'))
        fragment.add_css(self.resource_string('public/css/proctoru.css'))
        fragment.add_javascript(
            self.resource_string("static/js/src/studio_edit.js"))
        fragment.initialize_js('ProctoruStudio')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        This function is used to add values to the xblock student view
        after user instaructor adds proctorU exam block.
        """
        api_obj = ProctoruAPI()

        start_date = data.get('exam_start_date')
        end_date = data.get('exam_end_date')

        start_time = data.get('exam_start_time')
        end_time = data.get('exam_end_time')

        exam_start_datetime = start_date+'/'+start_time
        exam_end_datetime = end_date + '/'+end_time

        tzobj = pytz.timezone(win_tz[data.get("time_zone")])

        start_datetime = datetime.datetime.strptime(
            exam_start_datetime, "%m/%d/%Y/%H:%M")

        start_datetime = start_datetime.replace(tzinfo=pytz.utc)

        start_datetime = api_obj.getexamtime_staff(
            start_datetime.isoformat(), tzobj)

        end_datetime = datetime.datetime.strptime(
            exam_end_datetime, "%m/%d/%Y/%H:%M")

        end_datetime = end_datetime.replace(tzinfo=pytz.utc)

        end_datetime = api_obj.getexamtime_staff(
            end_datetime.isoformat(), tzobj)

        self.display_name = data.get("exam_name", "")
        self.description = data.get("exam_description", "")
        self.duration = data.get("exam_duration", "")
        self.start_date = start_datetime
        self.end_date = end_datetime
        self.exam_start_time = data.get("exam_start_time", "")
        self.exam_end_time = data.get("exam_end_time", "")
        self.notes = data.get("exam_notes", "")
        self.time_zone = data.get("time_zone")

        return {'status': 'success'}

    def author_edit_view(self, context):
        """This Function is overriddedn from StudioContainerXBlockMixin to allow
        the addition of children blocks."""
        fragment = Fragment()
        self.render_children(context, fragment, can_reorder=True, can_add=True)
        return fragment

    def staff_view(self):
        """
        Primary view for instructor to Set exam using proctorU xBlock.
        """
        api_obj = ProctoruAPI()

        students = api_obj.get_student_sessions(
            self.get_block_id())

        fragment = Fragment()

        fragment.add_content(loader.render_template('static/html/staff-view.html',
                                                    {'self': self,
                                                     'students': students, }))
        fragment.add_css(
            self.resource_string('public/css/custom_bootstrap.css'))
        fragment.add_css(self.resource_string('public/css/proctoru.css'))
        fragment.add_javascript(
            self.resource_string("static/js/src/lms_view.js"))
        fragment.initialize_js('ProctoruStaffBlock')
        return fragment

    @XBlock.json_handler
    def get_time_zones(self, data=None, suffix=None):
        """
        Get time zones by calling getTimeZoneList of ProctorU.
        """
        api_obj = ProctoruAPI()
        return api_obj.get_time_zones()

    @XBlock.json_handler
    def create_proctoru_account(self, data=None, suffix=None):
        """
        Create ProcorU account
        """
        api_obj = ProctoruAPI()
        self.student_old_time_zone = data.get("time_zone")
        self.student_time_zone = data.get("time_zone")
        return api_obj.create_user(self.runtime.user_id, data)

    @XBlock.json_handler
    def get_available_schedule(self, data=None, suffix=None):
        """
        Get available schedule
        """
        self.exam_date = data.get('date')
        return {
            'status': _('success')
        }

    @XBlock.json_handler
    def reschedule_exam(self, data=None, suffix=None):
        """
        Get available schedule
        """
        self.student_old_time_zone = self.student_time_zone
        self.is_rescheduled = True
        return {
            'status': _('success')
        }

    @XBlock.json_handler
    def start_exam(self, data=None, suffix=None):
        """
        Get available schedule
        """
        api_obj = ProctoruAPI()
        exam_data = api_obj.get_schedule_exam_arrived(
            User.objects.get(pk=self.runtime.user_id), self.get_block_id())
        reservation_data = api_obj.begin_reservation(
            self.runtime.user_id, exam_data.reservation_id, exam_data.reservation_no)
        if reservation_data.get('response_code') == 2:
            if len(reservation_data.get('message')) > 28:
                if reservation_data.get('message')[:28] == 'Reservation is in the future':
                    return {
                        'status': _('error'),
                        #FR 'msg': _(u"S'il vous plaît attendre le moment et essayez de nouveau."),
						'msg': _('Please wait for a moment and try again.'),
                    }
                else:
                    self.is_exam_start_clicked = False
                    self.is_rescheduled = False
                    self.is_exam_scheduled = False
                    return {
                        'status': _('error'),
                        #FR 'msg': _(u"S'il vous plaît Replanifiez Rendez-vous"),
						'msg': _('Please reschedule the appointment'),
                    }
            else:
                self.is_exam_start_clicked = False
                self.is_rescheduled = False
                self.is_exam_scheduled = False
                return {
                    'status': _('error'),
                    #FR 'msg': _(u"S'il vous plaît Replanifiez Rendez-vous"),
					'msg': _('Please reschedule the appointment'),
                }
        elif reservation_data.get('data'):
            if exam_data:
                exam_data.url = reservation_data.get('data').get('url')
                exam_data.save()
            self.is_exam_start_clicked = True
            return {
                'status': _('success'),
                'reservation_data': reservation_data.get('data')
            }
        else:
            return {
                'status': _('error')
            }

    @XBlock.json_handler
    def cancel_exam(self, data=None, suffix=None):
        """
        Get available schedule
        """
        api_obj = ProctoruAPI()
        response_data = api_obj.cancel_exam(
            User.objects.get(pk=self.runtime.user_id), self.get_block_id())
        self.is_exam_canceled = True
        self.is_exam_scheduled = False
        self.is_exam_start_clicked = False
        if response_data.get('response_code') == 1:
            return {
                'status': 'success',
                'msg': 'exam canceled',
            }
        else:
            return {
                'status': 'error',
                'msg': "Already canceled!",
            }

    @XBlock.json_handler
    def unlock_exam(self, data=None, suffix=None):
        """
        Get available schedule
        """
        password = data.get('password')
        if password == self.password:
            self.is_exam_unlocked = True
            api_obj = ProctoruAPI()
            exam_status = api_obj.start_exam(
                User.objects.get(pk=self.runtime.user_id), self.get_block_id())
            if exam_status:
                return {
                    'status': _('success')
                }
            else:
                return {
                    'status': _('error'),
                    'msg': _('Database error'),
                }
        else:
            return {
                'status': _('error'),
                'msg': _("invalid password")
            }

    @XBlock.json_handler
    def end_exam(self, data=None, suffix=None):
        """
        Get available schedule
        """
        self.is_exam_unlocked = False
        self.is_exam_ended = True
        api_obj = ProctoruAPI()
        exam_status = api_obj.end_exam(
            User.objects.get(pk=self.runtime.user_id), self.get_block_id())
        if exam_status:
            return {
                'status': _('success')
            }
        else:
            return {
                'status': _('error'),
                'msg': _('Database error'),
            }

    @XBlock.json_handler
    def get_student_activity(self, data=None, suffix=None):
        """
        Get available schedule
        """
        student_id = data.get("student_id")
        api_obj = ProctoruAPI()
        response_data = api_obj.get_student_activity(
            student_id, self.get_block_id(), self.start_date, self.end_date, self.time_zone)
        return response_data

    @XBlock.json_handler
    def call_addhoc(self, data=None, suffix=None):
        """
        call adhoc process
        """
        api_obj = ProctoruAPI()

        user_data = api_obj.get_user(self.runtime.user_id)

        reservation_id = ''.join(
            random.choice('0123456789ABCDEF') for i in range(40))

        shedule_time = data.get('shedule_time', None)
        try:
            notes =  'Password is - {0}\nExam Notes - {1}'.format(self.password, self.notes)
        except:
            notes = 'Password is - '+self.password.encode('utf-8')+' - '+(self.notes).encode('utf-8')
        student_data = {
            'time_sent': datetime.datetime.utcnow().isoformat(),
            'student_id': str(user_data.get('id', None))[:50],
            'last_name': user_data.get('last_name', None)[:50],
            'first_name': user_data.get('first_name', None)[:50],
            'email': user_data.get('email', None)[:50],
            'address1': user_data.get('address', None)[:100],
            'city': user_data.get('city', None)[:50],
            'country': user_data.get('country', "US")[:2],
            'phone1': str(user_data.get('phone_number', None))[:15],
            'time_zone_id': user_data.get('time_zone', None)[:60],
            'description': u"{0} {1} - {2} \n {3}".format(
                self.location.course_key.course,
                self.location.course_key.run,
                self.display_name,
                self.description
            )[:255],
            'notes': notes,
            'duration': self.duration,
            'start_date': shedule_time,
            'takeitnow': 'N',
            'reservation_id': reservation_id,
            'state': user_data.get('state', None),
        }

        if self.is_rescheduled:
            exam = api_obj.get_schedule_exam_arrived(
                self.runtime.user_id, self.get_block_id())
            if exam:
                student_data['reservation_id'] = exam.reservation_id
                student_data['reservation_no'] = exam.reservation_no

        json_response = api_obj.add_adhoc_process(student_data)
        if json_response.get('response_code') == 1:
            exam_data = {
                "start_date": shedule_time,
                "reservation_id": reservation_id,
                "reservation_no": json_response.get('data').get('reservation_no'),
                "user": User.objects.get(pk=int(user_data.get('id', None))),
                "block_id": self.get_block_id(),
                "url": json_response.get('data').get('url'),
            }
            # when actule schedule done
            self.exam_time = shedule_time
            self.is_exam_scheduled = True
            self.is_rescheduled = False
            self.is_exam_canceled = False

            api_obj.set_exam_schedule_arrived(exam_data)

            return {
                'status': _('success')
            }
        elif json_response.get('response_code') == 2:
            return {
                'status': _('error'),
                'msg': _('exam already scheduled')
            }
        else:
            return {
                'status': _('error'),
                'msg': _('Please contact administrator')
            }

    @XBlock.json_handler
    def cancle_rescheduling(self, data=None, suffix=""):
        """
        Cancel Rescheduling.
        """
        self.is_rescheduled = False
        return {"message": _('success')}

    @XBlock.json_handler
    def edit_proctoru_account(self, data=None, suffix=""):
        api_obj = ProctoruAPI()

        new_time_zone = data.get("time_zone", None)
        self.student_time_zone = new_time_zone
        proctoru_user, self.student_old_time_zone = api_obj.update_proctoru_account(
            self.runtime.user_id, data)
        student_data = {
            'student_id': proctoru_user.student.id,
            'first_name': proctoru_user.student.first_name,
            'last_name': proctoru_user.student.last_name,
            'time_sent': datetime.datetime.utcnow().isoformat(),
            'time_zone_id': proctoru_user.time_zone,
            'address1': proctoru_user.address,
            'city': proctoru_user.city,
            'country': proctoru_user.country,
            'state': proctoru_user.state,
            'phone1': proctoru_user.phone_number
        }

        api_obj.edit_proctoru_user(student_data)

        return {"status": "success"}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ProctorUXBlock",
             """<proctoru/>
             """),
            ("Multiple ProctorUXBlock",
             """<vertical_demo>
                <proctoru/>
                <proctoru/>
                <proctoru/>
                </vertical_demo>
             """),
        ]
