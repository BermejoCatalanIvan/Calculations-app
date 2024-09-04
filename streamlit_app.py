import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from datetime import datetime

# Helper functions
def format_number(num):
    return "{:,.2f}".format(num)

def format_percentage(num):
    return "{:.2f}%".format(num * 100)

def parse_number(num_str):
    try:
        return float(num_str.replace(',', ''))
    except ValueError:
        return 0.0

def create_pdf(calculations, title):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50
    y_position = height - margin

    # Set Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y_position, title)
    y_position -= 30

    # Include Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.setFont("Helvetica", 10)
    c.drawString(margin, y_position, f"Generated on: {timestamp}")
    y_position -= 20

    # Add a divider below the timestamp
    c.setStrokeColor(colors.black)
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 30

    # Define the desired order of sections
    section_order = list(calculations.keys())

    # Iterate over each section in the defined order
    for section in section_order:
        if section in calculations:
            if y_position < 100:  # Start a new page if too close to the bottom
                c.showPage()
                y_position = height - margin

            # Print section title
            if section != "affiliate_info":  # Skip the affiliate_info title
                c.setFont("Helvetica-Bold", 14)
                c.drawString(margin, y_position, section)
                y_position -= 20

            # Print section content
            c.setFont("Helvetica", 12)
            for label, value in calculations[section].items():
                c.drawString(margin, y_position, f"{label}: {value}")
                y_position -= 20

            # Add a divider line between sections
            c.setStrokeColor(colors.black)
            c.line(margin, y_position + 10, width - margin, y_position + 10)

            y_position -= 30  # Extra spacing after divider

    c.save()
    buffer.seek(0)
    return buffer

def download_pdf(calculations, title):
    pdf = create_pdf(calculations, title)
    st.download_button(
        label=f"Download {title} as PDF",
        data=pdf,
        file_name=f"{title.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

# Initialize session state
if 'calculations' not in st.session_state:
    st.session_state['calculations'] = {}
if 'all_calculations_done' not in st.session_state:
    st.session_state['all_calculations_done'] = False

# Custom CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    
    body {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    .stApp {
        background-color: #000000 !important;
    }

    .main .block-container {
        background-color: #000000 !important;
        border-radius: 0px !important;
        padding: 2rem 1rem !important;
    }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    h1, h2, h3, h4, .stHeader, .stFooter, .stText, .stTabs, p, label {
        color: #FFFFFF !important;
    }

    h1, h2, h3, h4 {
        color: #FFC000 !important;
    }

    .stButton>button {
        background-color: #FFC000;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border: 2px solid #000000 !important;
        text-align: center !important;
    }

    .stDownloadButton > button {
        background-color: #FFC000 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border: 2px solid #000000 !important;
        text-align: center !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #E5A800 !important;
        color: #000000 !important;
    }

    .stMarkdown > div > div > div > .stMarkdown > div:nth-child(2) > div {
        background-color: #FFC000 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    .positive-roi {
        background-color: #ccffcc !important;
        color: #006400 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    .stTabs [role="tablist"] .stTabsContainer {
        background-color: #1e1e1e !important;
        border-radius: 12px !important;
    }

    hr {
        border: 1px solid #FFC000 !important;
    }

    img {
        margin-bottom: 20px !important;
    }

    </style>
""", unsafe_allow_html=True)

# Centered ApeX Logo
st.markdown("""
    <div class="centered-logo">
        <img src="https://thewealthmastery.io/wp-content/uploads/2022/12/Apex-1024x536.jpg" width="400">
    </div>
""", unsafe_allow_html=True)

st.title("BD's Calculator Tool")

# Create tabs
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "INFO", 
    "EFFECTIVE COMMISSION", 
    "MAX PAYMENTS", 
    "Net Zero Point", 
    "Volume Requirements", 
    "ROI", 
    "SCENARIO"
])

# Tab 0: INFO
with tab0:
    st.header("Affiliate/KOL Information")
    st.write("""
        Please enter the Affiliate or KOL's name along with the Lead or Account number ID from Salesforce.
    """)
    affiliate_name = st.text_input("Affiliate/KOL Name:")
    salesforce_id = st.text_input("Lead or Account Number ID:")
    incentive_number = st.text_input("Incentive Number:")

    # Store the information in session state
    if st.button("Save Information"):
        st.session_state['calculations']["affiliate_info"] = {
            "Affiliate/KOL Name": affiliate_name,
            "Lead/Account Number ID": salesforce_id,
            "Incentive Number": incentive_number
        }
        st.success("Information saved successfully.")

    # Individual Print Button
    if "affiliate_info" in st.session_state['calculations']:
        download_pdf({"Affiliate/KOL Information": st.session_state['calculations']["affiliate_info"]}, "Affiliate_KOL_Information")

# Tab 1: Effective Commission Calculator
with tab1:
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
    volume_options = list(range(10, 101, 5)) + list(range(125, 301, 25))
    volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_0") * 1_000_000
    volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_0")
    volume = volume_select if parse_number(volume_input) == 0 else parse_number(volume_input)
    
    affiliate_commission_options = [x/100 for x in range(0, 61, 5)]
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
                    f"<div class='positive-roi'>"
                    f"{effective_commission_str}"
                    f"</div>",
                    unsafe_allow_html=True
                )

            # Store the result in session state, including the selected Affiliate and Master Affiliate Commission percentages
            st.session_state['calculations']["Effective Commission"] = {
                "Affiliate Commission": f"{format_percentage(aff_commission)}",
                "Master Affiliate Commission": f"{format_percentage(master_aff_commission)}",
                "Margin Commission": f"{format_percentage(margin_commission_percentage)}",
                "Effective Commission": f"{effective_commission_str}"
            }

    # Individual Print Button
    if "Effective Commission" in st.session_state['calculations']:
        download_pdf({"Effective Commission": st.session_state['calculations']["Effective Commission"]}, "Effective_Commission")

# Tab 2: Max Bonus & Payments Calculator
with tab2:
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

        # Store the result in session state
        st.session_state['calculations']["Max Bonus & Payments"] = {
            "Maximum Allowable Bonus & Payments": f"${format_number(max_bonus_payments)}"
        }

    # Individual Print Button
    if "Max Bonus & Payments" in st.session_state['calculations']:
        download_pdf({"Max Bonus & Payments": st.session_state['calculations']["Max Bonus & Payments"]}, "Max_Bonus_Payments")

# Tab 3: Net Zero Point Calculator (formerly Break-even)
with tab3:
    st.header("Net Zero Point Calculator")
    st.write("""
        This tab calculates the volume needed to reach the Net Zero Point based on the total budget and effective commission.
    """)
    st.latex(r'''
    \text{Trading Volume} = \frac{ \text{Budget} }{ \text{Average ApeX Fee} \times ( 1 - \text{Affiliate Commission} - \text{Master Affiliate Commission} ) }
    ''')
    st.write("""
        **Guide:**
        - **Total Budget for Net Zero Point:** Enter the total budget in dollars.
        - **Affiliate Commission:** Select the affiliate commission percentage.
        - **Master Affiliate Commission:** Select the master affiliate commission percentage.
    """)
    st.divider()

    # Inputs for the calculator
    budget_str = st.text_input("Enter Total Budget for Net Zero Point ($):", key="budget_str_1", value=format_number(6000.0))
    
    aff_commission = st.selectbox("Affiliate Commission:", options=affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="affiliate_commission_net_zero")
    master_aff_commission = st.selectbox("Master Affiliate Commission:", options=master_affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="master_affiliate_commission_net_zero")
    
    average_apex_fee = 0.000475

    # Calculate button
    if st.button("Calculate Net Zero Volume"):
        # Parse inputs
        budget = parse_number(budget_str)

        # Calculate Target Volume for Net Zero Point
        trading_volume_net_zero = budget / (average_apex_fee * (1 - aff_commission - master_aff_commission))

        # Display Results
        st.write("### Results")

        st.write("#### Net Zero Trading Volume")
        st.info(f"{format_number(trading_volume_net_zero)}")

        st.write("### Possible Outcomes")

        # Calculate possible outcomes
        positive_scenarios = [trading_volume_net_zero * (1 + x/100) for x in [15, 30]]
        negative_scenarios = [trading_volume_net_zero * (1 - x/100) for x in [15, 30]]

        # Display positive scenarios
        st.write("#### Positive Scenarios")
        st.info(f"Scenario 1 (+15%): {format_number(positive_scenarios[0])}")
        st.info(f"Scenario 2 (+30%): {format_number(positive_scenarios[1])}")

        # Display negative scenarios
        st.write("#### Negative Scenarios")
        st.info(f"Scenario 1 (-15%): {format_number(negative_scenarios[0])}")
        st.info(f"Scenario 2 (-30%): {format_number(negative_scenarios[1])}")

        # Store the result in session state
        st.session_state['calculations']["Net Zero Volume"] = {
            "Net Zero Trading Volume": f"{format_number(trading_volume_net_zero)}",
            "Positive Scenario 1": f"{format_number(positive_scenarios[0])}",
            "Positive Scenario 2": f"{format_number(positive_scenarios[1])}",
            "Negative Scenario 1": f"{format_number(negative_scenarios[0])}",
            "Negative Scenario 2": f"{format_number(negative_scenarios[1])}"
        }

    # Individual Print Button
    if "Net Zero Volume" in st.session_state['calculations']:
        download_pdf({"Net Zero Volume": st.session_state['calculations']["Net Zero Volume"]}, "Net_Zero_Volume")

# Tab 4: Volume Requirements Calculator
with tab4:
    st.header("Volume Requirements Calculator")
    st.write("""
        This tab calculates the volume required to achieve the desired bonus based on the fixed effective commission of 65%, 
        affiliate commission, and master affiliate commission.
    """)
    st.latex(r'''
    \text{Volume Required} = \frac{\text{Bonus}}{0.65 - \left( \text{Affiliate Commission} + \text{Master Affiliate Commission} \right) } \times \frac{1}{\text{Average ApeX Fee}}
    ''')
    st.write("""
        **Guide:**
        - **Bonus ($):** Enter the desired bonus in dollars.
        - **Affiliate Commission:** Select the affiliate commission percentage.
        - **Master Affiliate Commission:** Select the master affiliate commission percentage.
    """)
    st.divider()

    # Inputs for the calculator
    bonus_str = st.text_input("Enter Desired Bonus ($):", key="bonus_str_1", value="2000.00")
    aff_commission = st.selectbox("Affiliate Commission:", options=affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="affiliate_commission_vol_req")
    master_aff_commission = st.selectbox("Master Affiliate Commission:", options=master_affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="master_affiliate_commission_vol_req")

    average_apex_fee = 0.000475

    # Calculate button
    if st.button("Calculate Volume Requirements"):
        # Parse inputs
        bonus = parse_number(bonus_str)

        # Calculate Volume Required
        try:
            # Calculate the denominator (65% - (Affiliate Commission + Master Affiliate Commission))
            effective_commission = 0.65 - (aff_commission + master_aff_commission)

            if effective_commission <= 0:
                raise ValueError("The effective commission must be less than 65%.")

            # Calculate Volume Required
            volume_required = (bonus / effective_commission) / average_apex_fee

            # Display Results
            st.write("### Results")

            st.write("#### Volume Required")
            st.info(f"{format_number(volume_required / 1_000_000)} M")

            # Store the result in session state
            st.session_state['calculations']["Volume Required"] = {
                "Bonus": f"${format_number(bonus)}",
                "Affiliate Commission": f"{format_percentage(aff_commission)}",
                "Master Affiliate Commission": f"{format_percentage(master_aff_commission)}",
                "Volume Required": f"{format_number(volume_required / 1_000_000)} M"
            }

        except ValueError as e:
            st.error(str(e))

    # Individual Print Button
    if "Volume Required" in st.session_state['calculations']:
        download_pdf({"Volume Required": st.session_state['calculations']["Volume Required"]}, "Volume_Required")

# Tab 5: ROI Calculation
with tab5:
    st.header("ROI Calculation")
    st.write("""
        This tab calculates the standard ROI based on the given volume, budget, and effective commission.
    """)
    st.latex(r'''
    \text{ROI} = \frac{\text{ApeX Generated Fee} - \text{Budget}}{\text{Generated Affiliate Commission} + \text{Generated Master Affiliate Commission} + \text{Budget}} \times 100
    ''')
    st.write("""
        **Guide:**
        - **Introduce Volume (in millions):** Select or enter the trading volume.
        - **Affiliate Commission:** Select the affiliate commission percentage.
        - **Master Affiliate Commission:** Select the master affiliate commission percentage.
        - **Total Budget:** Enter the total budget in dollars.
    """)
    st.divider()

    # Inputs for the calculator
    target_volume_select = st.selectbox("Introduce Volume (in millions):", volume_options, key="volume_select_3") * 1_000_000
    target_volume_input = st.text_input("Or enter specific Volume:", value="0", key="volume_input_3")
    target_volume = target_volume_select if parse_number(target_volume_input) == 0 else parse_number(target_volume_input)

    aff_commission = st.selectbox("Affiliate Commission:", options=affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="affiliate_commission_roi")
    master_aff_commission = st.selectbox("Master Affiliate Commission:", options=master_affiliate_commission_options, format_func=lambda x: f"{int(x * 100)}%", key="master_affiliate_commission_roi")
    
    budget_str = st.text_input("Enter Total Budget ($):", value=format_number(7000.0), key="budget_str_2")

    # Calculate button
    if st.button("Calculate", key="calculate_standard"):
        # Parse inputs
        budget = parse_number(budget_str)
        
        average_apex_fee = 0.000475

        # Standard Calculation
        # Calculate Total Trading Fee
        total_trading_fee = target_volume * average_apex_fee

        # Calculate Generated Affiliate and Master Affiliate Commissions
        generated_affiliate_commission = total_trading_fee * aff_commission
        generated_master_affiliate_commission = total_trading_fee * master_aff_commission

        # Calculate ApeX Generated Fee
        apex_generated_fee = total_trading_fee * (1 - aff_commission - master_aff_commission)

        # Calculate ROI
        total_affiliate_spend = generated_affiliate_commission + generated_master_affiliate_commission + budget
        roi = ((apex_generated_fee - budget) / total_affiliate_spend) * 100 if total_affiliate_spend != 0 else 0

        # Store inputs in session_state for use in the scenario tab
        st.session_state['roi_target_volume'] = target_volume
        st.session_state['roi_budget'] = budget
        st.session_state['roi_affiliate_commission'] = aff_commission
        st.session_state['roi_master_affiliate_commission'] = master_aff_commission
        st.session_state['roi_apex_generated_fee'] = apex_generated_fee
        st.session_state['roi'] = roi
        st.session_state['roi_total_trading_fee'] = total_trading_fee

        # Standard Result
        st.write("### Standard Calculation")
        st.write("#### Volume Selected")
        st.info(f"{format_number(target_volume)}")

        st.write("#### ApeX Generated Fee")
        st.info(f"${format_number(apex_generated_fee)}")

        st.write("#### ROI")
        st.info(f"{format_number(roi)}%")

        # Store the result in session state
        st.session_state['calculations']["Standard ROI Calculation"] = {
            "Volume Selected": f"{format_number(target_volume)}",
            "ApeX Generated Fee": f"${format_number(apex_generated_fee)}",
            "ROI": f"{format_number(roi)}%"
        }

    # Individual Print Button
    if "Standard ROI Calculation" in st.session_state['calculations']:
        download_pdf({"Standard ROI Calculation": st.session_state['calculations']["Standard ROI Calculation"]}, "Standard_ROI_Calculation")

# Tab 6: Scenario Calculation
with tab6:
    st.header("Scenario Calculation")
    st.write("""
        This tab calculates the expected volume and ROI based on various market scenarios, applying the new ROI formula.
    """)
    st.latex(r'''
    \text{ROI} = \frac{\text{ApeX Generated Fee} - \text{Budget}}{\text{Generated Affiliate Commission} + \text{Generated Master Affiliate Commission} + \text{Budget}} \times 100
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
        affiliate_commission = st.session_state['roi_affiliate_commission']
        master_affiliate_commission = st.session_state['roi_master_affiliate_commission']
        apex_generated_fee = st.session_state['roi_apex_generated_fee']
        roi = st.session_state['roi']
    else:
        st.error("Please complete the ROI Calculation tab first.")
        st.stop()

    # Scenario multipliers with descriptions
    market_sentiment = st.selectbox("Market Sentiment (MS):", ["Positive (1.2)", "Neutral (1.0)", "Negative (0.5)"], index=0, key="market_sentiment")
    apex_status = st.selectbox("ApeX Status, Liquidity & Pairs (AS):", ["High (1.1)", "Neutral (1.0)", "Low (0.9)"], index=0, key="apex_status")
    kol_influence = st.selectbox("KOL Influence (KI):", ["High (1.3)", "Neutral (1.0)", "Low (0.7)"], index=2, key="kol_influence")
    affiliate_engagement = st.selectbox("Affiliate Engagement (AE):", ["High (1.25)", "Neutral (1.0)", "Low (0.75)"], index=1, key="affiliate_engagement")

    # Calculate button
    if st.button("Calculate Scenario", key="calculate_scenario"):
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
        total_trading_fee_scenario = v_expected_scenario * 0.000475

        # Calculate Generated Affiliate and Master Affiliate Commissions in Scenario
        generated_affiliate_commission_scenario = total_trading_fee_scenario * affiliate_commission
        generated_master_affiliate_commission_scenario = total_trading_fee_scenario * master_affiliate_commission

        # Calculate ApeX Generated Fee in Scenario
        apex_generated_fee_scenario = total_trading_fee_scenario * (1 - affiliate_commission - master_affiliate_commission)

        # Calculate ROI in Scenario
        total_affiliate_spend_scenario = generated_affiliate_commission_scenario + generated_master_affiliate_commission_scenario + budget
        roi_scenario = ((apex_generated_fee_scenario - budget) / total_affiliate_spend_scenario) * 100 if total_affiliate_spend_scenario != 0 else 0

        st.write("### Comparison with Scenario Multipliers")

        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Standard Calculation")
            st.write("**Volume Selected**")
            st.info(f"{format_number(base_volume)}")
            st.write("**ApeX Generated Fee**")
            st.info(f"${format_number(apex_generated_fee)}")
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

        # Store the result in session state
        st.session_state['calculations']["Scenario Calculation"] = {
            "Volume Selected": f"{format_number(base_volume)}",
            "ApeX Generated Fee with Scenario": f"${format_number(apex_generated_fee_scenario)}",
            "ROI with Scenario": f"{format_number(roi_scenario)}%"
        }

    # Individual Print Button
    if "Scenario Calculation" in st.session_state['calculations']:
        download_pdf({"Scenario Calculation": st.session_state['calculations']["Scenario Calculation"]}, "Scenario_Calculation")

