import sys
from pathlib import Path

# Allow tests to import vision/src
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from intrusion import IntrusionDetector


def test_person_outside():
    detector = IntrusionDetector(boundary_y=350)

    point = (500, 200)

    assert detector.get_state(point) == "outside"


def test_person_inside():
    detector = IntrusionDetector(boundary_y=350)

    point = (500, 500)

    assert detector.get_state(point) == "inside"


def test_outside_to_inside_triggers_intrusion():
    detector = IntrusionDetector(boundary_y=350)

    track_id = 1

    detector.check_intrusion(
        track_id,
        (500, 200)
    )

    intrusion = detector.check_intrusion(
        track_id,
        (500, 500)
    )

    assert intrusion is True


def test_staying_inside_does_not_trigger_again():
    detector = IntrusionDetector(boundary_y=350)

    track_id = 1

    detector.check_intrusion(
        track_id,
        (500, 200)
    )

    detector.check_intrusion(
        track_id,
        (500, 500)
    )

    intrusion = detector.check_intrusion(
        track_id,
        (500, 520)
    )

    assert intrusion is False


def test_different_people_have_separate_states():
    detector = IntrusionDetector(boundary_y=350)

    detector.check_intrusion(
        1,
        (500, 200)
    )

    detector.check_intrusion(
        2,
        (700, 200)
    )

    intrusion_person_1 = detector.check_intrusion(
        1,
        (500, 500)
    )

    assert intrusion_person_1 is True
    assert detector.person_states[2] == "outside"