import pygame
import math

pygame.init()

temp_node = None
temp_points = []
             
def circle_to_point_coll(circle_pos, radius, point):
    dx = point[0] - circle_pos[0]
    dy = point[1] - circle_pos[1]
    dist = math.sqrt(dx * dx + dy *dy)
    return dist <= radius

class MenuButton:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.submenu_open = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.submenu_open = not self.submenu_open
                return True
        return False

class SubmenuOption:
    def __init__(self, image, x, y, w, h, prop_class):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prop_class = prop_class
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                props.append(self.prop_class(event.pos[0], event.pos[1]))
                return True
        return False
    
class Edge:
    def __init__(self, from_node, to_node, points) -> None:
        self.from_node = from_node
        self.to_node = to_node
        self.hasElectric = False
        from_node.edges.add(self)
        to_node.edges.add(self)
        self.points = points
        
    
    def remove(self,dontDel):
        if self.from_node != dontDel:
            self.from_node.edges.remove(self)
        if self.to_node != dontDel:
            self.to_node.edges.remove(self)

    
    def setElectricity(self, hasElectric):
        if self.hasElectric == hasElectric:
            return
        self.hasElectric = hasElectric
        self.from_node.parent.update()
        self.to_node.parent.update()
   
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
    
    def movePoint(self, event):
        global moving_object_point_index, moving_offset_point, which_edge_point
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 3:
                for edge in self.edges:
                    for i, point in enumerate(edge.points):
                        if circle_to_point_coll(point, 8, pygame.mouse.get_pos()):
                            which_edge_point = edge
                            moving_object_point_index = i
                            moving_offset_point = (event.pos[0] - point[0], event.pos[1] - point[1])              

        if event.type == pygame.MOUSEBUTTONUP:
            moving_object_point_index = None
            which_edge_point = None
            
 
        if event.type == pygame.MOUSEMOTION:
            if moving_object_point_index is not None:
                which_edge_point.points[moving_object_point_index] = (event.pos[0] - moving_offset_point[0], event.pos[1] - moving_offset_point[1])        
    
    
class Prop:
    def __init__(self, img, x, y, w, h, nodes) -> None:
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.rect = self.img.get_rect(topleft=(x,y))
        self.nodes = nodes
    
    def update(self):
        pass
    
    def right_clicked(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)
    


    def movingObjects(self, event):
        global moving_object, moving_offset

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 3:
                    self.right_clicked()
                else:
                    moving_object = self
                    moving_offset = (event.pos[0] - self.rect.topleft[0], event.pos[1] - self.rect.topleft[1])
    
        if event.type == pygame.MOUSEBUTTONUP:
            moving_object = None

        if event.type == pygame.MOUSEMOTION:
            if moving_object is not None:
                moving_object.rect.topleft = (event.pos[0] - moving_offset[0], event.pos[1] - moving_offset[1])

    def draw_nodes_and_edges(self, screen):
        for node in self.nodes:
            pygame.draw.circle(screen, (0,0,0), node.get_pos(), node.radius, node.border)
            for edge in node.edges:
                draw_points(edge.points, edge.from_node.get_pos(), edge.to_node.get_pos(), edge.hasElectric)
        if temp_node is not None:
            pygame.draw.circle(screen, (0, 0, 0), pygame.mouse.get_pos(), 10, 1)  

    def foundCableNodes(self, event): 
        global temp_node
        if event.type == pygame.MOUSEBUTTONDOWN:
            for node in self.nodes:
                if circle_to_point_coll(node.get_pos(), node.radius, event.pos):
                    if(temp_node != None):
                        if temp_node != node:
                            Edge(temp_node, node, temp_points.copy())
                        temp_points.clear()    
                        temp_node = None
                    else:
                        temp_node = node
                    return True
        return False

class Lamp(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("lightbulb.png", x, y, 50, 50, [Node(self, -2, 43), Node(self, 52, 43)])

    def update(self):
        node_counter = 0
        edge_counter = 0
        for node in self.nodes:
            node_counter += 1
            for edge in node.edges:
                if edge.hasElectric:
                    edge_counter += 1
    
        if node_counter == edge_counter:
            self.img = pygame.image.load("lamp.png")
            self.img = pygame.transform.scale(self.img, (50, 50))
            self.rect = self.img.get_rect(topleft=self.rect.topleft)
            super().draw(screen)
        else:
            self.img = pygame.image.load("lightbulb.png")
            self.img = pygame.transform.scale(self.img, (50, 50))
            self.rect = self.img.get_rect(topleft=self.rect.topleft)
            super().draw(screen)                                  
           

class Battery(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("battery.png", x, y, 50, 50, [Node(self, -4, 25), Node(self, 54, 25)])

    def update(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.setElectricity(True)

class Key(Prop):
    def __init__(self, x, y) -> None:
        super().__init__("blackkey.png", x, y, 100, 50, [Node(self, -6, 30), Node(self, 107, 30)]) 
        self.is_open = False
    
    def right_clicked(self):
        self.is_open = not self.is_open

    def update(self):
        has_electric_node = None
        for node in self.nodes:
            for edge in node.edges:
                if self.is_open and edge.hasElectric:
                    has_electric_node = node
                    break
            if has_electric_node != None:
                break
        if has_electric_node != None:
            for node in self.nodes:
                if node == has_electric_node:
                    continue
                for edge in node.edges:
                    if self.is_open:
                        edge.setElectricity(True)
                    else:
                        edge.setElectricity(False)
        if self.is_open:
            self.img = pygame.image.load("key.png")
            self.img = pygame.transform.scale(self.img, (100, 50))
            self.rect = self.img.get_rect(topleft=self.rect.topleft)
            super().draw(screen)            

        else:
            self.img = pygame.image.load("blackkey.png")
            self.img = pygame.transform.scale(self.img, (100, 50))
            self.rect = self.img.get_rect(topleft=self.rect.topleft)
            super().draw(screen)    

                            
                 
def draw_points(points, from_pos, to_pos, has_electric):
    color = (242,218,9) if has_electric else (0,0,0)
    color2 = (255,0,0) if has_electric else (0,0,0)
    drew = False
    for i, point in enumerate(points):
        drew = True
        if i == 0:
            pygame.draw.line(screen, color, point, from_pos)
            pygame.draw.line(screen, color2, (point[0] - 5 , point[1] -5), (from_pos[0] -5, from_pos[1] - 5) )
        else:
            pygame.draw.line(screen, color, point, points[i-1])
            pygame.draw.line(screen, color2, (point[0] - 5 , point[1] -5), (points[i-1][0] - 5 , points[i-1][1] -5))
        
        if i == len(points)-1:
            pygame.draw.line(screen, color, point, to_pos)
            pygame.draw.line(screen, color2, (point[0] - 5 , point[1] -5), (to_pos[0] - 5 , to_pos[1] -5))

        pygame.draw.circle(screen, (0,0,0), point, 8, 1)
    if not drew:
        pygame.draw.line(screen, color, from_pos, to_pos)
        pygame.draw.line(screen, color2, (from_pos[0] - 5 , from_pos[1] -5), (to_pos[0] - 5 , to_pos[1] -5))



# Screen init
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Circuit Creator")
icon = pygame.image.load('electrical-circuit.png')
pygame.display.set_icon(icon)

props = []

edges = []


# Main loop
running = True
moving_object = None
moving_offset = (0,0)
moving_object_point_index = None
moving_offset_point = (0,0)
which_edge_point = None


main_menu_button = MenuButton("node.png", 10, 10)

submenu_open = False

lamp_option = SubmenuOption("lamp.png", 30, 50, 50, 50, Lamp)
battery_option = SubmenuOption("battery.png", 100, 50, 100, 50, Battery)
key_option = SubmenuOption("key.png", 200, 50, 180, 50, Key)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            for prop in props:
                if prop.rect.collidepoint(pygame.mouse.get_pos()):
                    for node in prop.nodes:
                        for edge in node.edges:
                            edge.remove(node)
                    props.remove(prop)
                    break
                for node in prop.nodes:
                    for edge in node.edges:
                        for point in edge.points:
                            if circle_to_point_coll(point, 8 , pygame.mouse.get_pos() ) :
                                edge.points.remove(point)


        # for prop in props:
        #     for node in prop.nodes:
        #         if node.parent is Key:
        #             for node in node.parent.nodes:
        #                 if node.parent.has_electric_thing == node:
        #                     for edge in node:
        #                         edge.hasElectricThings(True)
        #             continue
        #         for edge in node.edges:
        #             edge.hasElectricThings(True)

                

        for prop in props:
            for node in prop.nodes:
                node.movePoint(event)
                   


        should_point = True
        for prop in props:
            prop.movingObjects(event)
            if prop.foundCableNodes(event) and should_point:
                should_point = False


        if event.type == pygame.MOUSEBUTTONDOWN  and event.button == 3 and should_point and temp_node != None:
            temp_points.append(event.pos)

        main_menu_button.handle_event(event)

        if main_menu_button.submenu_open:
            submenu_options = [lamp_option, battery_option, key_option]
            for option in submenu_options:
                option.handle_event(event)

    screen.fill((255, 255, 255))

    main_menu_button.draw(screen)

    if main_menu_button.submenu_open:
        pygame.draw.rect(screen, (200, 200, 200), (0, 45, 400, 70))  
        submenu_options = [lamp_option, battery_option, key_option]
        for option in submenu_options:
            option.draw(screen)
    for prop in props:
        for node in prop.nodes:
            for edge in node.edges:
                edge.setElectricity(False)


    for prop in props:
        prop.update()
        prop.draw(screen)
        prop.draw_nodes_and_edges(screen)


    if temp_node is not None:
        draw_points(temp_points, temp_node.get_pos(), pygame.mouse.get_pos(), False )
    
    pygame.display.flip()

pygame.quit()