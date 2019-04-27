import unittest
import os
import mock
import handler as sut

class fakeAddress():
    def __init__(self, uri, *args, headers=None, allow_redirects=False):
        return

    @property
    def status_code(self):
        return 200

    def json(self):
        return {
            "stateOrRegion" : "",
            "city" : "Glasgow",
            "countryCode" : "UK",
            "postalCode" : "",
            "addressLine1" : "",
            "addressLine2" : "",
            "addressLine3" : "",
            "districtOrCounty" : ""
        }

class fakeLocation():
    @property
    def latitude(self):
        return 55.8642

    @property
    def longitude(self):
        return -4.2518

class TestHomeRequestIntentHandler(unittest.TestCase):
    @mock.patch.object(sut.Pollen, 'pollencount', "Awful")
    @mock.patch.object(sut.Nominatim, 'geocode', lambda self, city: fakeLocation())
    @mock.patch.object(sut.requests, 'get', fakeAddress)
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
                            'consentToken': 'TEST_CONSENT_TOKEN'
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
                'text': "Today in Glasgow, the Pollen Count is Awful",
                'type': "PlainText"})

    def testCard(self):
        self.assertEqual(
            self.result['response']['card'],
            {
                'title': "Pollen Count",
                'content': "Today in Glasgow, the Pollen Count is Awful",
                'type': "Simple"})

    def testShouldEndSession(self):
        self.assertTrue(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
