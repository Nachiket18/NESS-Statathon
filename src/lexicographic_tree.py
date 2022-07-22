class LexicoNode:
    def __init__(self, data: list, children: dict):
        self.data = data
        self.children = children

    def has_children(self):
        return len(self.children) > 0

    def add_node(self, edge, node):
        self.children[edge] = node

    def print_out(self, depth=0):
        def _indent(x):
            return "\t" * x

        print(_indent(depth), self.data)

        if self.has_children():
            for i in self.children:
                print("\n", _indent(depth + 1), "---", i)
                self.children[i].print_out(depth + 1)

    def _trav(self, targ_col: int, level: int = 0):
        if level >= targ_col:
            return self.data
        elif level < targ_col:
            items = [x._trav(targ_col, level + 1) for x in self.children.values()]
            return [i for flat_l in items for i in flat_l] #flattens list

    def nodes_at_level(self, col: int):
        return self._trav(col - 1)


if __name__ == "__main__":
    lex = LexicoNode([2, 3, 5, 20], {0: LexicoNode([69], {})})

    # lex2 = LexicoNode()

    lex.add_node(4, LexicoNode([10, 23, 34], {1: LexicoNode([50], {})}))
    lex.add_node(6, LexicoNode([10, 21, 34], {1: LexicoNode([50], {})}))
    print(lex.__dict__)

    print(lex.print_out())

    print(lex.nodes_at_level(1))

    # lex = LexicographicTree()

    # lex.addVertex(10)

    # print(lex.__dict__)
