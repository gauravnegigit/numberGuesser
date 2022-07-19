import pygame 
import tensorflow as tf
from tkinter import * 
from tkinter import messagebox 
import numpy as np 
import matplotlib.pyplot as plt
pygame.init()


class Pixel :
  def __init__(self , x , y , width , height ):
    self.x = x
    self.y = y 
    self.width = width 
    self.height = height
    self.color = (255 , 255 , 255)  # this is the RGB format for white color 
    self.neighbours = []
  
  def draw(self , surface):
    pygame.draw.rect(surface , self.color , (self.x , self.y , self.width ,self.height))
  
  def getNeighbours(self , g):
    j = self.x //20 
    i = self.y //20 

    # the variable i denotes the current row value 
    # the variable j denote sthe current column value 

    rows = cols = 28 

    # cases for horizontal and vertical numbers.
    if i < cols -1 :
      self.neighbours.append(g.pixels[i + 1][j])
    
    if i > 0 :
      self.neighbours.append(g.pixels[i - 1][j])
    
    if j < rows - 1 :
      self.neighbours.append(g.pixels[i][j + 1])

    if j > 0 :
      self.neighbours.append(g.pixels[i][j - 1])
    
    # looking for diagonal neighbours 
    if j > 0 and i > 0 :   # top left 
      self.neighbours.append(g.pixels[i - 1][j - 1])
    if j + 1 <rows and  i > 1 : # bottom left 
      self.neighbours.append(g.pixels[i - 1][j + 1])

    if j -1 < rows and i < cols -1 and j -1  > 0 : # top right
      self.neighbours.append(g.pixels[i + 1][j - 1])

    if j < rows - 1 and i < cols - 1 :     # top left 
      self.neighbours.append(g.pixels[i + 1][j + 1])
    

class Grid :
  pixels = []

  def __init__(self , row , col , width , height):
    self.rows = row 
    self.cols = col 
    self.len = row * col 
    self.width = width 
    self.height = height 
    self.generatePixels()
    
  
  def draw(self , surface):
    for row in self.pixels :
      for col in row :
        col.draw(surface)
      
  
  def generatePixels(self):
    x_gap = self.width // self.cols 
    y_gap = self.height // self.rows 

    self.pixels = []

    for r in range(self.rows):
      self.pixels.append([])
      for c in range(self.cols):
        self.pixels[r].append(Pixel(x_gap * c , y_gap * r , x_gap , y_gap ))
      
    
    for r in range(self.rows):
      for c in range(self.cols):
        self.pixels[r][c].getNeighbours(self)
    
  def clicked(self , pos):
    try :
      t = pos[0]
      w = pos[1]
      g1 = int(t) // self.pixels[0][0].width  # self.pixels contain the pixel objects so self.pixels[0][0] would give the width teh 1st pixel 
      g2 = int(w) // self.pixels[0][0].height 

      return self.pixels[g2][g1]

    except :
      pass 
  
  def convert_binary(self):

    """
    this method is comes in handy to convert the image in binary format by taking 0 in case of white and 1 in case of other colors 
    """
        
    li = self.pixels 

    newMatrix = [[] for x in range(len(li))]

    for i in range(len(li)):
      for j in range(len(li[i])) :
        if li[i][j].color == (255 , 255 , 255) :
          newMatrix[i].append(0)
        else :
          newMatrix[i].append(1)

    mnist = tf.keras.datasets.mnist 
    (x_train , y_train) , (x_test , y_test) = mnist.load_data()
    x_test = tf.keras.utils.normalize(x_test , axis = 1)         

    for row in range(28) :
      for x in range(28):
        x_test[0][row][x] = newMatrix[row][x]
    
    return x_test[:1]

def guess(li):
  model = tf.keras.models.load_model('m.model')

  predictions = model.predict(li)
  print(predictions[0])
  t = (np.argmax(predictions[0]))
  print("I predict this number is a : " , t)
  root = Tk()
  root.withdraw()
  messagebox.showinfo("Preediction" , "I predict this number is a " + str(t))
  root.destroy()

def main():
  run = True 

  while run :
    for event in pygame.event.get():
      if event.type == pygame.QUIT :
        run = False 
        pygame.quit()
        quit()
      
      if event.type == pygame.KEYDOWN :
        li = g.convert_binary()
        guess(li)
        g.generatePixels()
      
      if pygame.mouse.get_pressed()[0] :     # for left mouse click
        pos = pygame.mouse.get_pos()
        clicked = g.clicked(pos)
        clicked.color = (0 , 0 , 0)

        for n in clicked.neighbours : 
          n.color = (0 , 0 , 0)
        
      if pygame.mouse.get_pressed()[2]:      # for right mouse click 
        try :
          pos = pygame.mouse.get_pos()
          clicked = g.clicked(pos)
          clicked.color = (255 , 255 , 255)

        except :
          pass 
      
    g.draw(WIN)
    pygame.display.update()

# main screen constants 
WIDTH , HEIGHT =  560 , 560         # since there are 28 rows and columns each being 20 pixels wide 
WIN  = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Number Guesser")
g = Grid(28 , 28 , WIDTH , HEIGHT)

main()