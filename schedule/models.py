from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(max_length=10)

    def __str__(self):
        return self.subject_name


class Schedule(models.Model):
    day = models.CharField(max_length=10, choices=[
            ('sat', 'شنبه'),
            ('sun', 'یکشنبه'),
            ('mon', 'دوشنبه'),
            ('tue', 'سه شنبه'),
            ('wed', 'چهارشنبه'),
            ('thu', 'پنجشنبه'),
            ('fri', 'جمعه'),
        ]
        )
    period = models.PositiveIntegerField(choices=[
            (1, 'زنگ ۱'),
            (2, 'زنگ ۲'),
            (3, 'زنگ ۳'),
            (4, 'زنگ ۴'),
            (5, 'زنگ ۵'),
            (6, 'زنگ ۶'),
            (7, 'زنگ ۷'),
            (8, 'زنگ ۸'),
        ])

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
