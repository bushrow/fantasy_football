import matplotlib.pyplot as plt

from espn_api.fantasy_football import League
from espn_api.fantasy_football.analysis.reporting import create_week_summary
from espn_api.fantasy_football.analysis.visuals import plot_week

from secrets import ESPN_LEAGUE_ID, ESPN_S2, ESPN_SWID

league_id = ESPN_LEAGUE_ID
year = 2022
week = 17

league = League(league_id=league_id, swid=ESPN_SWID, espn_s2=ESPN_S2)

season_data = league.get_season_data(year)
performance_df = league.get_league_performance(year=year, week=week)
wk_matchups = season_data["games"][week - 1]

summary = create_week_summary(performance_df.loc[week])
ax = plot_week(wk_matchups, performance_df.loc[week], week)
plt.tight_layout()
plt.show()
