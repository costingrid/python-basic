"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import datetime
import pytest
from task_classes import Teacher, Student, Homework


def test_homework_is_active():
    homework = Homework('text', 1)
    assert homework.is_active() is True

    homework = Homework('text', 0)
    assert homework.is_active() is False


def test_student_do_homework():
    student = Student('Ivan', 'Ivanov')
    homework = Homework('text', 1)
    assert student.do_homework(homework) == homework

    homework = Homework('text', 0)
    assert student.do_homework(homework) is None


def test_teacher_create_homework():
    teacher = Teacher('Ivan', 'Ivanov')
    homework = teacher.create_homework('text', 1)
    assert isinstance(homework, Homework)
    assert homework.text == 'text'
    assert homework.days == 1
    assert homework.deadline == datetime.timedelta(days=1)
    assert homework.created.date() == datetime.datetime.now().date()


def test_homework_negative_days():
    with pytest.raises(ValueError):
        Homework('text', -1)
    with pytest.raises(ValueError):
        Teacher.create_homework('text', -1)


