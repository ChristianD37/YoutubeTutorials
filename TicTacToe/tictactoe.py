import os
from helpers import check_turn, check_for_win, draw_board

# Declare all the variables we're going to need
spots = {1 : '1', 2 : '2', 3: '3', 4 : '4', 5 : '5', 
         6 : '6', 7 : '7',  8 : '8', 9 : '9'}
playing, complete = True, False
turn = 0
prev_turn = -1
# Game Loop
while playing:
    # Reset the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    # Draw the current Game Board
    draw_board(spots)
    # If an invalid turn occurred, let the player know
    if prev_turn == turn:
      print("Invalid spot selected, please pick another.")
    prev_turn = turn
    print("Player " + str((turn % 2) +1 ) + "'s turn: Pick your spot or press q to quit")
    
    # Get input and make sure it's valid
    choice = input()
    # The game has ended, 
    if choice == 'q':
        playing = False
    elif str.isdigit(choice) and int(choice) in spots:
      # Check if the spot is already taken.
      if not spots[int(choice)] in {"X", "O"}:
        # If not, update board and increment the turn
        turn += 1
        spots[int(choice)] = check_turn(turn)
      
    # Check if the game has ended (and if someone won)
    if check_for_win(spots): playing, complete = False, True
    if turn > 8: playing = False
    
# Update the board one last time. 
os.system('cls' if os.name == 'nt' else 'clear')
draw_board(spots)
# If there was a winner, say who won
if complete:
  if check_turn(turn) == 'X': print("Player 1 Wins!")
  else: print("Player 2 Wins!")
else: 
  # Tie Game
  print("No Winner")
  
print("Thanks for playing!") 