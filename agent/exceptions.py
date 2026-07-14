class AgentBaseError(Exception):
    """Agent模块基础异常"""
    pass


class ModelProxyError(AgentBaseError):
    """第三方模型代理请求异常"""
    pass


class UnsupportedProviderError(ModelProxyError):
    """不支持的模型厂商"""
    pass


class VersionCheckFailedError(AgentBaseError):
    """Claude版本校验失败"""
    pass


class InvalidToolBlockError(AgentBaseError):
    """非法工具块格式"""
    pass
