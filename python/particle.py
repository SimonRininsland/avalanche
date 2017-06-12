# Class for a single Particle
# a Particle always has a position, velocity and a mass

class particle():
    def __init__(self, position, velocity, mass):
        # every Particle has an own position
        self.position = position

        # and an own velocity
        self.velocity = velocity

        # and an own mass
        self.mass = mass

    # apply the Force
    def applyForce(self, force, dt):
        # old velocity added by the force given in dependence to Time gone and the mass
        self.velocity = self.velocity + force * (dt / self.mass)

    # new position has to be calculated
    def increment(self, dt):
        # new position is old position + velocity in dependence to the time gone
        self.position = self.position + self.velocity * dt

    # some function to combine two particles to one @todo
    def combine(self, other):
        '''
        newPos = (self.position + other.position) * 0.5
        newMass = self.mass + other.mass
        newVel = (self.velocity * self.mass + other.velocity * other.mass) * (1 / newMass)
        self.position = newPos
        self.mass = newMass
        self.velocity = newVel
        '''