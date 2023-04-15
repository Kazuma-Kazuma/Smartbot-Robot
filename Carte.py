import random
import tkinter as tk

# Définir la taille de la carte
MAP_WIDTH = 20
MAP_HEIGHT = 20

# Définir les couleurs pour les différents types de terrain
COLORS = {
    "empty": "white",
    "start": "blue",
    "goal": "red",
    "path": "yellow",
    "charge": "green",
    "type1": "purple",
    "type2": "black",
    "type3": "gray",
}

# Générer la carte aléatoire
map_data = []
start_pos = (0, 0)
goal_pos = (0, 0)
charge_pos = (0, 0)
while (abs(start_pos[0] - goal_pos[0]) < 10 or abs(start_pos[1] - goal_pos[1]) < 10 or
       abs(start_pos[0] - goal_pos[0]) > 25 or abs(start_pos[1] - goal_pos[1]) > 25 or
       abs(goal_pos[0] - charge_pos[0]) > 10 or abs(goal_pos[1] - charge_pos[1]) > 10):
    map_data = []
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if random.random() < 0.1:
                tile_type = "empty"
            else:
                tile_type = "empty"
            row.append(tile_type)
        map_data.append(row)

    start_pos = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))
    goal_pos = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))
    charge_pos = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))

    # Ajouter les positions de charge supplémentaires
for i in range(3):
    charge_x = random.randint(0, MAP_WIDTH-1)
    charge_y = random.randint(0, MAP_HEIGHT-1)
    while (abs(charge_x - charge_pos[0]) < 15 and abs(charge_y - charge_pos[1]) < 15) and \
          map_data[charge_y][charge_x] != "empty":
        charge_x = random.randint(0, MAP_WIDTH-1)
        charge_y = random.randint(0, MAP_HEIGHT-1)
    map_data[charge_y][charge_x] = "charge"

     # Ajouter des blocs spéciaux
    for i in range(3):
        x, y = random.randint(1, MAP_WIDTH-3), random.randint(1, MAP_HEIGHT-3)
        for j in range(2):
            if map_data[y+j][x] == "empty" and map_data[y+j][x+1] == "empty":
                map_data[y+j][x] = "type1"
                map_data[y+j][x+1] = "type1"
    
    for i in range(3):
        x, y = random.randint(1, MAP_WIDTH-4), random.randint(2, MAP_HEIGHT-3)
        for j in range(2):
            if map_data[y+j][x] == "empty" and map_data[y+j][x+1] == "empty":
                map_data[y+j][x] = "type2"
                map_data[y+j][x+1] = "type2"

    for i in range(2):
        x, y, z = random.randint(1, MAP_WIDTH-3), random.randint(1, MAP_HEIGHT-3), random.randint(1, MAP_HEIGHT-4)
        for j in range(2):
            if map_data[y+j][x] == "empty" and map_data[y+j][x+1] == "empty" and map_data[z+j][x] == "empty" and map_data[z+j][x+1] == "empty":
                map_data[y+j][x] = "type3"
                map_data[y+j][x+1] = "type3"
                map_data[z+j][x] = "type3"
                map_data[z+j][x+1] = "type3"



# Mettre à jour la carte avec les positions de départ, d'arrivée et de charge
map_data[start_pos[1]][start_pos[0]] = "start"
map_data[goal_pos[1]][goal_pos[0]] = "goal"
map_data[charge_pos[1]][charge_pos[0]] = "charge"


# Créer la fenêtre
root = tk.Tk()
root.title("Carte pour livraison")

# Créer les cases de la carte
tiles = []
for y in range(MAP_HEIGHT):
    row = []
    for x in range(MAP_WIDTH):
        tile_type = map_data[y][x]
        color = COLORS[tile_type]
        tile = tk.Canvas(root, width=20, height=20, bg=color)
        tile.grid(row=y, column=x)
        row.append(tile)
    tiles.append(row)

    # Mettre à jour la fenêtre pour afficher les cases
root.update()

# Afficher la fenêtre
root.mainloop()