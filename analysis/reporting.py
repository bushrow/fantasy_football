from fantasy_football.analysis.text_content import TEXT_CONTENT


def create_week_summary(performance_df):
    proj_dict = {
        "gurus": {
            "filter": performance_df["Actual"] > performance_df["Projected"],
            "comparison": "Projected",
        },
        "perfect_lineup": {
            "filter": performance_df["Actual"] == performance_df["Optimal"],
            "comparison": "Optimal",
        },
        "ham_sammys": {
            "filter": performance_df["Actual"] == performance_df["Projected"],
            "comparison": "Projected",
        },
        "tinkerers": {
            "filter": performance_df["Actual"] < performance_df["Projected"],
            "comparison": "Projected",
        },
    }

    summary_texts = []
    for category, d in proj_dict.items():
        category_df = performance_df[d["filter"]]
        if not category_df.empty:
            category_text = []
            team_list = [t.strip() for t in category_df.index]
            if len(team_list) > 1:
                name_str = ", ".join(team_list[:-1])
                if len(team_list) > 2:
                    name_str += ","
                name_str += " and " + team_list[-1]
            else:
                name_str = team_list[0]
            grp_text = TEXT_CONTENT[category]["group"][0].format(name_str)
            if grp_text:
                category_text.append(grp_text)

            diffs = (category_df[d["comparison"]] - category_df["Actual"]).abs()
            indiv_name = diffs.idxmax()
            indiv_points = diffs.max()
            indiv_text = TEXT_CONTENT[category]["indiv"][0].format(
                indiv_name, indiv_points
            )
            if indiv_text:
                category_text.append(indiv_text)
            summary_texts.append("\n".join(category_text))

    summary = "\n\n".join(summary_texts)
    print(summary)
    return summary
