from django.shortcuts import render

from .models import Schedule


def home(request):
    return render(request, "schedule/home.html")


def weekly_schedule(request):

    days = [
        ("sat", "شنبه", 8),
        ("sun", "یکشنبه", 8),
        ("mon", "دوشنبه", 8),
        ("tue", "سه‌شنبه", 8),
        ("wed", "چهارشنبه", 8),
        ("thu", "پنجشنبه", 4),
    ]

    schedules = Schedule.objects.select_related("subject")

    schedule_map = {
        (item.day, item.period): item.subject
        for item in schedules
    }

    grid = []

    for day_code, day_name, period_count in days:

        row = []

        for period in range(1, period_count + 1):

            subject = schedule_map.get(
                (day_code, period)
            )

            row.append({
                "period": period,
                "subject": subject,
            })

        grid.append({
            "code": day_code,
            "name": day_name,
            "periods": row,
        })

    context = {
        "grid": grid,
    }

    return render(
        request,
        "schedule/weekly_schedule.html",
        context,
    )