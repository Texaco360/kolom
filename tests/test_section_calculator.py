from typing import List
from models.SectionData import SectionDTO , SegmentDTO, Point, GrossSectionCalculator, ResultsDTO

def test_it_calculate_a_section():
    points:list[Point] = []
    points.append(Point(0,0))
    points.append(Point(0,10))

    thickness = float(4);

    section = SectionDTO()
    segment = SegmentDTO(points[0], points[1], thickness)
    section.add_segment(segment)

    result = GrossSectionCalculator.calculate(section)

    expected_result = ResultsDTO
    result.centroid.y = float(0)
    result.centroid.z = float(5)
    result.inertia_y = (10/2)**2*10*4
    result.inertia_z = 0
    result.surface_area = 10*4

    print(result.centroid.y)
    assert result == expected_result