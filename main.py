import pygame

pygame.init()

class Edge:
    def __init__(self, fromNode, toNode) -> None:
        self.fromNode = fromNode
        self.toNode = toNode
    
    def __eq__(self, other: object) -> bool:
        return other.fromNode.id == self.fromNode.id and other.toNode.id == self.toNode.id

    def __hash__(self) -> int:
        return hash((self.fromNode.id, self.toNode.id))

class Node:
    counter = 0
    def __init__(self, x = 0, y = 0, radius = 8, border = 1) -> None:
        Node.counter += 1
        self.id = Node.counter
        self.edges = []
        self.radius = radius
        self.border = border
        self.x = x
        self.y = y

class Prop:
    def __init__(self, img, x, y, w, h, nodes) -> None:
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.rect = self.img.get_rect(topleft=(x,y))
        self.nodes = nodes
    
    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)
    
    def drawNodes(self, screen):
        for node in self.nodes:
            pygame.draw.circle(screen, (0,0,0), (self.rect.topleft[0]+ node.x,self.rect.topleft[1]+ node.y), node.radius, node.border)

class Lamp(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("lamp.png", x, y, 50, 50, [Node(11, 43), Node(40, 43)])

class Battery(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("battery.png", x, y, 50, 50, [Node(-4, 25), Node(54, 25)])

class Key(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("key.png", x, y, 100, 50, [Node(-6, 30), Node(107, 30)])
# Screen init
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Circuit Creator")
icon = pygame.image.load('electrical-circuit.png')
pygame.display.set_icon(icon)

props = [Lamp(30, 50), Battery(100, 50), Key (200, 50)]



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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if lamp_rect.collidepoint(event.pos):
        #         moving_object = 'lamp'
        #         moving_offset = (event.pos[0] - lamp_rect.topleft[0], event.pos[1] - lamp_rect.topleft[1])
        #     elif battery_rect.collidepoint(event.pos):
        #         moving_object = 'battery'
        #         moving_offset = (event.pos[0] - battery_rect.topleft[0], event.pos[1] - battery_rect.topleft[1])
        #     elif key_rect.collidepoint(event.pos):
        #         moving_object = 'key'
        #         moving_offset = (event.pos[0] - key_rect.topleft[0], event.pos[1] - key_rect.topleft[1])         
        # if event.type == pygame.MOUSEBUTTONUP:
        #     moving_object = None
        # if event.type == pygame.MOUSEMOTION:
        #     if moving_object == 'lamp':
        #         lamp_rect.topleft = (event.pos[0] - moving_offset[0], event.pos[1] - moving_offset[1])
        #     elif moving_object == 'battery':
        #         battery_rect.topleft = (event.pos[0] - moving_offset[0], event.pos[1] - moving_offset[1])
        #     elif moving_object == 'key':
        #         key_rect.topleft = (event.pos[0] - moving_offset[0], event.pos[1] - moving_offset[1])
        

    screen.fill((255, 255, 255))

    for prop in props:
        prop.draw(screen)
        prop.drawNodes(screen)

    pygame.display.flip()

pygame.quit()
