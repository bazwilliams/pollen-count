import unittest
import os
import mock
import handler as sut

class TestHomeRequestWithNoPermission(unittest.TestCase):
    def setUp(self):
        os.environ['SKILL_ID'] = "TEST_SKILL_ID"
        self.context = {
        }
        self.event = {
            'session': {
                'sessionId': 'unittest',
                'application': {
                    'applicationId': "TEST_SKILL_ID"
                }
            },
            'request': {
                'requestId': 'test-homerequest',
                'type': 'IntentRequest',
                'intent': {
                    'name': 'HomeRequestIntent'
                }
            },
            'context': {
                'System': {
                    'user': {
                        'userId': 'TEST_USER_ID',
                        'permissions': {
                        },
                    },
                    'device': {
                        'deviceId': 'TEST_DEVICE_ID'
                    },
                    'apiEndpoint': 'https://api.eu.amazonalexa.com'
                }
            }
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "I'm sorry, I was not able to lookup your home town. "\
                 "With your permission, I can provide you with this information. "\
                 "Please check your companion app for details",
                'type': "PlainText"})

    def testShouldHaveCard(self):
        self.assertEqual(self.result['response']['card'],
                         {
                             'type': 'AskForPermissionsConsent',
                             'permissions': [
                                 'read::alexa:device:all:address'
                             ]
                         })

    def testShouldEndSession(self):
        self.assertTrue(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
