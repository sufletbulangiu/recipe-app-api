"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe, 
    Tag,
    Ingredient,
)

class IngredientSerializer(serializers.ModelSerializer):
    """Ingredients for recipe."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for receipe."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handling getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
    
    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handling getting or creating ingredients as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredients_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredients_obj)

    
    def create(self, validate_data):
        """Create a receipe."""
        #print(f'Before: {validate_data}')
        tags = validate_data.pop('tags', [])
        ingredients = validate_data.pop('ingredients', [])
        #print(f'After: {tags}')
        recipe = Recipe.objects.create(**validate_data)
        self._get_or_create_tags(tags,  recipe)
        self._get_or_create_ingredients(ingredients,  recipe)
        return recipe

    
    def update(self, instance, validate_data):
        """Update receipe."""
        tags = validate_data.pop('tags', None)
        ingredients = validate_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validate_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']