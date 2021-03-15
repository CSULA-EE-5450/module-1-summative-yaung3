from uuid import uuid4
from typing import List, Tuple, Dict, Union
from tictactoe.tictactoe import TicTacToe
from user_db import UserDB
from dataclasses import dataclass
from fastapi import HTTPException, status
import asyncio


@dataclass
class TicTacToeGameInfo:
    players: List[str]
    game_uuid: str
    termination_password: str


class AsyncTicTacToeGameDB(object):
    def __init__(self, user_db: UserDB):
        self._current_games: Dict[str, TicTacToe] = {}
        self._current_games_info: Dict[str, TicTacToeGameInfo] = {}
        self._QUERY_TIME: float = 0.05
        self._user_db = user_db

    async def add_game(self):
        """
        Adds a new game of Tic Tac Toe

        :return: The game_id and termination password of the game that was created.
        """
        await asyncio.sleep(self._QUERY_TIME)
        game_uuid = str(uuid4())
        game_term_password = str(uuid4())
        self._current_games[game_uuid] = TicTacToe()
        self._current_games_info[game_uuid] = TicTacToeGameInfo(
            list(),
            game_uuid,
            game_term_password)
        return game_uuid, game_term_password

    async def add_player(self, game_uuid: str, username: str) -> int:
        """
        Add a existing user to the game.

        :param game_uuid: ID of the game.
        :param username: Username of the player to be added
        :return: number of players in the game
        """
        self._current_games_info[game_uuid].players.append(username)
        return len(self._current_games_info[game_uuid].players)

    async def list_games(self) -> List[Tuple[str, List[str]]]:
        """
        List out the games existing and the game_id and player names' associated with the games.

        :return: game_id and the list of players for all existing games
        """
        await asyncio.sleep(self._QUERY_TIME)
        players = TicTacToeGameInfo.players
        return [(game_id, players) for game_id, game in self._current_games.items()]

    async def get_game(self, game_id: str) -> Tuple[Union[TicTacToe, None], Union[TicTacToeGameInfo, None]]:
        """
        Retrieves the game info of a specific game

        :param game_id: ID of the specific game
        :return: the game data and game info
        """
        await asyncio.sleep(self._QUERY_TIME)
        return self._current_games.get(game_id, None), self._current_games_info.get(game_id, None)

    async def del_game(self, game_id: str, term_pass: str) -> bool:
        """
        Terminates a game and deletes from the list of games.

        :param game_id: ID of the game.
        :param term_pass: Termination password assigned at the creation of the game.
        :return: Boolean. True if game was deleted. False if there was an error in deletion.
        """
        try:
            await asyncio.sleep(self._QUERY_TIME)
            if self._current_games_info[game_id].termination_password == term_pass:
                del self._current_games[game_id]
                del self._current_games_info[game_id]
                return True
            else:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authorized")
        except KeyError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "game_id not found")

