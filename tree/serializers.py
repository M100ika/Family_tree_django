from rest_framework import serializers
from .models import Person
from datetime import datetime

class PersonSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    spouse = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ('photo',)

    def get_parents(self, obj):
        return [{'id': parent.id, 'first_name': parent.first_name, 'last_name': parent.last_name} 
                for parent in obj.parents.all()]

    def get_children(self, obj):
        return [{'id': child.id, 'first_name': child.first_name, 'last_name': child.last_name} 
                for child in obj.children.all()]

    def get_spouse(self, obj):
        if obj.spouse:
            return {'id': obj.spouse.id, 'first_name': obj.spouse.first_name, 'last_name': obj.spouse.last_name}
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Преобразуем даты в формат ISO
        if data.get('date_of_birth'):
            data['date_of_birth'] = instance.date_of_birth.isoformat()
        if data.get('date_of_death'):
            data['date_of_death'] = instance.date_of_death.isoformat()
        return data

    def to_internal_value(self, data):
        # Создаем копию данных для обработки
        data_copy = data.copy()
        
        # Преобразуем строковые даты в объекты datetime
        if 'date_of_birth' in data_copy and data_copy['date_of_birth']:
            try:
                data_copy['date_of_birth'] = datetime.strptime(data_copy['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError({'date_of_birth': 'Неверный формат даты'})
        
        if 'date_of_death' in data_copy and data_copy['date_of_death']:
            try:
                data_copy['date_of_death'] = datetime.strptime(data_copy['date_of_death'], '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError({'date_of_death': 'Неверный формат даты'})
        elif 'date_of_death' in data_copy:
            # Если date_of_death пустой или null, устанавливаем его как None
            data_copy['date_of_death'] = None
        
        # Обрабатываем пустые строки как пустые строки
        for field in ['middle_name', 'place_of_birth', 'place_of_death', 'biography', 
                     'personal_page', 'email', 'phone', 'address', 'occupation', 'education']:
            if field in data_copy and data_copy[field] is None:
                data_copy[field] = ''
        
        return super().to_internal_value(data_copy)

    def validate(self, data):
        """
        Проверка данных перед сохранением
        """
        # Проверяем, что дата смерти не раньше даты рождения
        if data.get('date_of_death') and data.get('date_of_birth'):
            if data['date_of_death'] < data['date_of_birth']:
                raise serializers.ValidationError({
                    'date_of_death': 'Дата смерти не может быть раньше даты рождения'
                })

        # Проверяем, что дата рождения не в будущем
        if data.get('date_of_birth'):
            today = datetime.now().date()
            if data['date_of_birth'] > today:
                raise serializers.ValidationError({
                    'date_of_birth': 'Дата рождения не может быть в будущем'
                })

        # Проверяем email, если он указан
        if data.get('email') and data['email']:
            if not '@' in data['email'] or not '.' in data['email']:
                raise serializers.ValidationError({
                    'email': 'Некорректный формат email'
                })

        # Проверяем URL персональной страницы, если он указан
        if data.get('personal_page') and data['personal_page']:
            if not data['personal_page'].startswith(('http://', 'https://')):
                raise serializers.ValidationError({
                    'personal_page': 'URL должен начинаться с http:// или https://'
                })

        return data 