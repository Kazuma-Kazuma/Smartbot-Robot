import random
import tkinter as tk
from queue import PriorityQueue

class Carte:
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

    # Définir les coûts initiaux pour tous les sommets
    start_cost = {start_pos: 0}
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if (x, y) != start_pos:
                start_cost[(x, y)] = float("inf")

    # Initialiser la file de priorité avec le sommet de départ
    pq = PriorityQueue()
    pq.put((0, start_pos))

    # Initialiser les parents pour tous les sommets
    parents = {}

    # Exécuter l'algorithme de Dijkstra
    Batterie = 100
    while not pq.empty():
        current_cost, current_pos = pq.get()

        # Si nous atteignons le point d'arrivée, arrêter l'algorithme
        if current_pos == goal_pos:
            break

        # Parcourir tous les voisins du sommet courant
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_pos = (current_pos[0]+dx, current_pos[1]+dy)
            if next_pos[0] < 0 or next_pos[0] >= MAP_WIDTH or next_pos[1] < 0 or next_pos[1] >= MAP_HEIGHT:
                # Ignorer les sommets qui sortent de la carte
                continue
            next_cost = current_cost + 1
            if map_data[next_pos[1]][next_pos[0]] != "empty" and map_data[next_pos[1]][next_pos[0]] != "goal" and map_data[next_pos[1]][next_pos[0]] != "charge":
                # Ignorer les sommets qui ne sont pas "vides"
                continue
            if next_cost < start_cost[next_pos]:
                # Mettre à jour le coût et le parent du sommet suivant
                start_cost[next_pos] = next_cost
                parents[next_pos] = current_pos
                pq.put((next_cost, next_pos))
    Batterie -= next_cost
    print (Batterie)

    # Reconstituer le chemin le plus court en partant du point d'arrivée
    path = [goal_pos]
    while path[-1] != start_pos:
        path.append(parents[path[-1]])
    path.reverse()
    del(path[0])
    del(path[-1])

    # Créer la fenêtre
    root = tk.Tk()
    root.title("Carte pour livraison")

    # Créer les cases de la carte
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_type = map_data[y][x]
            color = COLORS[tile_type]
            tile = tk.Canvas(root, width=20, height=20, bg=color)
            tile.grid(row=y, column=x)
    
    # Mettre en surbrillance le chemin sur la carte
    for pos in path:
        tile = tk.Canvas(root, width=20, height=20, bg="yellow")
        tile.grid(row=pos[1], column=pos[0])

    # Mettre à jour la fenêtre pour afficher les cases
    root.update()

    # Afficher la fenêtre
    root.mainloop()

    # Créer la fenêtre
    root2 = tk.Tk()
    root2.title("Deuxième carte pour livraison")

    goal_pos2 = (0, 0)
    goal_pos2 = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))
    while(map_data[goal_pos2[1]][goal_pos2[0]] != "empty"):
        goal_pos2 = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))   
    
    map_data[goal_pos2[1]][goal_pos2[0]] = "goal"

    # Créer les cases de la carte
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_type = map_data[y][x]
            color = COLORS[tile_type]
            tile = tk.Canvas(root2, width=20, height=20, bg=color)
            tile.grid(row=y, column=x)

    tile = tk.Canvas(root2, width=20, height=20, bg="white")
    tile.grid(row=start_pos[1], column=start_pos[0])
    tile = tk.Canvas(root2, width=20, height=20, bg="blue")
    tile.grid(row=goal_pos[1], column=goal_pos[0])
    tile = tk.Canvas(root2, width=20, height=20, bg="red")
    tile.grid(row=goal_pos2[1], column=goal_pos2[0])

    pq.put((0, goal_pos))

    while not pq.empty():
        current_cost, current_pos = pq.get()

        # Si nous atteignons le point d'arrivée, arrêter l'algorithme
        if current_pos == goal_pos2:
            break

        # Parcourir tous les voisins du sommet courant
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_pos = (current_pos[0]+dx, current_pos[1]+dy)
            if next_pos[0] < 0 or next_pos[0] >= MAP_WIDTH or next_pos[1] < 0 or next_pos[1] >= MAP_HEIGHT:
                # Ignorer les sommets qui sortent de la carte
                continue
            next_cost = current_cost + 1
            if map_data[next_pos[1]][next_pos[0]] != "empty" and map_data[next_pos[1]][next_pos[0]] != "goal" \
            and map_data[next_pos[1]][next_pos[0]] != "charge" and map_data[next_pos[1]][next_pos[0]] != "start":
                # Ignorer les sommets qui ne sont pas "vides"
                continue
            if next_cost < start_cost[next_pos]:
                # Mettre à jour le coût et le parent du sommet suivant
                start_cost[next_pos] = next_cost
                parents[next_pos] = current_pos
                pq.put((next_cost, next_pos))
    Batterie -= next_cost
    print (Batterie)

    # Reconstituer le chemin le plus court en partant du point d'arrivée
    path = [goal_pos2]
    while path[-1] != goal_pos:
        path.append(parents[path[-1]])
    path.reverse()
    del(path[0])
    del(path[-1])

    # Mettre en surbrillance le chemin sur la carte
    for pos in path:
        tile = tk.Canvas(root2, width=20, height=20, bg="yellow")
        tile.grid(row=pos[1], column=pos[0])

    # Mettre à jour la fenêtre pour afficher les cases
    root2.update()

    # Afficher la fenêtre
    root2.mainloop()
    # Créer la fenêtre
    root3 = tk.Tk()
    root3.title("Derniere carte pour livraison")

    goal_pos3 = (0, 0)
    goal_pos3 = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))
    while(map_data[goal_pos3[1]][goal_pos3[0]] != "empty"):
        goal_pos3 = (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))   
    
    map_data[goal_pos3[1]][goal_pos3[0]] = "goal"

    # Créer les cases de la carte
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_type = map_data[y][x]
            color = COLORS[tile_type]
            tile = tk.Canvas(root3, width=20, height=20, bg=color)
            tile.grid(row=y, column=x)

    tile = tk.Canvas(root3, width=20, height=20, bg="white")
    tile.grid(row=start_pos[1], column=start_pos[0])
    tile = tk.Canvas(root3, width=20, height=20, bg="white")
    tile.grid(row=goal_pos[1], column=goal_pos[0])
    tile = tk.Canvas(root3, width=20, height=20, bg="blue")
    tile.grid(row=goal_pos2[1], column=goal_pos2[0])
    tile = tk.Canvas(root3, width=20, height=20, bg="red")
    tile.grid(row=goal_pos3[1], column=goal_pos3[0])


    if Batterie > 60:
        pq.put((0, goal_pos2))

        while not pq.empty():
            current_cost, current_pos = pq.get()

            # Si nous atteignons le point d'arrivée, arrêter l'algorithme
            if current_pos == goal_pos3:
                break

            # Parcourir tous les voisins du sommet courant
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (current_pos[0]+dx, current_pos[1]+dy)
                if next_pos[0] < 0 or next_pos[0] >= MAP_WIDTH or next_pos[1] < 0 or next_pos[1] >= MAP_HEIGHT:
                    # Ignorer les sommets qui sortent de la carte
                    continue
                next_cost = current_cost + 1
                if map_data[next_pos[1]][next_pos[0]] != "empty" and map_data[next_pos[1]][next_pos[0]] != "goal" \
                and map_data[next_pos[1]][next_pos[0]] != "charge" and map_data[next_pos[1]][next_pos[0]] != "start":
                    # Ignorer les sommets qui ne sont pas "vides"
                    continue
                if next_cost < start_cost[next_pos]:
                    # Mettre à jour le coût et le parent du sommet suivant
                    start_cost[next_pos] = next_cost
                    parents[next_pos] = current_pos
                    pq.put((next_cost, next_pos))
        Batterie -= next_cost
        print (Batterie)

        # Reconstituer le chemin le plus court en partant du point d'arrivée
        path = [goal_pos3]
        while path[-1] != goal_pos2:
            path.append(parents[path[-1]])
        path.reverse()
        del(path[0])
        del(path[-1])

        # Mettre en surbrillance le chemin sur la carte
        for pos in path:
            tile = tk.Canvas(root3, width=20, height=20, bg="yellow")
            tile.grid(row=pos[1], column=pos[0])

        # Mettre à jour la fenêtre pour afficher les cases
        root3.update()

        # Afficher la fenêtre
        root3.mainloop()
    else:
        pq.put((0, goal_pos2))

        while not pq.empty():
            current_cost, current_pos = pq.get()

            # Si nous atteignons le point d'arrivée, arrêter l'algorithme
            if current_pos == charge_pos:
                break

            # Parcourir tous les voisins du sommet courant
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (current_pos[0]+dx, current_pos[1]+dy)
                if next_pos[0] < 0 or next_pos[0] >= MAP_WIDTH or next_pos[1] < 0 or next_pos[1] >= MAP_HEIGHT:
                    # Ignorer les sommets qui sortent de la carte
                    continue
                next_cost = current_cost + 1
                if map_data[next_pos[1]][next_pos[0]] != "empty" and map_data[next_pos[1]][next_pos[0]] != "goal" \
                and map_data[next_pos[1]][next_pos[0]] != "charge" and map_data[next_pos[1]][next_pos[0]] != "start":
                    # Ignorer les sommets qui ne sont pas "vides"
                    continue
                if next_cost < start_cost[next_pos]:
                    # Mettre à jour le coût et le parent du sommet suivant
                    start_cost[next_pos] = next_cost
                    parents[next_pos] = current_pos
                    pq.put((next_cost, next_pos))
        Batterie -= next_cost
        print (Batterie)

        # Reconstituer le chemin le plus court en partant du point d'arrivée
        path = [charge_pos]
        while path[-1] != goal_pos2:
            path.append(parents[path[-1]])
        path.reverse()
        del(path[0])
        del(path[-1])
        Batterie=100
        print("Batterie rechargée")
        # Mettre en surbrillance le chemin sur la carte
        for pos in path:
            tile = tk.Canvas(root3, width=20, height=20, bg="yellow")
            tile.grid(row=pos[1], column=pos[0])

        # Mettre à jour la fenêtre pour afficher les cases
        root3.update()

        # Afficher la fenêtre
        root3.mainloop()

        root4 = tk.Tk()
        root4.title("Derniere carte pour livraison")

        # Créer les cases de la carte
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile_type = map_data[y][x]
                color = COLORS[tile_type]
                tile = tk.Canvas(root4, width=20, height=20, bg=color)
                tile.grid(row=y, column=x)

        tile = tk.Canvas(root4, width=20, height=20, bg="white")
        tile.grid(row=start_pos[1], column=start_pos[0])
        tile = tk.Canvas(root4, width=20, height=20, bg="white")
        tile.grid(row=goal_pos[1], column=goal_pos[0])
        tile = tk.Canvas(root4, width=20, height=20, bg="blue")
        tile.grid(row=goal_pos2[1], column=goal_pos2[0])
        tile = tk.Canvas(root4, width=20, height=20, bg="red")
        tile.grid(row=goal_pos3[1], column=goal_pos3[0])

        pq.put((0, charge_pos))

        while not pq.empty():
            current_cost, current_pos = pq.get()

            # Si nous atteignons le point d'arrivée, arrêter l'algorithme
            if current_pos == goal_pos3:
                break

            # Parcourir tous les voisins du sommet courant
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (current_pos[0]+dx, current_pos[1]+dy)
                if next_pos[0] < 0 or next_pos[0] >= MAP_WIDTH or next_pos[1] < 0 or next_pos[1] >= MAP_HEIGHT:
                    # Ignorer les sommets qui sortent de la carte
                    continue
                next_cost = current_cost + 1
                if map_data[next_pos[1]][next_pos[0]] != "empty" and map_data[next_pos[1]][next_pos[0]] != "goal" \
                and map_data[next_pos[1]][next_pos[0]] != "charge" and map_data[next_pos[1]][next_pos[0]] != "start":
                    # Ignorer les sommets qui ne sont pas "vides"
                    continue
                if next_cost < start_cost[next_pos]:
                    # Mettre à jour le coût et le parent du sommet suivant
                    start_cost[next_pos] = next_cost
                    parents[next_pos] = current_pos
                    pq.put((next_cost, next_pos))
        Batterie -= next_cost
        print (Batterie)

        # Reconstituer le chemin le plus court en partant du point d'arrivée
        path = [goal_pos3]
        while path[-1] != charge_pos:
            path.append(parents[path[-1]])
        path.reverse()
        del(path[0])
        del(path[-1])
        Batterie=100
        print("Batterie rechargée")
        print(Batterie)
        # Mettre en surbrillance le chemin sur la carte
        for pos in path:
            tile = tk.Canvas(root4, width=20, height=20, bg="yellow")
            tile.grid(row=pos[1], column=pos[0])

        # Mettre à jour la fenêtre pour afficher les cases
        root3.update()

        # Afficher la fenêtre
        root3.mainloop()


            

