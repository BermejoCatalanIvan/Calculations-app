import streamlit as st

# Helper function to format numbers with thousand separators
def format_number(num):
    return "{:,.2f}".format(num)

def format_percentage(num):
    return "{:.2f}%".format(num * 100)

def parse_number(num_str):
    try:
        return float(num_str.replace(',', ''))
    except ValueError:
        return 0.0

st.title("ROI Calculators")

# Create tabs
tab0, tab1, tab2, tab3 = st.tabs(["Effective Commission Calculator", "Break-even Volume Calculator", "Standard Calculation", "Scenario Calculation"])

# Tab 0: Effective Commission Calculator
with tab0:
    st.header("Effective Commission Calculator")

    # Inputs for the calculator
    volume_options = list(range(10, 101, 10)) + list(range(125, 301, 25))
    volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_0") * 1_000_000
    volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_0")
    volume = volume_select if parse_number(volume_input) == 0 else parse_number(volume_input)
    
    affiliate_commission_options = [x/100 for x in range(20, 61, 5)]
    master_affiliate_commission_options = [x/100 for x in range(4, 11)]
    
    aff_commission = st.selectbox("Affiliate Commission:", options=affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="aff_commission_0")
    master_aff_commission = st.selectbox("Master Affiliate Commission:", options=master_affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="master_aff_commission_0")
    bonus_str = st.text_input("Bonus ($):", value="0.00", key="bonus_0")
    payments_str = st.text_input("Payments ($):", value="0.00", key="payments_0")

    # Calculate button
    if st.button("Calculate Effective Commission"):
        # Parse inputs
        bonus = parse_number(bonus_str)
        payments = parse_number(payments_str)

        if bonus == 0 and payments == 0:
            st.error("Either Bonus or Payments must be greater than zero.")
        else:
            # Calculate Fee Income
            average_apex_fee = 0.000475
            fee_income = volume * average_apex_fee

            # Calculate Margin
            margin = fee_income / (bonus + payments)

            # Calculate Total Commission
            total_commission = aff_commission + master_aff_commission + (margin / 100)

            # Display Results
            st.write("### Results")

            st.write("#### Effective Commission")
            st.info(f"{format_percentage(total_commission)}")

# Tab 1: Break-even Volume Calculator
with tab1:
    st.header("Break-even Volume Calculator")

    # Inputs for the calculator
    budget_str = st.text_input("Enter Total Budget for Break-even ($):", key="budget_str_1", value=format_number(6000.0))
    volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_1") * 1_000_000
    volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_1")
    volume = volume_select if parse_number(volume_input) == 0 else parse_number(volume_input)
    
    affiliate_effective_commission_options = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    affiliate_effective_commission = st.selectbox(
        "Affiliate Effective Commission:", 
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

# Tab 2: Standard Calculation
with tab2:
    st.header("Standard Calculation")

    # Inputs for the calculator
    target_volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_2") * 1_000_000
    target_volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_2")
    target_volume = target_volume_select if parse_number(target_volume_input) == 0 else parse_number(target_volume_input)

    affiliate_effective_commission_options = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
    affiliate_effective_commission = st.selectbox(
        "Affiliate Effective Commission:", 
        options=affiliate_effective_commission_options, 
        format_func=lambda x: f"{int(x * 100)}%",
        key="affiliate_effective_commission_standard"
    )
    budget_str = st.text_input("Enter Total Budget ($):", value=format_number(7000.0), key="budget_str_2")

    # Calculate button
    if st.button("Calculate", key="calculate_standard"):
        # Parse inputs
        budget = parse_number(budget_str)
        
        average_apex_fee = 0.000475

        # Standard Calculation
        # Calculate Total Trading Fee
        total_trading_fee = target_volume * average_apex_fee

        # Calculate ApeX Generated Fee
        apex_generated_fee = total_trading_fee * (1 - affiliate_effective_commission)

        # Calculate Effective Commission
        effective_commission = affiliate_effective_commission

        # Calculate ROI
        roi = ((apex_generated_fee - budget) / budget) * 100 if budget != 0 else 0

        # Store inputs in query parameters for use in the third tab
        st.experimental_set_query_params(
            target_volume=format_number(target_volume),
            budget_str=budget_str,
            affiliate_effective_commission=affiliate_effective_commission
        )

        # Standard Result
        st.write("### Standard Calculation")
        st.write("#### Total Trading Fee")
        st.info(f"${format_number(total_trading_fee)}")

        st.write("#### ApeX Generated Fee")
        st.info(f"${format_number(apex_generated_fee)}")

        st.write("#### ROI")
        st.info(f"{format_number(roi)}%")

# Tab 3: Scenario Calculation
with tab3:
    st.header("Scenario Calculation")

    # Retrieve stored inputs from query parameters
    query_params = st.experimental_get_query_params()
    base_volume = parse_number(query_params.get('target_volume', ["0"])[0])
    budget_str = query_params.get('budget_str', ["0"])[0]
    affiliate_effective_commission = float(query_params.get('affiliate_effective_commission', [0.5])[0])

    # Inputs for the calculator
    base_volume_str = st.text_input("Enter Base Volume for Scenario Calculation:", value=format_number(base_volume), key="base_volume_str")
    base_volume = parse_number(base_volume_str)

    # Scenario multipliers with descriptions
    market_sentiment = st.selectbox("Market Sentiment (MS):", ["Positive (1.2)", "Neutral (1.0)", "Negative (0.8)"], index=0, key="market_sentiment")
    apex_status = st.selectbox("ApeX Status, Liquidity & Pairs (AS):", ["High (1.1)", "Neutral (1.0)", "Low (0.9)"], index=0, key="apex_status")
    kol_influence = st.selectbox("KOL Influence (KI):", ["High (1.3)", "Neutral (1.0)", "Low (0.7)"], index=2, key="kol_influence")
    affiliate_engagement = st.selectbox("Affiliate Engagement (AE):", ["High (1.25)", "Neutral (1.0)", "Low (0.75)"], index=1, key="affiliate_engagement")

    # Calculate button
    if st.button("Calculate", key="calculate_scenario"):
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

        # Calculate expected volume with scenario multipliers
        v_expected_scenario = base_volume * ms_multiplier * as_multiplier * ki_multiplier * ae_multiplier
        apex_generated_fee_scenario = v_expected_scenario * average_apex_fee * (1 - affiliate_effective_commission)
        roi_scenario = ((apex_generated_fee_scenario - budget) / budget) * 100 if budget != 0 else 0

        st.write("### Calculation with Scenario Multipliers")
        st.write("#### Expected Volume with Scenario")
        st.info(f"{format_number(v_expected_scenario)}")

        st.write("#### ApeX Generated Fee with Scenario")
        st.info(f"${format_number(apex_generated_fee_scenario)}")

        st.write("#### ROI with Scenario")
        st.info(f"{format_number(roi_scenario)}%")
