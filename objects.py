import pygame
import itertools

class Ball:
    
    def __init__(self, _x = 10, _y = 10, _x_vel = 5, _y_vel = 5):
        self.x = _x
        self.y = _y
        self.radius = 5
        self.remove = False
        self.pass_to = 0
        self.x_vel = _x_vel
        self.y_vel = _y_vel
    
    ''' moves a ball back 1 time step, and then flips either the x or y velocity '''
    def reflect(self, dt, x_or_y):
        self.x -= self.x_vel * dt
        self.y -= self.y_vel * dt
        if x_or_y == "x":
            self.x_vel = - self.x_vel
        else:
            self.y_vel = -self.y_vel
    
    ''' steps forward one step '''
    def take_step(self, dt):
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

    def ball_on_ball(self, ball):
        diff_x = self.x - ball.x
        diff_y = self.y - ball.y
        dist = pow(diff_x,2) + pow(diff_y,2)
        if dist < pow(self.radius + ball.radius,2):
            return True
        else:
            return False


class World:
    
    def __init__(self, balls=None, _width = 100, _height = 100):
        self.l_neighbor=0
        self.r_neighbor=0
        self.t_neighbor=0
        self.b_neighbor=0
        self.x_l_lim = 0
        self.x_r_lim = _width
        self.y_b_lim = 0
        self.y_t_lim = _height
        self.balls = balls
    
    ''' Checks if a ball has collided with a wall '''
    def check_for_walls(self, ball):
        if ball.x <= self.x_l_lim:
            return "l"
        elif ball.x >= self.x_r_lim:
            return "r"
        elif ball.y >= self.y_t_lim:
            return "t"
        elif ball.y <= self.y_b_lim:
            return "b"
        else:
            return "c"
    
    ''' Checks if the side that the ball collided with is solid or not.
        Reflects if solid, and sets the ball to be passed to another world if not
    '''
    def update_collide(self, ball, collide, dt):
        if collide == "l":
            ball.pass_to = self.l_neighbor
            if self.l_neighbor == 0:
                ball.reflect(dt, "x")
            else:
                ball.remove = True
        if collide == "r":
            ball.pass_to = self.r_neighbor
            if self.r_neighbor == 0:
                ball.reflect(dt, "x")
            else:
                ball.remove = True
        if collide == "t":
            ball.pass_to = self.t_neighbor
            if self.t_neighbor == 0:
                ball.reflect(dt, "y")
            else:
                ball.remove = True
        if collide == "b":
            ball.pass_to = self.b_neighbor
            if self.b_neighbor == 0:
                ball.reflect(dt, "y")
            else:
                ball.remove = True

    def get_balls_from_server(self):
        return []

    def pass_balls_to_server(self, balls):
        return None
    
    def update(self, dt):
        ''' updating ball list from server '''
        new_balls = self.get_balls_from_server()
        self.balls[:] = self.balls + new_balls

        ''' updating each ball '''
        for ball in self.balls:
            ball.take_step(dt)
            collide = self.check_for_walls(ball)
            self.update_collide(ball, collide, dt)

        for ball1,ball2 in itertools.combinations(self.balls, r = 2):
            print ball1.ball_on_ball(ball2)
        
        ''' passing balls to remove to server and updating '''
        pass_balls = [ball for ball in self.balls if ball.remove]
        self.balls[:] = [ball for ball in self.balls if not ball.remove]
        self.pass_balls_to_server(pass_balls)

class Screen:
    
    def __init__(self, _width = 480, _height = 640, _thickness = 0):
        self.width = _width
        self.height = _height
        self.thickness = _thickness
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.disp = pygame.display.set_mode((self.width, self.height))

    def draw_stuff(self, balls):
        self.disp.fill(self.BLACK)
        for ball in balls:
            pygame.draw.circle(self.disp, self.WHITE, (int(ball.x),int(ball.y)), int(ball.radius), int(self.thickness))
        pygame.display.update()

