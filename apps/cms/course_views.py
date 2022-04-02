from django.shortcuts import render
from apps.course.models import Course, CourseCategory, Teacher
from .forms import CourseForm
from django.views.generic import View
from utils import restful
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


@method_decorator(permission_required(perm='course.change_course', login_url='/'), name='dispatch')
class PubCourse(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all(),
        }
        return render(request, 'cms/pub_course.html', context)

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')
            Course.objects.create(title=title, category=CourseCategory(id=category_id), video_url=video_url,
                                  cover_url=cover_url, price=price, duration=duration, profile=profile,
                                  teacher=Teacher(id=teacher_id))
            return restful.OK()
        else:
            return restful.params_errors(message=form.get_errors())
