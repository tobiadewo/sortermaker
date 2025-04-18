import random


class SortingHandler:
    sorted_idx = []  # The indices of items that have been sorted using the algorithm
    parent_idx = []  # The indices of the items at the beginning of the algorithm
    selected_idx = []  # The indices of items that have been saved using record()
    tied_idx = []  # The indices of items that are tied

    current_round = 1  # The current round of sorting
    total_rounds = 0  # The total number of rounds required to sort all items

    comparisons = 0  # The number of times record() has been called
    selections = []  # List that records the choice taken (left, right or tie) each round

    # Indices used to traverse sorted_idx
    outer_idx = [0, 0]
    inner_idx = [0, 0]

    # Variable used to traverse selected_idx
    pointer = 0

    # Last round's values for undo()
    sorted_idx_prev = []
    parent_idx_prev = []
    selected_idx_prev = []
    tied_idx_prev = []
    outer_idx_prev = []
    inner_idx_prev = []
    pointer_prev = 0
    comparisons_prev = 0

    # Value changes when undo() is called to stop it from being called twice in a row
    undone = False

    def update(self):
        self.sorted_idx_prev = self.sorted_idx[:]
        self.selected_idx_prev = self.selected_idx[:]
        self.parent_idx_prev = self.parent_idx[:]
        self.tied_idx_prev = self.tied_idx[:]
        self.outer_idx_prev = self.outer_idx[:]
        self.inner_idx_prev = self.inner_idx[:]
        self.pointer_prev = self.pointer
        self.comparisons_prev = self.comparisons

        self.undone = False

    def undo(self):
        if self.selections:
            self.selections = self.selections[:-1]

        self.sorted_idx = self.sorted_idx_prev[:]
        self.selected_idx = self.selected_idx_prev[:]
        self.parent_idx = self.parent_idx_prev[:]
        self.tied_idx = self.tied_idx_prev[:]
        self.outer_idx = self.outer_idx_prev[:]
        self.inner_idx = self.inner_idx_prev[:]
        self.pointer = self.pointer_prev
        self.comparisons = self.comparisons_prev

        self.current_round -= 1

        self.undone = True


H = SortingHandler()

items = []


def initialize():
    I = len(items)

    if I < 2:
        print("You need at least two items to sort.")

    random.shuffle(items)

    H.sorted_idx = [list(range(I))]
    H.parent_idx = [-1]
    H.selected_idx = [0 for _ in range(I)]
    H.tied_idx = [-1 for _ in range(I)]

    idx = 0
    S = len(H.sorted_idx)
    while idx < S:
        parent = H.sorted_idx[idx]
        if len(parent) > 1:
            left, right = parent[: len(parent) // 2], parent[len(parent) // 2 :]

            H.sorted_idx.append(left[:])
            H.total_rounds += len(H.sorted_idx[-1])
            H.parent_idx.append(idx)

            H.sorted_idx.append(right[:])
            H.total_rounds += len(H.sorted_idx[-1])
            H.parent_idx.append(idx)

        S = len(H.sorted_idx)
        idx += 1

    H.outer_idx = [len(H.sorted_idx) - 2, len(H.sorted_idx) - 1]  # Outer idx
    H.inner_idx = [0, 0]  # Inner idx

    H.outer_idx_prev = H.outer_idx[:]
    H.inner_idx_prev = H.inner_idx[:]

    compare()


def compare():
    left_idx = H.sorted_idx[H.outer_idx[0]][H.inner_idx[0]]
    right_idx = H.sorted_idx[H.outer_idx[1]][H.inner_idx[1]]

    left = items[left_idx]
    right = items[right_idx]

    print(f"Round #{H.current_round} ({H.comparisons / H.total_rounds:.2%} completed)")
    print(f"{left} vs. {right}")
    choice = input("").lower()
    choose(choice)


def choose(command):
    # Undo
    if command == "u" and not H.undone and H.current_round != 1:
        H.undo()
        compare()
        return

    H.update()

    # Left option was chosen
    if command == "l":
        if len(H.selections) + 1 == H.current_round:
            H.selections.append("Left")

        record("l")
        while H.tied_idx[H.selected_idx[H.pointer - 1]] != -1:
            record("l")

    # Right option was chosen
    elif command == "r":
        if len(H.selections) + 1 == H.current_round:
            H.selections.append("Right")

        record("r")
        while H.tied_idx[H.selected_idx[H.pointer - 1]] != -1:
            record("r")

    # Tie between left and right options
    elif command == "t":
        if len(H.selections) + 1 == H.current_round:
            H.selections.append("Left")

        record("l")
        while H.tied_idx[H.selected_idx[H.pointer - 1]] != -1:
            record("l")

        H.tied_idx[H.selected_idx[H.pointer - 1]] = H.sorted_idx[H.outer_idx[1]][
            H.inner_idx[1]
        ]

        record("r")
        while H.tied_idx[H.selected_idx[H.pointer - 1]] != -1:
            record("r")

    # Invalid option
    else:
        print("Invalid option. (l/r/t/u)")
        compare()
        return

    ####################################################################################

    l_size = len(H.sorted_idx[H.outer_idx[0]])
    r_size = len(H.sorted_idx[H.outer_idx[1]])

    if H.inner_idx[0] < l_size and H.inner_idx[1] == r_size:
        while H.inner_idx[0] < l_size:
            record("l")
    elif H.inner_idx[0] == l_size and H.inner_idx[1] < r_size:
        while H.inner_idx[1] < r_size:
            record("r")

    ####################################################################################

    l_size = len(H.sorted_idx[H.outer_idx[0]])
    r_size = len(H.sorted_idx[H.outer_idx[1]])

    if H.inner_idx[0] == l_size and H.inner_idx[1] == r_size:
        for i in range(l_size + r_size):
            H.sorted_idx[H.parent_idx[H.outer_idx[0]]][i] = H.selected_idx[i]

        H.sorted_idx = H.sorted_idx[:-2]
        H.outer_idx = [o - 2 for o in H.outer_idx]
        H.inner_idx = [0, 0]
        H.pointer = 0

        if len(H.selected_idx) > len(H.sorted_idx):
            for i in range(len(H.sorted_idx)):
                H.selected_idx[i] = 0
        else:
            H.selected_idx = [0 for _ in H.sorted_idx]

    ####################################################################################

    if H.outer_idx[0] < 0:
        show_results()
    else:
        H.current_round += 1
        compare()


def record(command):
    if command == "l":
        H.selected_idx[H.pointer] = H.sorted_idx[H.outer_idx[0]][H.inner_idx[0]]
        H.inner_idx[0] += 1
    else:
        H.selected_idx[H.pointer] = H.sorted_idx[H.outer_idx[1]][H.inner_idx[1]]
        H.inner_idx[1] += 1

    H.pointer += 1
    H.comparisons += 1


def show_results():
    rank = 1
    tied = 1

    final_idx = H.sorted_idx[0][:]
    rankings = []
    ties = [t == -1 for t in H.tied_idx].count(False)

    for i in range(len(items)):
        item_index = final_idx[i]
        item_name = items[item_index]
        rankings.append((rank, item_name))

        if not ties:
            rank += 1
        elif item_index < len(items) - 1:
            if H.tied_idx[item_index] == final_idx[item_index + 1]:
                tied += 1
            else:
                rank += tied
                tied = 1
        else:
            rank += tied
            tied = 1

    print("Results: ")
    for r, i in rankings:
        print(f"{r}.\t{i}")


if __name__ == "__main__":
    initialize()
