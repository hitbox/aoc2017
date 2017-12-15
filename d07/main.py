import os
import re
import textwrap

class Tower:

    def __init__(self):
        self.bottom = None

    def parse(self, inputstr):
        tower = {}
        weights = {}
        line_re = re.compile("(?P<name>[a-z]+) \((?P<weight>\d+)\)(?: \-> )?(?P<holding>.*)")
        for line in inputstr.splitlines():
            match = line_re.match(line)
            groups = match.groups()
            name, weight, holding = groups
            weight = int(weight)
            if holding:
                holding = holding.split(", ")
                tower[name] = holding
            weights[name] = weight
        self.tower = tower
        self.weights = weights
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
            total = sum(self.get_program_weights(name))
            yield (name, weight, total)

    def find_balanced_weight(self):
        totals = {}
        for name, weight, total in self._iter_weighted():
            if total not in totals:
                totals[total] = 0
            totals[total] += 1
        assert len(totals) == 2, totals
        for total, count in totals.items():
            if count > 1:
                return total

    def get_program_weights(self, start):
        # left off here, want this to yield "flat"
        yield self.weights[start]
        if start in self.tower:
            for holding in self.tower[start]:
                yield self.weights[holding]
                if holding in self.tower and self.tower[holding]:
                    for weight in self.get_program_weights(holding):
                        yield weight

    def find_corrected_weight(self):
        balanced_weight = self.find_balanced_weight()
        for name, weight, total in self._iter_weighted():
            holding = self.tower[name]
            if holding:
                print("holding: %s" % (holding, ))
                subweight = sum(sum(self.get_program_weights(name)) for name in holding)
            else:
                subweight = 0
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

    # test with recursive
    inputstr = "".join(textwrap.dedent("""\
                pbga (66)
                xhth (57)
                ebii (61)
                havc (66)
                ktlj (57) -> qoyq
                fwft (72) -> ktlj, cntj, xhth
                qoyq (66)
                padx (45) -> pbga, havc, qoyq
                tknk (41) -> ugml, padx, fwft
                jptl (61)
                ugml (68) -> gyxo, ebii, jptl
                gyxo (61)
                cntj (57)"""))
    # fwft (72) + ktlj (57) + qoyq (66) + cntj (57) + xhth (57) == 309

    print("\n\n\n")
    tower = Tower()
    tower.parse(inputstr)
    for name in tower.tower:
        if name == tower.bottom:
            continue
        weight = tower.weights[name]
        print("name: %s" % name)
        holding = tower.tower[name]
        if holding:
            subweights = [list(tower.get_program_weights(name)) for name in holding]
            print("subweights: %s" % (",".join(map(str, subweights))))
        else:
            subweights = []
        print("%s sum: %s" % (name, weight + sum()))
        print()

def main():
    tests()

    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    tower = Tower()
    tower.parse(open(input_path).read())

    print("part 1: %s" % tower.bottom)
    #print("part 2: %s" % tower.find_corrected_weight())

if __name__ == "__main__":
    main()
