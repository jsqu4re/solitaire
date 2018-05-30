import operator
import sys
import array

class Node:
    value = float(0)
    counts = int(0)

    def __init__(self, value, num_outputs):
        self.value = value
        self.intensity = [float(0.5)] * num_outputs

class Brain:
    min_value = float(0)
    max_value = float(100)

    counts = int(0)

    def __init__(self, num_outputs):
        self.num_outputs = num_outputs
        self.nodes = [Node(self.min_value, self.num_outputs), Node(self.max_value, self.num_outputs)]

    def sort(self):
        self.nodes.sort(key=operator.attrgetter('value'))

    def dump(self):
        self.sort()
        for node in self.nodes:
            print (str(node.value) + ": " + str(node.intensity) + " - " + str(node.counts))

    def categorize(self, input):
        self.counts += 1

        for node in self.nodes:
            if (node.value > input):
                node.counts += 1
                return node

        print( "FAIL" )
        return Node(0, self.num_outputs)

    def feedback(self, node, solution):
        for n in range(0, self.num_outputs):
            if (node.intensity[n] >= 0.5 and solution[n] > 0.5):
                node.intensity[n] += 1
                node.intensity[n] /= 2

            elif (node.intensity[n] <= 0.5 and solution[n] < 0.5):
                node.intensity[n] /= 2

            else:
                node.intensity[n] += 0.5
                node.intensity[n] /= 2

    def remove_unused_nodes(self):
        for node in self.nodes:
            if (node.counts == 0 and node.value != self.max_value and node.value != self.min_value):
                self.nodes.remove(node)

    def sleep(self):
        self.sort()

        self.remove_unused_nodes()

        self.dump()


        for n in range(0, len(self.nodes)):

            if (self.nodes[n].counts > 0): # Maybe use: self.counts / self.num_outputs
#                if (n == len(self.nodes) - 1):
#                    new_value = (self.nodes[n].value + self.nodes[n-1].value)/2
#                elif (n == 0):
#                    new_value = (self.nodes[n].value + self.min_value)/2
#                else:
                new_value = (self.nodes[n].value + self.nodes[n-1].value)/2

                if (new_value != self.nodes[n].value and new_value != self.nodes[n-1].value):
                    new_node = Node(new_value, self.num_outputs)
                    new_node.counts = self.nodes[n].counts
                    new_node.intensity = list(self.nodes[n].intensity)
                    self.nodes.append(new_node)


        # self.nodes[:] = [x for x in self.nodes if x.counts != 0]




        for node in self.nodes:
            node.counts = 0

        if (len(self.nodes) == 0):
            print ( "brain is done" )
            exit()
        
        self.nodes.sort(key=operator.attrgetter('value'))


## Main

def main():
    print ("start")
    brain = Brain(9)
    # Example: Map input to output
    for n in range (0, 100):

        print (" RUN : " + str(n))

        node = brain.categorize(2)
        brain.feedback(node, [0,0,0,0,0,0,0,0,1])

        node = brain.categorize(4)
        brain.feedback(node, [0,0,0,0,0,0,0,1,0])

        node = brain.categorize(7)
        brain.feedback(node, [0,0,0,0,0,0,1,0,1])

        node = brain.categorize(8)
        brain.feedback(node, [0,0,0,0,0,0,1,1,0])

        node = brain.categorize(6)
        brain.feedback(node, [0,0,0,0,0,0,1,0,0])

        brain.sleep()

    print ("done")


if __name__ == '__main__':
    sys.exit(main())
