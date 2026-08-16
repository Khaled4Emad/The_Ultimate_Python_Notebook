# import random

# import streamlit as st
# from supabase import Client, create_client


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Guess the Number",
#     page_icon="🎯",
#     layout="centered"
# )


# # ============================================================
# # SUPABASE CONNECTION
# # ============================================================

# @st.cache_resource
# def init_supabase() -> Client:
#     """
#     Create and cache the Supabase client.
#     """

#     return create_client(
#         st.secrets["SUPABASE_URL"],
#         st.secrets["SUPABASE_KEY"]
#     )


# supabase = init_supabase()


# # ============================================================
# # GAME LEVELS
# # ============================================================

# GAME_LEVELS = {
#     1: {
#         "name": "Easy",
#         "min": 1,
#         "max": 10,
#         "n_tries": 3,
#         "base_score": 100,
#     },

#     2: {
#         "name": "Intermediate",
#         "min": 1,
#         "max": 100,
#         "n_tries": 7,
#         "base_score": 300,
#     },

#     3: {
#         "name": "Hard",
#         "min": 1,
#         "max": 1000,
#         "n_tries": 15,
#         "base_score": 500,
#     },
# }


# # ============================================================
# # SESSION STATE INITIALIZATION
# # ============================================================

# def initialize_session_state():
#     """
#     Initialize all required Streamlit session state variables.
#     """

#     defaults = {
#         "player_name": "",
#         "game_level": 1,
#         "hidden": None,
#         "user_tries": 0,
#         "game_started": False,
#         "game_over": False,
#         "game_won": False,
#         "score": 0,
#         "message": "",
#         "message_type": "",
#         "score_saved": False,
#     }

#     for key, value in defaults.items():

#         if key not in st.session_state:
#             st.session_state[key] = value


# initialize_session_state()


# # ============================================================
# # START NEW GAME
# # ============================================================

# def start_new_game(level):
#     """
#     Start a new game using the selected difficulty level.
#     """

#     settings = GAME_LEVELS[level]

#     st.session_state.game_level = level

#     st.session_state.hidden = random.randint(
#         settings["min"],
#         settings["max"]
#     )

#     st.session_state.user_tries = 0

#     st.session_state.game_started = True
#     st.session_state.game_over = False
#     st.session_state.game_won = False

#     st.session_state.score = 0

#     st.session_state.message = ""
#     st.session_state.message_type = ""

#     st.session_state.score_saved = False


# # ============================================================
# # CALCULATE SCORE
# # ============================================================

# def calculate_score(level, tries):
#     """
#     Calculate the player's score.

#     Higher difficulty = higher base score.
#     Fewer attempts = higher bonus.
#     """

#     settings = GAME_LEVELS[level]

#     base_score = settings["base_score"]
#     maximum_tries = settings["n_tries"]

#     # Reward the player for using fewer attempts.
#     bonus = (maximum_tries - tries + 1) * 10

#     return base_score + bonus


# # ============================================================
# # SAVE SCORE TO SUPABASE
# # ============================================================

# def save_score(player_name, level, tries, score):
#     """
#     Save the player's winning score to Supabase.
#     """

#     level_name = GAME_LEVELS[level]["name"]

#     data = {
#         "player_name": player_name,
#         "game_level": level_name,
#         "tries": tries,
#         "score": score,
#     }

#     try:

#         response = (
#             supabase
#             .table("game_scores")
#             .insert(data)
#             .execute()
#         )

#         return True

#     except Exception as error:

#         st.error(
#             f"Unable to save your score.\n\n"
#             f"Error: {error}"
#         )

#         return False


# # ============================================================
# # GET TOP 3 PLAYERS
# # ============================================================

# def get_top_players():
#     """
#     Retrieve the top 3 scores from Supabase.
#     """

#     try:

#         response = (
#             supabase
#             .table("game_scores")
#             .select("*")
#             .order("score", desc=True)
#             .limit(3)
#             .execute()
#         )

#         return response.data

#     except Exception as error:

#         st.error(
#             f"Unable to load the leaderboard.\n\n"
#             f"Error: {error}"
#         )

#         return []


# # ============================================================
# # CHECK GUESS
# # ============================================================

# def check_guess(guess):
#     """
#     Check the player's guess.
#     """

#     if st.session_state.game_over:
#         return

#     level = st.session_state.game_level

#     settings = GAME_LEVELS[level]

#     hidden = st.session_state.hidden
#     maximum_tries = settings["n_tries"]

#     # ---------------------------------------------
#     # Count the attempt
#     # ---------------------------------------------

#     st.session_state.user_tries += 1

#     current_try = st.session_state.user_tries

#     # ---------------------------------------------
#     # Correct Guess
#     # ---------------------------------------------

#     if guess == hidden:

#         st.session_state.game_won = True
#         st.session_state.game_over = True

#         score = calculate_score(
#             level,
#             current_try
#         )

#         st.session_state.score = score

#         st.session_state.message = (
#             f"🎉 Congratulations! "
#             f"You got it in {current_try} "
#             f"{'try' if current_try == 1 else 'tries'}!"
#         )

#         st.session_state.message_type = "success"

#         return

#     # ---------------------------------------------
#     # Maximum Attempts
#     # ---------------------------------------------

#     if current_try >= maximum_tries:

#         st.session_state.game_over = True
#         st.session_state.game_won = False

#         st.session_state.message = (
#             f"Unfortunately, you used all "
#             f"{maximum_tries} tries."
#         )

#         st.session_state.message_type = "error"

#         return

#     # ---------------------------------------------
#     # Guess Too Low
#     # ---------------------------------------------

#     if guess < hidden:

#         st.session_state.message = (
#             "📈 No, increase!"
#         )

#     # ---------------------------------------------
#     # Guess Too High
#     # ---------------------------------------------

#     else:

#         st.session_state.message = (
#             "📉 No, decrease!"
#         )

#     st.session_state.message_type = "warning"


# # ============================================================
# # HEADER
# # ============================================================

# st.title("🎯 Guess the Number")

# st.markdown(
#     """
# Try to guess the hidden number before you run out of attempts!
# """
# )


# # ============================================================
# # PLAYER NAME
# # ============================================================

# st.subheader("👤 Player")

# player_name = st.text_input(
#     "Enter your name",
#     value=st.session_state.player_name,
#     max_chars=50,
#     placeholder="e.g. Khaled"
# )

# st.session_state.player_name = player_name.strip()


# # ============================================================
# # DIFFICULTY LEVELS
# # ============================================================

# st.subheader("🎮 Game Levels")


# col1, col2, col3 = st.columns(3)


# with col1:

#     st.markdown("### 🟢 Easy")

#     st.write("Numbers: **1 – 10**")
#     st.write("Tries: **3**")
#     st.write("Base Score: **100**")


# with col2:

#     st.markdown("### 🟡 Intermediate")

#     st.write("Numbers: **1 – 100**")
#     st.write("Tries: **7**")
#     st.write("Base Score: **300**")


# with col3:

#     st.markdown("### 🔴 Hard")

#     st.write("Numbers: **1 – 1000**")
#     st.write("Tries: **15**")
#     st.write("Base Score: **500**")


# # ============================================================
# # LEVEL SELECTION
# # ============================================================

# st.subheader("Choose Your Level")


# selected_level = st.selectbox(
#     "Difficulty",
#     options=[1, 2, 3],
#     format_func=lambda level: GAME_LEVELS[level]["name"],
#     index=st.session_state.game_level - 1,
# )


# # ============================================================
# # START GAME
# # ============================================================

# if not st.session_state.game_started:

#     st.divider()

#     st.info(
#         "Enter your name and choose a difficulty level "
#         "to start playing."
#     )

#     if st.button(
#         "🎮 Start Game",
#         type="primary",
#         use_container_width=True
#     ):

#         if not st.session_state.player_name:

#             st.warning(
#                 "Please enter your name first."
#             )

#         else:

#             start_new_game(selected_level)

#             st.rerun()


# # ============================================================
# # GAME
# # ============================================================

# if st.session_state.game_started:

#     level = st.session_state.game_level

#     settings = GAME_LEVELS[level]

#     level_name = settings["name"]
#     minimum = settings["min"]
#     maximum = settings["max"]
#     maximum_tries = settings["n_tries"]

#     st.divider()

#     st.subheader(
#         f"🎯 {level_name} Level"
#     )

#     st.write(
#         f"Hello **{st.session_state.player_name}**! "
#         f"Guess a number between "
#         f"**{minimum}** and **{maximum}**."
#     )

#     # --------------------------------------------------------
#     # ATTEMPT COUNTER
#     # --------------------------------------------------------

#     attempts = st.session_state.user_tries

#     remaining = maximum_tries - attempts

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         st.metric(
#             "Attempts",
#             f"{attempts} / {maximum_tries}"
#         )

#     with col2:

#         st.metric(
#             "Remaining",
#             remaining
#         )

#     with col3:

#         st.metric(
#             "Level",
#             level_name
#         )

#     # --------------------------------------------------------
#     # GUESS INPUT
#     # --------------------------------------------------------

#     if not st.session_state.game_over:

#         guess = st.number_input(
#             "Enter your guess",
#             min_value=minimum,
#             max_value=maximum,
#             value=minimum,
#             step=1,
#             key="guess_input"
#         )

#         if st.button(
#             "🎯 Guess",
#             type="primary",
#             use_container_width=True
#         ):

#             check_guess(int(guess))

#             st.rerun()

#     # --------------------------------------------------------
#     # GAME MESSAGE
#     # --------------------------------------------------------

#     if st.session_state.message:

#         message_type = st.session_state.message_type

#         if message_type == "success":

#             st.success(
#                 st.session_state.message
#             )

#         elif message_type == "warning":

#             st.warning(
#                 st.session_state.message
#             )

#         elif message_type == "error":

#             st.error(
#                 st.session_state.message
#             )

#             st.info(
#                 f"The hidden number was: "
#                 f"**{st.session_state.hidden}**"
#             )

#     # --------------------------------------------------------
#     # GAME WON
#     # --------------------------------------------------------

#     if (
#         st.session_state.game_over
#         and st.session_state.game_won
#     ):

#         st.balloons()

#         st.success(
#             f"🏆 Your Score: "
#             f"**{st.session_state.score} points**"
#         )

#         # ----------------------------------------------------
#         # SAVE SCORE
#         # ----------------------------------------------------

#         if not st.session_state.score_saved:

#             saved = save_score(
#                 player_name=st.session_state.player_name,
#                 level=level,
#                 tries=st.session_state.user_tries,
#                 score=st.session_state.score
#             )

#             if saved:

#                 st.session_state.score_saved = True

#                 st.success(
#                     "💾 Your score has been saved "
#                     "to the leaderboard!"
#                 )

#     # --------------------------------------------------------
#     # GAME OVER
#     # --------------------------------------------------------

#     if st.session_state.game_over:

#         st.divider()

#         if st.session_state.game_won:

#             st.subheader("🎉 You Won!")

#         else:

#             st.subheader("😔 Game Over")

#         # ----------------------------------------------------
#         # PLAY AGAIN
#         # ----------------------------------------------------

#         if st.button(
#             "🔄 Play Again",
#             type="primary",
#             use_container_width=True
#         ):

#             start_new_game(level)

#             st.rerun()


# # ============================================================
# # LEADERBOARD
# # ============================================================

# st.divider()

# st.subheader("🏆 Top 3 Players")


# top_players = get_top_players()


# if not top_players:

#     st.info(
#         "No scores yet. Be the first player "
#         "to reach the leaderboard! 🎮"
#     )

# else:

#     for index, player in enumerate(
#         top_players,
#         start=1
#     ):

#         player_name = player["player_name"]
#         game_level = player["game_level"]
#         tries = player["tries"]
#         score = player["score"]

#         if index == 1:
#             position = "🥇"

#         elif index == 2:
#             position = "🥈"

#         else:
#             position = "🥉"

#         col1, col2, col3, col4 = st.columns(
#             [0.6, 2.5, 1.5, 1]
#         )

#         with col1:

#             st.markdown(
#                 f"### {position}"
#             )

#         with col2:

#             st.markdown(
#                 f"**{player_name}**"
#             )

#         with col3:

#             st.write(
#                 f"{game_level}"
#             )

#         with col4:

#             st.write(
#                 f"**{score}** pts"
#             )


# # ============================================================
# # FOOTER
# # ============================================================

# st.divider()

# st.caption(
#     "🎯 Guess the Number • "
#     "Powered by Streamlit & Supabase"
# )



import random

import streamlit as st
from supabase import Client, create_client


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Guess the Number",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

@st.cache_resource
def init_supabase() -> Client:
    """
    Create and cache the Supabase client.
    """

    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


supabase = init_supabase()


# ============================================================
# GAME LEVELS
# ============================================================

GAME_LEVELS = {
    1: {
        "name": "Easy",
        "min": 1,
        "max": 10,
        "n_tries": 3,
        "base_score": 100,
    },

    2: {
        "name": "Intermediate",
        "min": 1,
        "max": 100,
        "n_tries": 7,
        "base_score": 300,
    },

    3: {
        "name": "Hard",
        "min": 1,
        "max": 1000,
        "n_tries": 15,
        "base_score": 500,
    },
}


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def initialize_session_state():
    """
    Initialize all required Streamlit session state variables.
    """

    defaults = {
        "player_name": "",
        "game_level": 1,
        "hidden": None,
        "user_tries": 0,
        "game_started": False,
        "game_over": False,
        "game_won": False,
        "score": 0,
        "message": "",
        "message_type": "",
        "score_saved": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


# ============================================================
# START NEW GAME
# ============================================================

def start_new_game(level):
    """
    Start a new game using the selected difficulty level.
    """

    settings = GAME_LEVELS[level]

    st.session_state.game_level = level

    st.session_state.hidden = random.randint(
        settings["min"],
        settings["max"]
    )

    st.session_state.user_tries = 0

    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.game_won = False

    st.session_state.score = 0

    st.session_state.message = ""
    st.session_state.message_type = ""

    st.session_state.score_saved = False


# ============================================================
# CALCULATE SCORE
# ============================================================

def calculate_score(level, tries):
    """
    Calculate the player's score.

    Higher difficulty = higher base score.
    Fewer attempts = higher bonus.
    """

    settings = GAME_LEVELS[level]

    base_score = settings["base_score"]
    maximum_tries = settings["n_tries"]

    bonus = (maximum_tries - tries + 1) * 10

    return base_score + bonus


# ============================================================
# SAVE SCORE TO SUPABASE
# ============================================================

def save_score(player_name, level, tries, score):
    """
    Save the player's winning score to Supabase.
    """

    level_name = GAME_LEVELS[level]["name"]

    data = {
        "player_name": player_name,
        "game_level": level_name,
        "tries": tries,
        "score": score,
    }

    try:

        supabase \
            .table("game_scores") \
            .insert(data) \
            .execute()

        return True

    except Exception as error:

        st.error(
            f"Unable to save your score.\n\n"
            f"Error: {error}"
        )

        return False


# ============================================================
# GET TOP 3 PLAYERS BY LEVEL
# ============================================================

def get_top_players(level_name):
    """
    Retrieve the top 3 players for a specific level.
    """

    try:

        response = (
            supabase
            .table("game_scores")
            .select(
                "player_name, game_level, tries, score"
            )
            .eq("game_level", level_name)
            .order("score", desc=True)
            .limit(3)
            .execute()
        )

        return response.data

    except Exception as error:

        st.error(
            f"Unable to load the {level_name} leaderboard.\n\n"
            f"Error: {error}"
        )

        return []


# ============================================================
# DISPLAY ONE PLAYER
# ============================================================

def display_player(player, position):
    """
    Display one player in the leaderboard.
    """

    player_name = player.get(
        "player_name",
        "Unknown"
    )

    tries = player.get(
        "tries",
        0
    )

    score = player.get(
        "score",
        0
    )

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    medal = medals.get(
        position,
        "🏅"
    )

    st.markdown(
        f"""
        **{medal} {player_name}**

        🎯 Score: **{score}**

        🔢 Tries: **{tries}**
        """
    )


# ============================================================
# DISPLAY LEADERBOARD FOR ONE LEVEL
# ============================================================

def display_level_leaderboard(level):
    """
    Display the Top 3 players for one specific level.
    """

    level_name = GAME_LEVELS[level]["name"]

    top_players = get_top_players(level_name)

    if not top_players:

        st.caption(
            "No players yet. Be the first! 🎮"
        )

        return

    for position, player in enumerate(
        top_players,
        start=1
    ):

        display_player(
            player,
            position
        )

        if position < len(top_players):

            st.divider()


# ============================================================
# CHECK GUESS
# ============================================================

def check_guess(guess):
    """
    Validate and check the player's guess.

    Invalid numbers outside the current level range
    do NOT consume an attempt.
    """

    if st.session_state.game_over:
        return

    level = st.session_state.game_level

    settings = GAME_LEVELS[level]

    minimum = settings["min"]
    maximum = settings["max"]

    hidden = st.session_state.hidden

    maximum_tries = settings["n_tries"]

    # --------------------------------------------------------
    # RANGE VALIDATION
    # --------------------------------------------------------

    if guess < minimum or guess > maximum:

        st.session_state.message = (
            f"⚠️ Invalid number! "
            f"Please enter a number between "
            f"**{minimum}** and **{maximum}**."
        )

        st.session_state.message_type = "error"

        # Invalid guess does NOT consume an attempt.
        return

    # --------------------------------------------------------
    # COUNT VALID ATTEMPT
    # --------------------------------------------------------

    st.session_state.user_tries += 1

    current_try = st.session_state.user_tries

    # --------------------------------------------------------
    # CORRECT GUESS
    # --------------------------------------------------------

    if guess == hidden:

        st.session_state.game_won = True
        st.session_state.game_over = True

        score = calculate_score(
            level,
            current_try
        )

        st.session_state.score = score

        st.session_state.message = (
            f"🎉 Congratulations! "
            f"You got it in {current_try} "
            f"{'try' if current_try == 1 else 'tries'}!"
        )

        st.session_state.message_type = "success"

        return

    # --------------------------------------------------------
    # MAXIMUM ATTEMPTS
    # --------------------------------------------------------

    if current_try >= maximum_tries:

        st.session_state.game_over = True
        st.session_state.game_won = False

        st.session_state.message = (
            f"Unfortunately, you used all "
            f"{maximum_tries} tries."
        )

        st.session_state.message_type = "error"

        return

    # --------------------------------------------------------
    # GUESS TOO LOW
    # --------------------------------------------------------

    if guess < hidden:

        st.session_state.message = (
            "📈 No, increase!"
        )

    # --------------------------------------------------------
    # GUESS TOO HIGH
    # --------------------------------------------------------

    else:

        st.session_state.message = (
            "📉 No, decrease!"
        )

    st.session_state.message_type = "warning"


# ============================================================
# SIDEBAR - TOP 3 PLAYERS
# ============================================================

with st.sidebar:

    st.title("🏆 Top 3 Players")

    st.caption(
        "Leaderboard for each difficulty level"
    )

    st.divider()

    # ========================================================
    # EASY LEADERBOARD
    # ========================================================

    st.subheader("🟢 Easy")

    st.caption(
        "Range: 1 - 10 • 3 Attempts"
    )

    display_level_leaderboard(1)

    st.divider()

    # ========================================================
    # INTERMEDIATE LEADERBOARD
    # ========================================================

    st.subheader("🟡 Intermediate")

    st.caption(
        "Range: 1 - 100 • 7 Attempts"
    )

    display_level_leaderboard(2)

    st.divider()

    # ========================================================
    # HARD LEADERBOARD
    # ========================================================

    st.subheader("🔴 Hard")

    st.caption(
        "Range: 1 - 1000 • 15 Attempts"
    )

    display_level_leaderboard(3)


# ============================================================
# HEADER
# ============================================================

st.title("🎯 Guess the Number")

st.markdown(
    """
    Try to guess the hidden number before
    you run out of attempts!
    """
)


# ============================================================
# PLAYER NAME
# ============================================================

st.subheader("👤 Player")

player_name = st.text_input(
    "Enter your name",
    value=st.session_state.player_name,
    max_chars=50,
    placeholder="e.g. Khaled"
)

st.session_state.player_name = player_name.strip()


# ============================================================
# DIFFICULTY LEVELS
# ============================================================

st.subheader("🎮 Game Levels")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 🟢 Easy")

    st.write(
        "Numbers: **1 – 10**"
    )

    st.write(
        "Tries: **3**"
    )

    st.write(
        "Base Score: **100**"
    )


with col2:

    st.markdown("### 🟡 Intermediate")

    st.write(
        "Numbers: **1 – 100**"
    )

    st.write(
        "Tries: **7**"
    )

    st.write(
        "Base Score: **300**"
    )


with col3:

    st.markdown("### 🔴 Hard")

    st.write(
        "Numbers: **1 – 1000**"
    )

    st.write(
        "Tries: **15**"
    )

    st.write(
        "Base Score: **500**"
    )


# ============================================================
# LEVEL SELECTION
# ============================================================

st.subheader("Choose Your Level")

selected_level = st.selectbox(
    "Difficulty",
    options=[1, 2, 3],
    format_func=lambda level: GAME_LEVELS[level]["name"],
    index=st.session_state.game_level - 1,
)


# ============================================================
# START GAME
# ============================================================

if not st.session_state.game_started:

    st.divider()

    st.info(
        "Enter your name and choose a difficulty level "
        "to start playing."
    )

    if st.button(
        "🎮 Start Game",
        type="primary",
        use_container_width=True
    ):

        if not st.session_state.player_name:

            st.warning(
                "Please enter your name first."
            )

        else:

            start_new_game(
                selected_level
            )

            st.rerun()


# ============================================================
# GAME
# ============================================================

if st.session_state.game_started:

    level = st.session_state.game_level

    settings = GAME_LEVELS[level]

    level_name = settings["name"]

    minimum = settings["min"]

    maximum = settings["max"]

    maximum_tries = settings["n_tries"]

    st.divider()

    st.subheader(
        f"🎯 {level_name} Level"
    )

    st.write(
        f"Hello **{st.session_state.player_name}**! "
        f"Guess a number between "
        f"**{minimum}** and **{maximum}**."
    )

    # ========================================================
    # ATTEMPT COUNTER
    # ========================================================

    attempts = st.session_state.user_tries

    remaining = maximum_tries - attempts

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Attempts",
            f"{attempts} / {maximum_tries}"
        )

    with col2:

        st.metric(
            "Remaining",
            remaining
        )

    with col3:

        st.metric(
            "Level",
            level_name
        )

    # ========================================================
    # GUESS INPUT
    # ========================================================

    if not st.session_state.game_over:

        guess = st.number_input(
            f"Enter your guess ({minimum} - {maximum})",
            min_value=minimum,
            max_value=maximum,
            value=minimum,
            step=1,
            key="guess_input"
        )

        st.caption(
            f"Your guess must be between "
            f"**{minimum}** and **{maximum}**."
        )

        if st.button(
            "🎯 Guess",
            type="primary",
            use_container_width=True
        ):

            check_guess(
                int(guess)
            )

            st.rerun()

    # ========================================================
    # GAME MESSAGE
    # ========================================================

    if st.session_state.message:

        message_type = (
            st.session_state.message_type
        )

        if message_type == "success":

            st.success(
                st.session_state.message
            )

        elif message_type == "warning":

            st.warning(
                st.session_state.message
            )

        elif message_type == "error":

            st.error(
                st.session_state.message
            )

            if st.session_state.game_over:

                st.info(
                    f"The hidden number was: "
                    f"**{st.session_state.hidden}**"
                )

    # ========================================================
    # GAME WON
    # ========================================================

    if (
        st.session_state.game_over
        and st.session_state.game_won
    ):

        st.balloons()

        st.success(
            f"🏆 Your Score: "
            f"**{st.session_state.score} points**"
        )

        # ----------------------------------------------------
        # SAVE SCORE
        # ----------------------------------------------------

        if not st.session_state.score_saved:

            saved = save_score(
                player_name=(
                    st.session_state.player_name
                ),
                level=level,
                tries=(
                    st.session_state.user_tries
                ),
                score=(
                    st.session_state.score
                )
            )

            if saved:

                st.session_state.score_saved = True

                st.success(
                    "💾 Your score has been saved "
                    "to the leaderboard!"
                )

    # ========================================================
    # GAME OVER
    # ========================================================

    if st.session_state.game_over:

        st.divider()

        if st.session_state.game_won:

            st.subheader(
                "🎉 You Won!"
            )

        else:

            st.subheader(
                "😔 Game Over"
            )

        # ----------------------------------------------------
        # PLAY AGAIN
        # ----------------------------------------------------

        if st.button(
            "🔄 Play Again",
            type="primary",
            use_container_width=True
        ):

            start_new_game(
                level
            )

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎯 Guess the Number • "
    "Powered by Streamlit & Supabase"
)