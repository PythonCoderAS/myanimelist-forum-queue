from typing import Optional

from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    part_number = models.PositiveIntegerField(null=True, default=None)
    board_id = models.PositiveIntegerField(null=True, default=None)
    anime_id = models.PositiveIntegerField(null=True, default=None)
    manga_id = models.PositiveIntegerField(null=True, default=None)
    club_id = models.PositiveIntegerField(null=True, default=None)
    body = models.TextField(null=False, validators=[MinLengthValidator(15)])
    topic_id = models.PositiveIntegerField(null=True, default=None)
    topic_created = models.DateTimeField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(board_id__isnull=False) | models.Q(club_id__isnull=False) | models.Q(
                anime_id__isnull=False) | models.Q(manga_id__isnull=False),
                                   name='post_board_id_or_club_id_or_anime_id_or_manga_id_not_null'),
            models.CheckConstraint(check=models.Q(part_number__isnull=True) | models.Q(
                models.Q(anime_id__isnull=False) | models.Q(manga_id__isnull=False), part_number__isnull=False),
                                   name="anime_id_or_manga_id_must_exist_if_part_number_exists"),
            models.CheckConstraint(
                check=models.Q(topic_id__isnull=True, topic_created__isnull=True) | models.Q(topic_id__isnull=False,
                                                                                             topic_created__isnull=False),
                name="topic_created_must_exist_if_topic_id_exists")
        ]

    @property
    def topic_url(self) -> Optional[str]:
        return self.topic_id and f"https://myanimelist.net/forum/?topicid={self.topic_id}"

    @property
    def board_url(self) -> Optional[str]:
        return self.board_id and f"https://myanimelist.net/forum/?board={self.board_id}"

    @property
    def club_home(self) -> Optional[str]:
        return self.club_id and f"https://myanimelist.net/clubs.php?cid={self.club_id}"

    @property
    def club_url(self) -> Optional[str]:
        return self.club_id and f"https://myanimelist.net/forum/?clubid={self.club_id}"

    @property
    def anime_home(self) -> Optional[str]:
        return self.anime_id and f"https://myanimelist.net/anime/{self.anime_id}"

    @property
    def anime_url(self) -> Optional[str]:
        return self.anime_id and f"https://myanimelist.net/forum/?animeid={self.anime_id}"

    @property
    def manga_home(self) -> Optional[str]:
        return self.manga_id and f"https://myanimelist.net/manga/{self.manga_id}"

    @property
    def manga_url(self) -> Optional[str]:
        return self.manga_id and f"https://myanimelist.net/forum/?mangaid={self.manga_id}"

    @property
    def display_title(self) -> str:
        if self.part_number:
            if self.anime_id:
                return f"{self.title} Episode {self.part_number} Discussion"
            elif self.manga_id:
                return f"{self.title} Chapter {self.part_number} Discussion"
        return self.title
