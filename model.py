import mesa
import agents
from agents import Carros


class Model(mesa.Model):
    calles = [
        ((0, 10), (21, 10)),
        ((20, 11), (-1, 11)),
        ((10, 20), (10, -1)),
        ((11, 0), (11, 21)),
    ]

    def __init__(self, n_agents_per_iter=2, max_agents=9, road_list=calles, width=21, height=21):
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.n_agents_per_iter = n_agents_per_iter
        self.iter = 0
        self.max_agents = max_agents
        self.contador = 0
        self.n_agents = 0
        self.vehicles = []
        self.luces = []
        self.contador_luces = 0
        self.total_moves = mesa.DataCollector(
            {
                "Total moves": self.get_total_moves,
            }
        )

        self.total_luces = mesa.DataCollector(
            {
                "Total luces moves": self.get_luces,
            }
        )

        self.total_carros = mesa.DataCollector(
            {
                "Total de carros": self.count_carros,
            }
        )
        self.total_moves.collect(self)
        self.total_luces.collect(self)
        self.total_carros.collect(self)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total moves": self.get_total_moves,
                "Total luces moves": self.get_luces,
                "Total carros": self.count_carros,

            },
            agent_reporters={
                "Cells cleaned": "cells_cleaned",
                "Moves": "moves",
            },
        )
        for x in range(width):
            for y in range(height):
                edificio = agents.Edificio(x, y)
                self.grid.place_agent(edificio, (x, y))
        for road in road_list:
            start, end = road
            X = end[0] - start[0]
            Y = end[1] - start[1]
            goes = ''
            cond = None
            if not X == 0:
                if X > 0:
                    goes = 'D'
                    cond = 0
                else:
                    goes = 'I'
                    cond = 1
            elif not Y == 0:
                if Y > 0:
                    goes = 'O'
                    cond = 0
                else:
                    goes = 'F'
                    cond = 1
            x = start[0]
            y = start[1]
            while x != end[0]:
                cell = self.grid.get_cell_list_contents((x, y), True)
                if any(isinstance(elem, agents.Edificio) for elem in cell):
                    self.grid.remove_agent(cell[0])
                if any(isinstance(elem, agents.Calle) for elem in cell):
                    cell[0].dir.append(goes)
                else:
                    r = agents.Calle(0, self)
                    r.dir.append(goes)
                    self.grid.place_agent(r, (x, y))
                if cond == 0:
                    x += 1
                else:
                    x -= 1
            while y != end[1]:
                cell = self.grid.get_cell_list_contents((x, y), True)
                if any(isinstance(elem, agents.Edificio) for elem in cell):
                    self.grid.remove_agent(cell[0])
                if any(isinstance(elem, agents.Calle) for elem in cell):
                    cell[0].dir.append(goes)
                else:
                    r = agents.Calle(1, self)
                    r.dir.append(goes)
                    self.grid.place_agent(r, (x, y))
                if cond == 0:
                    y += 1
                else:
                    y -= 1
        self.traff = (9, 10)
        self.grid.get_cell_list_contents((11, 20), True)[0].dir[0] = 'I'
        self.grid.get_cell_list_contents((10, 0), True)[0].dir[0] = 'D'
        self.grid.get_cell_list_contents((19, 10), True)[0].dir[0] = 'O'
        self.grid.get_cell_list_contents((0, 11), True)[0].dir[0] = 'F'
        self.semaforo = agents.Semaforo(0, self, self.traff, True)
        self.grid.place_agent(self.semaforo, self.traff)
        self.traff2 = (11, 10)
        self.semaforo2 = agents.Semaforo(1, self, self.traff2, False)
        self.grid.place_agent(self.semaforo2, self.traff2)
        self.semaforo.luces.append(self.semaforo2)
        self.semaforo2.luces.append(self.semaforo)
        self.luces.append(self.semaforo)
        self.luces.append(self.semaforo2)
        self.running = True

    def rand_vehicles(self):
        pos = [(0, 10), (11, 0)]
        if self.iter == 5:
            for i in range(self.n_agents_per_iter):
                if self.n_agents == self.max_agents:
                    continue
                else:
                    cell = self.grid.get_cell_list_contents(pos[i], True)
                    if not any(isinstance(elem, agents.Carros) for elem in cell):
                        self.vehicle = agents.Carros(i, self, pos[i])
                        self.grid.place_agent(self.vehicle, pos[i])
                        self.vehicles.append(self.vehicle)
                        self.n_agents += 1
            self.iter = 0
        else:
            self.iter += 1

    def get_total_moves(self):
        return self.contador

    def get_luces(self):
        return self.contador_luces

    def step(self):
        self.rand_vehicles()
        ps = []
        self.contador = self.contador + 1

        for vehicle in self.vehicles:
            vehicle.move()
            xy = vehicle.pos
            p = [xy[0], xy[1], 0]
            ps.append(p)
        for light in self.luces:
            light.check()
            self.contador_luces += 1
        self.schedule.step()
        self.total_moves.collect(self)
        self.total_luces.collect(self)
        self.total_carros.collect(self)
        return ps



    def run_model(self, n):
        for i in range(n):
            self.step()

    def count_carros(self):
        # Cuenta el número de celdas boxe
        carros = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Carros) for agent in cell_content):
                carros += 1
        return carros
