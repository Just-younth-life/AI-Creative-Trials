# 产品灰度配置示例
PRODUCT_GRAY_CONFIG = {
    "oauth_force_claude_version_check": True, # 灰度开关：强校验claude版本
    "strip_orphan_tool_block_strict": True, # 灰度：严格清洗孤立工具块防400报错
    "enable_unsigned_thinking_downgrade": True, # 灰度：无签名推理块降级为文本
    "third_party_proxy_support": ["minimax", "azure", "bedrock"] # 可动态新增代理厂商
}
