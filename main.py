import csv
from dataclasses import dataclass
import manim as manim
from typing import Generator, TextIO


@dataclass
class Circle:
    origin: tuple[float, float]
    radius: float


CircleGroup = list[Circle]

CIRCLES_PER_GROUP = 4


def removeCsvComments(csvFile: TextIO) -> Generator:
    for row in csvFile:
        raw = row.split("#")[0].strip()
        if raw:
            yield raw


def loadCircleGroups(csvPath: str) -> CircleGroup:
    ungrouped_circles: list[Circle] = []
    with open(csvPath) as f:
        reader = csv.reader(removeCsvComments(f))
        for row in reader:
            assert len(row) == 3
            ungrouped_circles.append(
                Circle((float(row[0]), float(row[1])), float(row[2]))
            )

    assert len(ungrouped_circles) % CIRCLES_PER_GROUP == 0

    groups = []
    for i in range(0, len(ungrouped_circles), CIRCLES_PER_GROUP):
        group = []
        for j in range(CIRCLES_PER_GROUP):
            group.append(ungrouped_circles[i + j])
        groups.append(group)

    return groups


if __name__ == "__main__":
    print(loadCircleGroups("circles.csv"))


class DefaultTemplate(manim.Scene):
    def construct(self):
        min_x: float = all_circles[0][0].origin[0]
        max_x: float = 0
        min_y: float = all_circles[0][0].origin[1]
        max_y: float = 0
        for circle_group in all_circles:
            for circle in circle_group:
                [x, y] = circle.origin
                r = circle.radius
                if x - r < min_x:
                    min_x = x - r
                if x + r > max_x:
                    max_x = x + r
                if y - r < min_y:
                    min_y = y - r
                if y + r > max_y:
                    max_y = y + r

        scale = max(max_x - min_x, max_y - min_y)

        normalized_circles = []
        for circle_group in all_circles:
            normalized_group = []
            for circle in circle_group:
                [x, y, r] = circle
                normalized_group.append(
                    [(x - min_x) / scale, (y - min_y) / scale, r / scale]
                )
            normalized_circles.append(normalized_group)

        print(f"{normalized_circles}")

        circleSet = 0
        circles = []
        for [x, y, r] in normalized_circles[circleSet]:
            circles.append(Circle(r).move_to([x, y, 0]))

        circles_2 = []
        for [x, y, r] in normalized_circles[circleSet + 1]:
            circles_2.append(Circle(r).move_to([x, y, 0]))

        print(circles)
        print(circles_2)

        # for (c1, c2) in zip(circles, circles_2):
        transforms = [Transform(c1, c2) for (c1, c2) in zip(circles, circles_2)]
        print(transforms)
        self.play(*transforms)
