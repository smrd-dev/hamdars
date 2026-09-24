from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.db import transaction

from .models import Schedule, Subject


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "weekly/",
                self.admin_site.admin_view(self.weekly_schedule),
                name="schedule_schedule_weekly",
            ),
        ]

        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return redirect("admin:schedule_schedule_weekly")

    def weekly_schedule(self, request):

        subjects = Subject.objects.all()

        days = [
            ("sat", "شنبه", 8),
            ("sun", "یکشنبه", 8),
            ("mon", "دوشنبه", 8),
            ("tue", "سه‌شنبه", 8),
            ("wed", "چهارشنبه", 8),
            ("thu", "پنجشنبه", 4),
        ]

        if request.method == "POST":

            with transaction.atomic():

                for day_code, day_name, period_count in days:

                    for period in range(1, period_count + 1):

                        field_name = f"{day_code}_{period}"
                        subject_id = request.POST.get(field_name)

                        schedule = Schedule.objects.filter(
                            day=day_code,
                            period=period
                        ).first()

                        if subject_id:

                            if schedule:
                                schedule.subject_id = subject_id
                                schedule.save()

                            else:
                                Schedule.objects.create(
                                    day=day_code,
                                    period=period,
                                    subject_id=subject_id
                                )

                        else:

                            if schedule:
                                schedule.delete()

            messages.success(
                request,
                "برنامه هفتگی با موفقیت ذخیره شد."
            )

            return redirect("admin:schedule_schedule_weekly")

        schedules = Schedule.objects.all()

        schedule_map = {
            (item.day, item.period): item.subject_id
            for item in schedules
        }

        grid = []

        for day_code, day_name, period_count in days:

            row = []

            for period in range(1, period_count + 1):

                selected_subject = schedule_map.get(
                    (day_code, period)
                )

                row.append({
                    "period": period,
                    "subject_id": selected_subject,
                })

            grid.append({
                "code": day_code,
                "name": day_name,
                "periods": row,
            })

        context = {
            **self.admin_site.each_context(request),
            "title": "برنامه هفتگی",
            "subjects": subjects,
            "grid": grid,
        }

        return render(
            request,
            "admin/schedule/schedule/weekly_schedule.html",
            context,
        )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass