from django.shortcuts import render
from django.views.generic.base import View
from minesweeper.forms import DifficultyForm
from minesweeper.funcs import get_session_key
from minesweeper.func_classes import (Field,
                                      Game)


class MainPageView(View):
    form_class = DifficultyForm
    template_name = 'minesweeper.html'

    def get(self, request):
        session_key = get_session_key(request)
        game_data = request.session.get(f'game_{session_key}')
        if game_data:
            game = Game.create_from_dict(game_data)
        else:
            game = Game()
            game.start_game()
            request.session[f'game_{session_key}'] = game.save_to_dict()
        return render(request, self.template_name, {'game': game, 'form': self.form_class()})

    def post(self, request):
        session_key = get_session_key(request)
        game_data = request.session.get(f'game_{session_key}')
        game = Game.create_from_dict(game_data)
        if request.POST.get('new_game'):
            difficulty = request.POST.get('difficulty')
            game = Game(difficulty)
            if difficulty == 'custom':
                form = DifficultyForm(request.POST)
                form.is_valid()
                diff_data = map(lambda x: form.cleaned_data.get(x), ['rows', 'columns', 'bombs'])
                Field.set_optional_difficulty(*diff_data)
            game.start_game()
        elif request.POST.get('end_game'):
            if game.difficulty == 'custom':
                diff_data = (*game.field.field_size, game.field.bomb_amount)
                Field.set_optional_difficulty(*diff_data)
            game.start_game()
        else:
            open_cell = request.POST.get('open_cell')
            flag_cell = request.POST.get('flag_cell')
            coordinate, option = (open_cell, 'open') if open_cell else (flag_cell, 'flag')
            coordinate = tuple(map(int, coordinate.split(',')))
            game.make_move(coordinate, option)
        request.session[f'game_{session_key}'] = game.save_to_dict()
        return render(request, self.template_name, {'game': game, 'form': self.form_class()})
