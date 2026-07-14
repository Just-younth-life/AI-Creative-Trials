-from .schema import AgentRequest, AgentResponse
from .config_loader import get_gray_switch
from .prompt_templates import build_agent_prompt
from .tool_provider import ModelProxyFactory
from .exceptions import VersionCheckFailedError


class AiCreativeAgent:
    def __init__(self):
        pass

    def _check_claude_version(self):
        """灰度：强制版本校验逻辑演示"""
        if get_gray_switch("oauth_force_claude_version_check"):
            mock_current_version = "claude-2.0"
            allow_version = "claude-3"
            if mock_current_version != allow_version:
                raise VersionCheckFailedError("Claude版本不匹配，请升级模型版本")

    async def run(self, req: AgentRequest) -> AgentResponse:
        # 1. 灰度分支：版本校验
        self._check_claude_version()

        # 2. 根据灰度开关动态组装prompt
        prompt = build_agent_prompt(
            user_query=req.user_query,
            enable_thinking_downgrade=get_gray_switch("enable_unsigned_thinking_downgrade"),
            enable_strict_tool_clean=get_gray_switch("strip_orphan_tool_block_strict")
        )

        # 3. 获取对应厂商模型代理
        proxy = ModelProxyFactory.get_proxy(req.model_provider)

        # 4. 请求大模型
        resp = await proxy.chat_completion(prompt)
        return resp
