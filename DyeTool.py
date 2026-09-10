from Tool import Tool

class DyeTool(Tool):
    def __init__(self):
        self.type = "dye"

    def mouse_down(self, pos, fluid, scene):

        i = int(pos[0] * fluid.width / scene.w)
        j = int(pos[1] * fluid.height / scene.h)

        r = 2

        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):

                ii = i + di
                jj = j + dj

                if 0 <= ii < fluid.width and 0 <= jj < fluid.height:
                    fluid.dye[ii + 1, jj + 1] += 1.0