import sys, pygame

#Intializing Pygame window and colors
pygame.init()
pygame.font.init()
icon = pygame.image.load("Icon.PNG")
pygame.display.set_icon(icon)
pygame.display.set_caption("Dijkstra's algorithm - Maze Solver")
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
black = (0,0,0)
white = (255,255,255)
green = (0,94,0)
red = (255,0,0)
yellow = (255,255,0)
blue = (0,255,255)
purple = (247,11,216)
screen.fill(white)
font = pygame.font.SysFont('Times New Roman', 15)
font2 = pygame.font.SysFont('Times New Roman', 30)

#performs the shortest distance calulation using dijkstra's algorithm
def dijkstra(graph, start, end, grid):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = float("inf")
    path = []

    #goes through and sets every node to infinity except for our starting node which is set to 0
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
    
    #runs through entire graph until all nodes have been visited
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        
        #runs through graph marking the distances between each and every node by adding the previously visted nodes weight to the new weight   
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)
        grid.drawSpread(minNode)

    print(shortest_distance)

    #Back Tracks through the graph using each nodes predecssor in order to find the path from start to end
    currentNode = end
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path no reachable')
            break
    #Prints summary information about the path
    if shortest_distance[end] != infinity:
        print('Shortest Distance is ' + str(shortest_distance[end]))
        print('And the path is ' + str(path))
    
        return path


class Menu:
    def __init__(self, *args, **kwargs):
        self.startend = 0
        self.banner = 0
        self.wall = 0
        self.drop = 0
        self.start = 0
        self.clear = 0
        self.quit = 0
       
    def drawMenu(self, blocksize):
        blocksize = blocksize*2

        #Drawing banner 
        rect = pygame.Rect(0,650,1280,480)
        pygame.draw.rect(screen,white,rect,0)
        self.banner = rect

        #drawing startend icon
        textsurface = font.render('Pick Start/End Node', True, (0,0,0))
        screen.blit(textsurface,(0,height - 75))
        x = 1
        rect = pygame.Rect(x*blocksize,height - 50,blocksize,blocksize)
        pygame.draw.rect(screen,green,rect,0)

        self.startend = rect

        #Drawing Wall Icon
        x += 1
        textsurface = font.render('Draw Walls',True, (0,0,0))
        screen.blit(textsurface,(x*blocksize*2,height - 75))
        rect = pygame.Rect(x*blocksize * 2,height - 50, blocksize, blocksize)
        pygame.draw.rect(screen, blue,rect, 0 )
        self.wall = rect

        #Drawing Start Icon
        x += 2
        textsurface = font.render('Start Djikstra', True, (0,0,0))
        screen.blit(textsurface, (x*blocksize*2, height - 75))
        rect = pygame.Rect(x*blocksize * 2, height - 50,blocksize,blocksize)
        pygame.draw.rect(screen,purple,rect,0)
        self.start = rect
        
        #Drawing Clear Icon
        x += 3
        textsurface = font.render('Clear Screen', True, (0,0,0))
        screen.blit(textsurface, (x*blocksize*1.8, height - 75))
        rect = pygame.Rect(x*blocksize * 1.8, height - 50,blocksize,blocksize)
        rect = pygame.draw.rect(screen,yellow,rect,0)
        self.clear = rect

        #Drawing Exit Icon
        x += 4
        textsurface = font.render('Exit Program', True, (0,0,0))
        screen.blit(textsurface, (x*blocksize*1.55, height - 75))
        rect = pygame.Rect(x*blocksize * 1.55, height - 50,blocksize,blocksize)
        rect = pygame.draw.rect(screen,red,rect,0)
        self.quit = rect
        pygame.display.update()

    
    #Handles What Menu the user chose
    def getInput(self,grid):
        done = True
        WallPos = []
        click = False
        start = 0
        end = 0
        check = 1
        while done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()

                    #User Inputs for Starting and Ending Node
                    if self.startend.collidepoint(mousePos) == True:
                        if (start != None and end != None):
                            grid.clearstart(start, end)
                        waiting = True
                        color = green
                        count = 0
                        Pos = []
                        start = 0
                        end = 0
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    check = grid.placeNode(color, 10)
                                    if check == 1:
                                        Pos.append(grid.arrayPos)
                                        count = count + 1
                                        color = red
                                if count == 2:
                                    waiting = False
                        start = Pos[0]
                        end = Pos[1]

                    #User Inputs for drawing barriers
                    elif self.wall.collidepoint(mousePos) == True:
                        waiting = True
                        check = []
                        textsurface = font2.render('Press Enter to Stop Drawing Walls', True,(255,0,0))
                        screen.blit(textsurface,(width * 0.6,height - 75))
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN or click == True:
                                    click = True
                                    grid.placeWall(blue,0)

                                    grid.boxArray.sort()
                                    
                                    i = 0
                                    stop = grid.boxArray.__len__()
                                    for num in WallPos:
                                        i = 0
                                        for i in range(grid.boxArray.__len__()):
                                            if grid.boxArray.__len__() == 0:
                                                break
                                            elif num == grid.boxArray[i]:
                                                grid.boxArray.remove(num)
                                                break
                                            i += 1
                                            
                                                 
                                    stop = grid.boxArray.__len__()
                                    for i in range (stop):
                                        if (grid.boxArray.__len__() != 0):
                                            WallPos.append(grid.boxArray[0])
                                            grid.boxArray.pop(0)
                                        i+= 1
                                    
                                    grid.boxArray.clear()
                                if event.type == pygame.MOUSEBUTTONUP:
                                    click = False
                        
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        waiting = False
                                        self.drawMenu(grid.blockSize) 
                    
                    #clear the screen
                    elif self.clear.collidepoint(mousePos) == True:
                        check = 0
                        WallPos = []
                        start = 0
                        end = 0
                        screen.fill(white)
                        grid.drawGrid()
                        self.drawMenu(grid.blockSize)
                        break

                    #Start Djikstra
                    elif self.start.collidepoint(mousePos) == True:
                        done = False
                        check = 1

                    #Close the Program
                    elif self.quit.collidepoint(mousePos) == True:
                        sys.exit()

        return (WallPos, start,end, check)

        
#Grid class handles drawing grid, placing nodes, and holding data about that grid
class Grid:

    def __init__(self, *args, **kwargs):
        self.rectArray = []
        self.arrayPos = 0
        self.blockSize = 20
        self.widthGrid = 0
        self.heightGrid = 0
        self.maxBlocks = 0
        self.spreadArray = []
        self.boxArray = []

    def drawGrid(self):
        self.rectArray.clear()
        for x in range(self.widthGrid):
            for y in range(self.heightGrid):
                rect = pygame.Rect(x*self.blockSize, y*self.blockSize, self.blockSize, self.blockSize)
                pygame.draw.rect(screen,black,rect,10)
                self.rectArray.append(rect)            

    def placeNode(self, color, thickness):
        mousePos = pygame.mouse.get_pos()
        self.arrayPos = 0
        for rect in self.rectArray:
            if rect.collidepoint(mousePos) == True:
                pygame.draw.rect(screen,color,rect,thickness)             
                pygame.display.update()
                return 1
            self.arrayPos += 1
            
        return 0

    def placeWall(self, color, thickness):
        mousePos = pygame.mouse.get_pos()
        rectMouse = pygame.Rect(mousePos[0] - self.blockSize / 2,mousePos[1] - self.blockSize / 2,self.blockSize,self.blockSize)
        
        i = 0
        for rect in self.rectArray:
            if rect.colliderect(rectMouse) == True:
                pygame.draw.rect(screen,color,rect,thickness)
                self.boxArray.append(i)
            i += 1

        pygame.display.update()
        return 0

    

    def drawPath(self, path):
        color = yellow
        for point in path:
            rect = self.rectArray[point]
            pygame.draw.rect(screen,color, rect, 5)
            pygame.display.update()

    def drawSpread(self, point):
        color = purple
        rect = self.rectArray[point]
        pygame.draw.rect(screen, color, rect, 1)
        self.spreadArray.append(rect)
        pygame.display.update()

    def clearstart(self,start,end):
        rect = self.rectArray[start]
        pygame.draw.rect(screen, black, rect, 10)
        rect = self.rectArray[end]
        pygame.draw.rect(screen,black,rect,10)



def driver():
    
    #Draws Grid
    grid = Grid()
    grid.widthGrid = int(width / grid.blockSize)
    grid.heightGrid = int((height / grid.blockSize) - 4)
    grid.maxBlocks = grid.widthGrid * grid.heightGrid
    grid.drawGrid()
    pygame.display.update()

    #Draws Menu
    menu = Menu()           
    menu.drawMenu(grid.blockSize)
    check = 0 

    while check == 0:
        WallPos, start, end, check = menu.getInput(grid)

    #Generating Graph structure of Grid for dijkstra calculation
    #accounting for topleft corner of graph
    WallPos.sort()


    weight = 1
    count = 0

    if WallPos.__len__() == 0:
        WallPos.append(40000)

    if (count == WallPos[0]):
        weight = 1000000000000
        WallPos.remove(count) 

    graph = {count:{count + grid.heightGrid:weight, count + 1:weight, (count +grid.heightGrid) + 1:(2*weight)}}
    weight = 1     
    count = 1
    for i in range(grid.rectArray.__len__() - 1):
    
        if (WallPos.__len__() != 0 and count == WallPos[0]):
            WallPos.remove(count)
            weight = 10000000000000

   
        #If grid is at bottom left corner
        if(count == (grid.heightGrid - 1)):
            graph[count] = {count + grid.heightGrid:weight, 
                            count - 1:weight, 
                            (count + grid.heightGrid) - 1:(2*weight)}

        #If grid is at top right corner
        elif(count == grid.maxBlocks - grid.heightGrid):
            graph[count] = {count + 1:weight, 
                            count - grid.heightGrid:weight, 
                            (count - grid.heightGrid) + 1:(2*weight)}

        #if grid is at bottom right corner
        elif(count == (grid.maxBlocks - 1)):
            graph[count] = {count - 1:weight,
                           count - grid.heightGrid:weight, 
                           (count - grid.heightGrid) - 1:(2*weight)}

        #if grid is between topleft and bottomleft
        elif(count > 0 and count < (grid.heightGrid - 1)):
                graph[count] = {count + grid.heightGrid:weight, 
                                count + 1:weight, 
                                count - 1:weight, 
                                (count + grid.heightGrid) + 1:(2 * weight), 
                                (count + grid.heightGrid) - 1:(2 * weight)}

        #if grid is between top right and bottom right
        elif(count > (grid.maxBlocks - grid.heightGrid) and count < (grid.maxBlocks - 1)):
                graph[count] = {count + 1:weight, 
                                count - 1:weight, 
                                count - grid.heightGrid:weight, 
                                (count - grid.heightGrid) - 1:(2*weight), 
                                (count - grid.heightGrid) + 1:(2*weight)}

        #if grid is between top left and top right
        elif((count % grid.heightGrid) == 0):
            graph[count] = {count + grid.heightGrid:weight, 
                            count + 1:weight, 
                            count - grid.heightGrid:weight, 
                            (count + grid.heightGrid) + 1:(2*weight), 
                            (count - grid.heightGrid) + 1:(2*weight)}

        #if grid is between bottom left and bottom right
        elif((count % grid.heightGrid) == (grid.heightGrid - 1)):
            graph[count] = {count + grid.heightGrid:weight, 
                            count - 1:weight, 
                            count - grid.heightGrid:weight, 
                            (count + grid.heightGrid) - 1:(2*weight), 
                            (count - grid.heightGrid) -1:(2*weight)}

        #graph is somewhere in the middle
        else:
            graph[count] = {count + grid.heightGrid:weight, 
                            count + 1:weight, count - 1:weight, 
                            count - grid.heightGrid:weight, 
                            (count + grid.heightGrid) + 1:(2*weight), 
                            (count - grid.heightGrid) + 1:(2*weight), 
                            (count + grid.heightGrid) - 1:(2*weight), 
                            (count - grid.heightGrid) - 1:(2*weight)}
        count += 1
        weight = 1
        i += 1

    #performing dijkstra calulation within given graph and start and end nodes
    path = dijkstra(graph, start, end, grid)

    #drawing path on grid
    grid.drawPath(path)

    waiting = True
    textsurface = font2.render('Press the Enter button to Start Over', True,(255,0,0))
    screen.blit(textsurface,(width * 0.6,height - 75))
    pygame.display.update()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False 
        
    screen.fill(white)
    driver()
        

#Starts the main driver program
driver()
