from rest_framework import serializers
from comments.models import Comment
from comments.validators import (
    validate_username,
    clean_comment_text,
    validate_text_file,
    validate_image,
    validate_xhtml
)
from comments.services import resize_image


class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_replies(self, obj):

        replies = obj.replies.all()

        return CommentSerializer(replies, many=True, context=self.context).data

    def validate_username(self, value):

        validate_username(value)

        return value

    def validate_text(self, value):

        cleaned = clean_comment_text(value)

        validate_xhtml(cleaned)

        return cleaned

    def validate_text_file(self, value):

        validate_text_file(value)

        return value

    def validate_image(self, value):

        validate_image(value)

        return value

    def create(self, validated_data):

        comment = super().create(validated_data)

        if comment.image:
            resize_image(comment.image)

        return comment
