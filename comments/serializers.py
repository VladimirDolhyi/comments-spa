from rest_framework import serializers
from captcha.models import CaptchaStore

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

    captcha_key = serializers.CharField(write_only=True, required=True)
    captcha_value = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def get_replies(self, obj):

        replies = obj.replies.all()

        return CommentSerializer(replies, many=True, context=self.context).data

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")

        if request and request.method == "GET":
            fields.pop("captcha_key", None)
            fields.pop("captcha_value", None)

        return fields

    def validate(self, data):

        captcha_key = data.pop("captcha_key")
        captcha_value = data.pop("captcha_value")

        captcha = CaptchaStore.objects.filter(
            hashkey=captcha_key,
            response=captcha_value.lower()
        ).first()

        if not captcha:
            raise serializers.ValidationError({
                "captcha": "Invalid captcha"
            })

        captcha.delete()

        return data

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


class PreviewSerializer(serializers.Serializer):
    text = serializers.CharField()

    def validate_text(self, value):

        cleaned = clean_comment_text(value)

        validate_xhtml(cleaned)

        return cleaned
