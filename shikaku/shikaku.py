import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams.update({'axes.linewidth': 2})
matplotlib.rcParams['xtick.major.size'] = 8
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['ytick.major.size'] = 8
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rc('text', usetex=True)
matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
import matplotlib.pyplot as plt


class MultipanelFigure(object):
    """
    Parameters
    ----------
    rows, cols : int
        The figure will have ``rows * cols`` panels.
    width, height : float
        The dimensions of the figure in inches.

    Attributes
    ----------
    F : matplotlib.figure.Figure
    current_panel_id : int
    """
    def __init__(self, rows, cols, width=6, height=6):
        self.F = plt.figure(figsize=(width, height))
        self.rows = rows
        self.cols = cols
        self.current_panel_id = 1
        self.xpad_factor = 0.05
        self.ypad_factor = 0.05
        self.origin_padding = False

    def get_new_panel(self):
        """
        Creates a new panel at the next empty position. Panels are
        created row-by-row, from left to right.

        Returns
        -------
        panel : matplotlib.axes.AxesSubplot
        """
        panel = self.F.add_subplot(self.rows, self.cols, self.current_panel_id)
        panel.tick_params(axis='both', direction='inout')
        self._adjust_spines(panel, ['left','bottom'])
        return panel

    def _adjust_spines(self, panel, spines):
        """
        Stylize panel to include only specified axes. Also shifts origin point
        slightly away from bottom-left corner.

        Parameters
        ----------
        panel : matplotlib.axes.AxesSubplot
        spines : list
            Example ``['left', 'bottom']`` would put the x-axis on the bottom
            and the y-axis on the left.
        """
        for loc, spine in panel.spines.items():
            if loc in spines:
                if self.origin_padding:
                    spine.set_position(('outward',10)) # outward by 10 points
                else:
                    pass
                spine.set_smart_bounds(False)
            else:
                spine.set_color('none') # don't draw spine

            # turn off ticks where there is no spine
            if 'left' in spines:
                panel.yaxis.set_ticks_position('left')
            else:
                # no yaxis ticks
                panel.yaxis.set_ticks([])

            if 'bottom' in spines:
                panel.xaxis.set_ticks_position('bottom')
            else:
                # no xaxis ticks
                panel.xaxis.set_ticks([])

    def add_panel_to_figure(self, panel, pad_axes=True, prettify_ticks=True,
                            xtick_fmt="%.0f", ytick_fmt="%.0f"):
        """
        Add a finished panel to the figure.

        Parameters
        ----------
        panel : matplotlib.axes.AxesSubplot
        pad_axes : bool
            Whether to add space before lower limit and above upper limit.
        prettify_ticks : bool
            Whether to reformat tick labels to make them prettier.
        xtick_fmt, ytick_fmt : str
            The formatting strings that will be applied to tick labels if
            ``prettify_ticks == True``.
        """
        if pad_axes:
            self._pad_axes(panel)
        if prettify_ticks:
            self._prettify_ticks(panel, xtick_fmt, ytick_fmt)
        self.F.add_subplot(panel)
        self.current_panel_id += 1

    def _pad_axes(self, panel):
        x_lim = panel.get_xlim()
        x_range = x_lim[1] - x_lim[0]
        x_pad = x_range * self.xpad_factor
        panel.set_xlim( (x_lim[0] - x_pad, x_lim[1] + x_pad) )

        y_lim = panel.get_ylim()
        y_range = y_lim[1] - y_lim[0]
        y_pad = y_range * self.ypad_factor
        panel.set_ylim( (y_lim[0] - y_pad, y_lim[1] + y_pad) )

    def _prettify_ticks(self, panel, xtick_fmt, ytick_fmt):
        x_ticks = panel.get_xticks()
        y_ticks = panel.get_yticks()
        x_ticklabels = [xtick_fmt % x for x in x_ticks]
        y_ticklabels = [ytick_fmt % y for y in y_ticks]
        panel.set_xticklabels(x_ticklabels)
        panel.set_yticklabels(y_ticklabels)

    def finalize_figure(self, plot_file_name):
        """
        Write figure to file.
        
        Parameters
        ----------
        plot_file_name : str
            File name for output, including extension. Extension will determine
            output format, e.g. pdf, png, eps.
        """
        plt.tight_layout()
        plt.draw()
        plt.savefig(plot_file_name, bbox_inches='tight')
        plt.clf()
        print "Wrote %s" % plot_file_name
