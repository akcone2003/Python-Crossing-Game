#Basic game setup
#Display

# Get access to pygame functions
import pygame

# -------------------------------------------------------------Global variables------------------------------------------------------

# Screen dimensions
SCREEN_TITLE = "Cross The Road"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# RGB colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('comicsans', 70)

# ----------------------------------------------------------------------Game class--------------------------------------------------------------------------
class Game:

    TICK_RATE = 60
    isGameOver = False

    # Constructor for game class
    def __init__(self, imagePath, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Create game window with specified dimensions
        self.gameScreen = pygame.display.set_mode((width, height))
        # Fill game window with specified color
        self.gameScreen.fill(WHITE_COLOR)
        # Display title
        pygame.display.set_caption(title)

        # Load background image
        backgroundImage = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(backgroundImage, (width, height))
    

    # Run the game function
    # Game loop
    def runGame(self, level):

        isGameOver = False
        didWin = False
        direction = 0

        # Spawn characters
        playerCharacter = Player('player.png', 375, 700, 50, 50)
        
        enemy0 = Enemy('enemy.png', 20, 600, 50, 50)
        # Speed increases with difficulty increase
        enemy0.SPEED *= level

        # Enemy 1 appears after first 3 rounds
        enemy1 = Enemy('enemy.png', self.width - 40, 400, 50, 50)
        enemy1.SPEED *= level

        # Enemy 2 appears after first 6 rounds
        enemy2 = Enemy('enemy.png', 20, 200, 50, 50)
        enemy2.SPEED *= level
        
        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        # Main game loop
        
        while not isGameOver:
            # Gets all the events happening in the game during each iteration of while loop
            # Events can be mouse clicks, collisions etc. 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if event results in game over, exit loop
                    isGameOver = True

                # detect when a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # key pressed is up key, move up
                    if event.key == pygame.K_UP:
                        direction = 1
                    # key pressed is down key, move down
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # detect when a key is released
                elif event.type == pygame.KEYUP:
                    # stop movement
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            # Draw the screen and background
            self.gameScreen.fill(WHITE_COLOR)
            self.gameScreen.blit(self.image, (0,0))

            # Render treausre
            treasure.draw(self.gameScreen)
            
            # Update player position
            playerCharacter.move(direction, self.height)
            # Draw the player
            playerCharacter.draw(self.gameScreen)

            # Update enemy position
            enemy0.move(self.width)
            # Draw the enemy
            enemy0.draw(self.gameScreen)

            if level > 1.5:
                # Update enemy position
                enemy1.move(self.width)
                # Draw the enemy
                enemy1.draw(self.gameScreen)
            if level > 2.5:
                # Update enemy position
                enemy2.move(self.width)
                # Draw the enemy
                enemy2.draw(self.gameScreen)

            # Detect collision with enemy or treasure
            if playerCharacter.detectCollision(enemy0):
                isGameOver = True
                didWin = False
                # Run lose logic and display caption
                caption = font.render('YOU DIED', True, BLACK_COLOR)
                self.gameScreen.blit(caption, (225, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif playerCharacter.detectCollision(enemy1):
                isGameOver = True
                didWin = False
                # Run lose logic and display caption
                caption = font.render('YOU DIED', True, BLACK_COLOR)
                self.gameScreen.blit(caption, (225, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif playerCharacter.detectCollision(enemy2):
                isGameOver = True
                didWin = False
                # Run lose logic and display caption
                caption = font.render('YOU DIED', True, BLACK_COLOR)
                self.gameScreen.blit(caption, (225, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif playerCharacter.detectCollision(treasure):
                isGameOver = True
                didWin = True
                # Run win logic and display caption
                caption = font.render('YOU WIN', True, BLACK_COLOR)
                self.gameScreen.blit(caption, (225, 350))
                pygame.display.update()
                clock.tick(1)
                break
            
            pygame.display.update() # update the display each frame
            clock.tick(self.TICK_RATE) # tick clock to update the game

        # Either run the game again if won or quit the game
        if didWin:
            self.runGame(level + 0.5)
        else:
            return

# ------------------------------------------------------------------Game Object Implementation-------------------------------------------------------------
class GameObject:
    def __init__(self, imagePath, x, y, width, height):
        objectImage = pygame.image.load(imagePath)
        # Scale image up
        self.image = pygame.transform.scale(objectImage, (width, height))
        
        self.xPos = x
        self.yPos = y

        self.width = width
        self.height = height

    # Draw object by blitting it onto the game screen
    def draw(self, background):
        background.blit(self.image, (self.xPos, self.yPos))



# --------------------------------------------------------------Player implementation---------------------------------------------------------------
class Player(GameObject):
    # Distance player will move per move
    SPEED = 10
    
    # Constructor for Player object
    def __init__(self, imagePath, x, y, width, height):
        super().__init__(imagePath, x, y, width, height)

    # Moving the player (based on Player's key presses)
    def move(self, direction, maxHeight):
        if direction > 0:
            self.yPos -= self.SPEED
        elif direction < 0:
            self.yPos += self.SPEED
        # Bounds checkings
        if self.yPos >= maxHeight - 40:
            self.yPos = maxHeight - 40

    # Detect if player hits enemy (game over)
    def detectCollision(self, otherEntity):
        # Check y position
        if self.yPos > otherEntity.yPos + otherEntity.height:
            return False
        elif self.yPos + self.height < otherEntity.yPos:
            return False
        
        # Check x position
        if self.xPos > otherEntity.xPos + otherEntity.width:
            return False
        elif self.xPos + self.width < otherEntity.xPos:
            return False
        
        return True

# -------------------------------------------------------------------Enemy implementation--------------------------------------------------------------
class Enemy(GameObject):
    # Distance enemy will move 
    SPEED = 5
    
  
    def __init__(self, imagePath, x, y, width, height):
        super().__init__(imagePath, x, y, width, height)

    # Moving the enemy
    # Includes bounds checking (enemy never goes off screen and will turn back once it reaches the end)
    def move(self, maxWidth):
        if self.xPos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.xPos >= maxWidth - 40:
            self.SPEED = -abs(self.SPEED)

        self.xPos += self.SPEED



# ----------------------------------------------------------------Utility----------------------------------------------------------------------------
pygame.init()



# Run the game
newGame = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
newGame.runGame(1)

   
# quit the program
pygame.quit()
quit()


 # gameScreen.blit(playerImage, (375, 375))

#playerImage = pygame.image.load('player.png')
#playerImage = pygame.transform.scale(playerImage, (60, 60))
