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

st.title("BDs Calculator")

# Create tabs
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "EFFECTIVE COMMISSION", 
    "MAX PAYMENTS", 
    "BREAK-EVEN", 
    "ROI", 
    "SCENARIO"
])

# Tab 0: Effective Commission Calculator
with tab0:
    st.header("Effective Commission Calculator")
    st.write("""
        This tab calculates the effective commission based on the given Affiliate Commission, Master Affiliate Commission, Bonus, and Payments.
    """)
    st.latex(r'''
    \text{Effective Commission} = \text{Affiliate Commission} + \text{Master Affiliate Commission} + \left( \frac{\text{Bonus} + \text{Payments}}{\text{Fee Income}} \right)
    ''')
    st.write("""
        **Guide:**
        - **Introduce Volume (in millions):** Select or enter the trading volume.
        - **Affiliate Commission:** Select the affiliate commission percentage.
        - **Master Affiliate Commission:** Select the master affiliate commission percentage.
        - **Bonus:** Enter the bonus amount in dollars.
        - **Payments:** Enter the payment amount in dollars.
    """)
    st.divider()

    # Inputs for the calculator
    volume_options = list(range(10, 101, 10)) + list(range(125, 301, 25))
    volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_0") * 1_000_000
    volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_0")
    volume = volume_select if parse_number(volume_input) == 0 else parse_number(volume_input)
    
    affiliate_commission_options = [x/100 for x in range(20, 61, 5)]
    master_affiliate_commission_options = [x/100 for x in range(0, 21)]
    
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

            # Calculate Margin Commission as a percentage
            margin_commission_percentage = (bonus + payments) / fee_income

            # Calculate Total Commission
            total_commission = aff_commission + master_aff_commission + margin_commission_percentage

            # Display Results
            st.write("### Results")

            st.write("#### Margin Commission")
            st.info(f"{format_percentage(margin_commission_percentage)}")

            st.write("#### Effective Commission")
            effective_commission_str = f"{format_percentage(total_commission)}"
            if total_commission > 0.65:
                st.markdown(
                    f"<div style='background-color: #ffcccc; padding: 20px; border-radius: 5px; text-align: center;'>"
                    f"<span style='color:red; font-size:24px; font-weight:bold;'>{effective_commission_str}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color: #ccffcc; padding: 20px; border-radius: 5px; text-align: center;'>"
                    f"<span style='font-size:24px; font-weight:bold;'>{effective_commission_str}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

# Tab 1: Max Bonus & Payments Calculator
with tab1:
    st.header("Max Bonus & Payments Calculator")
    st.write("""
        This tab calculates the maximum allowable sum of bonus and payments that can be offered to the affiliate without surpassing a 65% effective commission.
    """)
    st.latex(r'''
    \text{Max (Bonus + Payments)} = \left( 0.65 - \text{Affiliate Commission} - \text{Master Affiliate Commission} \right) \times ( \text{Volume} \times \text{Average ApeX Fee} )
    ''')
    st.write("""
        **Guide:**
        - **Introduce Volume (in millions):** Select or enter the trading volume.
        - **Affiliate Commission:** Select the affiliate commission percentage.
        - **Master Affiliate Commission:** Select the master affiliate commission percentage.
    """)
    st.divider()

    # Inputs for the calculator
    volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_1") * 1_000_000
    volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_1")
    volume = volume_select if parse_number(volume_input) == 0 else parse_number(volume_input)
    
    aff_commission = st.selectbox("Affiliate Commission:", options=affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="aff_commission_1")
    master_aff_commission = st.selectbox("Master Affiliate Commission:", options=master_affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="master_aff_commission_1")

    # Calculate button
    if st.button("Calculate Max (Bonus + Payments)"):
        # Calculate Fee Income
        average_apex_fee = 0.000475
        fee_income = volume * average_apex_fee

        # Calculate Margin Commission as a percentage
        margin_commission_percentage = (0.65 - aff_commission - master_aff_commission)

        # Calculate Max (Bonus + Payments)
        max_bonus_payments = margin_commission_percentage * fee_income

        # Display Results
        st.write("### Results")

        st.write("#### Maximum Allowable Bonus & Payments")
        st.info(f"${format_number(max_bonus_payments)}")

# Tab 2: Break-even Volume Calculator
with tab2:
    st.header("Break-even Volume Calculator")
    st.write("""
        This tab calculates the volume needed to reach the break-even point based on the total budget and effective commission.
    """)
    st.latex(r'''
    \text{Trading Volume} = \frac{ \text{Budget} }{ \text{Average ApeX Fee} \times ( 1 - \text{Affiliate Effective Commission} ) }
    ''')
    st.write("""
        **Guide:**
        - **Total Budget for Break-even:** Enter the total budget in dollars.
        - **Affiliate Effective Commission:** Select the effective commission percentage.
    """)
    st.divider()

    # Inputs for the calculator
    budget_str = st.text_input("Enter Total Budget for Break-even ($):", key="budget_str_1", value=format_number(6000.0))
    
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

        # Calculate Target Volume for Break Even Point
        trading_volume_break_even = budget / (average_apex_fee * (1 - affiliate_effective_commission))

        # Display Results
        st.write("### Results")

        st.write("#### Break Even Trading Volume")
        st.info(f"{format_number(trading_volume_break_even)}")

        st.write("### Possible ROI Outcomes")

        # Calculate possible ROI outcomes
        roi_positive_scenarios = [trading_volume_break_even * (1 + x/100) for x in [15, 30]]
        roi_negative_scenarios = [trading_volume_break_even * (1 - x/100) for x in [15, 30]]

        # Display positive scenarios
        st.write("#### Positive Scenarios")
        st.info(f"Scenario 1 (+15% ROI): {format_number(roi_positive_scenarios[0])}")
        st.info(f"Scenario 2 (+30% ROI): {format_number(roi_positive_scenarios[1])}")

        # Display negative scenarios
        st.write("#### Negative Scenarios")
        st.info(f"Scenario 1 (-15% ROI): {format_number(roi_negative_scenarios[0])}")
        st.info(f"Scenario 2 (-30% ROI): {format_number(roi_negative_scenarios[1])}")

# Tab 3: Standard Calculation
with tab3:
    st.header("ROI Calculation")
    st.write("""
        This tab calculates the standard ROI based on the given volume, budget, and effective commission.
    """)
    st.latex(r'''
    \text{ROI} = \left( \frac{ \text{ApeX Generated Fee} - \text{Budget} }{ \text{Budget} } \right) \times 100
    ''')
    st.write("""
        **Guide:**
        - **Introduce Volume (in millions):** Select or enter the trading volume.
        - **Affiliate Effective Commission:** Select the effective commission percentage.
        - **Total Budget:** Enter the total budget in dollars.
    """)
    st.divider()

    # Inputs for the calculator
    target_volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_3") * 1_000_000
    target_volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_3")
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

        # Store inputs in session_state for use in the scenario tab
        st.session_state['roi_target_volume'] = target_volume
        st.session_state['roi_budget'] = budget
        st.session_state['roi_affiliate_effective_commission'] = affiliate_effective_commission
        st.session_state['roi_apex_generated_fee'] = apex_generated_fee
        st.session_state['roi'] = roi
        st.session_state['roi_total_trading_fee'] = total_trading_fee

        # Standard Result
        st.write("### Standard Calculation")
        st.write("#### Total Trading Fee")
        st.info(f"${format_number(total_trading_fee)}")

        st.write("#### ApeX Generated Fee")
        st.info(f"${format_number(apex_generated_fee)}")

        st.write("#### ROI")
        st.info(f"{format_number(roi)}%")

# Tab 4: Scenario Calculation
with tab4:
    st.header("Scenario Calculation")
    st.write("""
        This tab calculates the expected volume and ROI based on various market scenarios.
    """)
    st.latex(r'''
    \text{Expected Volume} = \text{Base Volume} \times \text{MS} \times \text{AS} \times \text{KI} \times \text{AE}
    ''')
    st.write("""
        **Guide:**
        - **Market Sentiment (MS):** Select the market sentiment multiplier.
        - **ApeX Status, Liquidity & Pairs (AS):** Select the ApeX status multiplier.
        - **KOL Influence (KI):** Select the KOL influence multiplier.
        - **Affiliate Engagement (AE):** Select the affiliate engagement multiplier.
    """)
    st.divider()

    # Retrieve stored inputs from session_state
    if 'roi_target_volume' in st.session_state:
        base_volume = st.session_state['roi_target_volume']
        budget = st.session_state['roi_budget']
        affiliate_effective_commission = st.session_state['roi_affiliate_effective_commission']
        apex_generated_fee = st.session_state['roi_apex_generated_fee']
        roi = st.session_state['roi']
        total_trading_fee = st.session_state['roi_total_trading_fee']
    else:
        st.error("Please complete the ROI Calculation tab first.")
        st.stop()

    # Scenario multipliers with descriptions
    market_sentiment = st.selectbox("Market Sentiment (MS):", ["Positive (1.2)", "Neutral (1.0)", "Negative (0.5)"], index=0, key="market_sentiment")
    apex_status = st.selectbox("ApeX Status, Liquidity & Pairs (AS):", ["High (1.1)", "Neutral (1.0)", "Low (0.9)"], index=0, key="apex_status")
    kol_influence = st.selectbox("KOL Influence (KI):", ["High (1.3)", "Neutral (1.0)", "Low (0.7)"], index=2, key="kol_influence")
    affiliate_engagement = st.selectbox("Affiliate Engagement (AE):", ["High (1.25)", "Neutral (1.0)", "Low (0.75)"], index=1, key="affiliate_engagement")

    # Calculate button
    if st.button("Calculate", key="calculate_scenario"):
        # Define multipliers
        ms_dict = {"Positive (1.2)": 1.2, "Neutral (1.0)": 1.0, "Negative (0.5)": 0.5}
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
        apex_generated_fee_scenario = v_expected_scenario * 0.000475 * (1 - affiliate_effective_commission)
        roi_scenario = ((apex_generated_fee_scenario - budget) / budget) * 100 if budget != 0 else 0

        st.write("### Comparison with Scenario Multipliers")

        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Standard Calculation")
            st.write("**Volume Selected**")
            st.info(f"{format_number(base_volume)}")
            st.write("**Total Trading Fee**")
            st.info(f"${format_number(total_trading_fee)}")
            st.write("**ROI**")
            st.info(f"{format_number(roi)}%")

        with col2:
            st.write("#### Scenario Calculation")
            st.write("**Expected Volume with Scenario**")
            st.info(f"{format_number(v_expected_scenario)}")
            st.write("**ApeX Generated Fee with Scenario**")
            st.info(f"${format_number(apex_generated_fee_scenario)}")
            st.write("**ROI with Scenario**")
            st.info(f"{format_number(roi_scenario)}%")
