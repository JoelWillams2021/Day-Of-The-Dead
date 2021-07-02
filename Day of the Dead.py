#-------------------------------------------------------------------------------------------------------------------------------
# Name:        Day of the Dead
# Purpose:     A zombie shooter, where you have to survive hordes of the undead with the aid of some powerups like health packs
#
# Author:      Amogh Turaga
# Created:     29-Oct-2020
# Updated:     6-Nov-2020
#--------------------------------------------------------------------------------------------------------------------------------

import random
import time
import math


#Sets the core variables that will be used throughout the program
WIDTH = 1000
HEIGHT = 850

game_state = "start"
music.play_once("start menu song")

def start_up_variables():
    "A function that creates all the variables and actors that'll be used throughout the program"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    lives = 5
    futureTime = time.time()
    zombie_lives = 5
    zombie_clear = 0
    zombies = []
    final_lives = 0
    max_bullets = 1
    for i in range (30):
        single_zombie = Actor("zombie", (random.randint(0,WIDTH), random.randint(0,HEIGHT)) )
        zombies.append(single_zombie)
    health_packs = []
    for i in range (2):
        health_pack = Actor("health_pack", (random.randint(0,WIDTH), random.randint(0,HEIGHT)))
        health_packs.append(health_pack)       
    ammo_kits = []
    for i in range (2):
        ammo_kit = Actor("ammo_kit" , (random.randint(0,WIDTH), random.randint(0,HEIGHT)))
        ammo_kits.append(ammo_kit)
  
  
# Draws all the buttons in the menus that you can interact with
button_quit_draw = [395,425,125,55]
button_quit = Rect(button_quit_draw)
button_try_again_draw = [395,495,235,70.5]
button_try_again = Rect(button_try_again_draw)
button_start_draw = [367.5,220,185,45]
button_start = Rect(button_start_draw)


# Draws actors and sets up a actor list that will be modified later    
main_character = Actor("main_character", center = (75,75))
background = Actor("background")
bullets = []


 
def main_character_movement_health():
    "Sets up the main character's movement across the screen and health depletion"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    if keyboard.right:
        main_character.x += 5    
    elif keyboard.left:
        main_character.x += -5
    elif keyboard.up:
        main_character.y += -5
    elif keyboard.down:
        main_character.y += 5
    for zombie in zombies:
        if zombie.colliderect(main_character):
            if futureTime < time.time():
                lives -= 1
                futureTime = time.time() + 0.5
                music.set_volume(.1)
                music.play_once("health sound effect")
            if lives == 0:
                game_state = "Lose screen"
                
            

def arena_barriers():
    "Sets up arena barriers that player cannot cross"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    if main_character.left >= WIDTH:
        main_character.right = WIDTH
    elif main_character.right <= 0:
        main_character.left = 0
    elif main_character.top >= HEIGHT:
        main_character.bottom = HEIGHT
    elif main_character.bottom <= 0:
        main_character.top = 0
    
           
def on_mouse_move(pos):
    "If game state is in game scene (run) then set main character to face mouse and zombies to face main character"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    if game_state == "run":
        main_character.angle = main_character.angle_to(pos)
        for zombie in zombies:
            zombie.angle = zombie.angle_to(main_character.pos)
       
     
def zombie_movement_health():
    "Sets up zombie movement across the screen and health depletion"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, lives, final_lives
    for zombie in zombies:
        if main_character.x > zombie.x :
            zombie.x += 1
        if main_character.x < zombie.x:
            zombie.x += -1
        if main_character.y > zombie.y :
            zombie.y += 1
        if main_character.y < zombie.y:
            zombie.y += -1
        for bullet in bullets:
            if bullet.colliderect(zombie):
                zombies.remove(zombie)
                bullets.remove(bullet)
                zombie_clear += 1
            #Sets up read and write file variable at end
            if zombie_clear == 30:
                game_state = "Win screen"
                final_lives = lives
                
                
                
def on_mouse_up(pos, button):
    "On mouse up set up where bullets face, create the bullet actor and movement/positonal variables"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    mouse_value = mouse.LEFT
    if game_state != "start":
        if mouse_value == button and len(bullets) < max_bullets:
            bullet = Actor("bullet_projectile", pos=(main_character.pos))
            bullets.append(bullet)
            mouse_pos = pos
            bullet.angle = bullet.angle_to(mouse_pos)
            bullet.move = False   
            bullet.speed = 10  
            bullet.xDirection = 1 
            bullet.yDirection = 1



def bullet_movement():
    "Makes bullets move towards where mouse is clicked"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    for bullet in bullets:
        #Code used from here https://github.com/HDSB-GWS/ICS3-Python-Notes/blob/master/examples/pgzero/games/actor%20-%20move%20on%20angle.py (line 113-118)
        bullet.move = True
        bullet.xDirection = math.cos(math.radians(bullet.angle))
        bullet.yDirection = -math.sin(math.radians(bullet.angle))
        if bullet.move == True:
            bullet.x += bullet.speed*bullet.xDirection 
            bullet.y += bullet.speed*bullet.yDirection
            music.set_volume(.15)
            music.play_once("gunshot sound effect")
        #--------------------------------------------------------
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                bullets.remove(bullet)
                
       
def health_kit_collision():
    "Increase player's health if it collides with this actor"
    global lives, health_pack, max_bullets, mouse_value, futureTime, zombies_lives, game_state, zombie_clear,  zombies, health_packs, ammo_kits, final_lives
    for health_pack in health_packs:
        if main_character.colliderect(health_pack) and lives < 5:
            lives += 1
            health_packs.remove(health_pack)
            music.set_volume(.1)
            music.play_once("health kit sound effect")


def ammo_kit_collision():
    "Increase how many bullets you can shoot at once if it collides with this actor"
    global lives, ammo_kit, max_bullets, mouse_value, futureTime, zombies_lives, game_state, zombie_clear,  zombies, health_packs, ammo_kits, final_lives
    for ammo_kit in ammo_kits:
         if main_character.colliderect(ammo_kit):
            max_bullets += 2
            ammo_kits.remove(ammo_kit)
            music.set_volume(.2)
            music.play_once("ammo pick up")
    
    
def draw_text():
    "Draws useful game information onto game screen"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, final_lives
    screen.draw.text("Lives: " + str(lives), (350,30) , color = "white", fontsize = 35)
    screen.draw.text("Max bullets on screen: " + str(max_bullets), (45,30), color = "white", fontsize = 35 )
  
  
def write_files():
    "Updates a file with player's remaining lives after they've quit"
    global final_lives
    string = str(final_lives)
    file = open('highest_lives.txt', 'a')
    file.write(string)
    file.write("\n")
    file.close()
    

def read_files():
    "Reads the aformentioned file that gets updated and ouptuts it" 
    global final_lives
    reading_handle = open("highest_lives.txt", "r")
    while True:
        line = reading_handle.readline()
        if len(line) == 0:
            break
        print(line, end = "")
    reading_handle.close()
       
   
def on_mouse_down(pos):
    "On mouse down if player clicks try again or start, game goes to game screen and if player clicks quit output the read_files file/quit"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear,  zombies, health_packs, ammo_kits, final_lives
    if game_state == "Win screen" or game_state == "Lose screen":
        if button_quit.collidepoint(pos):
            write_files()
            read_files()
            quit()
        elif button_try_again.collidepoint(pos):
            game_state = "run"
            start_up_variables()
    if game_state == "start":
        if button_start.collidepoint(pos):
            game_state = "run"
            start_up_variables()
            
        
def update():
    "Update these functions (loop)"
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, bullet, zombie_clear,  zombies, health_packs, ammo_kits, final_lives
    if game_state == "run":
        main_character_movement_health()
        zombie_movement_health()
        bullet_movement()
        arena_barriers()
        health_kit_collision()
        ammo_kit_collision()
 

def draw():
    #Draws game scene actors if game state is run
    global max_bullets, mouse_value, lives, futureTime, zombies_lives, game_state, zombie_clear, zombies, health_packs, ammo_kits, final_lives
    if game_state == "run":
        screen.clear()
        background.draw()
        main_character.draw()
        for zombie in zombies:
            zombie.draw()
        for bullet in bullets:
            bullet.draw()
        for health_pack in health_packs:
            health_pack.draw()
        for ammo_kit in ammo_kits:
            ammo_kit.draw()
        draw_text()
    #If game state is lose screen or start screen or win screen draw these things
    if game_state == "Lose screen":
        screen.clear()
        music.stop()
        screen.fill ((186, 19, 27))
        screen.draw.filled_rect(button_quit, (255,69,0))
        screen.draw.text("Quit", centery = 455, right = 498, fontsize = 64, align = "center", color = "yellow")
        screen.draw.filled_rect(button_try_again, ((255,69,0)))
        screen.draw.text("Try again?", centery = 530, right = 619, fontsize = 64, align = "center", color = "yellow")
        screen.draw.text("YOU LOSE !", centery = 275, right = 655, fontsize = 75, align = "center", color = "green")
    elif game_state == "Win screen":
        screen.clear()
        music.stop()
        screen.fill ((66, 135, 245))
        screen.draw.filled_rect(button_quit, (186, 19, 27))
        screen.draw.text("Quit", centery = 455, right = 505, fontsize = 64, align = "center", color = "green")
        screen.draw.text("YOU WIN !", centery = 275, right = 595, fontsize = 75, align = "center", color = "white")
    elif game_state == "start":
        screen.clear()
        screen.fill ((186, 19, 27))
        screen.draw.filled_rect(button_start, (255,69,0))
        screen.draw.text("Start", centery = 242, right = 498, fontsize = 64, align = "center", color = "yellow")
        screen.draw.text("Day of the Dead", centery = 100, right = 625, fontsize = 64, align = "center", color = "yellow")
        screen.draw.text("Controls and Rules: \nLeft click to shoot zombies, arrow keys to move character. \n Kill all the zombies on the screen before lives counter is zero.",  centery = 445, right = 828, fontsize = 37, align = "center" , color = "yellow")
       
    
    
    
    
      
   