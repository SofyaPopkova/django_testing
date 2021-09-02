import pytest
import pytest_django
from django.urls import reverse
from students.models import Student, Course
from rest_framework.status import *


@pytest.mark.django_db
def test_getting_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == course.id


@pytest.mark.django_db
def test_getting_courses_list(api_client, course_factory):
    course_1 = course_factory()
    course_2 = course_factory()
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == 2

    response_ids = {r["id"] for r in response_json}
    assert response_ids == {course_1.id, course_2.id}


@pytest.mark.django_db
def test_sorting_courses_by_id(api_client, course_factory):
    url = reverse('courses-list')
    course_1 = course_factory()
    course_2 = course_factory()
    course_3 = course_factory()
    response = api_client.get(url)
    sorted_coursers = {course_1.id, course_2.id, course_3.id}
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    response_ids = {r["id"] for r in response_json}
    assert response_ids == sorted_coursers


@pytest.mark.django_db
def test_sorting_courses_by_name(api_client, course_factory):
    url = reverse('courses-list')
    course_1 = course_factory(name='Python')
    course_2 = course_factory(name='Go')
    course_3 = course_factory(name='Javascript')
    response = api_client.get(url)
    sorted_courses = {course_3.name, course_2.name, course_1.name}
    assert response.status_code == HTTP_200_OK

    response_json = response.json()
    response_ids = {r["name"] for r in response_json}
    assert response_ids == sorted_courses


@pytest.mark.django_db
def test_posting_course(api_client):
    url = reverse('courses-list')
    payload = {
        "name": "HTML"
    }
    courses_count = Course.objects.count()
    response = api_client.post(url, payload, format="json")
    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() > courses_count


@pytest.mark.django_db
def test_updating_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    payload = {
        "name": "New Course"
    }
    response = api_client.patch(url, payload, format="json")
    response_json = response.json()
    expected_name = payload["name"]
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == expected_name


@pytest.mark.django_db
def test_deleting_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=(course.id,))
    response = api_client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
