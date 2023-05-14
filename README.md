# Space Invaders Project
## CPSC 362 - Foundations of Software Engineering
### 2023-02-11 (Spring Semester 2023)
#### ahuynh86@csu.fullerton.edu
##### Andy Huynh

- The name of the game is "*Space Invaders*"
- 1-player


Project Goal:
The goal of this project is to recreate my own version of the Space Invaders game.
The Space Invaders game is a popular game that many people have recreated or made a version of their own. 
Whether it's imperfect or imperfect, I will try my best to attempt what others have tried to attempt. 


Game Objective:
The objective of the Space Invaders game is to control a player character that moves in only the y-axis(left and right).
As the enemy 'aliens' approach from the top of the screen, fend them off my shooting them before they destroy you.


Game Win condition:
- Shooting all of the 'aliens' until they are all wiped out.

Game-Over conditions:
- You run out of lives from getting shot at too much.
- The 'aliens' reach too close to you.


Game restrictions:
- Can only move left or right.

Prep to run game:
Game uses pygame and videogame packages. Also uses a virtual environment so check the requirements.txt
-To run a virtual environment in python:
-Creating virtual environment: python3 -m venv env
-Activate the virtual environment: source env/bin/activate
  This activates the virtual environment where pygame and videogame can be installed.
-Install the requirements: pip install -r requirements.txt
  OR
-pip install pygame  then  pip install -e videogame
  
