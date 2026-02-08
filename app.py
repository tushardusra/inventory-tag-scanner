import streamlit as st
import easyocr
import pandas as pd
from PIL import Image
import numpy as np
import io
from datetime import datetime

st.set_page_config(page_title="Inventory Tag Scanner", page_icon="📦", layout="wide")

st.title("📦 Inventory Tag OCR Scanner")
st.markdown("Extract inventory tag details automatically using AI!")
st.markdown("---")

# Initialize session state
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = []

@st.cache_resource
def load_ocr_model():
    """Load EasyOCR model"""
    return easyocr.Reader(['en'])

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        image_np = np.array(image)
        reader = load_ocr_model()
        results = reader.readtext(image_np)
        extracted_text = "\n".join([text[1] for text in results])
        return extracted_text
    except Exception as e:
        st.error(f"Error during OCR: {str(e)}")
        return None

def parse_inventory_tag(ocr_text):
    """Parse OCR text to extract inventory tag fields"""
    lines = ocr_text.split('\n')
    
    extracted = {
        'Book No.': '',
        'Tag Sr No.': '',
        'Material No.': '',
        'Quantity': '',
        'Mat. Location': '',
        'Confidence': 'Low'
    }
    
    try:
        # Extract Book No. (usually 4 digits after "Book No.")
        for i, line in enumerate(lines):
            if 'Book' in line and 'No' in line:
                for j in range(i, min(i+3, len(lines))):
                    clean_line = lines[j].replace(' ', '')
                    if clean_line.isdigit() and len(clean_line) >= 3:
                        extracted['Book No.'] = clean_line.strip()
                        break
        
        # Extract Tag Sr No.
        for i, line in enumerate(lines):
            if 'TAG' in line.upper() and 'Sr' in line:
                for j in range(i, min(i+3, len(lines))):
                    clean_line = lines[j].replace(' ', '')
                    if clean_line.isdigit() and len(clean_line) >= 4:
                        extracted['Tag Sr No.'] = clean_line.strip()
                        break
        
        # Extract Material No. (alphanumeric)
        for i, line in enumerate(lines):
            if 'MATERIAL' in line.upper() and 'No' in line:
                for j in range(i+1, min(i+3, len(lines))):
                    mat_line = lines[j].strip().replace(' ', '')
                    if len(mat_line) > 5 and any(c.isalpha() for c in mat_line):
                        extracted['Material No.'] = mat_line
                        break
        
        # Extract Quantity
        for i, line in enumerate(lines):
            if 'Quantity' in line:
                for j in range(i, min(i+3, len(lines))):
                    qty_line = lines[j].strip().replace(' ', '')
                    if qty_line.isdigit():
                        extracted['Quantity'] = qty_line
                        break
        
        # Extract Mat. Location
        for i, line in enumerate(lines):
            if 'Mat' in line and 'Location' in line:
                for j in range(i+1, min(i+2, len(lines))):
                    loc_line = lines[j].strip()
                    if loc_line and len(loc_line) > 2:
                        extracted['Mat. Location'] = loc_line
                        break
        
        # Check confidence
        if all([extracted['Book No.'], extracted['Tag Sr No.'], extracted['Material No.']]):
            extracted['Confidence'] = 'High'
        elif any([extracted['Book No.'], extracted['Tag Sr No.']]):
            extracted['Confidence'] = 'Medium'
        
        return extracted
    
    except Exception as e:
        st.warning(f"Error parsing data: {str(e)}")
        return extracted

# Main UI
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Select Mode", ["Single Tag", "Batch Processing"])
    
    st.markdown("---")
    st.info("""
    **How to use:**
    1. Upload a clear photo of your inventory tag
    2. The OCR will extract text automatically
    3. Review and edit extracted data if needed
    4. Export to Excel when done
    """)

# Main content
if mode == "Single Tag":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Upload Tag Image")
        uploaded_file = st.file_uploader(
            "Choose an inventory tag image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
            key='single_upload'
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Tag Image", use_column_width=True)
    
    with col2:
        st.subheader("📝 Extracted Data")
        
        if uploaded_file:
            with st.spinner("Processing image with OCR..."):
                ocr_text = extract_text_from_image(image)
            
            if ocr_text:
                st.success("✅ OCR Processing Complete!")
                
                # Parse the extracted text
                parsed_data = parse_inventory_tag(ocr_text)
                
                # Display confidence
                confidence_color = "🟢" if parsed_data['Confidence'] == 'High' else "🟡" if parsed_data['Confidence'] == 'Medium' else "🔴"
                st.metric("Confidence Level", parsed_data['Confidence'], confidence_color)
                
                # Create editable form
                st.subheader("Review & Edit")
                
                form_col1, form_col2 = st.columns(2)
                
                with form_col1:
                    book_no = st.text_input(
                        "Book No.",
                        value=parsed_data['Book No.'],
                        key='book_no_single'
                    )
                    tag_sr_no = st.text_input(
                        "Tag Sr No.",
                        value=parsed_data['Tag Sr No.'],
                        key='tag_sr_single'
                    )
                    material_no = st.text_input(
                        "Material No.",
                        value=parsed_data['Material No.'],
                        key='material_single'
                    )
                
                with form_col2:
                    quantity = st.text_input(
                        "Quantity",
                        value=parsed_data['Quantity'],
                        key='qty_single'
                    )
                    mat_location = st.text_input(
                        "Mat. Location",
                        value=parsed_data['Mat. Location'],
                        key='location_single'
                    )
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("✅ Add to List", use_container_width=True):
                        new_entry = {
                            'Book No.': book_no,
                            'Tag Sr No.': tag_sr_no,
                            'Material No.': material_no,
                            'Quantity': quantity,
                            'Mat. Location': mat_location
                        }
                        st.session_state.extracted_data.append(new_entry)
                        st.success("✅ Entry added to list!")
                        st.balloons()
                
                with col_btn2:
                    if st.button("🔄 Clear Form", use_container_width=True):
                        st.rerun()
                
                # Show raw OCR text in expander
                with st.expander("📋 Raw OCR Text"):
                    st.text_area("Extracted text:", value=ocr_text, height=200, disabled=True)

elif mode == "Batch Processing":
    st.subheader("📤 Batch Upload Multiple Tags")
    
    uploaded_files = st.file_uploader(
        "Upload multiple tag images",
        type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
        accept_multiple_files=True,
        key='batch_upload'
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} files selected for processing")
        
        if st.button("🚀 Process All Images", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {idx+1}/{len(uploaded_files)}: {uploaded_file.name}")
                
                try:
                    image = Image.open(uploaded_file)
                    ocr_text = extract_text_from_image(image)
                    
                    if ocr_text:
                        parsed_data = parse_inventory_tag(ocr_text)
                        parsed_data['Source File'] = uploaded_file.name
                        st.session_state.extracted_data.append(parsed_data)
                
                except Exception as e:
                    st.warning(f"⚠️ Error processing {uploaded_file.name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.success(f"✅ Completed! Processed {len(uploaded_files)} images")

# Display extracted data table
st.markdown("---")
st.subheader("📊 Extracted Data Summary")

if st.session_state.extracted_data:
    df = pd.DataFrame(st.session_state.extracted_data)
    
    # Display table
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Total Entries", len(st.session_state.extracted_data))
    
    with col_stat2:
        filled_entries = len([x for x in st.session_state.extracted_data if x.get('Book No.')])
        st.metric("Complete Entries", filled_entries)
    
    with col_stat3:
        st.metric("Requires Review", len(st.session_state.extracted_data) - filled_entries)
    
    # Export options
    st.subheader("💾 Export Data")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        # Excel export
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Inventory Tags', index=False)
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name=f"inventory_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col_exp2:
        # CSV export
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"inventory_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_exp3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.extracted_data = []
            st.success("✅ Data cleared!")
            st.rerun()

else:
    st.info("📷 Upload tag images to see extracted data here")