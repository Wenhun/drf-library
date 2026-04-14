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
        full_name = " ".join(
            part
            for part in [instance.first_name, instance.middle_name, instance.last_name]
            if part
        )
        return {"full_name": full_name}


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorNameSerializer(read_only=True, many=False)

    class Meta:
        model = model.Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorNameSerializer(read_only=True, many=False)

    class Meta:
        model = model.Book
        fields = ("id", "title", "author", "inventory", "daily_fee")
