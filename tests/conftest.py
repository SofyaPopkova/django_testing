import pytest
import pytest_django
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('students.Course', **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)

    return factory
