from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Book, Section, Collaboration


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class SectionDetailSerializer(serializers.ModelSerializer):
    # Create a custom method to organize sections hierarchically in sub_sections
    sub_sections = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = '__all__'

    def get_sub_sections(self, obj):
        sub_sections = Section.objects.filter(parent_section=obj)
        serialized_sub_sections = SectionDetailSerializer(sub_sections, many=True).data
        return serialized_sub_sections

class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = '__all__'


class CollaborationBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = ['id', 'user', 'can_edit']

class CollaborationDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Collaboration
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Book
        fields = ['id', 'author', 'title']

class BookDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    collaborators = CollaborationBookSerializer(many=True, source='collaboration_set')
    
    # Create a custom method to organize sections hierarchically in sub_sections
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_sections(self, obj):
        def recursive_serialize(section):
            serialized_section = SectionSerializer(section).data
            sub_sections = Section.objects.filter(parent_section=section)
            if sub_sections:
                serialized_section['sub_section'] = [recursive_serialize(sub) for sub in sub_sections]
            return serialized_section

        root_sections = Section.objects.filter(book=obj, parent_section=None)
        serialized_sections = [recursive_serialize(section) for section in root_sections]
        return serialized_sections