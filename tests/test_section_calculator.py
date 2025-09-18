
import pytest
from typing import List
from dataTransferObjects.SectionData import SectionDTO , SegmentDTO, Point, ResultsDTO
from services.SectionCalculator import GrossSectionCalculator

def results_dto_equal(a, b):
    from dataclasses import asdict
    a_dict = asdict(a)
    b_dict = asdict(b)
    for key in a_dict:
        if isinstance(a_dict[key], float):
            if not a_dict[key] == pytest.approx(b_dict[key]):
                return False
        elif hasattr(a_dict[key], '__dict__'):
            # For nested dataclasses like Point
            if not results_dto_equal(a_dict[key], b_dict[key]):
                return False
        else:
            if a_dict[key] != b_dict[key]:
                return False
    return True

def test_it_calculate_a_section():
    points:list[Point] = []
    points.append(Point(0,0))
    points.append(Point(0,10))

    thickness = float(4);

    section = SectionDTO()
    segment = SegmentDTO(points[0], points[1], thickness)
    section.add_segment(segment)

    result = GrossSectionCalculator.calculate(section)

    inertia_y = 4*(10)**3 /12

    expected_result = ResultsDTO(float(40), Point(float(0), float(5)), inertia_y, float(0))

    print(result.centroid.y)

    assert results_dto_equal(result, expected_result)