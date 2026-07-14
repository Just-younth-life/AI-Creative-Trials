import json
from typing import Any


def safe_json_loads(text: str) -> Any:
    """安全解析JSON，避免直接json.loads抛错"""
    try:
        return json.loads(text)
    except Exception:
        return None


def is_provider_supported(provider: str, support_list: list[str]) -> bool:
    """校验模型厂商是否在支持列表内"""
    return provider.lower() in [p.lower() for p in support_list]


def trim_extra_whitespace(text: str) -> str:
    """清理多余换行与空格，用于prompt预处理"""
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())
