"""
Agent internals —— Utility modules extracted from original run_agent.py

# Module Design Purpose
This subpackage stores pure stateless utility functions & self-contained data classes,
which were originally embedded in the 3600-line monolithic run_agent.py main file.

# Architecture Split Benefit
1. Separation of concerns: run_agent.py only retains core AIAgent orchestrator scheduling logic;
2. Reusable universal tools for all creative music generation tasks;
3. Isolate AI hallucination check, lyric syllable calibration, arrangement filter utilities;
4. Reduce main file code volume, lower iteration risk & bug impact range.

# Module Scope Definition
All code here belongs to underlying support layer, NOT core business orchestration:
- Lyric line word count equalization checker
- AI generate anti-hallucination parameter lock tool
- Arrangement instrument whitelist/blacklist filter
- BPM, melody MIDI matching verification tool
- Standard SOP text generation helper
"""
# 对外暴露核心类、异常、模型，方便上层导入
from .agent_core import AiCreativeAgent
from .schema import AgentRequest, AgentResponse
from .exceptions import AgentBaseError, ModelProxyError

__all__ = [
    "AiCreativeAgent",
    "AgentRequest",
    "AgentResponse",
    "AgentBaseError",
    "ModelProxyError"
]
