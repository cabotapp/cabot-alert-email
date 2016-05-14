from django.contrib.auth.models import User
from cabot.cabotapp.tests.tests_basic import LocalTestCase
from cabot.cabotapp.models import Service
from cabot.plugins.models import AlertPluginModel
from mock import Mock, patch
import cabot_alert_email.plugin


class TestEmailAlerts(LocalTestCase):
    def setUp(self):
        super(TestEmailAlerts, self).setUp()

        # Create email alert plugin and attach it to a service
        self.email_alert, created = AlertPluginModel.objects.get_or_create(
                slug='cabot_alert_email')
        self.service.alerts.add(self.email_alert)
        self.service.users_to_notify.add(self.user)
        self.service.save()
        self.service.update_status()
        
        # Set the users email address
        self.email_address = 'test@userprofile.co.uk'
        u = User.objects.get(pk=self.user.pk)
        u.email = self.email_address
        u.save()

    def test_model_attributes(self):
        self.assertEqual(self.service.users_to_notify.all().count(), 1)
        self.assertEqual(self.service.users_to_notify.get(pk=1).username, self.user.username)
        self.assertEqual(self.service.alerts.all().count(), 1)

    @patch('cabot_alert_email.plugin.send_mail')
    def test_send_mail(self, fake_send_mail):
        self.service.overall_status = Service.PASSING_STATUS
        self.service.old_overall_status = Service.ERROR_STATUS
        self.service.save()
        self.service.alert()
        fake_send_mail.assert_called_with(message=u'Service Service http://localhost/service/1/ is back to normal.\n\n', subject='Service back to normal: Service', recipient_list=[u'test@userprofile.co.uk'], from_email='Cabot <cabot@example.com>')

    @patch('cabot_alert_email.plugin.send_mail')
    def test_failure_alert(self, fake_send_mail):
        # Most recent failed
        self.service.overall_status = Service.CALCULATED_FAILING_STATUS
        self.service.old_overall_status = Service.PASSING_STATUS
        self.service.save()
        self.service.alert()
        fake_send_mail.assert_called_with(message=u'Service Service http://localhost/service/1/ alerting with status: failing.\n\nCHECKS FAILING:\n\nPassing checks:\n  PASSING - Port Open Check for Service - Type:  - Importance: Error\n  PASSING - Port Open Check for Service 2 - Type:  - Importance: Error\n\n\n', subject='failing status for service: Service', recipient_list=[u'test@userprofile.co.uk'], from_email='Cabot <cabot@example.com>')
