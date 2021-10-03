#! /usr/bin/python
'''
Create an eye using circles in Inkscape
'''
from math import sqrt,cos, sin, pi, pow

import inkex
from inkex import GenerateExtension
from inkex import Circle

# def calculateEyeRadius(height, iris_width, crescent_factor, shape):
#     if shape=="Lens":
#         radius=(pow(height,2)+pow((iris_width/2),2))/(2*(iris_width/2))
#         return (radius,radius)
#     else:
#         r2 = (pow(height,2)+pow((iris_width),2))/(2*(iris_width))
#         r3 = (pow(height,2)+pow((iris_width*crescent_factor),2))/(2*(iris_width*crescent_factor))
#         # raise ValueError(f"Circle 1 {r2}, Circle 2 {r3}, Height {height}, Iris width {iris_width}, Shape {shape}")
#         return (r2,r3)

# def rotate(radius, angle):
#     return {"x":cos(angle/180*pi)*radius, "y":sin(angle/180*pi)*radius}

# def interCircleDistance(iris_width, offset, iris_radiuses, stroke_w_eye, crescent_factor, shape):
#     if shape=="Lens":
#         d2 = iris_width/2-(iris_radiuses[0]-(stroke_w_eye/2))+offset
#         d3 = -1*(iris_width/2-(iris_radiuses[1]-(stroke_w_eye/2)))+offset
#         distance = (d2,d3)
#     else:
#         d2 = iris_width-(iris_radiuses[0]-(stroke_w_eye/2))+offset
#         d3 = iris_width*crescent_factor-(iris_radiuses[1]-(stroke_w_eye/2))+offset
#         distance = (d2,d3)
#         # the second one is larger
#     return distance

# def heightCalculator(main_circle_radius, offset):
#     return sqrt(pow(main_circle_radius,2)-pow(offset,2))

def placingRadiusCalculator(corrected_main_circle_radius, corrected_small_circle_radius, stroke_w_small, stroke_w_main, circle_pos):
    if circle_pos == "centre-on-edge":
        return corrected_main_circle_radius
    elif circle_pos == "centre-over-edge":
        return sqrt(pow(corrected_main_circle_radius,2)-pow(corrected_small_circle_radius,2))
    elif circle_pos == "circles-inner-edge":
        return corrected_main_circle_radius- corrected_small_circle_radius- (stroke_w_small+ stroke_w_main)/2
    elif circle_pos == "circles-outer-edge":
        return corrected_main_circle_radius+ corrected_small_circle_radius+ (stroke_w_small+ stroke_w_main)/2

def correctedCircleRadius(circle_diameter, circle_stroke):
    return (circle_diameter-circle_stroke)/2.0

class Circles(GenerateExtension):
    def __init__(self):
        GenerateExtension.__init__(self)
        #Main figure parsing
        self.arg_parser.add_argument("--d-main",
                        action="store", type=float,
                        dest="diameter", default=25.000,
                        help="The diameter of the main circle")
        self.arg_parser.add_argument("--d-small",
                        action="store", type=float,
                        dest="little_diameter", default=2.000,
                        help="The diameter of the small circles")
        self.arg_parser.add_argument("--num-small-circles",
                        action="store", type=int,
                        dest="num_small_circles", default=4.000,
                        help="The amount of small circles included")
        self.arg_parser.add_argument("--stroke-w-main",
                        action="store", type=float,
                        dest="stroke_w_main", default=0.500,
                        help="The width of the stroke on the main circle")
        self.arg_parser.add_argument("--stroke-w-small",
                        action="store", type=float,
                        dest="stroke_w_small", default=0.500,
                        help="The width of the stroke of the small circles")
        self.arg_parser.add_argument("--angle",
                        action="store", type=float,
                        dest="angle", default=0.000,
                        help="The angle change of the final figure")
        self.arg_parser.add_argument("--circle-pos",
                        action="store", type=str,
                        dest="circle_pos", default="Lens",
                        help="The positioning of the small circles on the large one")
        self.arg_parser.add_argument("--Individual-circle-control",
                        action="store", type=inkex.Boolean,
                        dest="Individual_circle_control", default="False",
                        help="Use individual circle control max 10")
        self.arg_parser.add_argument("--active-tab",
                        action="store", type=str,
                        dest="active_tab", default=0.0,
                        help="Which tab is active")
        # self.OptionParser.add_option("", "", action="store", type=float, dest="", default=25, help="")
        #Individual circles tab
        self.arg_parser.add_argument("--include-1",
                        action="store", type=inkex.Boolean,
                        dest="include1", default="False",
                        help="include circle 1")
        self.arg_parser.add_argument("--diameter-1",
                        action="store", type=float,
                        dest="diameter1", default=2.000,
                        help="The diameter of circle 1")
        self.arg_parser.add_argument("--stroke-w-1",
                        action="store", type=float,
                        dest="strokew1", default=0.500,
                        help="The width of the stroke of the circle 1")

        self.arg_parser.add_argument("--include-2",
                        action="store", type=inkex.Boolean,
                        dest="include2", default="False",
                        help="include circle 2")
        self.arg_parser.add_argument("--diameter-2",
                        action="store", type=float,
                        dest="diameter2", default=2.000,
                        help="The diameter of circle 2")
        self.arg_parser.add_argument("--stroke-w-2",
                        action="store", type=float,
                        dest="strokew2", default=0.500,
                        help="The width of the stroke of the circle 2")

        self.arg_parser.add_argument("--include-3",
                        action="store", type=inkex.Boolean,
                        dest="include3", default="False",
                        help="include circle 3")
        self.arg_parser.add_argument("--diameter-3",
                        action="store", type=float,
                        dest="diameter3", default=2.000,
                        help="The diameter of circle 3")
        self.arg_parser.add_argument("--stroke-w-3",
                        action="store", type=float,
                        dest="strokew3", default=0.500,
                        help="The width of the stroke of the circle 3")

        self.arg_parser.add_argument("--include-4",
                        action="store", type=inkex.Boolean,
                        dest="include4", default="False",
                        help="include circle 4")
        self.arg_parser.add_argument("--diameter-4",
                        action="store", type=float,
                        dest="diameter4", default=2.000,
                        help="The diameter of circle 4")
        self.arg_parser.add_argument("--stroke-w-4",
                        action="store", type=float,
                        dest="strokew4", default=0.500,
                        help="The width of the stroke of the circle 4")

        self.arg_parser.add_argument("--include-5",
                        action="store", type=inkex.Boolean,
                        dest="include5", default="False",
                        help="include circle 5")
        self.arg_parser.add_argument("--diameter-5",
                        action="store", type=float,
                        dest="diameter5", default=2.000,
                        help="The diameter of circle 5")
        self.arg_parser.add_argument("--stroke-w-5",
                        action="store", type=float,
                        dest="strokew5", default=0.500,
                        help="The width of the stroke of the circle 5")

        self.arg_parser.add_argument("--include-6",
                        action="store", type=inkex.Boolean,
                        dest="include6", default="False",
                        help="include circle 6")
        self.arg_parser.add_argument("--diameter-6",
                        action="store", type=float,
                        dest="diameter6", default=2.000,
                        help="The diameter of circle 6")
        self.arg_parser.add_argument("--stroke-w-6",
                        action="store", type=float,
                        dest="strokew6", default=0.500,
                        help="The width of the stroke of the circle 6")

        self.arg_parser.add_argument("--include-7",
                        action="store", type=inkex.Boolean,
                        dest="include7", default="False",
                        help="include circle 7")
        self.arg_parser.add_argument("--diameter-7",
                        action="store", type=float,
                        dest="diameter7", default=2.000,
                        help="The diameter of circle 7")
        self.arg_parser.add_argument("--stroke-w-7",
                        action="store", type=float,
                        dest="strokew7", default=0.500,
                        help="The width of the stroke of the circle 7")

        self.arg_parser.add_argument("--include-8",
                        action="store", type=inkex.Boolean,
                        dest="include8", default="False",
                        help="include circle 8")
        self.arg_parser.add_argument("--diameter-8",
                        action="store", type=float,
                        dest="diameter8", default=2.000,
                        help="The diameter of circle 8")
        self.arg_parser.add_argument("--stroke-w-8",
                        action="store", type=float,
                        dest="strokew8", default=0.500,
                        help="The width of the stroke of the circle 8")

        self.arg_parser.add_argument("--include-9",
                        action="store", type=inkex.Boolean,
                        dest="include9", default="False",
                        help="include circle 9")
        self.arg_parser.add_argument("--diameter-9",
                        action="store", type=float,
                        dest="diameter9", default=2.000,
                        help="The diameter of circle 9")
        self.arg_parser.add_argument("--stroke-w-9",
                        action="store", type=float,
                        dest="strokew9", default=0.500,
                        help="The width of the stroke of the circle 9")

        self.arg_parser.add_argument("--include-10",
                        action="store", type=inkex.Boolean,
                        dest="include10", default="False",
                        help="include circle 10")
        self.arg_parser.add_argument("--diameter-10",
                        action="store", type=float,
                        dest="diameter10", default=2.000,
                        help="The diameter of circle 10")
        self.arg_parser.add_argument("--stroke-w-10",
                        action="store", type=float,
                        dest="strokew10", default=0.500,
                        help="The width of the stroke of the circle 10")

    def generate(self): #pylint: disable=no-member
        pass
        so=self.options

        corrected_main_circle_radius = correctedCircleRadius(so.diameter, so.stroke_w_main)
        corrected_small_circle_radius = correctedCircleRadius(so.little_diameter, so.stroke_w_small)

        main_circle = Circle(cx="0", cy="0")
        main_circle.set("r", str(corrected_main_circle_radius))
        main_circle.set("style",f"fill:none;stroke:#ff0000;stroke-width:{str(so.stroke_w_main)};")
        yield main_circle
        
        small_circle_placing_radius = placingRadiusCalculator(corrected_main_circle_radius, corrected_small_circle_radius, so.stroke_w_small, so.stroke_w_main, so.circle_pos)
        if so.Individual_circle_control == False or so.num_small_circles>10:
            for n in range(so.num_small_circles):
                angle = (2.0*pi)/so.num_small_circles*n+pi/180*so.angle
                Current_circle = Circle(cx=str(cos(angle)*small_circle_placing_radius), cy=str(sin(angle)*small_circle_placing_radius))
                Current_circle.set("r", str(corrected_small_circle_radius))
                Current_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(so.stroke_w_small)};")
                yield Current_circle
        elif so.Individual_circle_control == True and so.num_small_circles<=10:
            individual_circles = {}
            individual_circles[0]=[so.include1,so.diameter1,so.strokew1]
            individual_circles[1]=[so.include2,so.diameter2,so.strokew2]
            individual_circles[2]=[so.include3,so.diameter3,so.strokew3]
            individual_circles[3]=[so.include4,so.diameter4,so.strokew4]
            individual_circles[4]=[so.include5,so.diameter5,so.strokew5]
            individual_circles[5]=[so.include6,so.diameter6,so.strokew6]
            individual_circles[6]=[so.include7,so.diameter7,so.strokew7]
            individual_circles[7]=[so.include8,so.diameter8,so.strokew8]
            individual_circles[8]=[so.include9,so.diameter9,so.strokew9]
            individual_circles[9]=[so.include10,so.diameter10,so.strokew10]
            # }
            for n in range(so.num_small_circles):
                if individual_circles[n][0]:
                    angle = (2.0*pi)/so.num_small_circles*n+pi/180*so.angle
                    corrected_small_circle_radius = correctedCircleRadius(individual_circles[n][1], individual_circles[n][2])
                    small_circle_placing_radius = placingRadiusCalculator(corrected_main_circle_radius, corrected_small_circle_radius, individual_circles[n][2], so.stroke_w_main, so.circle_pos)
                    # raise ValueError(f"n: {n}, include: {individual_circles[n][0]}, diameter: {individual_circles[n][1]}, stroke: {individual_circles[n][0]}, corrected radius: {corrected_small_circle_radius}, placing radius: {small_circle_placing_radius}")
                    Current_circle = Circle(cx=str(cos(angle)*small_circle_placing_radius), cy=str(sin(angle)*small_circle_placing_radius))
                    Current_circle.set("r", str(corrected_small_circle_radius))
                    Current_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(individual_circles[n][2])};")
                    yield Current_circle

        else:
            raise ValueError(f"Reduce the number of circles to 10 or fewer to control the circles individually")


        # requiredHeight = heightCalculator(corrected_main_circle_radius, so.offset)
        # irisRadiuses = calculateEyeRadius(requiredHeight, so.iris_width, so.crescent_factor, so.shape)
        # inter_circle_distance = interCircleDistance(so.iris_width, so.offset, irisRadiuses, so.stroke_w_eye, so.crescent_factor, so.shape)
        # # so.iris_width/2-(irisRadiuses[0]-(so.stroke_w_eye/2))

        # LC_coords = rotate(inter_circle_distance[0],so.angle)
        # Left_circle = Circle(cx=str(LC_coords["x"]), cy=str(LC_coords["y"]))
        # Left_circle.set("r", str(irisRadiuses[0]-(so.stroke_w_eye/2)))
        # Left_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(so.stroke_w_eye)};")

        # RC_coords = rotate(inter_circle_distance[1],so.angle)
        # Right_circle = Circle(cx=str(RC_coords["x"]), cy=str(RC_coords["y"]))
        # Right_circle.set("r", str(irisRadiuses[1]-(so.stroke_w_eye/2)))
        # Right_circle.set("style",f"fill:none;stroke:#000000;stroke-width:{str(so.stroke_w_eye)};")

        
        # yield Left_circle
        # yield Right_circle
    #     # raise inkex.AbortExtension(message="This is a test")
    #     # print("This is a test")
    #     #examples spirograph.py in /usr/share/inkscape/extensions
        # gcodetools.py
    # /usr/share/inkscape/extensions/draw_from_triangle.py
    # /home/kataai/Downloads/nicechart.py
    
    # self.options
        pass
    
if __name__ == '__main__':
    c= Circles()
    c.run()