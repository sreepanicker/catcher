# This game is primarly to show case the usage of pygame , Sprite and collide feature 
# Chopper is droping parachutes from the sky, the player needs to cpature the parachutes
# using boat. Boat can be operated using left and right key. 


#importing the pygame 
import pygame, random

# Screen Size 
WIDTH = 900
HEIGHT = 700

#Colors values
LIGHT_RED= (204, 51, 0) 
DARK_RED = (255,128,128) 

#Score board & life counts
score = 0
lifeCount = 10


#Chopper class ,loading the chopper image
#setting the initial corordinate X and Y , 800 100
# 
class Chopper(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.x =800
		self.y =100
		self.image = pygame.image.load("chopper.png")
		self.rect = self.image.get_rect()
		self.rect.center = (self.x ,self.y)
#updating the cordinate of the chopper 
	def update(self):
		self.x -=5
		if self.x <=0 : # if it reached 0, then moved to the right side 
			self.x =800
		self.rect.center = (self.x ,self.y)


# defining parachute for jumping 
class Parachute(pygame.sprite.Sprite):
	def __init__(self,xLoc):
		super().__init__()
		self.x =xLoc
		self.y=100
		self.image = pygame.image.load("jump4.png")
		self.rect =self.image.get_rect()
		self.rect.center = (self.x ,self.y)
#update the parachute coordinates, jump
	def update(self):
		self.y +=5
		self.rect.center = (self.x ,self.y)


#define boat to capture parachute 
class Boat(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.x =400
		self.y =650
		self.image = pygame.image.load("boat.png")
		self.rect = self.image.get_rect()
		self.rect.center = (self.x ,self.y)
	def changeLoc(self,xLoc):
		self.x = self.x + xLoc
		if self.x <=0 :
			self.x =0
		if self.x >= 900 :
			self.x =900
	def update(self):
		self.rect.center = (self.x ,self.y)


# define a forest class , if Parachut hit forst, loose the life 
class Forest(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		forest = pygame.image.load("parallax-mountain-trees.png")
		forestscale = pygame.transform.scale(forest,(2000,40))
		self.image =forestscale
		self.rect =self.image.get_rect()
		self.rect.center = (0,680)


def printscoreAndLife():
	font = pygame.font.Font('freesansbold.ttf', 32) 
	text = font.render('Score : ' + str(score), True, LIGHT_RED, DARK_RED) 
	textRect = text.get_rect() 
	textRect.center = (600,50)
	screen.blit(text,textRect)
	textLife = font.render('Life Count : ' + str(lifeCount), True, LIGHT_RED, DARK_RED) 
	textRectLife = textLife.get_rect() 
	textRectLife.center = (200,50)
	screen.blit(textLife,textRectLife)


#Initializing the pygame ,Screen and Clock
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


#background images 
#original background
bgImage = pygame.image.load("parallax-mountain-bg.png")
#Scale to the screen
bgImage = pygame.transform.scale(bgImage,(WIDTH,HEIGHT))
#Mountains 
bgImage2 = pygame.image.load("parallax-mountain-montain-far.png")
bgImage2 = pygame.transform.scale(bgImage2,(500,50))
bgImage3 = pygame.image.load("parallax-mountain-mountains.png")
bgImage3 = pygame.transform.scale(bgImage3,(500,50))


#drawing single item object to the screen, chopper ,boat etc
chopper =  Chopper()
boat = Boat()
forest = Forest()
generic_list = pygame.sprite.Group()
generic_list.add(chopper)
generic_list.add(boat)
generic_list.add(forest)

#creating parachute Array
parachute_list = pygame.sprite.Group()


def addToParachuteList():
	ran = random.randrange(0,50)
	if ran == 10 :
		parachute  = Parachute(chopper.x )
		parachute_list.add(parachute)
	

#detect the catch 
def detectCatach():
	colidelist = pygame.sprite.spritecollide(boat,parachute_list,True)
	data =0
	if len(colidelist) > 0:
		data+=len(colidelist)
	return data

# checking the crashes
def detectcrashes():
	crashList = pygame.sprite.spritecollide(forest,parachute_list,True)
	crash =0
	if len(crashList) > 0:
		crash+=len(crashList)
	return crash

# variable to exit the main loop
done = False
screen.blit(bgImage,(0,0))
screen.blit(bgImage2,(0,300))
screen.blit(bgImage2,(300,300))
screen.blit(bgImage3,(400,300))
printscoreAndLife()

while not done:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			if event.key == pygame.K_q :
				done = True
			if event.key == pygame.K_LEFT :
				boat.changeLoc(-15)
			if event.key == pygame.K_RIGHT :
				boat.changeLoc(15)

	#Drawing the background images 
	
	screen.blit(bgImage,(0,0))
	screen.blit(bgImage2,(0,300))
	screen.blit(bgImage2,(300,300))
	screen.blit(bgImage3,(400,300))
	printscoreAndLife()

	# checking the lifeCount 
	if lifeCount > 0 :
		generic_list.draw(screen)
		generic_list.update()
		addToParachuteList()
		parachute_list.draw(screen)
		parachute_list.update()

		#getting number of catches 
		collioncount = detectCatach() 
		#increasing the catch count 
		score+=collioncount
		#removing the soliders who is not visible in the screen 
		count = detectcrashes()
		lifeCount -= count
	pygame.display.flip();
	clock.tick(20)

pygame.quit()




