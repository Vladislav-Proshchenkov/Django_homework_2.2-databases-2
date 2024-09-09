from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scopes


class ScopesInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            # form.cleaned_data
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            if 'tag' not in form.cleaned_data:
                raise ValidationError('Нет тега')

            print(form.cleaned_data)
            if form.cleaned_data['is_main'] == True:
                count += 1
            print('count', count)
        if count == 0:
            raise ValidationError('Нет главного тега')
        if count > 1:
            raise ValidationError('У статьи может быть только один главный тег')


            # raise ValidationError('Тут всегда ошибка')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scopes
    formset = ScopesInlineFormset
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
