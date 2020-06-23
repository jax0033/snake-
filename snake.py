import pygame
import random

#beautiful, init mate?
pygame.init()
screen  = pygame.display.set_mode((802,802))
width,height = 802,802
font = pygame.font.Font("freesansbold.ttf",32)


#draws a block filling a grid point onto the screen
def block(coords, color=(255,0,0)):
	x,y = gridalign((coords[0],coords[1]))[0], gridalign((coords[0],coords[1]))[1]
	x2,y2 = x+47,y+47
	pygame.draw.polygon(screen,color, ((x,y),(x2,y),(x2,y2),(x,y2)),0)

#draws the grid onto the screen
def grid():
	for n in range(17):
		pygame.draw.line(screen, (255,255,255), (n*50,0), (n*50,height), 2)
		for n in range(17):
			pygame.draw.line(screen, (255,255,255), (0,n*50), (width,n*50), 2)

def sscore(x,y,score):
	render = font.render(f"Score : {score}", True, (255,255,255))
	screen.blit(render,(x,y))

#aligns a given point to the grid
def gridalign(coords):
	x = coords[0]
	y = coords[1]
	#aligns X
	temp = True
	n = 0
	while temp:
		if x <= n*50:
			x = (n-1)*50
			temp = False
		n += 1
	#aligns Y
	temp = True
	n=0
	while temp:
		if y <= n*50:
			y = (n-1)*50
			temp = False
		n += 1

	return (round(x+2),round(y+2))

"""
Head class, contains SnakeXYposition, its last XYposition and its last move
"""

class Head:
	def __init__(self,headx,heady,lastposition,lastmove):
		self.headx = headx
		self.heady = heady
		self.lastposition = lastposition
		self.lastmove = lastmove

	def moveup(self):
		self.lastposition = (self.headx,self.heady)
		self.heady -= 50
		self.lastmove = "up"

	def movedown(self):
		self.lastposition = (self.headx,self.heady)
		self.heady += 50
		self.lastmove = "down"

	def moveleft(self):
		self.lastposition = (self.headx,self.heady)
		self.headx -= 50
		self.lastmove = "left"

	def moveright(self):
		self.lastposition = (self.headx,self.heady)
		self.headx += 50
		self.lastmove = "right"

"""
Body class, contains BodyXYposition
"""

class Body:
	def __init__(self,bodyx,bodyy):
		self.bodyx = bodyx
		self.bodyy = bodyy


def speedtimervisualized(x,y,text):
	render = font.render(f"Speed : {text}", True, (197,155,239))
	screen.blit(render,(x,y))


"""
puts the last element of 'lst' at the front (and later it will be set to the position of the Head.lastposition).
"""
def bodymove(lst):
	temp = []
	temp.append(lst[-1])
	lst.pop(-1)
	for part in lst:
		temp.append(part)
	return temp

rn = random.randint(0,800),random.randint(0,800)

snakehead = Head(440,440,None,"up")

body_parts = [Body(snakehead.headx,snakehead.heady+50),Body(snakehead.headx,snakehead.heady+100)]

foodtypes = ["normal","normal","normal","normal","normal","triple points","speed1","slow1"]

lastmove = "up"
counter = 1200000
fruitspawn = 0
score = 0
speed = 340000

#bools
speedtimer = False
enable_last_move = True
running = True
eventloop = True
fruit_ = True
newbodypart = False
while running:
	#resets the counter if above limit so it wont overflow
	if counter >= 800000001:
		counter = 1

	#basically the most unreliable in game timer
	if counter %speed == 0:

		#fills the screen with black so we get a 'blank' canvas/screen
		screen.fill((0,0,0))



		#checks for pressed keys (up down right left arrow keys)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				
				if eventloop:
					
					#if key is pressed snake moves in according direction and it disables key inputs for that loop and disables the automove of the snake
					if event.key == pygame.K_LEFT and snakehead.lastmove != "right":
						snakehead.moveleft()
						enable_last_move = False
						eventloop = False

					elif event.key == pygame.K_UP and snakehead.lastmove != "down":
						snakehead.moveup()
						enable_last_move = False
						eventloop = False
					
					elif event.key == pygame.K_DOWN and snakehead.lastmove != "up":
						snakehead.movedown()
						enable_last_move = False
						eventloop = False
					
					elif event.key == pygame.K_RIGHT and snakehead.lastmove != "left":
						snakehead.moveright()
						enable_last_move = False
						eventloop = False

		#automatically moves the snake in the direction is moved last
		if enable_last_move:
			if snakehead.lastmove == "up":
				snakehead.moveup()

			elif snakehead.lastmove == "down":
				snakehead.movedown()

			elif snakehead.lastmove == "left":
				snakehead.moveleft()

			elif snakehead.lastmove == "right":
				snakehead.moveright()
		
		while fruit_:
			fruitspawn = 0
		 	
		 	#while fruit true it will spawn a fruit on a grid that is not occupied by the snakehead or body
			rand = gridalign((random.randint(0,800),random.randint(0,800)))
			for part in body_parts:
				xy = gridalign((part.bodyx,part.bodyy))
				if xy[0] == rand[0] and xy[1] == rand[1]:
					fruitspawn += 1

			if fruitspawn == 0:
				food = rand
				foodtype = random.choice(foodtypes)
				if foodtype == "normal":
					foodcolor = (255,0,0)
				elif foodtype == "triple points":
					foodcolor = (205,0,255)
				
				elif foodtype == "speed1":
					foodcolor = (0,200,255)


				elif foodtype == "slow1":
					foodcolor = (44,44,44)
				fruit_ = False

		#checks if snakehead is on the same pos as the food and adds a new part to the snake
		snakehead_aligned = gridalign((snakehead.headx,snakehead.heady))
		if food[0] == snakehead_aligned[0] and food[1] == snakehead_aligned[1]:
			if foodtype == "normal":
				newbodypart = True
				fruit_ = True
				score += 1

			elif foodtype == "triple points":
				newbodypart = True
				score += 3
				fruit_ = True


			elif foodtype == "speed1":
				newbodypart = True
				speed = 200000
				speedtimer = True
				score += 1
				speedcounter = 240
				fruit_ = True

			elif foodtype == "slow1":
				newbodypart = True
				speed = 500000
				speedcounter = 120
				speedtimer = True
				score += 1
				fruit_ = True

		if newbodypart:
			body_parts.append(Body(snakehead.lastposition[0],snakehead.lastposition[1]))
			newbodypart = False
			body_parts = bodymove(body_parts)

		else:
			body_parts = bodymove(body_parts)
			body_parts[0].bodyx,body_parts[0].bodyy = snakehead.lastposition[0],snakehead.lastposition[1]

		if snakehead.headx > 800 or snakehead.headx < 0:
			running = False
			defeat = True
		if snakehead.heady > 800 or snakehead.heady < 0:
			running = False
			defeat = True

		if score > 20:
			running = False
			defeat = False
			win = True

		for part in body_parts:
			if part.bodyx == snakehead.headx and part.bodyy == snakehead.heady:
				running = False
				defeat = True
			block((part.bodyx,part.bodyy), color = (0,255,0))


		block(food, foodcolor)	
		block((snakehead.headx,snakehead.heady), color=(255,0,0))

		enable_last_move = True
		grid()
		sscore(10,10,score)
		eventloop = True
		
		if speedtimer:
			speedtimervisualized(600,750,speedcounter)

			speedcounter -= 3
			if speedcounter <= 0:
				speedtiemr = False
				speedcounter = 0
				speed = 340000


		pygame.display.update()
	counter+=1

	
	
#endings, havent really thought of anything for them. will probably add something in the next update.
if defeat:
	print("You lost! "*999)
	win = False

if win:
	print("You won! "*999)

"""
															created by jax0033@protonmail.com
"""
