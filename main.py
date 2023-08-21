import pygame
import math

pygame.init()


temp_node = None

def IsKeyClose() -> bool:
    result = False
    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  
                result = not result
    return result
 
                
def circle_to_point_coll(circle_pos, radius, point):
    dx = point[0] - circle_pos[0]
    dy = point[1] - circle_pos[1]
    dist = math.sqrt(dx * dx + dy *dy)
    return dist <= radius

class Edge:
    def __init__(self, from_node, to_node) -> None:
        self.from_node = from_node
        self.to_node = to_node
        self.hasElectric = False
        from_node.edges.add(self)
        to_node.edges.add(self)
        
    
    def __eq__(self, other: object) -> bool:
        return other.from_node.id == self.from_node.id and other.to_node.id == self.to_node.id

    def __hash__(self) -> int:
        return hash((self.from_node.id, self.to_node.id))
    

class Node:
    counter = 0
    def __init__(self, parent, x = 0, y = 0, radius = 8, border = 1) -> None:
        Node.counter += 1
        self.id = Node.counter
        self.edges = set()
        self.radius = radius
        self.border = border
        self.x = x
        self.y = y
        self.parent = parent
    
    def get_pos(self):
        return (self.parent.rect.topleft[0] + self.x, self.parent.rect.topleft[1] + self.y)
    
class Prop:
    def __init__(self, img, x, y, w, h, nodes) -> None:
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.rect = self.img.get_rect(topleft=(x,y))
        self.nodes = nodes
    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)
    
    def draw_nodes_and_edges(self, screen):
        for node in self.nodes:
            pygame.draw.circle(screen, (0,0,0), node.get_pos(), node.radius, node.border)
            for edge in node.edges:
                if edge.hasElectric:
                    pygame.draw.line(screen, (242,218,9), edge.from_node.get_pos(), edge.to_node.get_pos())
                else:
                    pygame.draw.line(screen, (0,0,0), edge.from_node.get_pos(), edge.to_node.get_pos())

    def movingObjects(self, event):
        global moving_object, moving_offset

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                moving_object = self
                moving_offset = (event.pos[0] - self.rect.topleft[0], event.pos[1] - self.rect.topleft[1])
    
        if event.type == pygame.MOUSEBUTTONUP:
            moving_object = None

        if event.type == pygame.MOUSEMOTION:
            if moving_object is not None:
                moving_object.rect.topleft = (event.pos[0] - moving_offset[0], event.pos[1] - moving_offset[1])

    def foundCableNodes(self, event): 
        global temp_node
        if event.type == pygame.MOUSEBUTTONDOWN:
            for node in self.nodes:
                if circle_to_point_coll(node.get_pos(), node.radius, event.pos):
                    if(temp_node != None):
                        if temp_node != node:
                            Edge(temp_node, node)
                        temp_node = None
                    else:
                        temp_node = node
                    break
           
class Lamp(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("lightbulb.png", x, y, 50, 50, [Node(self, -2, 43), Node(self, 52, 43)])

    def update(self):
        counter = 0
        for node in self.nodes:
            for edge in node.edges:
                if edge.hasElectric:
                    counter = counter + 1
                    if counter == 2:
                        print("lamba yanıyo")
                        self.img = pygame.image.load("lamp.png")
                        self.img = pygame.transform.scale(self.img, (50, 50))
                        self.rect = self.img.get_rect(topleft=self.rect.topleft)
                        super().draw(screen)
                    else:
                        self.img = pygame.image.load("lightbulb.png")
                        self.img = pygame.transform.scale(self.img, (50, 50))
                        self.rect = self.img.get_rect(topleft=self.rect.topleft)
                        super().draw(screen)

        counter = 0    

class Battery(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("battery.png", x, y, 50, 50, [Node(self, -4, 25), Node(self, 54, 25)])

    def update(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.hasElectric = True

class Key(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("key.png", x, y, 100, 50, [Node(self, -6, 30), Node(self, 107, 30)])
        self.open = False
        self.prev_key_state = False  # Yeni bir değişken ekleyin

    def update(self):
        key_state = IsKeyClose()
        
        if key_state != self.prev_key_state:
            self.prev_key_state = key_state
            if key_state:
                self.open = not self.open

        for node in self.nodes:
            for edge in node.edges:
                edge.hasElectric = self.open
                        
                    
                
# Screen init
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Circuit Creator")
icon = pygame.image.load('electrical-circuit.png')
pygame.display.set_icon(icon)

props = [Key (200, 50),Lamp(30, 50), Battery(100, 50) ]

edges = []

# Main loop
running = True
moving_object = None  
moving_offset = (0, 0)  
drawing_cable = False
start_cable_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for prop in props:
            prop.movingObjects(event)
            prop.foundCableNodes(event)
            
           
    
    screen.fill((255, 255, 255))

    for prop in props:
        prop.update()
        prop.draw(screen)
        prop.draw_nodes_and_edges(screen)
        

    if temp_node != None:
        pygame.draw.line(screen, (0,0,0), temp_node.get_pos(), pygame.mouse.get_pos())
    pygame.display.flip()

pygame.quit()