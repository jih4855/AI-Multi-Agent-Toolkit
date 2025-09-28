import ollama
import google.generativeai as genai
from openai import OpenAI
import os
import sys
# Ensure module import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from module.llm_agent import LLM_Agent

# 예시 사용법

multi_agent_tasks = {
    "Agent 1": "도시에서 발생하는 환경 문제(대기, 수질, 쓰레기 등)를 정리하고, 가장 시급한 과제를 제시한다.",
    "Agent 2": "친환경 교통수단(대중교통, 자전거, 전기차 등)을 기반으로 지속 가능한 교통 인프라 계획을 제안한다.",
    "Agent 3": "재생에너지(태양광, 풍력, 스마트 그리드 등)를 활용하여 효율적인 에너지 공급 방안을 설계한다.",
    "Agent 4": "도시 공간 구조(공원, 주거, 상업지구 배치 등)를 최적화한다."
}
multi_agent_system_prompts = {
    "Agent 1": "당신은 환경 전문가입니다. 도시의 환경 문제를 분석하고, 가장 시급한 문제를 제시하세요.",
    "Agent 2": "당신은 교통 전문가입니다. 지속 가능한 교통 인프라 계획을 제안하세요.",
    "Agent 3": "당신은 에너지 전문가입니다. 재생에너지를 활용한 에너지 공급 방안을 설계하세요.",
    "Agent 4": "당신은 도시 계획 전문가입니다. 도시 공간 구조를 최적화하는 방안을 제시하세요."
}
user_prompts ={
    "Agent 1": "현재는 테스트 이므로 본인의 역할을 1문장으로 요약해서 답변하세요.",
    "Agent 2": "현재는 테스트 이므로 본인의 역할을 1문장으로 요약해서 답변하세요.",
    "Agent 3": "현재는 테스트 이므로 본인의 역할을 1문장으로 요약해서 답변하세요.",
    "Agent 4": "현재는 테스트 이므로 본인의 역할을 1문장으로 요약해서 답변하세요."
}

order = ["Agent 1", "Agent 2", "Agent 3", "Agent 4"]

import dotenv
import os
dotenv.load_dotenv()

multi_agent = LLM_Agent(model_name="gemma3n", provider="ollama")

agent_responses = {
    name: multi_agent.__call__(multi_agent_system_prompts[name], user_prompts[name], multi_agent_tasks[name])
    for name in order
}
response_list = [agent_responses[name] for name in order]

multi_agent_responses = multi_agent.aggregate_responses(
    "당신은 도시 계획 전문가입니다. 지속 가능한 도시 설계 방안을 제시하세요.",
    "다음은 여러 전문가의 의견입니다. 이를 바탕으로 최종 요약 및 통합된 지속 가능한 도시 설계 방안을 제시하세요.",
    "현재는 테스트 이므로 본인의 역할을 1문장으로 요약해서 답변하세요.",
    response_list
)

print("Agent 1 Response:", agent_responses["Agent 1"])
print("Agent 2 Response:", agent_responses["Agent 2"])
print("Agent 3 Response:", agent_responses["Agent 3"])
print("Agent 4 Response:", agent_responses["Agent 4"])
print("Multi-Agent Responses:", multi_agent_responses)