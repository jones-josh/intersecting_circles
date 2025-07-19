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


def loadCircleGroups(csvPath: str) -> list[CircleGroup]:
    ungroupedCircles: list[Circle] = []
    with open(csvPath) as f:
        reader = csv.reader(removeCsvComments(f))
        for row in reader:
            assert len(row) == 3
            ungroupedCircles.append(
                Circle((float(row[0]), float(row[1])), float(row[2]))
            )

    assert len(ungroupedCircles) % CIRCLES_PER_GROUP == 0

    groups = []
    for i in range(0, len(ungroupedCircles), CIRCLES_PER_GROUP):
        group = []
        for j in range(CIRCLES_PER_GROUP):
            group.append(ungroupedCircles[i + j])
        groups.append(group)

    return groups


# forces all circles to exist in [0, 1] in x and y, translates and scales
# each group individually
def normalizeCircleGroups(groups: list[CircleGroup]) -> list[CircleGroup]:
    normalizedGroups: list[CircleGroup] = []
    for circleGroup in groups:
        minX: float = min([c.origin[0] - c.radius for c in circleGroup])
        maxX: float = max([c.origin[0] + c.radius for c in circleGroup])
        minY: float = min([c.origin[1] - c.radius for c in circleGroup])
        maxY: float = max([c.origin[1] + c.radius for c in circleGroup])

        groupWidth = maxX - minX
        groupHeight = maxY - minY
        scale: float = max(groupWidth, groupHeight)
        print(f"SCALE: {scale}")

        normalizedGroup: CircleGroup = []
        for circle in circleGroup:
            [x, y] = circle.origin
            r = circle.radius
            origin_x = (x - minX) / scale
            origin_x += (1 - groupWidth / scale) / 2  # center horizontally
            origin_y = (y - minY) / scale
            origin_y += (1 - groupHeight / scale) / 2  # center vertically
            normalizedGroup.append(Circle((origin_x, origin_y), r / scale))
            assert x - minX > 0
            assert scale > 0
        normalizedGroups.append(normalizedGroup)

    return normalizedGroups


if __name__ == "__main__":
    print(normalizeCircleGroups(loadCircleGroups("circles.csv")))


class DefaultTemplate(manim.Scene):
    def construct(self):
        normalizedCircles = normalizeCircleGroups(loadCircleGroups("circles.csv"))
        for group in loadCircleGroups("circles.csv"):
            for c in group:
                print(f"(x-{c.origin[0]})^2 + (y-{c.origin[1]})^2 = {c.radius}^2")

        print("------------")
        oldCircles = normalizedCircles[-1]

        drawCircleGroups = []
        for group in normalizedCircles:
            drawCircles = []
            for c in group:
                drawCircles.append(manim.Circle(c.radius).move_to([*c.origin, 0]))
                print(f"(x-{c.origin[0]})^2 + (y-{c.origin[1]})^2 = {c.radius}^2")
            drawCircleGroups.append(drawCircles)

        # currentGroup = drawCircleGroups[-1]
        # for nextGroup in drawCircleGroups:
        #     animations = []
        #     for currentCircle, nextCircle in zip(currentGroup, nextGroup):
        #         animations.append(manim.Transform(currentCircle, nextCircle))
        #     self.play(animations)

        # for nextGroup in normalizedCircles:
        #     animations = []
        #     for c, nextCircle in zip(drawCircles, nextGroup, oldCircles):
        #         animations.append(c.animate.move_to([*nextCircle.origin, 0]))
        #         print(f"move_to {[*nextCircle.origin, 0]}")
        #         # animations.append(c.animate.set_radius(nextCircle.radius))
        #         print(f"set_radius {nextCircle.radius}")
        #     self.play(*animations)
        #     oldCircles = nextGroup

        for group in drawCircleGroups:
            self.play([manim.Create(c) for c in group])
            self.play([manim.Uncreate(c) for c in group])
