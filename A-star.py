import heapq

class Tag_Puzzle:
    def __init__(self, state, end_state, parent=None, move=None, depth=0):
        self.state = state # текущее состояние пазла
        self.end_state = end_state # конечное состояние пазла
        self.parent = parent # родительский узел
        self.move = move # движение плитки
        self.depth = depth # глубина узла
        self.cost = self.Manhattan_distance() + self.depth # вычисление стоимости узла
        
    def __lt__(self, other):
        #сравнение узлов при добавлении в очередь с приоритетом.
        return self.cost < other.cost

    # Проверка пазла на решаемость
    def check_solvability(self):
        count_inverse = 0
        size = len(self.state)
        pos_zero = self.state.index(0)
        row_zero = pos_zero // 4
        # Считаем кол-во инверсий
        for i in range(size):
            for j in range(i + 1, size):
                # инверсии - числа находящиеся правее и меньше проверяемого числа
                if self.state[i] > self.state[j] and self.state[j] != 0:
                    count_inverse += 1
        # Пазл решаемый, если кол-во инверсий четное и ноль находится на нечетной строке или кол-во инверсий нечетное и ноль находится на четной строке
        if (count_inverse % 2 == 0 and row_zero % 2 == 1) or (count_inverse % 2 == 1 and row_zero % 2 == 0):
            return True
        return False

    # Находим манхэттенские расстояния
    def Manhattan_distance(self):
        # Манхэттенское расстояние - путь от текущего положения до целевого
        manhattan_distance = 0
        for i in range(len(self.state)):
            if self.state[i] != 0:
                x1, y1 = i % 4, i // 4
                x2, y2 = self.end_state.index(self.state[i]) % 4, self.end_state.index(self.state[i]) // 4
                manhattan_distance += abs(x2 - x1) + abs(y2 - y1)
        return manhattan_distance

    # Алгоритм A*
    def a_star(self):
        size = int(len(self.state) ** 0.5)
        goal_state = list(range(1, size ** 2)) + [0]
        open_list = [self] # Открытый список, используемый для хранения узлов, которые нужно рассмотреть
        closed_list = set() # Закрытый список, используемый для хранения просмотренных узлов
        
        while open_list:
            current_node = heapq.heappop(open_list) # Извлекаем узел с наименьшей стоимостью
            if current_node.state == goal_state:  # Если достигнуто конечное состояние
                path = []
                while current_node.parent: # Восстанавливаем путь до начального состояния
                    path.append(current_node.move)
                    current_node = current_node.parent
                return path[::-1] # Возвращаем путь в обратном порядке
        
            closed_list.add(tuple(current_node.state)) # Добавляем текущее состояние в закрытый список
            moves = current_node.get_children() # Получаем возможные ходы из текущего состояния
            for move in moves:
                action, new_state, tile_number = move
                child = Tag_Puzzle(new_state, self.end_state, current_node, (tile_number, action), current_node.depth + 1)
                if tuple(child.state) in closed_list:  # Проверяем, не рассматривали ли мы это состояние ранее
                    continue
                heapq.heappush(open_list, child) # добавляем потомка в открытый список

        return None

    #Получение возможных ходов из текущего состояния пазла
    def get_children(self):
        children = []
        zero_index = self.state.index(0) #Находим позицию пустой клетки
        row, col = zero_index // 4, zero_index % 4 # Получаем координаты пустой клетки
        # Возможные варианты перемещения
        directions = {"влево": (0, 1), "вправо": (0, -1), "вверх": (1, 0), "вниз": (-1, 0)}
        
        for action, (dr, dc) in directions.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_index = new_row * 4 + new_col # Получаем индекс новой клетки после движения
                new_state = self.state[:] # Создаем копию текущего состояния
                # Двигаем плитку
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                # Добавляем ход и новое состояние в список потомков
                children.append((action, new_state, self.state[new_index]))

        return children

#Решение пазла
def solve_puzzle(input_state):
    #Конечное состояние плиток
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    puzzle = Tag_Puzzle(input_state, goal_state)

    # Проверка пазл на решаемость
    if not puzzle.check_solvability():
        return "Расположение не является не решаемым."
    else:
        solution = puzzle.a_star()
        steps = []
        # Вывод каждого шага
        for step, (tile, direction) in enumerate(solution, start=1):
            steps.append(f"Шаг {step}: Перемещаем {tile} {direction}")
        return "\n".join(steps)

input_state = list(map(int, input("Введите последовательность чисел через пробел: ").split()))
print(solve_puzzle(input_state))