import os
import re
import textwrap

from pprint import pformat, pprint as pp

class Tower:

    def __init__(self):
        self.bottom = None
        self.tower = None
        self.weights = None

    def parse(self, inputstr):
        self.tower = {}
        self.weights = {}
        line_re = re.compile("(?P<name>[a-z]+) \((?P<weight>\d+)\)(?: \-> )?(?P<holding>.*)")
        for line in inputstr.splitlines():
            match = line_re.match(line)
            groups = match.groups()
            name, weight, holding = groups
            self.weights[name] = int(weight)
            if holding:
                holding = holding.split(", ")
                self.tower[name] = holding
        self.bottom = self._find_bottom()

    def _find_bottom(self):
        all_children = []
        for name, holding in self.tower.items():
            all_children.extend(holding)
        for name in self.tower:
            if name not in all_children:
                return name

    def _iter_weighted(self):
        totals = {}
        for name, _ in self.tower.items():
            if name == self.bottom:
                continue
            weight = self.weights[name]
            subweight = sum(self.get_program_weights(name))
            yield (name, weight, subweight)

    def get_program_weights(self, start):
        if start not in self.tower:
            return
        for holding in self.tower[start]:
            yield self.weights[holding]
            if holding in self.tower:
                yield from self.get_program_weights(holding)

    def find_balanced_weight(self):
        totals = {}
        for name, weight, subweight in self._iter_weighted():
            total = weight + subweight
            if total not in totals:
                totals[total] = 0
            totals[total] += 1
        assert len(totals) == 2, pformat(totals)
        for total, count in totals.items():
            if count > 1:
                return total

    def find_wrong_weight(self, root):
        for child in self.tower[root]:
            if child in self.tower:
                self.find_wrong_weight(child)
            else:
                print(child)
                subweights = list(self.get_program_weights(child))
                if len(set(subweights)) > 1:
                    print(subweights)

    def find_corrected_weight(self):
        balanced_weight = self.find_balanced_weight()
        for name, weight, subweight in self._iter_weighted():
            holding = self.tower[name]
            total = weight + subweight

            if total != balanced_weight:
                correction = balanced_weight - weight - subweight
                return weight + correction

def tests():
    inputstr = "".join(textwrap.dedent("""\
                pbga (66)
                xhth (57)
                ebii (61)
                havc (66)
                ktlj (57)
                fwft (72) -> ktlj, cntj, xhth
                qoyq (66)
                padx (45) -> pbga, havc, qoyq
                tknk (41) -> ugml, padx, fwft
                jptl (61)
                ugml (68) -> gyxo, ebii, jptl
                gyxo (61)
                cntj (57)"""))
    tower = Tower()
    tower.parse(inputstr)
    assert tower.bottom == "tknk"
    assert tower.find_corrected_weight() == 60

    # test with recursion
    inputstr = "".join(textwrap.dedent("""\
                pbga (66)
                xhth (57)
                ebii (61)
                havc (66)
                ktlj (57) -> qoyq
                fwft (72) -> ktlj, cntj, xhth
                qoyq (66) -> ebii
                padx (45) -> pbga, havc, qoyq
                tknk (41) -> ugml, padx, fwft
                jptl (61)
                ugml (68) -> gyxo, ebii, jptl
                gyxo (61)
                cntj (57)"""))
    # fwft (72) + [ktlj (57) + [qoyq (66) + ebii (61)]] + cntj (57) + xhth (57) == 370
    tower = Tower()
    tower.parse(inputstr)
    name = "fwft"
    assert tower.weights[name] + sum(tower.get_program_weights(name)) == 370

def main():
    tests()

    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    tower = Tower()
    tower.parse(open(input_path).read())

    print("part 1: %s" % tower.bottom)

    tower.find_wrong_weight(tower.bottom)
    #print("part 2: %s" % tower.find_corrected_weight())

if __name__ == "__main__":
    main()
