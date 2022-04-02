from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.news.models import News, Banner, Comment
from apps.cms.models import NewsCategory
from apps.course.models import Course, Teacher, CourseCategory
from apps.payinfo.models import PayInfo


class Command(BaseCommand):
    def handle(self, *args, **options):  # 处理命令的逻辑代码

        # 1.编辑组（管理文章、管理课程、管理评论、管理轮播图）
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(PayInfo),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGruop = Group.objects.create(name='编辑')  # 创建分组
        editGruop.permissions.set(edit_permissions)
        editGruop.save()
        self.stdout.write(self.style.SUCCESS('编辑分组创建完成！'))

        # 2.财务组（课程订单/付费咨询等）
        # 3.管理员组（编辑组+财务组）
        # 4.超级管理员
