from database.user_database import setup_user_database, get_all_users
from database.tournament_database import setup_tournament_database, create_tournament, register_team_in_tournament, create_team, create_game, get_all_tournaments, get_all_teams
from backend.users import log_in
from datetime import datetime, timedelta

# Constants
LOG_IN_MENU = '''
Please log in to start. Enter your username:
    
> '''
PASSWORD_MENU = '''
Enter your password:

> '''

# Loops for input
def control_loop():
    command = input(LOG_IN_MENU).strip()
    is_logged_in = False
    while command != 'quit':
        if not is_logged_in:
            username = command
            password = input(PASSWORD_MENU)
            user_type = log_in(username, password)
            if not user_type:
                message = "\nLog in failed.\n" + LOG_IN_MENU
            else:
                message = f"You are logged in as type: {user_type}"
                is_logged_in = True
        else:
            message = f"You are logged in as type: {user_type}"

        command = input(message)
    print("Goodbye")

if __name__ == "__main__":
    setup_user_database()
    setup_tournament_database()
    # create_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
    #     datetime.now() + timedelta(days=2))
    # create_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
    #     datetime.now() + timedelta(days=2))
    # create_tournament("UChicago Tournament", "co-ed", 18, 24, datetime.now(),
    #     datetime.now() + timedelta(days=2))
    # create_team("UChicago", "co-ed", 18, 24, 2)
    # register_team_in_tournament(1, 1)
    # print(get_all_tournaments())
    # print(get_all_teams())
    # create_game(datetime.now() + timedelta(days=1), 1)
    control_loop()


# Example test cases for log_in function:
# # Should be TournamentManager
# print(log_in("tm123", "password"))
# # Should be None
# print(log_in("tm123", "wrongpassword"))
# # Should be None
# print(log_in("tm1234", "password"))
# # Should be Other
# print(log_in("soccerfan01", "password"))