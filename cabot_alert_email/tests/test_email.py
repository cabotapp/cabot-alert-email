from cabot.cabotapp.tests.tests_basic import LocalTestCase
from mock import Mock, patch

from cabot.cabotapp.models import UserProfile, Service
from cabot_alert_email import models
from cabot.cabotapp.alert import update_alert_plugins


class TestEmailAlerts(LocalTestCase):
    def setUp(self):
        super(TestEmailAlerts, self).setUp()

        self.user_profile = UserProfile(user=self.user)
        self.user_profile.save()
        self.user_profile.user.email = "test@userprofile.co.uk"
        self.user_profile.user.save()
        self.service.users_to_notify.add(self.user)
        self.service.save()

        update_alert_plugins()
        self.email_alert = models.EmailAlert.objects.get(title=models.EmailAlert.name)
        self.email_alert.save()

        self.service.alerts.add(self.email_alert)
        self.service.save()
        self.service.update_status()

    def test_model_attributes(self):
        self.assertEqual(self.service.users_to_notify.all().count(), 1)
        self.assertEqual(self.service.users_to_notify.get(pk=1).username, self.user.username)

        self.assertEqual(self.service.alerts.all().count(), 1)

    @patch('cabot_alert_email.models.send_mail')
    def test_send_mail(self, fake_send_mail):
        self.service.overall_status = Service.PASSING_STATUS
        self.service.old_overall_status = Service.ERROR_STATUS
        self.service.save()
        self.service.alert()
        fake_send_mail.assert_called_with(message=u'Service Service http://localhost/service/1/ is back to normal.\n\n', subject='Service back to normal: Service', recipient_list=[u'test@userprofile.co.uk'], from_email='Cabot <cabot@example.com>')

    @patch('cabot_alert_email.models.send_mail'
)    def test_failure_alert(self, fake_send_mail):
        # Most recent failed
        self.service.overall_status = Service.CALCULATED_FAILING_STATUS
        self.service.old_overall_status = Service.PASSING_STATUS
        self.service.save()
        self.service.alert()
        fake_send_mail.assert_called_with(message=u'Service Service http://localhost/service/1/ alerting with status: failing.\n\nCHECKS FAILING:\n\nPassing checks:\n  PASSING - Graphite Check - Type: Metric check - Importance: Error\n  PASSING - Http Check - Type: HTTP check - Importance: Critical\n  PASSING - Jenkins Check - Type: Jenkins check - Importance: Error\n\n\n', subject='failing status for service: Service', recipient_list=[u'test@userprofile.co.uk'], from_email='Cabot <cabot@example.com>')
        