from django.db import models


class Comment(models.Model):

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    username = models.CharField(max_length=255)
    email = models.EmailField()
    homepage = models.URLField(blank=True)

    text = models.TextField()

    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True
    )

    text_file = models.FileField(
        upload_to="files/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
