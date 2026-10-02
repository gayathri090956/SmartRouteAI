import streamlit as st
import pandas as pd
import pickle


# =========================================================
# LOAD MODEL
# =========================================================

try:
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("❌ model.pkl not found. Please run: python train_model.py")
    st.stop()


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="SmartRoute AI",
    page_icon="🚦",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🚦 SmartRoute AI")

st.subheader(
    "ML-Based Traffic-Aware Route Recommendation System"
)

st.write(
    """
    SmartRoute AI predicts travel time and compares alternative
    routes using traffic, construction, drainage, road condition,
    weather, distance and time of day.
    """
)

st.divider()


# =========================================================
# ROUTE INFORMATION
# =========================================================

st.header("📍 Route Information")

col1, col2 = st.columns(2)

with col1:
    source = st.text_input(
        "Starting Location",
        "Majestic"
    )

with col2:
    destination = st.text_input(
        "Destination",
        "Whitefield"
    )


# =========================================================
# CURRENT ROAD CONDITIONS
# =========================================================

st.header("🚦 Current Road Conditions")

col1, col2, col3 = st.columns(3)

with col1:
    traffic = st.slider(
        "Traffic Level",
        min_value=1,
        max_value=5,
        value=3
    )

with col2:
    construction = st.selectbox(
        "Construction Site",
        ["No", "Yes"]
    )

with col3:
    drainage = st.selectbox(
        "Drainage / Waterlogging",
        ["No", "Yes"]
    )


# =========================================================
# OTHER CONDITIONS
# =========================================================

st.header("🌦️ Other Conditions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    road_condition = st.slider(
        "Road Condition",
        min_value=1,
        max_value=5,
        value=4
    )

with col2:
    weather = st.selectbox(
        "Weather",
        ["Normal", "Rain", "Heavy Rain"]
    )

with col3:
    distance = st.number_input(
        "Distance (km)",
        min_value=1.0,
        max_value=50.0,
        value=5.0,
        step=0.5
    )

with col4:
    time = st.slider(
        "Time of Day",
        min_value=0,
        max_value=23,
        value=8
    )


# =========================================================
# CONVERT INPUT VALUES
# =========================================================

construction_value = 1 if construction == "Yes" else 0

drainage_value = 1 if drainage == "Yes" else 0


if weather == "Normal":
    weather_value = 1
elif weather == "Rain":
    weather_value = 2
else:
    weather_value = 3


# =========================================================
# FIND BEST ROUTE BUTTON
# =========================================================

if st.button(
    "🔍 Find Best Route",
    use_container_width=True
):

    # =====================================================
    # CURRENT ROUTE
    # =====================================================

    current_route = pd.DataFrame({
        "Traffic_Level": [traffic],
        "Construction": [construction_value],
        "Drainage_Leak": [drainage_value],
        "Road_Condition": [road_condition],
        "Weather": [weather_value],
        "Distance_km": [distance],
        "Time_of_Day": [time]
    })

    predicted_time = model.predict(current_route)[0]


    # =====================================================
    # CURRENT ROUTE ANALYSIS
    # =====================================================

    st.divider()

    st.header("📊 Current Route Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Predicted Travel Time",
            f"{predicted_time:.1f} min"
        )

    with col2:
        st.metric(
            "Distance",
            f"{distance:.1f} km"
        )

    with col3:

        if traffic <= 2:
            traffic_status = "Low Traffic"
        elif traffic == 3:
            traffic_status = "Moderate Traffic"
        else:
            traffic_status = "Heavy Traffic"

        st.metric(
            "Traffic Status",
            traffic_status
        )


    # =====================================================
    # WARNINGS
    # =====================================================

    st.header("⚠️ Route Warnings")

    warnings = []

    if traffic >= 4:
        warnings.append(
            "🚦 Heavy traffic detected."
        )

    if construction_value == 1:
        warnings.append(
            "🚧 Construction activity detected."
        )

    if drainage_value == 1:
        warnings.append(
            "💧 Drainage / waterlogging problem detected."
        )

    if weather_value == 2:
        warnings.append(
            "🌧️ Rain may increase travel time."
        )

    if weather_value == 3:
        warnings.append(
            "⛈️ Heavy rain may significantly affect travel."
        )

    if road_condition <= 2:
        warnings.append(
            "🛣️ Poor road condition detected."
        )

    if len(warnings) > 0:

        for warning in warnings:
            st.warning(warning)

    else:

        st.success(
            "✅ No major road problems detected."
        )


    # =====================================================
    # ALTERNATIVE ROUTES
    # =====================================================

    st.divider()

    st.header("🛣️ Alternative Route Comparison")

    st.write(
        "The system compares three possible route scenarios "
        "and predicts the expected travel time for each."
    )


    # =====================================================
    # ROUTE A - MAIN ROAD
    # =====================================================

    route_a = pd.DataFrame({
        "Traffic_Level": [traffic],
        "Construction": [construction_value],
        "Drainage_Leak": [drainage_value],
        "Road_Condition": [road_condition],
        "Weather": [weather_value],
        "Distance_km": [distance],
        "Time_of_Day": [time]
    })


    # =====================================================
    # ROUTE B - ALTERNATIVE ROAD
    # =====================================================

    route_b = pd.DataFrame({
        "Traffic_Level": [
            max(1, traffic - 1)
        ],

        "Construction": [0],

        "Drainage_Leak": [0],

        "Road_Condition": [4],

        "Weather": [weather_value],

        "Distance_km": [
            distance + 1
        ],

        "Time_of_Day": [time]
    })


    # =====================================================
    # ROUTE C - OUTER ROAD
    # =====================================================

    route_c = pd.DataFrame({
        "Traffic_Level": [
            max(1, traffic - 2)
        ],

        "Construction": [0],

        "Drainage_Leak": [0],

        "Road_Condition": [5],

        "Weather": [weather_value],

        "Distance_km": [
            distance + 2
        ],

        "Time_of_Day": [time]
    })


    # =====================================================
    # PREDICT TRAVEL TIME
    # =====================================================

    time_a = model.predict(route_a)[0]

    time_b = model.predict(route_b)[0]

    time_c = model.predict(route_c)[0]


    # =====================================================
    # DISPLAY THREE ROUTES
    # =====================================================

    col1, col2, col3 = st.columns(3)


    # -----------------------------------------------------
    # ROUTE A
    # -----------------------------------------------------

    with col1:

        st.subheader("🛣️ Route A")

        st.write("**Main Road**")

        st.metric(
            "Distance",
            f"{distance:.1f} km"
        )

        st.metric(
            "Predicted Time",
            f"{time_a:.1f} min"
        )

        st.write(
            f"Traffic Level: {traffic}/5"
        )


    # -----------------------------------------------------
    # ROUTE B
    # -----------------------------------------------------

    with col2:

        st.subheader("🛣️ Route B")

        st.write("**Alternative Road**")

        st.metric(
            "Distance",
            f"{distance + 1:.1f} km"
        )

        st.metric(
            "Predicted Time",
            f"{time_b:.1f} min"
        )

        st.write(
            f"Traffic Level: {max(1, traffic - 1)}/5"
        )


    # -----------------------------------------------------
    # ROUTE C
    # -----------------------------------------------------

    with col3:

        st.subheader("🛣️ Route C")

        st.write("**Outer Road**")

        st.metric(
            "Distance",
            f"{distance + 2:.1f} km"
        )

        st.metric(
            "Predicted Time",
            f"{time_c:.1f} min"
        )

        st.write(
            f"Traffic Level: {max(1, traffic - 2)}/5"
        )


    # =====================================================
    # COMPARISON TABLE
    # =====================================================

    st.subheader("📋 Route Comparison Table")

    route_results = pd.DataFrame({

        "Route": [
            "Route A - Main Road",
            "Route B - Alternative Road",
            "Route C - Outer Road"
        ],

        "Distance (km)": [
            round(distance, 1),
            round(distance + 1, 1),
            round(distance + 2, 1)
        ],

        "Traffic Level": [
            traffic,
            max(1, traffic - 1),
            max(1, traffic - 2)
        ],

        "Predicted Travel Time (min)": [
            round(time_a, 1),
            round(time_b, 1),
            round(time_c, 1)
        ]
    })


    st.dataframe(
        route_results,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # FIND FASTEST ROUTE
    # =====================================================

    route_times = [
        time_a,
        time_b,
        time_c
    ]

    best_index = route_times.index(
        min(route_times)
    )


    route_names = [
        "Route A - Main Road",
        "Route B - Alternative Road",
        "Route C - Outer Road"
    ]


    best_route = route_names[best_index]

    best_time = route_times[best_index]


    # =====================================================
    # RECOMMENDATION
    # =====================================================

    st.success(
        f"""
        🚗 **Recommended Route: {best_route}**

        Predicted travel time: **{best_time:.1f} minutes**
        """
    )


    # =====================================================
    # WHY THIS ROUTE?
    # =====================================================

    st.subheader("💡 Why this route?")

    if best_index == 0:

        st.write(
            """
            Route A has the lowest predicted travel time
            among the three simulated route scenarios.
            """
        )

    elif best_index == 1:

        st.write(
            """
            Route B has reduced traffic and avoids the
            construction and drainage problems of the main route.
            """
        )

    else:

        st.write(
            """
            Route C has lower traffic and better road conditions,
            which results in a lower predicted travel time.
            """
        )


# =========================================================
# MAP
# =========================================================

st.divider()

st.header("🗺️ Traffic Area Visualization")

st.write(
    """
    Demonstration map showing example locations.
    This prototype can later be connected to real-time
    traffic, weather, construction and mapping APIs.
    """
)


map_data = pd.DataFrame({

    "lat": [
        12.9716,
        12.9784,
        12.9850,
        12.9950,
        13.0050
    ],

    "lon": [
        77.5946,
        77.6000,
        77.6100,
        77.6200,
        77.6300
    ]
})


st.map(map_data)


# =========================================================
# ABOUT PROJECT
# =========================================================

st.divider()

st.header("🤖 About SmartRoute AI")

st.write(
    """
    SmartRoute AI is a Machine Learning prototype designed
    to support traffic-aware route planning.

    The Random Forest Regression model predicts travel time
    using:

    • Traffic level
    • Construction activity
    • Drainage / waterlogging
    • Road condition
    • Weather
    • Distance
    • Time of day

    The system compares three simulated route scenarios
    and recommends the route with the lowest predicted
    travel time.
    """
)


st.caption(
    "SmartRoute AI | Machine Learning Internship Project"
)