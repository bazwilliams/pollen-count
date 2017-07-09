import unittest
import os
import handler as sut

class TestCancelIntentHandler(unittest.TestCase):
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
                'requestId': 'test-cancelrequest',
                'type': 'IntentRequest',
                'intent': {
                    'name': 'AMAZON.CancelIntent'
                }
            }
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "Thank you for using Pollen Count. Have a nice day! ",
                'type': "PlainText"})

    def testShouldNotHaveCard(self):
        self.assertFalse(self.result['response'].get('card'))

    def testShouldEndSession(self):
        self.assertTrue(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
