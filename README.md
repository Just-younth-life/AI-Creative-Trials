# AI Creative Trials
本仓库是个人AI创意试验项目集，专注轻量化AI产品原型开发与持续迭代：
- **创意落地**：可运行Demo，覆盖多智能体协同、网页AI应用、RAG知识库、提示词工程、长文本解析；
- **方案沉淀**：配套完整产品资料：PRD、竞品分析、交互规范、可部署前端代码；
- **行业思考**：记录AI产品落地、人机交互、幻觉治理、商业化、出海产品差异化思路。
  
全部项目低门槛复现，适用于学习实践、创业原型验证。

## 项目直达网页
三思集：https://just-youth-life.github.io/AI-Creative-Trials/project-Ai-assessment-sansiji/

松间知宁：https://just-youth-life.github.io/AI-Creative-Trials/project-sensor-songjianzhining/

松间知宁-手机端原型交互预览页：https://just-youth-life.github.io/AI-Creative-Trials/project-sensor-viewing/

## Agent 智能体模块（轻量化多模型调度框架）
本模块实现灰度策略驱动的AI智能体，支持多家海外大模型厂商接入，面向AI创意产品原型验证。
agent/config_const.py # 产品灰度开关常量定义
agent/config_loader.py # 配置加载、校验、单例管理
agent/schema.py # Pydantic 结构化数据模型
agent/ exceptions.py # 统一业务异常
agent/utils.py # 通用工具函数
agent/prompt_templates.py # 动态提示词模板
agent/tool_provider.py # 多模型代理工厂（Azure / Bedrock / Minimax）
agent/agent_core.py # Agent 核心调度逻辑
### 核心亮点
1. **灰度配置驱动功能**：无需修改业务代码、无需重启服务，通过开关控制推理策略、工具清洗逻辑，模拟真实产品A/B灰度运营；
2. **工厂模式多模型兼容**：统一封装多家海外LLM代理，新增模型厂商只需要扩展代理类；
3. **分层解耦架构**：配置层→核心调度→模型代理层→HTTP接入层，同时支持CLI脚本调用与Web API调用；
4. **强类型约束**：基于Pydantic做入参、配置校验，提前拦截非法配置与请求。
接口地址：`POST /api/agent/chat`

## 快速运行
### 安装依赖
```bash
pip install -r requirements.txt

###启动方式
# 方式1：命令行本地调试
python main.py
# 方式2：启动FastAPI HTTP服务
python api_server.py
