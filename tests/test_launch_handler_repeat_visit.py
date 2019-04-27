import unittest
import os
import mock
import handler as sut

class fakeLocation():
    @property
    def latitude(self):
        return 55.8642

    @property
    def longitude(self):
        return -4.2518
    
    @property
    def city(self):
        return 'glasgow'

class TestLaunchIntentHandlerRepeatVisit(unittest.TestCase):
    @mock.patch.object(sut.Pollen, 'pollencount', "Awful")
    @mock.patch.object(sut.UserData, 'get', lambda self, location: fakeLocation())
    @mock.patch.object(sut.Nominatim, 'geocode', lambda self, city: fakeLocation())
    def setUp(self):
        os.environ['SKILL_ID'] = "TEST_SKILL_ID"
        self.context = {}
        self.event = {
            'session': {
                'sessionId': 'unittest',
                'application': {
                    'applicationId': "TEST_SKILL_ID"
                }
            },
            'request': {
                'requestId': 'test-launchrequest',
                'type': 'LaunchRequest'
            },
            'context': {
                'System': {
                    'user': {
                        'userId': 'TEST_USER_ID'
                    }
                }
            }
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "Welcome back! Today in glasgow, the Pollen Count is Awful",
                'type': "PlainText"})

    def testCard(self):
        self.assertEqual(
            self.result['response']['card'],
            {
                'title': "Pollen Count",
                'content': "Welcome back! Today in glasgow, the Pollen Count is Awful",
                'type': "Simple"})

    def testShouldEndSession(self):
        self.assertTrue(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
