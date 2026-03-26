import re

import requests
from collections import Counter
from pathlib import Path

url = f"https://api.github.com/search/issues?q=author:LumanSuen+type:pr+is:merged&per_page=1000"

r = requests.get(url)
r.raise_for_status()
items = r.json()["items"]

repos = [item["repository_url"].split("/")[-2] + "/" + item["repository_url"].split("/")[-1] for item in items]
count = Counter(repos)

lines = [
    "<!-- begin -->",
    "### 👩‍💻 Open Source Contributions",
    "| Repository | PRs |",
    "|-------------|-----|"
]
for repo, num in count.most_common():
    lines.append(f"| [{repo}](https://github.com/{repo}/pulls?q=author%3ALumanSuen+) | {num} |")
for repo in []:
    c = requests.get(f"https://api.github.com/repos/{repo}/commits?author=LumanSuen&per_page=1")

    lines.append(f"| [{repo}](https://github.com/{repo}/commits/main/?author=LumanSuen) | {len(c.json())} |")
lines.append("<!-- end -->")

pattern = r"(<!-- begin -->)(.*?)(<!-- end -->)"

readme = re.sub(pattern,'\n'.join(lines), Path("README.md").read_text(encoding="utf-8"), flags=re.DOTALL)
print(readme)
Path("README.md").write_text(readme, encoding="utf-8")
print("✅ contributions table generated.")
