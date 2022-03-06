import argparse
from api_requests import ApiRequests
from grouped_teams import GroupedTeams
from folder_structure import FolderStructure
from players_stats import PlayerStats
from teams_stats import TeamStats


def grouped_teams():
    resp_all_teams = ApiRequests().get_all_teams()
    grouped = GroupedTeams(resp_all_teams)
    grouped.get_unique_divisions()
    grouped.show_results(grouped.create_grouped_teams())


def players_stats(name):
    player_stats = PlayerStats()
    player_stats.save_player_stats_locally()
    player_stats.get_players_stats_columns()
    player_stats.view_player_stats_by_name(name)


def teams_stats(year_season, condition):
    season_teams_stats = TeamStats()
    total_pages = season_teams_stats.get_meta_teams_stats_total_pages(year_season)

    season_teams_stats.delete_existing_csv_files()
    season_teams_stats.delete_teams_stats_json_file()

    season_teams_stats.get_all_season_teams_stats(total_pages, year_season)
    season_teams_stats.create_teams_names_set()
    season_teams_stats.create_list_for_teams_statistic()
    season_teams_stats.count_statistics_for_teams()

    if condition == 'csv':
        season_teams_stats.write_teams_stats_to_csv()
    if condition == 'json':
        season_teams_stats.write_teams_stats_to_json()
    if condition == 'database':
        season_teams_stats.write_teams_stats_to_sqlite_db()
    if condition == 'console':
        season_teams_stats.show_teams_stats_on_console()


if __name__ == '__main__':
    FolderStructure().create_folder_structure()
    FolderStructure().delete_existing_csv_files()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    grouped_teams_parser = subparsers.add_parser(
        'grouped-teams',
        help='This argument shows on the console all teams divided by division'
    )

    players_stats_parser = subparsers.add_parser(
        'players-stats',
        help='This argument shows a player or players who are the tallest and weight the most.'
    )
    players_stats_parser.add_argument(
        '--name',
        action='store',
        type=str,
        required=True,
        help="Input player's first name or surname to get result."
    )

    teams_stats_parser = subparsers.add_parser(
        'teams-stats',
        help='This argument shows teams statistics.'
    )
    teams_stats_parser.add_argument(
        '--season',
        action='store',
        type=int,
        required=True,
        choices=range(1979, 2022),  # There is no data from 2022, so the choice ends on the year 2021.
        help='Input season from which you want to get statistics'
    )

    teams_stats_parser.add_argument(
        '--output',
        action='store',
        type=str,
        default='stdout',
        choices=['csv', 'json', 'sqlite', 'stdout'],
        help='Chose the output method. Default output is console.'
    )

    args = parser.parse_args()

    if args.command == 'grouped-teams':
        grouped_teams()

    if args.command == 'players-stats':
        players_stats(args.name)

    if args.command == 'teams-stats' and args.output == 'stdout':
        teams_stats(args.season, condition='console')

    if args.command == 'teams-stats' and args.output == 'csv':
        teams_stats(args.season, condition='csv')

    if args.command == 'teams-stats' and args.output == 'json':
        teams_stats(args.season, condition='json')

    if args.command == 'teams-stats' and args.output == 'sqlite':
        teams_stats(args.season, condition='database')
