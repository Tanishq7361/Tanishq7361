"""
Refresh the living SVGs (stats, languages, heatmap) from the GitHub GraphQL API.

  GH_TOKEN=... GH_USER=Tanishq7361 python scripts/update_stats.py
  python scripts/update_stats.py --demo <dir>     # render sample data, no network
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dynamic_assets as dyn

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

PROFILE_Q = """
query($login:String!){ user(login:$login){
  createdAt
  pullRequests{ totalCount }
  repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, first:100){
    totalCount
    nodes{ stargazerCount languages(first:12, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } }
  }
}}"""

CAL_Q = """
query($login:String!,$from:DateTime!,$to:DateTime!){ user(login:$login){
  contributionsCollection(from:$from, to:$to){
    totalCommitContributions
    contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
  }
}}"""


def gql(token, query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "realm-scribe"},
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        out = json.load(r)
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]["user"]


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(token, login):
    now = dt.datetime.now(dt.timezone.utc)
    prof = gql(token, PROFILE_Q, {"login": login})
    created = dt.datetime.fromisoformat(prof["createdAt"].replace("Z", "+00:00"))
    days = {}
    for year in range(created.year, now.year + 1):
        start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
        end = min(now, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
        cal = gql(token, CAL_Q, {"login": login, "from": iso(start), "to": iso(end)})["contributionsCollection"]["contributionCalendar"]
        for wk in cal["weeks"]:
            for day in wk["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
    last = gql(token, CAL_Q, {"login": login, "from": iso(now - dt.timedelta(days=364)), "to": iso(now)})
    return {"profile": prof, "created": created, "now": now, "days": days,
            "commits": last["contributionsCollection"]["totalCommitContributions"]}


def _fmt(d, year=False):
    return f"{d.strftime('%b')} {d.day}" + (f", {d.year}" if year else "")


def streaks(days, today):
    dates = sorted(k for k in days if dt.date.fromisoformat(k) <= today)
    counts = [(dt.date.fromisoformat(k), days[k]) for k in dates]
    best, run, start = (0, None, None), 0, None
    for d, c in counts:
        if c > 0:
            run += 1
            start = start if run > 1 else d
            if run > best[0]:
                best = (run, start, d)
        else:
            run = 0
    cur, cur_start, cur_end = 0, None, None
    i = len(counts) - 1
    if i >= 0 and counts[i][1] == 0:      # today not done yet: streak may still be alive
        i -= 1
    while i >= 0 and counts[i][1] > 0:
        cur += 1
        cur_start, cur_end = counts[i][0], cur_end or counts[i][0]
        i -= 1
    return (cur, cur_start, cur_end), best


def compute(raw):
    today = raw["now"].date()
    days = raw["days"]
    (cur, cs, ce), (lg, ls, le) = streaks(days, today)
    ranges = lambda a, b: "" if not a else (_fmt(a) if a == b else f"{_fmt(a)} – {_fmt(b)}")
    lr = ""
    if ls:
        lr = ranges(ls, le) + (f", {le.year}" if le.year != today.year else "")

    # last 53 Sunday-first weeks
    sunday = today - dt.timedelta(days=(today.weekday() + 1) % 7)
    weeks = []
    for w in range(52, -1, -1):
        s = sunday - dt.timedelta(weeks=w)
        col = []
        for k in range(7):
            d = s + dt.timedelta(days=k)
            col.append((None, 0) if d > today else (d.isoformat(), days.get(d.isoformat(), 0)))
        weeks.append(col)
    year_total = sum(c for wk in weeks for _, c in wk)

    prof = raw["profile"]
    repos = prof["repositories"]["nodes"]
    size = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            size[e["node"]["name"]] = size.get(e["node"]["name"], 0) + e["size"]
    tot = sum(size.values()) or 1
    langs = sorted(((n, 100 * v / tot) for n, v in size.items()), key=lambda t: -t[1])

    return {
        "total": sum(days.values()), "since_label": f"since {raw['created'].strftime('%b %Y')}",
        "cur": cur, "cur_range": ranges(cs, ce), "longest": lg, "longest_range": lr,
        "commits": raw["commits"], "prs": prof["pullRequests"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos), "repos": prof["repositories"]["totalCount"],
        "langs": langs, "weeks": weeks, "year_total": year_total,
        "updated_label": "Ledger updated " + raw["now"].strftime("%b %d, %Y · %H:%M UTC"),
    }


def write_all(data, out):
    os.makedirs(out, exist_ok=True)
    for name, fn in (("stats.svg", dyn.stats), ("langs.svg", dyn.langs), ("heatmap.svg", dyn.heatmap)):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(fn(data))
        print("wrote", name)


def demo():
    import random
    rng = random.Random(3)
    today = dt.date(2026, 9, 29)
    days = {(today - dt.timedelta(days=i)).isoformat(): (0 if rng.random() < .35 else rng.choice([1, 2, 3, 5, 8, 12, 20])) for i in range(400)}
    for i in range(7):
        days[(today - dt.timedelta(days=i)).isoformat()] = 3 + i
    prof = {"createdAt": "2024-12-19T00:00:00Z", "pullRequests": {"totalCount": 14},
            "repositories": {"totalCount": 18, "nodes": [
                {"stargazerCount": 4, "languages": {"edges": [{"size": 52000, "node": {"name": "TypeScript"}}, {"size": 31000, "node": {"name": "Python"}}, {"size": 9000, "node": {"name": "CSS"}}]}},
                {"stargazerCount": 2, "languages": {"edges": [{"size": 24000, "node": {"name": "C++"}}, {"size": 6000, "node": {"name": "JavaScript"}}, {"size": 3000, "node": {"name": "HTML"}}]}}]}}
    raw = {"profile": prof, "created": dt.datetime(2024, 12, 19, tzinfo=dt.timezone.utc),
           "now": dt.datetime(2026, 9, 29, 6, 0, tzinfo=dt.timezone.utc), "days": days, "commits": 512}
    return compute(raw)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--demo":
        write_all(demo(), sys.argv[2])
        sys.exit(0)
    token = os.environ.get("GH_TOKEN")
    login = os.environ.get("GH_USER", "Tanishq7361")
    if not token:
        sys.exit("GH_TOKEN is not set")
    write_all(compute(fetch(token, login)), ASSETS)
