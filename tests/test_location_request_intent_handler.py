import unittest
import os
import mock
import handler as sut

class TestLocationRequestIntentHandler(unittest.TestCase):
    @mock.patch.object(sut.Pollen, 'pollencount', "Awful")
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
                            'value': 'glasgow'
                        }
                    }
                }
            }
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "Today in glasgow, the Pollen Count is Awful",
                'type': "PlainText"})

    def testCard(self):
        self.assertEqual(
            self.result['response']['card'],
            {
                'title': "Pollen Count",
                'content': "Today in glasgow, the Pollen Count is Awful",
                'type': "Simple"})

    def testShouldEndSession(self):
        self.assertTrue(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
