import pygame
import math
WHITE = (255, 255, 255)

# Axis definition
class Line:
    def __init__(self,center, angle, length):
        self.center = center
        self.angle = angle
        self.length = length
    def draw_line(self, screen):
        angle_radians = math.radians(self.angle)
        endpoint_x1 = self.center[0] + self.length/2 * math.cos(angle_radians)
        endpoint_y1 = self.center[1] + self.length/2 * math.sin(angle_radians)
        endpoint_x2 = self.center[0] - self.length/2 * math.cos(angle_radians)
        endpoint_y2 = self.center[1] - self.length/2 * math.sin(angle_radians)
        pygame.draw.line(screen, WHITE, (endpoint_x1,endpoint_y1), (endpoint_x2, endpoint_y2), 3)

        
class PointsLine:
    pointA = (0,0)
    pointB = (0,0)
    def __init__(self,axis1Index,axis1Val,axis2Index,axis2Val):
        self.axis1Index = axis1Index
        self.axis1Val = axis1Val #Value as a percentage from 0 to 1
        self.axis2Index = axis2Index
        self.axis2Val = axis2Val
        print(axis1Val)
        print(axis2Val)
    def draw_line(self, screen):
        #Calculate line
        pygame.draw.line(screen, WHITE, self.pointA, self.pointB, 1)      


class Axis:
    name = "ObjName"
    values = ""
    min = -float('inf')
    max = float('inf')
    i = -1
    def __init__(self,line, screen):
        self.line = line
        self.draw_axis(screen)
    def draw_axis(self, screen):
        #Draw main axis
        self.line.draw_line(screen)

        #Draw corners
        perp_angle1 = self.line.angle + 90
        perp_angle2 = self.line.angle + 90
        perp_length = 10  # Length of the perpendicular lines

        center1_x = self.line.center[0] + (self.line.length/2) * math.cos(math.radians(self.line.angle))
        center1_y = self.line.center[1] + (self.line.length/2) * math.sin(math.radians(self.line.angle))

        center2_x = self.line.center[0] - (self.line.length/2)* math.cos(math.radians(self.line.angle))
        center2_y = self.line.center[1] - (self.line.length/2)* math.sin(math.radians(self.line.angle))

        perp1 = Line((center1_x,center1_y),perp_angle1,perp_length)
        perp2 = Line((center2_x,center2_y),perp_angle2,perp_length)

        perp1.draw_line(screen)
        perp2.draw_line(screen)

        # Create a font object
        font = pygame.font.Font(None, 20)  # You can replace 'None' with a specific font file path if needed

        # Render the text
        text = font.render(self.name, True, (255, 255, 255))  # White text
        screen.blit(text, (center2_x -30, center2_y-25))
