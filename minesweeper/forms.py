from django import forms


CHOICES = [
    ('easy', 'Beginner'),
    ('medium', 'Skilled'),
    ('hard', 'Expert'),
    ('custom', 'Custom'),
]


class DifficultyForm(forms.Form):
    difficulty = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=CHOICES,
        initial='medium',
    )
    rows = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 20,
            'class': 'field_input',
        }),
    )
    columns = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 30,
            'class': 'field_input',
        }),
    )
    bombs = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 145,
            'class': 'field_input',
        }),
    )

    def clean_rows(self):
        rows = self.cleaned_data['rows']
        if rows.isdigit():
            rows = int(rows)
            if rows < 9:
                rows = 9
            elif rows > 25:
                rows = 25
        else:
            rows = 20
        return rows

    def clean_columns(self):
        columns = self.cleaned_data['columns']
        if columns.isdigit():
            columns = int(columns)
            if columns < 9:
                columns = 9
            elif columns > 50:
                columns = 50
        else:
            columns = 30
        return columns

    def clean(self):
        cleaned_data = super().clean()
        rows, cols, bombs = map(lambda x: cleaned_data.get(x), ['rows', 'columns', 'bombs'])
        bombs = int(bombs) if bombs.isdigit() else 145
        if bombs < 1:
            bombs = 1
        elif bombs > rows * cols:
            bombs = rows * cols // 2
        cleaned_data.update({'bombs': bombs})
        return cleaned_data
