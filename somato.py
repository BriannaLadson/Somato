from PIL import Image, ImageDraw, ImageChops
import math

def bezier(p0, p1, p2, p3, steps=50):
	points = []

	for i in range(steps + 1):
		t = i / steps

		x = (
			(1 - t) ** 3 * p0[0]
			+ 3 * (1 - t) ** 2 * t * p1[0]
			+ 3 * (1 - t) * t ** 2 * p2[0]
			+ t ** 3 * p3[0]
		)

		y = (
			(1 - t) ** 3 * p0[1]
			+ 3 * (1 - t) ** 2 * t * p1[1]
			+ 3 * (1 - t) * t ** 2 * p2[1]
			+ t ** 3 * p3[1]
		)

		points.append((x, y))

	return points


class Iris:
	def __init__(
		self,
		center,
		radius_x,
		radius_y=None,
		color="brown"
	):
		self.center = center
		self.radius_x = radius_x

		if radius_y is None:
			radius_y = radius_x

		self.radius_y = radius_y
		self.color = color

	def bounds(self):
		x, y = self.center

		return (
			x - self.radius_x,
			y - self.radius_y,
			x + self.radius_x,
			y + self.radius_y
		)


class Eye:
	def __init__(
		self,
		p0,
		upper_p1,
		upper_p2,
		p3,
		lower_p1,
		lower_p2,
		thickness,
		iris=None,
		sclera_color="white",
		outline_color="black",
		scale=1,
		scale_x=1,
		scale_y=1,
		rotation=0
	):
		self.p0 = p0
		self.upper_p1 = upper_p1
		self.upper_p2 = upper_p2
		self.p3 = p3

		self.lower_p1 = lower_p1
		self.lower_p2 = lower_p2

		self.thickness = thickness
		self.iris = iris

		self.sclera_color = sclera_color
		self.outline_color = outline_color

		self.scale = scale
		self.scale_x = scale_x
		self.scale_y = scale_y
		self.rotation = rotation

	def transform_point(self, point):
		center_x = (self.p0[0] + self.p3[0]) / 2
		center_y = (self.p0[1] + self.p3[1]) / 2

		x = point[0] - center_x
		y = point[1] - center_y

		x *= self.scale * self.scale_x
		y *= self.scale * self.scale_y

		angle = math.radians(self.rotation)

		rotated_x = (
			x * math.cos(angle)
			- y * math.sin(angle)
		)

		rotated_y = (
			x * math.sin(angle)
			+ y * math.cos(angle)
		)

		return (
			rotated_x + center_x,
			rotated_y + center_y
		)

	def get_shape(self):
		p0 = self.transform_point(self.p0)
		upper_p1 = self.transform_point(self.upper_p1)
		upper_p2 = self.transform_point(self.upper_p2)
		p3 = self.transform_point(self.p3)

		lower_p1 = self.transform_point(self.lower_p1)
		lower_p2 = self.transform_point(self.lower_p2)

		upper = bezier(
			p0,
			upper_p1,
			upper_p2,
			p3
		)

		lower = bezier(
			p0,
			lower_p1,
			lower_p2,
			p3
		)

		return upper + lower[::-1]

	def draw(self, image):
		draw = ImageDraw.Draw(image)

		shape = self.get_shape()

		draw.polygon(
			shape,
			fill=self.sclera_color,
			outline=self.outline_color,
			width=self.thickness
		)

		if self.iris is not None:
			eye_mask = Image.new(
				"L",
				image.size,
				0
			)

			eye_mask_draw = ImageDraw.Draw(eye_mask)

			eye_mask_draw.polygon(
				shape,
				fill=255
			)

			iris_mask = Image.new(
				"L",
				image.size,
				0
			)

			iris_mask_draw = ImageDraw.Draw(iris_mask)

			iris_mask_draw.ellipse(
				self.iris.bounds(),
				fill=255
			)

			visible_iris = ImageChops.multiply(
				eye_mask,
				iris_mask
			)

			iris_layer = Image.new(
				"RGBA",
				image.size,
				self.iris.color
			)

			image.paste(
				iris_layer,
				(0, 0),
				visible_iris
			)

			draw.polygon(
				shape,
				outline=self.outline_color,
				width=self.thickness
			)


class Somato:
	def __init__(
		self,
		width=800,
		height=400,
		background_color="white"
	):
		self.image = Image.new(
			"RGBA",
			(width, height),
			background_color
		)

		self.body_parts = []

	def add(self, body_part):
		self.body_parts.append(body_part)

	def render(self):
		for body_part in self.body_parts:
			body_part.draw(self.image)

	def save(self, file_name):
		self.render()
		self.image.save(file_name)