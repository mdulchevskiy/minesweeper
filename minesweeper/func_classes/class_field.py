from itertools import product
from random import sample
from copy import deepcopy
from minesweeper.func_classes.class_cell import Cell


class Field:
    __difficulty_setup = {
        'easy': {'field_size': (9, 9), 'bomb_amount': 10},
        'medium': {'field_size': (16, 16), 'bomb_amount': 40},
        'hard': {'field_size': (16, 30), 'bomb_amount': 99},
        'custom': {'field_size': None, 'bomb_amount': None},
    }

    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.field_size = Field.__difficulty_setup[difficulty]['field_size']
        self.bomb_amount = Field.__difficulty_setup[difficulty]['bomb_amount']
        self.field = None
        self.__field_dict = {}

    @classmethod
    def set_optional_difficulty(cls, rows, cols, bombs):
        """Задает параметры для пользовательской сложности."""
        cls.__difficulty_setup.update({
            'custom': {'field_size': (rows, cols), 'bomb_amount': bombs},
        })

    @classmethod
    def create_from_dict(cls, data_dict):
        """Создает экземпляр класса из словаря."""
        field_object = cls()
        for attr in data_dict:
            attr_value = data_dict.get(attr)
            if attr == 'field':
                attr_value = [[Cell.create_from_dict(cell_dict) for cell_dict in line] for line in attr_value]
                field_dict = {cell.coordinate: cell for cell in sum(attr_value, [])}
                setattr(field_object, '_Field__field_dict', field_dict)
            setattr(field_object, attr, attr_value)
        return field_object

    def save_to_dict(self):
        """Создает словарь из объекта."""
        data_dict = self.__dict__
        data_dict.update({'field': [[cell.__dict__ for cell in line] for line in data_dict['field']]})
        data_dict.pop('_Field__field_dict', None)
        return data_dict

    def create_field(self):
        """Создает игровое поле, а также добавляет в словарь все созданные объекты класса Cell."""
        field = [[Cell(i, j) for j in range(self.field_size[1])] for i in range(self.field_size[0])]
        self.__field_dict.update({cell.coordinate: cell for cell in sum(field, [])})
        self.field = field

    @property
    def field_dict(self):
        """Возвращает словарь из всех созданных объектов класса Cell."""
        return self.__field_dict

    def set_bombs(self):
        """Расстанавливает бомбы на поле в случайном порядке."""
        potential_bombs = list(product(range(self.field_size[0]), range(self.field_size[1])))
        bomb_coordinates = sample(potential_bombs, k=self.bomb_amount)
        for cell in self.__field_dict.values():
            if cell.coordinate in bomb_coordinates:
                cell.bomb = True

    def set_cells_info(self):
        """Присваивает ячейкам информацию о количестве бомб в их периметре."""
        for cell in self.__field_dict.values():
            bombs_around = 0
            for coordinate in cell.get_perimeter():
                new_cell = self.__field_dict.get(coordinate)
                if new_cell and new_cell.bomb:
                    bombs_around += 1
            cell.cell_info = 'b' if cell.bomb else f'{bombs_around}'

    def flag_cell(self, coordinate):
        """Отмечает ячейку флагом."""
        cell = self.__field_dict.get(coordinate)
        cell.flag = True if not cell.flag else False

    def flag_all_cells(self):
        """Отмечает все ячейки с бомбами флагом."""
        for cell in self.__field_dict.values():
            if cell.bomb:
                cell.flag = True

    def make_cells_visible(self, coordinate):
        """Делает ячейку\область ячеек видимой в зависимости от их статуса."""
        cell = self.__field_dict.get(coordinate)
        cell.last_cell = True
        # Если была открыта ячейка с бомбой, то открываются все ячейки с бомбами.
        if cell.cell_info == 'b':
            cell.flag = False
            for cell in self.__field_dict.values():
                if cell.bomb and not cell.flag:
                    cell.visible = True
        # Если была открыта ячейка в периметре которой отсутствуют бомбы,
        # то открывается вся смежная область, в которой отсутствуют бомбы.
        elif cell.cell_info == '0':
            # Из координат формируется область в периметре которой отсутствуют бомбы.
            visible_coordinates = {coordinate}
            checked_coordinates = set()
            while True:
                coordinates = deepcopy(visible_coordinates)
                for coordinate in coordinates:
                    if coordinate not in checked_coordinates:
                        cell = self.__field_dict.get(coordinate)
                        perimeter = cell.get_perimeter()
                        for new_coordinate in perimeter:
                            new_cell = self.__field_dict.get(new_coordinate)
                            if new_cell and new_cell.cell_info == '0':
                                visible_coordinates.add(new_coordinate)
                        checked_coordinates.add(coordinate)
                if visible_coordinates == checked_coordinates:
                    break
            # Открываются ячейки из сформированной области, а также из ее периметра.
            for coordinate in visible_coordinates:
                cell = self.__field_dict.get(coordinate)
                cell.visible = True
                perimeter = cell.get_perimeter()
                for new_coordinate in perimeter:
                    new_cell = self.__field_dict.get(new_coordinate)
                    if new_cell:
                        new_cell.visible = True
        # Если была открыта ячейка в периметре которой присутствуют бомбы,
        # то открывается только выбранная ячейка.
        else:
            cell.visible = True
