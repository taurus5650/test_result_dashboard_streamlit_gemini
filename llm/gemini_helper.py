import hashlib
import os
import requests
import json
import re

class GeminiHelper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'
        self.cache = {} # To avoid same data request repeatly

    def _make_cache_key(self, service_team: str, error_list: list[str]) -> str:
        joined = service_team + '\n'.join(error_list)
        return hashlib.md5(joined.encode('utf-8')).hexdigest()

    def anlayze_failure_reason(self, service_team: str, error_list: list[str]) -> dict:
        cache_key = self._make_cache_key(service_team=service_team, error_list=error_list)
        if cache_key in self.cache:
            return self.cache[cache_key]

        prompt = (f"""
            Analyze every dimension of this QA request.
            

        """)



