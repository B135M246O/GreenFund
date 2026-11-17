from datetime import datetime

import pytest


@pytest.fixture
def charity_project(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='Школьная аллея',
        description='Саженцы и ограждения для школьной аллеи',
        full_amount=1000000,
        create_date=datetime.now(),
    )


@pytest.fixture
def charity_project_cleanup(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='Чистый берег',
        description='Мешки, перчатки и вывоз мусора с берега',
        full_amount=5000000,
        create_date=datetime.now(),
    )


@pytest.fixture
def small_fully_charity_project(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='Городской парк',
        description='Восстановление городского парка',
        full_amount=100,
        fully_invested=True,
        close_date=datetime.strptime('2010-10-11T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.now(),
    )


@pytest.fixture
def charity_project_little_invested(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='Школьная аллея',
        description='Саженцы и ограждения для школьной аллеи',
        full_amount=1000000,
        invested_amount=100,
        create_date=datetime.now(),
    )


@pytest.fixture
def closed_charity_project(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='Школьная аллея',
        description='Саженцы и ограждения для школьной аллеи',
        full_amount=100,
        invested_amount=100,
        fully_invested=True,
        close_date=datetime.strptime('2010-10-11T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.now(),
    )


@pytest.fixture
def donation(freezer, mixer):
    freezer.move_to('2011-11-11')
    return mixer.blend(
        'app.models.donation.Donation',
        user_id=2,
        comment='На озеленение',
        full_amount=100,
        create_date=datetime.now(),
    )


@pytest.fixture
def another_donation(freezer, mixer):
    freezer.move_to('2012-12-12')
    return mixer.blend(
        'app.models.donation.Donation',
        user_id=1,
        comment='На уборку от администратора',
        full_amount=2000,
        create_date=datetime.now(),
    )
