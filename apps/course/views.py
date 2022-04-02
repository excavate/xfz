from django.shortcuts import render
from .models import Course
from utils import restful
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


@permission_required(perm='course.add_course', login_url='/')
def course_index(request):
    context = {
        'courses': Course.objects.all(),
    }
    return render(request, 'course/course_index.html', context=context)


@permission_required(perm='course.add_course', login_url='/')
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        context = {
            'course': course,
        }
        return render(request, 'course/course_detail.html', context=context)
    except Course.DoesNotExist:
        return restful.params_errors(message='没有该课程！')


@permission_required(perm='course.add_course', login_url='/')
def course_order(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        context = {
            'course': course
        }
        return render(request, 'course/course_order.html', context=context)
    except Course.DoesNotExist:
        return restful.params_errors(message='没有该课程！')
