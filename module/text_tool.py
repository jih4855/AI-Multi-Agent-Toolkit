import os
import re
import json

class Text_tool:
    def __init__(self, chunk_size:int=1000, overlap:int=0, max_length:int=None):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.max_length = max_length

    
    def split_text_with_overlap(self, text: str) -> list:
        chunks = []
        start = 0

        while start < len(text):
            prev_start = start
            end = start + self.chunk_size

            chunk = text[start:end]
            chunks.append(chunk.strip())

            if end >= len(text):
                break

            start = end - self.overlap

            # 안전장치
            if start <= prev_start:
                start = prev_start + self.chunk_size

        return chunks

    def safe_filename(self, filename:str) -> str:
        """파일명을 안전하게 변환"""
        # 특수문자 제거 및 공백을 언더스코어로 변경
        safe_name = re.sub(r'[<>:"/\\|?*]', '', filename)
        safe_name = re.sub(r'[\'",.]', '', safe_name)
        safe_name = re.sub(r'\s+', '_', safe_name)

        # 길이 제한
        if len(safe_name) > self.max_length:
            safe_name = safe_name[:self.max_length]

        return safe_name


    def save_result_json(self, final_output: str, output_filename: str, save_foldername: str):
        safe_output_filename = self.safe_filename(output_filename)
        safe_save_foldername = self.safe_filename(save_foldername)
        if not os.path.exists(safe_save_foldername):
            os.makedirs(safe_save_foldername, exist_ok=True)

        try:
            # JSON 형태인지 확인하고 저장
            if isinstance(final_output, str):
                try:
                    #'''json ... ``` 형태의 JSON 추출 시도
                    json_match = re.search(r'```json\s*(.*?)\s*```', final_output, re.DOTALL) #LLM 출력에서 JSON 부분만 추출
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        json_str = final_output  # 전체 문자열을 JSON으로 시도
                    json_data = json.loads(json_str)
                    filepath = os.path.join(safe_save_foldername, f"{safe_output_filename}.json")
                    with open(filepath, 'w', encoding='utf-8') as outfile:
                        json.dump(json_data, outfile, ensure_ascii=False, indent=2)
                    print(f"✅ JSON 저장 완료: {filepath}")
                    return
                except json.JSONDecodeError:
                    pass

            # JSON이 아니거나 파싱 실패 시 객체 그대로 저장
            if isinstance(final_output, (dict, list)):
                filepath = os.path.join(safe_save_foldername, f"{safe_output_filename}.json")
                with open(filepath, 'w', encoding='utf-8') as outfile:
                    json.dump(final_output, outfile, ensure_ascii=False, indent=2)
                print(f"✅ JSON 저장 완료: {filepath}")
            else:
                # 텍스트로 저장
                filepath = os.path.join(safe_save_foldername, f"{safe_output_filename}.txt")
                with open(filepath, 'w', encoding='utf-8') as outfile:
                    outfile.write(str(final_output))
                print(f"✅ 텍스트 저장 완료: {filepath}")

        except Exception as e:
            print(f"❌ 저장 오류: {e}")