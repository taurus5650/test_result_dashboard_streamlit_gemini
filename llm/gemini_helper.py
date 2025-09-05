import hashlib
import json
import re

import requests


class GeminiHelper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
        self.cache = {}  # To avoid same data request repeatly

    def _make_cache_key(self, service_team: str, error_list: list[str], date: str) -> str:
        joined = f"{date}::{service_team}" + '\n'.join(error_list)
        return hashlib.md5(joined.encode('utf-8')).hexdigest()

    def anlayze_failure_reason(self, service_team: str, error_list: list[str], date: str) -> dict:
        cache_key = self._make_cache_key(service_team, error_list, date)
        if cache_key in self.cache:
            return self.cache[cache_key]

        prompt = f"""
            You are an expert QA analyst.

            Below is a list of failed test case error messages from the "{service_team}" team:

            {chr(10).join([f"{i + 1}. {e}" for i, e in enumerate(error_list)])}

            Please return your insights in strict **JSON** format with **concise content only**, max 3–5 sentences per section.

            Return:
            {{
              "summary": "...",
              "root_cause_analysis": "...",
              "suggestions": ["...", "..."]
            }}
        """

        headers = {"Content-Type": "application/json"}

        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1024
            }
        }

        response = requests.post(
            url=f'{self.endpoint}?key={self.api_key}',
            headers=headers,
            data=json.dumps(body)
        )

        try:
            content = response.json()['candidates'][0]['content']['parts'][0]['text']
            json_text = re.search(r'\{.*\}', content, re.DOTALL).group()
            result = json.loads(json_text)
            self.cache[cache_key] = result
            return result
        except Exception as e:
            return {
                "summary": "AI anlaysis failed.",
                "root_cause_analysis": str(e),
                "suggestions": ['Please try again later.']
            }
