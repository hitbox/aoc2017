import os

TEST = """\
0: 3
1: 2
4: 4
6: 4"""

TOP = 0

class Layer:

    def __init__(self, depth, range_):
        self.depth = depth
        self.range_ = range_
        self.scanner = TOP
        self.delta = 1

    def __repr__(self):
        return "<Layer(%s, %s, %s)>" % (self.depth, self.range_, self.scanner)

    def step(self):
        next_ = self.scanner + self.delta
        if next_ >= self.range_ or next_ < 0:
            self.delta *= -1
        self.scanner += self.delta

    def render(self, at_range):
        value = "   "
        if self.range_ == 0:
            if at_range == 0:
                value = "..."
        elif self.range_ > at_range:
            if self.scanner == at_range:
                value = "[S]"
            else:
                value = "[ ]"
        return value


class Firewall:

    def __init__(self, inputstr):
        self.state = self.parse(inputstr)

    def parse(self, inputstr):
        state = {}
        self.packet = None
        self._maxrange = 0
        for layer, line in enumerate(inputstr.splitlines()):
            depth, range_ = map(int, line.split(": "))
            state[depth] = Layer(depth, range_)
            if range_ > self._maxrange:
                self._maxrange = range_

        for layer in range(min(state), max(state)):
            if layer not in state:
                state[layer] = Layer(layer, 0)
        return state

    def step(self):
        self.step_packet()
        self.step_layers()

    def step_layers(self):
        for layer in self.state.values():
            layer.step()

    def step_packet(self):
        if self.packet is None:
            self.packet = 0
        else:
            self.packet += 1

    def is_caught(self):
        layer = self.state[self.packet]
        return layer.scanner == TOP

    def severity(self):
        caught = 0
        for _ in range(len(self.state)):
            self.step_packet()
            if self.is_caught():
                layer = self.state[self.packet]
                caught += layer.depth * layer.range_
            self.step_layers()
        return caught

    def render(self):
        lines = []
        names = sorted(self.state)
        lines.append(" ".join("{:^3}".format(name) for name in names))

        for range_ in range(self._maxrange):
            strs = []
            for name in names:
                layer = self.state[name]
                s = layer.render(range_)
                if range_ == 0 and self.packet == name:
                    s = "(%s)" % s[1]
                strs.append(s)
            lines.append(" ".join(strs))
        return "\n".join(lines)


def tests():
    firewall = Firewall(TEST)
    assert firewall.severity() == 24

def get_input():
    return open(os.path.join(os.path.dirname(__file__), "input.txt")).read().strip()

def main():
    tests()

    firewall = Firewall(get_input())
    print("part 1: %s" % (firewall.severity(), ))

if __name__ == "__main__":
    main()
