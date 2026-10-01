"""Regenerate every static & dynamic Cyberpunk HUD SVG in ../assets (python scripts/build_assets.py)."""
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
        ("about", "OPERATIVE DOSSIER", "tactical identity & protocols"),
        ("armory", "CYBER ARSENAL", "core weapons & tech systems"),
        ("quests", "ACTIVE MISSIONS", "deployed systems & repositories"),
        ("feats", "COMBAT TELEMETRY", "hackathons & citations"),
        ("ledger", "NEURAL LEDGER", "living record of deeds"),
        ("contact", "COMMS ARRAY", "open transmission channels"),
    ]:
        write(f"h-{slug}.svg", st.section_header(title, sub))
    write("about.svg", st.about())
    write("armory.svg", st.arsenal())
    write("quest-equisplit.svg", st.quest_equisplit())
    write("quest-vaayu.svg", st.quest_vaayu())
    write("quest-cachecore.svg", st.quest_cachecore())
    write("feats.svg", st.feats())
    write("btn-repo.svg", st.button("ACCESS REPO", "github", 250))
    write("btn-demo.svg", st.button("LAUNCH DEMO", "portal", 250))
    write("btn-email.svg", st.button("TRANSMIT MESSAGE", "mail", 250))
    write("btn-linkedin.svg", st.button("NEURAL LINK", "in", 250))
    write("btn-github.svg", st.button("CYBER ARCHIVE", "github", 250))
    write("footer.svg", st.footer())

    # Generate dynamic telemetry SVGs with default data
    seed = {
        "total": 512, "cur": 14, "cur_range": "Active Streak",
        "longest": 28, "longest_range": "All-Time Best", "since_label": "since first commit",
        "commits": 420, "prs": 18, "stars": 12, "repos": 23, "updated_label": "// TELEMETRY SYNCED WITH GITHUB //"
    }
    sample_langs = [("C++", 48.2), ("Java", 24.5), ("Python", 14.8), ("JavaScript", 6.5), ("SQL", 3.8), ("HTML/CSS", 2.2)]
    write("stats.svg", dyn.stats(seed))
    write("langs.svg", dyn.langs({"langs": sample_langs}))
    write("heatmap.svg", dyn.heatmap({"year_total": 512}))
