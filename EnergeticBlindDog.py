from aima.agents import *


class Food(Thing):
    pass


class Water(Thing):
    pass


class EnergeticBlindDog(Agent):
    location = [0, 1]
    direction = Direction("down")

    def moveforward(self, success=True):
        """moveforward possible only if success (i.e. valid destination location)"""
        if not success:
            return
        if self.direction.direction == Direction.R:
            self.location[0] += 1
        elif self.direction.direction == Direction.L:
            self.location[0] -= 1
        elif self.direction.direction == Direction.D:
            self.location[1] += 1
        elif self.direction.direction == Direction.U:
            self.location[1] -= 1

    def turn(self, d):
        self.direction = self.direction + d

    def eat(self, thing):
        """returns True upon success or False otherwise"""
        if isinstance(thing, Food):
            return True
        return False

    def drink(self, thing):
        """ returns True upon success or False otherwise"""
        if isinstance(thing, Water):
            return True
        return False


def program(percepts):
    """Returns an action based on it's percepts"""

    for p in percepts:  # first eat or drink - you're a dog!
        if isinstance(p, Food):
            return 'eat'
        elif isinstance(p, Water):
            return 'drink'
        if isinstance(p, Bump):  # then check if you are at an edge and have to turn
            choice = random.choice((1, 2))
        else:
            choice = random.choice((1, 2, 3, 4))  # 1-right, 2-left, others-forward
    if choice == 1:
        return 'turnright'
    elif choice == 2:
        return 'turnleft'
    else:
        return 'moveforward'


class Park2D(GraphicEnvironment):
    def percept(self, agent):
        """return a list of things that are in our agent's location"""
        things = self.list_things_at(agent.location)
        loc = copy.deepcopy(agent.location)  # find out the target location
        # Check if agent is about to bump into a wall
        if agent.direction.direction == Direction.R:
            loc[0] += 1
        elif agent.direction.direction == Direction.L:
            loc[0] -= 1
        elif agent.direction.direction == Direction.D:
            loc[1] += 1
        elif agent.direction.direction == Direction.U:
            loc[1] -= 1
        if not self.is_inbounds(loc):
            things.append(Bump())
        return things

    def execute_action(self, agent, action):
        """changes the state of the environment based on what the agent does."""
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
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]):
                    print('{} ate {} at location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])
        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]):
                    print('{} drank {} at location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])

    def is_done(self):
        """By default, we're done when we can't find a live agent,
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water"""
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        return dead_agents or no_edibles


park = Park2D(5, 5, color={'EnergeticBlindDog': (200, 0, 0), 'Water': (0, 200, 200), 'Food': (230, 115, 40)})
dog = EnergeticBlindDog(program)
dogfood = Food()
water = Water()
park.add_thing(dogfood, [1, 2])
park.add_thing(water, [0, 1])
morewater = Water()
morefood = Food()
park.add_thing(morewater, [2, 4])
park.add_thing(morefood, [4, 3])
park.add_thing(dog, [0, 0])
print("dog started at [0,0], facing down. Let's see if he found any food or water!")

park.run()
i = input('Press any key to exit')

# while True:
#     i = input('step')
#     park.update(delay=0)
#     park.step()
#     if i == 'x':
#         exit(0)
