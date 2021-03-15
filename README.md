# EE 5450 Module 1 Summative
# Tic Tac Toe game 

# How to game works 
1. The player menu allows the user to select their sign, between X and O, and the second player gets the other sign automatically assigned. 
The plyaer menu should look like this: 
```
Player 1
Enter the name : Ye

Player 2
Enter the name : Ye2

Turn to choose for Ye
Enter 1 for X
Enter 2 for O
```
2. The 1st player is asked to type in an integer between 1 and 9 to place their sign on the grid. 
The reequest shoudl appear as following:
```
	     |     |
	     |     |   
	_____|_____|_____
	     |     |
	     |     |   
	_____|_____|_____
	     |     |
	     |     |   
	     |     |


Player: Ye with 'X'. It is your turn. Which box? : 
```

3. The grid number asssignment on the game board is as follows: 
```
	     |     |
	  1  |  2  |  3  
	_____|_____|_____
	     |     |
	  4  |  5  |  6
	_____|_____|_____
	     |     |
	  7  |  8  |  9 
	     |     |
 ```
 4. The move is executed when the user input the grid number desired. 
```
Player: Ye with 'X'. It is your turn. Which box? : 5


	     |     |
	     |     |   
	_____|_____|_____
	     |     |
	     |  X  |   
	_____|_____|_____
	     |     |
	     |     |   
	     |     |
```
 5. The turns are switched automatically as soon as the current player has placed their chosen sign. 
```
Player: Ye with 'X'. It is your turn. Which box? : 5


	     |     |
	     |     |   
	_____|_____|_____
	     |     |
	     |  X  |   
	_____|_____|_____
	     |     |
	     |     |   
	     |     |


Player: Ye2 with 'O'. It is your turn. Which box? : 
```
 6. The game ends when there is a winner or the game is drawn. 
Game win example:
```
Player: Ye with 'X'. It is your turn. Which box? : 6


	     |     |
	  O  |     |   
	_____|_____|_____
	     |     |
	  X  |  X  |  X
	_____|_____|_____
	     |     |
	     |     |  O
	     |     |


Player: Ye with 'X has won the game!!
```
Game draw example: 
```
Player: Ye with 'X'. It is your turn. Which box? : 9


	     |     |
	  O  |  X  |  X
	_____|_____|_____
	     |     |
	  X  |  X  |  O
	_____|_____|_____
	     |     |
	  O  |  O  |  X
	     |     |


Game Drawn 
```
Note: The details of the Tic Tac Toe game code can be read in the docstrings of the tictactoe.py

# How to play the game via MQTT client 
The game can be played using a MQTT client, such as MQTT explorer (. 
- The MQTT web code is configured to the client "test.mosquitto.org" and unsecured port 1883.
- The commands for the game can be published to the topic "command" with the message type set to Raw

## MQTT message command list
1. create_user 
```
Creates a user in the data base.
    Topic: commands
    MQTT Message: create_user username
    :param client: the MQTT broker client
    :param message_prop: username desired
    :return:username and password
```
2. create_game 
```
Creates a Tic Tac Toe session
    Topic: commands
    MQTT Message: create_game
    :param client: MQTT broker client
    :return: the game_id and termination password of the created game
```
3. add_player_to_game
```
 Adds a player to the existing Tic Tac Toe game.
    Topic: commands
    MQTT message: add_player_to_game game_uuid, username
    :param client: MQTT client
    :param message_prop: game_uuid = ID of the game, username: username of the user to be added
```
4. initialize 
```
Initialize the Tic Tac Toe game.
    Topic: commands
    MQTT message: initialize game_uuid
    :param client: MQTT broker client
    :param game_uuid: ID of the Tic Tac Toe game
 ```
 5. current_sign
 ```
 Gives the current sign (X or O) of the current player.
    Topic: commands
    MQTT message: current_sign game_uuid
    :param client: MQTT Broker Client
    :param game_uuid: the ID of the game
    :return: the sign of current player
```
6. player_move
```
Execute a player's requested move.
    Topic: commands
    MQTT message: player_move game_uuid, move
    :param client: MQTT Broker Client
    :param message_prop: game_uuid = ID of the game, move = Grid number of where the players would like to place their sign
```
7. winner_check
```
Checks if there's a winner in the game or if the game is drawn
    Topic: commands
    MQTT message: winner_check game_uuid
    :param client: MQTT broker client
    :param game_uuid: the ID of the game in interest
```

