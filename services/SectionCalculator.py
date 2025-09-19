
import math
from dataclasses import dataclass
from dataTransferObjects.SectionData import SectionDTO, SegmentDTO, Point, ResultsDTO

@dataclass
class SegmentResultsDTO:
    area: float
    centroid: Point
    inertia_yy: float
    inertia_zz: float

class GrossSectionCalculator:
    @staticmethod
    def calculate_segment(segment: SegmentDTO) -> SegmentResultsDTO:
        dy = segment.end_pt.y - segment.start_pt.y
        dz = segment.end_pt.z - segment.start_pt.z
        length = math.sqrt(dy**2 + dz**2)
        area = length * segment.thickness
        mid_y = (segment.start_pt.y + segment.end_pt.y) / 2
        mid_z = (segment.start_pt.z + segment.end_pt.z) / 2
        inertia_yy = (segment.start_pt.z**2 + segment.end_pt.z**2 + segment.start_pt.z * segment.end_pt.z) * area / 3
        inertia_zz = (segment.start_pt.y**2 + segment.end_pt.y**2 + segment.start_pt.y * segment.end_pt.y) * area / 3
        return SegmentResultsDTO(
            area=area,
            centroid=Point(y=mid_y, z=mid_z),
            inertia_yy=inertia_yy,
            inertia_zz=inertia_zz
        )
    @staticmethod
    def calculate(section: SectionDTO) -> ResultsDTO:
        area_sum:float = 0.0
        static_y:float = 0.0
        static_z:float = 0.0
        inertia_yy:float = 0.0
        inertia_zz:float = 0.0

        for segment in section.segments:
            dy = segment.end_pt.y - segment.start_pt.y
            dz = segment.end_pt.z - segment.start_pt.z
            length = math.sqrt(dy**2 + dz**2)
            area = length * segment.thickness
            mid_y = (segment.start_pt.y + segment.end_pt.y) / 2
            mid_z = (segment.start_pt.z + segment.end_pt.z) / 2

            area_sum += area
            static_y += area * mid_y
            static_z += area * mid_z

            inertia_yy += (segment.start_pt.z**2 + segment.end_pt.z**2 + segment.start_pt.z * segment.end_pt.z) * area / 3
            inertia_zz += (segment.start_pt.y**2 + segment.end_pt.y**2 + segment.start_pt.y * segment.end_pt.y) * area / 3

        centroid_y = static_y / area_sum
        centroid_z = static_z / area_sum
        inertia_y = inertia_yy - area_sum * centroid_z**2
        inertia_z = inertia_zz - area_sum * centroid_y**2

        return ResultsDTO(
            surface_area=area_sum,
            centroid=Point(y=centroid_y, z=centroid_z),
            inertia_y=inertia_y,
            inertia_z=inertia_z
        )
