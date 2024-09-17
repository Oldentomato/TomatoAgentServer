import redis

# Redis에 연결
r = redis.Redis(host='redis_containerDev', port=6379)

# r.flushdb() # redis안에 값 전부 초기화 (필요시 사용)

try:
    # 모든 키 가져오기
    keys = r.keys("*")  # "*"는 모든 키를 의미합니다.
    
    all_data = {}
    
    for key in keys:
        # 키와 값을 바이트 형식으로 가져옵니다.
        key_bytes = key
        # key_str = key.decode('utf-8')  # 이 부분은 디코딩 없이 바이트로 유지하려면 주석 처리
        value = None
        
        # 키의 타입에 따라 값을 가져옵니다.
        if r.type(key) == b'string':
            value = r.get(key)
        elif r.type(key) == b'hash':
            value = r.hgetall(key)
        else:
            value = f"Unsupported type: {r.type(key)}"
        
        # 결과를 저장
        all_data[key_str] = value
    
    print(all_data)

except redis.RedisError as e:
    print(f"Redis error: {e}")