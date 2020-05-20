from aima.agents import *


class Suciedad(Thing):
    pass


class Aspiradora(Agent):
    location = [0, 0]

    direction = Direction('right')

    def moveforward(self, success=True):
        if not success:
            return
        if self.direction.direction == Direction.R:
            self.location[0] += 1
        elif self.direction.direction == Direction.L:
            self.location[0] -= 1

    def turn(self, d):
        self.direction = Direction(d)

    def aspirar(self, thing):
        if isinstance(thing, Suciedad):
            return True
        return False


def program(percepts):
    for p in percepts:
        if isinstance(p, Suciedad):
            return 'aspirar'
        if isinstance(p, Bump):
            return random.choice(('turnright', 'turnleft'))

    return 'moveforward'


class World(GraphicEnvironment):
    def percept(self, agent):
        things = self.list_things_at(agent.location)

        loc = copy.deepcopy(agent.location)

        if agent.direction.direction == Direction.R:
            print(loc)
            loc[0] += 1
        elif agent.direction.direction == Direction.L:
            print(loc)
            loc[0] -= 1

        if not self.is_inbounds(loc):
            things.append(Bump())

        return things

    def execute_action(self, agent, action):
        if action == 'turnright':
            print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
            agent.turn(Direction.R)
        elif action == 'turnleft':
            print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
            agent.turn(Direction.L)
        elif action == 'moveforward':
            print('{} decided to move {}wards at location: {}'.format(str(agent)[1:-1], agent.direction.direction,
                                                                      agent.location))
            agent.moveforward()
        elif action == 'aspirar':
            items = self.list_things_at(agent.location, tclass=Suciedad)

            if len(items) != 0:
                if agent.aspirar(items[0]):
                    print('{} aspira {} at location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))

                    self.delete_thing(items[0])

    def is_done(self):
        """By default, we're done when we can't find a live agent,
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water"""
        no_edibles = not any(isinstance(thing, Suciedad) for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        return dead_agents or no_edibles


world = World(4, 4, color={'Suciedad': (230, 115, 40), 'Aspiradora': (200, 0, 0)})
aspiradora = Aspiradora(program)
s1 = Suciedad()
s2 = Suciedad()

world.add_thing(s1, [1, 0])
world.add_thing(s2, [2, 0])
world.add_thing(aspiradora, [0, 0])

world.run()

input('Press any key to exit')
