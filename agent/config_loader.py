from pydantic import TypeAdapter
from .config_const import PRODUCT_GRAY_CONFIG
from .schema import GrayConfigSchema

# 全局缓存解析后的灰度配置
_GRAY_CONFIG: GrayConfigSchema | None = None


def load_gray_config() -> GrayConfigSchema:
    """加载并校验全局灰度配置，单例缓存"""
    global _GRAY_CONFIG
    if _GRAY_CONFIG is not None:
        return _GRAY_CONFIG

    adapter = TypeAdapter(GrayConfigSchema)
    _GRAY_CONFIG = adapter.validate_python(PRODUCT_GRAY_CONFIG)
    return _GRAY_CONFIG


def get_gray_switch(key: str):
    """快速读取单个灰度配置"""
    cfg = load_gray_config()
    return getattr(cfg, key)
