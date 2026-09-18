"""Offline regression tests: python -m unittest discover -s tests -v."""

import unittest
from unittest.mock import Mock, patch

import requests

from utils import recommendations


class RecommendationTests(unittest.TestCase):
    def setUp(self):
        self.network = {
            "Packet_Loss": 5,
            "Latency": 20,
            "Jitter": 3,
            "Bandwidth_Usage": 40,
        }
        self.weather = {"temperature": 20, "humidity": 50, "condition": "Clear"}
        patcher = patch.object(recommendations.requests, "post")
        self.post = patcher.start()
        self.addCleanup(patcher.stop)
        self.response = Mock()
        self.post.return_value = self.response

    def generate(self):
        return recommendations.generate_network_failure_recommendations(
            self.network, self.weather
        )

    def test_success_and_bounded_request(self):
        self.response.json.return_value = [
            {"generated_text": "<s>1. Check cables.</s>"}
        ]
        self.assertEqual(self.generate(), "1. Check cables.")
        self.assertEqual(self.post.call_args.kwargs["timeout"], (5, 30))
        self.response.raise_for_status.assert_called_once_with()

    def test_transport_failures(self):
        for error in (requests.Timeout("secret"), requests.ConnectionError("secret")):
            with self.subTest(error=type(error).__name__):
                self.post.side_effect = error
                self.assertEqual(self.generate(), recommendations.UNAVAILABLE_MESSAGE)

    def test_http_error_does_not_parse_body(self):
        self.response.raise_for_status.side_effect = requests.HTTPError("secret")
        self.assertEqual(self.generate(), recommendations.UNAVAILABLE_MESSAGE)
        self.response.json.assert_not_called()

    def test_invalid_json(self):
        self.response.json.side_effect = ValueError("invalid JSON")
        self.assertEqual(self.generate(), recommendations.UNAVAILABLE_MESSAGE)

    def test_malformed_payloads(self):
        payloads: list[object] = [
            None,
            {},
            {"error": "loading"},
            [],
            [None],
            ["text"],
            [{}],
            [{"generated_text": None}],
            [{"generated_text": 12}],
            [{"generated_text": "  "}],
            [{"generated_text": "<s></s>"}],
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.response.json.return_value = payload
                self.assertEqual(self.generate(), recommendations.UNAVAILABLE_MESSAGE)

    def test_echoed_prompt_is_removed(self):
        def respond(*args, **kwargs):
            self.response.json.return_value = [
                {"generated_text": kwargs["json"]["inputs"] + "\n1. Inspect router."}
            ]
            return self.response

        self.post.side_effect = respond
        self.assertEqual(self.generate(), "1. Inspect router.")


if __name__ == "__main__":
    unittest.main()
