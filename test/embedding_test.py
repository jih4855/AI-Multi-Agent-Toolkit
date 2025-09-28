import ollama

def get_embedding_example():
    # 임베딩할 텍스트
    text = ["안녕하세요! 저는 AI 어시스턴트입니다.", "오늘 날씨는 어떤가요?", "파이썬으로 임베딩을 생성하는 예제입니다."]
    embeddings = []
    try:
        for i in text:
            # Ollama 임베딩 API 호출
            response = ollama.embeddings(
                model='embeddinggemma',  # 임베딩 모델
                prompt=i  # 임베딩할 텍스트
            )

            # 임베딩 벡터 추출
            embedding = response['embedding']

            print(f"텍스트: {i}")
            print(f"임베딩 차원: {len(embedding)}")
            print(f"첫 10개 값: {embedding[:10]}")

            embeddings.append(embedding)

    except Exception as e:
        print(f"임베딩 생성 오류: {e}")
        return None

    return embeddings

if __name__ == "__main__":
    embeddings = get_embedding_example()
    if embeddings is not None:
        print("모든 임베딩 생성 성공:")
        for i, emb in enumerate(embeddings):
            print(f"텍스트 {i+1}: {emb}")
    else:
        print("임베딩 생성 실패")
    embeddings = get_embedding_example()