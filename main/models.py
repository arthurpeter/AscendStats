from functools import lru_cache
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, date
from .predictor import ClimberGradePredictor
from django_countries.fields import CountryField
import calendar
from dateutil.relativedelta import relativedelta

class User(AbstractUser):
    # Add your custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, null=True, blank=True)
    country = CountryField(blank_label='(Select Country)', null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    ape_index = models.FloatField(null=True, blank=True)
    max_grade = models.IntegerField(null=True, blank=True)
    current_flash_grade = models.FloatField(null=True, blank=True)
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    level_up_xp = models.IntegerField(default=10)

    MAX_LEVEL = 100
    BASE_EXP = 10
    GROWTH_FACTOR = 2
    
    @classmethod
    @lru_cache(maxsize=1)  # Cache the result of this method
    def get_xp_per_level(cls):
        """
        Dynamically generates and caches the XP required for each level up to MAX_LEVEL.
        """
        return [
            int(cls.BASE_EXP + ((level ** cls.GROWTH_FACTOR) * 0.2))
            for level in range(1, cls.MAX_LEVEL)
        ]
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def calculate_experience(self):
        climb_grades = self.climb_set.filter(success=True).values_list("grade", flat=True)
        max_grade = self.max_grade or 0
        flash_grade = self.current_flash_grade or 0
        exponent = ((max(1, max_grade) + max(1, flash_grade)) / 2) ** 0.5

        return sum(x if x else 0.5 for x in climb_grades) * exponent

    def calculate_level(self):
        xp_per_level = self.get_xp_per_level()
        remaining_exp = self.calculate_experience()
        level = 1

        for xp_needed in xp_per_level:
            if remaining_exp >= xp_needed:
                level += 1
                remaining_exp -= xp_needed
            else:
                break

        self.level = min(level, self.MAX_LEVEL)
        self.experience_points = remaining_exp
        self.level_up_xp = 0 if level >= self.MAX_LEVEL else xp_per_level[level - 1]
        self.save()
    
    def calculate_flash_grade(self):
        one_month_ago = timezone.now() - timedelta(days=30)
        climbs = Climb.objects.filter(user=self, date__gte=one_month_ago).values("grade", "attempts", "success")
        data = list(climbs)
        # Handle the case where there are no climbs
        if not data:
            self.current_flash_grade = None
            self.save()
            return
        predictor = ClimberGradePredictor(data)
        climber_grade, m = predictor.predict_climber_grade()
        self.current_flash_grade = climber_grade
        self.save()

    def calculate_max_grade(self):
        climbs = Climb.objects.filter(user=self, success=True)
        self.max_grade = max([climb.grade for climb in climbs], default=None)
        self.save()
    
    def get_style_distribution(self):
        # Get the current time
        now = timezone.now()
        # Calculate the date one month ago
        one_month_ago = now - timedelta(days=30)

        climbs = Climb.objects.filter(
            user=self,
            style__isnull=False,
            date__gte=one_month_ago
        )
        styles = {'Balance': 0, 'Dynamic': 0, 'Powerful': 0, 'Technical': 0}
        for climb in climbs:
            if climb.style in styles:
                styles[climb.style] += 1
        return styles
    
    def calculate_preferred_style(self):
        styles = self.get_style_distribution()
        result = max(styles, key=styles.get, default=None)
        if sum(styles.values()) < 10:
            return None
        return result
    
    def get_max_grades_last_six_months(self):
        max_grades = []
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)

        for i in range(5, -1, -1):  # Loop through the past 6 months
            # Calculate the first and last day of the month
            first_day_of_month = first_day_of_current_month - relativedelta(months=i)
            last_day_of_month = first_day_of_month + relativedelta(day=31)  # Safely get the last day of the month

            # Make the dates timezone-aware
            first_day_of_month = timezone.make_aware(datetime.combine(first_day_of_month, datetime.min.time()))
            last_day_of_month = timezone.make_aware(datetime.combine(last_day_of_month, datetime.max.time()))

            # Filter climbs for the user in the current month
            climbs_in_month = Climb.objects.filter(
                user=self,
                success=True,
                date__gte=first_day_of_month,
                date__lte=last_day_of_month
            )

            # Get the max grade for the month or None if no climbs exist
            max_grade = climbs_in_month.aggregate(models.Max('grade'))['grade__max']
            max_grades.append(max_grade)

        return max_grades
    
    def get_success_rate(self, start_date=None):
        if start_date is None:
            start_date = timezone.now() - timedelta(days=30)

        climbs = Climb.objects.filter(user=self, date__gte=start_date)
        if not climbs.exists():
            return {}

        # Initialize a dictionary to store total attempts and successes per grade
        grade_stats = {}
        for climb in climbs:
            grade = f'V{climb.grade}'
            if grade not in grade_stats:
                grade_stats[grade] = {'attempts': 0, 'successes': 0}
            grade_stats[grade]['attempts'] += climb.attempts
            if climb.success:
                grade_stats[grade]['successes'] += 1

        # Calculate success rates for each grade
        success_rates = {}
        for grade, stats in grade_stats.items():
            success_rates[grade] = (stats['successes'] / stats['attempts']) * 100 if stats['attempts'] > 0 else 0

        # Sort success rates by grade numerically
        return dict(sorted(success_rates.items(), key=lambda x: int(x[0][1:])))
    
    def get_average_grade(self):
        # Get all climbs for the user
        climbs = Climb.objects.filter(user=self).order_by('date')
        if not climbs.exists():
            return {}  # No climbs exist for the user

        # Initialize a dictionary to store averages
        averages = {}

        # Group climbs by year and month
        for climb in climbs:
            month_year = climb.date.strftime('%B %Y')  # Format as 'Month Year'
            if month_year not in averages:
                averages[month_year] = {'total_grade': 0, 'count': 0}
            averages[month_year]['total_grade'] += climb.grade
            averages[month_year]['count'] += 1

        # Calculate the average grade for each month
        results = {
            month_year: round(data['total_grade'] / data['count'], 2)
            for month_year, data in averages.items()
        }

        return results
    
    def get_session_analysis(self):
        # Get the last 30 days of climbs
        climbs = Climb.objects.filter(user=self).order_by('date').filter(date__gte=timezone.now() - timedelta(days=30))
        if not climbs.exists():
            return {}
        
        # Get the climbs from the last session
        last_session_date = climbs.last().date
        climbs_last_session = climbs.filter(date__gte=last_session_date - timedelta(hours=6))

        # Calculate average grade and attempts for all climbs
        all_climbs_stats = climbs.filter(success=True).aggregate(
            total_grade=models.Sum('grade'),
            total_attempts=models.Sum('attempts'),
            count=models.Count('id')
        )
        average_grade = all_climbs_stats['total_grade'] / all_climbs_stats['count']
        average_attempts = all_climbs_stats['total_attempts'] / all_climbs_stats['count']

        # Calculate average grade and attempts for the last session
        last_session_stats = climbs_last_session.filter(success=True).aggregate(
            total_grade=models.Sum('grade'),
            total_attempts=models.Sum('attempts'),
            count=models.Count('id')
        )
        average_grade_last_session = last_session_stats['total_grade'] / last_session_stats['count']
        average_attempts_last_session = last_session_stats['total_attempts'] / last_session_stats['count']

        # Define thresholds for "similar" performance
        grade_threshold = 0.1 * average_grade  # Allowable difference in grades
        attempts_threshold = 0.1 * average_attempts  # Allowable difference in attempts

        # Generate analysis
        analysis = ""
        if abs(average_grade_last_session - average_grade) <= grade_threshold and abs(average_attempts_last_session - average_attempts) <= attempts_threshold:
            analysis = "You had a session very similar to your average. Keep up the consistent performance!"
        elif average_grade_last_session <= average_grade and average_attempts_last_session >= average_attempts:
            analysis = "You had a less successful session compared to your average. Consider taking a break or adjusting your training."
        elif average_grade_last_session < average_grade and average_attempts_last_session < average_attempts:
            analysis = "You had a good session with a lower average grade, but with fewer attempts. Keep pushing!"
        elif average_grade_last_session > average_grade and average_attempts_last_session > average_attempts:
            analysis = "You had a good session with a higher average grade, but more attempts. Great job!"
        elif average_grade_last_session >= average_grade and average_attempts_last_session <= average_attempts:
            analysis = "You had an amazing session with a higher average grade and fewer attempts. Remember not to overdo it!"
        elif abs(average_grade_last_session - average_grade) <= grade_threshold:
            analysis = "Your average grade this session was very close to your overall average. Great consistency!"
        elif abs(average_attempts_last_session - average_attempts) <= attempts_threshold:
            analysis = "Your average attempts this session were very close to your overall average. Keep it up!"

        return {
            'average_grade': average_grade,
            'average_attempts': average_attempts,
            'average_grade_last_session': average_grade_last_session,
            'average_attempts_last_session': average_attempts_last_session,
            'analysis': analysis
        }

    
class Climb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(17)], null=False)
    success = models.BooleanField(default=True, null=False)
    attempts = models.IntegerField(default=1, null=False)
    date = models.DateTimeField(null=False)
    style = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        elif timezone.is_naive(self.date):
            self.date = timezone.make_aware(self.date)
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Success" if self.success else "Fail"
        return f"V{self.grade} - {status} in {self.attempts} attempts - {self.date}"