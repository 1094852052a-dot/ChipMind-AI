import requests
from openai import OpenAI
from core.config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL, OPENAI_API_KEY, OPENAI_MODEL
)
from core.prompts import SYSTEM_PROMPT


def ask_ollama(messages, model=None, temperature=0.2):
    model = model or OLLAMA_MODEL
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": False,
        "options": {"temperature": temperature}
    }
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=300
    )
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("content", "模型没有返回内容。")


def ask_openai(messages, model=None, temperature=0.2):
    if not OPENAI_API_KEY:
        raise RuntimeError("未配置 OPENAI_API_KEY。请在项目根目录 .env 文件中填写。")
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=model or OPENAI_MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=temperature
    )
    return response.choices[0].message.content or "模型没有返回内容。"


def check_ollama():
    response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=8)
    response.raise_for_status()
    data = response.json()
    return [item.get("name", "") for item in data.get("models", [])]
