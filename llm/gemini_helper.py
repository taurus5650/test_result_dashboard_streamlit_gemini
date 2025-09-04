import hashlib
import json
import re

import requests


class GeminiHelper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
        self.cache = {}  # To avoid same data request repeatly

    def _make_cache_key(self, service_team: str, error_list: list[str]) -> str:
        joined = service_team + '\n'.join(error_list)
        return hashlib.md5(joined.encode('utf-8')).hexdigest()

    def anlayze_failure_reason(self, service_team: str, error_list: list[str]) -> dict:
        cache_key = self._make_cache_key(service_team=service_team, error_list=error_list)
        if cache_key in self.cache:
            return self.cache[cache_key]

        prompt = f"""
            You are an expert QA analyst. Analyze every dimension of this QA request.
            Below are the error messages from the {service_team} team during a specific testing period:

            {chr(10).join([f"{i + 1}. {e}" for i, e in enumerate(error_list)])}

            Please return your analysis in the following **strict** JSON format with **3 sections**:

            1. `summary`: A high-level English summary of the testing results.
            2. `root_cause_analysis`: A breakdown of error types and potential root causes.
            3. `suggestions`: A to-do list of actionable next steps for the QA or Dev team.

            OUTPUT FORMAT:
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
