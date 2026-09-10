from DyeTool import DyeTool
from BoundaryTool import BoundaryTool

import pygame_gui, pygame

class UI:

    def __init__(self, sim_w, sim_h, panel_w):
        self.sim_w = sim_w
        self.sim_h = sim_h
        self.panel_w = panel_w

        win_w = self.sim_w + self.panel_w
        win_h = self.sim_h

        self.manager = pygame_gui.UIManager((win_w, win_h))


        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.sim_w, 0), (self.panel_w, win_h)),
            manager=self.manager
        )

        self.layer_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["dye", "speed", "pressure", "dye+speed", "dye+pressure"],
            starting_option="dye",
            relative_rect=pygame.Rect((10, 20), (220, 30)),
            manager=self.manager,
            container=self.panel
        )
        self.selected_layer = "dye"

        self.tool_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=["dye", "boundary", "select"],
            starting_option="dye",
            relative_rect=pygame.Rect((10, 60), (220, 30)),
            manager=self.manager,
            container=self.panel
        )
        self.selected_tool = DyeTool()


    def process_events(self, fluid, scene):

        running = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            self.manager.process_events(event)

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.layer_dropdown:
                    self.selected_layer = event.text

                if event.ui_element == self.tool_dropdown:
                    match event.text:
                        case "dye":
                            self.selected_tool = DyeTool()
                        case "boundary":
                            self.selected_tool = BoundaryTool()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.selected_tool.enter_down(fluid, scene)

            if event.type == pygame.MOUSEMOTION:
                self.selected_tool.mouse_move(pygame.mouse.get_pos())

        self.mouse_down(fluid, scene)

        return running


        

    def mouse_down(self, fluid, scene):

        if not pygame.mouse.get_pressed()[0]:
            return

        mx, my = pygame.mouse.get_pos()

        if mx >= self.sim_w or my >= self.sim_h:
            return

        self.selected_tool.mouse_down((mx, my), fluid, scene)

    def draw(self, screen, dt):

        self.manager.update(dt)
        self.manager.draw_ui(screen)