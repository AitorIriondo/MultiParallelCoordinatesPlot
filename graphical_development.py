import pygame
import math
import random
import tkinter as tk
from tkinter import filedialog
import threading
import queue
from axis_class import Line
from axis_class import PointsLine
from axis_class import Axis
import pandas as pd
from controller import Controller


# creating a data frame
#df = pd.read_csv("estela_with_constraints.csv", delimiter =";")

# Function to ask the user for a file
def ask_for_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    root.destroy()  # Close the tkinter window
    return file_path

# Prompt the user for the file
file_path = ask_for_file()

if file_path:  # Check if a file was selected
    # Read the selected CSV file into a DataFrame
    df = pd.read_csv(file_path, delimiter=",")
    print(f"Dataset loaded successfully from {file_path}")
else:
    print("No file selected. Exiting.")


# Initialize Pygame
pygame.init()

# Constants for the screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

# Colors
WHITE = (255, 255, 255)

# Iterate through column names and their data
class Environment:
    axisArray = []
    pointLines = []
    def __init__(self,screen):
        self.screen = screen
    def addAxis(self, line):
        self.axisArray.append(Axis(line,screen))
    def addPointLine(self, axis1Index,axis1Val,axis2Index,axis2Val):
        self.pointLines.append(PointsLine(axis1Index,axis1Val,axis2Index,axis2Val))
    def updatePointLines(self):
        for line in self.pointLines:
            centerA = self.axisArray[line.axis1Index].line.center
            valueA = line.axis1Val
            centerB = self.axisArray[line.axis2Index].line.center
            valueB = line.axis2Val
            pointAx = centerA[0] + (self.axisArray[line.axis1Index].line.length*(valueA-0.5)) * math.cos(math.radians(self.axisArray[line.axis1Index].line.angle))
            pointAy = centerA[1] + (self.axisArray[line.axis1Index].line.length*(valueA-0.5)) * math.sin(math.radians(self.axisArray[line.axis1Index].line.angle))
            pointBx = centerB[0] + (self.axisArray[line.axis2Index].line.length*(valueB-0.5)) * math.cos(math.radians(self.axisArray[line.axis2Index].line.angle))
            pointBy = centerB[1] + (self.axisArray[line.axis2Index].line.length*(valueB-0.5)) * math.sin(math.radians(self.axisArray[line.axis2Index].line.angle))
            line.pointA = (pointAx,pointAy)
            line.pointB = (pointBx,pointBy)
            line.draw_line(self.screen)
    def update(self):
        self.screen.fill((0, 0, 0))

        for axis in self.axisArray:
            axis.draw_axis(screen)

        self.updatePointLines()

def createRandomLine():
    return Line((random.randint(100,1200), random.randint(100,600)), 90, 200)

# Create a Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multi-Parallel Coordinates Plot")

#Create environment
env = Environment(screen)

#Create controller
con = Controller(df)


def run_tkinter():
    def on_item_click(event):
        selected_item = listbox.curselection()
        if selected_item:
            item_index = selected_item[0]
            queue.put(item_index)  # Put the selected item index into the queue
            print(f"Clicked on item {item_index}")

    root = tk.Tk()
    root.title("List of Names")

    listbox = tk.Listbox(root)
    for i, name in enumerate(names):
        listbox.insert(tk.END, name)
        listbox.bind("<ButtonRelease-1>", on_item_click)

    listbox.pack()

    root.mainloop()

# Start the Tkinter GUI in a separate thread
names = con.normalized_df.columns.to_list()
queue = queue.Queue()
tkinter_thread = threading.Thread(target=run_tkinter)
tkinter_thread.daemon = True
tkinter_thread.start()


def createAxisFromIndex(i):
    names = con.normalized_df.columns.to_list()
    column_values = con.normalized_df[names[i]]
    line = createRandomLine()
    env.addAxis(line)
    env.axisArray[-1].name = names[i]
    env.axisArray[-1].values = column_values
    env.axisArray[-1].i = len(env.axisArray)-1

createAxisFromIndex(4)

# Draw lines
def createLinesbetweenAxis( axs1, axs2):
    for i in range(len(axs1.values)):
        env.addPointLine(axs1.i,axs1.values[i],axs2.i,axs2.values[i])


# Game loop
dragging = False
running = True

# Flags to track the right-click events
selected_line_index_aux = -1
selected_line_index = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Drag event handle
    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            selected_line_index = None
            for i, axis in enumerate(env.axisArray):
                line_endpoint_x = axis.line.center[0] + axis.line.length * math.cos(math.radians(axis.line.angle))
                line_endpoint_y = axis.line.center[1] + axis.line.length * math.sin(math.radians(axis.line.angle))
                if math.hypot(mouse_x - axis.line.center[0], mouse_y - axis.line.center[1]) < 30:
                    selected_line_index = i
                    dragging = True
                    mouse_offset = [axis.line.center[0] - mouse_x, axis.line.center[1] - mouse_y]
        elif event.button == 3:  # Right-click
            mouse_x, mouse_y = event.pos
            for i, axis in enumerate(env.axisArray):
                if i == selected_line_index:
                    continue  # Skip the selected line
                line_endpoint_x = axis.line.center[0] + axis.line.length * math.cos(math.radians(axis.line.angle))
                line_endpoint_y = axis.line.center[1] + axis.line.length * math.sin(math.radians(axis.line.angle))
                if math.hypot(mouse_x - axis.line.center[0], mouse_y - axis.line.center[1]) < 30:
                    # Right-click on another line
                    if (selected_line_index_aux == -1):
                        selected_line_index_aux = i
                    selected_line_index = i
                    right_click_triggered = True
                    if(selected_line_index_aux != selected_line_index):
                        createLinesbetweenAxis(env.axisArray[selected_line_index_aux], env.axisArray[selected_line_index])
                        selected_line_index_aux = -1 
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            dragging = False
    elif event.type == pygame.MOUSEMOTION:
        if dragging and selected_line_index is not None:
            mouse_x, mouse_y = event.pos
            env.axisArray[selected_line_index].line.center = [mouse_x + mouse_offset[0], mouse_y + mouse_offset[1]]  
    try:
        item_index = queue.get_nowait()
        if item_index is not None:
            # Process the selected item index from Tkinter in your Pygame logic
            # For example, draw a line based on the selected index
            if 0 <= item_index < len(con.normalized_df):
                createAxisFromIndex(item_index)
    except:
        pass
    # Update the display
    env.update()
    pygame.display.flip()


# Quit Pygame
pygame.quit()