from typing import Optional

from django.core.validators import MinLengthValidator
from django.db import models

from skcode import parse_skcode, render_to_html


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    part_number = models.PositiveIntegerField(null=True, default=None, blank=True)
    board_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    anime_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    manga_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    club_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    body = models.TextField(null=False, validators=[MinLengthValidator(15)])
    topic_id = models.PositiveIntegerField(null=True, default=None, blank=True)
    topic_created = models.DateTimeField(null=True, default=None, blank=True)
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
                name="topic_created_must_exist_if_topic_id_exists"),
            models.CheckConstraint(check=models.Q(board_id__isnull=False, club_id__isnull=True, anime_id__isnull=True,
                                                  manga_id__isnull=True) | models.Q(board_id__isnull=True,
                                                                                    club_id__isnull=False,
                                                                                    anime_id__isnull=True,
                                                                                    manga_id__isnull=True) | models.Q(
                board_id__isnull=True, club_id__isnull=True, anime_id__isnull=False, manga_id__isnull=True) | models.Q(
                board_id__isnull=True, club_id__isnull=True, anime_id__isnull=True, manga_id__isnull=False),
                                   name="only_one_of_board_id_or_club_id_or_anime_id_or_manga_id_must_exist")
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

    @property
    def rendered(self):
        return render_to_html(parse_skcode(self.body))

    @property
    def created_time_string(self) -> str:
        return self.created.strftime("%c")

    @property
    def topic_created_time_string(self) -> Optional[str]:
        return self.topic_created and self.topic_created.strftime("%c")
