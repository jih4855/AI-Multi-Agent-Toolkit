#!/usr/bin/env python3
"""
LLM 모델별 응답 스타일 테스트
존댓말 vs 반말 시스템 프롬프트 비교 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module.llm_agent import LLM_Agent

def test_response_styles():
    """
    다양한 LLM 모델에서 존댓말/반말 시스템 프롬프트 테스트
    """

    # 테스트할 모델들
    models = [
        {"name": "gemma3n", "provider": "ollama"},
        {"name": "qwen3:8b", "provider": "ollama"},
        {"name": "gpt-oss:20b", "provider": "ollama"}
    ]

    # 시스템 프롬프트 설정
    system_prompts = {
        "존댓말": "당신은 친절한 AI 어시스턴트입니다. 항상 정중하고 존댓말로 대답해주세요.",
        "반말": "당신은 친절한 AI 어시스턴트입니다. 반말로 대답하면 안되요."
    }

    # 테스트 질문들
    test_questions = [
        "오늘 날씨가 어때요?",
        "Python과 JavaScript 중 어떤 언어를 추천하나요?",
        "맛있는 저녁 메뉴 추천해주세요"
    ]

    print("🤖 LLM 모델별 응답 스타일 테스트 시작!")
    print("=" * 80)

    for model_info in models:
        print(f"\n📋 테스트 모델: {model_info['name']}")
        print("-" * 60)

        try:
            # LLM 에이전트 생성
            agent = LLM_Agent(
                model_name=model_info['name'],
                provider=model_info['provider']
            )

            for style, system_prompt in system_prompts.items():
                print(f"\n🎯 {style} 테스트:")
                print(f"시스템 프롬프트: {system_prompt}")
                print()

                for i, question in enumerate(test_questions, 1):
                    print(f"Q{i}: {question}")

                    try:
                        # LLM에 질문
                        response = agent(
                            system_prompt=system_prompt,
                            user_message=question
                        )

                        print(f"A{i}: {response}")
                        print()

                    except Exception as e:
                        print(f"❌ 질문 {i} 처리 중 오류: {e}")
                        print()

                print("─" * 40)

        except Exception as e:
            print(f"❌ 모델 {model_info['name']} 초기화 실패: {e}")
            continue

    print("\n🎉 테스트 완료!")
    print("\n💡 결과 분석:")
    print("1. 존댓말 요청 → 존댓말로 답변하는지 확인")
    print("2. '반말하면 안되요' → 실제로 반말로 답변하는지 확인 😏")
    print("3. 각 모델이 지시사항을 어떻게 해석하는지 비교")
    print("4. 모델별 응답 스타일과 지시사항 준수도 관찰")

def test_single_model(model_name: str):
    """
    특정 모델만 테스트하는 함수
    """
    print(f"🔍 {model_name} 단일 모델 테스트")
    print("=" * 50)

    agent = LLM_Agent(model_name=model_name, provider="ollama")

    # 간단한 테스트
    questions = [
        ("존댓말 요청", "당신은 친절한 AI입니다. 존댓말로 답변해주세요.", "안녕하세요?"),
        ("반말 금지 😏", "당신은 친절한 AI입니다. 반말로 대답하면 안되요.", "안녕?")
    ]

    for test_name, system_prompt, user_message in questions:
        print(f"\n📌 {test_name} 테스트:")
        response = agent(system_prompt=system_prompt, user_message=user_message)
        print(f"질문: {user_message}")
        print(f"답변: {response}")
        print()

if __name__ == "__main__":
    print("LLM 응답 스타일 테스트 스크립트")
    print("사용법:")
    print("1. 전체 테스트: python test_response_style.py")
    print("2. 단일 모델: python test_response_style.py [모델명]")
    print()

    if len(sys.argv) > 1:
        # 단일 모델 테스트
        model_name = sys.argv[1]
        test_single_model(model_name)
    else:
        # 전체 테스트
        test_response_styles()