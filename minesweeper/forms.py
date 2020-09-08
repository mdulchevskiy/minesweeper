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
        rows = int(rows) if rows.isdigit() else 20
        return rows if rows >= 9 else 9

    def clean_columns(self):
        columns = self.cleaned_data['columns']
        columns = int(columns) if columns.isdigit() else 30
        return columns if columns >= 9 else 9

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
