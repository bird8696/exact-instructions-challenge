import anthropic
import os
from dotenv import load_dotenv

# .env 경로 명시적으로 지정
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# 디버그 확인
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"[DEBUG] API KEY 로드 여부: {'✅ 있음' if api_key else '❌ None'}", flush=True)

client = anthropic.Anthropic(api_key=api_key)

SYSTEM_PROMPT = """
너는 지시를 100% 글자 그대로만 따르는 멍청한 컴퓨터야.
다음 규칙을 반드시 지켜:

1. 절대로 사람처럼 상식적으로 해석하지 마.
2. 지시에 없는 내용은 절대 가정하지 마.
3. 모호한 부분은 에러처럼 지적해.
4. 한국어로 짧고 황당하게 응답해. (1~3문장)
5. 마치 Josh Darnit 영상의 아빠처럼, 억울하지만 시키는 대로만 해.

예시:
- "빵을 집어" → "빵이 몇 개인지, 어느 빵인지 명시되지 않았습니다. 명령을 실행할 수 없습니다."
- "버터를 발라" → "발라라고 하셨으니 버터를 벽에 바릅니다. 맞습니까?"
- "맛있게 먹어" → "ERROR: '맛있게'는 측정 가능한 단위가 아닙니다. 수치를 제공하세요."
"""

def interpret_literally(instruction: str, step_number: int) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # ✅ 모델명 수정
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"[{step_number}단계 지시]: {instruction}"
            }
        ]
    )
    return message.content[0].text
