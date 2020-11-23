############################################
# Infection Spread Simulator - Ryan Knight #
############################################

###########################################
# This is the second version.             #
# Non-sandboxing limits processing strain #
###########################################

#Imports
import pygame #python -m pip install -U pygame --user
import tkinter as tk
from tkinter import *
import os
import random
import platform
from numpy.random import choice

#Internal and reference values(%)
start = False
change_allowed = True
new_start = False
outbreaks = 0
measles_spread_chance = 90
measles_vaccine_effectiveness = 97
measles_incubation = 1000
measles_contagious = 800

population_cap = 500
collide_timer = 7
black, white, red  = pygame.Color(0,0,0), pygame.Color(255,255,255), pygame.Color(255,0,0)
green, blue, orange = pygame.Color(0,255,0), pygame.Color(0,255,255), pygame.Color(255,165,0)
yellow = pygame.Color(255,255,0)
WIDTH = 650
HEIGHT = 650
UNIT_SIZE = 10
title = "Infection Spread Simulator (Ryan Knight) "
Delay_checkbox_value, Incubation_checkbox_value = 0,0

#Initialise
root = tk.Tk()
embed = tk.Frame(root, width = WIDTH, height = HEIGHT) #Pygame window embed frame
root.title(title+"(Idle)")
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #Simulation window oriented left
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
#    os.environ['SDL_VIDEODRIVER'] = 'dummy' #"Cross Platform" (untested) UNIX may need 'dummy' driver to work.
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #Pygame window inside embed frame
screen.fill(pygame.Color(255,255,255))
pygame.display.init()
pygame.display.update()

#Tkinter Functions
def ResetSliders():
    global Incubation_checkbox_value, Delay_checkbox_value, measles_incubation, measles_contagious
    Transmission_scale.set(measles_spread_chance)
    Immunity_scale.set(measles_vaccine_effectiveness)
    if Incubation_checkbox_value == 0:
        Incubation_checkbox.select()
        IncubationEnable()
    Incubation_scale.set(measles_contagious)
    if Delay_checkbox_value == 0:
        Delay_checkbox.select()
        DelayEnable()
    Contagious_scale.set(measles_incubation)
def PatientZero():
    make_unit("infected")
def DelayEnable():
    global Delay_checkbox_value
    #Enabling checkbox
    if Delay_checkbox_value == 0:
        Delay_checkbox_value = 1
        Contagious_scale.config(state = "normal")
    #Disabling checkbox
    else:
        Delay_checkbox_value = 0
        Contagious_scale.set(0)
        Contagious_scale.config(state = DISABLED)
def IncubationEnable():
    global Incubation_checkbox_value
    if Incubation_checkbox_value == 0:
        Incubation_checkbox_value = 1
        Incubation_scale.config(state = "normal")
    else:
        Incubation_checkbox_value = 0
        Incubation_scale.set(0)
        Incubation_scale.config(state = DISABLED)
def StartStop():
    global start, change_allowed, root, unit_list, outbreaks, title, new_start, Incubation_checkbox_value, Delay_checkbox_value
    #When simulation is running:
    if change_allowed == True:
        new_start = True
        Transmission_scale.config(state = DISABLED)
        Cluster_scale.config(state=DISABLED)
        Immunity_scale.config(state = DISABLED)
        Vaccine_scale.config(state = DISABLED)
        Population_scale.config(state = DISABLED)
        Contagious_scale.config(state = DISABLED)
        Incubation_scale.config(state = DISABLED)
        Infection_button.config(state = "normal")
        Measles_button.config(state = DISABLED)
        Delay_checkbox.config(state = DISABLED)
        Incubation_checkbox.config(state = DISABLED)
        Endemic_label.config(text="")
        start = True
        change_allowed = False
        root.title(title+"(Running)")
    #When simulation is stopped:
    elif change_allowed == False:
        Cluster_scale.config(state="normal")
        Transmission_scale.config(state = "normal")
        Immunity_scale.config(state = "normal")
        Vaccine_scale.config(state = "normal")
        Population_scale.config(state = "normal")
        Infection_button.config(state = DISABLED)
        Measles_button.config(state = "normal")
        Delay_checkbox.config(state = "normal")
        Incubation_checkbox.config(state = "normal")
        if Incubation_checkbox_value == 1:
            Incubation_scale.config(state = "normal")
        if Delay_checkbox_value == 1:
            Contagious_scale.config(state = "normal")
        unit_list = []
        outbreaks = 0
        start = False
        change_allowed = True
        root.title(title+"(Idle)")
        
#Tkinter scale objects
#Main
Transmission_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL,resolution=0.1,label="Transmission Probability (%)",length=250)
Transmission_scale.set(measles_spread_chance)
Transmission_scale.pack()
Immunity_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL,resolution=0.1,label="Vaccine Effectiveness (%)",length=250)
Immunity_scale.set(measles_vaccine_effectiveness)
Immunity_scale.pack()
Vaccine_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL,resolution=0.1,label="Vaccination Rate (%)",length=250)
Vaccine_scale.set(50)
Vaccine_scale.pack()
Population_scale = Scale(root, from_=0, to=population_cap, orient=HORIZONTAL,resolution=1,label="Population Density",length=250)
Population_scale.set(0)
Population_scale.pack()

#Optional additions
Delay_checkbox = Checkbutton(root, text="Enable contagious period",command=DelayEnable)
Delay_checkbox.pack()
Contagious_scale = Scale(root, from_=100, to=2000, orient=HORIZONTAL,resolution=100,label="Contagious period (Ticks)",length=250,state=DISABLED)
Contagious_scale.set(0)
Contagious_scale.pack()
Incubation_checkbox = Checkbutton(root, text="Enable incubation period",command=IncubationEnable)
Incubation_checkbox.pack()
Incubation_scale = Scale(root, from_=100, to=2000, orient=HORIZONTAL,resolution=100,label="Incubation period (Ticks)",length=250,state=DISABLED)
Incubation_scale.set(0)
Incubation_scale.pack()
Cluster_scale = Scale(root, from_=0, to=1, orient=HORIZONTAL,resolution=0.01,label="Clustering Parameter",length=250)
Cluster_scale.set(0)
Cluster_scale.pack()

#Tkinter choice objects/ Other
Measles_button = Button(root,text="Measles Values", command=ResetSliders,width=34)
Measles_button.pack()
Infection_button = Button(root,text="Add Patient Zero", command=PatientZero,width=34,state=DISABLED)
Infection_button.pack()
Reset_button = Button(root,text="Start / Reset", command=StartStop,width=34)
Reset_button.pack()

Tick_label = Label(root,text=("Tick: 0"), font=("Helvetica", 12))
Tick_label.pack()
Endemic_label = Label(root,text=(""),font=("Helvetica",10))
Endemic_label.pack()
Outbreak_label = Label(root,text=(""),font=("Helvetica",10))
Outbreak_label.pack()

##canvas = Canvas(root, width = 170, height = 176) 
##img = PhotoImage(file="Key.ppm")      
##canvas.create_image(image=img)
##canvas.pack()

#Pygame Operating Class / Functions
class Unit(pygame.sprite.Sprite):
    def __init__(self,spawn_type):
        global outbreaks, cluster_hub, Cluster_level
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.change_x = random.randrange(-2, 2) 
        self.change_y = random.randrange(-2, 2)
        self.collide_delay = 0
        self.infectious_time = 0
        self.incubation_time = 0
        self.clustered = False
        
        #Vaccination status generation/Clustering
               
        if spawn_type == "healthy":
            vaccination_rate = Vaccine_scale.get()/100
            if choice([0, 1], p=[(1-vaccination_rate),vaccination_rate]) == 0:
                #Unvaccinated
                self.status = 0
                if choice([0, 1], p=[(1-Cluster_level),Cluster_level]) == 1:
                    self.clustered = True
            else:
                #Vaccinated
                self.status = 1
        else:
            #Transmissible Infected
            outbreaks = outbreaks + 1
            self.status = 2

            
        #Unvaccinated Clustering movement set #(400-300*Cluster_level)
        if self.clustered == True:
            self.x = random.randrange(int(round(cluster_hub[0]-(400-300*Cluster_level))),int(round(cluster_hub[0]+(400-300*Cluster_level))))
            self.y = random.randrange(int(round(cluster_hub[1]-(400-300*Cluster_level))),int(round(cluster_hub[1]+(400-300*Cluster_level))))
            self.spawnx = self.x
            self.spawny = self.y
        else: #Standard movement set
            self.x = random.randrange(UNIT_SIZE, WIDTH - UNIT_SIZE) 
            self.y = random.randrange(UNIT_SIZE, HEIGHT - UNIT_SIZE) #gephi
            self.spawnx = self.x
            self.spawny = self.y

    #Sets a unit's colour. Called when updating the screen.
    def AssignColour(self):
        if self.status == 0: #Unvaccinated
            self.image.fill(green)
        elif self.status == 1: #Vaccinated
            self.image.fill(blue)
        elif self.status == 2: #Infected (Contagious)
            self.image.fill(red)
        elif self.status == 3: #Infected (Incubating)
            self.image.fill(yellow)
        elif self.status == 4: #Infected (Non-Contagious)
            self.image.fill(orange)
        
 
def make_unit(spawn_type):
    unit = Unit(spawn_type)
    unit_list.append(unit)
    unit.AssignColour()
    return unit


def main():
    global unit_list, outbreaks, start, new_start, Delay_checkbox_value, Incubation_checkbox_value, Cluster_level, cluster_hub
    tick_counter = 0
    unit_list = []
    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                done = True

        if start == True:
            #(Stop/Start restrictions, allows limiting heavy resource steps to once per run.)
            #Once/Restart running loop:
            if new_start == True:
                counterlock = False

                Cluster_level = Cluster_scale.get()
                if Cluster_level != 0:
                    cluster_hub = [random.randint(100, WIDTH-100),random.randint(100, HEIGHT-100)]
                
                Population = Population_scale.get()
                for x in range(Population):
                    make_unit("healthy")
                
                #Get slider values
                Transmission_rate = Transmission_scale.get()/100
                Vaccine_work_rate = Immunity_scale.get()/100
                Contagious_time = Contagious_scale.get()
                Incubation_time = Incubation_scale.get()

                tick_counter = 0
                new_start = False

            #Once/tick running loop: 
            #Unit movement and collision
            for unit in unit_list:
                unit.x = unit.x + unit.change_x 
                unit.y = unit.y + unit.change_y

                #Collision recognition
                if unit.collide_delay == 0:
                    UnitsCollided = pygame.sprite.spritecollide(unit, unit_list, False)
                    for item in UnitsCollided:
                        if item != unit:
                            if unit.status == 2 or item.status == 2:
                                if unit.status == 0 or item.status == 0:
                                    if choice([0, 1], p=[(1-Transmission_rate),Transmission_rate]) == 1:
                                        if Incubation_checkbox_value == 0:
                                            unit.status = 2
                                            item.status = 2
                                        else:
                                            if unit.status != 2:
                                                unit.status = 3
                                            else:
                                                item.status = 3
                                elif unit.status == 1 or item.status == 1:
                                    if choice([0, 1], p=[(1-Vaccine_work_rate),Vaccine_work_rate]) == 0:
                                        if Incubation_checkbox_value == 0:
                                            unit.status = 2
                                            item.status = 2
                                        else:
                                            if unit.status != 2:
                                                unit.status = 3
                                            else:
                                                item.status = 3
            
                            #print("collision")
                            item.collide_delay = collide_timer
                            unit.collide_delay = collide_timer
                else:
                    unit.collide_delay = unit.collide_delay - 1

                #Wall bounce
                rebound_x,rebound_y = False, False
                if unit.y > HEIGHT - UNIT_SIZE or unit.y < UNIT_SIZE: #if collide with roof/floor flip direction
                    unit.change_y *= -1
                    rebound_y = True
                if unit.x > WIDTH - UNIT_SIZE or unit.x < UNIT_SIZE: #if collide with sides flip direction
                    unit.change_x *= -1
                    rebound_x = True

                if unit.clustered == True:
                    if (unit.x < cluster_hub[0]-(400-300*Cluster_level) or unit.x > cluster_hub[0]+(400-300*Cluster_level)) and rebound_x == False:
                        unit.change_x *= -1
                    if (unit.y < cluster_hub[1]-(400-300*Cluster_level) or unit.y > cluster_hub[1]+(400-300*Cluster_level)) and rebound_y == False:
                        unit.change_y *= -1
                unit.rect.topleft = unit.x, unit.y

            #Contagious to non-contagious countdown
            if Delay_checkbox_value == 1:
                for unit in unit_list:
                    if unit.status == 2:
                        unit.infectious_time = unit.infectious_time + 1
                        if unit.infectious_time >= Contagious_time:
                            unit.status = 4
            #Incubation to contagious countdown
            if Incubation_checkbox_value == 1:
                for unit in unit_list:
                    if unit.status == 3:
                        unit.incubation_time = unit.incubation_time + 1
                        if unit.incubation_time >= Incubation_time:
                            unit.status = 2

            #Tick counter goes up after patient zero added.
            if outbreaks > 0:
                tick_counter = tick_counter + 1
                Outbreak_label.config(text=("Outbreaks: "+ str(outbreaks)))
            if counterlock == False:
                infected = 0
                for unit in unit_list:
                    if unit.status == 2 or unit.status == 3 or unit.status == 4:
                        infected = infected + 1
                if infected+outbreaks > (Population+outbreaks)/2:
                    Endemic_label.config(text=("Epidemic after tick: "+ str(tick_counter)))
                    counterlock = True
                  
        #Screen rendering
        screen.fill(white)
        for unit in unit_list:
            unit.AssignColour()
            screen.blit(unit.image,[unit.x, unit.y])

        clock.tick(60)
        pygame.display.flip()            
        Tick_label.config(text=("Tick: "+ str(tick_counter)))
        pygame.display.update()
        root.update()  


                                                   
if __name__ == "__main__":
    main()
