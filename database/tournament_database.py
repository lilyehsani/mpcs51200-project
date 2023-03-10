from datetime import datetime, timedelta
from util.util import get_conn_curs, commit_close
from database.user_database import get_user_by_id

# Constants
DB_FILENAME = "tournaments.db"

###############################################################################
# CREATE
###############################################################################

# Creates the tournaments-related tables in the database.
# *** Basic Tables ***
# Tournaments table:
# id: int, automatically increments on insert
# name: string, common name of tournament
# eligible_gender: string, ('m', 'f', or 'co-ed')
# eligible_age_min: int, minimum eligible age for tournament
# eligible_age_max: int, maximum eligible age for tournament
# start_date: datetime, starting date and time of the tournament
# end_date: datetime, ending date and time of the tournament
# is_reg_open: int, 0 for registration closed, 1 for open
#
# Teams table:
# id: int, automatically increments on insert
# name: string, common name of team
# team_gender: string, ('m', 'f', or 'co-ed')
# team_age_min: int, minimum age of player on team
# team_age_max: int, maximum age of player on team
# team_manager: int, ID of user who created team
#
# Players table:
# id: int, automatically increments on insert
# name: string, player's name
# gender: string, ('m', 'f', or 'other')
# age: int, player's age
#
# Games table:
# id: int, automatically increments on insert
# home_team: int, foreign key (Teams)
# away_team: int, foreign key (Teams)
# time: datetime, time that the game takes place
# location: string, where the game takes place

# Scores table:
# id: int, automatically increments on insert
# home_team_score: int, score for the home team
# away_team_score: int, score for the away team
def create_basic_tables():
    conn, curs = get_conn_curs(DB_FILENAME)

    tournaments_create = ("CREATE TABLE if not exists Tournaments " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "eligible_gender VARCHAR(5), eligible_age_min INT, " +
        "eligible_age_max INT, start_date DATETIME, end_date DATETIME, " + 
        "tournament_manager INT, location VARCHAR(50), is_reg_open INT)")
    
    teams_create = ("CREATE TABLE if not exists Teams " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "team_gender VARCHAR(5), team_age_min INT, team_age_max INT, " +
        "team_manager INT)")

    players_create = ("CREATE TABLE if not exists Players " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(250), " +
        "gender VARCHAR(5), age INT)")

    games_create = ("CREATE TABLE if not exists Games " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, home_team INT, " +
        "away_team INT, time DATETIME, location VARCHAR(50), " +
        "FOREIGN KEY(home_team) REFERENCES Teams(id), " +
        "FOREIGN KEY(away_team) REFERENCES Teams(id))")
    
    scores_create = ("CREATE TABLE if not exists Scores " +
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, home_team_score INT, " +
        "away_team_score INT)")

    # Remove these lines for data persistence, but they are good for testing
    # curs.execute("DROP TABLE if exists TournamentRegistrations")
    # curs.execute("DROP TABLE if exists PlayersOnTeams")
    # curs.execute("DROP TABLE if exists GamesInTournaments")
    # curs.execute("DROP TABLE if exists Players")
    # curs.execute("DROP TABLE if exists Games")
    # curs.execute("DROP TABLE if exists Teams")
    # curs.execute("DROP TABLE if exists Tournaments")

    # clear_tournament_database()

    # Execute the statements
    statements = [tournaments_create, teams_create, players_create, 
        games_create, scores_create]
    for statement in statements:
        curs.execute(statement)

    commit_close(conn, curs)

# *** Relational Tables ***
# TournamentRegistrations table:
# tournament_id: int, foreign key
# team_id: int, foreign key
#
# PlayersOnTeams table:
# team_id: int, foreign key
# player_id: int, foreign key
#
# GamesInTournaments table:
# tournament_id: int, foreign key
# game_id: int, foreign key
def create_relational_tables():
    conn, curs = get_conn_curs(DB_FILENAME)

    tournament_registrations_create = ("CREATE TABLE if not exists " +
        "TournamentRegistrations (tournament_id INT, team_id INT, " +
        "FOREIGN KEY(tournament_id) REFERENCES Tournaments(id), " +
        "FOREIGN KEY(team_id) REFERENCES Teams(id))")

    players_on_teams_create = ("CREATE TABLE if not exists PlayersOnTeams " +
        "(team_id INT, player_id INT, " +
        "FOREIGN KEY(team_id) REFERENCES Teams(id), " +
        "FOREIGN KEY(player_id) REFERENCES Players(id))")

    games_in_tournaments_create = ("CREATE TABLE if not exists " +
        "GamesInTournaments (tournament_id INT, game_id INT, " +
        "FOREIGN KEY(tournament_id) REFERENCES Tournaments(id), " +
        "FOREIGN KEY(game_id) REFERENCES Games(id))")

    game_scores_create = ("CREATE TABLE if not exists GameScores" +
        "(game_id INT, score_id INT, " +
        "FOREIGN KEY(game_id) REFERENCES Games(id), " +
        "FOREIGN KEY(score_id) REFERENCES Scores(id))")

    # Execute the statements
    statements = [tournament_registrations_create, players_on_teams_create,
        games_in_tournaments_create, game_scores_create]
    for statement in statements:
        curs.execute(statement)

    commit_close(conn, curs)

# Creates a tournament
def create_tournament(name: str, eligible_gender: str, eligible_age_min: int, 
        eligible_age_max: int, start_date: datetime, end_date: datetime,
        tournament_manager: int, location: str):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(location, str)), "location must be a string"
    assert(isinstance(eligible_gender, str)), ("eligible_gender must be a " +
        "string")
    assert(isinstance(eligible_age_min, int)), ("eligible_age_min must be " +
        "an int")
    assert(isinstance(eligible_age_max, int)), ("eligible_age_max must be " +
        "an int")
    assert(isinstance(tournament_manager, int)), ("tournament_manager must " +
        "be an int")
    assert(isinstance(start_date, datetime)), "start_date must be a datetime"
    assert(isinstance(end_date, datetime)), "end_date must be a datetime"
    assert(start_date < end_date), "start_date must be before end_date"

    is_reg_open = 1

    tournament_insert = ("INSERT INTO Tournaments (name, eligible_gender, " +
        "eligible_age_min, eligible_age_max, start_date, end_date, " +
        "tournament_manager, location, is_reg_open) VALUES " +
        "(?,?,?,?,?,?,?,?,?)")
    tournament_data = (name, eligible_gender, eligible_age_min,
        eligible_age_max, start_date, end_date, tournament_manager, location,
        is_reg_open)

    curs.execute(tournament_insert, tournament_data)
    commit_close(conn, curs)

# Creates a game in Games table and connects it to an existing tournament in
# GamesInTournaments table
# Potentially raises sqlite errors, they must be caught by calling function
def create_game(time: datetime, tournament_id: int, location: str, 
        home_team: int = None, away_team: int = None):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(time, datetime)), "time must be a datetime"
    assert(isinstance(tournament_id, int)), "tournament_id must be an int"
    assert(isinstance(location, str)), "location must be a string"
    assert(isinstance(home_team, int) or home_team is None), ("home_team " +
        "must be an int or None")
    assert(isinstance(away_team, int) or away_team is None), ("away_team " +
        "must be an int or None")

    game_insert = ("INSERT INTO Games (home_team, away_team, time, " +
        "location) VALUES (?,?,?,?)")
    game_data = (home_team, away_team, time, location)

    curs.execute(game_insert, game_data)
    game_id = curs.lastrowid

    game_tournament_insert = ("INSERT INTO GamesInTournaments " +
        "(tournament_id, game_id) VALUES (?,?)")
    game_tournament_data = (tournament_id, game_id)

    curs.execute(game_tournament_insert, game_tournament_data)

    commit_close(conn, curs)


# Creates a team in Teams table
def create_team(name: str, team_gender: str, team_age_min: int,
        team_age_max: int, team_manager: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(team_gender, str)), "team_gender must be a string"
    assert(isinstance(team_age_min, int)), "team_age_min must be an int"
    assert(isinstance(team_age_max, int)), "team_age_max must be an int"
    assert(isinstance(team_manager, int)), "team_manager must be an int"

    team_insert = ("INSERT INTO Teams (name, team_gender, " +
        "team_age_min, team_age_max, team_manager) VALUES (?,?,?,?,?)")
    team_data = (name, team_gender, team_age_min, team_age_max, team_manager)

    curs.execute(team_insert, team_data)

    commit_close(conn, curs)

# Creates a player in Players table and connects it to an existing team in
# PlayersOnTeams table
# Potentially raises sqlite errors, they must be caught by calling function
def create_player(name: str, gender: str, age: int, team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(name, str)), "name must be a string"
    assert(isinstance(gender, str)), "gender must be a string"
    assert(isinstance(age, int)), "age must be an int"
    assert(isinstance(team_id, int)), "team_id must be an int"

    player_insert = "INSERT INTO Players (name, gender, age) VALUES (?,?,?)"
    player_data = (name, gender, age)

    curs.execute(player_insert, player_data)
    player_id = curs.lastrowid

    player_team_insert = ("INSERT INTO PlayersOnTeams (team_id, player_id) " +
        "VALUES (?,?)")
    player_team_data = (team_id, player_id)

    curs.execute(player_team_insert, player_team_data)

    commit_close(conn, curs)

# Registers an existing team in an existing tournament by inserting into
# TournamentRegistrations table
# Potentially raises sqlite errors, they must be caught by calling function
def register_team_in_tournament(tournament_id: int, team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    # Ensures that each input is of the correct type, throws an AssertionError
    # with the provided message if not
    assert(isinstance(tournament_id, int)), "tournament_id must be an int"
    assert(isinstance(team_id, int)), "team_id must be an int"

    tournament_team_insert = ("INSERT INTO TournamentRegistrations " +
        "(tournament_id, team_id) VALUES (?,?)")
    tournament_team_data = (tournament_id, team_id)

    curs.execute(tournament_team_insert, tournament_team_data)

    commit_close(conn, curs)

def create_game_score(game_id: int, home_team_score: int, 
        away_team_score: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    assert(isinstance(game_id, int)), "game_id must be an int"
    assert(isinstance(home_team_score, int)), "home_team_score must be an int"
    assert(isinstance(away_team_score, int)), "away_team_score must be an int"

    score_insert = ("INSERT INTO Scores (home_team_score, away_team_score) " +
        "VALUES (?,?)")
    score_data = (home_team_score, away_team_score)

    curs.execute(score_insert, score_data)
    score_id = curs.lastrowid

    game_score_insert = ("INSERT INTO GameScores (game_id, score_id) " +
        "VALUES (?,?)")
    game_score_data = (game_id, score_id)

    curs.execute(game_score_insert, game_score_data)

    commit_close(conn, curs)

###############################################################################
# READ
###############################################################################

# Gets all tournaments in the Tournaments table
# Return format is a dictionary where key is the ID of the tournament
# and value is another dictionary with tournament_id, name, eligible_gender, 
# eligible_age_min, eligible_age_max, start_date, end_date, and 
# registered_teams (which is a list of dictionaries of each team's information)
def get_all_tournaments():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments")
    rows = curs.fetchall()
    
    tournaments = {}
    for row in rows:
        tournament_id = row[0]
        tournaments[tournament_id] = get_tournament_by_id(tournament_id)

    commit_close(conn, curs)

    return tournaments

# Gets all teams in the Teams table
# Return format is a dictionary where key is the ID of the team
# and value is another dictionary with team_id, name, team_gender, 
# team_age_min, team_age_max, team manager (which is a dictionary of that
# user's information), and roster (which is a list of dictionaries of each
# player's information)
def get_all_teams():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams")
    rows = curs.fetchall()
    
    teams = {}
    for row in rows:
        team_id = row[0]
        teams[team_id] = get_team_by_id(team_id)

    commit_close(conn, curs)

    return teams

def get_teams_by_manager(manager_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE team_manager = ?",
                 [manager_id])
    rows = curs.fetchall()

    teams = {}
    for row in rows:
        team_id = row[0]
        teams[team_id] = get_team_by_id(team_id)

    commit_close(conn, curs)

    return teams

def get_players_by_team(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    select_roster = "SELECT * FROM PlayersOnTeams WHERE team_id = ?"
    select_data = [team_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    players = {}
    for roster_item in roster:
        player_id = roster_item[1]
        players[player_id] = get_player_by_id(player_id)

    commit_close(conn, curs)

    return players

def get_tournament_by_name(tournament_name: str):
    # Is tournament name in database?
    conn, curs = get_conn_curs(DB_FILENAME)
    query = "SELECT * FROM Tournaments WHERE name = '{}'".format(tournament_name)

    curs.execute(query)
    rows = curs.fetchall()
    if len(rows) > 0:
        ids = rows[0][0]
        return ids
    else:
        return False

def get_tournaments_by_manager(manager_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments WHERE tournament_manager = ?",
                 [manager_id])
    rows = curs.fetchall()

    tournaments = {}
    for row in rows:
        tournament_id = row[0]
        tournaments[tournament_id] = get_tournament_by_id(tournament_id)

    commit_close(conn, curs)

    return tournaments

def get_tournament_by_id(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments WHERE id = ?", [tournament_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Tournament does not exist")

    select_registrations = ("SELECT * FROM TournamentRegistrations " +
        "WHERE tournament_id = ?")
    select_data = [tournament_id]

    curs.execute(select_registrations, select_data)
    registrations = curs.fetchall()

    teams = []
    for registration in registrations:
        team_id = registration[1]
        teams.append(get_team_by_id(team_id))

    tournament_info = rows[0]

    tournament = {
        "tournament_id": tournament_info[0],
        "name": tournament_info[1],
        "eligible_gender": tournament_info[2],
        "eligible_age_min": tournament_info[3],
        "eligible_age_max": tournament_info[4],
        "start_date": tournament_info[5],
        "end_date": tournament_info[6],
        "is_reg_open": tournament_info[9],
        "registered_teams": teams,
        "location": tournament_info[8]
    }

    commit_close(conn, curs)

    return tournament

def get_score_by_game(game_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    select = ("SELECT * FROM GameScores " +
        "WHERE game_id = ?")
    select_data = [game_id]

    curs.execute(select, select_data)
    score_id = curs.fetchall()

    commit_close(conn, curs)

    # print(f"score id {score_id}")

    # use most recent score
    if score_id:
        return get_score_by_id(score_id[-1][1]) 
    else:
        return None


def get_score_by_id(score_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    select = ("SELECT * FROM Scores " +
        "WHERE id = ?")
    select_data = [score_id]

    curs.execute(select, select_data)
    score = curs.fetchall()

    commit_close(conn, curs)

    # print(score)

    return {"homescore": score[0][1], "awayscore": score[0][2]}

def get_games_by_tournament(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    select_games = ("SELECT * FROM GamesInTournaments " +
        "WHERE tournament_id = ?")
    select_data = [tournament_id]

    curs.execute(select_games, select_data)
    games_in_tournaments = curs.fetchall()

    games = {}
    for relation in games_in_tournaments:
        game_id = relation[1]
        games[game_id] = get_game_by_id(game_id)

    commit_close(conn, curs)

    return games

def get_game_by_id(game_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Games WHERE id = ?", [game_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Game does not exist")
    
    game_info = rows[0]

    game = {
        "game_id": game_info[0],
        "home_team": game_info[1],
        "away_team": game_info[2],
        "time": game_info[3],
        "location": game_info[4]
    }

    commit_close(conn, curs)

    return game

def get_team_by_id(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE id = ?", [team_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Team does not exist")

    select_roster = "SELECT * FROM PlayersOnTeams WHERE team_id = ?"
    select_data = [team_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    players = []
    for roster_item in roster:
        player_id = roster_item[1]
        players.append(get_player_by_id(player_id))

    team_info = rows[0]

    team = {
        "team_id": team_info[0],
        "name": team_info[1],
        "team_gender": team_info[2],
        "team_age_min": team_info[3],
        "team_age_max": team_info[4],
        "team_manager": get_user_by_id(team_info[5]),
        "roster": players
    }

    commit_close(conn, curs)

    return team

def get_player_by_id(player_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Players WHERE id = ?", [player_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Player does not exist")

    player_info = rows[0]

    player = {
        "player_id": player_info[0],
        "name": player_info[1],
        "gender": player_info[2],
        "age": player_info[3]
    }

    commit_close(conn, curs)
    
    return player

def get_team_manager_id(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE id = ?", [team_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Team does not exist")

    team_manager_id = rows[0][5]

    commit_close(conn, curs)

    return team_manager_id

def get_tournament_manager_id(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments WHERE id = ?", [tournament_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Tournament does not exist")

    tounament_manager_id = rows[0][7]

    commit_close(conn, curs)

    return tounament_manager_id

def get_team_ids():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams")
    rows = curs.fetchall()
    
    team_ids = []
    for row in rows:
        team_id = row[0]
        team_ids.append(team_id)

    commit_close(conn, curs)
    return team_ids

def get_tournament_ids():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Tournaments")
    rows = curs.fetchall()

    tournament_ids = []
    for row in rows:
        tournament_id = row[0]
        tournament_ids.append(tournament_id)

    commit_close(conn, curs)
    return tournament_ids

def get_player_ids():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Players")
    rows = curs.fetchall()

    player_ids = []
    for row in rows:
        player_id = row[0]
        player_ids.append(player_id)

    commit_close(conn, curs)
    return player_ids

# Returns team actual age range
# Returns none, none if no players
def get_team_age_range(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE id = ?", [team_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Team does not exist")

    select_roster = "SELECT * FROM PlayersOnTeams WHERE team_id = ?"
    select_data = [team_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    min_age = None
    max_age = None
    for roster_item in roster:
        player_id = roster_item[1]
        age = get_player_by_id(player_id)["age"]
        if not max_age or age > max_age:
            max_age = age
        if not min_age or age < min_age:
            min_age = age

    commit_close(conn, curs)
    return min_age, max_age

# Returns team genders: m, f, or mixed
# Returns none if no players
def get_team_gender_range(team_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("SELECT * FROM Teams WHERE id = ?", [team_id])
    rows = curs.fetchall()

    if len(rows) < 1:
        raise Exception("Team does not exist")

    select_roster = "SELECT * FROM PlayersOnTeams WHERE team_id = ?"
    select_data = [team_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    male = False
    female = False
    for roster_item in roster:
        # print(f"getting team_id {roster_item[0]} player_id {roster_item[1]}")
        player_id = roster_item[1]
        gender = get_player_by_id(player_id)["gender"]
        if gender == "m":
            male = True
        else:
            female = True

    commit_close(conn, curs)

    if male and female:
        return "mixed"
    elif male:
        return "m"
    elif female:
        return "f"
    else:
        return None

# Get team by player id
def get_team_by_player(player_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    select_roster = "SELECT * FROM PlayersOnTeams WHERE player_id = ?"
    select_data = [player_id]

    curs.execute(select_roster, select_data)
    roster = curs.fetchall()

    team_id = None
    if roster:
        team_id = roster[0][0]

    commit_close(conn, curs)
    # print(f"team id: {team_id} player id: {player_id}")

    return team_id

def check_if_registered(team_id: int, tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)
    select_registrations = ("SELECT * FROM TournamentRegistrations " +
        "WHERE tournament_id = ? AND team_id = ?")
    select_data = [tournament_id, team_id]

    curs.execute(select_registrations, select_data)
    registrations = curs.fetchall()

    if registrations:
        return True
    return False
    

###############################################################################
# UPDATE
###############################################################################
def update_tournament_location(tournament_id: int,
                    location: str):
    conn, curs = get_conn_curs(DB_FILENAME)
    query = ("UPDATE Tournaments SET location = ?" + 
    "WHERE id = ?")

    data = [location, str(tournament_id)]
    curs.execute(query, data)
    commit_close(conn, curs)

def close_reg(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("UPDATE Tournaments SET is_reg_open = 0 WHERE id = {}".format(tournament_id))

    commit_close(conn, curs)

###############################################################################
# DELETE
###############################################################################

# Deletes the tournament with the given id
def delete_tournament(tournament_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM Tournaments WHERE id = {}".format(tournament_id))

    commit_close(conn, curs)

# Deletes the player with the given id
def delete_player(player_id: int):
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DELETE FROM PlayersOnTeams WHERE player_id = {}".format(player_id))
    curs.execute("DELETE FROM Players WHERE id = {}".format(player_id))

    commit_close(conn, curs)

# Drops all tables
def clear_tournament_database():
    conn, curs = get_conn_curs(DB_FILENAME)

    curs.execute("DROP TABLE if exists TournamentRegistrations")
    curs.execute("DROP TABLE if exists PlayersOnTeams")
    curs.execute("DROP TABLE if exists GamesInTournaments")
    curs.execute("DROP TABLE if exists GameScores")
    curs.execute("DROP TABLE if exists Locations")
    curs.execute("DROP TABLE if exists Scores")
    curs.execute("DROP TABLE if exists Players")
    curs.execute("DROP TABLE if exists Games")
    curs.execute("DROP TABLE if exists Teams")
    curs.execute("DROP TABLE if exists Tournaments")

    commit_close(conn, curs)

    
###############################################################################
# SETUP
###############################################################################

def setup_tournament_database():
    create_basic_tables()
    create_relational_tables()
