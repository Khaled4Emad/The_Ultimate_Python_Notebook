import random
import streamlit as st


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Guess the Number",
    page_icon="🎯",
    layout="centered"
)


# ============================================================
# Game Settings
# ============================================================

GAME_LEVELS = {
    1: {
        "name": "Easy",
        "limits": range(1, 11),
        "n_tries": 3,
    },
    2: {
        "name": "Intermediate",
        "limits": range(1, 101),
        "n_tries": 7,
    },
    3: {
        "name": "Hard",
        "limits": range(1, 1001),
        "n_tries": 15,
    },
}


# ============================================================
# Initialize Game State
# ============================================================

def initialize_game():
    """Initialize a new game."""

    if "game_level" not in st.session_state:
        st.session_state.game_level = 1

    if "hidden" not in st.session_state:
        st.session_state.hidden = random.choice(
            GAME_LEVELS[st.session_state.game_level]["limits"]
        )

    if "user_tries" not in st.session_state:
        st.session_state.user_tries = 0

    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    if "game_won" not in st.session_state:
        st.session_state.game_won = False

    if "message" not in st.session_state:
        st.session_state.message = ""

    if "message_type" not in st.session_state:
        st.session_state.message_type = ""


# ============================================================
# Start New Game
# ============================================================

def start_new_game(level):
    """Start a completely new game."""

    st.session_state.game_level = level

    limits = GAME_LEVELS[level]["limits"]

    st.session_state.hidden = random.choice(limits)
    st.session_state.user_tries = 0
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.message = ""
    st.session_state.message_type = ""


# ============================================================
# Check Guess
# ============================================================

def check_guess(guess):
    """Check the player's guess."""

    if st.session_state.game_over:
        return

    level_settings = GAME_LEVELS[st.session_state.game_level]

    n_tries = level_settings["n_tries"]
    hidden = st.session_state.hidden

    # Count the attempt
    st.session_state.user_tries += 1

    current_try = st.session_state.user_tries

    # Correct Guess
    if guess == hidden:

        st.session_state.game_won = True
        st.session_state.game_over = True

        st.session_state.message = (
            f"You got it successfully in "
            f"{current_try} "
            f"{'try' if current_try == 1 else 'tries'}! 🎉"
        )

        st.session_state.message_type = "success"

        return

    # Maximum Attempts Reached
    if current_try >= n_tries:

        st.session_state.game_over = True
        st.session_state.game_won = False

        st.session_state.message = (
            f"Unfortunately, you used the maximum "
            f"number of tries ({n_tries})."
        )

        st.session_state.message_type = "error"

        return

    # Guess Too Low
    if guess < hidden:

        st.session_state.message = "No, increase! 📈"
        st.session_state.message_type = "warning"

    # Guess Too High
    else:

        st.session_state.message = "No, decrease! 📉"
        st.session_state.message_type = "warning"


# ============================================================
# Initialize
# ============================================================

initialize_game()


# ============================================================
# Header
# ============================================================

st.title("🎯 Guess the Number")

st.write(
    "Try to guess the hidden number before you run out of attempts!"
)


# ============================================================
# Game Levels
# ============================================================

st.subheader("Game Levels")

level_col1, level_col2, level_col3 = st.columns(3)

with level_col1:
    st.info(
        "**🟢 Easy**\n\n"
        "Numbers: **1–10**\n\n"
        "Tries: **3**"
    )

with level_col2:
    st.info(
        "**🟡 Intermediate**\n\n"
        "Numbers: **1–100**\n\n"
        "Tries: **7**"
    )

with level_col3:
    st.info(
        "**🔴 Hard**\n\n"
        "Numbers: **1–1000**\n\n"
        "Tries: **15**"
    )


# ============================================================
# Difficulty Selection
# ============================================================

st.subheader("Choose Your Level")

selected_level = st.selectbox(
    "Game Level",
    options=[1, 2, 3],
    format_func=lambda level: GAME_LEVELS[level]["name"],
    index=st.session_state.game_level - 1,
)


# If user changes the level
if selected_level != st.session_state.game_level:

    start_new_game(selected_level)

    st.rerun()


# ============================================================
# Current Game Information
# ============================================================

level_settings = GAME_LEVELS[st.session_state.game_level]

level_name = level_settings["name"]
n_tries = level_settings["n_tries"]

min_number = min(level_settings["limits"])
max_number = max(level_settings["limits"])

st.divider()

st.subheader(f"Level: {level_name}")

st.write(
    f"Guess a number between **{min_number}** and **{max_number}**."
)


# ============================================================
# Attempts Counter
# ============================================================

remaining_tries = n_tries - st.session_state.user_tries

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Attempts",
        f"{st.session_state.user_tries} / {n_tries}"
    )

with col2:
    st.metric(
        "Remaining",
        remaining_tries
    )


# ============================================================
# Guess Input
# ============================================================

if not st.session_state.game_over:

    guess = st.number_input(
        "Enter your guess",
        min_value=min_number,
        max_value=max_number,
        step=1,
        value=min_number,
        key="guess_input",
    )

    if st.button(
        "🎯 Guess",
        type="primary",
        use_container_width=True,
    ):

        check_guess(int(guess))

        st.rerun()


# ============================================================
# Game Message
# ============================================================

if st.session_state.message:

    if st.session_state.message_type == "success":

        st.success(st.session_state.message)

    elif st.session_state.message_type == "error":

        st.error(st.session_state.message)

        st.info(
            f"The hidden number was: "
            f"**{st.session_state.hidden}**"
        )

    elif st.session_state.message_type == "warning":

        st.warning(st.session_state.message)


# ============================================================
# Game Over
# ============================================================

if st.session_state.game_over:

    st.divider()

    if st.session_state.game_won:

        st.balloons()

        st.success(
            "🏆 Congratulations! You won the game!"
        )

    else:

        st.error(
            "Game Over! Better luck next time."
        )

    # --------------------------------------------------------
    # Play Again
    # --------------------------------------------------------

    st.subheader("Play Again?")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Play Again",
            type="primary",
            use_container_width=True,
        ):

            start_new_game(st.session_state.game_level)

            st.rerun()

    with col2:

        if st.button(
            "🚪 Exit",
            use_container_width=True,
        ):

            st.session_state.message = (
                "Thanks for playing! 👋"
            )

            st.session_state.game_over = True

            st.stop()