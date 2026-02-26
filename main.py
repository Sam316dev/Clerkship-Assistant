import streamlit as st
import random

st.set_page_config(page_title="Dr. Sam's EMR", page_icon="🩺", layout="wide")

# ==========================================
# SIDEBAR: PATIENT DATA ERASURE
# ==========================================
with st.sidebar:
    st.markdown("### Session Control")
    st.info("Ensure patient privacy on the wards. Erase data before clerking the next patient.")
    if st.button("Erase Data & Start New Patient", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# CUSTOM UI INJECTION
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    .stButton>button {
        background-color: #0056b3; color: white; border-radius: 8px; font-weight: 600;
        border: none; padding: 10px 24px; width: 100%; transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #003d82; color: white; box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    .streamlit-expanderHeader {
        font-weight: 600 !important; color: #004085 !important;
        background-color: #e2eef9 !important; border-radius: 6px; border: 1px solid #b8daff;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #d1e7dd; border-radius: 6px 6px 0px 0px;
        padding: 10px 20px; font-weight: 500; color: #0f5132;
    }
    .stTabs [aria-selected="true"] { background-color: #0056b3; color: white; font-weight: bold; }
    p, span, label { color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER & CLINICAL DISCLAIMERS
# ==========================================
header_images = [
    "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=1200&q=80"
]
selected_image = random.choice(header_images)

st.markdown(f"""
    <div style="background-image: linear-gradient(rgba(0, 50, 100, 0.7), rgba(0, 50, 100, 0.7)), url('{selected_image}'); 
                background-size: cover; background-position: center; border-radius: 12px; padding: 40px; 
                text-align: center; color: white; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h1 style="color: white; font-size: 3em; margin-bottom: 0px;">🩺 Dr. Sam's Clerkship Assistant</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">Clinical Reasoning & Case Formulation Tool</p>
    </div>
""", unsafe_allow_html=True)

st.error("**CLINICAL DISCLAIMER:** This tool does not diagnose patients. It is designed to assist medical students in structuring case presentations and developing differential reasoning. Always correlate clinically.", icon="⚠️")

# ==========================================
# INITIALIZE VARIABLES & CLINICAL FLAGS
# ==========================================
r_haem_o, r_cv_o, r_gi_o, r_gu_o, r_neuro_o, r_msk_o, r_endo_o = "", "", "", "", "", "", ""
occ_other, eth_other, rel_other, pmh_other, all_other, comp_other, fhx_other, h_other, sys_other = "", "", "", "", "", "", "", "", ""

flag_malignancy_keyword = False
flag_stroke, flag_seizure, flag_meningism, flag_sol, flag_neuropathy = [False]*5
flag_chronic_cough, flag_hemoptysis, flag_purulent_sputum, flag_sudden_dyspnea, flag_pleuritic_pain, flag_nocturnal_symptoms = [False]*6
flag_polyuria, flag_hyperthyroid, flag_hypothyroid, flag_compressive_goiter, flag_weight_loss_paradox = [False]*5
flag_ischemic_pain, flag_heart_failure, flag_arrhythmia, flag_cardiac_syncope = [False]*4
flag_gi_bleed, flag_jaundice, flag_peritonitis, flag_obstruction, flag_pud = [False]*5
flag_hematuria, flag_renal_colic, flag_luts, flag_nephrotic_edema, flag_uremia = [False]*5
flag_anemia, flag_scd_crisis, flag_plt_bleed, flag_coag_bleed, flag_lymphoma = [False]*5

hpc_narratives, complaint_names_for_summary = [], []
systemic, pmh_list = [], []
allergies, compliance = "No", "Select..."
smoking, alcohol, housing = "Never", "None", "Adequate"
cigs_per_day, years_smoked, pack_years = 0, 0, 0.0
alcohol_type, bottles_per_week = "None", 0
sex_active, partners, protection, sti_hx = "Declined to answer", "N/A", "N/A", "N/A"

pallor, icterus, cyanosis, clubbing, edema, lymph = "Absent", "Absent", "Absent", "Absent", "Absent", "Absent"
temp, hr, rr, bp_sys, bp_dia = 37.0, 80, 16, 120, 80

pulse_rhythm, pulse_char, jvp_status, apex_loc, heaves_thrills, heart_sounds, murmur = "Regular", "Normal volume", "Not elevated", "5th ICS", "Absent", "S1 and S2", "None"
gi_inspection, gi_palpation, gi_organomegaly, gi_percussion, gi_auscultation = [], "Soft, non-tender", "None", "Normal tympany", "Normal active"
renal_inspection, renal_palpation, renal_auscultation, fluid_status = [], "Non-tender", "No bruits", "Euvolemic"
gcs_score = 15
cranial_nerves, motor_tone, motor_power, reflexes, plantar_response, meningeal_signs = "Intact", "Normal tone", "Grade 5/5", "Normoreflexia", "Flexor", "Absent"
haem_signs, haem_lymph, haem_spleen = [], "No palpable nodes", "Not palpable"
resp_inspection, trachea_palpation, resp_percussion, resp_auscultation, resp_added_sounds = [], "Central", "Resonant", "Vesicular", []
neck_insp, neck_palp, eye_s, trem_s = "Normal", "Normal", "Normal", "Absent"

tab_hx, tab_pe, tab_dx = st.tabs(["History Taking", "Physical Examination", "Case Formulation & Discussion"])

# ==========================================
# TAB 1: HISTORY TAKING
# ==========================================
with tab_hx:
    with st.expander("1. Demographics (NASAROME)", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Patient Alias / Bed No.", value="Bed 1")
            age = st.number_input("Age", 0, 120, 45)
            sex = st.selectbox("Sex", ["Select", "Male", "Female"])
        with col2:
            address = st.text_input("Address (Endemic area check)")
            religion = st.selectbox("Religion", ["Select", "Christianity", "Islam", "Traditional", "Other"])
            if religion == "Other": rel_other = st.text_input("Specify Religion:")
            marital = st.selectbox("Marital Status", ["Select", "Single", "Married", "Divorced", "Widowed", "Other"])
        with col3:
            occupation = st.selectbox("Occupation", ["Civil Servant", "Trader", "Student", "Unemployed", "Retired", "Other"])
            if occupation == "Other": occ_other = st.text_input("Specify Occupation:")
            ethnicity = st.selectbox("Ethnicity", ["Select", "Yoruba", "Igbo", "Hausa", "Other"])
            if ethnicity == "Other": eth_other = st.text_input("Specify Ethnicity:")

    with st.expander("2 & 3. Presenting Complaints & HPC", expanded=True):
        units_selected = st.multiselect("Select Internal Medicine Unit(s)", ["Cardiology", "Respiratory", "Gastroenterology", "Nephrology", "Endocrinology", "Neurology", "Haematology"], default=["Cardiology"])
        
        if "Cardiology" in units_selected:
            st.markdown("#### 🫀 Cardiology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_c")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Chest Pain", "Palpitations", "Shortness of Breath (Dyspnea)", "Lower Limb Swelling (Edema)", "Fainting (Syncope)", "Other"], key=f"cpc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"cdur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Minutes", "Hours", "Days", "Weeks", "Months"], key=f"cdu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Chest Pain":
                        complaint_names_for_summary.append("Chest Pain")
                        cp_char = st.selectbox("Character", ["Select...", "Crushing/Heavy/Tightness", "Sharp/Stabbing", "Tearing"], key=f"cc_{i}")
                        cp_rad = st.selectbox("Radiation", ["Select...", "Left arm/Jaw/Neck", "Back", "No radiation"], key=f"crad_{i}")
                        cp_exert = st.selectbox("Relation to Exertion", ["Select...", "Occurs at rest", "Brought on by exertion, relieved by rest"], key=f"cex_{i}")
                        if cp_char == "Crushing/Heavy/Tightness" or cp_rad == "Left arm/Jaw/Neck": flag_ischemic_pain = True
                        narrative += f"Character is {cp_char.lower()}, radiating to {cp_rad.lower()}. Exertion relation: {cp_exert.lower()}."
                    elif pc == "Palpitations":
                        complaint_names_for_summary.append("Palpitations")
                        palp_reg = st.selectbox("Rhythm", ["Select...", "Regular and fast", "Irregularly irregular (skipped beats)"], key=f"creg_{i}")
                        if palp_reg == "Irregularly irregular (skipped beats)": flag_arrhythmia = True
                        narrative += f"Described as {palp_reg.lower()}."
                    elif pc == "Shortness of Breath (Dyspnea)":
                        complaint_names_for_summary.append("Dyspnea")
                        orthopnea = st.selectbox("Orthopnea", ["No", "Yes (Uses multiple pillows)"], key=f"cort_{i}")
                        pnd = st.selectbox("Paroxysmal Nocturnal Dyspnea (PND)", ["No", "Yes (Wakes up gasping)"], key=f"cpnd_{i}")
                        if orthopnea != "No" or pnd != "No": flag_heart_failure = True
                        narrative += f"Orthopnea: {orthopnea.lower()}, PND: {pnd.lower()}."
                    elif pc == "Lower Limb Swelling (Edema)":
                        complaint_names_for_summary.append("Pedal Edema")
                        edema_type = st.selectbox("Type", ["Select...", "Bilateral, ascending, pitting", "Unilateral, painful"], key=f"ced_{i}")
                        if "Bilateral" in edema_type: flag_heart_failure = True
                        narrative += f"Swelling is {edema_type.lower()}."
                    elif pc == "Fainting (Syncope)":
                        complaint_names_for_summary.append("Syncope")
                        syncope_trigger = st.selectbox("Trigger", ["Select...", "During exertion (Cardiac)", "After standing up (Postural)", "Emotional stress/pain (Vasovagal)"], key=f"csyn_{i}")
                        if "Cardiac" in syncope_trigger: flag_cardiac_syncope = True
                        narrative += f"Triggered {syncope_trigger.lower()}."
                    elif pc == "Other":
                        other_pc = st.text_input("Specify:", key=f"copc_{i}")
                        complaint_names_for_summary.append(other_pc)
                        narrative = f"**{other_pc.capitalize()}** for {duration_num} {duration_unit}."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Respiratory" in units_selected:
            st.markdown("#### 🫁 Respiratory")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_r")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Cough", "Breathlessness (Dyspnea)", "Chest Pain (Pleuritic)", "Hemoptysis", "Other"], key=f"rpc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"rdur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Days", "Weeks", "Months", "Years"], key=f"rdu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Cough":
                        complaint_names_for_summary.append("Cough")
                        if duration_num >= 3 and duration_unit in ["Weeks", "Months", "Years"]: flag_chronic_cough = True
                        cough_type = st.selectbox("Type of Cough", ["Select...", "Dry / Non-productive", "Productive (Sputum)"], key=f"rct_{i}")
                        narrative += f"The cough is {cough_type.lower()}. "
                        if cough_type == "Productive (Sputum)":
                            sputum_color = st.selectbox("Sputum Color", ["Select...", "Clear/White", "Yellow/Green", "Rusty", "Pink frothy"], key=f"rsc_{i}")
                            if sputum_color in ["Yellow/Green", "Rusty"]: flag_purulent_sputum = True
                            blood = st.selectbox("Blood in sputum?", ["No", "Blood-streaked", "Frank Hemoptysis"], key=f"rbld_{i}")
                            if blood != "No": flag_hemoptysis = True
                            narrative += f"Productive of {sputum_color.lower()} sputum, with {blood.lower()} blood. "
                    elif pc == "Breathlessness (Dyspnea)":
                        complaint_names_for_summary.append("Dyspnea")
                        breath_onset = st.selectbox("Onset", ["Select...", "Sudden (Minutes/Hours)", "Gradual (Days/Weeks)"], key=f"rbo_{i}")
                        if breath_onset == "Sudden (Minutes/Hours)": flag_sudden_dyspnea = True
                        narrative += f"Onset was {breath_onset.lower()}."
                    elif pc == "Chest Pain (Pleuritic)":
                        complaint_names_for_summary.append("Pleuritic Chest Pain")
                        flag_pleuritic_pain = True
                        narrative += "Pain is pleuritic (worse on deep inspiration)."
                    elif pc == "Hemoptysis":
                        complaint_names_for_summary.append("Hemoptysis")
                        flag_hemoptysis = True
                        hemoptysis_vol = st.selectbox("Volume", ["Select...", "Streaks", "Teaspoon", "Cupful (Massive!)"], key=f"rhv_{i}")
                        narrative += f"Volume of hemoptysis is {hemoptysis_vol.lower()}."
                    elif pc == "Other":
                        other_pc = st.text_input("Specify:", key=f"ropc_{i}")
                        complaint_names_for_summary.append(other_pc)
                        narrative = f"**{other_pc.capitalize()}** for {duration_num} {duration_unit}."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Gastroenterology" in units_selected:
            st.markdown("#### 🌭 Gastroenterology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_g")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Abdominal Pain", "Vomiting", "Change in Bowel Habits", "Gastrointestinal Bleeding", "Jaundice", "Dysphagia", "Other"], key=f"gpc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"gdur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Hours", "Days", "Weeks", "Months", "Years"], key=f"gdu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Abdominal Pain":
                        complaint_names_for_summary.append("Abdominal Pain")
                        abdo_site = st.selectbox("Site", ["Select...", "Epigastric", "RUQ", "RIF", "Generalized", "Central", "LLQ"], key=f"gsit_{i}")
                        abdo_onset = st.selectbox("Onset", ["Select...", "Sudden", "Gradual"], key=f"gons_{i}")
                        abdo_char = st.selectbox("Character", ["Select...", "Colicky", "Burning", "Sharp", "Dull ache"], key=f"gchr_{i}")
                        abdo_rad = st.selectbox("Radiation", ["Select...", "To the back", "To right shoulder", "To groin", "None"], key=f"grad_{i}")
                        abdo_rel = st.selectbox("Exacerbating/Relieving", ["Select...", "Worse with meals", "Better with meals", "Relieved by leaning forward"], key=f"grel_{i}")
                        if abdo_site == "Epigastric" and "meals" in abdo_rel: flag_pud = True
                        if abdo_site == "RIF": flag_peritonitis = True
                        if "Colicky" in abdo_char: flag_obstruction = True
                        narrative += f"Located in {abdo_site.lower()} (Onset: {abdo_onset.lower()}). Described as {abdo_char.lower()}."
                    elif pc == "Vomiting":
                        complaint_names_for_summary.append("Vomiting")
                        vom_content = st.selectbox("Content", ["Select...", "Undigested food", "Bilious", "Coffee-ground/Blood", "Feculent"], key=f"gvct_{i}")
                        if vom_content == "Coffee-ground/Blood": flag_gi_bleed = True
                        if vom_content in ["Feculent", "Bilious"]: flag_obstruction = True
                        narrative += f"Vomitus contains {vom_content.lower()}."
                    elif pc == "Gastrointestinal Bleeding":
                        complaint_names_for_summary.append("GI Bleed")
                        flag_gi_bleed = True
                        bleed_type = st.selectbox("Type", ["Select...", "Hematemesis", "Melena", "Hematochezia"], key=f"gbl_{i}")
                        narrative += f"Presented with {bleed_type.lower()}."
                    elif pc == "Other":
                        other_pc = st.text_input("Specify:", key=f"gopc_{i}")
                        complaint_names_for_summary.append(other_pc)
                        narrative = f"**{other_pc.capitalize()}** for {duration_num} {duration_unit}."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Nephrology" in units_selected:
            st.markdown("#### 🫘 Nephrology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_n")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Loin/Flank Pain", "Urine Appearance", "LUTS", "Edema", "Uremia Symptoms", "Other"], key=f"npc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"ndur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Hours", "Days", "Weeks", "Months", "Years"], key=f"ndu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Loin/Flank Pain":
                        complaint_names_for_summary.append("Loin Pain")
                        loin_char = st.selectbox("Character", ["Select...", "Colicky", "Dull ache"], key=f"nlc_{i}")
                        loin_rad = st.selectbox("Radiation", ["Select...", "To groin", "To back", "None"], key=f"nlr_{i}")
                        if "Colicky" in loin_char and "groin" in loin_rad: flag_renal_colic = True
                        narrative += f"Character: {loin_char.lower()}, radiating {loin_rad.lower()}."
                    elif pc == "Urine Appearance":
                        complaint_names_for_summary.append("Urine Change")
                        u_app = st.selectbox("Appearance", ["Select...", "Hematuria", "Frothy", "Coca-cola"], key=f"nua_{i}")
                        if u_app == "Hematuria":
                            flag_hematuria = True
                            painful = st.selectbox("Painful?", ["Painless", "Painful"], key=f"nhp_{i}")
                            if painful == "Painless" and age > 50: flag_malignancy_keyword = True
                        elif u_app == "Frothy": flag_nephrotic_edema = True
                        narrative += f"Urine appearance: {u_app.lower()}."
                    elif pc == "Uremia Symptoms":
                        flag_uremia = True
                        uremic_sx = st.multiselect("Symptoms", ["Hiccups", "Pruritus", "Altered sensorium"], key=f"nux_{i}")
                        narrative += f"Uremic features: {', '.join(uremic_sx).lower()}."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Endocrinology" in units_selected:
            st.markdown("#### 🦋 Endocrinology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_e")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Polyuria/Polydipsia", "Weight Change", "Neck Swelling", "Temperature Intolerance", "Other"], key=f"epc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"edur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Days", "Weeks", "Months", "Years"], key=f"edu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Polyuria/Polydipsia":
                        flag_polyuria = True
                        narrative += "Presented with excessive thirst and urination."
                    elif pc == "Weight Change":
                        wt_dir = st.selectbox("Direction", ["Unintentional Loss", "Gain"], key=f"ewd_{i}")
                        wt_app = st.selectbox("Appetite", ["Increased", "Decreased", "Normal"], key=f"ewa_{i}")
                        if wt_dir == "Unintentional Loss" and wt_app == "Increased": flag_weight_loss_paradox = True
                        narrative += f"{wt_dir.lower()} with {wt_app.lower()} appetite."
                    elif pc == "Temperature Intolerance":
                        intol = st.selectbox("Intolerance", ["Heat", "Cold"], key=f"eit_{i}")
                        if intol == "Heat": flag_hyperthyroid = True
                        else: flag_hypothyroid = True
                        narrative += f"Reports {intol.lower()} intolerance."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Neurology" in units_selected:
            st.markdown("#### 🧠 Neurology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_nn")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Weakness", "Seizures", "Headache", "Numbness", "Other"], key=f"nnpc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"nndur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Minutes", "Hours", "Days", "Weeks"], key=f"nndu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Weakness":
                        weak_onset = st.selectbox("Onset", ["Select...", "Sudden", "Gradual"], key=f"nwon_{i}")
                        weak_dist = st.selectbox("Distribution", ["Hemiparesis", "Paraparesis", "Quadriparesis"], key=f"nwdi_{i}")
                        if weak_onset == "Sudden" or weak_dist == "Hemiparesis": flag_stroke = True
                        narrative += f"Onset: {weak_onset.lower()}, Distribution: {weak_dist.lower()}."
                    elif pc == "Seizures":
                        flag_seizure = True
                        seiz_assoc = st.multiselect("Features", ["Tongue biting", "Incontinence", "Post-ictal confusion"], key=f"nsas_{i}")
                        narrative += f"Features: {', '.join(seiz_assoc).lower()}."
                    elif pc == "Headache":
                        ha_assoc = st.multiselect("Red Flags", ["Neck stiffness", "Projectile vomiting", "Worse in morning"], key=f"nhas_{i}")
                        if "Neck stiffness" in ha_assoc: flag_meningism = True
                        if "Worse in morning" in ha_assoc: flag_sol = True
                        narrative += f"Associations: {', '.join(ha_assoc).lower()}."
                    hpc_narratives.append(narrative)
            st.divider()

        if "Haematology" in units_selected:
            st.markdown("#### 🩸 Haematology")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1, key="num_h")
            for i in range(num_pcs):
                pc = st.selectbox(f"Select Complaint {i+1}", ["Select...", "Fatigue", "Bone Pain", "Bleeding", "Lump", "Other"], key=f"hpc_{i}")
                if pc != "Select...":
                    colA, colB = st.columns(2)
                    with colA: duration_num = st.number_input("Duration length", 1, 100, 1, key=f"hdur_{i}")
                    with colB: duration_unit = st.selectbox("Duration unit", ["Days", "Weeks", "Months"], key=f"hdu_{i}")
                    narrative = f"**{pc}** for {duration_num} {duration_unit}. "
                    if pc == "Fatigue": flag_anemia = True
                    elif pc == "Bone Pain": flag_scd_crisis = True
                    elif pc == "Bleeding":
                        b_type = st.selectbox("Type", ["Mucosal", "Deep tissue"], key=f"hbty_{i}")
                        if b_type == "Mucosal": flag_plt_bleed = True
                        else: flag_coag_bleed = True
                    elif pc == "Lump":
                        l_char = st.selectbox("Char", ["Rubbery, painless", "Hard, fixed"], key=f"hlch_{i}")
                        if "rubbery" in l_char.lower(): flag_lymphoma = True
                    hpc_narratives.append(narrative)
            st.divider()

        systemic = st.multiselect("Associated Systemic Symptoms", ["None", "Fever", "Night Sweats", "Weight Loss (>10%)", "Fatigue", "Bone Pain", "Aura", "Other"])
        if "Other" in systemic: sys_other = st.text_input("Specify other systemic symptom:")

    with st.expander("4. Past Medical History (PMH) & Drugs", expanded=False):
        pmh_list = st.multiselect("Chronic conditions:", ["None", "Hypertension", "Diabetes Mellitus", "Sickle Cell Disease", "Asthma", "Previous Stroke", "Epilepsy", "AFib", "PUD", "Liver Cirrhosis", "Tuberculosis", "Malignancy", "HIV/Syphilis", "Other"])
        if "Other" in pmh_list: pmh_other = st.text_input("Specify other condition:")
        allergies = st.selectbox("Known drug allergies?", ["No", "Yes", "Other"])
        if allergies in ["Yes", "Other"]: all_other = st.text_input("Specify allergy:")
        compliance = st.selectbox("Medication History", ["Select...", "Routine Antimalarial prophylaxis", "Routine Folic Acid", "Takes NSAIDs heavily", "Regular medication compliant", "Poor compliance", "Other"])
        if compliance == "Other": comp_other = st.text_input("Specify medication history:")

    with st.expander("5. Family, Social & Sexual History", expanded=False):
        fhx = st.multiselect("Family history of:", ["None", "Sickle Cell Disease", "Hemophilia", "Stroke", "IHD", "Hypertension", "Cancer", "Other"])
        if "Other" in fhx: fhx_other = st.text_input("Specify other family history:")
        st.markdown("##### Social & Lifestyle Context")
        smoking = st.selectbox("Smoking History", ["Never", "Ex-smoker", "Current Smoker"])
        if smoking in ["Ex-smoker", "Current Smoker"]:
            col_s1, col_s2 = st.columns(2)
            with col_s1: cigs_per_day = st.number_input("Cigarettes per day", 0, 100, 0)
            with col_s2: years_smoked = st.number_input("Years smoked", 0, 100, 0)
            pack_years = (cigs_per_day / 20) * years_smoked
        alcohol = st.selectbox("Alcohol Intake", ["None", "Occasional", "Heavy/Dependent"])
        if alcohol in ["Occasional", "Heavy/Dependent"]:
            col_a1, col_a2 = st.columns(2)
            with col_a1: alcohol_type = st.selectbox("Type of Alcohol", ["Beer", "Wine", "Spirits", "Local", "Mixed", "Other"])
            with col_a2: bottles_per_week = st.number_input("Bottles/Shots per week", 0, 100, 0)
        housing = st.selectbox("Toxic Risks / Lifestyle", ["Adequate", "Exposed to Benzene / Radiation", "IV Drug Use", "High Stress / Sedentary", "Other"])
        if housing == "Other": h_other = st.text_input("Specify lifestyle risk:")
        st.markdown("##### Sexual & Reproductive History")
        sex_active = st.selectbox("Currently Sexually Active?", ["Select...", "Yes", "No", "Declined to answer"])
        if sex_active == "Yes":
            col_x1, col_x2 = st.columns(2)
            with col_x1: partners = st.selectbox("Number of partners (last 6 mo)", ["1 (Monogamous)", "2-3", ">3"])
            with col_x2: protection = st.selectbox("Barrier Contraception", ["Consistent use", "Inconsistent use", "None"])
            sti_hx = st.selectbox("History of STIs or Genital Ulcers?", ["No", "Yes", "Unsure"])

    with st.expander("6. Review of Systems (ROS) - Exhaustive", expanded=False):
        ros_haem = st.multiselect("Haematology", ["None", "Spontaneous bruising", "Recurrent infections", "Bone pain", "Leg ulcers", "Bleeding gums", "Epistaxis", "Other"])
        if "Other" in ros_haem: r_haem_o = st.text_input("Specify Haem:")
        ros_cv = st.multiselect("Cardiovascular", ["None", "Chest pain", "Palpitations", "Leg swelling", "Orthopnea", "PND", "Syncope", "Claudication", "Other"])
        if "Other" in ros_cv: r_cv_o = st.text_input("Specify CV:")
        ros_gi = st.multiselect("Gastrointestinal", ["None", "Nausea", "Vomiting", "Dysphagia", "Odynophagia", "Heartburn/Dyspepsia", "Abdominal pain", "Bloating", "Early satiety", "Jaundice", "Diarrhea", "Constipation", "Melena", "Hematochezia", "Other"])
        if "Other" in ros_gi: r_gi_o = st.text_input("Specify GI:")
        ros_gu = st.multiselect("Genitourinary", ["None", "Dysuria", "Hematuria", "Frequency", "Urgency", "Nocturia", "Hesitancy", "Poor stream", "Frothy urine", "Incontinence", "Genital discharge", "Other"])
        if "Other" in ros_gu: r_gu_o = st.text_input("Specify GU:")
        ros_neuro = st.multiselect("Neurological", ["None", "Headache", "Syncope", "Seizures", "Weakness", "Numbness/Tingling", "Visual changes", "Speech difficulty", "Tremors", "Memory loss", "Other"])
        if "Other" in ros_neuro: r_neuro_o = st.text_input("Specify Neuro:")
        ros_msk = st.multiselect("Musculoskeletal", ["None", "Bone pain", "Joint swelling", "Joint stiffness", "Muscle wasting", "Myalgia", "Other"])
        if "Other" in ros_msk: r_msk_o = st.text_input("Specify MSK:")
        ros_endo = st.multiselect("Endocrine", ["None", "Polyuria", "Polydipsia", "Polyphagia", "Heat intolerance", "Cold intolerance", "Excessive sweating", "Loss of libido", "Other"])
        if "Other" in ros_endo: r_endo_o = st.text_input("Specify Endo:")

# ==========================================
# TAB 2: PHYSICAL EXAMINATION
# ==========================================
with tab_pe:
    with st.expander("1. General Physical Examination", expanded=True):
        colA, colB = st.columns(2)
        with colA:
            pallor = st.selectbox("Pallor", ["Absent", "Mild", "Moderate", "Severe (Paper white)"])
            icterus = st.selectbox("Icterus", ["Absent", "Present (Hemolysis/Liver)"])
            cyanosis = st.selectbox("Cyanosis", ["Absent", "Central", "Peripheral"])
        with colB:
            clubbing = st.selectbox("Clubbing", ["Absent", "Grade 1", "Grade 2", "Grade 3", "Grade 4"])
            edema = st.selectbox("Pedal Edema", ["Absent", "Pitting", "Anasarca"])
            lymph = st.selectbox("Lymphadenopathy (General)", ["Absent", "Cervical", "Axillary", "Generalized", "Left Supraclavicular (Virchow's Node)"])
        st.markdown("##### Vitals:")
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        with col_v1: temp = st.number_input("Temp (°C)", 35.0, 42.0, 37.0, 0.1)
        with col_v2: hr = st.number_input("Pulse Rate (bpm)", 30, 200, 80)
        with col_v3: bp_sys = st.number_input("BP Systolic", 60, 250, 120)
        with col_v4: bp_dia = st.number_input("BP Diastolic", 30, 150, 80)
        rr = st.number_input("Respiratory Rate (cpm)", 8, 60, 16)

    if "Haematology" in units_selected:
        with st.expander("2. Systemic Examination (Haematology)", expanded=True):
            haem_signs = st.multiselect("Peripheral Signs", ["Normal", "Koilonychia", "Glossitis / Angular Stomatitis", "Petechiae / Purpura", "Chronic Leg Ulcers"])
            haem_lymph = st.selectbox("Specific Lymph Node Exam", ["No palpable nodes", "Discrete, rubbery, painless nodes", "Matted, hard, fixed nodes", "Tender, warm nodes"])
            haem_spleen = st.selectbox("Abdominal Palpation (Spleen)", ["Not palpable", "Palpable (Mild/Moderate)", "Massive Splenomegaly (Crossing umbilicus)"])
    if "Neurology" in units_selected:
        with st.expander("2. Systemic Examination (Neurology)", expanded=True):
            gcs_score = st.number_input("Glasgow Coma Scale (GCS)", 3, 15, 15)
            cranial_nerves = st.selectbox("Cranial Nerves (II-XII)", ["Intact", "CN VII Palsy", "CN III Palsy"])
            motor_tone = st.selectbox("Tone", ["Normal tone", "Hypertonia / Spasticity (UMN)", "Hypotonia / Flaccidity (LMN)"])
            motor_power = st.selectbox("Power (0-5)", ["Grade 5/5", "Grade 4/5", "Grade 3/5", "Grade 0-2/5"])
            reflexes = st.selectbox("Reflexes", ["Normoreflexia (++ )", "Hyperreflexia (+++ ) [UMN]", "Hyporeflexia (+/0) [LMN]"])
            plantar_response = st.selectbox("Plantar Reflex", ["Flexor (Normal)", "Extensor (Upgoing - UMN sign)"])
            meningeal_signs = st.selectbox("Meningeal Irritation", ["Absent", "Neck Stiffness / Positive Kernig's"])
    if "Cardiology" in units_selected:
        with st.expander("2. Systemic Examination (Cardiovascular)", expanded=True):
            pulse_rhythm = st.selectbox("Pulse Rhythm", ["Regular", "Irregularly Irregular (AFib)"])
            jvp_status = st.selectbox("JVP", ["Not elevated", "Elevated"])
            apex_loc = st.selectbox("Apex Beat", ["5th ICS Normal", "Displaced laterally"])
            heart_sounds = st.selectbox("Heart Sounds", ["S1 and S2 normal", "S3 Gallop present"])
            murmur = st.selectbox("Murmurs", ["None", "Pansystolic", "Ejection systolic", "Diastolic"])
    if "Gastroenterology" in units_selected:
        with st.expander("2. Systemic Examination (Abdomen/GI)", expanded=True):
            gi_inspection = st.multiselect("Inspection", ["Flat/Scaphoid", "Distension", "Caput Medusae"])
            gi_palpation = st.selectbox("Palpation", ["Soft, non-tender", "Epigastric tenderness", "Guarding/Rebound"])
            gi_organomegaly = st.selectbox("Organomegaly", ["None", "Hepatomegaly", "Splenomegaly", "Hepatosplenomegaly"])
            gi_percussion = st.selectbox("Percussion", ["Normal tympany", "Shifting dullness (Ascites)"])
    if "Respiratory" in units_selected:
        with st.expander("2. Systemic Examination (Respiratory)", expanded=True):
            resp_inspection = st.multiselect("Inspection (Chest)", ["Normal contour", "Barrel chest", "Asymmetrical movement"])
            trachea_palpation = st.selectbox("Trachea Position", ["Central", "Deviated to Left", "Deviated to Right"])
            resp_percussion = st.selectbox("Percussion Note", ["Resonant (Normal)", "Hyper-resonant", "Dull (Consolidation)", "Stony Dull (Effusion)"])
            resp_auscultation = st.selectbox("Breath Sounds", ["Vesicular (Normal)", "Bronchial", "Diminished", "Absent"])
            resp_added_sounds = st.multiselect("Added Sounds", ["None", "Fine Crepitations", "Coarse Crepitations", "Wheeze", "Pleural Rub"])
    if "Nephrology" in units_selected:
        with st.expander("2. Systemic Examination (Renal/Genitourinary)", expanded=True):
            renal_inspection = st.multiselect("Inspection", ["Normal", "AV Fistula mark", "Asterixis (Flapping tremor)"])
            renal_palpation = st.selectbox("Palpation", ["Non-tender, kidneys not ballotable", "Kidney(s) ballotable", "Costovertebral angle (CVA) tenderness", "Palpable bladder"])
            renal_auscultation = st.selectbox("Auscultation", ["No bruits", "Renal artery bruit present"])
            fluid_status = st.selectbox("Overall Fluid Status Assessment", ["Euvolemic", "Fluid Overload (Hypervolemic)", "Dehydrated (Hypovolemic)"])
    if "Endocrinology" in units_selected:
        with st.expander("2. Systemic Examination (Endocrine)", expanded=True):
            neck_insp = st.selectbox("Neck Inspection", ["Normal", "Visible Goiter"])
            neck_palp = st.selectbox("Neck Palpation", ["Normal", "Diffuse smooth enlargement", "Multinodular", "Hard fixed mass"])
            eye_s = st.selectbox("Eye Signs", ["Normal", "Exophthalmos / Proptosis", "Lid lag"])
            trem_s = st.selectbox("Tremors", ["Absent", "Fine tremor", "Flapping tremor"])

# ==========================================
# TAB 3: CASE FORMULATION & DISCUSSION
# ==========================================
with tab_dx:
    st.markdown("### Case Formulation & Discussion")
    if st.button("Generate Clinical Presentation"):
        sys_str = "Associated systemic symptoms include " + ", ".join(systemic).lower() if systemic else "There are no associated systemic symptoms."
        pmh_str = ", ".join(pmh_list) if pmh_list and "None" not in pmh_list else "no known chronic illnesses"
        soc_str = f"The patient is a {smoking.lower()}."
        if smoking in ["Current Smoker", "Ex-smoker"]: soc_str = f"The patient is a {smoking.lower()} ({pack_years:.1f} pack-years)."
        if alcohol != "None": soc_str += f" Alcohol intake is {alcohol.lower()} ({bottles_per_week} bottles/week of {alcohol_type})."
        if sex_active == "Yes": soc_str += f" Sexually active with {partners} partners, {protection.lower()} barrier use. STI history: {sti_hx.lower()}."
        all_ros = []
        def parse_ros(ros_list, other_val, name):
            if ros_list and "None" not in ros_list:
                clean_list = [item for item in ros_list if item != "Other"]
                if "Other" in ros_list and other_val: clean_list.append(other_val)
                if clean_list: all_ros.append(f"{name}: " + ", ".join(clean_list))
        parse_ros(ros_haem, r_haem_o if "r_haem_o" in locals() else "", "Haem")
        parse_ros(ros_cv, r_cv_o if "r_cv_o" in locals() else "", "CV")
        parse_ros(ros_gi, r_gi_o if "r_gi_o" in locals() else "", "GI")
        parse_ros(ros_gu, r_gu_o if "r_gu_o" in locals() else "", "GU")
        parse_ros(ros_neuro, r_neuro_o if "r_neuro_o" in locals() else "", "Neuro")
        parse_ros(ros_msk, r_msk_o if "r_msk_o" in locals() else "", "MSK")
        parse_ros(ros_endo, r_endo_o if "r_endo_o" in locals() else "", "Endo")
        ros_final_str = " \n- ".join(all_ros) if all_ros else "unremarkable across major systems."
        piccel_pos = [p for p in [f"{pallor.lower()} pallor" if pallor != "Absent" else "", "jaundice" if icterus != "Absent" else "", f"{lymph.lower()} lymphadenopathy" if lymph != "Absent" else ""] if p]
        piccel_str = ", ".join(piccel_pos) if piccel_pos else "no pallor, jaundice, cyanosis, clubbing, pedal edema, or lymphadenopathy"
        
        presentation = f"**Good morning Sir/Ma, I present {name}, a {age}-year-old {marital} {sex}, who works as a {occupation}.**\n\n"
        presentation += "**History of Presenting Complaint (HPC):**\n"
        for narrative in hpc_narratives: presentation += f"- {narrative}\n"
        presentation += f"\n{sys_str}\n\n"
        presentation += f"**Background History:**\nKnown history of {pmh_str}. {soc_str}. Medications: {compliance.lower()}.\n\n"
        presentation += f"**Review of Systems (ROS):**\nPositive for:\n- {ros_final_str}\n\n"
        presentation += f"**Objective Findings (O/E):**\nPatient was comfortable, with {piccel_str}. Vitals: T={temp}°C, HR={hr}bpm, BP={bp_sys}/{bp_dia}mmHg, RR={rr}cpm.\n"
        
        if "Haematology" in units_selected: presentation += f"**Haematological Exam:** Signs: {', '.join(haem_signs).lower()}. Lymph nodes: {haem_lymph.lower()}. Spleen: {haem_spleen.lower()}.\n\n"
        if "Neurology" in units_selected: presentation += f"**Neurological Exam:** GCS {gcs_score}/15. Cranial nerves: {cranial_nerves.lower()}. Motor: {motor_tone.lower()}, power {motor_power.lower()}, {reflexes.lower()}. Plantars: {plantar_response.lower()}.\n\n"
        if "Cardiology" in units_selected: presentation += f"**Cardiovascular Exam:** Pulse {hr}bpm, {pulse_rhythm.lower()}. JVP {jvp_status.lower()}. Apex beat {apex_loc.lower()}. Auscultation: {heart_sounds.lower()}, {murmur.lower()}.\n\n"
        if "Respiratory" in units_selected: presentation += f"**Respiratory Exam:** Trachea {trachea_palpation.lower()}. Percussion {resp_percussion.lower()}. Auscultation: {resp_auscultation.lower()} with {', '.join(resp_added_sounds).lower()}.\n\n"
        if "Gastroenterology" in units_selected: presentation += f"**Abdominal Exam:** Palpation {gi_palpation.lower()}, {gi_organomegaly.lower()}. Percussion {gi_percussion.lower()}.\n\n"
        if "Nephrology" in units_selected: presentation += f"**Renal Exam:** Palpation {renal_palpation.lower()}. Auscultation {renal_auscultation.lower()}. Fluid status: {fluid_status.lower()}.\n\n"
        if "Endocrinology" in units_selected: presentation += f"**Endocrine Exam:** Neck {neck_palp.lower()}. Eyes {eye_s.lower()}. Tremor {trem_s.lower()}.\n\n"
        
        st.info(presentation)
        
        # ==========================================
        # GLOBAL DIAGNOSTIC ENGINE (v22.0)
        # ==========================================
        clinical_diffs = []

        if "Fever" in systemic or temp > 37.5:
            clinical_diffs.append({
                "title": "Sepsis / Malaria / Enteric Fever",
                "supports": f"Documented fever (T: {temp}°C) and systemic inflammatory response.",
                "negates": "Negative mRDT, sterile blood cultures, and normal WBC count.",
                "clinical_pearl": "In our setting, rule out Malaria first. Consider Typhoid if fever is stepwise."
            })
        if flag_ischemic_pain or (bp_sys > 160 or bp_dia > 100):
            clinical_diffs.append({
                "title": "ACS / Hypertensive Emergency",
                "supports": f"Ischemic-type chest pain or severely elevated BP ({bp_sys}/{bp_dia}).",
                "negates": "Normal serial ECGs, negative Troponins.",
                "clinical_pearl": "Check for 'Target Organ Damage': blurred vision, hematuria, or confusion."
            })
        if flag_heart_failure or "Pedal Edema" in complaint_names_for_summary or "S3 Gallop" in heart_sounds:
            clinical_diffs.append({
                "title": "Congestive Heart Failure (CHF)",
                "supports": "Orthopnea, PND, pedal edema, and gallop rhythm.",
                "negates": "Normal JVP, clear lung bases, and Ejection Fraction >50% on Echo.",
                "clinical_pearl": "Bilateral pitting edema + raised JVP is CHF until proven otherwise."
            })
        if flag_chronic_cough or flag_hemoptysis or "Night Sweats" in systemic:
            clinical_diffs.append({
                "title": "Pulmonary TB / Bronchogenic Carcinoma",
                "supports": f"Chronic cough, hemoptysis, and constitutional symptoms.",
                "negates": "MTB Not Detected on GeneXpert and negative sputum cytology.",
                "clinical_pearl": "Rule out TB first for public health."
            })
        if "Dull (Consolidation)" in resp_percussion or "Bronchial" in resp_auscultation:
             clinical_diffs.append({
                "title": "Lobar Pneumonia / Consolidation",
                "supports": "Localized dull percussion note and bronchial breath sounds.",
                "negates": "Resonant percussion and vesicular breath sounds.",
                "clinical_pearl": "Look for 'Rusty Sputum' and pleuritic chest pain to confirm Pneumonia."
            })
        if flag_stroke or "Extensor (Upgoing - UMN sign)" in plantar_response or "Hyperreflexia" in reflexes:
            clinical_diffs.append({
                "title": "Cerebrovascular Accident (Stroke)",
                "supports": "Sudden focal deficit, UMN signs, and potential HTN history.",
                "negates": "Resolution <24h (TIA) or CT Brain showing no vascular lesion.",
                "clinical_pearl": "Always check RBS (Random Blood Sugar) to rule out a 'Hypoglycemic Mimic'."
            })
        if flag_meningism or "Neck Stiffness / Positive Kernig's" in meningeal_signs:
            clinical_diffs.append({
                "title": "Acute Meningitis",
                "supports": "Fever, headache, and signs of meningeal irritation.",
                "negates": "Normal CSF analysis (Biochemistry/Microscopy).",
                "clinical_pearl": "Do not wait for results to start antibiotics if suspicion is high."
            })
        if flag_uremia or flag_nephrotic_edema or "Frothy" in str(hpc_narratives):
            clinical_diffs.append({
                "title": "Acute-on-Chronic Kidney Disease",
                "supports": "Uremic symptoms, frothy urine, and pedal edema.",
                "negates": "Serum Creatinine and GFR within normal limits.",
                "clinical_pearl": "Check for 'Small Shrunken Kidneys' on ultrasound."
            })
        if flag_jaundice or flag_gi_bleed or "Hepatomegaly" in gi_organomegaly:
            clinical_diffs.append({
                "title": "Chronic Liver Disease / Portal Hypertension",
                "supports": "Icterus, abdominal distension, and signs of portosystemic shunting.",
                "negates": "Normal Liver Function Tests (LFTs) and normal abdominal imaging.",
                "clinical_pearl": "Check for Asterixis (flapping tremor) to assess for Hepatic Encephalopathy."
            })
        if flag_anemia or pallor != "Absent":
            clinical_diffs.append({
                "title": "Severe Anemic Syndrome",
                "supports": f"Clinical pallor ({pallor}), dizziness, and exertional dyspnea.",
                "negates": "Hematocrit (PCV) > 30%.",
                "clinical_pearl": "In our setting, common causes are Nutritional (Iron), Malaria, or Hookworm."
            })
        if flag_scd_crisis or "Sickle Cell Disease" in pmh_list:
             clinical_diffs.append({
                "title": "Vaso-occlusive Crisis (SCD)",
                "supports": "Severe bone/joint pain in a known Sickler.",
                "negates": "Absence of previous genotype confirmation.",
                "clinical_pearl": "Check for triggers: Cold weather, malaria, or dehydration."
            })
        if flag_polyuria or "Diabetes Mellitus" in pmh_list:
            clinical_diffs.append({
                "title": "Diabetes Mellitus (DKA Risk)",
                "supports": "Osmotic symptoms (Polyuria/Polydipsia) and known hyperglycemia.",
                "negates": "Normal Fasting Blood Glucose.",
                "clinical_pearl": "If the patient has 'Sweet/Fruity' breath, investigate for Diabetic Ketoacidosis immediately."
            })
        if flag_malignancy_keyword or "Weight Loss (>10%)" in systemic:
            clinical_diffs.append({
                "title": "🚨 Occult Malignancy / Lymphoma",
                "supports": "Significant unintentional weight loss and hard/fixed lymphadenopathy.",
                "negates": "Absence of B-symptoms and negative imaging/biopsy.",
                "clinical_pearl": "Focus on Prostate (Men), Breast/Cervical (Women), or Colorectal screenings."
            })
# ==========================================
        # 10. THE "INTERSECTION" SYNDROMES (v24.0)
        # ==========================================
        # These use .insert(0) to push life-threatening multi-system overlaps to the TOP of the list.

        # 1. Cardiorenal Syndrome
        if flag_heart_failure and (flag_uremia or flag_nephrotic_edema):
            clinical_diffs.insert(0, {
                "title": "🚨 Cardiorenal Syndrome",
                "supports": "Concurrent signs of cardiac volume overload (CHF) and renal impairment/uremia.",
                "negates": "Normal Ejection Fraction and normal Serum Creatinine.",
                "clinical_pearl": "Diuretic resistance is common. Strict fluid balance and cardiology/nephrology cross-consult required."
            })

        # 2. Cor Pulmonale (Right Heart Failure secondary to Lung Disease)
        if flag_chronic_cough and flag_heart_failure:
            clinical_diffs.insert(0, {
                "title": "🚨 Cor Pulmonale",
                "supports": "Chronic respiratory symptoms coupled with signs of right-sided heart failure (edema, elevated JVP).",
                "negates": "Normal right ventricular size and pressure on Echocardiogram.",
                "clinical_pearl": "Treat the underlying lung pathology (e.g., COPD/PTB) while managing the fluid overload."
            })

        # 3. Hepatic Encephalopathy
        if flag_jaundice and (gcs_score < 15 or "Altered sensorium" in str(hpc_narratives) or flag_seizure):
            clinical_diffs.insert(0, {
                "title": "🚨 Hepatic Encephalopathy",
                "supports": "Liver dysfunction (jaundice/stigmata) presenting with altered consciousness or seizures.",
                "negates": "Normal blood ammonia levels and normal EEG.",
                "clinical_pearl": "Look for precipitants: GI bleed, infection, constipation, or electrolyte imbalance. Initiate Lactulose."
            })

        # 4. Sickle Cell Acute Chest Syndrome (ACS)
        if (flag_scd_crisis or "Sickle Cell Disease" in pmh_list) and (flag_sudden_dyspnea or flag_pleuritic_pain or flag_chronic_cough):
            clinical_diffs.insert(0, {
                "title": "🚨 Acute Chest Syndrome (SCD)",
                "supports": "Respiratory distress or chest pain in a known Sickle Cell patient.",
                "negates": "Clear lung fields on CXR.",
                "clinical_pearl": "A leading cause of death in SCD. Requires urgent exchange transfusion and broad-spectrum antibiotics."
            })

        # 5. Uremic Encephalopathy
        if flag_uremia and gcs_score < 15:
            clinical_diffs.insert(0, {
                "title": "🚨 Uremic Encephalopathy",
                "supports": "Severe renal failure features combined with a drop in Glasgow Coma Scale.",
                "negates": "Alternative causes of coma (e.g., stroke, hypoglycemia).",
                "clinical_pearl": "Indication for urgent hemodialysis. Do not delay."
            })

        # 6. Thyroid Storm (Thyrotoxic Crisis)
        if flag_hyperthyroid and (temp > 38.5 or hr > 110 or flag_arrhythmia):
            clinical_diffs.insert(0, {
                "title": "🚨 Thyroid Storm",
                "supports": f"Hyperthyroid symptoms coupled with hyperpyrexia (T: {temp}) and tachycardia/arrhythmia (HR: {hr}).",
                "negates": "Normal Free T3/T4 and TSH levels.",
                "clinical_pearl": "Medical emergency. Treat with Beta-blockers (Propranolol), PTU, and Iodine (give Iodine *after* PTU)."
            })

        # 7. Sepsis / Septic Shock
        if (temp > 38.0 or temp < 36.0) and (hr > 90 or rr > 20) and bp_sys < 90:
            clinical_diffs.insert(0, {
                "title": "🚨 Septic Shock",
                "supports": f"SIRS criteria met (T:{temp}, HR:{hr}, RR:{rr}) with hypotension (BP:{bp_sys}/{bp_dia}).",
                "negates": "Normal lactate and negative blood cultures.",
                "clinical_pearl": "Commence the 'Sepsis Six' immediately. Do not wait for lab confirmation to start broad-spectrum IV antibiotics."
            })
            
        # 8. Pulmonary-Renal Syndrome (e.g., Goodpasture's / GPA)
        if flag_hemoptysis and flag_hematuria:
            clinical_diffs.insert(0, {
                "title": "🚨 Pulmonary-Renal Syndrome",
                "supports": "Simultaneous alveolar hemorrhage (hemoptysis) and glomerulonephritis (hematuria).",
                "negates": "Negative auto-antibodies (Anti-GBM, ANCA).",
                "clinical_pearl": "Rare but fatal. Think Goodpasture's disease or Granulomatosis with Polyangiitis (GPA). Needs urgent immunosuppression."
            })

        # 9. Hypertensive Encephalopathy
        if bp_sys > 180 and (flag_stroke or gcs_score < 15 or flag_seizure):
            clinical_diffs.insert(0, {
                "title": "🚨 Hypertensive Encephalopathy",
                "supports": f"Malignant hypertension (BP {bp_sys}/{bp_dia}) presenting with neurological fallout.",
                "negates": "CT Brain showing a massive established stroke/bleed instead of reversible edema.",
                "clinical_pearl": "Lower BP gradually (max 25% reduction in first hours) to prevent cerebral ischemia."
            })
        if clinical_diffs:
            for idx, diff in enumerate(clinical_diffs):
                with st.expander(f"**{idx+1}. {diff['title']}**", expanded=True):
                    st.markdown(f"**What Supports This:** {diff['supports']}")
                    st.markdown(f"**What Negates/Is Missing:** {diff['negates']}")
                    st.success(f"**Clinical Pearl:** {diff['clinical_pearl']}")
        st.write("---")
        top_diff = clinical_diffs[0]['title'] if clinical_diffs else "an underlying pathology"
        st.info(f"**Case Summary:** {age}-year-old presenting with {', '.join(complaint_names_for_summary)}. Most likely differential is **{top_diff}**.")
