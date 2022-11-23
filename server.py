from agents import Edificio, Semaforo, Calle, Carros
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Model
import mesa


def agent_portrayal(agent):
    portrayal = {}
    if type(agent) is Edificio:
        portrayal = {
            "Color": "green",
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1,
        }
    if type(agent) is Semaforo:
        if agent.horiz == True:
            w, h = .25, .5
            color = 'green'
        else:
            w, h = .5, .25
            color = 'red'
        if agent.current_cycle == 1:
            color = 'green'
        else:
            color = 'red'
        portrayal = {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "Layer": 3,
            "w": w,
            "h": h,
        }
    if type(agent) is Calle:
        portrayal = {
            "Shape": "rect",
            "Color": 'gray',
            "Filled": "true",
            "Layer": 1,
            "w": 1,
            "h": 1,
        }
    if type(agent) is Carros:
        portrayal = {
            "Shape": "circle",
            "Color": 'orange',
            "Filled": "true",
            "Layer": 2,
            "r": 0.5
        }
    return portrayal


chart = mesa.visualization.ChartModule(
    [{"Label": "Total moves", "Color": "blue" }], data_collector_name="total_moves"
)

chart2 = mesa.visualization.ChartModule(
    [{"Label": "Total luces moves", "Color": "Green"}],
    data_collector_name="total_luces",
    canvas_height=60,
    canvas_width=80,
)
chart3 = mesa.visualization.ChartModule(
    [{"Label": "Total de carros", "Color": "Red"}],
    data_collector_name="total_carros",
    canvas_height=60,
    canvas_width=80,
)


width, height = 20, 20
width += 1
height += 1

grid = CanvasGrid(agent_portrayal, width, height, 600, 600)
server = mesa.visualization.ModularServer(Model, [grid, chart, chart2, chart3], "Semaforos inteligentes",
    {
    'n_agents_per_iter': 2,
    'width': width,
    'height': height
}
)
server.port = 6996
server.launch()
