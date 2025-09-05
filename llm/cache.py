import os
import re
import json
import hashlib
import requests
from dotenv import load_dotenv
import streamlit

from llm.gemini_helper import GeminiHelper

load_dotenv()
GEMINI_HELPER = GeminiHelper(api_key=os.getenv('GEMINI_API_KEY'))


@streamlit.cache_resource
def get_ai_summary_cached(service_team: str, error_list: list[str], date: str) -> dict:
    """
    Caches AI analysis results to avoid repeated token usage on same queries.
    """
    return GEMINI_HELPER.anlayze_failure_reason(
        service_team=service_team,
        error_list=error_list,
        date=date
    )
