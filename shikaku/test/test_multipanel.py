from unittest import TestCase
from ..shikaku import MultipanelFigure
import numpy as np

class TestMultiPanel(TestCase):
    def setUp(self):
        pass

    def test_create_multipanel_figure(self):
        fig = MultipanelFigure(rows=2, cols=2, width=8, height=8)
        x = np.arange(20)

        panel_1 = fig.get_new_panel()
        panel_1.plot(x, x, 'c-', lw=4)
        fig.add_panel_to_figure(panel_1)

        panel_2 = fig.get_new_panel()
        panel_2.plot(x, 2*x, 'r-', lw=4)
        fig.add_panel_to_figure(panel_2)

        panel_3 = fig.get_new_panel()
        panel_3.plot(x, x**2, 'k-', lw=4)
        fig.add_panel_to_figure(panel_3)

        panel_4 = fig.get_new_panel()
        panel_4.plot(x, -x, 'go', lw=4)
        fig.add_panel_to_figure(panel_4)

        fig.finalize_figure('figure.pdf')
