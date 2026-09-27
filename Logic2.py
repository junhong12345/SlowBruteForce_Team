import json
import os
from pathlib import Path


class SBFDetector:

    def __init__(self):

        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"

        self.file_path = self.app_path / "Logic1_analysis_result.json"
        self.result_file_path = self.app_path / "STD_status_result.json"
        self.filtered_result_path = self.app_path / "STD_filtered_result.json"

        self.data = []

        # std >= 2 저장용
        self.filtered_data = []


    def load_logs(self):

        try:

            if os.path.exists(self.file_path):

                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)

                print(f"{self.file_path} 파일이 성공적으로 로드되었습니다.")

            else:
                print(f"{self.file_path} 파일이 존재하지 않습니다.")

        except Exception as e:
            print(f"파일 로드 중 에러 발생: {e}")


    def detect_bots(self):

        block_count = 0
        additional_analysis_count = 0

        if not self.data:
            print("분석할 데이터가 없음")
            return

        for res in self.data:

            std = res.get("std_deviation")
            count = res.get("connection_count")

            # connection_count가 없는 비정상 데이터
            if count is None:
                continue

            # Logic1에서 5회 이하로 제외된 IP
            if std is None:

                res["status"] = "insufficient"

                print(
                    f"IP : {res['ip']} 데이터 부족 "
                    f"(접속 횟수: {count}회)"
                )

                continue

            # STD < 2 : General Brute Force
            if std < 2:

                res["status"] = "block"

                print(
                    f"IP : {res['ip']} 자동화 공격 "
                    f"(std: {std:.2f})"
                )

                block_count += 1

            # STD >= 2 : CV 추가 분석
            else:

                res["status"] = "needs_additional_analysis"

                self.filtered_data.append(res)

                print(
                    f"IP : {res['ip']} 추가 분석 대상 "
                    f"(std: {std:.2f})"
                )

                additional_analysis_count += 1


        print(f"\n자동화 공격 탐지 개수 : {block_count}")
        print(f"추가 분석 대상 개수 : {additional_analysis_count}")
        print(f"std >= 2 데이터 개수 : {len(self.filtered_data)}")


    def save_results(self):

        try:

            # 전체 결과 저장
            with open(self.result_file_path, "w", encoding="utf-8") as f:

                json.dump(
                    self.data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            print(f"{self.result_file_path} 저장 완료")


            # STD >= 2 추가 분석 대상 저장
            with open(self.filtered_result_path, "w", encoding="utf-8") as f:

                json.dump(
                    self.filtered_data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            print(f"{self.filtered_result_path} 저장 완료")

        except Exception as e:
            print(f"파일 저장 중 에러 발생: {e}")


if __name__ == "__main__":

    detector = SBFDetector()

    detector.load_logs()
    detector.detect_bots()
    detector.save_results()
