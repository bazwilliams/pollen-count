import unittest
import os
import mock
import handler as sut

class TestLocationRequestIntentHandlerLocationFailure(unittest.TestCase):
    @mock.patch.object(sut.Nominatim, 'geocode', lambda self, city: None)
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
                'requestId': 'test-locationrequest',
                'type': 'IntentRequest',
                'intent': {
                    'name': 'LocationRequestIntent',
                    'slots': {
                        'Location': {
                            'name': 'Location',
                            'value': 'neverland'
                        }
                    }
                }
            },
            'context':{}
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "I'm sorry, I was not able to lookup neverland. "\
                 "You can request the pollen count for your "\
                 "current location by saying 'give me an update'. You can also ask for "\
                 "the count anywhere in the UK by asking, 'what is the pollen count in "\
                 "Glasgow'. How can I help? ",
                'type': "PlainText"})

    def testShouldNotHaveCard(self):
        self.assertFalse(self.result['response'].get('card'))

    def testShouldNotEndSession(self):
        self.assertFalse(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
