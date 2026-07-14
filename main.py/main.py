import asyncio
from agent.agent_core import AiCreativeAgent
from agent.schema import AgentRequest
from agent.exceptions import AgentBaseError


async def main():
    # 1. 初始化智能Agent实例
    agent = AiCreativeAgent()

    # 2. 构造用户请求
    request = AgentRequest(
        user_query="帮我构思一条海外休闲游戏新版本运营活动方案",
        session_id="session_20260714_001",
        model_provider="azure"   # 可选 minimax / azure / bedrock
    )

    try:
        # 3. 执行Agent完整调度链路
        result = await agent.run(request)

        # 4. 打印返回结果
        print("==== Agent 响应结果 ====")
        print(f"使用模型厂商：{result.provider}")
        print(f"模型回答内容：\n{result.content}")
        print(f"工具调用列表：{result.tool_calls}")
        print(f"推理思考块：{result.thinking_block}")

    except AgentBaseError as e:
        print(f"Agent运行异常: {type(e).__name__} - {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
