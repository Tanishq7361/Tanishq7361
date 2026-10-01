"""Regenerate every static SVG in ../assets  (python scripts/build_assets.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dynamic_assets as dyn
import static_assets as st

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:26s}{len(content) / 1024:7.1f} KB")


if __name__ == "__main__":
    write("header.svg", st.header())
    write("titles.svg", st.titles())
    write("divider.svg", st.divider())
    for slug, title, sub in [
        ("about", "The Wanderer's Tale", "who walks these lands"),
        ("armory", "The Armory", "tongues, tools & forges"),
        ("quests", "Quests & Campaigns", "works forged with my own hands"),
        ("feats", "Feats of Valor", "hackathons & honours"),
        ("ledger", "Ledger of the Realm", "the living record of my deeds"),
        ("contact", "Send a Raven", "seek an audience"),
    ]:
        write(f"h-{slug}.svg", st.section_header(title, sub))
    write("about.svg", st.about())
    write("armory.svg", st.arsenal())
    write("quest-argus.svg", st.quest_argus())
    write("quest-aicalc.svg", st.quest_aicalc())
    write("feats.svg", st.feats())
    write("btn-repo.svg", st.button("BEHOLD THE REPO", "github", 250))
    write("btn-demo.svg", st.button("ENTER THE LIVE DEMO", "portal", 280))
    write("btn-email.svg", st.button("SEND A RAVEN", "mail", 250))
    write("btn-linkedin.svg", st.button("THE GUILD HALL", "in", 250))
    write("btn-github.svg", st.button("THE ARCHIVE", "github", 250))
    write("footer.svg", st.footer())
    # dynamic files: only create placeholders when missing (the workflow owns them)
    seed = {"total": 738, "cur": 7, "cur_range": "Sep 23 – Sep 29", "longest": 7,
            "longest_range": "Jun 14 – Jun 20, 2025", "since_label": "since Dec 2024"}
    for name, fn, data in [("stats.svg", dyn.stats, seed), ("langs.svg", dyn.langs, {}), ("heatmap.svg", dyn.heatmap, {})]:
        if not os.path.exists(os.path.join(OUT, name)):
            write(name, fn(data))
