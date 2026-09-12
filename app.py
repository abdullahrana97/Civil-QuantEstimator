

import io
import json
from datetime import datetime

import streamlit as st

from utils.calculations import (
    calc_brickwork,
    calc_plaster,
    calc_concrete,
    calc_steel,
)

from utils.data import (
    MORTAR_RATIOS,
    CONCRETE_RATIOS,
    WASTAGE_DEFAULTS,
    STEEL_BAR_SIZES_MM,
)

from utils.groq_helper import ask_groq


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Civil QuantEstimate",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

def init_state():

    defaults = {
        "page": "Dashboard",
        "last_result": None,
        "last_module": None,
        "calculation_count": 0,
        "calculation_history": [],
        "dark_mode": True,

    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# =========================================================
# THEME
# =========================================================

def get_theme():

    # Follow the theme selected by Streamlit:
    # Light / Dark / System
    try:
        is_dark = st.context.theme.type == "dark"
    except Exception:
        is_dark = False

    if is_dark:

        return {
            "bg": "#071313",
            "card": "#0d1d1c",
            "card2": "#102422",
            "text": "#f3faf7",
            "muted": "#94aaa5",
            "border": "rgba(55, 220, 157, .16)",
            "green": "#36d99b",
            "green_dark": "#159c6d",
            "green_soft": "rgba(54,217,155,.12)",
            "green_border": "rgba(54,217,155,.24)",
            "green_text": "#aaf1d3",
            "sidebar": "#061b18",
            "sidebar_text": "#d8e8e3",
            "sidebar_muted": "#78918c",
            "welcome": "linear-gradient(135deg, #0c2924, #0a1b1b)",
            "ai": "linear-gradient(135deg,#0b2b25,#0b1d1d)",
            "result": "linear-gradient(135deg,#0c2924,#0b1c1b)",
            "input": "#0b1d1c",
            "button": "#102422",
            "button_text": "#e9f8f3",
            "button_border": "rgba(54,217,155,.15)",
            "button_hover": "#15342f",
        }

    return {

        "bg": "#f5f8f7",
        "card": "#ffffff",
        "card2": "#eef5f2",
        "text": "#13211f",
        "muted": "#657773",
        "border": "rgba(19, 60, 49, .12)",
        "green": "#159c6d",
        "green_dark": "#12885e",
        "green_soft": "rgba(21,156,109,.10)",
        "green_border": "rgba(21,156,109,.22)",
        "green_text": "#08704d",
        "sidebar": "#10251b",
        "sidebar_text": "#e9f8f3",
        "sidebar_muted": "#91aaa2",
        "welcome": "linear-gradient(135deg, #e9f7f1, #f7fbf9)",
        "ai": "linear-gradient(135deg,#e7f7f0,#f4faf8)",
        "result": "linear-gradient(135deg,#e9f7f1,#f5faf8)",
        "input": "#ffffff",
        "button": "#f0f6f4",
        "button_text": "#19302b",
        "button_border": "rgba(19,60,49,.12)",
        "button_hover": "#dceee8",
    }


theme = get_theme()


# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    try:

        with open("style.css", "r", encoding="utf-8") as file:
            css = file.read()

        css_with_variables = f"""
        <style>

        :root {{
            --cq-bg: {theme["bg"]};
            --cq-card: {theme["card"]};
            --cq-card2: {theme["card2"]};

            --cq-text: {theme["text"]};
            --cq-muted: {theme["muted"]};

            --cq-border: {theme["border"]};

            --cq-green: {theme["green"]};
            --cq-green-dark: {theme["green_dark"]};

            --cq-green-soft: {theme["green_soft"]};
            --cq-green-border: {theme["green_border"]};
            --cq-green-text: {theme["green_text"]};

            --cq-sidebar: {theme["sidebar"]};
            --cq-sidebar-text: {theme["sidebar_text"]};
            --cq-sidebar-muted: {theme["sidebar_muted"]};

            --cq-welcome: {theme["welcome"]};
            --cq-ai: {theme["ai"]};
            --cq-result: {theme["result"]};

            --cq-input: {theme["input"]};

            --cq-button: {theme["button"]};
            --cq-button-text: {theme["button_text"]};
            --cq-button-border: {theme["button_border"]};
            --cq-button-hover: {theme["button_hover"]};
        }}

        {css}

        </style>
        """

        st.html(css_with_variables)

    except FileNotFoundError:

        st.error(
            "style.css was not found. "
            "Make sure style.css is in the same folder as app.py."
        )


load_css()


# =========================================================
# HTML HELPER
# =========================================================

def render_html(content):
    """
    Render custom HTML safely using Streamlit's HTML renderer.
    """

    st.html(content)


# =========================================================
# NAVIGATION
# =========================================================

def nav_button(label, target):

    if st.sidebar.button(
        label,
        use_container_width=True,
        type="primary"
        if st.session_state.page == target
        else "secondary",
    ):
        st.session_state.page = target
        st.rerun()


# =========================================================
# SAVE RESULT AS JSON
# =========================================================

def save_result(results, module):

    payload = {
        "application": "Civil QuantEstimate",
        "module": module,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "results": results,
    }

    return json.dumps(
        payload,
        indent=4,
        default=str,
    ).encode("utf-8")


# =========================================================
# CREATE PDF
# =========================================================

def make_pdf(results, module):

    try:

        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

    except ImportError:

        return b""

    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    width, height = A4

    y = height - 55

    pdf.setFont(
        "Helvetica-Bold",
        20,
    )

    pdf.drawString(
        45,
        y,
        "Civil QuantEstimate",
    )

    y -= 28

    pdf.setFont(
        "Helvetica-Bold",
        14,
    )

    pdf.drawString(
        45,
        y,
        module or "Quantity Estimation",
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        10,
    )

    pdf.drawString(
        45,
        y,
        datetime.now().strftime(
            "Generated: %Y-%m-%d %H:%M"
        ),
    )

    y -= 32

    for key, value in (results or {}).items():

        pdf.setFont(
            "Helvetica-Bold",
            10,
        )

        pdf.drawString(
            55,
            y,
            str(key)[:35],
        )

        pdf.setFont(
            "Helvetica",
            10,
        )

        pdf.drawString(
            270,
            y,
            str(value)[:50],
        )

        y -= 20

        if y < 55:

            pdf.showPage()

            y = height - 55

    pdf.save()

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# RECORD CALCULATION
# =========================================================

def record_calculation(module, results):

    st.session_state.last_result = results

    st.session_state.last_module = module

    st.session_state.calculation_count += 1

    st.session_state.calculation_history.append(
        {
            "module": module,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
    )


# =========================================================
# DISPLAY RESULTS
# =========================================================

def show_results(module, results):

    record_calculation(
        module,
        results,
    )

    render_html(
        """
        <div class="result">
            <div class="result-title">
                ✓ Calculation complete
            </div>
        </div>
        """
    )

    result_columns = st.columns(
        min(
            4,
            max(
                1,
                len(results),
            ),
        )
    )

    for index, (key, value) in enumerate(
        results.items()
    ):

        with result_columns[
            index % len(result_columns)
        ]:

            st.metric(
                label=key,
                value=value,
            )


# =========================================================
# CALCULATOR HEADER
# =========================================================

def calculator_header(
    icon,
    title,
    subtitle,
):

    render_html(
        f"""
        <div class="eyebrow">
            Quantity Takeoff
        </div>

        <div class="page-title">
            {icon} {title}
        </div>

        <div class="page-subtitle">
            {subtitle}
        </div>
        """
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html(
        """
        <div class="brand">

            <div class="brand-top">

                <div class="brand-icon">
                    🏗️
                </div>

                <div class="brand-name">
                    Civil <span>QuantEstimate</span>
                </div>

            </div>

            <div class="brand-sub">
                CIVIL ENGINEERING QUANTITY TAKEOFF
            </div>

        </div>
        """
    )

    render_html(
        '<div class="nav-label">WORKSPACE</div>'
    )

    nav_button(
        "⌂  Dashboard",
        "Dashboard",
    )

    render_html(
        '<div class="nav-label">QUANTITY TAKEOFF</div>'
    )

    nav_button(
        "🧱  Brickwork",
        "Brickwork",
    )

    nav_button(
        "🪣  Plaster",
        "Plaster",
    )

    nav_button(
        "🏗️  Concrete / RCC",
        "Concrete / RCC",
    )

    nav_button(
        "🔩  Steel / BBS",
        "Steel / BBS",
    )

    render_html(
        '<div class="nav-label">AI TOOLS</div>'
    )

    nav_button(
        "✨  CiviGuide AI",
        "CiviGuide AI",
    )

    render_html(
        """
        <div class="sidebar-bottom">

            Formula-based estimates for
            faster quantity takeoff.

            <br><br>

            <strong>CiviGuide AI</strong>
            provides civil-engineering
            guidance for your calculations.

            <br><br>

            v1.0 · Hackathon Edition

        </div>
        """
    )


# =========================================================
# TOP BAR
# =========================================================

top1, top2, top3 = st.columns(
    [5.5, 1.1, 1.1]
)

with top1:

    render_html(
        """
        <div class="eyebrow">
            Civil QuantEstimate Workspace
        </div>
        """
    )


with top2:

    pdf_data = (
        make_pdf(
            st.session_state.last_result,
            st.session_state.last_module,
        )
        if st.session_state.last_result
        else b""
    )

    st.download_button(
        "📄 PDF",
        data=pdf_data,
        file_name="civil_quantestimate_report.pdf",
        mime="application/pdf",
        disabled=not bool(pdf_data),
        use_container_width=True,
    )


with top3:

    json_data = (
        save_result(
            st.session_state.last_result,
            st.session_state.last_module,
        )
        if st.session_state.last_result
        else b"{}"
    )

    st.download_button(
        "💾 Save",
        data=json_data,
        file_name="civil_quantestimate_result.json",
        mime="application/json",
        disabled=not bool(
            st.session_state.last_result
        ),
        use_container_width=True,
    )


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    render_html(
        """
        <div class="welcome">

            <span class="badge">
                🏗️ SMART QUANTITY TAKEOFF
            </span>

            <h1>
                Build smarter.
                <span>Estimate faster.</span>
            </h1>

            <p>
                Calculate construction quantities using
                transparent engineering formulas, organize
                your results, and get civil-engineering
                guidance from CiviGuide AI.
            </p>

        </div>
        """
    )

    count = st.session_state.calculation_count

    time_saved = count * 0.25

    time_text = (
        f"{time_saved:.1f} hrs"
        if time_saved
        else "0 hrs"
    )

    m1, m2, m3, m4 = st.columns(4)

    cards = [

        (
            "🧮",
            "Total Calculations",
            str(count),
            "This session",
        ),

        (
            "⏱️",
            "Time Saved",
            time_text,
            "Estimated 15 min / calculation",
        ),

        (
            "✓",
            "Formula Accuracy",
            "100%",
            "Deterministic formula engine",
        ),

        (
            "📐",
            "Takeoff Modules",
            "4",
            "Brick · Plaster · Concrete · Steel",
        ),
    ]

    for col, card in zip(
        (m1, m2, m3, m4),
        cards,
    ):

        icon, label, value, note = card

        with col:

            render_html(
                f"""
                <div class="metric">

                    <div class="metric-icon">
                        {icon}
                    </div>

                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>

                    <div class="metric-note">
                        {note}
                    </div>

                </div>
                """
            )

    render_html(
        """
        <div class="section-title">
            Quantity Takeoff
        </div>

        <div class="section-sub">
            Choose what you want to estimate.
        </div>
        """
    )

    tools = [

        (
            "🧱",
            "Brickwork",
            "Bricks, masonry volume and mortar requirements.",
            "Brickwork",
        ),

        (
            "🪣",
            "Plaster",
            "Plaster area, mortar and material quantities.",
            "Plaster",
        ),

        (
            "🏗️",
            "Concrete / RCC",
            "Concrete volume and mix material quantities.",
            "Concrete / RCC",
        ),

        (
            "🔩",
            "Steel / BBS",
            "Reinforcement bar weight and wastage.",
            "Steel / BBS",
        ),
    ]

    cols = st.columns(4)

    for col, tool in zip(
        cols,
        tools,
    ):

        icon, title, description, target = tool

        with col:

            render_html(
                f"""
                <div class="tool-card">

                    <div class="tool-icon">
                        {icon}
                    </div>

                    <div class="tool-title">
                        {title}
                    </div>

                    <div class="tool-desc">
                        {description}
                    </div>

                </div>
                """
            )

            if st.button(
                f"Open {title} →",
                key=f"dashboard_{target}",
                use_container_width=True,
            ):

                st.session_state.page = target

                st.rerun()

    render_html(
        """
        <div class="section-title">
            CiviGuide AI
        </div>

        <div class="section-sub">
            Your civil-engineering quantity copilot.
        </div>

        <div class="ai-panel">

            <div class="tool-icon">
                ✨
            </div>

            <h3>
                CiviGuide AI
            </h3>

            <p>
                Ask about quantity estimation,
                formulas, mix ratios, reinforcement,
                or your latest calculation.
            </p>

        </div>
        """
    )

    if st.button(
        "Open CiviGuide AI →",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.page = "CiviGuide AI"

        st.rerun()


# =========================================================
# BRICKWORK
# =========================================================

elif st.session_state.page == "Brickwork":

    calculator_header(
        "🧱",
        "Brickwork Estimator",
        "Estimate wall masonry, bricks and mortar requirements.",
    )

    left, right = st.columns(2)

    with left:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Wall Dimensions
                </div>
            """
        )

        length = st.number_input(
            "Wall Length (m)",
            min_value=0.0,
            value=10.0,
            step=0.1,
        )

        height = st.number_input(
            "Wall Height (m)",
            min_value=0.0,
            value=3.0,
            step=0.1,
        )

        thickness = st.number_input(
            "Wall Thickness (m)",
            min_value=0.01,
            value=0.23,
            step=0.01,
        )

        quantity = st.number_input(
            "Number of Walls",
            min_value=1,
            value=1,
            step=1,
        )

        render_html(
            """
            </div>
            """
        )

    with right:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Material Settings
                </div>
            """
        )

        mortar_ratio = st.selectbox(
            "Mortar Ratio",
            list(MORTAR_RATIOS.keys()),
            index=min(
                2,
                len(MORTAR_RATIOS) - 1,
            ),
        )

        wastage = st.number_input(
            "Wastage (%)",
            min_value=0.0,
            value=float(
                WASTAGE_DEFAULTS["brickwork"]
            ),
            step=0.5,
        )

        opening_area = st.number_input(
            "Total Opening Area (m²)",
            min_value=0.0,
            value=2.1,
            step=0.1,
        )

        render_html(
            """
            </div>
            """
        )

    render_html(
        """
        <div class="helper">
            Enter the total door/window opening area
            to subtract it from the wall.
        </div>
        """
    )

    if st.button(
        "Calculate Brickwork",
        type="primary",
        use_container_width=True,
    ):

        results = calc_brickwork(
            length,
            height,
            thickness,
            quantity,
            mortar_ratio,
            wastage,
            opening_area,
        )

        show_results(
            "Brickwork",
            results,
        )


# =========================================================
# PLASTER
# =========================================================

elif st.session_state.page == "Plaster":

    calculator_header(
        "🪣",
        "Plaster Estimator",
        "Estimate plaster area and mortar material requirements.",
    )

    left, right = st.columns(2)

    with left:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Surface Dimensions
                </div>
            """
        )

        length = st.number_input(
            "Length (m)",
            min_value=0.0,
            value=10.0,
            step=0.1,
        )

        height = st.number_input(
            "Height (m)",
            min_value=0.0,
            value=3.0,
            step=0.1,
        )

        quantity = st.number_input(
            "Number of Surfaces",
            min_value=1,
            value=1,
            step=1,
        )

        opening_area = st.number_input(
            "Opening Area to Subtract (m²)",
            min_value=0.0,
            value=2.1,
            step=0.1,
        )

        render_html(
            """
            </div>
            """
        )

    with right:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Plaster Settings
                </div>
            """
        )

        thickness_mm = st.number_input(
            "Plaster Thickness (mm)",
            min_value=1.0,
            value=12.0,
            step=1.0,
        )

        mortar_ratio = st.selectbox(
            "Mortar Ratio",
            list(MORTAR_RATIOS.keys()),
            index=min(
                1,
                len(MORTAR_RATIOS) - 1,
            ),
        )

        wastage = st.number_input(
            "Wastage (%)",
            min_value=0.0,
            value=float(
                WASTAGE_DEFAULTS["plaster"]
            ),
            step=0.5,
        )

        render_html(
            """
            </div>
            """
        )

    if st.button(
        "Calculate Plaster",
        type="primary",
        use_container_width=True,
    ):

        results = calc_plaster(
            length,
            height,
            quantity,
            thickness_mm,
            mortar_ratio,
            wastage,
            opening_area,
        )

        show_results(
            "Plaster",
            results,
        )


# =========================================================
# CONCRETE / RCC
# =========================================================

elif st.session_state.page == "Concrete / RCC":

    calculator_header(
        "🏗️",
        "Concrete / RCC Estimator",
        "Estimate concrete volume and mix material quantities.",
    )

    left, right = st.columns(2)

    with left:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Element Dimensions
                </div>
            """
        )

        length = st.number_input(
            "Length (m)",
            min_value=0.0,
            value=5.0,
            step=0.1,
        )

        width = st.number_input(
            "Width (m)",
            min_value=0.0,
            value=0.3,
            step=0.05,
        )

        thickness = st.number_input(
            "Thickness / Depth (m)",
            min_value=0.0,
            value=0.15,
            step=0.01,
        )

        quantity = st.number_input(
            "Number of Elements",
            min_value=1,
            value=1,
            step=1,
        )

        render_html(
            """
            </div>
            """
        )

    with right:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Concrete Settings
                </div>
            """
        )

        mix_ratio = st.selectbox(
            "Mix Ratio",
            list(CONCRETE_RATIOS.keys()),
            index=min(
                1,
                len(CONCRETE_RATIOS) - 1,
            ),
        )

        wastage = st.number_input(
            "Wastage (%)",
            min_value=0.0,
            value=float(
                WASTAGE_DEFAULTS["concrete"]
            ),
            step=0.5,
        )

        render_html(
            """
            <div class="helper">
                Select the concrete grade / nominal mix
                used for your estimate.
            </div>

            </div>
            """
        )

    if st.button(
        "Calculate Concrete",
        type="primary",
        use_container_width=True,
    ):

        results = calc_concrete(
            length,
            width,
            thickness,
            quantity,
            mix_ratio,
            wastage,
        )

        show_results(
            "Concrete / RCC",
            results,
        )


# =========================================================
# STEEL / BBS
# =========================================================

elif st.session_state.page == "Steel / BBS":

    calculator_header(
        "🔩",
        "Steel / BBS Estimator",
        "Estimate reinforcement bar quantities and steel weight.",
    )

    left, right = st.columns(2)

    with left:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Bar Details
                </div>
            """
        )

        bar_dia = st.selectbox(
            "Bar Diameter (mm)",
            STEEL_BAR_SIZES_MM,
            index=min(
                3,
                len(STEEL_BAR_SIZES_MM) - 1,
            ),
        )

        bar_length = st.number_input(
            "Bar Length (m)",
            min_value=0.0,
            value=6.0,
            step=0.1,
        )

        no_of_bars = st.number_input(
            "Number of Bars",
            min_value=1,
            value=10,
            step=1,
        )

        render_html(
            """
            </div>
            """
        )

    with right:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Wastage
                </div>
            """
        )

        wastage = st.number_input(
            "Wastage (%)",
            min_value=0.0,
            value=float(
                WASTAGE_DEFAULTS["steel"]
            ),
            step=0.5,
        )

        render_html(
            """
            <div class="helper">
                Use the total number and length of
                bars for this estimate.
            </div>

            </div>
            """
        )

    if st.button(
        "Calculate Steel",
        type="primary",
        use_container_width=True,
    ):

        results = calc_steel(
            bar_dia,
            bar_length,
            no_of_bars,
            wastage,
        )

        show_results(
            "Steel / BBS",
            results,
        )


# =========================================================
# CIVIGUIDE AI
# =========================================================

elif st.session_state.page == "CiviGuide AI":

    calculator_header(
        "✨",
        "CiviGuide AI",
        "Your AI assistant for civil engineering and quantity estimation.",
    )

    if st.session_state.last_result:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Latest Calculation
                </div>
            """
        )

        st.caption(
            st.session_state.last_module
        )

        st.json(
            st.session_state.last_result
        )

        render_html(
            """
            </div>
            """
        )

        st.write("")

    question = st.text_area(
        "Ask CiviGuide",
        placeholder=(
            "Example: Explain how the mortar quantity "
            "in my brickwork result was calculated."
        ),
        height=140,
    )

    if st.button(
        "✨ Ask CiviGuide",
        type="primary",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            context = (
                str(st.session_state.last_result)
                if st.session_state.last_result
                else "No calculation has been made yet."
            )

            with st.spinner(
                "CiviGuide is thinking..."
            ):

                answer = ask_groq(
                    question,
                    context,
                )

            render_html(
                """
                <div class="ai-panel">

                    <div class="tool-icon">
                        ✨
                    </div>

                    <h3>
                        CiviGuide Response
                    </h3>

                </div>
                """
            )

            st.markdown(answer)


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="footer">

        Civil QuantEstimate ·
        Formula-based quantity takeoff ·
        CiviGuide AI ·
        Hackathon Edition

    </div>
    """
)
