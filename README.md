# Cyvatar
2D Game with a similar Battle style of Megaman Battle Network but with a personal touch

<img width="963" height="563" alt="Screenshot 2026-11-08 111712" src="https://github.com/user-attachments/assets/5d824141-5372-4ad6-9b11-31cf2d4d3a22" />

I'm not sure if I should continue this project using pygame, since the performance limitations could become a problem later on. In any case, I will leave this repository here for anyone that would like an initial good foundation to improve upon istead of starting from zero. 

## This implementation includes:
### HP Barr
  - Has the same size regardless of the MAX amount of HP the player has. But the actual HP is proportionally made to fit in inside of the barr.
  - Changes color in a discrete manner according to the HP level;
### Energy Barr
  - The color lerps according to the energy level. It goes from a light blue (max energy) and dark blue (low energy);
  - A certain amount of time after the last energy usage, the barr automatically starts to fill up again at a linear rate;
  - If the barr is fully depleted, the amount of time to wait before the automatic recharge is greater;
### Mana Barr
  - Created with a series of images, each one representing, aproximately
  - When charging, the images are displayed one after the other, thus creating the illusion of a charging progression.
  - The barr starts with an empty image (empty barr) and ends with a full magic flame (full barr);
### Caracter Movement
  - Character is able to move through the Battle Field's grid using energy.
  - There is a cooldown time after the character has been moved;
  - The Caracter is bound by the Battlefield limits, wich go from the first row of the grid to the center of the grid;
  - If the Player is performing other actions (ex: Charging or Blocking) he will be prevented from moving;
### Attack
  - Attacks can be perfomed by consuming the amount of energy associated to that attack;
  - Player has different types of attacks available to choose from;
  - The attack that is currently equipped is displayed by the HUD;
  - Each attack has a cooldown time before it can be used again;
  - The cooldown for each attack depends on its type;
### Charging
  - When charging, the level of Mana increases as shown by the Mana Barr;
  - A DragonBall-like aura animation is displayed around the Character;
  - Player is unable to move when charging;
### Inputs 
- Mapped from a DualSense controller;
- L2: Switch the currently equiped attack to another energy consuming attack (it cycles back to the starting attack);
- L1: Charge Mana;
- R2: Use Block;
- R1: Use currently equiped attack;
- Arrows: Character Movement;

