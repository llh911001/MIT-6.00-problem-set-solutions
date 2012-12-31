# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import pylab
import ps11_visualize

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned_tiles = set()
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x, y = int(pos.getX()), int(pos.getY())
        self.cleaned_tiles.add((x, y))
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m, n) in self.cleaned_tiles
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned_tiles)
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        rand_x = round(random.uniform(0, self.width), 1)
        rand_y = round(random.uniform(0, self.height), 1)
        return Position(rand_x, rand_y)
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        return 0 <= pos.getX() <= self.width and 0 <= pos.getY() <= self.height


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.p = self.room.getRandomPosition()
        self.d = random.randrange(0, 360)
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.p = position
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        current_p = self.getRobotPosition()
        self.room.cleanTileAtPosition(current_p)
        new_p = current_p.getNewPosition(self.getRobotDirection(), self.speed)
        while not self.room.isPositionInRoom(new_p):
            self.setRobotDirection(random.randrange(0, 360))
            new_p = current_p.getNewPosition(self.getRobotDirection(), self.speed)
        self.setRobotPosition(new_p)


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    all_trials_progress_list = []

    for i in range(num_trials):
        if visualize:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        robots = [robot_type(room, speed) for i in range(num_robots)]
        progress_list = []
        cleaned_percentage = 0.0
        while cleaned_percentage < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
                if visualize:
                    anim.update(room, robots)
                cleaned_percentage = float(room.getNumCleanedTiles())/float(room.getNumTiles())
                progress_list.append(cleaned_percentage)
        if visualize:
            anim.done()
        all_trials_progress_list.append(progress_list)

    return all_trials_progress_list

runSimulation(2, 1.0, 5, 5, 0.8, 10, Robot, True)

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    print tots
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4

def get_average_time(list_of_lists):
    inner_list_lens = [len(l) for l in list_of_lists]
    return sum(inner_list_lens)/len(list_of_lists)

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    # linear ascending
    rooms = [(5, 5), (10, 10), (15, 15), (20, 20), (25, 25)]
    X = [w*h for w, h in rooms]
    Y = []
    for width, height in rooms:
        lol = runSimulation(2, 1.0, width, height, 0.75, 25, Robot, False)
        Y.append(get_average_time(lol))
    pylab.plot(X, Y)
    pylab.xlabel('Room area')
    pylab.ylabel('Timesteps')
    pylab.title('Time to clean 75% of a square room with 2 robots, for various room areas')
    pylab.savefig('plot1.png')

    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # constant
    X = range(1, 11)
    Y = []
    for nb in X:
        lol = runSimulation(nb, 1.0, 25, 25, 0.75, 25, Robot, False)
        Y.append(get_average_time(lol))
    pylab.plot(X, Y)
    pylab.xlabel('Number of robots')
    pylab.ylabel('Timesteps')
    pylab.xticks(range(0, 11))
    pylab.yticks([0, 500, 1000, 1500])
    pylab.title('Time to clean 75% of a 25*25 room with various robots, from 1 to 10')
    pylab.savefig('plot2.png')

    pylab.show()

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # ascending
    rooms = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    X = [20, 25, 40, 50, 80, 100]
    Y = []
    for width, height in rooms:
        lol = runSimulation(2, 1.0, width, height, 0.75, 25, Robot, False)
        Y.append(get_average_time(lol))
    pylab.plot(X, Y)
    pylab.xlabel('Room shape')
    pylab.ylabel('Timesteps')
    pylab.xticks([0]+X, ['0', '20x20', '25x16', '40x10', '50x8', '80x5', '100x4'])
    pylab.yticks([0, 500, 1000, 1500])
    pylab.title('Time to clean 75% of a room of area 400 with 2 robots, for various room shapes')
    pylab.savefig('plot3.png')

    pylab.show()

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # ascending, overlaps
    coverages = pylab.np.linspace(0.1, 1.0, 10)
    for nb, color in [(1, 'blue'), (2, 'red'), (3, 'green'), (4, 'yellow'), (5, 'black')]:
        Y = []
        for coverage in coverages:
            lol = runSimulation(nb, 1.0, 25, 25, coverage, 25, Robot, False)
            Y.append(get_average_time(lol))
        pylab.plot(coverages, Y, color=color, label='%d robots' % nb)
    pylab.xlabel('Percentage cleaned')
    pylab.ylabel('Timesteps')
    pylab.xticks(pylab.np.linspace(0, 1.0, 11))
    pylab.title('Time to clean various percentages of certain room, for each of 1-5 robots')
    pylab.legend(loc='upper left')
    pylab.savefig('plot4.png')

    pylab.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        current_p = self.getRobotPosition()
        self.room.cleanTileAtPosition(current_p)
        self.setRobotDirection(random.randrange(0, 360)) # after every time step, it chooses a new random direction
        new_p = current_p.getNewPosition(self.getRobotDirection(), self.speed)
        while not self.room.isPositionInRoom(new_p):
            self.setRobotDirection(random.randrange(0, 360))
            new_p = current_p.getNewPosition(self.getRobotDirection(), self.speed)
        self.setRobotPosition(new_p)

#runSimulation(2, 1.0, 5, 5, 0.8, 10, RandomWalkRobot, True)

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    num_robots = 1 # because we already know num_robots does not matter time steps
    speed = 1.0
    width, height = 25, 25
    coverages = pylab.np.linspace(0.1, 1.0, 10)
    num_trials = 25
    for robot, bot_name, color in [(Robot, 'Robot', 'blue'), (RandomWalkRobot,'RandomWalkRobot', 'red')]:
        Y = []
        for coverage in coverages:
            lol = runSimulation(num_robots, speed, width, height, coverage, num_trials, robot, False)
            Y.append(get_average_time(lol))
        pylab.plot(coverages, Y, color=color, label=bot_name)
    pylab.xlabel('Percentage cleaned')
    pylab.ylabel('Timesteps')
    pylab.xticks(pylab.np.linspace(0, 1.0, 11))
    pylab.title('Time to clean various percentages of certain room, for each of Robot and RandomWalkRobot')
    pylab.legend(loc='upper left')
    pylab.savefig('plot5.png')

    pylab.show()
