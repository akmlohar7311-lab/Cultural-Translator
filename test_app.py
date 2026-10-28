"""Offline unittest suite; does NOT make live Gemini API requests."""
import os
import unittest
from unittest.mock import MagicMock, patch

import app as project


class TranslationTests(unittest.TestCase):
    def test_blank_rejected(self):
        with self.assertRaisesRegex(ValueError, 'enter some text'):
            project.translate_and_localize('  ', 'English', 'Marathi', 'Original', '')

    def test_invalid_target_rejected(self):
        with self.assertRaisesRegex(ValueError, 'valid target'):
            project.translate_and_localize('hi', 'English', 'Klingon', 'Original', '')

    def test_invalid_source_rejected(self):
        with self.assertRaisesRegex(ValueError, 'valid source'):
            project.translate_and_localize('hi', 'Klingon', 'Marathi', 'Original', '')

    def test_invalid_tone_rejected(self):
        with self.assertRaisesRegex(ValueError, 'valid tone'):
            project.translate_and_localize('hi', 'English', 'Marathi', 'Dramatic', '')

    def test_input_too_long(self):
        with self.assertRaisesRegex(ValueError, '4,000'):
            project.translate_and_localize('z' * 4001, 'English', 'Marathi', 'Original', '')

    def test_region_too_long(self):
        with self.assertRaisesRegex(ValueError, '80 characters'):
            project.translate_and_localize('hi', 'English', 'Marathi', 'Original', 'X' * 81)

    def test_missing_api_key(self):
        with patch.dict(os.environ, {'GEMINI_API_KEY': ''}):
            with self.assertRaisesRegex(RuntimeError, 'API key is missing'):
                project.translate_and_localize('Hello', 'English', 'Marathi', 'Original', '')

    def test_model_output_parsed_one_api_call(self):
        response = MagicMock()
        response.text = ('{"standard_translation":"नमस्कार",'
                         '"localized_translation":"नमस्कार!",'
                         '"cultural_note":"कोणताही विशेष सांस्कृतिक बदल नाही."}')
        client = MagicMock()
        client.models.generate_content.return_value = response
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'DUMMY_FOR_TESTING_ONLY'}):
            with patch.object(project.genai, 'Client', return_value=client):
                basic, localized, note = project.translate_and_localize(
                    'Hello', 'English', 'Marathi', 'Formal', 'Maharashtra'
                )
        self.assertEqual(basic, 'नमस्कार')
        self.assertEqual(localized, 'नमस्कार!')
        self.assertTrue(note)
        self.assertEqual(client.models.generate_content.call_count, 1)
        client.close.assert_called_once()
        self.assertIn('An apple a day', client.models.generate_content.call_args.kwargs['contents'])

    def test_model_empty_output(self):
        client = MagicMock()
        client.models.generate_content.return_value.text = None
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'DUMMY_FOR_TESTING_ONLY'}):
            with patch.object(project.genai, 'Client', return_value=client):
                with self.assertRaisesRegex(RuntimeError, 'empty response'):
                    project.translate_and_localize('Hello', 'English', 'Marathi', 'Original', '')
        client.close.assert_called_once()

    def test_model_malformed_json(self):
        client = MagicMock()
        client.models.generate_content.return_value.text = 'not-json'
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'DUMMY_FOR_TESTING_ONLY'}):
            with patch.object(project.genai, 'Client', return_value=client):
                with self.assertRaisesRegex(RuntimeError, 'unexpected result'):
                    project.translate_and_localize('Hello', 'English', 'Marathi', 'Original', '')
        client.close.assert_called_once()

    def test_503_readable(self):
        self.assertIn('busy', project.readable_error(Exception('503 UNAVAILABLE')))

    def test_403_readable(self):
        self.assertIn('denied', project.readable_error(Exception('403 PERMISSION_DENIED')))

    def test_homepage_dark_layout_and_controls(self):
        response = project.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn('--base:#080d19', body)
        self.assertIn('id="swap"', body)
        self.assertIn('id="history-items"', body)
        self.assertIn('sessionStorage', body)
        self.assertIn('Akash Lohar', body)
        self.assertLess(body.index('Akash Lohar'), body.index('Rafat Sayyed'))

    def test_post_validation_shows_error_without_api(self):
        response = project.app.test_client().post('/', data={
            'source_text': ' ', 'source_language': 'English',
            'target_language': 'Marathi', 'tone': 'Original', 'region': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter some text', response.get_data(as_text=True))

    def test_post_results_are_html_escaped(self):
        with patch.object(project, 'translate_and_localize', return_value=(
            '<script>alert("x")</script>', 'शुभेच्छा!', 'म्हण')
        ):
            response = project.app.test_client().post('/', data={
                'source_text': 'Break a leg!', 'source_language': 'English',
                'target_language': 'Marathi', 'tone': 'Original', 'region': ''
            })
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('&lt;script&gt;', body)
        self.assertNotIn('<p id="standard-output" class="translated"><script>', body)
        self.assertIn('id="latest-result"', body)


if __name__ == '__main__':
    unittest.main()
