import random
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh


# ============================================================
# Constants
# ============================================================

TURN_TIME_LIMIT = 10


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)


# ============================================================
# Game Functions
# ============================================================

def create_board():
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]


def start_round():
    """
    Randomly select:
    - Which player starts
    - X / O assignment
    """

    players = [
        st.session_state.player1,
        st.session_state.player2
    ]

    # Randomly select starting player
    random.shuffle(players)

    st.session_state.starting_player = players[0]
    st.session_state.current_player = players[0]

    # Randomly assign X and O
    symbols = ["X", "O"]
    random.shuffle(symbols)

    st.session_state.symbols = {
        players[0]: symbols[0],
        players[1]: symbols[1]
    }

    # Create new board
    st.session_state.board = create_board()

    # Reset round state
    st.session_state.round_over = False
    st.session_state.round_winner = None

    # Start the 10-second timer
    st.session_state.turn_start_time = time.time()


def start_game():
    st.session_state.game_started = True
    st.session_state.game_finished = False

    st.session_state.current_round = 1

    st.session_state.score = {
        st.session_state.player1: 0,
        st.session_state.player2: 0
    }

    start_round()


def reset_game():

    keys_to_remove = [
        "game_started",
        "game_finished",
        "player1",
        "player2",
        "total_rounds",
        "current_round",
        "score",
        "board",
        "current_player",
        "starting_player",
        "symbols",
        "round_over",
        "round_winner",
        "turn_start_time"
    ]

    for key in keys_to_remove:

        if key in st.session_state:
            del st.session_state[key]


def check_win(board, symbol):

    winning_combinations = [

        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for combination in winning_combinations:

        if all(
            board[row][col] == symbol
            for row, col in combination
        ):
            return True

    return False


def check_draw(board):

    return all(
        board[row][col] != ""
        for row in range(3)
        for col in range(3)
    )


def change_player():

    if st.session_state.current_player == st.session_state.player1:

        st.session_state.current_player = (
            st.session_state.player2
        )

    else:

        st.session_state.current_player = (
            st.session_state.player1
        )

    # Reset timer for the new player
    st.session_state.turn_start_time = time.time()


def make_move(row, col):

    if st.session_state.round_over:
        return False

    board = st.session_state.board

    player = st.session_state.current_player

    symbol = st.session_state.symbols[player]

    # Ignore occupied cell
    if board[row][col] != "":
        return False

    # Make move
    board[row][col] = symbol

    # Check winner
    if check_win(board, symbol):

        st.session_state.score[player] += 1

        st.session_state.round_winner = player
        st.session_state.round_over = True

        return True

    # Check draw
    if check_draw(board):

        st.session_state.round_winner = None
        st.session_state.round_over = True

        return True

    # Change player
    change_player()

    return True


def make_random_move():

    if st.session_state.round_over:
        return

    board = st.session_state.board

    player = st.session_state.current_player

    # Find all empty cells
    empty_cells = [
        (row, col)
        for row in range(3)
        for col in range(3)
        if board[row][col] == ""
    ]

    # No empty cells
    if not empty_cells:
        return

    # Select random empty cell
    row, col = random.choice(empty_cells)

    # Make the move
    make_move(row, col)

    # Store information for UI
    st.session_state.timeout_move = True


def next_round():

    if (
        st.session_state.current_round
        >= st.session_state.total_rounds
    ):

        st.session_state.game_finished = True

        return

    st.session_state.current_round += 1

    start_round()


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .score-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(128, 128, 128, 0.3);
    }

    .score-name {
        font-size: 20px;
        font-weight: 700;
    }

    .score-number {
        font-size: 42px;
        font-weight: 800;
    }

    .round-info {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin: 15px 0;
    }

    .timer {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        margin: 15px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Session State Initialization
# ============================================================

if "game_started" not in st.session_state:

    st.session_state.game_started = False


# ============================================================
# Welcome / Setup Screen
# ============================================================

if not st.session_state.game_started:

    st.markdown(
        '<div class="main-title">🎮 Tic Tac Toe</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'The classic game — now with multiple rounds!'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # Players
    # --------------------------------------------------------

    st.subheader("👥 Players")

    col1, col2 = st.columns(2)

    with col1:

        player1 = st.text_input(
            "Player 1",
            placeholder="Enter player 1 name"
        )

    with col2:

        player2 = st.text_input(
            "Player 2",
            placeholder="Enter player 2 name"
        )

    # --------------------------------------------------------
    # Game Settings
    # --------------------------------------------------------

    st.subheader("🏆 Game Settings")

    total_rounds = st.number_input(
        "Number of rounds",
        min_value=1,
        max_value=99,
        value=3,
        step=2
    )

    st.info(
        "🎲 The starting player and X/O symbols "
        "will be randomly selected for every round."
    )

    st.warning(
        f"⏱️ Each player has only "
        f"**{TURN_TIME_LIMIT} seconds** to make a move."
    )

    st.write("")

    # --------------------------------------------------------
    # Start Game
    # --------------------------------------------------------

    if st.button(
        "🚀 Start Game",
        use_container_width=True,
        type="primary"
    ):

        if not player1.strip():

            st.error(
                "Please enter Player 1 name."
            )

        elif not player2.strip():

            st.error(
                "Please enter Player 2 name."
            )

        elif (
            player1.strip().lower()
            == player2.strip().lower()
        ):

            st.error(
                "Players must have different names."
            )

        else:

            st.session_state.player1 = player1.strip()

            st.session_state.player2 = player2.strip()

            st.session_state.total_rounds = int(
                total_rounds
            )

            start_game()

            st.rerun()


# ============================================================
# Game Finished
# ============================================================

elif st.session_state.game_finished:

    st.markdown(
        '<div class="main-title">🏆 Game Over!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Final Results</div>',
        unsafe_allow_html=True
    )

    st.divider()

    player1 = st.session_state.player1
    player2 = st.session_state.player2

    score1 = st.session_state.score[player1]
    score2 = st.session_state.score[player2]

    # --------------------------------------------------------
    # Final Score
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
                <div class="score-card">

                <div class="score-name">
                    {player1}
                </div>

                <div class="score-number">
                    {score1}
                </div>

                </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
                <div class="score-card">

                <div class="score-name">
                    {player2}
                </div>

                <div class="score-number">
                    {score2}
                </div>

                </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # --------------------------------------------------------
    # Champion
    # --------------------------------------------------------

    if score1 > score2:

        st.success(
            f"🎉 {player1} is the Champion!"
        )

    elif score2 > score1:

        st.success(
            f"🎉 {player2} is the Champion!"
        )

    else:

        st.info(
            "🤝 The match ended in a draw!"
        )

    st.write("")

    # --------------------------------------------------------
    # Play Again
    # --------------------------------------------------------

    if st.button(
        "🔄 Play Again",
        use_container_width=True,
        type="primary"
    ):

        reset_game()

        st.rerun()


# ============================================================
# Game Screen
# ============================================================

else:

    # ========================================================
    # Auto Refresh
    # ========================================================

    # Refresh every 1 second so the countdown is updated.
    st_autorefresh(
        interval=1000,
        key="turn_timer"
    )

    # ========================================================
    # Player Information
    # ========================================================

    player1 = st.session_state.player1
    player2 = st.session_state.player2

    score1 = st.session_state.score[player1]
    score2 = st.session_state.score[player2]

    # ========================================================
    # Header
    # ========================================================

    st.markdown(
        '<div class="main-title">🎮 Tic Tac Toe</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="round-info">
            Round {st.session_state.current_round}
            / {st.session_state.total_rounds}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # Score
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        symbol1 = st.session_state.symbols[player1]

        st.markdown(
            f"""
    <div class="score-card">
    <div class="score-name">{player1} &nbsp; {symbol1}</div>
    <div class="score-number">{score1}</div>
    </div>
    """,
            unsafe_allow_html=True
        )


    with col2:

        symbol2 = st.session_state.symbols[player2]

        st.markdown(
            f"""
    <div class="score-card">
    <div class="score-name">{player2} &nbsp; {symbol2}</div>
    <div class="score-number">{score2}</div>
    </div>
    """,
            unsafe_allow_html=True
        )

    st.write("")

    # ========================================================
    # Timer / Timeout
    # ========================================================

    if not st.session_state.round_over:

        elapsed_time = (
            time.time()
            - st.session_state.turn_start_time
        )

        remaining_time = max(
            0,
            TURN_TIME_LIMIT - int(elapsed_time)
        )

        current_player = (
            st.session_state.current_player
        )

        current_symbol = (
            st.session_state.symbols[current_player]
        )

        # ----------------------------------------------------
        # Timeout
        # ----------------------------------------------------

        if elapsed_time >= TURN_TIME_LIMIT:

            st.warning(
                f"⏰ {current_player} ran out of time!"
            )

            make_random_move()

            st.rerun()

        # ----------------------------------------------------
        # Normal Timer
        # ----------------------------------------------------

        else:

            st.info(
                f"🎯 **{current_player}'s Turn** "
                f"({current_symbol})"
            )

            st.markdown(
                f"""
                <div class="timer">
                    ⏱️ {remaining_time} seconds
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # Round Status
    # ========================================================

    if st.session_state.round_over:

        if st.session_state.round_winner:

            winner = (
                st.session_state.round_winner
            )

            st.success(
                f"🎉 {winner} won Round "
                f"{st.session_state.current_round}!"
            )

        else:

            st.info(
                "🤝 This round ended in a draw!"
            )


    # ========================================================
    # Board
    # ========================================================

    st.write("")

    board = st.session_state.board

    for row in range(3):

        columns = st.columns(3)

        for col in range(3):

            value = board[row][col]

            button_label = (
                value
                if value
                else " "
            )

            if columns[col].button(
                button_label,
                key=(
                    f"cell_"
                    f"{st.session_state.current_round}_"
                    f"{row}_"
                    f"{col}"
                ),
                use_container_width=True,
                disabled=(
                    st.session_state.round_over
                    or value != ""
                )
            ):

                make_move(row, col)

                st.rerun()


    # ========================================================
    # Next Round
    # ========================================================

    if st.session_state.round_over:

        st.write("")

        if (
            st.session_state.current_round
            < st.session_state.total_rounds
        ):

            if st.button(
                "➡️ Next Round",
                use_container_width=True,
                type="primary"
            ):

                next_round()

                st.rerun()

        else:

            if st.button(
                "🏆 Show Final Results",
                use_container_width=True,
                type="primary"
            ):

                next_round()

                st.rerun()


    # ========================================================
    # Restart
    # ========================================================

    st.divider()

    if st.button(
        "🔄 Restart Game",
        use_container_width=True
    ):

        reset_game()

        st.rerun()