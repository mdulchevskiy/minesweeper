from minesweeper.func_classes.class_field import Field


class Game:
    def __init__(self, difficulty='medium'):
        self.game_status = 'Created'
        self.difficulty = difficulty
        self.field = None

    @classmethod
    def create_from_dict(cls, data_dict):
        """Создает экземпляр класса из словаря."""
        game_object = cls()
        for attr in data_dict:
            attr_value = data_dict.get(attr)
            if attr == 'field':
                attr_value = Field.create_from_dict(data_dict['field'])
            setattr(game_object, attr, attr_value)
        return game_object

    def save_to_dict(self):
        """Создает словарь из объекта."""
        data_dict = self.__dict__
        data_dict.update({'field': data_dict['field'].save_to_dict()})
        data_dict.pop('_Field__field_dict', None)
        return data_dict

    def start_game(self):
        """Начинает игру."""
        self.game_status = 'Started'
        self.field = Field(self.difficulty)
        self.field.create_field()
        self.field.set_bombs()
        self.field.set_cells_info()

    def get_game_status(self):
        """Возвращает статус игры."""
        cells = self.field.field_dict.values()
        lose = sum([cell.visible for cell in cells if cell.bomb]) > 0
        win = all([cell.visible for cell in cells if not cell.bomb])
        status = 'Lose' if lose else ('Win' if win else 'Continue')
        return status

    def make_move(self, coordinate, move_type='open'):
        """Делает ход: открывает ячейку или помечает ее флагом."""
        move_dict = {
            'open': self.field.make_cells_visible,
            'flag': self.field.flag_cell,
        }
        move_func = move_dict.get(move_type)
        move_func(coordinate)
        self.game_status = self.get_game_status()
        if self.game_status == 'Win':
            self.field.flag_all_cells()
