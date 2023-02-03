import matplotlib.pyplot as plt
import pandas as pd


def plot_week(
    matchups: list,
    score_df: pd.DataFrame,
    week: int,
    x_min: int = 40,
    x_max: int = 200,
    legend_loc: int | str = 0,
):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # hardcoded plot adjustments
    row_space = 5

    # for y-axis tick labels
    tm_list, tm_ticks, tm_bold = [], [], []

    y_current = 0
    for matchup in matchups:
        home_name = matchup.team_1.team_name
        away_name = matchup.team_2.team_name

        tm_list.append(str(matchup.team_1))
        tm_list.append(str(matchup.team_2))

        if matchup.winner == matchup.team_1:
            tm_bold.extend([1, 0])
        else:
            tm_bold.extend([0, 1])

        for pts in [score_df.loc[home_name], score_df.loc[away_name]]:
            tm_ticks.append(y_current)
            ax.plot(
                [x_min, x_max], [y_current, y_current], "k--", linewidth=1, alpha=0.1
            )

            if (pts["Projected"] - 4) > pts["Actual"]:
                ax.plot(
                    [pts["Actual"] + 2, pts["Projected"] - 2.25],
                    [y_current, y_current],
                    "r-",
                    lw=4,
                )
            elif (pts["Projected"] + 4) < pts["Actual"]:
                ax.plot(
                    [pts["Projected"] + 2.25, pts["Actual"] - 1.5],
                    [y_current, y_current],
                    "g-",
                )

            if (pts["Optimal"] - 2) > pts["Actual"]:
                ax.plot(
                    [pts["Actual"] + 1, pts["Optimal"] - 1],
                    [y_current, y_current],
                    "k-",
                )

            ax.scatter(
                pts["Projected"], y_current, c="w", s=200, marker="o", edgecolor="g"
            )
            ax.scatter(pts["Actual"], y_current, c="k", s=100)

            # if optimal==actual, need to put blue inside black
            if pts["Optimal"] == pts["Actual"]:
                ax.scatter(pts["Optimal"], y_current, c="w", s=25)
                ax.scatter(pts["Optimal"], y_current, c="b", s=25, alpha=0.2)
            else:
                # white underneath in case of overlap
                ax.scatter(pts["Optimal"], y_current, c="w", s=100, alpha=0.75)
                ax.scatter(pts["Optimal"], y_current, c="b", s=100, alpha=0.2)

            y_current += row_space

        y_current += 2 * row_space

    # setting y-axis
    ax.set(yticks=tm_ticks, yticklabels=tm_list)
    for k, tick in enumerate(ax.yaxis.get_major_ticks()):
        if tm_bold[k] == 1:
            tick.label1.set_fontweight("bold")

    # legend stuff
    ax.scatter([], [], c="k", s=100, label="Actual")
    ax.scatter([], [], c="w", s=200, marker="o", edgecolor="g", label="ESPN")
    ax.scatter([], [], c="b", s=100, alpha=0.2, label="Best Possible")
    ax.legend(
        loc=legend_loc,
        borderaxespad=2,
        borderpad=1,
        labelspacing=1.5,
        shadow=True,
        fontsize=12,
    )

    ax.set(title="Week %d" % week)

    return ax
