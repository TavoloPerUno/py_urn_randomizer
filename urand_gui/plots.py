import itertools

import pandas as pd
from bokeh.embed import components
from bokeh.layouts import column, row
from bokeh.models import (
    CDSView,
    ColumnDataSource,
    DatetimeTickFormatter,
    FactorRange,
    GroupFilter,
    HoverTool,
    Legend,
    NumeralTickFormatter,
    Paragraph,
    Select,
)
from bokeh.models.callbacks import CustomJS
from bokeh.palettes import Dark2_5 as bokeh_palette
from bokeh.plotting import figure
from bokeh.resources import INLINE

palette = ["#ba32a0", "#f85479", "#f8c260", "#00c2ba"]

chart_font = "Helvetica"
chart_title_font_size = "16pt"
chart_title_alignment = "center"
axis_label_size = "14pt"
axis_ticks_size = "12pt"
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = "bold italic"


def palette_generator(length, palette):
    int_div = length // len(palette)
    remainder = length % len(palette)
    return (palette * int_div) + palette[:remainder]


def plot_styler(p):
    p.title.text_font_size = chart_title_font_size
    p.title.text_font = chart_font
    p.title.align = chart_title_alignment
    p.title.text_font_style = chart_font_style_title
    p.y_range.start = 0
    p.x_range.range_padding = chart_inner_left_padding
    p.xaxis.axis_label_text_font = chart_font
    p.xaxis.major_label_text_font = chart_font
    p.xaxis.axis_label_standoff = int(default_padding * 0.3)
    p.xaxis.axis_label_text_font_size = axis_label_size
    p.xaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_text_font = chart_font
    p.yaxis.major_label_text_font = chart_font
    p.yaxis.axis_label_text_font_size = axis_label_size
    p.yaxis.major_label_text_font_size = axis_ticks_size
    p.yaxis.axis_label_standoff = int(default_padding * 0.3)
    p.toolbar.logo = None
    p.toolbar_location = None
    p.x_range.range_padding = 0.1
    p.legend.background_fill_alpha = 0.0
    p.xaxis.major_label_orientation = 0.18
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    # p.legend.orientation = "vertical"
    p.sizing_mode = "stretch_width"
    p.xaxis.axis_label_text_font_size = "7pt"
    p.xaxis.major_label_text_font_size = "7pt"
    p.yaxis.axis_label_text_font_size = "7pt"
    p.yaxis.major_label_text_font_size = "7pt"


def plt_factor_treatment_assignments(study):
    factors = list(study.factors.keys())
    title_select_factor = Paragraph(
        text="Factor:", sizing_mode="stretch_both", align="end"
    )
    select_factor = Select(
        title="",
        value=factors[0],
        options=factors,
        sizing_mode="stretch_both",
        align="start",
        width_policy="fit",
    )

    pdf_urns = study.get_study_urns()
    pdf_all = study.export_history()
    pdf_all = (
        pdf_all.groupby("trt")
        .size()
        .reset_index()
        .rename(columns={0: "n_participants"})
    )
    n_participants = pdf_all["n_participants"].sum()
    tooltips_all = [("No. participants", "@n_participants")]
    p_all = figure(
        x_range=study.treatments,
        height=450,
        width=500,
        title="All participants ({0})".format(n_participants),
        toolbar_location=None,
        tools="",
        tooltips=tooltips_all,
        sizing_mode="stretch_width",
    )
    source_all = ColumnDataSource(data=pdf_all[["trt", "n_participants"]])
    p_all.add_tools(HoverTool(tooltips=[("No. participants", "@n_participants")]))
    p_all.vbar(x="trt", top="n_participants", width=0.9, alpha=0.9, source=source_all)
    p_all.xgrid.grid_line_color = None
    p_all.y_range.start = 0

    p_all.yaxis.axis_label = "No. participants"
    p_all.xaxis.axis_label = "Treatment"
    plot_styler(p_all)

    pdf_factors = pdf_urns.assign(
        **dict(
            [
                (
                    "pc_trt_{0}".format(trt).replace("-", ""),
                    pdf_urns["trt_{0}".format(trt)]
                    * 100
                    / pdf_urns[
                        [col for col in pdf_urns.columns if col.startswith("trt_")]
                    ].sum(axis=1),
                )
                for trt in study.treatments
            ]
        )
    )
    pdf_factors = pdf_factors.assign(
        **dict(
            [
                (trt, pdf_factors["pc_trt_{0}".format(trt).replace("-", "")])
                for trt in study.treatments
            ]
        )
    )
    tooltips = [
        ("Trtmt {0} ".format(trt), "@pc_trt_{0}".format(trt.replace("-", "")))
        for trt in study.treatments
    ]
    src = ColumnDataSource(data=pdf_factors)
    filter = GroupFilter(column_name="factor", group=factors[0])
    view = CDSView(filter=filter)

    p = figure(
        height=450,
        width=500,
        title="By factor",
        toolbar_location=None,
        tools="",
        tooltips=tooltips,
        x_range=FactorRange(),
        y_range=[0, 110],
        sizing_mode="stretch_width",
    )
    p.x_range.factors = study.factors[factors[0]]
    lst_color = list(
        itertools.islice(itertools.cycle(bokeh_palette), len(study.treatments))
    )
    lst_vbar = p.vbar_stack(
        [trt for trt in study.treatments],
        x="factor_level",
        width=0.9,
        alpha=0.5,
        color=lst_color,
        source=src,
        view=view,
    )
    legend = Legend(
        items=[
            (trt, [plt_vbar]) for (trt, plt_vbar) in zip(study.treatments, lst_vbar)
        ],
        location=(0, 30),
        title="Treatments",
    )
    p.add_layout(legend, "right")
    p.yaxis.axis_label = "Percentage"
    p.xaxis.axis_label = "Factor levels"
    plot_styler(p)

    callback = CustomJS(
        args=dict(
            select=select_factor, src=src, filter=filter, factors=study.factors, plot=p
        ),
        code="""
          filter.group = select.value
          filter.change.emit()
          src.change.emit()
          plot.x_range.factors = factors[select.value]
        """,
    )

    select_factor.js_on_change("value", callback)

    # select_factor.on_change('value', pick_new_factor)
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script_p, div_p = components(
        row(
            column(p_all, sizing_mode="stretch_width"),
            column(
                row(title_select_factor, select_factor, align="end"),
                p,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )
    )
    return script_p, div_p, js_resources, css_resources


def plt_enrollment_timeline(study):
    """Cumulative enrollment over time, broken down by treatment arm."""
    pdf = study.export_history()
    if len(pdf) == 0:
        return "", ""

    pdf = pdf.sort_values("datetime")
    pdf["datetime"] = pd.to_datetime(pdf["datetime"], utc=True)

    lst_color = list(
        itertools.islice(itertools.cycle(bokeh_palette), len(study.treatments))
    )
    color_map = dict(zip(study.treatments, lst_color))

    # --- Cumulative enrollment by treatment ---
    p_enroll = figure(
        height=300,
        width=700,
        title="Cumulative Enrollment",
        x_axis_type="datetime",
        toolbar_location=None,
        tools="",
        sizing_mode="stretch_width",
    )
    legend_items = []
    for trt in study.treatments:
        pdf_trt = pdf[pdf["trt"] == trt].copy()
        pdf_trt["cumcount"] = range(1, len(pdf_trt) + 1)
        src = ColumnDataSource(
            data={"datetime": pdf_trt["datetime"], "cumcount": pdf_trt["cumcount"]}
        )
        line = p_enroll.line(
            "datetime",
            "cumcount",
            source=src,
            line_width=2,
            color=color_map[trt],
            alpha=0.8,
        )
        p_enroll.scatter(
            "datetime",
            "cumcount",
            source=src,
            size=5,
            color=color_map[trt],
            alpha=0.8,
        )
        legend_items.append((trt, [line]))

    legend = Legend(items=legend_items, location="top_left", title="Treatments")
    p_enroll.add_layout(legend, "right")
    p_enroll.yaxis.axis_label = "Participants"
    p_enroll.xaxis.axis_label = "Date"
    p_enroll.xaxis.formatter = DatetimeTickFormatter(days="%b %d", months="%b %Y")
    p_enroll.y_range.start = 0
    p_enroll.xgrid.grid_line_color = None
    p_enroll.sizing_mode = "stretch_width"
    p_enroll.title.text_font_size = chart_title_font_size
    p_enroll.title.text_font = chart_font
    p_enroll.title.align = chart_title_alignment
    p_enroll.title.text_font_style = chart_font_style_title
    p_enroll.legend.background_fill_alpha = 0.0

    # --- Imbalance ratio over time ---
    pdf_sorted = pdf.sort_values("datetime").copy()
    cumcounts = {}
    ratios = []
    datetimes = []
    for _, row_data in pdf_sorted.iterrows():
        trt = row_data["trt"]
        cumcounts[trt] = cumcounts.get(trt, 0) + 1
        counts = list(cumcounts.values())
        max_c = max(counts)
        min_c = min(counts)
        total = sum(counts)
        # Imbalance = (max - min) / total
        ratios.append((max_c - min_c) / total if total > 0 else 0)
        datetimes.append(row_data["datetime"])

    src_imb = ColumnDataSource(data={"datetime": datetimes, "imbalance": ratios})
    p_imbalance = figure(
        height=300,
        width=700,
        title="Treatment Imbalance Over Time",
        x_axis_type="datetime",
        toolbar_location=None,
        tools="",
        sizing_mode="stretch_width",
    )
    p_imbalance.line(
        "datetime",
        "imbalance",
        source=src_imb,
        line_width=2,
        color="#e74c3c",
        alpha=0.8,
    )
    p_imbalance.scatter(
        "datetime",
        "imbalance",
        source=src_imb,
        size=5,
        color="#e74c3c",
        alpha=0.8,
    )
    p_imbalance.yaxis.axis_label = "Imbalance ratio"
    p_imbalance.xaxis.axis_label = "Date"
    p_imbalance.xaxis.formatter = DatetimeTickFormatter(days="%b %d", months="%b %Y")
    p_imbalance.yaxis.formatter = NumeralTickFormatter(format="0.0%")
    p_imbalance.y_range.start = 0
    p_imbalance.xgrid.grid_line_color = None
    p_imbalance.sizing_mode = "stretch_width"
    p_imbalance.title.text_font_size = chart_title_font_size
    p_imbalance.title.text_font = chart_font
    p_imbalance.title.align = chart_title_alignment
    p_imbalance.title.text_font_style = chart_font_style_title

    add_tooltip = HoverTool(
        tooltips=[("Date", "@datetime{%b %d, %Y}"), ("Imbalance", "@imbalance{0.1%}")],
        formatters={"@datetime": "datetime"},
    )
    p_imbalance.add_tools(add_tooltip)

    script_timeline, div_timeline = components(
        row(p_enroll, p_imbalance, sizing_mode="stretch_width")
    )
    return script_timeline, div_timeline
