import re
import json
from collections import Counter
from pathlib import Path
from urllib.request import urlopen

url = f"https://api.github.com/search/issues?q=author:JiayaoS+type:pr+created:%3E2023-01-01&per_page=1000"
excluded_owners = {"Loxonl", "JiayaoS"}

with urlopen(url) as response:
    items = json.loads(response.read())["items"]

repos = []
for item in items:
    owner, repo = item["repository_url"].split("/")[-2:]
    if owner in excluded_owners:
        continue
    repos.append(f"{owner}/{repo}")
count = Counter(repos)

lines = [
    "<!-- begin -->",
    "### 👩‍💻 Open Source Contributions",
    "| Repository | PRs |",
    "|-------------|-----|"
]
for repo, num in count.most_common():
    lines.append(f"| [{repo}](https://github.com/{repo}/pulls?q=author%3AJiayaoS+) | {num} |")
for repo in []:
    with urlopen(f"https://api.github.com/repos/{repo}/commits?author=JiayaoS&per_page=1") as response:
        commits = json.loads(response.read())

    lines.append(f"| [{repo}](https://github.com/{repo}/commits/main/?author=JiayaoS) | {len(commits)} |")
while lines and not lines[-1].strip():
    lines.pop()
lines.append("")
lines.append("<!-- end -->")

pattern = r"(<!-- begin -->)(.*?)(<!-- end -->)"

readme = re.sub(pattern,'\n'.join(lines), Path("README.md").read_text(encoding="utf-8"), flags=re.DOTALL)
print(readme)
Path("README.md").write_text(readme, encoding="utf-8")
print("✅ contributions table generated.")
