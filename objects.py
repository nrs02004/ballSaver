import pygame
import itertools
import math

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

    ''' Takes in a ball, and outputs a list of [normalized x, normalized y, normalized x_vel, normalized y_vel] '''
    def create_norm_dat_from_ball(self, ball):
        return [ball.x / self.x_r_lm, ball.y/self.y_t_lim, ball.x_vel/self.x_r_lim, ball.y_vel/self.y_t_lim]
    
    ''' Takes in a vector of [normalized x, normalized y, normalized x_vel, normalized y_vel, radius], and outputs a ball'''
    def create_ball_from_norm_dat(self, norm_x, norm_y, norm_x_vel, norm_y_vel, radius):
        return Ball(norm_x * self.x_r_lm, norm_y * self.y_t_lim, norm_x_vel * self.x_r_lm, norm_y_vel * self.y_t_lim, radius)
    
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

    ''' checks if balls collide, and if so reflects balls off their orthogonal separating plane '''
    def ball_on_ball(self, ball1, ball2, dt):
        diff_x = ball1.x - ball2.x
        diff_y = ball1.y - ball2.y
        dist = math.sqrt(pow(diff_x,2) + pow(diff_y,2))
        if dist < ball1.radius + ball2.radius:
            norm_diff_x = diff_x/dist; norm_diff_y = diff_y/dist
            coll_vel1 = ball1.x_vel * norm_diff_x + ball1.y_vel * norm_diff_y
            coll_vel2 = (ball2.x_vel * norm_diff_x + ball2.y_vel * norm_diff_y)
            ball1.take_step(-dt); ball2.take_step(-dt)
            ball1.x_vel -= 2*coll_vel1*norm_diff_x; ball1.y_vel -= 2*coll_vel1*norm_diff_y
            ball2.x_vel -= 2*coll_vel2*norm_diff_x; ball2.y_vel -= 2*coll_vel2*norm_diff_y
    
    def get_balls_from_server(self):
        balls = []
        ''' NEED TO WRITE *get_ball_dat_from_server*   
        ball_dat = get_ball_dat_from_server()
        for dat in ball_dat:
            balls.append(create_ball_from_norm_dat(dat.x, dat.y, dat.x_vel, dat.y_vel, dat.radius))
        '''
        return balls

    def pass_balls_to_server(self, balls):
        ball_dat = []
        for ball in balls:
            ball_dat.append(create_norm_dat_from_ball(ball))
        ''' NEED TO WRITE *pass_ball_dat_to_server*
        pass_ball_dat_to_server()
        '''
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
            self.ball_on_ball(ball1, ball2, dt)
        
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

