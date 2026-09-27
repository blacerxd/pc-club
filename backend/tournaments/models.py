from django.db import models
from django.utils.translation import gettext_lazy as _

class Tournament(models.Model):
    class FormatChoices(models.TextChoices):
        SINGLE_ELIM = 'single_elimination', _('Single Elimination')
        DOUBLE_ELIM = 'double_elimination', _('Double Elimination')
        ROUND_ROBIN = 'round_robin', _('Round Robin')
        SWISS = 'swiss', _('Swiss')

    class StatusChoices(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        REGISTRATION = 'registration_open', _('Registration Open')
        ONGOING = 'ongoing', _('Ongoing')
        FINISHED = 'finished', _('Finished')
        CANCELLED = 'cancelled', _('Cancelled')

    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tournaments',
        help_text="Оставьте пустым, если турнир общий или онлайн"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    game = models.ForeignKey('catalog.Game', on_delete=models.PROTECT, related_name='tournaments')

    description = models.TextField(blank=True)
    banner = models.URLField(max_length=255, null=True, blank=True)

    format = models.CharField(max_length=20, choices=FormatChoices.choices, default=FormatChoices.SINGLE_ELIM)
    team_size = models.PositiveIntegerField(default=1, help_text="1 для соло-турниров")
    max_participants = models.PositiveIntegerField()

    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    prize_pool = models.CharField(max_length=255, blank=True, help_text="Например: 100 000 руб. или 5000 бонусов")
    status = models.CharField(max_length=25, choices=StatusChoices.choices, default=StatusChoices.DRAFT)

    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='created_tournaments')

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.URLField(max_length=255, null=True, blank=True)
    captain = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='captained_teams')

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    class RoleChoices(models.TextChoices):
        CAPTAIN = 'captain', _('Captain')
        MEMBER = 'member', _('Member')

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=15, choices=RoleChoices.choices, default=RoleChoices.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команд"
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user} в {self.team.name} ({self.get_role_display()})"


class TournamentParticipant(models.Model):
    class StatusChoices(models.TextChoices):
        REGISTERED = 'registered', _('Registered')
        CHECKED_IN = 'checked_in', _('Checked In')
        ELIMINATED = 'eliminated', _('Eliminated')
        WINNER = 'winner', _('Winner')
        DISQUALIFIED = 'disqualified', _('Disqualified')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, help_text="Для соло-участия")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, help_text="Для командного участия")

    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.REGISTERED)
    seed = models.PositiveIntegerField(null=True, blank=True, help_text="Позиция в сетке")

    class Meta:
        verbose_name = "Участник турнира"
        verbose_name_plural = "Участники турниров"

    def __str__(self):
        participant = self.team.name if self.team else self.user
        return f"{participant} — {self.tournament.title}"


class Match(models.Model):
    class StatusChoices(models.TextChoices):
        SCHEDULED = 'scheduled', _('Scheduled')
        ONGOING = 'ongoing', _('Ongoing')
        FINISHED = 'finished', _('Finished')

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    round_number = models.PositiveIntegerField(help_text="Номер раунда (например, 1 - 1/8 финала, 2 - 1/4 и т.д.)")

    participant1 = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='matches_as_p1')
    participant2 = models.ForeignKey(
        TournamentParticipant,
        on_delete=models.CASCADE,
        related_name='matches_as_p2',
        null=True,
        blank=True,
        help_text="Оставьте пустым, если это техническая победа (bye)"
    )

    winner = models.ForeignKey(TournamentParticipant, on_delete=models.CASCADE, related_name='matches_won', null=True, blank=True)
    score = models.CharField(max_length=50, blank=True, help_text="Счет, например '2:1' или '16:14'")

    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.SCHEDULED)

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"

    def __str__(self):
        p2 = self.participant2 if self.participant2 else "BYE"
        return f"{self.participant1} vs {p2} (Раунд {self.round_number})"
