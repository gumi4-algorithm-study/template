import os
import re
from datetime import datetime
import github
import pytz

# GitHub 리포지토리 정보
repo_name = os.getenv("GITHUB_REPOSITORY", "GUMI4-ALGO")
token = os.getenv("GITHUB_TOKEN")

# GitHub API 클라이언트 생성
g = github.Github(token)
repo = g.get_repo(repo_name)


def get_problems_from_readme():
    readme_content = repo.get_contents("README.md").decoded_content.decode("utf-8")
    problems = {}
    current_week = None

    for line in readme_content.split("\n"):
        week_match = re.match(r"\|\s*(\d+)주차\s*\|", line)
        if week_match:
            current_week = int(week_match.group(1))
            problems[current_week] = []

        if current_week is not None and "|" in line:
            problem_numbers = re.findall(r"BOJ(\d+)", line)
            problems[current_week].extend(problem_numbers)

    print("problems", problems)
    return problems


def get_current_week():
    # start_date = datetime(2023, 5, 1, tzinfo=pytz.timezone("Asia/Seoul"))
    # today = datetime.now(pytz.timezone("Asia/Seoul"))
    # return (today - start_date).days // 7 + 1

    # test code
    return 1


problems = get_problems_from_readme()
print("problems after get_problems_from_readme", problems)
current_week = get_current_week()

# 참가자 디렉토리 목록
participants = [
    d for d in os.listdir(".") if os.path.isdir(d) and not d.startswith(".")
]

issue_body = f"## {current_week}주차 문제 풀이 현황 (테스트)\n\n"

for participant in participants:
    solved = []
    unsolved = []
    participant_dir = os.path.join(participant, f"{current_week}주차")

    if os.path.exists(participant_dir):
        print(f"Checking directory: {participant_dir}")
        print("Files in directory:", os.listdir(participant_dir))

        for problem in problems.get(current_week, []):
            print(f"Checking problem: {problem}")
            if any(
                re.match(f"(BOJ)?{problem}\\.java$", file)
                for file in os.listdir(participant_dir)
            ):
                solved.append(f"BOJ{problem}")
            else:
                unsolved.append(f"BOJ{problem}")
    else:
        unsolved = [f"BOJ{problem}" for problem in problems.get(current_week, [])]

    issue_body += f"### {participant}\n"
    issue_body += f"- 풀은 문제: {', '.join(solved) if solved else '없음'}\n"
    issue_body += f"- 풀지 않은 문제: {', '.join(unsolved) if unsolved else '없음'}\n\n"

# 이슈 생성
# repo.create_issue(title=f"{current_week}주차 문제 풀이 현황 (테스트)", body=issue_body)

# 테스트 코드
repo.create_issue(title=f"테스트: {current_week}주차 문제 풀이 현황", body=issue_body)
