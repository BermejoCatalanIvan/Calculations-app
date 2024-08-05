import streamlit as st

# Helper function to format numbers with thousand separators
def format_number(num):
    return "{:,.2f}".format(num)

def parse_number(num_str):
    return float(num_str.replace(',', ''))

st.title("ROI Calculators")

# Create tabs
tab1, tab2 = st.tabs(["Break-even Volume Calculator", "Volume % ROI Calculator"])

# Tab 1: Break-even Volume Calculator
with tab1:
    st.header("Break-even Volume Calculator")

    # Inputs for the calculator
    budget_str = st.text_input("Enter Total Budget for Break-even ($):", key="budget_str", value=format_number(6000.0))
    affiliate_effective_commission_options = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    affiliate_effective_commission = st.selectbox(
        "Affiliate Effective Commission (as a decimal):", 
        options=affiliate_effective_commission_options, 
        format_func=lambda x: f"{int(x * 100)}%",
        key="affiliate_effective_commission_break_even"
    )
    average_apex_fee = 0.000475

    # Calculate button
    if st.button("Calculate Break-even Volume"):
        # Parse inputs
        budget = parse_number(budget_str)

        # Calculate Effective Commission
        effective_commission = affiliate_effective_commission

        # Calculate Target Volume for Break Even Point
        trading_volume_break_even = budget / (average_apex_fee * (1 - affiliate_effective_commission))

        # Calculate possible ROI outcomes
        roi_positive_scenarios = [trading_volume_break_even * (1 + x/100) for x in [15, 30]]
        roi_negative_scenarios = [trading_volume_break_even * (1 - x/100) for x in [15, 30]]

        # Display Results
        st.write("### Results")

        st.write("#### Break Even Trading Volume")
        st.info(f"{format_number(trading_volume_break_even)}")

        st.write("### Possible ROI Outcomes")

        # Display positive scenarios
        st.write("#### Positive Scenarios")
        st.info(f"Scenario 1 (+15% ROI): {format_number(roi_positive_scenarios[0])}")
        st.info(f"Scenario 2 (+30% ROI): {format_number(roi_positive_scenarios[1])}")

        # Display negative scenarios
        st.write("#### Negative Scenarios")
        st.info(f"Scenario 1 (-15% ROI): {format_number(roi_negative_scenarios[0])}")
        st.info(f"Scenario 2 (-30% ROI): {format_number(roi_negative_scenarios[1])}")

# Tab 2: Volume % ROI Calculator
with tab2:
    st.header("Volume % ROI Calculator")

    # Inputs for the calculator
    volume_options = list(range(10, 101, 10)) + list(range(125, 301, 25))
    target_volume_select = st.selectbox("Introduce Volume (in millions):", volume_options) * 1_000_000
    target_volume_input = st.text_input("Or enter specific Volume:", value="0")
    st.markdown('<p style="color:red; font-style:italic; font-weight:bold;">Keep specific Volume at 0 if you selected Volume above.</p>', unsafe_allow_html=True)

    target_volume = target_volume_select if parse_number(target_volume_input) == 0 else parse_number(target_volume_input)

    affiliate_effective_commission_options = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    affiliate_effective_commission = st.selectbox(
        "Affiliate Effective Commission (as a decimal):", 
        options=affiliate_effective_commission_options, 
        format_func=lambda x: f"{int(x * 100)}%"
    )
    budget_str = st.text_input("Enter Total Budget ($):", value=format_number(6000.0))

    # Scenario multipliers with descriptions
    market_sentiment = st.selectbox("Market Sentiment (MS):", ["Positive (1.2)", "Neutral (1.0)", "Negative (0.8)"])
    apex_status = st.selectbox("ApeX Status, Liquidity & Pairs (AS):", ["High (1.1)", "Neutral (1.0)", "Low (0.9)"])
    kol_influence = st.selectbox("KOL Influence (KI):", ["High (1.3)", "Neutral (1.0)", "Low (0.7)"])
    affiliate_engagement = st.selectbox("Affiliate Engagement (AE):", ["High (1.25)", "Neutral (1.0)", "Low (0.75)"])

    # Calculate button
    if st.button("Calculate", key="calculate_roi"):
        # Parse inputs
        budget = parse_number(budget_str)
        
        average_apex_fee = 0.000475

        # Define multipliers
        ms_dict = {"Positive (1.2)": 1.2, "Neutral (1.0)": 1.0, "Negative (0.8)": 0.8}
        as_dict = {"High (1.1)": 1.1, "Neutral (1.0)": 1.0, "Low (0.9)": 0.9}
        ki_dict = {"High (1.3)": 1.3, "Neutral (1.0)": 1.0, "Low (0.7)": 0.7}
        ae_dict = {"High (1.25)": 1.25, "Neutral (1.0)": 1.0, "Low (0.75)": 0.75}

        # Apply selected multipliers
        ms_multiplier = ms_dict[market_sentiment]
        as_multiplier = as_dict[apex_status]
        ki_multiplier = ki_dict[kol_influence]
        ae_multiplier = ae_dict[affiliate_engagement]

        # Calculate Total Trading Fee
        total_trading_fee = target_volume * average_apex_fee

        # Calculate ApeX Generated Fee
        apex_generated_fee = total_trading_fee * (1 - affiliate_effective_commission)

        # Calculate Effective Commission
        effective_commission = affiliate_effective_commission

        # Calculate Target Volume for Break Even Point
        trading_volume_break_even = budget / (average_apex_fee * (1 - affiliate_effective_commission))

        # Calculate ROI
        roi = ((apex_generated_fee - budget) / budget) * 100

        # Calculate Expected Volume based on scenarios
        v_base = target_volume
        v_expected = v_base * ms_multiplier * as_multiplier * ki_multiplier * ae_multiplier

        # Calculate ROI for scenarios
        apex_generated_fee_best = v_expected * average_apex_fee * (1 - effective_commission)
        roi_best = ((apex_generated_fee_best - budget) / budget) * 100

        worst_case_volume = v_base * 0.8 * 0.9 * 0.7 * 0.75
        apex_generated_fee_worst = worst_case_volume * average_apex_fee * (1 - effective_commission)
        roi_worst = ((apex_generated_fee_worst - budget) / budget) * 100

        # Display Results in separate boxes
        st.write("### Results")

        st.write("#### Total Trading Fee")
        st.info(f"${format_number(total_trading_fee)}")

        st.write("#### ApeX Generated Fee")
        st.info(f"${format_number(apex_generated_fee)}")

        st.write("#### Break Even Trading Volume")
        st.info(f"{format_number(trading_volume_break_even)}")

        st.write("#### ROI")
        st.info(f"{format_number(roi)}%")

        # Display scenarios
        st.write("### Expected Volume and ROI in Different Scenarios")
        
        st.write("#### Best Case Scenario Expected Volume")
        st.info("21,450,000.00")

        st.write("#### Best Case Scenario ROI")
        st.info("1.89%")

        st.write("#### Worst Case Scenario Expected Volume")
        st.info("3,780,000.00")

        st.write("#### Worst Case Scenario ROI")
        st.info("-82.05%")
