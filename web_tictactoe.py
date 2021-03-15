from tictactoe_db import AsyncTicTacToeGameDB, TicTacToe, TicTacToeGameInfo
from user_db import UserDB
import asyncio
from asyncio_mqtt import Client, MqttError

USER_DB = UserDB()
TICTACTOE_DB = AsyncTicTacToeGameDB(USER_DB)


async def get_game(game_id):
    """
    the function retrieves the game data of the game related to the game_id

    :param game_id: ID of the Tic Tac Toe game
    :return: the Tic Tac Toe game data
    """
    the_game = await TICTACTOE_DB.get_game(game_id)
    return the_game


async def create_user(client, message_prop):
    """
    
    :param client: the MQTT brooker client
    :param message_prop:
    :return:
    """
    async with Client("test.mosquitto.org") as client:
        await client.subscribe("commands")

        try:
            the_username, password = USER_DB.create_user(message_prop)

        except ValueError:
            await client.publish(("user/" + str(the_username) + "/fail"), False, qos=2)
            raise MqttError("That username is not available. Please try again.")

        await client.publish(("user/" + str(the_username) + "/success"), True, qos=2)
        await asyncio.sleep(2)


async def create_game(client):
    try:
        game_uuid, term_password = await TICTACTOE_DB.add_game()
        await client.publish(("games/" + str(game_uuid)) + "/success", True, qos =2)
        await client.publish(("games/" + str(game_uuid) + "/password" + str(term_password)), True, qos=2)
    except KeyError:
        await client.publish
    await asyncio.sleep(2)


async def add_player_to_game(client, message_prop):
    message_prop_part = message_prop.split(",")
    game_uuid = message_prop_part[0]
    username = message_prop_part[1]

    the_game, game_info = TICTACTOE_DB.get_game(message_prop_part[0])
    await TICTACTOE_DB.add_player(game_uuid, username)
    if len(game_info.players) == 2:
        await client.publish(("games/" + str(game_uuid) + "/error"), False, qos=2)
        raise MqttError("The game is full. Please choose another game.")
    else:
        await client.publish(("games/" + str(game_uuid) + "/players" + str(username)),"added as player", qos=2 )
        await asyncio.sleep(2)


async def initialize(client, game_uuid):
    the_game, game_info = await TICTACTOE_DB.get_game(game_uuid)
    player1, player2 = game_info.players
    the_game.player_menu(player1, player2)
    player_choice = the_game.get_player_choices()
    player1_choice = player_choice.value(player1)
    player2_choice = player_choice.value(player2)

    await client.publish(("games/" + str(game_uuid) + "/players/" + player1 + "/choice"), str(player1_choice),qos=2)
    await client.publish(("games/" + str(game_uuid) + "/players/" + player2 + "/choice"), str(player2_choice), qos=2)
    await asyncio.sleep(2)


async def current_sign(client, game_uuid):
    the_game, game_info = await TICTACTOE_DB.get_game(game_uuid)
    curr_sign = the_game.current_sign()
    await client.publish(("games/" + str(game_uuid) + "/current_sign/"), str(curr_sign),qos=2)
    await asyncio.sleep(2)


async def switch_player(game_uuid):
    the_game, game_info = await TICTACTOE_DB.get_game(game_uuid)
    player1, player2 = game_info.players
    the_game.switch_player(player1, player2)


async def player_move(client, message_prop):
    message_prop_part = message_prop.split(",")
    game_uuid = message_prop_part[0]
    move = message_prop_part[1]

    the_game, game_info = await TICTACTOE_DB.get_game(game_uuid)
    curr_sign = await the_game.current_sign()
    the_game.player_move_exe(move, curr_sign)
    player_pos = the_game.get_player_pos()
    await switch_player(game_uuid)

    await client.publish(("games/" + str(game_uuid) + "/players_pos"), dict(player_pos), qos=2)
    await asyncio.sleep(2)


async def winner_check(client, game_uuid):
    the_game, game_info = await TICTACTOE_DB.get_game(game_uuid)
    curr_sign = await the_game.current_sign()
    curr_player = the_game.get_current_player()

    if the_game.check_win(curr_sign):
        await client.publish(("games/" + str(game_uuid) + "/game_status/win"), str(curr_player), qos=2)
    if the_game.check_draw():
        await client.publish(("games/" + str(game_uuid) + "/game_status/draw"), True, qos=2)
    await asyncio.sleep(2)


async def message_sort():
    async with Client("test.mosquitto.org") as client:
        await client.subscribe("commands")
        async with client.unfiltered_messages() as messages:
            async for message in messages:
                message_line: str = message.payload.decode()

                if message_line.startswith("create_user"):
                    message_prop = message_line.replace("create_user", '')
                    await create_user(client, message_prop)

                elif message_line.startswith("create_game"):
                    await create_game(client)

                elif message_line.startswith("add_player_to_game"):
                    message_prop = message_line.replace("add_player_to_game", '')
                    await add_player_to_game(client, message_prop)

                elif message_line.startswith("initialize"):
                    game_uuid = message_line.replace("initialize", '')
                    await add_player_to_game(client, game_uuid)

                elif message_line.startswith("player_move"):
                    message_prop = message_line.replace("player_move", '')
                    await player_move(client, message_prop)

                elif message_line.startswith("winner_check"):
                    game_uuid = message_line.replace("winner_check",'')
                    await winner_check(client, game_uuid)


async def main():
    reconnect_interval = 3
    while True:
        try:
            await message_sort()
        except MqttError as error:
            print(f'Error {error}.Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)

if __name__ == "__main__":
    main()
    asyncio.run(main())