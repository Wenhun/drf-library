from rest_framework import serializers

import library.models as model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Author
        fields = ("id", "first_name", "last_name", "middle_name")


class AuthorNameSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = model.Author
        fields = ("full_name",)

    def to_representation(self, instance):
        return " ".join(
            part
            for part in [instance.first_name, instance.middle_name, instance.last_name]
            if part
        )


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorNameSerializer(read_only=True, many=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=model.Author.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = model.Book
        fields = (
            "id",
            "title",
            "author",
            "author_ids",
            "cover",
            "inventory",
            "daily_fee",
        )

    def create(self, validated_data):
        authors = validated_data.pop("author_ids")
        book = model.Book.objects.create(**validated_data)
        book.author.set(authors)
        return book


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorNameSerializer(read_only=True, many=True)

    class Meta:
        model = model.Book
        fields = ("id", "title", "author", "inventory", "daily_fee")
