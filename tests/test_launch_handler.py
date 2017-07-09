
import unittest
import os
import handler as sut

class TestLaunchIntentHandler(unittest.TestCase):
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
            }
        }
        self.result = sut.lambda_handler(self.event, self.context)

    def testOutputSpeech(self):
        self.assertEqual(
            self.result['response']['outputSpeech'],
            {
                'text': "Welcome to Pollen Count, you can request the pollen count for your "\
                 "current location by saying 'give me an update'. You can also ask for "\
                 "the count anywhere in the UK by asking, 'what is the pollen count is in "\
                 "Glasgow'. How can I help? ",
                'type': "PlainText"})

    def testCard(self):
        self.assertEqual(
            self.result['response']['card'],
            {
                'title': "Welcome",
                'content': "Welcome to Pollen Count, you can request the pollen count for your "\
                 "current location by saying 'give me an update'. You can also ask for "\
                 "the count anywhere in the UK by asking, 'what is the pollen count is in "\
                 "Glasgow'. How can I help? ",
                'type': "Simple"})

    def testShouldNotEndSession(self):
        self.assertFalse(self.result['response']['shouldEndSession'])

    def testResponse(self):
        self.assertEqual(self.result['sessionAttributes'], {})
        self.assertEqual(self.result['version'], "1.0")

if __name__ == "__main__":
    unittest.main()
