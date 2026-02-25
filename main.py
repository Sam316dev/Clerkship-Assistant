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

inspection, palpation, percussion, auscultation, added_sounds = [], "Central", "Resonant (Normal)", "Vesicular (Normal)", []
neck_inspection, neck_palpation, eye_signs, skin_signs, tremor = "Normal", "Normal", "Normal", "Normal", "Absent"
pulse_rhythm, pulse_char, jvp_status, apex_loc, heaves_thrills, heart_sounds, murmur = "Regular", "Normal volume", "Not elevated", "5th ICS", "Absent", "S1 and S2", "None"
gi_inspection, gi_palpation, gi_organomegaly, gi_percussion, gi_auscultation = [], "Soft, non-tender", "None", "Normal tympany", "Normal active"
renal_inspection, renal_palpation, renal_auscultation, fluid_status = [], "Non-tender", "No bruits", "Euvolemic"
gcs_score = 15
cranial_nerves, motor_tone, motor_power, reflexes, plantar_response, meningeal_signs = "Intact", "Normal tone", "Grade 5/5", "Normoreflexia", "Flexor", "Absent"
haem_signs, haem_lymph, haem_spleen = [], "No palpable nodes", "Not palpable"

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
        unit = st.selectbox("Select Internal Medicine Unit", ["Select...", "Haematology", "Neurology", "Gastroenterology", "Nephrology", "Cardiology", "Respiratory", "Endocrinology"])
        
        # ---------------------------------------------------------
        # THE CORE ENGINE (Simplified for UI flow, all flags retained)
        # ---------------------------------------------------------
        if unit in ["Haematology", "Neurology", "Gastroenterology", "Nephrology", "Cardiology", "Respiratory", "Endocrinology"]:
            st.info(f"{unit} module active. Fill out specific complaints below.")
            num_pcs = st.number_input("Number of presenting complaints?", min_value=1, max_value=5, value=1)
            for i in range(num_pcs):
                other_pc = st.text_input(f"Specify Complaint {i+1} ({unit}):", key=f"xopc_{i}")
                colA, colB = st.columns(2)
                with colA: duration_num = st.number_input("Duration", 1, 100, 1, key=f"xdur_{i}")
                with colB: duration_unit = st.selectbox("Unit", ["Hours", "Days", "Weeks", "Months", "Years"], key=f"xdu_{i}")
                
                # Dynamic Checkbox triggers for backend logic based on Unit
                if unit == "Neurology":
                    if st.checkbox("Sudden onset weakness/facial droop (Stroke)", key=f"nq1_{i}"): flag_stroke = True
                    if st.checkbox("Convulsions with tongue biting (Seizure)", key=f"nq2_{i}"): flag_seizure = True
                    if st.checkbox("Glove & stocking numbness (Neuropathy)", key=f"nq3_{i}"): flag_neuropathy = True
                elif unit == "Cardiology":
                    if st.checkbox("Crushing Chest Pain (ACS)", key=f"cq1_{i}"): flag_ischemic_pain = True
                    if st.checkbox("Orthopnea / PND (Heart Failure)", key=f"cq2_{i}"): flag_heart_failure = True
                elif unit == "Respiratory":
                    if st.checkbox("Chronic Cough & Hemoptysis (TB/Malignancy)", key=f"rq3_{i}"): flag_chronic_cough = True; flag_hemoptysis = True
                elif unit == "Gastroenterology":
                    if st.checkbox("Colicky pain & Vomiting (Obstruction)", key=f"gq4_{i}"): flag_obstruction = True
                    if st.checkbox("Melena / Hematemesis (GI Bleed)", key=f"gq5_{i}"): flag_gi_bleed = True
                    if st.checkbox("Epigastric pain relating to meals (PUD)", key=f"gq6_{i}"): flag_pud = True
                elif unit == "Nephrology":
                    if st.checkbox("Painless Hematuria (Malignancy)", key=f"nep1_{i}"): flag_hematuria = True; flag_malignancy_keyword = True
                    if st.checkbox("Colicky Loin-to-Groin Pain (Stones)", key=f"nep2_{i}"): flag_renal_colic = True
                elif unit == "Haematology":
                    if st.checkbox("Bone/Joint pain with known SCD (Crisis)", key=f"hae1_{i}"): flag_scd_crisis = True
                    if st.checkbox("Painless rubbery nodes + Night Sweats (Lymphoma)", key=f"hae2_{i}"): flag_lymphoma = True
                elif unit == "Endocrinology":
                    if st.checkbox("Polyuria/Polydipsia (Diabetes)", key=f"end1_{i}"): flag_polyuria = True
                    if st.checkbox("Heat intolerance & Palpitations (Thyrotoxicosis)", key=f"end2_{i}"): flag_hyperthyroid = True

                if other_pc:
                    complaint_names_for_summary.append(other_pc)
                    hpc_narratives.append(f"**{other_pc.capitalize()}** for {duration_num} {duration_unit}.")
            st.divider()

        systemic = st.multiselect("Associated Systemic Symptoms (B-Symptoms / Global)", ["None", "Fever", "Drenching Night Sweats", "Unintentional Weight Loss (>10%)", "Fatigue", "Bone Pain", "Aura", "Other"])
        if "Other" in systemic: sys_other = st.text_input("Specify other systemic symptom:")

    with st.expander("4. Past Medical History (PMH) & Drugs", expanded=False):
        pmh_list = st.multiselect("Chronic conditions:", ["None", "Hypertension", "Diabetes Mellitus", "Sickle Cell Disease", "Asthma", "Previous Stroke", "Epilepsy", "Atrial Fibrillation", "Peptic Ulcer Disease", "Liver Cirrhosis", "Tuberculosis", "Malignancy", "HIV/Syphilis", "Other"])
        if "Other" in pmh_list: pmh_other = st.text_input("Specify other condition:")
        allergies = st.selectbox("Known drug allergies?", ["No", "Yes", "Other"])
        if allergies == "Yes" or allergies == "Other": all_other = st.text_input("Specify allergy:")
        compliance = st.selectbox("Medication History", ["Select...", "Routine Antimalarial prophylaxis", "Routine Folic Acid", "Takes NSAIDs heavily", "Regular medication compliant", "Poor compliance", "Other"])
        if compliance == "Other": comp_other = st.text_input("Specify medication history:")

    with st.expander("5. Family, Social & Sexual History", expanded=False):
        fhx = st.multiselect("Family history of:", ["None", "Sickle Cell Disease", "Hemophilia", "Stroke", "Ischemic Heart Disease", "Hypertension", "Cancer", "Other"])
        if "Other" in fhx: fhx_other = st.text_input("Specify other family history:")
        
        st.markdown("##### Social & Lifestyle Context")
        smoking = st.selectbox("Smoking History", ["Never", "Ex-smoker", "Current Smoker"])
        if smoking in ["Ex-smoker", "Current Smoker"]:
            col_s1, col_s2 = st.columns(2)
            with col_s1: cigs_per_day = st.number_input("Cigarettes per day", 0, 100, 0)
            with col_s2: years_smoked = st.number_input("Years smoked", 0, 100, 0)
            pack_years = (cigs_per_day / 20) * years_smoked
        
        # RESTORED ALCOHOL DROPDOWNS
        alcohol = st.selectbox("Alcohol Intake", ["None", "Occasional", "Heavy/Dependent"])
        if alcohol in ["Occasional", "Heavy/Dependent"]:
            col_a1, col_a2 = st.columns(2)
            with col_a1: alcohol_type = st.selectbox("Type of Alcohol", ["Beer", "Wine", "Spirits", "Local (Palm wine/Ogogoro)", "Mixed", "Other"])
            with col_a2: bottles_per_week = st.number_input("Bottles/Shots per week", 0, 100, 0)
            
        housing = st.selectbox("Toxic Risks / Lifestyle", ["Adequate", "Exposed to Benzene / Radiation", "IV Drug Use", "High Stress / Sedentary", "Other"])
        if housing == "Other": h_other = st.text_input("Specify lifestyle risk:")

        # ADDED SEXUAL HISTORY
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
        
        ros_msk = st.multiselect("Musculoskeletal", ["None", "Bone pain", "Joint swelling", "Joint stiffness (Morning)", "Muscle wasting", "Myalgia", "Other"])
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

    # DYNAMIC EXAM SECTION
    if unit == "Haematology":
        with st.expander("2. Systemic Examination (Haematology)", expanded=True):
            haem_signs = st.multiselect("Peripheral Signs", ["Normal", "Koilonychia", "Glossitis / Angular Stomatitis", "Petechiae / Purpura", "Chronic Leg Ulcers"])
            haem_lymph = st.selectbox("Specific Lymph Node Exam", ["No palpable nodes", "Discrete, rubbery, painless nodes", "Matted, hard, fixed nodes", "Tender, warm nodes"])
            haem_spleen = st.selectbox("Abdominal Palpation (Spleen)", ["Not palpable", "Palpable (Mild/Moderate)", "Massive Splenomegaly (Crossing umbilicus)"])

    elif unit == "Neurology":
        with st.expander("2. Systemic Examination (Neurology)", expanded=True):
            gcs_score = st.number_input("Glasgow Coma Scale (GCS)", 3, 15, 15)
            cranial_nerves = st.selectbox("Cranial Nerves (II-XII)", ["Intact", "CN VII Palsy", "CN III Palsy"])
            motor_tone = st.selectbox("Tone", ["Normal tone", "Hypertonia / Spasticity (UMN)", "Hypotonia / Flaccidity (LMN)"])
            motor_power = st.selectbox("Power (0-5)", ["Grade 5/5", "Grade 4/5", "Grade 3/5", "Grade 0-2/5"])
            reflexes = st.selectbox("Reflexes", ["Normoreflexia (++ )", "Hyperreflexia (+++ ) [UMN]", "Hyporeflexia (+/0) [LMN]"])
            plantar_response = st.selectbox("Plantar Reflex", ["Flexor (Normal)", "Extensor (Upgoing - UMN sign)"])
            meningeal_signs = st.selectbox("Meningeal Irritation", ["Absent", "Neck Stiffness / Positive Kernig's"])

    elif unit == "Cardiology":
        with st.expander("2. Systemic Examination (Cardiovascular)", expanded=True):
            pulse_rhythm = st.selectbox("Pulse Rhythm", ["Regular", "Irregularly Irregular (AFib)"])
            jvp_status = st.selectbox("JVP", ["Not elevated", "Elevated"])
            apex_loc = st.selectbox("Apex Beat", ["5th ICS Normal", "Displaced laterally"])
            heart_sounds = st.selectbox("Heart Sounds", ["S1 and S2 normal", "S3 Gallop present"])
            murmur = st.selectbox("Murmurs", ["None", "Pansystolic", "Ejection systolic", "Diastolic"])

    elif unit == "Gastroenterology":
        with st.expander("2. Systemic Examination (Abdomen/GI)", expanded=True):
            gi_inspection = st.multiselect("Inspection", ["Flat/Scaphoid", "Distension", "Caput Medusae"])
            gi_palpation = st.selectbox("Palpation", ["Soft, non-tender", "Epigastric tenderness", "Guarding/Rebound"])
            gi_organomegaly = st.selectbox("Organomegaly", ["None", "Hepatomegaly", "Splenomegaly", "Hepatosplenomegaly"])
            gi_percussion = st.selectbox("Percussion", ["Normal tympany", "Shifting dullness (Ascites)"])

    elif unit == "Respiratory":
        with st.expander("2. Systemic Examination (Respiratory)", expanded=True):
            inspection = st.multiselect("Inspection (Chest)", ["Normal contour", "Barrel chest", "Asymmetrical movement"])
            palpation = st.selectbox("Trachea Position", ["Central", "Deviated to Left", "Deviated to Right"])
            percussion = st.selectbox("Percussion Note", ["Resonant (Normal)", "Hyper-resonant", "Dull (Consolidation)", "Stony Dull (Effusion)"])
            auscultation = st.selectbox("Breath Sounds", ["Vesicular (Normal)", "Bronchial", "Diminished", "Absent"])
            added_sounds = st.multiselect("Added Sounds", ["None", "Fine Crepitations", "Coarse Crepitations", "Wheeze", "Pleural Rub"])
            
    elif unit == "Nephrology":
        with st.expander("2. Systemic Examination (Renal/Genitourinary)", expanded=True):
            renal_inspection = st.multiselect("Inspection", ["Normal", "AV Fistula mark", "Asterixis (Flapping tremor)"])
            renal_palpation = st.selectbox("Palpation", ["Non-tender, kidneys not ballotable", "Kidney(s) ballotable", "Costovertebral angle (CVA) tenderness", "Palpable bladder"])
            renal_auscultation = st.selectbox("Auscultation", ["No bruits", "Renal artery bruit present"])
            fluid_status = st.selectbox("Overall Fluid Status Assessment", ["Euvolemic", "Fluid Overload (Hypervolemic)", "Dehydrated (Hypovolemic)"])

    elif unit == "Endocrinology":
        with st.expander("2. Systemic Examination (Endocrine)", expanded=True):
            neck_inspection = st.selectbox("Neck Inspection", ["Normal", "Visible Goiter"])
            neck_palpation = st.selectbox("Neck Palpation", ["Normal", "Diffuse smooth enlargement", "Multinodular", "Hard fixed mass"])
            eye_signs = st.selectbox("Eye Signs", ["Normal", "Exophthalmos / Proptosis", "Lid lag"])
            skin_signs = st.selectbox("Skin/Hair", ["Normal", "Warm & Moist", "Dry & Coarse", "Acanthosis Nigricans"])
            tremor = st.selectbox("Tremors", ["Absent", "Fine tremor", "Flapping tremor"])

# ==========================================
# TAB 3: CASE FORMULATION & DISCUSSION
# ==========================================
with tab_dx:
    st.markdown("### Case Formulation & Discussion")
    
    if st.button("Generate Clinical Presentation"):
        
        sys_str = "Associated systemic symptoms include " + ", ".join(systemic).lower() if systemic else "There are no associated systemic symptoms."
        pmh_str = ", ".join(pmh_list) if pmh_list and "None" not in pmh_list else "no known chronic illnesses"
        
        # Format Social & Sexual History properly
        soc_str = f"The patient is a {smoking.lower()}."
        if smoking in ["Current Smoker", "Ex-smoker"]: soc_str = f"The patient is a {smoking.lower()} ({pack_years:.1f} pack-years)."
        if alcohol != "None": soc_str += f" Alcohol intake is {alcohol.lower()} ({bottles_per_week} bottles/week of {alcohol_type})."
        if sex_active == "Yes": soc_str += f" Sexually active with {partners} partners, {protection.lower()} barrier use. STI history: {sti_hx.lower()}."

        # Compile ROS, replacing "Other" with actual typed values safely
        all_ros = []
        def parse_ros(ros_list, other_val, name):
            if ros_list and "None" not in ros_list:
                clean_list = [item for item in ros_list if item != "Other"]
                if "Other" in ros_list and other_val: clean_list.append(other_val)
                if clean_list: all_ros.append(f"{name}: " + ", ".join(clean_list))
                
        parse_ros(ros_haem, r_haem_o if "Other" in ros_haem else "", "Haem")
        parse_ros(ros_cv, r_cv_o if "Other" in ros_cv else "", "CV")
        parse_ros(ros_gi, r_gi_o if "Other" in ros_gi else "", "GI")
        parse_ros(ros_gu, r_gu_o if "Other" in ros_gu else "", "GU")
        parse_ros(ros_neuro, r_neuro_o if "Other" in ros_neuro else "", "Neuro")
        parse_ros(ros_msk, r_msk_o if "Other" in ros_msk else "", "MSK")
        parse_ros(ros_endo, r_endo_o if "Other" in ros_endo else "", "Endo")
        
        ros_final_str = " \n- ".join(all_ros) if all_ros else "unremarkable across major systems."

        piccel_pos = [p for p in [f"{pallor.lower()} pallor" if pallor != "Absent" else "", "jaundice" if icterus != "Absent" else "", f"{lymph.lower()} lymphadenopathy" if lymph != "Absent" else ""] if p]
        piccel_str = ", ".join(piccel_pos) if piccel_pos else "no pallor, jaundice, cyanosis, clubbing, pedal edema, or lymphadenopathy"
        
        # --- PRESENTATION OUTPUT ---
        st.markdown("#### Senior Registrar Ward Round Presentation")
        
        presentation = f"**Good morning Sir/Ma, I present {name}, a {age}-year-old {marital} {sex}, who works as a {occupation if occupation != 'Other' else occ_other}.**\n\n"
        presentation += "**History of Presenting Complaint (HPC):**\n"
        for narrative in hpc_narratives: presentation += f"- {narrative}\n"
        presentation += f"\n{sys_str}\n\n"
        presentation += f"**Background History:**\nKnown history of {pmh_str}. {soc_str} Family history notable for {', '.join(fhx).lower() if fhx and 'None' not in fhx else 'nil significant'}. Medications: {compliance.lower()}.\n\n"
        presentation += f"**Review of Systems (ROS):**\nPositive for:\n- {ros_final_str}\n\n"
        presentation += f"**Objective Findings (O/E):**\nPatient was comfortable, with {piccel_str}. Vitals: T={temp}°C, HR={hr}bpm, BP={bp_sys}/{bp_dia}mmHg.\n"
        
        if unit == "Haematology": presentation += f"**Haematological Exam:** Peripheral signs: {', '.join(haem_signs).lower()}. Lymph nodes: {haem_lymph.lower()}. Spleen: {haem_spleen.lower()}.\n\n"
        elif unit == "Neurology": presentation += f"**Neurological Exam:** GCS {gcs_score}/15. Cranial nerves: {cranial_nerves.lower()}. Motor: {motor_tone.lower()}, power {motor_power.lower()}, {reflexes.lower()}. Plantars: {plantar_response.lower()}.\n\n"
        elif unit == "Cardiology": presentation += f"**Cardiovascular Exam:** Pulse {hr}bpm, {pulse_rhythm.lower()}. JVP {jvp_status.lower()}. Apex beat {apex_loc.lower()}. Auscultation: {heart_sounds.lower()}, {murmur.lower()}.\n\n"
        elif unit == "Respiratory": presentation += f"**Respiratory Exam:** Trachea {palpation.lower()}. Percussion {percussion.lower()}. Auscultation: {auscultation.lower()} with {', '.join(added_sounds).lower()}.\n\n"
        elif unit == "Gastroenterology": presentation += f"**Abdominal Exam:** Palpation {gi_palpation.lower()}, {gi_organomegaly.lower()}. Percussion {gi_percussion.lower()}.\n\n"
        elif unit == "Nephrology": presentation += f"**Renal Exam:** Palpation {renal_palpation.lower()}. Auscultation {renal_auscultation.lower()}. Fluid status: {fluid_status.lower()}.\n\n"
        elif unit == "Endocrinology": presentation += f"**Endocrine Exam:** Neck {neck_palpation.lower()}. Eyes {eye_signs.lower()}. Tremor {tremor.lower()}.\n\n"
            
        st.info(presentation)
        
        # --- CLINICAL REASONING & DISCUSSION ---
        st.write("---")
        st.markdown("#### Clinical Evaluation & Case Discussion")
        
        clinical_diffs = []
        
        # MASTER LOGIC EVALUATOR
        if flag_scd_crisis or "Sickle Cell Disease" in pmh_list:
            clinical_diffs.append({"title": "Sickle Cell Disease (Vaso-occlusive Crisis)", "supports": "Bone pain, known SCD.", "negates": "Absence of triggers.", "clinical_pearl": "Vaso-occlusive crises are triggered by hypoxia, dehydration, infection (malaria), or cold. Look for chronic stigmata like gnathopathy and leg ulcers."})
        if flag_lymphoma or ("Drenching Night Sweats" in systemic) or haem_lymph == "Discrete, rubbery, painless nodes":
            clinical_diffs.append({"title": "🚨 Lymphoma (Hodgkin / Non-Hodgkin)", "supports": "Painless rubbery nodes, B-Symptoms.", "negates": "Requires Excisional Biopsy.", "clinical_pearl": "Painless, rubbery lymphadenopathy associated with 'B-Symptoms' (fever, drenching night sweats, and weight loss) is highly suspicious."})
        if flag_stroke or "Extensor (Upgoing - UMN sign)" in plantar_response or bp_sys > 160:
            clinical_diffs.append({"title": "Cerebrovascular Accident (Stroke)", "supports": "Sudden focal deficit, UMN signs, HTN.", "negates": "Gradual onset.", "clinical_pearl": "Differentiate ischemic from hemorrhagic via non-contrast CT."})
        if flag_seizure or "Epilepsy" in pmh_list:
            clinical_diffs.append({"title": "Seizure Disorder", "supports": "Convulsions, tongue biting.", "negates": "Lack of post-ictal confusion suggests syncope.", "clinical_pearl": "Post-ictal state is the golden differentiator."})
        if flag_ischemic_pain or bp_sys > 160:
            clinical_diffs.append({"title": "Acute Coronary Syndrome / HTN Crisis", "supports": "Chest pain, elevated BP.", "negates": "N/A", "clinical_pearl": "Urgent ECG and Troponin required to rule out MI."})
        if flag_heart_failure or "Elevated" in jvp_status:
            clinical_diffs.append({"title": "Heart Failure", "supports": "Orthopnea, elevated JVP.", "negates": "Normal fluid status.", "clinical_pearl": "Assess for left vs right-sided failure."})
        if flag_chronic_cough or flag_hemoptysis:
            clinical_diffs.append({"title": "Pulmonary Tuberculosis (PTB) / Malignancy", "supports": "Chronic cough, hemoptysis.", "negates": "Clear chest x-ray.", "clinical_pearl": "Sputum AFB/GeneXpert is mandatory in endemic areas."})
        if flag_obstruction or gi_auscultation == "Tinkling sounds":
            clinical_diffs.append({"title": "🚨 Intestinal Obstruction", "supports": "Colicky pain, vomiting, tinkling bowel sounds.", "negates": "Passing flatus.", "clinical_pearl": "A surgical emergency requiring drip and suck."})
        if flag_renal_colic or flag_hematuria:
            clinical_diffs.append({"title": "Nephrolithiasis / Malignancy", "supports": "Colicky loin pain, hematuria.", "negates": "Painless presentation points to malignancy.", "clinical_pearl": "Painless frank hematuria in an adult >50 years is malignancy until proven otherwise."})
        if flag_polyuria or "Diabetes Mellitus" in pmh_list:
            clinical_diffs.append({"title": "Diabetes Mellitus", "supports": "Polyuria, known history.", "negates": "Requires FBG/HbA1c.", "clinical_pearl": "Check for end-organ damage (retinopathy, neuropathy, nephropathy)."})

        # Render Case Discussion
        if clinical_diffs:
            for idx, diff in enumerate(clinical_diffs):
                with st.expander(f"**{idx+1}. {diff['title']}**", expanded=True):
                    st.markdown(f"**What Supports This:** {diff['supports']}")
                    st.markdown(f"**What Negates/Is Missing:** {diff['negates']}")
                    st.success(f"**Clinical Pearl:** {diff['clinical_pearl']}")
        else:
            st.warning("Input more specific pathological findings to trigger clinical evaluation.")

        # --- CASE SUMMARY ---
        st.write("---")
        st.markdown("#### Clinical Evaluation Summary")
        top_diff = clinical_diffs[0]['title'] if clinical_diffs else "an underlying pathology"
        complaints_str = ", ".join(complaint_names_for_summary) if complaint_names_for_summary else "systemic complaints"
        
        summary_paragraph = f"**In summary**, we have a {age}-year-old {sex} presenting primarily with {complaints_str}, on a background of {pmh_str}. "
        summary_paragraph += f"Examination is significant for {piccel_str}. "
        summary_paragraph += f"Based on this structured clinical picture, the leading differential to investigate further is **{top_diff}**. Clinical correlation and definitive investigations are required."
        
        st.info(summary_paragraph)
