from .utils import trim_extra_whitespace

# Agent系统基础提示词
SYSTEM_PROMPT = trim_extra_whitespace("""
你是一个具备工具调用能力的智能Agent。
当你需要调用工具时，请输出标准工具调用格式；若无工具可调用，直接自然语言回复用户。
""")

# 无签名推理块降级模板（灰度开关生效时使用）
THINKING_DOWNGRADE_PROMPT = trim_extra_whitespace("""
检测到无签名推理块，不再启用结构化思考输出，请将思考内容融合到正文回答中。
""")

# 工具清洗前置提示词
TOOL_STRIP_PROMPT = trim_extra_whitespace("""
严格过滤孤立、残缺、无法解析的工具调用片段，防止接口返回400参数错误。
""")


def build_agent_prompt(user_query: str, enable_thinking_downgrade: bool, enable_strict_tool_clean: bool) -> str:
    """根据灰度开关动态组装Prompt"""
    segments = [SYSTEM_PROMPT]
    if enable_thinking_downgrade:
        segments.append(THINKING_DOWNGRADE_PROMPT)
    if enable_strict_tool_clean:
        segments.append(TOOL_STRIP_PROMPT)
    segments.append(f"用户问题：{user_query}")
    return "\n\n".join(segments)
