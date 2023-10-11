from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from main.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(name='TestCourse', description='TestCourseDescription')
        self.lesson = Lesson.objects.create(
            course=self.course,
            name='TestLesson',
            description='TestLessonDescription',
            video_url='https://youtube.com',
            owner=self.user,

        )

    def test_lesson_create(self):
        data = {
            "course": self.course.name,
            "name": "test",
            "description": "test",
            "video_url": "https://youtube.com",
            "owner": self.user.pk
        }
        response = self.client.post(
            reverse('courses:lesson_create'),
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "course": self.course.name,
                "name": "test",
                "description": "test",
                "preview": None,
                "video_url": self.lesson.video_url,
                "owner": self.user.pk
            }
        )

    def test_lesson_list(self):
        response = self.client.get(
            reverse('courses:lesson_list'),
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "course": self.course.name,
                        "name": self.lesson.name,
                        "description": self.lesson.description,
                        "preview": None,
                        "video_url": self.lesson.video_url,
                        "owner": self.user.pk
                    }
                ]
            }
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('education:lesson_get', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.name,
                "name": self.lesson.name,
                "description": self.lesson.description,
                "preview": None,
                "video_url": self.lesson.video_url,
                "owner": self.user.pk
            }
        )

    def test_lesson_update(self):
        data = {
            "course": self.course.name,
            "name": "test",
            "video_url": "https://youtube.com/test2/"
        }
        response = self.client.patch(
            reverse('education:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.name,
                "name": "TEST2",
                "description": self.lesson.description,
                "preview": None,
                "video_url": "https://youtube.com/test2/",
                "owner": self.user.pk
            }
        )

    def test_lesson_destroy(self):
        response = self.client.delete(
            reverse('courses:lesson_delete', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Lesson.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(name="TEST", description="TEST", owner=self.user)

        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscription.objects.create(**self.data)

    def test_create_subscription(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': True
        }

        response = self.client.post(
            reverse('education:subscription-list'),
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "is_subscribed": True,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_unsubscribe(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': False
        }

        response = self.client.patch(
            reverse('education:subscription-detail', kwargs={'id': self.subscription.pk}),
            data=data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            1
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.pk,
                "is_subscribed": False,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )
