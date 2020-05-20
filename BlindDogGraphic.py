from aima.agents import *


class Food(Thing):
    pass


class Water(Thing):
    pass


class Park2D(GraphicEnvironment):
    def percept(self, agent):
        """return a list of things that are in our agent's location"""
        things = self.list_things_at(agent.location)
        return things

    def execute_action(self, agent, action):
        """changes the state of the environment based on what the agent does."""
        if action == "move down":
            print('{} decided to {} at location: {}'.format(str(agent)[1:-1], action, agent.location))
            agent.movedown()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]):  # Have the dog eat the first item
                    print('{} ate {} at location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])  # Delete it from the Park after.
        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]):  # Have the dog drink the first item
                    print('{} drank {} at location: {}'
                          .format(str(agent)[1:-1], str(items[0])[1:-1], agent.location))
                    self.delete_thing(items[0])  # Delete it from the Park after.

    def is_done(self):
        """By default, we're done when we can't find a live agent,
        but to prevent killing our cute dog, we will stop before itself - when there is no more food or water"""
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        return dead_agents or no_edibles


class BlindDog(Agent):
    location = [0, 1]  # change location to a 2d value
    direction = Direction("down")  # variable to store the direction our dog is facing

    def movedown(self):
        self.location[1] += 1

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
    """Returns an action based on the dog's percepts"""
    for p in percepts:
        if isinstance(p, Food):
            return 'eat'
        elif isinstance(p, Water):
            return 'drink'
    return 'move down'


park = Park2D(5, 20, color={'BlindDog': (200, 0, 0), 'Water': (0, 200, 200),
                            'Food': (230, 115, 40)})  # park width is set to 5, and height to 20
dog = BlindDog(program)
dogfood = Food()
water = Water()

park.add_thing(dogfood, [0, 5])
park.add_thing(water, [0, 7])
morewater = Water()
park.add_thing(morewater, [0, 15])
park.add_thing(dog, [0, 1])

print("BlindDog starts at (1,1) facing downwards, lets see if he can find any food!")
park.run(20)

input('Press enter to exit')
