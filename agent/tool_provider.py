from typing import Dict
from .schema import AgentResponse
from .exceptions import UnsupportedProviderError, ModelProxyError
from .config_loader import load_gray_config
from .utils import is_provider_supported


class BaseModelProxy:
    """第三方模型代理基类"""
    async def chat_completion(self, prompt: str) -> AgentResponse:
        raise NotImplementedError


class AzureProxy(BaseModelProxy):
    async def chat_completion(self, prompt: str) -> AgentResponse:
        # 此处替换真实azure sdk请求逻辑
        return AgentResponse(content="azure model reply", provider="azure")


class MinimaxProxy(BaseModelProxy):
    async def chat_completion(self, prompt: str) -> AgentResponse:
        return AgentResponse(content="minimax model reply", provider="minimax")


class BedrockProxy(BaseModelProxy):
    async def chat_completion(self, prompt: str) -> AgentResponse:
        return AgentResponse(content="bedrock model reply", provider="bedrock")


class ModelProxyFactory:
    _mapping: Dict[str, BaseModelProxy] = {
        "azure": AzureProxy(),
        "minimax": MinimaxProxy(),
        "bedrock": BedrockProxy()
    }

    @classmethod
    def get_proxy(cls, provider: str) -> BaseModelProxy:
        gray_cfg = load_gray_config()
        if not is_provider_supported(provider, gray_cfg.third_party_proxy_support):
            raise UnsupportedProviderError(f"不支持的模型厂商: {provider}")
        instance = cls._mapping.get(provider.lower())
        if not instance:
            raise ModelProxyError("代理实例不存在")
        return instance
