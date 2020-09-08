class Cell:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.coordinate = (x, y)
        self.bomb = False
        self.flag = False
        self.last_cell = False
        self.visible = False
        self.cell_info = '0'

    @classmethod
    def create_from_dict(cls, data_dict):
        """Создает экземпляр класса из словаря."""
        cell_object = cls()
        for attr in data_dict:
            attr_value = tuple(data_dict.get(attr)) if attr == 'coordinate' else data_dict.get(attr)
            setattr(cell_object, attr, attr_value)
        return cell_object

    def get_perimeter(self):
        """Возвращает координаты периметра ячейки."""
        cell_perimeter = []
        for i_offset in range(-1, 2):
            for j_offset in range(-1, 2):
                cell_perimeter.append((self.x + i_offset, self.y + j_offset))
        return cell_perimeter

    def __repr__(self):
        return f'cell_{self.x}{self.y}'
